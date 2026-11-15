from dataclasses import replace

import pytest
from pydantic import ValidationError
from test_engine_foundations_shallow_r import RULE
from test_loads_interim_source import inputs as source_inputs
from test_loads_interim_source import resolve

from app.core.exceptions import (
    CalculationError,
    ExpressionError,
    InputValidationError,
    UnitError,
)
from app.engine import foundations_shallow_loads as loads
from app.engine.boundary import convert
from app.engine.legacy_module import LegacyOptions
from app.engine.module import execute_module, module_run_identity
from app.schemas.api import FieldError
from app.schemas.calculation import (
    CONTACT_INPUTS,
    CalculationRequest,
    CalculationResult,
    CheckReason,
    CheckStep,
    DerivedViolation,
    EngineerFormulaStep,
    QuantityValue,
    RoundingRule,
    ValidatedBound,
)
from app.schemas.parameters import EngineerRule
from app.schemas.units import UNITS, Dimension


@pytest.fixture(scope="module")
def data() -> loads.Parameters:
    return resolve().parameters


@pytest.fixture
def module() -> loads.FoundationsLoadsModule:
    return loads.FoundationsLoadsModule(loads.contract(RoundingRule(decimals=2, mode="half_up"), RULE))


def inputs(**changes: float) -> dict[str, QuantityValue]:
    result = source_inputs()
    return result | {name: QuantityValue(value=value, unit=result[name].unit) for name, value in changes.items()}


def run(module: loads.FoundationsLoadsModule, data: loads.Parameters, **changes: float) -> CalculationResult:
    return module.execute_public(inputs(**changes), data, LegacyOptions())


def values(result: CalculationResult) -> dict[str, float]:
    return {step.step_id: step.result.value for step in result.trace}


def check_reason(result: CalculationResult) -> CheckReason:
    assert isinstance(result.verdict_reason, CheckReason)
    return result.verdict_reason


def derived_reason(result: CalculationResult) -> DerivedViolation:
    assert isinstance(result.verdict_reason, DerivedViolation)
    return result.verdict_reason


def test_moment_and_volume_units() -> None:
    assert UNITS["m3"].dimension == Dimension.VOLUME
    assert UNITS["kN*m"].dimension == Dimension.MOMENT
    assert convert(QuantityValue(value=1000, unit="N*m"), "kN*m").value == 1
    assert convert(QuantityValue(value=1, unit="MN*m"), "kN*m").value == 1000
    with pytest.raises(UnitError):
        convert(QuantityValue(value=1, unit="m3"), "m2")


