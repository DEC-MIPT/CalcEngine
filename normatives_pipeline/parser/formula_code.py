"""Формула → исполняемый код: надёжное решение + менее валидные альтернативы."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from sympy import Expr, Symbol, lambdify
from sympy.parsing.latex import parse_latex


@dataclass(frozen=True)
class BoundFormula:
    latex: str
    expr: Expr
    symbols: tuple[Symbol, ...]

    def as_callable(self) -> Callable[..., float]:
        return lambdify(self.symbols, self.expr)


def demo_formula_5_7() -> BoundFormula:
    """Расчётное сопротивление грунта R (СП 22.13330.2016, формула 5.7).

    Надёжное представление: явная таблица символов + детерминированное построение
    выражения (без eval и без parse_latex).
    """
    g_c1 = Symbol("gamma_c1")
    g_c2 = Symbol("gamma_c2")
    k = Symbol("k")
    m_g = Symbol("M_gamma")
    k_z = Symbol("k_z")
    b = Symbol("b")
    g_ii = Symbol("gamma_II")
    m_q = Symbol("M_q")
    d_1 = Symbol("d_1")
    g_ii_p = Symbol("gamma_II_prime")
    d_b = Symbol("d_b")
    m_c = Symbol("M_c")
    c_ii = Symbol("c_II")

    expr = (g_c1 * g_c2 / k) * (
        m_g * k_z * b * g_ii
        + m_q * d_1 * g_ii_p
        + (m_q - 1) * d_b * g_ii_p
        + m_c * c_ii
    )
    latex = (
        r"R = \frac{\gamma_{c1}\gamma_{c2}}{k}\left["
        r"M_{\gamma} k_z b \gamma_{II} + M_q d_1 \gamma'_{II} "
        r"+ (M_q - 1) d_b \gamma'_{II} + M_c c_{II}\right]"
    )
    return BoundFormula(
        latex=latex,
        expr=expr,
        symbols=(g_c1, g_c2, k, m_g, k_z, b, g_ii, m_q, d_1, g_ii_p, d_b, m_c, c_ii),
    )


def alternative_parse_latex(latex: str) -> Expr:
    """Менее валидно: наивный parse_latex.

    Теряет многосимвольные индексы: \\gamma_{c1} → c*1, \\gamma_{II} → I*I.
    """
    return parse_latex(latex)


def alternative_latex_only(latex: str) -> str:
    """Менее валидно: только LaTeX, без исполнения."""
    return latex


def alternative_codegen(expr: Expr) -> str:
    """Менее валидно: строка Python-кода (опасна при eval)."""
    return str(expr)
