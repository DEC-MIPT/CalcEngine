import logging
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from catalog_fixture import PILOT
from interim_fixture import PENDING, from_catalog, manifest, rejected, verified, write
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from test_engine_foundations_shallow_r import ROUNDING, RULE, inputs

from app.core.exceptions import ParameterSourceUnavailableError
from app.engine import foundations_shallow_r as pilot
from app.engine.registry import CalculatorRegistry
from app.models.calculation_result import CalculationResultRow
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.calculation import CalculationRequest
from app.schemas.normatives import CatalogSnapshot
from app.services.calculation import CalculationService
from app.services.interim_data import Profile
from app.services.interim_source import interim_sources

COPY = "synthetic_pilot_copy"
"""Второй синтетический тип с калькулятором пилота: показывает, что другие типы считаются."""

TODAY = date(2026, 10, 21)
MODELS = {PILOT: pilot.Parameters, COPY: pilot.Parameters}
SELECTORS = {PILOT: pilot.SELECTORS, COPY: pilot.SELECTORS}


def registry() -> CalculatorRegistry:
    found = CalculatorRegistry()
    contract = pilot.contract(ROUNDING, RULE)
    found.register(contract, pilot.FoundationsShallowR())
    found.register(contract.model_copy(update={"name": COPY}), pilot.FoundationsShallowR())
    return found


def sources(root: Path, files: dict[str, dict[str, Any]], profile: Profile = "strict") -> Any:
    write(root / "doc" / "manifest.yaml", manifest())
    for calculation_type, data in files.items():
        write(root / "doc" / f"{calculation_type}.yaml", data)
    return interim_sources(registry(), root, profile, TODAY, MODELS, SELECTORS)


def with_record(data: dict[str, Any], list_name: str, index: int, record: dict[str, Any]) -> dict[str, Any]:
    changed = list(data[list_name])
    changed[index] = record
    return data | {list_name: changed}


def pending(record: dict[str, Any]) -> dict[str, Any]:
    return record | {"verification": PENDING}


def index_of(data: dict[str, Any], list_name: str, **match: Any) -> int:
    return next(index for index, record in enumerate(data[list_name]) if all(record.get(k) == v for k, v in match.items()))


def messages(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.name == "app.services.interim_source"]


def test_every_type_with_a_file_gets_the_interim_source_with_its_digest_and_profile(tmp_path: Path) -> None:
    found = sources(tmp_path, {PILOT: from_catalog(PILOT)})

    resolved = found[PILOT].resolve(PILOT, inputs())

    assert set(found) == {PILOT}
    assert isinstance(resolved.parameters, pilot.Parameters)
    assert resolved.source is not None
    assert (resolved.source.kind, resolved.source.profile) == ("interim", "strict")
    assert resolved.source.data_sha256 is not None and len(resolved.source.data_sha256) == 64


def test_a_file_of_a_type_without_a_parameter_model_gets_no_source(tmp_path: Path) -> None:
    write(tmp_path / "doc" / "manifest.yaml", manifest())
    write(tmp_path / "doc" / f"{COPY}.yaml", from_catalog(PILOT))

    assert interim_sources(registry(), tmp_path, "strict", TODAY, {PILOT: pilot.Parameters}, SELECTORS) == {}


def test_strict_refuses_a_parameter_with_only_pending_records_and_other_types_still_compute(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "formulas", parameter="r")
    found = sources(tmp_path, {PILOT: with_record(data, "formulas", index, pending(data["formulas"][index])), COPY: from_catalog(PILOT)})

    with caplog.at_level(logging.WARNING), pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())

    assert messages(caplog) == [f"code=interim_parameter_unusable type={PILOT} profile=strict parameter=r"]
    assert isinstance(found[COPY].resolve(COPY, inputs()).parameters, pilot.Parameters)


def test_strict_refuses_a_parameter_with_only_rejected_records(tmp_path: Path) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "thresholds", parameter="k_z_threshold")
    found = sources(tmp_path, {PILOT: with_record(data, "thresholds", index, rejected(data["thresholds"][index]))}, "draft")

    with pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())


def test_a_pending_table_row_under_strict_refuses_the_type_instead_of_missing_the_row(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "table_values", parameter="m_q", heading_value=10.0)
    found = sources(tmp_path, {PILOT: with_record(data, "table_values", index, pending(data["table_values"][index]))})

    with caplog.at_level(logging.WARNING), pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())

    assert messages(caplog) == [f"code=interim_parameter_unusable type={PILOT} profile=strict parameter=m_q"]