def test_registered_contract_and_central_sequence(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    result = run(module, data, Mx=0, My=0)
    assert len(module.contract.inputs) == 15
    assert tuple(output.quantity for output in result.outputs) == loads.OUTPUT_NAMES
    pressure = [output.value for output in result.outputs if output.quantity != "R"]
    assert pressure == [120] * 9
    assert tuple(step.step_id for step in result.trace[:8]) == ("gamma_c1", "gamma_c2", "k", "M_gamma", "M_q", "M_c", "k_z", "R")
    assert [step.step_id for step in result.trace if isinstance(step, CheckStep)] == list(loads.CHECKS)
    assert check_reason(result).step_id == loads.CHECKS[-1]
    geometry = {step.step_id: step for step in result.trace}
    assert geometry["A"].result == QuantityValue(value=6, unit="m2")
    assert geometry["Wx"].result == QuantityValue(value=2, unit="m3")
    assert geometry["Wy"].result == QuantityValue(value=3, unit="m3")
    assert result.unverified_step_count == sum(step.kind != "engineer_formula" for step in result.trace)


@pytest.mark.parametrize("height", [0, 1, 2])
def test_signed_transfer_and_cancellation(module: loads.FoundationsLoadsModule, data: loads.Parameters, height: float) -> None:
    result = run(module, data, Mx=-10*height, Qx=10, My=6*height, Qy=-6, h=height)
    raw = values(result)
    assert raw["Mx_base"] == raw["My_base"] == 0
    assert all(raw[name] == raw["p"] for name in loads.OUTPUT_NAMES[2:])
    assert raw["V"] == 720


def test_force_and_moment_unit_equivalence_and_versioned_identity(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    original = inputs()
    changed = original | {"N": QuantityValue(value=600000, unit="N"), "Mx": QuantityValue(value=10000, unit="N*m"),
                          "My": QuantityValue(value=0.02, unit="MN*m"), "Qx": QuantityValue(value=0, unit="MN")}
    first = module.execute_public(original, data, LegacyOptions())
    second = module.execute_public(changed, data, LegacyOptions())
    assert first == second
    normalized = module.normalize(loads.Inputs(**changed))
    assert first.input_hash == module_run_identity(module.metadata, normalized, data, LegacyOptions())
    assert first.input_hash != run(module, data, Mx=11).input_hash


def test_axis_interchange_of_pure_pressure_module(data: loads.Parameters) -> None:
    original = inputs(Mx=-30, Qx=7, My=14, Qy=-3)
    swapped = original | {"b": original["l"], "l": original["b"], "Mx": original["My"], "My": original["Mx"], "Qx": original["Qy"], "Qy": original["Qx"]}
    _, first, _ = loads.pressure_steps(original, data)
    _, second, _ = loads.pressure_steps(swapped, data)
    assert first["p"] == second["p"]
    assert first["p_x_min"] == second["p_y_min"]
    assert first["p_x_max"] == second["p_y_max"]
    assert first["p_corner_pm"] == second["p_corner_mp"]
    assert first["p_corner_pp"] == second["p_corner_pp"]


@pytest.mark.parametrize(("name", "value"), [("b", 0), ("l", 0), ("d", 0), ("gamma_II", 0), ("gamma_II_prime", 0),
    ("h", -1), ("d_1", -1), ("d_b", -1), ("N", -1), ("c_II", -1), ("phi_II", -1), ("phi_II", 46), ("phi_II", 20.5), ("b", 4)])
def test_request_and_direct_calls_reject_engineering_domains(module: loads.FoundationsLoadsModule, data: loads.Parameters, name: str, value: float) -> None:
    supplied = inputs(**{name: value})
    with pytest.raises(InputValidationError) as caught:
        CalculationRequest(calculation_type=loads.NAME, inputs=supplied).check_against(module.contract)
    assert any(isinstance(field, FieldError) and field.location[-1] == name for field in caught.value.fields)
    with pytest.raises(InputValidationError):
        module.execute_public(supplied, data, LegacyOptions())


def test_independent_depths_and_zero_admitted_values(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    result = run(module, data, h=0, d=3, d_1=0, N=0, Mx=0, My=0, c_II=0)
    assert values(result)["p"] == 60
    assert result.verdict != "refused"


@pytest.mark.parametrize(("mx", "my", "corner"), [(180, 180, "mm"), (-180, 180, "pm"), (180, -180, "mp"), (-180, -180, "pp")])
def test_biaxial_contact_refusal_with_nonnegative_axial_minima(module: loads.FoundationsLoadsModule, data: loads.Parameters, mx: float, my: float, corner: str) -> None:
    result = run(module, data, Mx=mx, My=my)
    assert result.verdict == "refused" and result.outputs == ()
    raw = values(result)
    assert raw["p_x_min"] >= 0 and raw["p_y_min"] >= 0
    assert raw["p_corner_min"] == -30
    assert derived_reason(result).limiting_corner == corner
    assert derived_reason(result).related_inputs == CONTACT_INPUTS
    assert not any(isinstance(step, CheckStep) for step in result.trace)
    assert CalculationResult.model_validate_json(result.model_dump_json()) == result


def test_zero_contact_and_first_tie(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    zero = run(module, data, Mx=240, My=0)
    assert values(zero)["p_corner_min"] == 0
    assert zero.verdict != "refused"
    tied = run(module, data, Mx=0, My=400)
    assert derived_reason(tied).limiting_corner == "pm"
    tied_other = run(module, data, Mx=0, My=-400)
    assert derived_reason(tied_other).limiting_corner == "pp"


def test_method_bound_refusal_retains_historical_shape(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    resolved = resolve()
    refused = module.execute_public(inputs(d_b=3), data, LegacyOptions(method_range=resolved.method_range))
    assert refused.verdict == "refused"
    assert refused.verdict_reason.kind == "bound"
    assert refused.trace == refused.outputs == ()
    assert refused.unverified_step_count == 0
    assert module.execute_public(inputs(d_b=2), data, LegacyOptions(method_range=resolved.method_range)).verdict != "refused"


def test_checks_use_unrounded_values_and_support_zero_resistance(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    base = run(module, data, Mx=0, My=0)
    resistance = values(base)["R"]
    pressure = resistance + 0.00001
    result = run(module, data, N=(pressure - 20) * 6, Mx=0, My=0)
    assert result.verdict == "fail" and check_reason(result).step_id == "p_le_R"
    assert result.outputs[0].value == result.outputs[1].value
    zero_data = data.model_copy(update={"resistance": data.resistance.model_copy(update={"gamma_c1": data.resistance.gamma_c1.model_copy(update={"value": QuantityValue(value=0, unit="1")})})})
    zero = run(module, zero_data, Mx=0, My=0)
    assert zero.verdict == "fail"
    assert values(zero)["edge_limit"] == values(zero)["corner_limit"] == 0


@pytest.mark.parametrize(("mx", "my", "pressure_ratio", "deciding"), [(0, 0, 1.01, "p_le_R"), (0.3, 0, 0.95, "p_x_max_le_limit"),
    (0, 0.3, 0.95, "p_y_max_le_limit"), (0.38, 0.38, 0.8, "p_corner_max_le_limit")])
def test_each_first_bearing_failure(module: loads.FoundationsLoadsModule, data: loads.Parameters, mx: float, my: float, pressure_ratio: float, deciding: str) -> None:
    resistance = values(run(module, data))["R"]
    result = run(module, data, N=(pressure_ratio * resistance - 20)*6, Mx=mx*resistance*2, My=my*resistance*3)
    assert result.verdict == "fail" and check_reason(result).step_id == deciding


@pytest.mark.parametrize("changed", [{"limiting_corner": "invalid"}, {"related_inputs": ("unknown",)},
    {"value": QuantityValue(value=0, unit="kPa")}, {"source": EngineerRule(engineer="other", rationale="other")},
    {"limit": QuantityValue(value=1, unit="kPa")}])
def test_derived_details_reject_corruption(module: loads.FoundationsLoadsModule, data: loads.Parameters, changed: dict[str, object]) -> None:
    reason = run(module, data, Mx=180, My=180).verdict_reason
    with pytest.raises(ValidationError):
        DerivedViolation.model_validate(reason.model_dump() | changed)


@pytest.mark.parametrize("change", ["corner", "minimum", "guard", "trace_source", "check", "outputs"])
def test_public_result_rejects_corrupt_diagnostic_trace(module: loads.FoundationsLoadsModule, data: loads.Parameters, change: str) -> None:
    result = run(module, data, Mx=180, My=180)
    raw = result.model_dump()
    if change == "corner":
        raw["verdict_reason"]["limiting_corner"] = "pp"
    elif change == "minimum":
        raw["verdict_reason"]["value"]["value"] = -1
    elif change == "guard":
        raw["trace"] = tuple(step for step in raw["trace"] if step["step_id"] != "p_corner_min")
    elif change == "trace_source":
        raw["trace"] = tuple(step | {"source": {"engineer": "other", "rationale": "other"}} if step["step_id"] == "p_corner_min" else step for step in raw["trace"])
    elif change == "check":
        raw["trace"] += (run(module, data).model_dump()["trace"][-1],)
    else:
        raw["outputs"] = run(module, data).model_dump()["outputs"]
    with pytest.raises(ValidationError):
        CalculationResult.model_validate(raw)


def test_private_diagnostic_validator_recomputes_and_rejects_mismatches(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    supplied = loads.Inputs(**inputs(Mx=180, My=180))
    execution = execute_module(module, supplied, data, LegacyOptions())
    diagnostic = execution.outcome.diagnostic
    assert diagnostic is not None
    with pytest.raises(CalculationError):
        module.validate_diagnostic(diagnostic.model_copy(update={"step_id": "unknown"}), execution.outcome.trace, supplied, data, LegacyOptions())
    assert module.adapt_result(execution).verdict == "refused"


def test_nonfinite_intermediate_is_typed_error(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    with pytest.raises(ExpressionError):
        run(module, data, l=1e308, b=1e308)
    with pytest.raises(ExpressionError):
        loads.pressure_steps(inputs(b=1e-300, l=1e-300), data)


def test_no_unadmitted_validated_range(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    bound = ValidatedBound(quantity="N", kind="max", value=1, inclusive=True, source=RULE)
    with pytest.raises(CalculationError):
        module.execute_public(inputs(), data, LegacyOptions(validated_range=(bound,)))


def test_engineer_trace_has_source_and_forbids_norm_refs(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    engineer = next(step for step in run(module, data).trace if isinstance(step, EngineerFormulaStep))
    with pytest.raises(ValidationError):
        EngineerFormulaStep.model_validate(engineer.model_dump() | {"norm_refs": data.p_corner.norm_refs})
    assert replace(module).contract == module.contract


def test_exact_fraction_does_not_round_trapezoidal_case_to_triangular(data: loads.Parameters) -> None:
    supplied = inputs(N=1, Mx=40.33333333333333, My=0)
    trace, quantities, _ = loads.pressure_steps(supplied, data)
    assert quantities["V"].value == 121
    assert quantities["e_x"].value / supplied["b"].value == 1 / 6
    diagram = next(step for step in trace if step.step_id == "pressure_diagram_x")
    assert diagram.expression == data.diagram_cases.cases[0].condition_latex
    zero_trace, _, _ = loads.pressure_steps(inputs(Mx=240, My=0), data)
    zero_diagram = next(step for step in zero_trace if step.step_id == "pressure_diagram_x")
    assert zero_diagram.expression == data.diagram_cases.cases[1].condition_latex


def test_arithmetic_and_data_guards_are_typed(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    with pytest.raises(ExpressionError):
        run(module, data, Mx=1e308, Qx=1e308, h=2)
    empty_diagram = data.model_copy(update={"diagram_cases": data.diagram_cases.model_copy(update={"cases": ()})})
    with pytest.raises(CalculationError):
        loads.pressure_steps(inputs(), empty_diagram)
    no_vertical_force = data.model_copy(update={"gamma_mt": data.gamma_mt.model_copy(update={"value": QuantityValue(value=0, unit="kN/m3")})})
    with pytest.raises(ExpressionError):
        loads.pressure_steps(inputs(N=0), no_vertical_force)


def test_registration_rejects_missing_rounding_entries() -> None:
    from app.engine.registry import CalculatorRegistry

    with pytest.raises(CalculationError):
        loads.register(CalculatorRegistry(), {})
    with pytest.raises(CalculationError):
        loads.register(object(), {})


def test_module_adapter_rejects_missing_completed_outputs(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    execution = execute_module(module, loads.Inputs(**inputs()), data, LegacyOptions())
    broken = execution.model_copy(update={"outcome": execution.outcome.model_copy(update={"outputs": None})})
    with pytest.raises(CalculationError):
        module.adapt_result(broken)


def test_typed_outputs_reject_wrong_units() -> None:
    supplied = {name: QuantityValue(value=1, unit="kPa") for name in loads.OUTPUT_NAMES}
    with pytest.raises(ValidationError):
        loads.Outputs(**(supplied | {"p": QuantityValue(value=1, unit="MPa")}))


def test_public_diagnostic_preserves_first_equal_minimum(module: loads.FoundationsLoadsModule, data: loads.Parameters) -> None:
    tied = run(module, data, Mx=0, My=400)
    raw = tied.model_dump()
    raw["verdict_reason"]["limiting_corner"] = "mm"
    with pytest.raises(ValidationError):
        CalculationResult.model_validate(raw)


def test_custom_module_registration_requires_unique_matching_metadata(module: loads.FoundationsLoadsModule) -> None:
    from app.core.exceptions import AlreadyRegisteredError, ContractMetadataError
    from app.engine.registry import CalculatorRegistry

    registry = CalculatorRegistry()
    registry.register_module(module.contract, module)
    assert registry.module(loads.NAME) is module
    from app.engine.module_adapter import ModuleCalculator

    calculator = registry.get(loads.NAME)
    assert isinstance(calculator, ModuleCalculator)
    assert calculator.module is module
    with pytest.raises(AlreadyRegisteredError):
        registry.register_module(module.contract, module)
    with pytest.raises(ContractMetadataError):
        CalculatorRegistry().register_module(module.contract.model_copy(update={"name": "wrong"}), module)
    missing_label = module.contract.model_copy(update={"inputs": (module.contract.inputs[0].model_copy(update={"label": None}),)})
    with pytest.raises(ContractMetadataError):
        CalculatorRegistry().register_module(missing_label, module)
    from app.engine.foundations_shallow_r import FoundationsShallowR

    with pytest.raises(ContractMetadataError):
        CalculatorRegistry().register(missing_label, FoundationsShallowR())


def test_register_installs_all_output_rounding_entries(module: loads.FoundationsLoadsModule) -> None:
    from app.engine.registry import CalculatorRegistry
    from app.parameters.param_schemas import RoundingEntry

    entries = {name: RoundingEntry(rule=module.contract.outputs[0].rounding_rule, source=RULE) for name in loads.OUTPUT_NAMES}
    registry = CalculatorRegistry()
    loads.register(registry, entries)
    assert registry.contract(loads.NAME) == module.contract
