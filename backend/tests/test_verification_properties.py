from collections.abc import Callable, Mapping
from typing import Any

import pytest
import test_verification_catalog_properties as on_catalog
from hypothesis import given, settings
from hypothesis import strategies as st
from pilot_invariants import (
    FORMULA_INVARIANTS,
    PILOT_RANGES,
    R_AFFINE_IN_C_II,
    R_AFFINE_IN_D_1,
    R_GROWS_WITH_B,
    R_GROWS_WITH_C_II,
    R_GROWS_WITH_D_B,
    R_GROWS_WITH_GAMMA_II,
)
from test_engine_foundations_shallow_r import (
    ROUNDING,
    RULE,
    entry,
    formula,
    num,
    parameters,
)
from test_verification_invariants import RANGES, SPECIFIC
from test_verification_runner import (
    CONTRACT,
    METHOD,
    PARAMETERS,
    TYPE,
    Parameters,
    SyntheticCalculator,
)
from verification_strategies import Subject, inputs_in_range

from app.engine import foundations_shallow_r as pilot
from app.engine.base import Calculator
from app.engine.boundary import convert, inputs_to_base_units
from app.engine.pipeline import CalculatorOutput, calculate
from app.schemas.calculation import CalculationResult, QuantityValue
from app.services.parameter_source import ResolvedParameters
from app.verification.invariants import (
    DETERMINISM,
    UNIT_CHANGE,
    Invariant,
    InvariantPlan,
    determinism_holds,
    invariant_coverage,
    plan_problems,
    shared_invariants,
    unit_change_holds,
)

CASES = settings(max_examples=100, deadline=None, database=None)
"""100 случаев на инвариант и тип, без лимита времени на случай и без базы примеров (решение 16)."""

PILOT_CONTRACT = pilot.contract(ROUNDING, RULE)
P_DOES_NOT_CHANGE_R = Invariant(
    identifier="p-does-not-change-R",
    statement="The pressure p does not change R; it changes only the verdict.",
    quantities=("p", "R"),
)
VERDICT_IS_P_LE_R = Invariant(
    identifier="verdict-is-p-le-R",
    statement="The verdict is pass exactly when p <= R, with R unrounded.",
    quantities=("p", "R"),
)
VERDICT_MONOTONE_IN_P = Invariant(
    identifier="verdict-monotone-in-p",
    statement="If the check passes at a pressure p, it passes at every smaller p.",
    quantities=("p", "R"),
)
"""Инварианты пилота, не зависящие от формулы R; подтверждены инженером (Аким) 2026-10-06 (задача 2.11)."""

def pilot_parameters(given: Mapping[str, QuantityValue], **changes: Any) -> pilot.Parameters:
    """Синтетические параметры пилота со строками таблицы, выбранными по ``phi_II`` входов."""
    phi = convert(given["phi_II"], "deg").value
    return parameters(
        m_gamma=entry("M_gamma", 0.5, phi), m_q=entry("M_q", 5.0, phi), m_c=entry("M_c", 10.0, phi), **changes
    )


SUBJECTS = (
    Subject(
        contract=CONTRACT,
        calculator=SyntheticCalculator(),
        parameters=lambda _: PARAMETERS,
        method_range=METHOD,
        plan=InvariantPlan(calculation_type=TYPE, valid_range=RANGES, invariants=(*shared_invariants(CONTRACT), SPECIFIC)),
    ),
    Subject(
        contract=PILOT_CONTRACT,
        calculator=pilot.FoundationsShallowR(),
        parameters=pilot_parameters,
        method_range=(),
        plan=InvariantPlan(
            calculation_type=pilot.NAME,
            valid_range=PILOT_RANGES,
            invariants=(
                *shared_invariants(PILOT_CONTRACT),
                P_DOES_NOT_CHANGE_R,
                VERDICT_IS_P_LE_R,
                VERDICT_MONOTONE_IN_P,
                *FORMULA_INVARIANTS,
            ),
        ),
    ),
)
"""Типы, на которых проверяются инварианты. Пилот считается здесь на синтетических параметрах;
инварианты, которые зависят от формулы R, проверяются на формуле и коэффициентах
ингестированного каталога в ``test_verification_catalog_properties.py`` (задача 2.11)."""
PILOT = SUBJECTS[1]