def test_a_pending_bound_under_strict_refuses_the_type_instead_of_widening_the_range(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "method_bounds", quantity="phi_II", kind="max")
    found = sources(tmp_path, {PILOT: with_record(data, "method_bounds", index, pending(data["method_bounds"][index]))})

    with caplog.at_level(logging.WARNING), pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())

    assert messages(caplog) == [f"code=interim_parameter_unusable type={PILOT} profile=strict parameter=phi_II/max"]


def test_a_corrected_record_next_to_a_rejected_one_replaces_it(tmp_path: Path) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "table_values", parameter="m_q", heading_value=20.0)
    wrong = rejected(data["table_values"][index] | {"value": 99.0})
    found = sources(tmp_path, {PILOT: data | {"table_values": [*data["table_values"], wrong]}})

    selected: Any = found[PILOT].resolve(PILOT, inputs()).parameters

    assert selected.m_q.value.value == 5.0


def test_draft_uses_pending_records_and_marks_the_profile(tmp_path: Path) -> None:
    found = sources(tmp_path, {PILOT: from_catalog(PILOT, checked=False)}, "draft")

    resolved = found[PILOT].resolve(PILOT, inputs())

    assert resolved.source is not None
    assert (resolved.source.kind, resolved.source.profile) == ("interim", "draft")
    selected: Any = resolved.parameters
    assert all(reference.status == "unverified" for reference in selected.r.norm_refs)


def test_draft_never_uses_a_rejected_record(tmp_path: Path) -> None:
    data = from_catalog(PILOT, checked=False)
    index = index_of(data, "checks", parameter="check_norm_refs")
    found = sources(tmp_path, {PILOT: with_record(data, "checks", index, rejected(data["checks"][index]))}, "draft")

    with pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())


def test_a_record_that_breaks_the_contract_refuses_the_type_naming_the_parameter(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "thresholds", parameter="k_z_threshold")
    broken = verified(data["thresholds"][index] | {"unit": "<NOT-A-UNIT>"}, "thresholds")
    found = sources(tmp_path, {PILOT: with_record(data, "thresholds", index, broken)})

    with caplog.at_level(logging.WARNING), pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())

    assert messages(caplog) == [f"code=interim_data_invalid type={PILOT} parameter=k_z_threshold"]


def test_a_breach_without_a_parameter_is_named_by_its_type(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "method_bounds", quantity="b", kind="max")
    broken = verified(data["method_bounds"][index] | {"quantity": "<NOT-AN-INPUT>"}, "method_bounds")
    found = sources(tmp_path, {PILOT: with_record(data, "method_bounds", index, broken)})

    with caplog.at_level(logging.WARNING), pytest.raises(ParameterSourceUnavailableError):
        found[PILOT].resolve(PILOT, inputs())

    assert messages(caplog) == [f"code=interim_data_invalid type={PILOT}"]


def test_an_input_outside_the_range_gives_a_snapshot_with_the_interim_source(tmp_path: Path) -> None:
    found = sources(tmp_path, {PILOT: from_catalog(PILOT)})

    resolved = found[PILOT].resolve(PILOT, inputs() | {"phi_II": inputs()["phi_II"].model_copy(update={"value": 40.0})})

    assert isinstance(resolved.parameters, CatalogSnapshot)
    assert resolved.source is not None and resolved.source.kind == "interim"


def test_references_of_verified_records_are_not_raised(tmp_path: Path, sqlite_session: Session) -> None:
    found = sources(tmp_path, {PILOT: from_catalog(PILOT)})
    service = CalculationService(registry(), sources=found, results=CalculationResultRepository(sqlite_session))

    envelope = service.submit(CalculationRequest(calculation_type=PILOT, inputs=inputs()))

    references = list(envelope.norm_refs)
    for step in envelope.trace:
        assert step.kind != "engineer_formula"
        references.extend(step.norm_refs)
    assert references
    assert {(reference.status, reference.provenance) for reference in references} == {("unverified", "machine-extracted")}


def test_strict_refusal_runs_no_engine_and_stores_nothing(
    tmp_path: Path, sqlite_session: Session, engine_calls: list[str]
) -> None:
    data = from_catalog(PILOT)
    index = index_of(data, "formulas", parameter="r")
    found = sources(tmp_path, {PILOT: with_record(data, "formulas", index, pending(data["formulas"][index]))})
    results = CalculationResultRepository(sqlite_session)
    service = CalculationService(registry(), sources=found, results=results)

    with pytest.raises(ParameterSourceUnavailableError):
        service.submit(CalculationRequest(calculation_type=PILOT, inputs=inputs()))

    assert engine_calls == []
    assert sqlite_session.scalar(select(func.count()).select_from(CalculationResultRow)) == 0
