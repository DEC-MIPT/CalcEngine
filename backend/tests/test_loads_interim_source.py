import hashlib
import json
import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pytest
import yaml
from interim_fixture import write
from pydantic import BaseModel
from test_engine_foundations_shallow_r import ROUNDING, RULE

from app.core.config import INTERIM_ROOT
from app.core.exceptions import InputValidationError, ParameterSourceUnavailableError
from app.engine import foundations_shallow_loads as loads
from app.engine import foundations_shallow_r as pilot
from app.engine.registry import CalculatorRegistry
from app.parameters.interim_loader import load_interim_root
from app.parameters.interim_schemas import InterimTypeFile
from app.schemas.calculation import QuantityValue
from app.services.interim_data import (
    Profile,
    document_digest,
    effective_status,
    record_digest,
)
from app.services.interim_source import (
    LOADS_DOCUMENT,
    LOADS_FILES,
    LOADS_SUPPLEMENT,
    interim_sources,
    loads_source_digest,
)
from app.services.parameter_assembly import ParameterDataError

TODAY = date(2026, 11, 15)
PILOT_DIGEST = "446d4d36d47342f73ddfec50938520f30b2a0b1333114bf4a2d93659646f1b7e"  # pragma: allowlist secret
MODELS: dict[str, type[BaseModel]] = {pilot.NAME: pilot.Parameters, loads.NAME: loads.Parameters}
SELECTORS = {pilot.NAME: pilot.SELECTORS}


def registry() -> CalculatorRegistry:
    found = CalculatorRegistry()
    pilot.register(found, ROUNDING, RULE)
    found.register(loads.contract(ROUNDING, RULE), pilot.FoundationsShallowR())
    return found


def inputs() -> dict[str, QuantityValue]:
    values = {"b": 2, "l": 3, "d_1": 1.5, "d_b": 0, "gamma_II": 18,
              "gamma_II_prime": 18, "c_II": 10, "phi_II": 20,
              "d": 1, "h": 1, "N": 600, "Mx": 10, "My": 20, "Qx": 0, "Qy": 0}
    return {quantity.name: QuantityValue(value=values[quantity.name], unit=quantity.base_unit)
            for quantity in loads.INPUTS}


def resolve(root: Path = INTERIM_ROOT, profile: Profile = "strict") -> Any:
    found = interim_sources(registry(), root, profile, TODAY, MODELS, SELECTORS)
    return found[loads.NAME].resolve(loads.NAME, inputs())


@pytest.fixture
def copied_root(tmp_path: Path) -> Path:
    root = tmp_path / "normatives"
    shutil.copytree(INTERIM_ROOT, root)
    return root


def data(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_fixed_binding_resolves_all_typed_components_and_preserves_exact_forms() -> None:
    result = resolve()
    assert isinstance(result.parameters, loads.Parameters)
    pressure = data(INTERIM_ROOT / LOADS_FILES["pressure"])
    bound = result.method_range[0]
    assert (bound.quantity, bound.kind, bound.value, bound.inclusive) == ("d_b", "max", 2, True)
    assert result.parameters.applicability_condition.value_fraction.model_dump() == {"numerator": 1, "denominator": 6}
    assert result.parameters.diagram_cases.caption_forms_as_printed == tuple(pressure["diagram_cases"][0]["caption_forms_as_printed"])
    assert [case.condition_latex for case in result.parameters.diagram_cases.cases] == [
        case["condition_latex"] for case in pressure["diagram_cases"][0]["cases"]]
    assert all(ref.status == "unverified" and ref.provenance == "machine-extracted"
               for ref in result.parameters.p_corner.norm_refs)


def test_supplement_is_current_and_traces_only_the_signed_source_item() -> None:
    worksheet = data(Path(__file__).parents[2] / "docs/verification/foundations-pressure-from-loads/LOADS-DB-1.yaml")
    item, = worksheet["items"]
    assert item["verdict"] == "верно" and item["record"] == "d_b_cap_2m"
    assert worksheet["signature"]["by"] == item["by"] == "Akim"
    supplement = InterimTypeFile.model_validate(data(INTERIM_ROOT / LOADS_FILES["scope"]))
    record, = supplement.method_bounds
    assert len(supplement.records()) == 1
    assert record.page == int(item["page"]) == 36
    assert record.verification.by == item["by"]
    assert record.verification.at is not None
    assert record.verification.at.isoformat() == item["at"]
    assert record.verification.portion == worksheet["portion"]
    assert record.verification.comment is not None and item["shown_digest"] in record.verification.comment
    assert effective_status(record) == "human-verified"
    assert record.verification.value_digest == record_digest(record)


def test_source_aggregate_uses_canonical_fixed_constituents_and_preserves_pilot() -> None:
    documents = {doc.name: document_digest(doc) for doc in load_interim_root(INTERIM_ROOT, ())}
    assert documents[LOADS_DOCUMENT] == PILOT_DIGEST
    expected = hashlib.sha256(json.dumps({
        "format": "foundations-shallow-loads-source-v1",
        "documents": [{"name": name, "data_sha256": documents[name]} for name in sorted(documents)],
    }, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
    result = resolve()
    assert result.source.data_sha256 == expected
    assert (result.source.kind, result.source.profile) == ("interim", "strict")
    assert result.source.data_sha256 != PILOT_DIGEST
    assert loads_source_digest(dict(reversed(list(documents.items())))) == expected


@pytest.mark.parametrize("constituent", [LOADS_DOCUMENT, LOADS_SUPPLEMENT])
def test_aggregate_changes_when_either_constituent_changes(copied_root: Path, constituent: str) -> None:
    before = resolve(copied_root).source.data_sha256
    path = copied_root / constituent / "manifest.yaml"
    write(path, data(path) | {"sunset": {"date": "2099-12-31", "event": "changed test sunset"}})
    assert resolve(copied_root).source.data_sha256 != before


@pytest.mark.parametrize("documents", [{}, {LOADS_DOCUMENT: "a" * 64},
                                      {LOADS_DOCUMENT: "a" * 64, LOADS_SUPPLEMENT: "b" * 64, "other": "c" * 64}])
def test_aggregate_refuses_incomplete_or_nonallowlisted_constituents(documents: dict[str, str]) -> None:
    with pytest.raises(ParameterDataError):
        loads_source_digest(documents)


@pytest.mark.parametrize("component", list(LOADS_FILES))
def test_missing_component_fails_closed(copied_root: Path, component: str) -> None:
    (copied_root / LOADS_FILES[component]).unlink()
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root)


@pytest.mark.parametrize("component", list(LOADS_FILES))
def test_a_component_in_another_directory_does_not_satisfy_the_alias(copied_root: Path, component: str) -> None:
    path = copied_root / LOADS_FILES[component]
    other = copied_root / "other"
    other.mkdir()
    shutil.copy(path.parent / "manifest.yaml", other / "manifest.yaml")
    path.rename(other / path.name)
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root)


@pytest.mark.parametrize(("component", "list_name"), [("resistance", "formulas"), ("pressure", "formulas"),
                                                      ("pressure", "applicability_conditions"),
                                                      ("pressure", "diagram_cases"), ("scope", "method_bounds")])
def test_strict_requires_every_constituent_record_but_draft_may_use_pending(
    copied_root: Path, component: str, list_name: str,
) -> None:
    path = copied_root / LOADS_FILES[component]
    content = data(path)
    content[list_name][0]["verification"] = {"status": "pending"}
    write(path, content)
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root)
    assert resolve(copied_root, "draft").source.profile == "draft"


