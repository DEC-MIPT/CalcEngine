import json
from pathlib import Path
from typing import Any

import pytest
from test_engine_foundations_shallow_r import RULE
from test_loads_interim_source import resolve

from app.core.exceptions import CalculationError, InputValidationError, UnitError
from app.engine import foundations_shallow_loads as loads
from app.engine import foundations_shallow_weights as weights
from app.engine.legacy_module import LegacyOptions
from app.schemas.api import FieldError
from app.schemas.calculation import (
    CONTACT_INPUTS,
    WEIGHTS_CONTACT_INPUTS,
    CalculationRequest,
    CalculationResult,
    CheckStep,
    DerivedViolation,
    QuantityValue,
    RoundingRule,
    ValidatedBound,
)
from app.schemas.parameters import EngineerRule
from app.verification.models import ReferenceExample

FIXTURE = Path(__file__).parent / "fixtures" / "foundations_weights_references.json"
EXAMPLES = tuple(ReferenceExample.model_validate(item) for item in json.loads(FIXTURE.read_text()))


@pytest.fixture(scope="module")
def data() -> weights.Parameters:
    return resolve().parameters


@pytest.fixture
def module() -> weights.FoundationsWeightsModule:
    return weights.FoundationsWeightsModule(weights.contract(RoundingRule(decimals=2, mode="half_up"), RULE))


def given(case: int = 0, **changes: float) -> dict[str, QuantityValue]:
    original = dict(EXAMPLES[case].inputs)
    return original | {
        name: QuantityValue(value=value, unit=original[name].unit)
        for name, value in changes.items()
    }


def run(module: weights.FoundationsWeightsModule, data: weights.Parameters, case: int = 0,
        **changes: float) -> CalculationResult:
    return module.execute_public(given(case, **changes), data, LegacyOptions())


def trace_values(result: CalculationResult) -> dict[str, float]:
    return {step.step_id: step.result.value for step in result.trace}


def invalid_inputs(error: InputValidationError) -> list[str | int]:
    names: list[str | int] = []
    for field in error.fields:
        assert isinstance(field, FieldError)
        names.append(field.location[-1])
    return names


def test_reference_fixture_preserves_admitted_inputs_and_tolerance_provenance() -> None:
    assert [example.example_id for example in EXAMPLES] == ["weights-C", "weights-X", "weights-XY"]
    for example in EXAMPLES:
        assert isinstance(example, ReferenceExample)
        assert example.calculation_type == weights.NAME
        assert example.origin == "manual calculation"
        assert "Final admission" in example.citation.locator
        assert "24044046751e1024b457deef3ca4f99fb9bc8cb261e741ce43cb2f928cbe5578" in example.citation.locator  # pragma: allowlist secret
        assert len(example.inputs) == 19
        assert "d" not in example.inputs
        assert tuple(example.expected_outputs) == weights.OUTPUT_NAMES
        for expected in example.expected_outputs.values():
            assert expected.unit == "kPa"
            assert expected.tolerance == 0.005
            assert expected.tolerance_kind == "absolute"
            assert isinstance(expected.tolerance_source, EngineerRule)
            assert expected.tolerance_source.engineer == "Akim"


@pytest.mark.parametrize("case", range(3), ids=["weights-C", "weights-X", "weights-XY"])
def test_three_admitted_manual_references(module: weights.FoundationsWeightsModule,
                                         data: weights.Parameters, case: int) -> None:
    result = run(module, data, case)
    example = EXAMPLES[case]
    raw = trace_values(result)
    assert tuple(output.quantity for output in result.outputs) == tuple(example.expected_outputs)
    for output in result.outputs:
        expected = example.expected_outputs[output.quantity]
        assert output.value == pytest.approx(expected.value, abs=expected.tolerance, rel=0)
        assert raw[output.quantity] == pytest.approx(expected.value, abs=expected.tolerance, rel=0)
        assert output.unit == expected.unit
    assert raw["V"] == [720, 750, 750][case]
    assert raw["Mx_base"] == [0, 70, 70][case]
    assert raw["My_base"] == [0, 0, -60][case]
    assert raw["G_sum"] == [120, 150, 150][case]
    checks = [step for step in result.trace if isinstance(step, CheckStep)]
    assert [step.step_id for step in checks] == list(loads.CHECKS)
    assert [step.result.value for step in checks] == [[120, 120, 120, 120], [125, 160, 125, 160], [125, 160, 145, 180]][case]
    assert [step.right.value for step in checks] == pytest.approx([152.02, 182.424, 182.424, 228.03], rel=0, abs=1e-10)
    assert all(step.passed for step in checks)
    assert result.verdict == "pass"
    assert result.verdict_reason.kind == "check"
    assert result.verdict_reason.step_id == "p_corner_max_le_limit"
    assert "gamma_mt" not in raw
    assert all(sub.symbol != "d" for step in result.trace for sub in step.substitutions)


