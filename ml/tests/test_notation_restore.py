"""Юнит-тесты восстановления индексов формул по словарю обозначений."""

from __future__ import annotations

import pytest

from normatives_pipeline.formulas.notation_restore import (
    _canon,
    _close,
    _symbol_sub_canon,
    restore_indices,
)


def test_symbol_sub_canon_cyrillic() -> None:
    assert _symbol_sub_canon("Рраб") == "rab"
    assert _symbol_sub_canon("Нз") == "z"
    assert _symbol_sub_canon("vф") == "f"


def test_canon_maps_omoglyphs() -> None:
    assert _canon("pa6") == "pab"
    assert _canon("3") == "z"
    assert _canon("з") == "z"


def test_close_allows_one_error() -> None:
    assert _close("pab", "rab")
    assert not _close("np", "pr")


def test_restore_indices_replaces_translit() -> None:
    latex = r"P N \geq\frac{P_{pa6}+P_{\tau}} {1.4}"
    result = restore_indices(latex, ["Рраб", "P\uf074"])
    assert r"P_{rab}" in result


def test_restore_indices_keeps_non_cyrillic() -> None:
    latex = r"H_{\kappa}=H_{3} a_{3} / 100 + 0.3"
    result = restore_indices(latex, ["Нз", "аз"])
    assert r"H_{\kappa}" in result
    assert r"H_{z}" in result
    assert r"a_{z}" in result


@pytest.mark.parametrize("symbols", [[], None])
def test_restore_indices_no_symbols(symbols: list[str] | None) -> None:
    latex = r"x_{abc} + y"
    assert restore_indices(latex, symbols or []) == latex


def test_symbol_sub_canon_single_char_returns_empty() -> None:
    assert _symbol_sub_canon("P") == ""


def test_close_empty_first_arg_returns_false() -> None:
    assert not _close("", "ab")


def test_close_empty_second_arg_returns_false() -> None:
    assert not _close("ab", "")


def test_restore_indices_no_close_match_inner_loop_exhausted() -> None:
    # "rab" vs "xyz": 3 diffs > 1 → _close returns False → inner loop exits normally
    result = restore_indices(r"P_{xyz}", ["Рраб"])
    assert r"P_{xyz}" in result
