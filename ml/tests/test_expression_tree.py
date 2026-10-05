"""Тесты дерева выражения каталога (раздел 2.2)."""

from __future__ import annotations

import pytest

from normatives_pipeline.formulas import expression_tree as tree

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
