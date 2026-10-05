from collections.abc import Mapping

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
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

from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput
from app.schemas.calculation import QuantityValue
from app.verification.invariants import (
    InvariantPlan,
    determinism_holds,
    plan_problems,
    shared_invariants,
    unit_change_holds,
)

CASES = settings(max_examples=100, deadline=None, database=None)
"""100 случаев на инвариант и тип, без лимита времени на случай и без базы примеров (решение 16)."""

SUBJECTS = (
    Subject(
        contract=CONTRACT,
        calculator=SyntheticCalculator(),
        parameters=PARAMETERS,
        method_range=METHOD,
        plan=InvariantPlan(calculation_type=TYPE, valid_range=RANGES, invariants=(*shared_invariants(CONTRACT), SPECIFIC)),
    ),
)
"""Типы, на которых проверяются общие инварианты; пилот добавится с его планом (задача 2.11)."""


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

    assert unit_change_holds(subject.contract, subject.calculator, inputs, subject.parameters, subject.method_range)


@pytest.mark.parametrize("subject", SUBJECTS, ids=subject_id)
@CASES
@given(data=st.data())
def test_the_same_inputs_give_the_same_result(subject: Subject, data: st.DataObject) -> None:
    inputs = data.draw(inputs_in_range(subject.plan))

    assert determinism_holds(subject.contract, subject.calculator, inputs, subject.parameters, subject.method_range)


@CASES
@given(data=st.data())
def test_generated_inputs_stay_inside_the_valid_range(data: st.DataObject) -> None:
    inputs = data.draw(inputs_in_range(SUBJECTS[0].plan))

    assert set(inputs) == {"b", "q"}
    in_metres = inputs["b"].value * {"m": 1.0, "cm": 1e-2, "mm": 1e-3}[inputs["b"].unit]
    assert 1.0 - 1e-9 <= in_metres <= 40.0 + 1e-9
    assert inputs["q"].unit == "1" and 0.5 <= inputs["q"].value <= 2.0


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