def test_new_quantity_contract_has_its_own_methodology_identity(module: weights.FoundationsWeightsModule,
                                                               data: weights.Parameters) -> None:
    assert len(module.contract.inputs) == 19
    assert tuple(item.name for item in module.contract.inputs) == tuple(weights.Inputs.model_fields)
    assert "d" not in {item.name for item in module.contract.inputs}
    assert module.metadata.identifier == "foundations_shallow_weights"
    assert module.metadata.methodology_version != loads.FoundationsLoadsModule(module.contract).metadata.methodology_version
    CalculationRequest(calculation_type=weights.NAME, inputs=given()).check_against(module.contract)
    first = run(module, data)
    assert first == run(module, data)
    assert first.input_hash != run(module, data, G_fund=61).input_hash


@pytest.mark.parametrize("moment", [0, 100])
def test_zero_vertical_resultant_is_rejected_before_calculation(module: weights.FoundationsWeightsModule,
                                                               data: weights.Parameters,
                                                               monkeypatch: pytest.MonkeyPatch,
                                                               moment: float) -> None:
    def unexpected_calculate(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("zero-resultant request reached calculation")

    monkeypatch.setattr(weights.FoundationsWeightsModule, "calculate", unexpected_calculate)
    values = given(N=0, G_fund=0, G_soil=0, G_other=0, Mx=moment)
    request = CalculationRequest(calculation_type=weights.NAME, inputs=values)
    with pytest.raises(InputValidationError) as exc:
        request.check_against(module.contract)
    assert set(invalid_inputs(exc.value)) == {"N", "G_fund", "G_soil", "G_other"}
    with pytest.raises(InputValidationError):
        module.execute_public(values, data, LegacyOptions())


def test_positive_weight_allows_zero_structural_force(module: weights.FoundationsWeightsModule,
                                                     data: weights.Parameters) -> None:
    result = run(module, data, N=0)
    assert trace_values(result)["V"] == 120
    assert all(output.value == 20 for output in result.outputs if output.quantity != "R")


@pytest.mark.parametrize("name", ["G_fund", "G_soil", "G_other"])
def test_negative_weight_rejected_with_named_field(module: weights.FoundationsWeightsModule,
                                                  data: weights.Parameters, name: str) -> None:
    values = given(**{name: -1})
    with pytest.raises(InputValidationError) as exc:
        CalculationRequest(calculation_type=weights.NAME, inputs=values).check_against(module.contract)
    assert name in invalid_inputs(exc.value)
    with pytest.raises(InputValidationError):
        module.execute_public(values, data, LegacyOptions())


@pytest.mark.parametrize("height,expected_moment,expected_min,expected_max", [(0, 50, 100, 150), (1, 70, 90, 160), (2, 90, 80, 170)])
def test_added_base_moment_is_not_transferred_twice(module: weights.FoundationsWeightsModule,
                                                  data: weights.Parameters, height: float,
                                                  expected_moment: float, expected_min: float,
                                                  expected_max: float) -> None:
    raw = trace_values(run(module, data, 1, h=height))
    assert raw["Mx_base"] == expected_moment
    assert raw["p"] == 125
    assert raw["p_x_min"] == expected_min
    assert raw["p_x_max"] == expected_max


def test_signed_cut_and_base_moments_cancel_independently(module: weights.FoundationsWeightsModule,
                                                        data: weights.Parameters) -> None:
    result = run(module, data, 1, h=2, Mx=30, Qx=-10, Mx_add_base=-10,
                 My=-20, Qy=15, My_add_base=-10)
    raw = trace_values(result)
    assert raw["Mx_base"] == raw["My_base"] == 0
    assert all(output.value == 125 for output in result.outputs if output.quantity != "R")


def test_unit_equivalence_includes_every_added_weight_and_moment(module: weights.FoundationsWeightsModule,
                                                               data: weights.Parameters) -> None:
    values = given(2)
    changed = dict(values)
    for name in ("N", "G_fund", "G_soil", "G_other", "Qx", "Qy"):
        changed[name] = QuantityValue(value=values[name].value * 1000, unit="N")
    for name in ("Mx", "My", "Mx_add_base", "My_add_base"):
        changed[name] = QuantityValue(value=values[name].value * 1000, unit="N*m")
    assert module.execute_public(values, data, LegacyOptions()) == module.execute_public(changed, data, LegacyOptions())


def test_zero_corner_is_admitted_without_tolerance(module: weights.FoundationsWeightsModule,
                                                 data: weights.Parameters) -> None:
    result = run(module, data, N=0, Mx=40)
    raw = trace_values(result)
    assert raw["p"] == 20
    assert raw["p_corner_min"] == 0
    assert result.verdict != "refused"
    assert len([step for step in result.trace if step.kind == "check"]) == 4


def test_negative_corner_refuses_despite_positive_axial_minima(module: weights.FoundationsWeightsModule,
                                                            data: weights.Parameters) -> None:
    result = run(module, data, Mx=140, My=210)
    raw = trace_values(result)
    assert raw["p_x_min"] == raw["p_y_min"] == 50
    assert raw["p_corner_min"] == -20
    assert result.verdict == "refused"
    assert result.outputs == ()
    assert not any(step.kind == "check" for step in result.trace)
    assert result.verdict_reason.kind == "derived"
    assert result.verdict_reason.limiting_corner == "mm"
    assert result.verdict_reason.related_inputs == WEIGHTS_CONTACT_INPUTS
    assert "d" not in result.verdict_reason.related_inputs
    assert "G_fund" in result.verdict_reason.related_inputs


def test_averaged_thickness_is_undeclared_for_explicit_type(module: weights.FoundationsWeightsModule) -> None:
    values = given() | {"d": QuantityValue(value=1, unit="m")}
    with pytest.raises(InputValidationError) as exc:
        CalculationRequest(calculation_type=weights.NAME, inputs=values).check_against(module.contract)
    assert invalid_inputs(exc.value) == ["d"]


def test_added_weight_requires_force_unit(module: weights.FoundationsWeightsModule) -> None:
    values = given() | {"G_fund": QuantityValue(value=60, unit="kPa")}
    with pytest.raises(InputValidationError) as exc:
        CalculationRequest(calculation_type=weights.NAME, inputs=values).check_against(module.contract)
    assert invalid_inputs(exc.value) == ["G_fund"]
    with pytest.raises(UnitError):
        module.normalize(weights.Inputs(**values))


def test_new_mode_does_not_claim_validated_range(module: weights.FoundationsWeightsModule,
                                                data: weights.Parameters) -> None:
    assert run(module, data).warnings == ()
    bound = ValidatedBound(quantity="N", kind="max", value=1, inclusive=True, source=RULE)
    with pytest.raises(CalculationError, match="validated range has no engineer admission"):
        module.execute_public(given(), data, LegacyOptions(validated_range=(bound,)))


def test_explicit_diagnostic_rejects_averaged_mode_inputs(module: weights.FoundationsWeightsModule,
                                                        data: weights.Parameters) -> None:
    supplied = weights.Inputs(**given(Mx=140, My=210))
    outcome = module.calculate(supplied, data, LegacyOptions())
    diagnostic = outcome.diagnostic
    assert diagnostic is not None
    assert isinstance(diagnostic.details, DerivedViolation)
    assert diagnostic.details.related_inputs == WEIGHTS_CONTACT_INPUTS
    assert "d" not in diagnostic.details.related_inputs
    altered = diagnostic.model_copy(update={
        "details": diagnostic.details.model_copy(update={"related_inputs": CONTACT_INPUTS}),
    })
    with pytest.raises(CalculationError, match="diagnostic differs from the domain calculation"):
        module.validate_diagnostic(altered, outcome.trace, supplied, data, LegacyOptions())
