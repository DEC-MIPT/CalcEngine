"""Формула → код: надёжный путь (формула 5.7) и альтернативы."""

from __future__ import annotations

from sympy import Symbol

from normatives_pipeline.parser import formula_code


def test_demo_formula_5_7_computes() -> None:
    bound = formula_code.demo_formula_5_7()
    f = bound.as_callable()
    values = [1.25, 1.0, 1.1, 0.5, 1.0, 2.0, 18.0, 3.0, 1.5, 9.0, 1.0, 2.0, 25.0]
    assert round(f(*values), 2) == 143.75


def test_demo_formula_symbols_order() -> None:
    bound = formula_code.demo_formula_5_7()
    assert len(bound.symbols) == 13
    assert bound.symbols[0].name == "gamma_c1"


def test_alternative_latex_only() -> None:
    assert formula_code.alternative_latex_only("x = y") == "x = y"


def test_alternative_codegen() -> None:
    out = formula_code.alternative_codegen(Symbol("a") + Symbol("b"))
    assert out == "a + b"


def test_alternative_parse_latex_runs() -> None:
    expr = formula_code.alternative_parse_latex("\\gamma_{c1}")
    assert expr is not None