def subject_id(subject: Subject) -> str:
    return subject.contract.name


@pytest.mark.parametrize("subject", SUBJECTS, ids=subject_id)
def test_every_subject_has_a_plan_that_fits_its_contract(subject: Subject) -> None:
    assert plan_problems(subject.plan, subject.contract) == ()


@pytest.mark.parametrize("subject", SUBJECTS, ids=subject_id)
@CASES
@given(data=st.data())
def test_an_input_in_another_unit_gives_the_same_result(subject: Subject, data: st.DataObject) -> None:
    inputs = data.draw(inputs_in_range(subject.plan))

    assert unit_change_holds(subject.contract, subject.calculator, inputs, subject.parameters(inputs), subject.method_range)


@pytest.mark.parametrize("subject", SUBJECTS, ids=subject_id)
@CASES
@given(data=st.data())
def test_the_same_inputs_give_the_same_result(subject: Subject, data: st.DataObject) -> None:
    inputs = data.draw(inputs_in_range(subject.plan))

    assert determinism_holds(subject.contract, subject.calculator, inputs, subject.parameters(inputs), subject.method_range)


@CASES
@given(data=st.data())
def test_generated_inputs_stay_inside_the_valid_range(data: st.DataObject) -> None:
    inputs = data.draw(inputs_in_range(SUBJECTS[0].plan))

    assert set(inputs) == {"b", "q"}
    in_metres = inputs["b"].value * {"m": 1.0, "cm": 1e-2, "mm": 1e-3}[inputs["b"].unit]
    assert 1.0 - 1e-9 <= in_metres <= 40.0 + 1e-9
    assert inputs["q"].unit == "1" and 0.5 <= inputs["q"].value <= 2.0


@CASES
@given(data=st.data())
def test_y_grows_with_b_in_the_synthetic_type(data: st.DataObject) -> None:
    subject = SUBJECTS[0]
    inputs = inputs_to_base_units(subject.contract, data.draw(inputs_in_range(subject.plan)))
    upper = RANGES[0].upper
    larger = data.draw(st.floats(min_value=inputs["b"].value, max_value=upper, allow_nan=False))
    grown = {**inputs, "b": QuantityValue(value=larger, unit="m")}

    def y(given: dict[str, QuantityValue]) -> float:
        result = calculate(subject.contract, subject.calculator, given, subject.parameters(given), method_range=subject.method_range)
        return next(output.value for output in result.outputs if output.quantity == "y")

    assert y(inputs) <= y(grown)


def pilot_run(inputs: dict[str, QuantityValue]) -> CalculationResult:
    return calculate(PILOT.contract, PILOT.calculator, inputs, PILOT.parameters(inputs), method_range=PILOT.method_range)


def unrounded_r(result: CalculationResult) -> float:
    return next(step.result.value for step in result.trace if step.step_id == "R")


def with_p(inputs: dict[str, QuantityValue], p: float) -> dict[str, QuantityValue]:
    return {**inputs, "p": QuantityValue(value=p, unit="kPa")}


@CASES
@given(data=st.data())
def test_the_pressure_does_not_change_r(data: st.DataObject) -> None:
    inputs = data.draw(inputs_in_range(PILOT.plan))
    other = data.draw(st.floats(min_value=50.0, max_value=600.0, allow_nan=False))

    first, second = pilot_run(inputs), pilot_run(with_p(inputs, other))

    assert first.outputs == second.outputs
    assert unrounded_r(first) == unrounded_r(second)


@CASES
@given(data=st.data())
def test_the_verdict_is_pass_exactly_when_p_is_at_most_unrounded_r(data: st.DataObject) -> None:
    inputs = inputs_to_base_units(PILOT.contract, data.draw(inputs_in_range(PILOT.plan)))

    result = pilot_run(inputs)

    assert (result.verdict == "pass") is (inputs["p"].value <= unrounded_r(result))


