import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest
from pydantic import TypeAdapter
from sqlalchemy.orm import Session
from test_engine_foundations_shallow_r import REF, ROUNDING, RULE, inputs, parameters
from test_engine_modules import engineer_step
from test_reporting_docx import read_back
from test_reporting_model import REQUEST

import app.services.calculation as calculation_service_module
from app.core.exceptions import CalculationError, DECError
from app.engine import foundations_shallow_r as pilot
from app.engine.boundary import run as run_legacy_boundary
from app.engine.legacy_module import LegacyOptions, LegacyQuantityModule
from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.calculation import (
    BoundViolation,
    CalculationResult,
    MethodBound,
    QuantityValue,
    ResultEnvelope,
)
from app.schemas.module import ModuleDiagnostic, ModuleExecution, ModuleOutcome
from app.schemas.normatives import CatalogSnapshot
from app.services.calculation import CalculationService, norm_sources

GOLDEN = json.loads((Path(__file__).parent / "fixtures" / "pilot_envelope_before_metadata.json").read_text())


@pytest.mark.parametrize("case", sorted(GOLDEN))
def test_existing_golden_result_runs_through_the_common_executor(case: str, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.engine import pipeline

    calls = []
    execute = pipeline.execute_module

    def observe(module: Any, *args: Any, **kwargs: Any) -> Any:
        calls.append(module.metadata.identifier)
        return execute(module, *args, **kwargs)

    monkeypatch.setattr(pipeline, "execute_module", observe)
    recorded = GOLDEN[case]
    given = {name: QuantityValue(**value) for name, value in recorded["inputs"].items()}
    result = calculate(pilot.contract(ROUNDING, RULE), pilot.FoundationsShallowR(), given, parameters())

    assert result.model_dump(mode="json") == recorded["result"]
    assert calls == [pilot.NAME]


@pytest.mark.parametrize("case", sorted(GOLDEN))
def test_historical_saved_result_reads_and_renders_without_calculation(
    case: str, sqlite_session: Session, monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded = GOLDEN[case]
    result_id = UUID("00000000-0000-0000-0000-000000000001")
    envelope = ResultEnvelope.model_validate(recorded["result"] | {"result_id": result_id})
    repository = CalculationResultRepository(sqlite_session)
    repository.add(
        result_id=result_id, calculation_type=pilot.NAME,
        engine_version=envelope.engine_version, input_hash=envelope.input_hash,
        inputs=recorded["inputs"], envelope=envelope.model_dump(mode="json"), norm_sources=norm_sources(envelope),
    )
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)

    def no_calculation(*args: Any, **kwargs: Any) -> Any:
        pytest.fail("historical result was recomputed")

    monkeypatch.setattr(calculation_service_module, "calculate", no_calculation)
    monkeypatch.setattr(pilot.FoundationsShallowR, "calculate", no_calculation)
    service = CalculationService(registry, results=repository)
    before = service.get(result_id)
    paragraphs, rows = read_back(service.report(result_id, REQUEST))

    assert before.envelope == envelope
    assert service.get(result_id) == before
    assert CalculationResult.model_validate(recorded["result"]).input_hash == envelope.input_hash
    assert "2 Расчёт" in paragraphs
    assert "3 Заключение" in paragraphs
    assert rows


def test_legacy_registry_exposes_a_typed_module_and_rejects_unknown_names() -> None:
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)

    assert registry.module(pilot.NAME).metadata.identity_policy == "legacy"
    assert registry.module(pilot.NAME).data_schema.validate_python(parameters()) == parameters()
    with pytest.raises(DECError):
        registry.module("unknown")


def test_legacy_adapter_rejects_a_diagnostic_that_disagrees_with_applicability() -> None:
    module = LegacyQuantityModule(pilot.contract(ROUNDING, RULE), pilot.FoundationsShallowR(), TypeAdapter(pilot.Parameters))
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))
    details = BoundViolation(value=QuantityValue(value=2.0, unit="m"), bound=bound)
    diagnostic = ModuleDiagnostic(code="method_bound", source=(REF,), details=details)

    with pytest.raises(CalculationError, match="diagnostic"):
        module.validate_diagnostic(diagnostic, (), inputs(), parameters(), LegacyOptions())


def test_legacy_adapter_never_exposes_internal_engineer_steps() -> None:
    module = LegacyQuantityModule(pilot.contract(ROUNDING, RULE), pilot.FoundationsShallowR(), TypeAdapter(pilot.Parameters))
    execution: ModuleExecution[Mapping[str, QuantityValue], BoundViolation] = ModuleExecution(
        metadata=module.metadata, input_hash="0" * 64,
        outcome=ModuleOutcome(execution="completed", applicability="applicable", outputs={"R": QuantityValue(value=1.0, unit="kPa")}, trace=(engineer_step(),)),
    )

    with pytest.raises(CalculationError, match="engineer_formula"):
        module.adapt_result(execution)


def test_catalog_snapshot_refusal_keeps_legacy_hash_without_running_calculator(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)
    snapshot = CatalogSnapshot(formulas={}, table_rows=(), thresholds={}, checks={})
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    def no_calculation(*args: Any, **kwargs: Any) -> Any:
        pytest.fail("snapshot reached numerical calculation")

    monkeypatch.setattr(pilot.FoundationsShallowR, "calculate", no_calculation)
    calculator: Any = registry.get(pilot.NAME)
    expected = run_legacy_boundary(registry.contract(pilot.NAME), calculator, inputs(), snapshot, method_range=(bound,))
    result = calculate(
        registry.contract(pilot.NAME), calculator, inputs(), snapshot,
        method_range=(bound,), module=registry.module(pilot.NAME),
    )

    assert result.verdict == "refused"
    assert result.trace == result.outputs == ()
    assert result.input_hash == expected.input_hash


@pytest.mark.parametrize("invalid", [False, True])
def test_snapshot_parameters_are_rejected_in_range_or_when_malformed(invalid: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)
    snapshot = CatalogSnapshot(formulas={}, table_rows=(), thresholds={}, checks={})
    if invalid:
        snapshot = snapshot.model_copy(update={"checks": {"bad": ()}})
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    def no_calculation(*args: Any, **kwargs: Any) -> Any:
        pytest.fail("invalid snapshot reached numerical calculation")

    monkeypatch.setattr(pilot.FoundationsShallowR, "calculate", no_calculation)
    with pytest.raises(CalculationError):
        calculate(
            registry.contract(pilot.NAME), registry.get(pilot.NAME), inputs(), snapshot,
            method_range=(bound,) if invalid else (), module=registry.module(pilot.NAME),
        )
