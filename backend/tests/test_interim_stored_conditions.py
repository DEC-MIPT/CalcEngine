from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any

import pytest
from interim_fixture import (
    PENDING,
    VERIFIER,
    formula,
    from_catalog,
    manifest,
    type_file,
    write,
)
from pydantic import ValidationError
from test_engine_foundations_shallow_r import inputs
from test_interim_source import COPY, PILOT, messages, sources

from app.core.config import INTERIM_ROOT
from app.core.exceptions import (
    ParameterSourceUnavailableError,
    ParameterValidationError,
)
from app.engine.hashing import canonical_json
from app.parameters.interim_loader import load_interim_root
from app.parameters.interim_schemas import InterimRecord, InterimTypeFile
from app.services.interim_data import (
    Profile,
    check_documents,
    document_digest,
    effective_status,
    record_digest,
)

TYPE = "stored_conditions"
FUTURE_TYPE = "foundations_pressure_from_loads"
FAMILIES = ("applicability_conditions", "diagram_cases")


def condition(**changes: Any) -> dict[str, Any]:
    common = {key: value for key, value in formula().items() if key in {"norm_refs", "page", "verification"}}
    return common | {
        "parameter": "stored_rule",
        "quantity": "x/y",
        "applies_to": "formula_alpha",
        "latex": "x/y <= 2/7",
        "unit": "1",
        "relation": "le",
        "value_fraction": {"numerator": 2, "denominator": 7},
    } | changes


def diagram(**changes: Any) -> dict[str, Any]:
    common = {key: value for key, value in formula().items() if key in {"norm_refs", "page", "verification"}}
    return common | {
        "parameter": "stored_rule",
        "units": {"x": "m", "y": "m"},
        "cases": [{"figure_case": "alpha", "diagram": "synthetic", "condition_latex": "x < y/7"}],
        "caption_forms_as_printed": ["x < 1/7"],
    } | changes


def specimen(family: str, **changes: Any) -> dict[str, Any]:
    return (condition if family == FAMILIES[0] else diagram)(**changes)


def parsed(family: str, record: dict[str, Any]) -> InterimRecord:
    return InterimTypeFile.model_validate(type_file(**{family: [record]})).records()[0][1]


def documents(root: Path, **lists: Any) -> Any:
    write(root / "doc" / "manifest.yaml", manifest())
    write(root / "doc" / f"{TYPE}.yaml", type_file(**lists))
    return load_interim_root(root, {TYPE})


def test_optional_records_follow_the_five_original_lists_and_preserve_exact_content() -> None:
    data = type_file(formulas=[formula()], applicability_conditions=[condition()], diagram_cases=[diagram()])
    value = InterimTypeFile.model_validate(data)

    assert [path for path, _ in value.records()] == ["formulas[0]", "applicability_conditions[0]", "diagram_cases[0]"]
    assert value.applicability_conditions[0].value_fraction.model_dump() == {"numerator": 2, "denominator": 7}
    assert value.diagram_cases[0].cases[0].condition_latex == "x < y/7"
    assert value.diagram_cases[0].caption_forms_as_printed == ("x < 1/7",)


@pytest.mark.parametrize("field", ["numerator", "denominator"])
@pytest.mark.parametrize("value", [True, False, 2.0, "2", None])
def test_fraction_components_reject_coercion(field: str, value: object) -> None:
    record = condition()
    record["value_fraction"][field] = value
    with pytest.raises(ValidationError):
        parsed(FAMILIES[0], record)


@pytest.mark.parametrize("denominator", [0, -1])
def test_a_fraction_requires_a_positive_denominator(denominator: int) -> None:
    with pytest.raises(ValidationError):
        parsed(FAMILIES[0], condition(value_fraction={"numerator": 2, "denominator": denominator}))


@pytest.mark.parametrize("relation", ["lt", "le", "eq", "ge", "gt"])
def test_all_declared_comparison_relations_are_stored(relation: str) -> None:
    assert parsed(FAMILIES[0], condition(relation=relation)).model_dump()["relation"] == relation


def test_an_unrecognized_relation_is_rejected() -> None:
    with pytest.raises(ValidationError):
        parsed(FAMILIES[0], condition(relation="approx"))


