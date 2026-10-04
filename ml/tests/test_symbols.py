"""Нормализация символов обозначений: юнит-тесты."""

from __future__ import annotations

import pytest

from normatives_pipeline.parser import symbols


@pytest.mark.parametrize(
    ("raw", "ident", "latex"),
    [
        ("γc1", "gamma_c1", "\\gamma_{c1}"),
        ("γc2", "gamma_c2", "\\gamma_{c2}"),
        ("γg", "gamma_g", "\\gamma_{g}"),
        ("Δp", "Delta_p", "\\Delta_{p}"),
        ("ΣТ", "Sigma_T_cyr", "\\Sigma_{\\text{Т}}"),
        ("Gп", "G_p_cyr", "G_{\\text{п}}"),
        ("Кп", "K_p_cyr", "\\text{К}_{\\text{п}}"),
        ("qs", "q_s", "q_{s}"),
        ("k", "k", "k"),
        ("b´", "b_pr", "b'"),
        ("R´0", "R_0_pr", "R_{0}'"),
    ],
)
def test_normalize_symbol(raw: str, ident: str, latex: str) -> None:
    assert symbols.normalize_symbol(raw) == (ident, latex)


@pytest.mark.parametrize(
    ("raw", "ident", "latex"),
    [
        ("Кп = 1,15", "K_p_cyr", "\\text{К}_{\\text{п}}"),
        ("К = 0,5", "K_cyr", "\\text{К}"),
    ],
)
def test_normalize_symbol_strips_value(raw: str, ident: str, latex: str) -> None:
    assert symbols.normalize_symbol(raw) == (ident, latex)


def test_math_alphanumeric_nfkc() -> None:
    assert symbols.normalize_symbol("𝑞𝑠") == ("q_s", "q_{s}")


@pytest.mark.parametrize(
    ("latin", "cyrillic"),
    [
        ("a", "а"),
        ("a", "А"),
        ("s", "с"),
        ("s", "С"),
        ("e", "е"),
        ("k", "к"),
        ("K", "К"),
        ("r", "р"),
        ("y", "у"),
    ],
)
def test_cyrillic_id_does_not_collide_with_latin(latin: str, cyrillic: str) -> None:
    lat = symbols.normalize_symbol(latin)
    cyr = symbols.normalize_symbol(cyrillic)
    assert lat is not None and cyr is not None
    assert lat[1] != cyr[1]
    assert lat[0] != cyr[0]
    assert cyr[0].endswith(symbols.CYR_SUFFIX)


@pytest.mark.parametrize(("lower", "upper"), [("а", "А"), ("с", "С"), ("е", "Е")])
def test_cyrillic_case_is_preserved(lower: str, upper: str) -> None:
    lo = symbols.normalize_symbol(lower)
    up = symbols.normalize_symbol(upper)
    assert lo is not None and up is not None
    assert lo[0] != up[0]
    assert lo[1] != up[1]


def test_cyrillic_without_translit_gets_hex_id() -> None:
    assert symbols.normalize_symbol("ё") == ("u0451_cyr", "\\text{ё}")


@pytest.mark.parametrize(
    "raw",
    ["", "   ", "123", "Таблица Б.1", "песков мелких и пылеватых"],
)
def test_normalize_symbol_rejects_garbage(raw: str) -> None:
    assert symbols.normalize_symbol(raw) is None


@pytest.mark.parametrize(
    ("raw", "parts"),
    [
        ("N, A, γmt, W", ["N", "A", "γmt", "W"]),
        ("Na и Ma", ["Na", "Ma"]),
        ("ξq, ξc, ξγ", ["ξq", "ξc", "ξγ"]),
        ("b´ и l´", ["b´", "l´"]),
        ("ssl,g и Δssl,g", ["ssl,g", "Δssl,g"]),
        ("hn,p и hsat,p", ["hn,p", "hsat,p"]),
        ("σzp,i", ["σzp,i"]),
    ],
)
def test_split_symbols(raw: str, parts: list[str]) -> None:
    assert symbols.split_symbols(raw) == parts


def test_split_symbols_keeps_compound_subscript_whole() -> None:
    ident, latex = symbols.normalize_symbol("ssl,g")
    assert latex == "s_{sl,g}"
    assert ident == "s_sl_g"
