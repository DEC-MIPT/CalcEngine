from datetime import date

import pytest
from test_loads_acceptance import EXAMPLES

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.engine import foundations_shallow_r as pilot
from app.engine.foundations_shallow_loads import NAME as LOADS
from app.engine.pipeline import calculate
from app.schemas.calculation import MethodBound, NormRef, QuantityValue
from app.services.calculation import CalculationService
from app.services.catalog import build_registry
from app.services.interim_source import interim_sources
from app.verification.invariants import determinism_holds, unit_change_holds
from app.verification.regression import CorpusEntry, freeze, run_regression
from app.verification.runner import ExampleParameters

CASES = ((pilot.NAME, "pass"), (pilot.NAME, "fail"), (LOADS, "pass"),
         (LOADS, "fail"), (LOADS, "bound"), (LOADS, "contact"))


def given(name: str, state: str) -> dict[str, QuantityValue]:
    inputs = dict(EXAMPLES[0].inputs)
    if name == pilot.NAME:
        inputs = {field.name: inputs[field.name] for field in pilot.INPUTS if field.name != "p"}
        inputs["p"] = QuantityValue(value=120 if state == "pass" else 220, unit="kPa")
    elif state == "fail":
        inputs["N"] = QuantityValue(value=1200, unit="kN")
    elif state == "bound":
        inputs["d_b"] = QuantityValue(value=3, unit="m")
    elif state == "contact":
        inputs["Mx"] = QuantityValue(value=200, unit="kN*m")
        inputs["My"] = QuantityValue(value=300, unit="kN*m")
    return inputs


def changed_units(inputs: dict[str, QuantityValue]) -> dict[str, QuantityValue]:
    alternatives = {"m": ("mm", 1000), "kPa": ("Pa", 1000), "kN/m3": ("N/m3", 1000),
                    "kN*m": ("N*m", 1000), "kN": ("N", 1000)}
    return {
        name: QuantityValue(value=value.value * alternatives[value.unit][1], unit=alternatives[value.unit][0])
        if value.unit in alternatives else value
        for name, value in inputs.items()
    }


@pytest.mark.parametrize(("name", "state"), CASES)
def test_every_registered_type_uses_common_verifiers_with_prepared_sources(name: str, state: str) -> None:
    registry = build_registry(PARAMS_ROOT)
    assert {contract.name for contract in registry.contracts()} == {case[0] for case in CASES}
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 16))[name]
    inputs = given(name, state)
    resolved = source.resolve(name, inputs)
    contract, calculator = registry.contract(name), registry.get(name)
    result = CalculationService(registry).run(name, inputs, resolved.parameters, method_range=resolved.method_range)
    expected = "refused" if state in ("bound", "contact") else state
    assert result.verdict == expected
    if expected == "pass":
        assert result.outputs[0].value == 152.02
    direct = calculate(contract, calculator, inputs, resolved.parameters, method_range=resolved.method_range)
    assert direct.model_dump() == result.model_dump(exclude={"result_id", "parameter_source"})
    assert determinism_holds(contract, calculator, inputs, resolved.parameters, resolved.method_range)
    assert unit_change_holds(contract, calculator, changed_units(inputs), resolved.parameters, resolved.method_range)
    entry = freeze(f"prepared-{name}-{state}", name, inputs, result)

    def resolve(item: CorpusEntry) -> ExampleParameters:
        parameters = source.resolve(item.calculation_type, item.inputs)
        return ExampleParameters(parameters.parameters, parameters.method_range)

    report = run_regression((entry,), registry, resolve)
    assert report.verdict == "GO"
    assert [check.outcome for check in report.checks] == ["unchanged"]
    assert report.checks[0].error is None
    assert report.checks[0].differences == ()


@pytest.mark.parametrize("name", (pilot.NAME, LOADS))
def test_common_verifiers_preserve_explicit_method_ranges_for_every_registered_type(name: str) -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 16))[name]
    inputs = given(name, "pass")
    resolved = source.resolve(name, inputs)
    contract, calculator = registry.contract(name), registry.get(name)
    synthetic_reference = NormRef(
        document="<TEST-ONLY-SYNTHETIC-RANGE>", edition="unverified", clause="unverified",
        status="unverified", provenance="machine-extracted",
    )
    bound = MethodBound(quantity="b", kind="max", value=1, inclusive=True, source=(synthetic_reference,))
    ranges = (bound,)
    result = CalculationService(registry).run(name, inputs, resolved.parameters, method_range=ranges)
    assert result.verdict == "refused"
    assert result.outputs == result.trace == ()
    assert calculate(contract, calculator, inputs, resolved.parameters, method_range=ranges).model_dump() == result.model_dump(exclude={"result_id", "parameter_source"})
    assert determinism_holds(contract, calculator, inputs, resolved.parameters, ranges)
    assert unit_change_holds(contract, calculator, changed_units(inputs), resolved.parameters, ranges)
    entry = freeze(f"bounded-{name}", name, inputs, result)
    report = run_regression((entry,), registry, lambda _: ExampleParameters(resolved.parameters, ranges))
    assert report.verdict == "GO"
    assert report.checks[0].outcome == "unchanged"
