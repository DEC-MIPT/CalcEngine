"""Юнит-тесты нормализации распознанного LaTeX (correct_latex, _pick_formula_line)."""

from __future__ import annotations

import pytest

from normatives_pipeline.formulas.detect import _pick_formula_line, correct_latex


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (r"\not\sim_{x} = 0.7", r"\sim_{x} = 0.7"),
        (r"F_{\tt B.o} = q", r"F_{ B.o} = q"),
        (r"\beta_{\tt 06}", r"\beta_{ 06}"),
        (r"\mathrm{\tiny{x}}", r"\mathrm{x}"),
        (r"\boldsymbol{y} + \mathit{z}", r"y + z"),
        (r"a \enspace b \qquad c \quad d", r"a b c d"),
        (r"0 , 7 + 1 , 4", r"0.7 + 1.4"),
        (r"q \[ 8 5 8 ]", r"q [ 8 5 8 ]"),
        (r"{} \mu_m = x", r"\mu_m = x"),
        (r"x ~ y \, z \; w \! v", r"x y z w v"),
    ],
)
def test_correct_latex(raw: str, expected: str) -> None:
    assert correct_latex(raw) == expected


def test_correct_latex_keeps_mathrm_semantics() -> None:
    latex = r"N_{\mathrm{T M}}=\sqrt{F_{\mathrm{T M}} / 2}"
    assert "\\mathrm{T M}" in correct_latex(latex)


def test_correct_latex_decimal_comma_in_subscript() -> None:
    assert correct_latex(r"P N \geq\frac{P + P}{1 , 4}") == r"P N \geq\frac{P + P}{1.4}"


def test_correct_latex_array_block_picks_math_line() -> None:
    latex = r"\begin{array}{c} x = 1 + 2 \\ просто текст \end{array}"
    result = correct_latex(latex)
    assert r"\begin{array}" not in result
    assert r"\end{array}" not in result
    assert "x = 1 + 2" in result


def test_correct_latex_array_block_empty_lines_fallback() -> None:
    latex = r"\begin{array}{c} \end{array}"
    result = correct_latex(latex)
    assert r"\begin{array}" not in result


def test_pick_formula_line_selects_most_math_heavy() -> None:
    lines = ["просто текст", "x = y + z / 2", "a + b"]
    assert _pick_formula_line(lines) == "x = y + z / 2"


def test_pick_formula_line_empty_returns_empty_string() -> None:
    assert _pick_formula_line([]) == ""


def test_pick_formula_line_single_element() -> None:
    assert _pick_formula_line(["a = b"]) == "a = b"
