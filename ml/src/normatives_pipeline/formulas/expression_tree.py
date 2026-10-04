"""Дерево выражения формулы в JSON-форме каталога.

Форма узлов зафиксирована спецификацией
``normatives-catalog`` "Expression tree form in the catalog" (design.md, решение 3):
её читает движок backend'а, поэтому пайплайн строит дерево на ingestion и не хранит
формулу, которую не смог перевести.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import sympy  # type: ignore[import-untyped]

FUNCTIONS = frozenset(
    {"sqrt", "exp", "ln", "log10", "sin", "cos", "tan", "abs", "min", "max"}
)
MAX_DEPTH = 64
MAX_NODES = 4096

_CALL_NAMES = {
    "sqrt": "sqrt",
    "exp": "exp",
    "log": "ln",
    "log10": "log10",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "Abs": "abs",
    "Min": "min",
    "Max": "max",
}


class ExpressionTreeError(ValueError):
    """Формула не переводится в форму дерева каталога."""


def _number(expr: sympy.Basic) -> dict[str, Any]:
    if not expr.is_finite:
        raise ExpressionTreeError(f"не конечное число: {expr!r}")
    value = int(expr) if expr.is_Integer else float(expr)
    return {"kind": "number", "value": value}


def _split_negated(term: sympy.Basic) -> tuple[bool, sympy.Basic]:
    coeff, rest = term.as_coeff_Mul()
    if coeff == -1:
        return True, rest
    return False, term


def _call(expr: sympy.Function) -> dict[str, Any]:
    name = expr.func.__name__
    args = list(expr.args)
    function: str | None
    if name == "log":
        if len(args) == 2:
            if args[1] != 10:
                raise ExpressionTreeError(f"log с основанием {args[1]!r} не поддержан")
            function, args = "log10", args[:1]
        else:
            function = "ln"
    else:
        function = _CALL_NAMES.get(name)
    if function not in FUNCTIONS:
        raise ExpressionTreeError(f"функция {name!r} вне закрытого списка")
    return {"kind": "call", "function": function, "args": [_to_node(a) for a in args]}


def _to_node(expr: sympy.Basic) -> dict[str, Any]:
    if expr.is_Number:
        return _number(expr)
    if expr.is_Symbol:
        return {"kind": "symbol", "name": str(expr)}
    if expr.is_Add:
        terms = list(expr.args)
        node = _to_node(terms[0])
        for term in terms[1:]:
            negated, inner = _split_negated(term)
            node = {
                "kind": "sub" if negated else "add",
                "left": node,
                "right": _to_node(inner),
            }
        return node
    if expr.is_Mul:
        coeff, rest = expr.as_coeff_Mul()
        if coeff == -1:
            return {"kind": "neg", "operand": _to_node(rest)}
        factors = list(expr.args)
        node = _to_node(factors[0])
        for factor in factors[1:]:
            node = {"kind": "mul", "left": node, "right": _to_node(factor)}
        return node
    if expr.is_Pow:
        base, exponent = expr.args
        if exponent == sympy.Rational(1, 2):
            return {"kind": "call", "function": "sqrt", "args": [_to_node(base)]}
        return {"kind": "pow", "left": _to_node(base), "right": _to_node(exponent)}
    if isinstance(expr, sympy.Function):
        return _call(expr)
    raise ExpressionTreeError(f"узел {expr!r} ({type(expr).__name__}) не переводится")


def _children(node: dict[str, Any]) -> list[dict[str, Any]]:
    kind = node["kind"]
    if kind in {"add", "sub", "mul", "div", "pow"}:
        return [node["left"], node["right"]]
    if kind == "neg":
        return [node["operand"]]
    if kind == "call":
        return list(node["args"])
    return []


def validate_tree(node: dict[str, Any]) -> None:
    """Проверяет дерево против набора узлов, списка функций и лимитов.

    Raises:
        ExpressionTreeError: вид узла вне набора, функция вне списка, дерево
            глубже ``MAX_DEPTH`` или длиннее ``MAX_NODES``.
    """
    stack: list[tuple[dict[str, Any], int]] = [(node, 1)]
    count = 0
    while stack:
        current, depth = stack.pop()
        count += 1
        if count > MAX_NODES:
            raise ExpressionTreeError(f"дерево длиннее {MAX_NODES} узлов")
        if depth > MAX_DEPTH:
            raise ExpressionTreeError(f"дерево глубже {MAX_DEPTH}")
        kind = current.get("kind")
        if kind == "number":
            if not isinstance(current.get("value"), (int, float)):
                raise ExpressionTreeError("у числа нет value")
        elif kind == "symbol":
            if not current.get("name"):
                raise ExpressionTreeError("у символа нет name")
        elif kind == "call":
            if current.get("function") not in FUNCTIONS:
                raise ExpressionTreeError(f"функция {current.get('function')!r} вне списка")
            if not current.get("args"):
                raise ExpressionTreeError("у вызова нет аргументов")
        elif kind not in {"add", "sub", "mul", "div", "pow", "neg"}:
            raise ExpressionTreeError(f"вид узла {kind!r} вне набора")
        for child in _children(current):
            stack.append((child, depth + 1))


def build_tree(expression: str, symbol_names: Iterable[str]) -> dict[str, Any]:
    """Строит дерево выражения из его текстовой формы.

    Args:
        expression: выражение в форме sympy (как в реестре формул) или LaTeX-совместимое.
        symbol_names: идентификаторы символов, чтобы ``beta``/``theta``/``delta``
            не разрешились в одноимённые функции sympy.

    Returns:
        Дерево в JSON-форме каталога.

    Raises:
        ExpressionTreeError: выражение не разбирается или не переводится в форму.
    """
    local = {name: sympy.Symbol(name) for name in symbol_names}
    local["log10"] = sympy.Function("log10")
    try:
        expr = sympy.sympify(expression, locals=local)
    except (sympy.SympifyError, SyntaxError, TypeError, ValueError) as exc:
        raise ExpressionTreeError(f"выражение не разбирается: {exc}") from exc
    node = _to_node(expr)
    validate_tree(node)
    return node


def tree_symbols(node: dict[str, Any]) -> list[str]:
    """Перечисляет имена символов дерева, каждое один раз, в порядке первого чтения."""
    found: list[str] = []
    seen: set[str] = set()
    stack = [node]
    while stack:
        current = stack.pop()
        if current.get("kind") == "symbol":
            name = current["name"]
            if name not in seen:
                seen.add(name)
                found.append(name)
        stack.extend(reversed(_children(current)))
    return found
