from collections.abc import Mapping
from typing import Literal

from app.core.exceptions import UnitError
from app.engine.expression import evaluate_expression
from app.schemas.calculation import (
    CheckStep,
    FormulaStep,
    NormRefs,
    QuantityValue,
    Substitution,
    TableStep,
)
from app.schemas.expression import symbols
from app.schemas.resolved import Formula, TableValue

Operator = Literal["le", "lt", "ge", "gt"]

_LATEX: Mapping[Operator, str] = {"le": r"\le", "lt": "<", "ge": r"\ge", "gt": ">"}


def _substitution(symbol: str, value: QuantityValue) -> Substitution:
    return Substitution(symbol=symbol, value=value.value, unit=value.unit)


def formula_step(
    step_id: str, formula: Formula, values: Mapping[str, QuantityValue]
) -> FormulaStep:
    """Evaluate a formula; each value must carry the unit the formula binds to its symbol."""
    result = evaluate_expression(
        formula.tree, {name: value.value for name, value in values.items()}, step_id
    )
    used = symbols(formula.tree)
    for name in used:
        if values[name].unit != formula.units[name]:
            raise UnitError(
                f"step {step_id!r}: {name!r} is in {values[name].unit!r},"
                f" the formula expects {formula.units[name]!r}"
            )
    return FormulaStep(
        step_id=step_id,
        expression=formula.latex,
        substitutions=tuple(_substitution(name, values[name]) for name in used),
        result=QuantityValue(value=result, unit=formula.units[formula.result_symbol]),
        norm_refs=formula.norm_refs,
    )


def table_step(step_id: str, entry: TableValue, selectors: Mapping[str, QuantityValue]) -> TableStep:
    """Record a table entry and the values that selected it."""
    arguments = ", ".join(selectors)
    expression = rf"{entry.latex} = {entry.latex}\left({arguments}\right)" if selectors else entry.latex
    return TableStep(
        step_id=step_id,
        expression=expression,
        substitutions=tuple(_substitution(name, value) for name, value in selectors.items()),
        result=entry.value,
        norm_refs=entry.norm_refs,
    )


def check_step(
    step_id: str,
    left: tuple[str, QuantityValue],
    operator: Operator,
    right: tuple[str, QuantityValue],
    norm_refs: NormRefs,
) -> CheckStep:
    """Compare two values in the same unit; ``left`` and ``right`` pair a LaTeX symbol with a value."""
    (left_symbol, left_value), (right_symbol, right_value) = left, right
    if left_value.unit != right_value.unit:
        raise UnitError(
            f"step {step_id!r} compares {left_value.unit!r} with {right_value.unit!r}"
        )
    passed = {
        "le": left_value.value <= right_value.value,
        "lt": left_value.value < right_value.value,
        "ge": left_value.value >= right_value.value,
        "gt": left_value.value > right_value.value,
    }[operator]
    return CheckStep(
        step_id=step_id,
        expression=f"{left_symbol} {_LATEX[operator]} {right_symbol}",
        substitutions=(
            _substitution(left_symbol, left_value),
            _substitution(right_symbol, right_value),
        ),
        result=left_value,
        norm_refs=norm_refs,
        operator=operator,
        right=right_value,
        passed=passed,
    )
