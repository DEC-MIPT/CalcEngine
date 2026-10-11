"""Тесты дерева выражения каталога (раздел 2.2)."""

from __future__ import annotations

import pytest
import sympy

from normatives_pipeline.formulas import expression_tree as tree
from normatives_pipeline.formulas.expression_tree import ExpressionTreeError, _call

PILOT_R_SYMBOLS = [
    "gamma_c1",
    "gamma_c2",
    "k",
    "M_gamma",
    "k_z",
    "b",
    "gamma_II",
    "M_q",
    "d_1",
    "gamma_II_prime",
    "d_b",
    "M_c",
    "c_II",
]
PILOT_R = (
    "(gamma_c1*gamma_c2/k)*(M_gamma*k_z*b*gamma_II + M_q*d_1*gamma_II_prime "
    "+ (M_q - 1)*d_b*gamma_II_prime + M_c*c_II)"
)


def test_number_and_symbol() -> None:
    assert tree.build_tree("2", []) == {"kind": "number", "value": 2}
    assert tree.build_tree("2.5", []) == {"kind": "number", "value": 2.5}
    assert tree.build_tree("b", ["b"]) == {"kind": "symbol", "name": "b"}


def test_polynomial_shapes() -> None:
    assert tree.build_tree("a + b", ["a", "b"]) == {
        "kind": "add",
        "left": {"kind": "symbol", "name": "a"},
        "right": {"kind": "symbol", "name": "b"},
    }
    assert tree.build_tree("a - b", ["a", "b"]) == {
        "kind": "sub",
        "left": {"kind": "symbol", "name": "a"},
        "right": {"kind": "symbol", "name": "b"},
    }
    assert tree.build_tree("-a", ["a"]) == {
        "kind": "neg",
        "operand": {"kind": "symbol", "name": "a"},
    }
    assert tree.build_tree("a*b", ["a", "b"])["kind"] == "mul"
    assert tree.build_tree("a/b", ["a", "b"])["kind"] == "mul"
    assert tree.build_tree("a**2", ["a"]) == {
        "kind": "pow",
        "left": {"kind": "symbol", "name": "a"},
        "right": {"kind": "number", "value": 2},
    }


def test_sqrt_becomes_call() -> None:
    node = tree.build_tree("sqrt(a)", ["a"])
    assert node == {
        "kind": "call",
        "function": "sqrt",
        "args": [{"kind": "symbol", "name": "a"}],
    }


def test_trig_and_logs() -> None:
    assert tree.build_tree("cos(phi)", ["phi"])["function"] == "cos"
    assert tree.build_tree("sin(phi)", ["phi"])["function"] == "sin"
    assert tree.build_tree("log(x)", ["x"])["function"] == "ln"
    assert tree.build_tree("log10(x)", ["x"])["function"] == "log10"


def test_symbol_defaults_are_not_sympy_functions() -> None:
    node = tree.build_tree("beta + theta", ["beta", "theta"])
    assert node["left"] == {"kind": "symbol", "name": "beta"}
    assert node["right"] == {"kind": "symbol", "name": "theta"}


def test_pilot_r_expression_builds() -> None:
    node = tree.build_tree(PILOT_R, PILOT_R_SYMBOLS)
    tree.validate_tree(node)
    assert set(tree.tree_symbols(node)) == set(PILOT_R_SYMBOLS)


def test_unknown_function_is_refused() -> None:
    with pytest.raises(tree.ExpressionTreeError):
        tree.build_tree("gamma(a)", ["a"])


def test_unparsable_expression_is_refused() -> None:
    with pytest.raises(tree.ExpressionTreeError):
        tree.build_tree("a +", ["a"])


def test_validate_depth_limit() -> None:
    node: dict = {"kind": "symbol", "name": "a"}
    for _ in range(tree.MAX_DEPTH):
        node = {"kind": "neg", "operand": node}
    with pytest.raises(tree.ExpressionTreeError):
        tree.validate_tree(node)


def test_validate_node_limit() -> None:
    node: dict = {"kind": "symbol", "name": "a"}
    for _ in range(tree.MAX_NODES):
        node = {"kind": "add", "left": {"kind": "number", "value": 1}, "right": node}
    with pytest.raises(tree.ExpressionTreeError):
        tree.validate_tree(node)


def test_infinite_number_is_refused() -> None:
    with pytest.raises(tree.ExpressionTreeError, match="конечное"):
        tree.build_tree("oo", [])


def test_log_base_2_refused_via_call() -> None:
    # sympy expands log(x, base) to Mul before _to_node sees it, so test _call directly
    x = sympy.Symbol("x")
    log_fn = sympy.Function("log")
    with pytest.raises(ExpressionTreeError, match="основанием"):
        _call(log_fn(x, sympy.Integer(2)))


def test_log_base_10_two_args_via_call() -> None:
    x = sympy.Symbol("x")
    log_fn = sympy.Function("log")
    node = _call(log_fn(x, sympy.Integer(10)))
    assert node["kind"] == "call"
    assert node["function"] == "log10"
    assert len(node["args"]) == 1


def test_relational_node_is_refused() -> None:
    with pytest.raises(tree.ExpressionTreeError):
        tree.build_tree("x >= y", ["x", "y"])


def test_validate_too_many_nodes_wide_tree() -> None:
    def _balanced(depth: int) -> dict:
        if depth == 0:
            return {"kind": "symbol", "name": "a"}
        return {"kind": "add", "left": _balanced(depth - 1), "right": _balanced(depth - 1)}

    # 2^13 - 1 = 8191 nodes; max traversal depth = 12 < MAX_DEPTH (64)
    node = _balanced(12)
    with pytest.raises(tree.ExpressionTreeError, match="длиннее"):
        tree.validate_tree(node)


def test_validate_number_without_numeric_value() -> None:
    with pytest.raises(tree.ExpressionTreeError, match="value"):
        tree.validate_tree({"kind": "number", "value": "not-a-number"})


def test_validate_symbol_without_name() -> None:
    with pytest.raises(tree.ExpressionTreeError, match="name"):
        tree.validate_tree({"kind": "symbol", "name": ""})


def test_validate_call_unknown_function() -> None:
    node = {"kind": "call", "function": "unknown", "args": [{"kind": "symbol", "name": "x"}]}
    with pytest.raises(tree.ExpressionTreeError, match="функция"):
        tree.validate_tree(node)


def test_validate_call_no_args() -> None:
    node = {"kind": "call", "function": "sqrt", "args": []}
    with pytest.raises(tree.ExpressionTreeError, match="аргументов"):
        tree.validate_tree(node)


def test_validate_unknown_kind() -> None:
    with pytest.raises(tree.ExpressionTreeError, match="вид узла"):
        tree.validate_tree({"kind": "custom_node"})
