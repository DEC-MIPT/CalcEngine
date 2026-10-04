"""Юнит-тесты нормализации распознанного LaTeX (correct_latex)."""

from __future__ import annotations

import pytest

from normatives_pipeline.formulas.detect import correct_latex


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
