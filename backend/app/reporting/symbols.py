import re
from collections.abc import Iterable, Mapping

from app.reporting.format import LATEX_OPERATORS, latex_quantity
from app.reporting.formula import Line, Math, Segment
from app.schemas.calculation import (
    CalculationTypeContract,
    CheckStep,
    QuantityValue,
    RoundingRule,
    TableStep,
    TraceStep,
)


def _left_side(expression: str) -> str | None:
    depth = 0
    for index, char in enumerate(expression):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "=" and depth == 0:
            return expression[:index].strip() or None
    return None


def step_symbol(step: TraceStep) -> str | None:
    """Находит обозначение шага трассы в LaTeX по его выражению.

    У проверки это всё выражение, у остальных шагов — левая часть до первого знака
    ``=`` вне фигурных скобок; у табличного шага без знака ``=`` — всё выражение.

    Args:
        step: шаг трассы.

    Returns:
        Обозначение в LaTeX или ``None``, если выражение его не даёт.
    """
    if isinstance(step, CheckStep):
        return step.expression
    left = _left_side(step.expression)
    if left is None and isinstance(step, TableStep):
        return step.expression
    return left


def symbol_table(contract: CalculationTypeContract, steps: Iterable[TraceStep]) -> dict[str, str]:
    """Собирает обозначения в LaTeX для имён шагов и величин отчёта.

    Обозначения входов и выходов из контракта заменяют обозначения, найденные по
    выражениям шагов с тем же именем.

    Args:
        contract: контракт типа расчёта.
        steps: шаги трассы.

    Returns:
        Обозначение в LaTeX по имени шага или величины.
    """
    table = {step.step_id: symbol for step in steps if (symbol := step_symbol(step)) is not None}
    for quantity in (*contract.inputs, *contract.outputs):
        if quantity.symbol:
            table[quantity.name] = quantity.symbol
    return table


_IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


_CORNER_SUBSCRIPT = re.compile(r"_\{([+-]{2})\}")


def _corner_subscripts(expression: str) -> str:
    return _CORNER_SUBSCRIPT.sub(lambda match: r"_{\text{" + match[1].replace("-", "−") + "}}", expression)


def math_symbol(name: str, symbols: Mapping[str, str]) -> Math:
    symbol = symbols.get(name, name)
    if _IDENTIFIER.fullmatch(symbol) and (symbol.count("_") > 1 or name not in symbols):
        return Math(r"\mathrm{" + symbol.replace("_", r"\_") + "}")
    return Math(_corner_subscripts(symbol))


_INLINE_EQUATION = re.compile(r"[A-Za-z][A-Za-z0-9_]*=[A-Za-z0-9_+*/²-]+")


def rationale_line(text: str, symbols: Mapping[str, str]) -> Line:
    parts: list[Segment] = []
    start = 0
    for match in _INLINE_EQUATION.finditer(text):
        parts.append(text[start:match.start()])
        latex = _IDENTIFIER.sub(lambda token: math_symbol(token[0], symbols).latex, match[0])
        parts.append(Math(latex.replace("*", r"\cdot ").replace("²", "^2")))
        start = match.end()
    parts.append(text[start:])
    return tuple(parts)


def check_expression(step: CheckStep, symbols: Mapping[str, str]) -> str:
    if len(step.substitutions) != 2:
        return step.expression
    left, right = (item.symbol for item in step.substitutions)
    op = LATEX_OPERATORS[step.operator]
    if step.expression != f"{left} {op} {right}" or not all(_IDENTIFIER.fullmatch(name) for name in (left, right)):
        return step.expression
    return f"{math_symbol(left, symbols).latex} {op} {math_symbol(right, symbols).latex}"


def named(name: str, symbols: Mapping[str, str]) -> Segment:
    """Печатает имя шага или величины её обозначением, а без обозначения — самим именем.

    Args:
        name: имя шага или величины.
        symbols: обозначения в LaTeX по имени.

    Returns:
        Формула обозначения или имя текстом.
    """
    return Math(symbols[name]) if name in symbols else name


def equation(
    name: str, value: QuantityValue, symbols: Mapping[str, str], rule: RoundingRule | None = None
) -> Line:
    """Печатает равенство величины и её значения, например ``b = 2 м``.

    Args:
        name: имя величины.
        value: значение с единицей.
        symbols: обозначения в LaTeX по имени.
        rule: правило округления, если величина — выход.

    Returns:
        Одна формула равенства или, без обозначения, имя текстом и формула значения.
    """
    if name in symbols:
        return (Math(f"{symbols[name]} = {latex_quantity(value, rule)}"),)
    return (f"{name} = ", Math(latex_quantity(value, rule)))