@CASES
@given(data=st.data())
def test_a_check_that_passes_at_p_passes_at_every_smaller_p(data: st.DataObject) -> None:
    inputs = inputs_to_base_units(PILOT.contract, data.draw(inputs_in_range(PILOT.plan)))
    smaller = data.draw(st.floats(min_value=50.0, max_value=inputs["p"].value, allow_nan=False))

    if pilot_run(inputs).verdict == "pass":
        assert pilot_run(with_p(inputs, smaller)).verdict == "pass"


def test_the_pilot_range_gives_both_verdicts() -> None:
    lowest = {item.quantity: QuantityValue(value=item.lower, unit=item.unit) for item in PILOT_RANGES}
    highest = {item.quantity: QuantityValue(value=item.upper, unit=item.unit) for item in PILOT_RANGES}

    assert (pilot_run(with_p(highest, 50.0)).verdict, pilot_run(with_p(lowest, 600.0)).verdict) == ("pass", "fail")


PROPERTY_TESTS = {
    **{(subject.contract.name, DETERMINISM): test_the_same_inputs_give_the_same_result for subject in SUBJECTS},
    **{(subject.contract.name, UNIT_CHANGE): test_an_input_in_another_unit_gives_the_same_result for subject in SUBJECTS},
    (TYPE, SPECIFIC.identifier): test_y_grows_with_b_in_the_synthetic_type,
    (pilot.NAME, P_DOES_NOT_CHANGE_R.identifier): test_the_pressure_does_not_change_r,
    (pilot.NAME, VERDICT_IS_P_LE_R.identifier): test_the_verdict_is_pass_exactly_when_p_is_at_most_unrounded_r,
    (pilot.NAME, VERDICT_MONOTONE_IN_P.identifier): test_a_check_that_passes_at_p_passes_at_every_smaller_p,
    (pilot.NAME, R_AFFINE_IN_C_II.identifier): on_catalog.test_equal_steps_of_c_ii_give_equal_steps_of_r,
    (pilot.NAME, R_AFFINE_IN_D_1.identifier): on_catalog.test_equal_steps_of_d_1_give_equal_steps_of_r,
    (pilot.NAME, R_GROWS_WITH_C_II.identifier): on_catalog.test_a_larger_c_ii_gives_an_r_not_smaller,
    (pilot.NAME, R_GROWS_WITH_GAMMA_II.identifier): on_catalog.test_a_larger_gamma_ii_gives_an_r_not_smaller,
    (pilot.NAME, R_GROWS_WITH_D_B.identifier): on_catalog.test_a_larger_d_b_gives_an_r_not_smaller,
    (pilot.NAME, R_GROWS_WITH_B.identifier): on_catalog.test_a_larger_b_gives_an_r_not_smaller,
}
"""Property-тест каждого инварианта каждого субъекта: пара (тип, инвариант) -> функция теста."""


CONTINUOUS_K_Z = formula(r"k_z = \kappa", num(1.25), "k_z", {"k_z": "1"})
"""Синтетическая ``k_z`` ниже порога, равная ``b / 4`` на синтетическом пороге 5 м."""


def synthetic_catalog(**changes: Any) -> Callable[[Mapping[str, QuantityValue]], ResolvedParameters]:
    """Синтетическая замена каталога для контрольных прогонов тестов, зависящих от формулы R."""
    return lambda given: ResolvedParameters(parameters=pilot_parameters(given, **changes), method_range=())


