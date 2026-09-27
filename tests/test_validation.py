"""Семантическое сравнение формул: normalize_latex, canonical_latex, formulas_equal."""

from __future__ import annotations

from normatives_pipeline.validation import (
    canonical_latex,
    formulas_equal,
    normalize_latex,
)

ETALON_55 = r"\Delta h \leq a (\mathrm{tg}\,\varphi_I + c_I / p)"
RESULT_55 = r"\Delta h \leq a ( \mathrm{tg} \varphi_{\mathrm{I}}+ c_{\mathrm{I}} / p )"

ETALON_57 = (
    r"R = \frac{\gamma_{c1}\gamma_{c2}}{k}\left["
    r"M_{\gamma} k_z b \gamma_{II} + M_q d_1 \gamma'_{II} "
    r"+ (M_q - 1) d_b \gamma'_{II} + M_c c_{II}\right]"
)
RESULT_57 = (
    r"R={\frac{\gamma_{c 1} \gamma_{c 2}} {k}} \big[ M_{_{\gamma}} k_{_{z}} b "
    r"\gamma_{_{\mathrm{I I}}}+M_{_{q}} d_{_{1}} \gamma_{_{\mathrm{I I}}}^{\prime}"
    r"+\big( M_{_{q}}-1 \big) d_{_{b}} \gamma_{_{\mathrm{I I}}}^{\prime}"
    r"+M_{_{c}} c_{_{\mathrm{I I}}} \big]"
)


def test_formulas_equal_55() -> None:
    assert formulas_equal(ETALON_55, RESULT_55)


def test_formulas_equal_57() -> None:
    assert formulas_equal(ETALON_57, RESULT_57)


def test_formulas_equal_differs() -> None:
    assert not formulas_equal(ETALON_55, ETALON_57)


def test_normalize_latex_strips_cosmetics() -> None:
    assert normalize_latex(r"\mathrm{tg}\,\varphi_I") == r"tg\varphi_I"
    assert normalize_latex(r"\big[ x \big]") == "[x]"
    assert normalize_latex(r"M_{_{\gamma}}") == r"M_{\gamma}"


def test_canonical_latex_returns_value() -> None:
    assert canonical_latex("x + 1") is not None
