from collections.abc import Mapping

from app.core.exceptions import CalculationError, UnitError
from app.engine.boundary import convert
from app.engine.expression import evaluate_expression
from app.schemas.calculation import (
    CheckStep,
    FormulaStep,
    NormRefs,
    Operator,
    QuantityValue,
    Substitution,
    TableStep,
)
from app.schemas.expression import symbols
from app.schemas.resolved import Formula, TableValue

_LATEX: Mapping[Operator, str] = {"le": r"\le", "lt": "<", "ge": r"\ge", "gt": ">"}


def _substitution(symbol: str, value: QuantityValue) -> Substitution:
    return Substitution(symbol=symbol, value=value.value, unit=value.unit)


def formula_step(
    step_id: str, formula: Formula, values: Mapping[str, QuantityValue]
) -> FormulaStep:
    """Вычисляет формулу и записывает шаг трассы.

    Args:
        step_id: идентификатор шага.
        formula: формула с деревом выражения, LaTeX, единицами символов и ``NormRef``.
        values: значения символов; у каждого — та единица, которую формула связывает с
            его символом.

    Returns:
        Шаг формулы с подстановками и результатом.

    Единицы символов проверяются до вычисления, поэтому неверная единица называется
    как ошибка единицы, даже если вычисление тоже упало бы.

    Raises:
        ExpressionError: если дерево не проходит проверку или значение не конечное.
        UnitError: если единица значения не та, что связана с символом.
    """
    used = symbols(formula.tree)
    for name in used:
        if name in values and values[name].unit != formula.units[name]:
            raise UnitError(
                f"step {step_id!r}: {name!r} is in {values[name].unit!r},"
                f" the formula expects {formula.units[name]!r}"
            )
    result = evaluate_expression(
        formula.tree, {name: value.value for name, value in values.items()}, step_id
    )
    return FormulaStep(
        step_id=step_id,
        expression=formula.latex,
        substitutions=tuple(_substitution(name, values[name]) for name in used),
        result=QuantityValue(value=result, unit=formula.units[formula.result_symbol]),
        norm_refs=formula.norm_refs,
    )


def confirm_selectors(entry: TableValue, inputs: Mapping[str, QuantityValue], selected_by: str | None) -> None:
    """Подтверждает, что табличное значение выбрано по тем входам, которые получил движок.

    Значение, которое метод выбирает по входу, обязано нести заголовок именно этого
    входа, а значение, которое метод по входу не выбирает, — не нести ни одного
    (``normative-catalog-backend`` design.md, решение 6). Заголовок переводится в базовую
    единицу входа тем же ``convert``, что и при выборе строки в источнике параметров, и
    сравнивается со входом точно (``calculation-engine`` "Table value selectors"). Движок
    ничего не ищет — только подтверждает выбор.

    Args:
        entry: табличное значение со своими ``selectors``.
        inputs: входы в базовых единицах.
        selected_by: вход, по которому метод выбирает это значение, или ``None``.

    Raises:
        CalculationError: если заголовки значения не те, что требует метод, символ
            заголовка не вход, заголовок не переводится в единицу входа или не равен ему.
    """
    expected = () if selected_by is None else (selected_by,)
    if tuple(selector.symbol for selector in entry.selectors) != expected:
        raise CalculationError(f"table value {entry.symbol!r}: selectors differ from the method's")
    for selector in entry.selectors:
        if selector.symbol not in inputs:
            raise CalculationError(f"table value {entry.symbol!r}: selector {selector.symbol!r} is not an input")
        given = inputs[selector.symbol]
        try:
            heading = convert(selector.value, given.unit)
        except UnitError:
            raise CalculationError(
                f"table value {entry.symbol!r}: selector {selector.symbol!r} cannot be expressed in {given.unit!r}"
            ) from None
        if heading.value != given.value:
            raise CalculationError(f"table value {entry.symbol!r}: selector {selector.symbol!r} differs from the input")


def table_step(step_id: str, entry: TableValue, symbols: Mapping[str, str]) -> TableStep:
    """Записывает шаг трассы для табличного значения и заголовков, которые его выбрали.

    Подстановки — заголовки из ``entry.selectors`` в их собственной единице, под именами
    входов. В выражении каждый заголовок назван обозначением своего входа в LaTeX, чтобы
    выражение отображалось (``calculation-engine`` "Typed trace step").

    Args:
        step_id: идентификатор шага.
        entry: табличное значение со своими ``NormRef`` и заголовками.
        symbols: обозначение в LaTeX для имени каждого входа типа расчёта.

    Returns:
        Шаг таблицы.

    Raises:
        CalculationError: если у заголовка нет обозначения в ``symbols``.
    """
    missing = [selector.symbol for selector in entry.selectors if selector.symbol not in symbols]
    if missing:
        raise CalculationError(f"table value {entry.symbol!r}: selector {missing[0]!r} has no LaTeX symbol")
    arguments = ", ".join(symbols[selector.symbol] for selector in entry.selectors)
    expression = rf"{entry.latex} = {entry.latex}\left({arguments}\right)" if entry.selectors else entry.latex
    return TableStep(
        step_id=step_id,
        expression=expression,
        substitutions=tuple(_substitution(selector.symbol, selector.value) for selector in entry.selectors),
        result=entry.value,
        norm_refs=entry.norm_refs,
    )


def compare(
    step_id: str, left: QuantityValue, operator: Operator, right: QuantityValue
) -> bool:
    """Сравнивает два значения в одной единице — для шага проверки или ветви метода.

    Args:
        step_id: шаг, который называется в ошибке.
        left: левое значение.
        operator: оператор сравнения.
        right: правое значение.

    Returns:
        Результат сравнения.

    Raises:
        UnitError: если единицы значений различаются.
    """
    if left.unit != right.unit:
        raise UnitError(f"step {step_id!r} compares {left.unit!r} with {right.unit!r}")
    return {
        "le": left.value <= right.value,
        "lt": left.value < right.value,
        "ge": left.value >= right.value,
        "gt": left.value > right.value,
    }[operator]


def check_step(
    step_id: str,
    left: tuple[str, QuantityValue],
    operator: Operator,
    right: tuple[str, QuantityValue],
    norm_refs: NormRefs,
) -> CheckStep:
    """Записывает шаг проверки: сравнение двух значений в одной единице.

    Args:
        step_id: идентификатор проверки, объявленный в контракте.
        left: пара из символа LaTeX и значения слева.
        operator: оператор сравнения.
        right: пара из символа LaTeX и значения справа.
        norm_refs: ссылки на нормы, из которых взята проверка.

    Returns:
        Шаг проверки с обоими значениями и итогом ``passed``.

    Raises:
        UnitError: если единицы значений различаются.
    """
    (left_symbol, left_value), (right_symbol, right_value) = left, right
    passed = compare(step_id, left_value, operator, right_value)
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
