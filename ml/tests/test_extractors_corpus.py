"""Извлечение по всем неисторическим документам (сканы исключены)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from normatives_pipeline.parser import extractors, symbols, text_layer

REPO = Path(__file__).resolve().parents[2]
NORM_DOCS = REPO / "docs/normative-base"

CURRENT_DOCS = [
    "СП 22.13330.2016.pdf",
    "СП 24.13330.2021.pdf",
    "СП 30.13330.2020.pdf",
    "СП 31.13330.2021.pdf",
    "СП 45.13330.2017.pdf",
]


@pytest.fixture(scope="session")
def corpus_pages() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for filename in CURRENT_DOCS:
        path = NORM_DOCS / filename
        if not path.exists():
            pytest.skip(f"нет файла: {path}")
        result[filename] = text_layer.read_pages(path)
    return result


@pytest.mark.parametrize("filename", CURRENT_DOCS)
def test_clauses_extracted(filename: str, corpus_pages: dict[str, list[str]]) -> None:
    clauses = extractors.extract_clauses(corpus_pages[filename])
    assert len(clauses) > 0
    for c in clauses:
        assert re.fullmatch(r"\d+(?:\.\d+){1,3}", c.number)
        assert c.text.strip()


@pytest.mark.parametrize("filename", CURRENT_DOCS)
def test_formulas_and_notation_normalized(
    filename: str, corpus_pages: dict[str, list[str]]
) -> None:
    pages = corpus_pages[filename]
    clauses = extractors.extract_clauses(pages)
    numbered = extractors.associate_formulas_to_clauses(
        clauses, extractors.extract_formulas(pages)
    )
    unnumbered, un_notation = extractors.extract_unnumbered_formulas(pages, clauses)
    all_formulas = numbered + unnumbered
    assert len(all_formulas) > 0

    notation = extractors.extract_formula_notation(pages, numbered)
    notation.update(un_notation)

    for f in all_formulas:
        assert f.number
        for n in notation.get(f.number, []):
            for sym in symbols.split_symbols(n.symbol):
                norm = symbols.normalize_symbol(sym)
                if norm is None:
                    continue
                ident, latex = norm
                assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", ident)
                assert latex


def test_numbering_schemes(corpus_pages: dict[str, list[str]]) -> None:
    f22 = extractors.extract_formulas(corpus_pages["СП 22.13330.2016.pdf"])
    assert any(re.fullmatch(r"\d+\.\d+", f.number) for f in f22)

    f30 = extractors.extract_formulas(corpus_pages["СП 30.13330.2020.pdf"])
    assert any(re.fullmatch(r"\d+", f.number) for f in f30)

    p45 = corpus_pages["СП 45.13330.2017.pdf"]
    clauses = extractors.extract_clauses(p45)
    unnumbered, _ = extractors.extract_unnumbered_formulas(p45, clauses)
    assert len(unnumbered) > 0


def test_tables_extracted_with_numbers() -> None:
    path = NORM_DOCS / "СП 22.13330.2016.pdf"
    if not path.exists():
        pytest.skip(f"нет файла: {path}")
    tables = extractors.extract_tables(path)
    assert len(tables) > 0
    numbered = {t.number for t in tables if t.number}
    assert "5.5" in numbered
    t55 = next(t for t in tables if t.number == "5.5")
    assert len(t55.rows) >= 20
