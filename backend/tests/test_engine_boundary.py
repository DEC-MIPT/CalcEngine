import math
from collections.abc import Mapping

import pytest

from app.core.exceptions import CalculationError, UnitError
from app.engine.base import Calculator
from app.engine.boundary import (
    convert,
    inputs_to_base_units,
    make_outputs,
    run,
)
from app.engine.steps import formula_step
from app.schemas.calculation import (
    CalculationTypeContract,
    FormulaStep,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
)
from app.schemas.expression import parse_expression
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import Formula

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-FORMULA>",
    status="unverified",
    provenance="machine-extracted",
)

CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(
        QuantityDeclaration(name="b", base_unit="m"),
        QuantityDeclaration(name="p", base_unit="kPa"),
    ),
    outputs=(
        OutputDeclaration(
            name="y",
            base_unit="m",
            rounding_rule=RoundingRule(decimals=2, mode="half_up"),
            rounding_source=EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>"),
        ),
    ),
    checks=("check",),
)

FORMULA = Formula(
    latex=r"y = 2 b",
    tree=parse_expression(
        {"kind": "mul", "left": {"kind": "number", "value": 2}, "right": {"kind": "symbol", "name": "b"}}
    ),
    result_symbol="y",
    units={"b": "m", "y": "m"},
    norm_refs=(REF,),
)


class TraceCalculator(Calculator[Mapping[str, QuantityValue], Formula, FormulaStep]):
    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Formula) -> FormulaStep:
        return formula_step("y", parameters, inputs)


class SpyCalculator(Calculator[Mapping[str, QuantityValue], None, None]):
    def __init__(self) -> None:
        self.calls = 0

    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: None) -> None:
        self.calls += 1


def q(value: float, unit: str) -> QuantityValue:
    return QuantityValue(value=value, unit=unit)


@pytest.mark.parametrize(
    "value,target,expected",
    [
        (q(1500.0, "mm"), "m", 1.5),
        (q(25.0, "cm"), "m", 0.25),
        (q(0.2, "MPa"), "kPa", 200.0),
        (q(18.0, "kN/m3"), "N/m3", 18000.0),
        (q(180.0, "deg"), "rad", math.pi),
        (q(3.0, "m"), "m", 3.0),
    ],
)
def test_convert_to_another_unit_of_the_same_dimension(
    value: QuantityValue, target: str, expected: float
) -> None:
    converted = convert(value, target)

    assert converted.unit == target
    assert converted.value == pytest.approx(expected)


def test_convert_to_the_same_unit_keeps_the_value_exactly() -> None:
    assert convert(q(0.1, "m"), "m") == q(0.1, "m")


def test_convert_rejects_another_dimension() -> None:
    with pytest.raises(UnitError, match="cannot convert 'kPa'"):
        convert(q(1.0, "kPa"), "m")


def test_convert_rejects_an_unknown_unit() -> None:
    with pytest.raises(UnitError, match="'furlong'"):
        convert(QuantityValue.model_construct(value=1.0, unit="furlong"), "m")


def test_convert_rejects_a_value_that_overflows() -> None:
    with pytest.raises(UnitError, match="not a finite number"):
        convert(q(1e308, "MN"), "N")


def test_a_non_base_input_shows_in_the_trace_in_its_base_unit() -> None:
    step = run(CONTRACT, TraceCalculator(), {"b": q(1500.0, "mm"), "p": q(0.2, "MPa")}, FORMULA)

    assert [(s.symbol, s.value, s.unit) for s in step.substitutions] == [("b", 1.5, "m")]
    assert step.result == q(3.0, "m")


def test_inputs_come_in_the_contract_order_and_base_units() -> None:
    converted = inputs_to_base_units(CONTRACT, {"p": q(0.2, "MPa"), "b": q(1.0, "m")})

    assert list(converted) == ["b", "p"]
    assert converted["p"] == q(200.0, "kPa")


@pytest.mark.parametrize(
    "inputs", [{"b": q(1.0, "m")}, {"b": q(1.0, "m"), "p": q(1.0, "kPa"), "z": q(1.0, "m")}]
)
def test_inputs_must_match_the_declared_inputs(inputs: dict[str, QuantityValue]) -> None:
    with pytest.raises(CalculationError, match="declared inputs"):
        inputs_to_base_units(CONTRACT, inputs)


@pytest.mark.parametrize(
    "value",
    [QuantityValue.model_construct(value=1.0, unit="furlong"), q(1.0, "kPa")],
    ids=["unknown-unit", "other-dimension"],
)
def test_a_wrong_unit_fails_before_any_step_runs(value: QuantityValue) -> None:
    calculator = SpyCalculator()

    with pytest.raises(UnitError):
        run(CONTRACT, calculator, {"b": value, "p": q(1.0, "kPa")}, None)

    assert calculator.calls == 0


def test_an_output_leaves_in_its_base_unit_with_its_rule_and_source() -> None:
    (output,) = make_outputs(CONTRACT, {"y": q(2500.0, "mm")})

    declared = CONTRACT.outputs[0]
    assert (output.quantity, output.value, output.unit) == ("y", 2.5, "m")
    assert (output.rounding_rule, output.rounding_source) == (
        declared.rounding_rule,
        declared.rounding_source,
    )


def test_an_output_in_another_dimension_fails() -> None:
    with pytest.raises(UnitError):
        make_outputs(CONTRACT, {"y": q(1.0, "kPa")})


@pytest.mark.parametrize("values", [{}, {"y": q(1.0, "m"), "z": q(1.0, "m")}])
def test_outputs_must_match_the_declared_outputs(values: dict[str, QuantityValue]) -> None:
    with pytest.raises(CalculationError, match="declared outputs"):
        make_outputs(CONTRACT, values)