@pytest.mark.parametrize(
    ("family", "change"),
    [
        (FAMILIES[0], {"unexpected": "text"}),
        (FAMILIES[0], {"value_fraction": {"numerator": 2, "denominator": 7, "unexpected": 1}}),
        (FAMILIES[1], {"unexpected": "text"}),
        (FAMILIES[1], {"cases": [{"figure_case": "alpha", "diagram": "synthetic", "condition_latex": "x<y", "unexpected": 1}]}),
        (FAMILIES[0], {"quantity": "x" * 65}),
        (FAMILIES[0], {"applies_to": "x" * 65}),
        (FAMILIES[0], {"latex": "x" * 501}),
        (FAMILIES[1], {"units": {"x" * 65: "m"}}),
        (FAMILIES[1], {"units": {"x": "m" * 65}}),
        (FAMILIES[1], {"cases": []}),
        (FAMILIES[1], {"caption_forms_as_printed": []}),
        (FAMILIES[1], {"caption_forms_as_printed": ["x" * 501]}),
        (FAMILIES[1], {"cases": [{"figure_case": "x" * 65, "diagram": "synthetic", "condition_latex": "x<y"}]}),
        (FAMILIES[1], {"cases": [{"figure_case": "alpha", "diagram": "x" * 65, "condition_latex": "x<y"}]}),
        (FAMILIES[1], {"cases": [{"figure_case": "alpha", "diagram": "synthetic", "condition_latex": "x" * 501}]}),
        (FAMILIES[1], {"cases": [{"figure_case": "alpha", "diagram": "synthetic", "condition_latex": "x<y", "edge_ordinate_latex": "x" * 501}]}),
    ],
)
def test_nested_extensions_reject_unknown_fields_empty_lists_and_overlong_labels(family: str, change: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        parsed(family, specimen(family, **change))


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("missing", ["norm_refs", "page", "verification"])
def test_extended_records_require_the_shared_provenance_fields(family: str, missing: str) -> None:
    record = specimen(family)
    del record[missing]
    with pytest.raises(ValidationError):
        parsed(family, record)


@pytest.mark.parametrize("explicit_empty", [False, True])
def test_optional_empty_lists_preserve_the_legacy_document_digest(tmp_path: Path, explicit_empty: bool) -> None:
    data = type_file(formulas=[formula()])
    if explicit_empty:
        data |= {family: [] for family in FAMILIES}
    (document,) = documents(tmp_path, **data)
    record = document.files[0].content.formulas[0]
    legacy_content = document.files[0].content.model_dump(mode="json", exclude=set(FAMILIES))
    legacy_contents = {"manifest.yaml": document.manifest.model_dump(mode="json"), f"{TYPE}.yaml": legacy_content}
    legacy_digest = sha256(canonical_json([
        {"path": path, "content": legacy_contents[path]} for path in sorted(legacy_contents)
    ]).encode()).hexdigest()
    assert document_digest(document) == legacy_digest
    body = record.model_dump(mode="json", exclude={"verification"})
    assert record_digest(record) == sha256(canonical_json(body).encode()).hexdigest()


@pytest.mark.parametrize("family", FAMILIES)
def test_verification_only_changes_document_digest_but_not_record_digest(tmp_path: Path, family: str) -> None:
    record = specimen(family)
    (before,) = documents(tmp_path, **{family: [record]})
    changed = record | {"verification": {"status": "pending", "comment": "synthetic note"}}
    (after,) = documents(tmp_path, **{family: [changed]})
    assert document_digest(before) != document_digest(after)
    assert record_digest(before.files[0].content.records()[0][1]) == record_digest(after.files[0].content.records()[0][1])


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("change", ["nested", "reference", "page"])
def test_extended_content_changes_both_digests(tmp_path: Path, family: str, change: str) -> None:
    record = specimen(family)
    (before,) = documents(tmp_path, **{family: [record]})
    changed = deepcopy(record)
    if change == "nested":
        if family == FAMILIES[0]:
            changed["value_fraction"]["numerator"] = 3
        else:
            changed["cases"][0]["condition_latex"] = "x <= y/7"
    elif change == "reference":
        changed["norm_refs"][0]["document"] = "<OTHER-SYNTHETIC-DOCUMENT>"
    else:
        changed["page"] = 2
    (after,) = documents(tmp_path, **{family: [changed]})
    assert document_digest(before) != document_digest(after)
    assert record_digest(before.files[0].content.records()[0][1]) != record_digest(after.files[0].content.records()[0][1])


@pytest.mark.parametrize("family", FAMILIES)
def test_extended_records_have_the_same_verifier_and_effective_status_rules(tmp_path: Path, family: str) -> None:
    record = specimen(family)
    verification = {"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "portion": "synthetic", "value_digest": record_digest(parsed(family, record))}
    checked = record | {"verification": verification}
    assert effective_status(parsed(family, checked)) == "human-verified"
    assert effective_status(parsed(family, checked | {"page": 2})) == "pending"
    bad_verifier = checked | {"verification": verification | {"by": "<UNKNOWN-VERIFIER>"}}
    with pytest.raises(ParameterValidationError, match="not a listed verifier"):
        documents(tmp_path, **{family: [bad_verifier]})


def test_strict_logs_each_new_pending_record_without_values(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    found = documents(tmp_path, applicability_conditions=[condition()], diagram_cases=[diagram()])
    caplog.clear()
    check_documents(found, "strict")
    unchecked = [r.message for r in caplog.records if "interim_record_unchecked" in r.message]
    assert unchecked == [
        f"code=interim_record_unchecked file=doc/{TYPE}.yaml record=applicability_conditions[0] status=pending",
        f"code=interim_record_unchecked file=doc/{TYPE}.yaml record=diagram_cases[0] status=pending",
    ]
    assert not any("2/7" in message or "x < y/7" in message for message in unchecked)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("profile", ["strict", "draft"])
@pytest.mark.parametrize("status", ["pending", "human-verified", "rejected"])
@pytest.mark.parametrize("parameter", ["stored_rule", "r"])
def test_registered_types_refuse_stored_conditions_before_filtering(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, family: str, profile: Profile, status: str, parameter: str
) -> None:
    record = specimen(family, parameter=parameter)
    if status == "human-verified":
        verification = {"status": status, "by": VERIFIER, "at": "2026-10-21", "portion": "synthetic", "value_digest": record_digest(parsed(family, record))}
    elif status == "rejected":
        verification = {"status": status, "by": VERIFIER, "at": "2026-10-21", "comment": "synthetic rejection"}
    else:
        verification = PENDING
    data = from_catalog(PILOT) | {family: [record | {"verification": verification}]}
    found = sources(tmp_path, {PILOT: data, COPY: from_catalog(PILOT)}, profile)
    caplog.clear()
    with pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())
    assert any(f"type={PILOT}" in message and parameter in message for message in messages(caplog))
    assert found[COPY].resolve(COPY, inputs()).parameters is not None


def test_real_future_type_is_pending_unregistered_and_keeps_exact_applicability(caplog: pytest.LogCaptureFixture) -> None:
    (document,) = load_interim_root(INTERIM_ROOT, {PILOT})
    file = next(file for file in document.files if file.calculation_type == FUTURE_TYPE)
    assert Counter(path.split("[")[0] for path, _ in file.content.records()) == {
        "formulas": 3, "table_values": 3, "applicability_conditions": 1, "diagram_cases": 1,
    }
    assert all(record.verification.status == "pending" for _, record in file.content.records())
    (rule,) = file.content.applicability_conditions
    assert rule.value_fraction.model_dump() == {"numerator": 1, "denominator": 6}
    assert rule.relation == "le"
    assert file.content.method_bounds == ()
    (figures,) = file.content.diagram_cases
    assert figures.caption_forms_as_printed == ("e<1/6", "e=1/6", "e>1/6")
    assert [case.figure_case for case in figures.cases] == ["б", "в", "г"]
    assert figures.cases[0].condition_latex == "e<l/6"
    assert figures.cases[1].edge_ordinate_latex == "p_{min}=0"
    assert any(f"interim_type_unregistered file=sp-22-13330-2016/{FUTURE_TYPE}.yaml" in r.message for r in caplog.records)
