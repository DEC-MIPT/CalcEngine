from typing import Any

import pytest
from pydantic import ValidationError

from app.core.exceptions import CalculationError, ExpressionError, UnitError
from app.engine.boundary import convert
from app.engine.steps import check_step, confirm_selectors, formula_step, table_step
from app.schemas.calculation import (
    CalculationResult,
    CheckReason,
    CheckStep,
    FormulaStep,
    NormRef,
    QuantityValue,
    TableStep,
)
from app.schemas.expression import parse_expression, symbols
from app.schemas.resolved import Formula, Selector, TableValue

HASH = "0" * 64


def ref(clause: str) -> NormRef:
    return NormRef(
        document="<NORM-DOC-PLACEHOLDER>",
        edition="unverified",
        clause=clause,
        status="unverified",
        provenance="machine-extracted",
    )


FORMULA_REF = ref("<CLAUSE-FORMULA>")
TABLE_REF = ref("<CLAUSE-TABLE>")
CHECK_REF = ref("<CLAUSE-CHECK>")

SYNTHETIC_TREE = {
    "kind": "add",
    "left": {
        "kind": "mul",
        "left": {"kind": "symbol", "name": "a"},
        "right": {"kind": "symbol", "name": "x"},
    },
    "right": {
        "kind": "mul",
        "left": {"kind": "symbol", "name": "b"},
        "right": {"kind": "symbol", "name": "a"},
    },
}


def synthetic_formula(**changes: Any) -> Formula:
    fields: dict[str, Any] = {
        "latex": r"y = a x + b a",
        "tree": parse_expression(SYNTHETIC_TREE),
        "result_symbol": "y",
        "units": {"a": "1", "x": "kPa", "b": "kPa", "y": "kPa"},
        "norm_refs": (FORMULA_REF,),
    }
    return Formula.model_validate(fields | changes)


def m(value: float) -> QuantityValue:
    return QuantityValue(value=value, unit="m")


def kpa(value: float) -> QuantityValue:
    return QuantityValue(value=value, unit="kPa")


VALUES = {"a": QuantityValue(value=2.0, unit="1"), "x": kpa(3.0), "b": kpa(4.0)}


def test_symbols_are_listed_once_in_reading_order() -> None:
    assert symbols(parse_expression(SYNTHETIC_TREE)) == ("a", "x", "b")


def test_formula_step_evaluates_the_tree_and_records_its_substitutions() -> None:
    step = formula_step("y", synthetic_formula(), VALUES)

    assert step.expression == r"y = a x + b a"
    assert step.result == kpa(2.0 * 3.0 + 4.0 * 2.0)
    assert [(s.symbol, s.value, s.unit) for s in step.substitutions] == [
        ("a", 2.0, "1"),
        ("x", 3.0, "kPa"),
        ("b", 4.0, "kPa"),
    ]
    assert step.norm_refs == (FORMULA_REF,)


def test_formula_step_rejects_a_value_in_another_unit() -> None:
    with pytest.raises(UnitError, match="'x'"):
        formula_step("y", synthetic_formula(), VALUES | {"x": QuantityValue(value=3.0, unit="MPa")})


def test_a_wrong_unit_is_reported_even_when_the_evaluation_would_fail() -> None:
    dividing = synthetic_formula(
        latex=r"y = x / (b - b)",
        tree=parse_expression(
            {
                "kind": "div",
                "left": {"kind": "symbol", "name": "x"},
                "right": {
                    "kind": "sub",
                    "left": {"kind": "symbol", "name": "b"},
                    "right": {"kind": "symbol", "name": "b"},
                },
            }
        ),
        units={"x": "kPa", "b": "kPa", "y": "1"},
    )

    with pytest.raises(UnitError, match="'b'"):
        formula_step("y", dividing, {"x": kpa(3.0), "b": QuantityValue(value=4.0, unit="MPa")})
    with pytest.raises(ExpressionError, match="no finite value"):
        formula_step("y", dividing, {"x": kpa(3.0), "b": kpa(4.0)})


def test_formula_step_names_a_symbol_without_a_value() -> None:
    values = {name: value for name, value in VALUES.items() if name != "b"}

    with pytest.raises(ExpressionError, match="'b'"):
        formula_step("y", synthetic_formula(), values)


@pytest.mark.parametrize(
    "units",
    [{"a": "1", "x": "kPa", "y": "kPa"}, {"a": "1", "x": "kPa", "b": "kPa"}],
    ids=["tree-symbol", "result-symbol"],
)
def test_a_formula_binds_every_symbol_to_a_unit(units: dict[str, str]) -> None:
    with pytest.raises(ValidationError, match="symbols without a unit"):
        synthetic_formula(units=units)


PHI = Selector(symbol="phi", value=QuantityValue(value=20.0, unit="deg"))


def table_entry(*selectors: Selector) -> TableValue:
    return TableValue(
        symbol="k",
        latex=r"k_{t}",
        value=QuantityValue(value=0.5, unit="1"),
        norm_refs=(TABLE_REF,),
        selectors=selectors,
    )


def test_table_step_records_the_entry_and_its_selectors() -> None:
    step = table_step("k", table_entry(PHI))

    assert step.expression == r"k_{t} = k_{t}\left(phi\right)"
    assert [(s.symbol, s.value, s.unit) for s in step.substitutions] == [("phi", 20.0, "deg")]
    assert step.result == QuantityValue(value=0.5, unit="1")
    assert step.norm_refs == (TABLE_REF,)