@pytest.mark.parametrize("list_name", ["applicability_conditions", "diagram_cases"])
def test_missing_required_extended_record_fails_closed(copied_root: Path, list_name: str) -> None:
    path = copied_root / LOADS_FILES["pressure"]
    write(path, data(path) | {list_name: []})
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root, "draft")


@pytest.mark.parametrize(("list_name", "change"), [
    ("applicability_conditions", {"parameter": "unsupported"}),
    ("applicability_conditions", {"relation": "lt"}),
    ("diagram_cases", {"parameter": "unsupported"}),
    ("diagram_cases", {"units": {"e": "m"}}),
])
def test_unsupported_extended_binding_fails_closed(copied_root: Path, list_name: str, change: dict[str, Any]) -> None:
    path = copied_root / LOADS_FILES["pressure"]
    content = data(path)
    content[list_name][0].update(change)
    write(path, content)
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root, "draft")


@pytest.mark.parametrize("change", [{"inclusive": False}, {"quantity": "h"}, {"kind": "min"}, {"unit": "cm"}])
def test_unsupported_supplement_bound_fails_closed(copied_root: Path, change: dict[str, Any]) -> None:
    path = copied_root / LOADS_FILES["scope"]
    content = data(path)
    content["method_bounds"][0].update(change)
    write(path, content)
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root, "draft")


def test_invalid_engineering_range_is_rejected_before_table_selection() -> None:
    source = interim_sources(registry(), INTERIM_ROOT, "strict", TODAY, MODELS, SELECTORS)[loads.NAME]
    with pytest.raises(InputValidationError):
        source.resolve(loads.NAME, inputs() | {"phi_II": QuantityValue(value=46, unit="deg")})


@pytest.mark.parametrize("component", ["resistance", "pressure"])
def test_extended_resistance_or_pressure_global_bound_cannot_bypass_the_reviewed_binding(
    copied_root: Path, component: str,
) -> None:
    path = copied_root / LOADS_FILES[component]
    content = data(path)
    if component == "resistance":
        content["applicability_conditions"] = data(copied_root / LOADS_FILES["pressure"])["applicability_conditions"]
    else:
        content["method_bounds"] = data(copied_root / LOADS_FILES["scope"])["method_bounds"]
    write(path, content)
    with pytest.raises(ParameterSourceUnavailableError):
        resolve(copied_root, "draft")


@pytest.mark.parametrize("with_replacement", [False, True])
def test_rejected_constituent_is_never_used_and_a_live_replacement_can_resolve(
    copied_root: Path, with_replacement: bool,
) -> None:
    path = copied_root / LOADS_FILES["scope"]
    content = data(path)
    rejected = content["method_bounds"][0] | {
        "verification": {"status": "rejected", "by": "Akim", "at": "2026-11-08", "comment": "synthetic rejection"}}
    content["method_bounds"] = [rejected, *content["method_bounds"]] if with_replacement else [rejected]
    write(path, content)
    if with_replacement:
        assert resolve(copied_root).method_range[0].value == 2
    else:
        with pytest.raises(ParameterSourceUnavailableError):
            resolve(copied_root, "draft")
