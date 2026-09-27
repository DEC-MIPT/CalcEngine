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
        ("ΣТ", "Sigma_t", "\\Sigma_{\\text{Т}}"),
        ("Gп", "G_p", "G_{\\text{п}}"),
        ("Кп", "k_p", "\\text{К}_{\\text{п}}"),
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
        ("Кп = 1,15", "k_p", "\\text{К}_{\\text{п}}"),
        ("К = 0,5", "k", "\\text{К}"),
    ],
)
def test_normalize_symbol_strips_value(raw: str, ident: str, latex: str) -> None:
    assert symbols.normalize_symbol(raw) == (ident, latex)


def test_math_alphanumeric_nfkc() -> None:
    assert symbols.normalize_symbol("𝑞𝑠") == ("q_s", "q_{s}")


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
    ],
)
def test_split_symbols(raw: str, parts: list[str]) -> None:
    assert symbols.split_symbols(raw) == parts