def test_table_step_lists_every_selector_in_order() -> None:
    b = Selector(symbol="b", value=QuantityValue(value=2.0, unit="m"))

    step = table_step("k", table_entry(PHI, b))

    assert step.expression == r"k_{t} = k_{t}\left(phi, b\right)"
    assert [(s.symbol, s.value, s.unit) for s in step.substitutions] == [("phi", 20.0, "deg"), ("b", 2.0, "m")]


def test_a_table_value_has_one_selector_per_symbol() -> None:
    with pytest.raises(ValidationError, match="one selector per symbol"):
        table_entry(PHI, PHI)


def test_a_heading_equal_to_the_input_is_confirmed() -> None:
    confirm_selectors(table_entry(PHI), {"phi": QuantityValue(value=20.0, unit="deg")})


def test_a_table_value_without_selectors_needs_no_input() -> None:
    confirm_selectors(table_entry(), {})


@pytest.mark.parametrize("given", [20.000000000000004, 21.0])
def test_a_heading_that_differs_from_the_input_is_refused(given: float) -> None:
    with pytest.raises(CalculationError, match="'phi' differs from the input"):
        confirm_selectors(table_entry(PHI), {"phi": QuantityValue(value=given, unit="deg")})


def test_a_heading_on_a_symbol_that_is_not_an_input_is_refused() -> None:
    with pytest.raises(CalculationError, match="'phi' is not an input"):
        confirm_selectors(table_entry(PHI), {"b": QuantityValue(value=20.0, unit="m")})


def test_a_heading_of_another_dimension_is_refused() -> None:
    heading = Selector(symbol="phi", value=QuantityValue(value=20.0, unit="m"))

    with pytest.raises(CalculationError, match="cannot be expressed in 'deg'") as exc_info:
        confirm_selectors(table_entry(heading), {"phi": QuantityValue(value=20.0, unit="deg")})

    assert exc_info.value.__cause__ is None


def test_a_heading_in_another_unit_is_confirmed_for_an_input_in_that_unit() -> None:
    heading = Selector(symbol="phi", value=QuantityValue(value=0.3, unit="rad"))
    base_unit_input = convert(QuantityValue(value=0.3, unit="rad"), "deg")

    confirm_selectors(table_entry(heading), {"phi": base_unit_input})
    step = table_step("k", table_entry(heading))

    assert base_unit_input.value != 0.3
    assert [(s.symbol, s.value, s.unit) for s in step.substitutions] == [("phi", 0.3, "rad")]


def test_table_step_without_selectors() -> None:
    step = table_step("k", table_entry())

    assert step.expression == r"k_{t}"
    assert step.substitutions == ()


@pytest.mark.parametrize(
    "operator,left,expected",
    [
        ("le", 5.0, True),
        ("le", 5.1, False),
        ("lt", 5.0, False),
        ("lt", 4.9, True),
        ("ge", 5.0, True),
        ("ge", 4.9, False),
        ("gt", 5.0, False),
        ("gt", 5.1, True),
    ],
)
def test_check_step_compares_by_its_operator(operator: Any, left: float, expected: bool) -> None:
    step = check_step("c", ("p", kpa(left)), operator, ("R", kpa(5.0)), (CHECK_REF,))

    assert step.passed is expected
    assert step.result == kpa(left)
    assert step.right == kpa(5.0)
    assert step.operator == operator


def test_check_step_expression_and_substitutions() -> None:
    step = check_step("c", ("p", kpa(4.0)), "le", ("R", kpa(5.0)), (CHECK_REF,))

    assert step.expression == r"p \le R"
    assert [(s.symbol, s.value) for s in step.substitutions] == [("p", 4.0), ("R", 5.0)]


def test_check_step_rejects_two_units() -> None:
    with pytest.raises(UnitError, match="'c'"):
        check_step("c", ("p", kpa(4.0)), "le", ("d", m(5.0)), (CHECK_REF,))


def completed_calculation() -> CalculationResult:
    k = table_step("k", table_entry(PHI))
    y = formula_step("y", synthetic_formula(), VALUES)
    check = check_step("check", ("y", y.result), "le", ("y_{max}", kpa(20.0)), (CHECK_REF,))
    return CalculationResult(
        engine_version="0.1.0",
        input_hash=HASH,
        outputs=(),
        norm_refs=(TABLE_REF, FORMULA_REF, CHECK_REF),
        engineer_rules=(),
        verdict="pass",
        verdict_reason=CheckReason(step_id="check"),
        warnings=(),
        trace=(k, y, check),
        unverified_step_count=3,
    )


STEP_FIELDS = {"kind", "step_id", "expression", "substitutions", "result", "norm_refs"}
FIELDS_OF_KIND = {
    FormulaStep: STEP_FIELDS,
    TableStep: STEP_FIELDS,
    CheckStep: STEP_FIELDS | {"operator", "right", "passed"},
}


def has_none(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, dict):
        return any(has_none(item) for item in value.values())
    if isinstance(value, list | tuple):
        return any(has_none(item) for item in value)
    return False


def test_every_step_of_a_completed_calculation_has_all_fields_of_its_kind_none_null() -> None:
    result = completed_calculation()

    assert {type(step) for step in result.trace} == set(FIELDS_OF_KIND)
    for step in result.trace:
        dumped = step.model_dump()
        assert set(dumped) == FIELDS_OF_KIND[type(step)], step.step_id
        assert not has_none(dumped), step.step_id
        assert step.norm_refs
        assert all(s.symbol and s.unit for s in step.substitutions)
        assert step.result.unit
