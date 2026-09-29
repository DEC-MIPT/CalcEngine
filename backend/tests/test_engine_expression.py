import ast
import math
from pathlib import Path
from typing import Any

import pytest

from app.core.exceptions import DECError, ExpressionError
from app.engine import expression
from app.engine.expression import MAX_DEPTH, MAX_NODES, evaluate_expression
from app.schemas.expression import ExpressionNode, parse_expression


def num(value: float) -> dict[str, Any]:
    return {"kind": "number", "value": value}


def sym(name: str) -> dict[str, Any]:
    return {"kind": "symbol", "name": name}


def op(kind: str, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {"kind": kind, "left": left, "right": right}


def call(function: str, *args: dict[str, Any]) -> dict[str, Any]:
    return {"kind": "call", "function": function, "args": list(args)}


def tree(data: dict[str, Any]) -> ExpressionNode:
    return parse_expression(data)


def evaluate(data: dict[str, Any], **bindings: float) -> float:
    return evaluate_expression(tree(data), bindings, "s1")


def test_a_tree_of_allowed_nodes_gives_its_value() -> None:
    data = op(
        "add",
        op("mul", sym("a"), op("pow", sym("x"), num(2))),
        op("div", {"kind": "neg", "operand": sym("b")}, op("sub", num(5), num(3))),
    )

    assert evaluate(data, a=2.0, x=3.0, b=4.0) == 2.0 * 3.0**2 + (-4.0) / 2.0


@pytest.mark.parametrize(
    "data,expected",
    [
        (call("sqrt", num(9)), 3.0),
        (call("exp", num(0)), 1.0),
        (call("ln", num(1)), 0.0),
        (call("log10", num(100)), 2.0),
        (call("sin", num(0)), 0.0),
        (call("cos", num(0)), 1.0),
        (call("tan", num(0)), 0.0),
        (call("abs", num(-2)), 2.0),
        (call("min", num(3), num(1), num(2)), 1.0),
        (call("max", num(3), num(1)), 3.0),
    ],
)
def test_each_allowed_function(data: dict[str, Any], expected: float) -> None:
    assert evaluate(data) == pytest.approx(expected)


def test_evaluation_is_deterministic() -> None:
    data = op("div", call("sqrt", sym("x")), num(3))

    assert evaluate(data, x=2.0) == evaluate(data, x=2.0)


@pytest.fixture
def evaluation_spy(monkeypatch: pytest.MonkeyPatch) -> list[object]:
    calls: list[object] = []
    original = expression._evaluate

    def spy(node: Any, bindings: Any) -> float:
        calls.append(node)
        return original(node, bindings)

    monkeypatch.setattr(expression, "_evaluate", spy)
    return calls


@pytest.mark.parametrize(
    "data",
    [call("__import__", num(1)), call("sqrt", num(1), num(2)), call("min", num(1))],
    ids=["unknown-function", "too-many-args", "too-few-args"],
)
def test_a_function_outside_the_allowed_set_fails_before_evaluation(
    data: dict[str, Any], evaluation_spy: list[object]
) -> None:
    with pytest.raises(ExpressionError):
        evaluate(op("add", num(1), data))

    assert evaluation_spy == []


@pytest.mark.parametrize(
    "data",
    [
        {"kind": "attribute", "name": "x"},
        {"kind": "number", "value": "1+1"},
        {"kind": "call", "function": "sqrt", "args": []},
        {"kind": "symbol", "name": "x", "code": "print(1)"},
        "x + 1",
    ],
    ids=["unknown-kind", "string-number", "no-args", "extra-field", "raw-string"],
)
def test_a_node_outside_the_allowed_set_is_rejected_as_a_dec_error(data: object) -> None:
    with pytest.raises(ExpressionError):
        parse_expression(data)


def chain(depth: int) -> dict[str, Any]:
    data = num(1)
    for _ in range(depth - 1):
        data = {"kind": "neg", "operand": data}
    return data


def balanced(depth: int) -> dict[str, Any]:
    if depth == 1:
        return num(1)
    return op("add", balanced(depth - 1), balanced(depth - 1))


def test_a_tree_at_the_depth_limit_is_evaluated() -> None:
    assert evaluate(chain(MAX_DEPTH)) == (-1.0) ** (MAX_DEPTH - 1)


def test_a_tree_deeper_than_the_limit_fails_before_evaluation(
    evaluation_spy: list[object],
) -> None:
    with pytest.raises(ExpressionError, match="deeper than"):
        evaluate(chain(MAX_DEPTH + 1))

    assert evaluation_spy == []


def test_a_tree_with_too_many_nodes_fails_before_evaluation(
    evaluation_spy: list[object],
) -> None:
    data = balanced(13)
    assert 2**13 - 1 > MAX_NODES

    with pytest.raises(ExpressionError, match="more than"):
        evaluate(data)

    assert evaluation_spy == []


def test_a_tree_too_deep_to_parse_is_a_dec_error() -> None:
    with pytest.raises(ExpressionError):
        parse_expression(chain(10_000))


def test_a_symbol_without_a_value_fails_naming_it(evaluation_spy: list[object]) -> None:
    with pytest.raises(ExpressionError, match="'gamma'"):
        evaluate(op("mul", sym("x"), sym("gamma")), x=1.0)

    assert evaluation_spy == []


@pytest.mark.parametrize(
    "data,bindings",
    [
        (op("div", num(1), sym("x")), {"x": 0.0}),
        (call("sqrt", num(-1)), {}),
        (call("ln", num(0)), {}),
        (op("pow", num(-8), op("div", num(1), num(3))), {}),
        (op("pow", num(10), num(400)), {}),
        (op("mul", num(1e308), num(10)), {}),
        (sym("x"), {"x": math.inf}),
    ],
    ids=["division-by-zero", "sqrt-negative", "ln-zero", "complex-power", "overflow", "inf", "inf-binding"],
)
def test_a_value_that_is_not_finite_fails_naming_the_step(
    data: dict[str, Any], bindings: dict[str, float]
) -> None:
    with pytest.raises(ExpressionError, match="'s1'"):
        evaluate(data, **bindings)


def test_expression_error_is_a_dec_error() -> None:
    assert issubclass(ExpressionError, DECError)


def test_the_interpreter_executes_no_code() -> None:
    forbidden = {"eval", "exec", "compile", "__import__", "sympify", "parse_expr", "lambdify"}
    for module in (expression.__file__, Path(expression.__file__).parents[1] / "schemas" / "expression.py"):
        syntax = ast.parse(Path(module).read_text(encoding="utf-8"))
        names = {node.id for node in ast.walk(syntax) if isinstance(node, ast.Name)}
        names |= {node.attr for node in ast.walk(syntax) if isinstance(node, ast.Attribute)}
        imported = {
            alias.name
            for node in ast.walk(syntax)
            if isinstance(node, ast.Import | ast.ImportFrom)
            for alias in node.names
        }
        assert not forbidden & (names | imported), module
        assert "sympy" not in {
            node.module for node in ast.walk(syntax) if isinstance(node, ast.ImportFrom)
        }