@pytest.mark.parametrize(
    "test",
    [
        on_catalog.test_equal_steps_of_c_ii_give_equal_steps_of_r,
        on_catalog.test_equal_steps_of_d_1_give_equal_steps_of_r,
        on_catalog.test_a_larger_c_ii_gives_an_r_not_smaller,
        on_catalog.test_a_larger_gamma_ii_gives_an_r_not_smaller,
        on_catalog.test_a_larger_d_b_gives_an_r_not_smaller,
        on_catalog.test_a_larger_b_gives_an_r_not_smaller,
        on_catalog.test_r_does_not_drop_across_the_k_z_threshold,
    ],
)
def test_the_formula_tests_pass_on_a_synthetic_r_that_keeps_the_invariants(test: Callable[..., None]) -> None:
    test(resolve=synthetic_catalog(k_z_below=CONTINUOUS_K_Z))


def test_the_threshold_test_finds_a_drop_of_r_at_the_k_z_threshold() -> None:
    with pytest.raises(AssertionError):
        on_catalog.test_r_does_not_drop_across_the_k_z_threshold(resolve=synthetic_catalog())


def test_every_listed_invariant_has_a_property_test() -> None:
    coverage = invariant_coverage([subject.plan for subject in SUBJECTS], PROPERTY_TESTS)

    assert (coverage.verdict, coverage.untested) == ("GO", ())


def test_every_registered_test_is_a_property_based_test() -> None:
    assert all(getattr(test, "is_hypothesis_test", False) for test in PROPERTY_TESTS.values())


@CASES
@given(data=st.data())
def test_a_whole_input_is_generated_as_a_whole_value_in_its_own_unit(data: st.DataObject) -> None:
    phi = data.draw(inputs_in_range(PILOT.plan))["phi_II"]

    assert phi.unit == "deg"
    assert phi.value.is_integer() and 0.0 <= phi.value <= 45.0


def test_an_input_in_millimetres_gives_the_same_result_as_in_metres() -> None:
    inputs = {"b": QuantityValue(value=2500.0, unit="mm"), "q": QuantityValue(value=1.5, unit="1")}

    assert unit_change_holds(CONTRACT, SyntheticCalculator(), inputs, PARAMETERS, METHOD)


class DriftingCalculator(Calculator[Mapping[str, QuantityValue], Parameters, CalculatorOutput]):
    """Калькулятор с изменяемым состоянием: каждый вызов даёт другой результат."""

    def __init__(self) -> None:
        self.calls = 0
        self.inner = SyntheticCalculator()

    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Parameters) -> CalculatorOutput:
        self.calls += 1
        shifted = {**inputs, "q": QuantityValue(value=inputs["q"].value + self.calls, unit="1")}
        return self.inner.calculate(shifted, parameters)


def test_a_calculator_with_state_breaks_determinism() -> None:
    inputs = {"b": QuantityValue(value=2.0, unit="m"), "q": QuantityValue(value=1.0, unit="1")}

    assert not determinism_holds(CONTRACT, DriftingCalculator(), inputs, PARAMETERS, METHOD)


def test_a_calculator_with_state_breaks_unit_change_consistency() -> None:
    inputs = {"b": QuantityValue(value=2000.0, unit="mm"), "q": QuantityValue(value=1.0, unit="1")}

    assert not unit_change_holds(CONTRACT, DriftingCalculator(), inputs, PARAMETERS, METHOD)


def test_inputs_left_in_their_own_units_break_unit_change_consistency(monkeypatch: pytest.MonkeyPatch) -> None:
    def units_seen(
        contract: object, calculator: object, inputs: Mapping[str, QuantityValue], *args: object, **kwargs: object
    ) -> tuple[str, ...]:
        return tuple(value.unit for value in inputs.values())

    monkeypatch.setattr("app.verification.invariants.calculate", units_seen)
    in_metres = {"b": QuantityValue(value=2.0, unit="m"), "q": QuantityValue(value=1.0, unit="1")}
    in_millimetres = {"b": QuantityValue(value=2000.0, unit="mm"), "q": QuantityValue(value=1.0, unit="1")}

    assert unit_change_holds(CONTRACT, SyntheticCalculator(), in_metres, PARAMETERS, METHOD)
    assert not unit_change_holds(CONTRACT, SyntheticCalculator(), in_millimetres, PARAMETERS, METHOD)
