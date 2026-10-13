"""Unit tests for latex_reconstruct pure functions (coverage gap closure).

Tests target specific uncovered branches without requiring a real PDF page.
All functions tested here are deterministic and operate on plain char-dicts.
"""
from __future__ import annotations

from normatives_pipeline.parser.latex_reconstruct import (
    _assemble,
    _char_at,
    _has_rel,
    _line_latex,
    _marker,
    _slashes,
    _sum_groups,
    base_char,
    transliterate,
)


def _ch(text: str, x0: float = 0.0, top: float = 0.0, size: float = 10.0) -> dict:
    return {
        "text": text,
        "x0": x0,
        "x1": x0 + size * 0.6,
        "top": top,
        "bottom": top + size,
        "size": size,
        "height": size,
        "width": size * 0.6,
    }


# ---------------------------------------------------------------------------
# base_char: PUA / Latin lookalike / acute accent (lines 69, 71, 75)
# ---------------------------------------------------------------------------


def test_base_char_acute_accent() -> None:
    # U+00B4 ACUTE ACCENT — Adobe Symbol maps to prime superscript
    assert base_char(chr(0x00B4)) == "^{\\prime}"


def test_base_char_pua_leq() -> None:
    # U+F0A3 — Adobe Symbol PUA: less-or-equal sign
    assert base_char(chr(0xF0A3)) == "\\leq "


def test_base_char_latin_lookalike() -> None:
    # U+F041 — Adobe Symbol PUA: Latin capital A lookalike
    assert base_char(chr(0xF041)) == "A"


# ---------------------------------------------------------------------------
# transliterate: uppercase Cyrillic branch (line 88)
# ---------------------------------------------------------------------------


def test_transliterate_uppercase_cyrillic() -> None:
    result = transliterate("Б")  # Б
    assert result and result[0].isupper()


def test_transliterate_lowercase_unchanged_in_case() -> None:
    result = transliterate("б")  # б
    assert result == result.lower()


# ---------------------------------------------------------------------------
# _char_at: beyond-end -> None (line 120)
# ---------------------------------------------------------------------------


def test_char_at_beyond_end_returns_none() -> None:
    row = [{"text": "abc"}]
    assert _char_at(row, 5) is None


def test_char_at_zero_returns_first() -> None:
    c = {"text": "x"}
    assert _char_at([c], 0) is c


# ---------------------------------------------------------------------------
# _assemble: empty input -> "" (line 161)
# ---------------------------------------------------------------------------


def test_assemble_empty_list() -> None:
    assert _assemble([]) == ""


def test_assemble_whitespace_only() -> None:
    assert _assemble([_ch(" "), _ch("\t")]) == ""


# ---------------------------------------------------------------------------
# _marker: _char_at returns None -> continue (line 134, also covers line 120)
# ---------------------------------------------------------------------------


def test_marker_skips_when_char_at_returns_none() -> None:
    # Multi-char text element: target "(5)" is found at text index 1, but
    # _char_at on a single 4-char element returns None for idx=1.
    big = {
        "text": "x(5)",
        "x0": 10.0, "x1": 50.0,
        "top": 50.0, "bottom": 60.0,
        "size": 10.0, "height": 10.0, "width": 40.0,
    }
    assert _marker([big], "5") is None


# ---------------------------------------------------------------------------
# _slashes: w <= 0 -> continue (line 200)
# ---------------------------------------------------------------------------


class _MockPage:
    def __init__(self, rects=None, lines_=None):
        self.rects = rects or []
        self.lines = lines_ or []


def test_slashes_skips_zero_width_segment() -> None:
    # Hits line 198: w <= 0 branch
    zero_w = {"width": 0, "height": 10, "top": 5, "x0": 70, "x1": 70}
    page = _MockPage(rects=[zero_w])
    assert _slashes(page, 0, 20, 60, 200) == []


def test_slashes_skips_bad_aspect_ratio() -> None:
    # Hits line 200: w/h > 0.9 branch (too square, not a diagonal stroke)
    bad_ratio = {"width": 10, "height": 10, "top": 5, "x0": 70, "x1": 80}
    page = _MockPage(rects=[bad_ratio])
    assert _slashes(page, 0, 20, 60, 200) == []


def test_slashes_accepts_valid_diagonal() -> None:
    valid = {"width": 5, "height": 12, "top": 5, "x0": 70, "x1": 75}
    page = _MockPage(rects=[valid])
    result = _slashes(page, 0, 20, 60, 200)
    assert valid in result


# ---------------------------------------------------------------------------
# _has_rel: True branch (line 268)
# ---------------------------------------------------------------------------


def test_has_rel_true_with_eq() -> None:
    assert _has_rel([_ch("=")])


def test_has_rel_true_with_geq() -> None:
    assert _has_rel([_ch("≥")])  # >=


def test_has_rel_false_no_rel_chars() -> None:
    assert not _has_rel([_ch("a"), _ch("b")])


# ---------------------------------------------------------------------------
# _sum_groups: sub and sup branches (lines 301, 303)
# ---------------------------------------------------------------------------


def test_sum_groups_with_sub_and_sup() -> None:
    # "∑" is in _BIG_TOKENS so _base_size ignores it; need a normal char to
    # establish base_size=10 so that sub/sup at size=6 qualify as small (<8).
    normal = {
        "text": "E",
        "x0": 80.0, "x1": 90.0,
        "top": 50.0, "bottom": 60.0,
        "size": 10.0, "height": 10.0, "width": 10.0,
    }
    s = {
        "text": "∑",
        "x0": 100.0, "x1": 114.0,
        "top": 50.0, "bottom": 66.0,
        "size": 14.0, "height": 14.0, "width": 14.0,
    }
    sub_ch = {
        "text": "i",
        "x0": 104.0, "x1": 110.0,
        "top": 68.0, "bottom": 74.0,
        "size": 6.0, "height": 6.0, "width": 6.0,
    }
    sup_ch = {
        "text": "n",
        "x0": 104.0, "x1": 110.0,
        "top": 38.0, "bottom": 44.0,
        "size": 6.0, "height": 6.0, "width": 6.0,
    }
    band = [normal, s, sub_ch, sup_ch]
    result = _sum_groups(band, set())
    assert len(result) == 1
    _x, _y, latex, _used = result[0]
    assert "_{" in latex
    assert "^{" in latex


def test_sum_groups_sub_only() -> None:
    normal = {
        "text": "E",
        "x0": 80.0, "x1": 90.0,
        "top": 50.0, "bottom": 60.0,
        "size": 10.0, "height": 10.0, "width": 10.0,
    }
    s = {
        "text": "∑",
        "x0": 100.0, "x1": 114.0,
        "top": 50.0, "bottom": 66.0,
        "size": 14.0, "height": 14.0, "width": 14.0,
    }
    sub_ch = {
        "text": "i",
        "x0": 104.0, "x1": 110.0,
        "top": 68.0, "bottom": 74.0,
        "size": 6.0, "height": 6.0, "width": 6.0,
    }
    result = _sum_groups([normal, s, sub_ch], set())
    assert "_{" in result[0][2]
    assert "^{" not in result[0][2]


# ---------------------------------------------------------------------------
# _line_latex: trailing fracs appended after char loop (lines 388-389)
# ---------------------------------------------------------------------------


def test_line_latex_trailing_fraction() -> None:
    # fraction at x=200, beyond all chars; fires the trailing while loop
    line = {"top": 50.0, "chars": [_ch("A", x0=100.0, top=50.0)]}
    fraction = [(200.0, 50.0, "\\frac{a}{b}")]
    result = _line_latex(line, [], fraction)
    assert "\\frac{a}{b}" in result


def test_line_latex_two_trailing_fractions() -> None:
    # Both fractions have x > all char x1 values; both are appended by trailing while.
    line = {"top": 50.0, "chars": [_ch("A", x0=100.0, top=50.0)]}
    fraction = [(200.0, 50.0, "\\frac{a}{b}"), (220.0, 50.0, "\\frac{c}{d}")]
    result = _line_latex(line, [], fraction)
    assert "\\frac{a}{b}" in result
    assert "\\frac{c}{d}" in result
