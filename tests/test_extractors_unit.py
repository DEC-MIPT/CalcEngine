"""Юнит-тесты экстракторов на синтетическом тексте (без PDF)."""

from __future__ import annotations

from normatives_pipeline.parser import extractors

PAGES = [
    (
        "5.3 Нормативные и расчетные значения характеристик грунтов\n"
        "5.3.16 Все расчеты оснований следует выполнять с использованием\n"
        "расчетных значений характеристик грунтов X, вычисляемых по формуле\n"
        "X = Xn / γg, (5.1)\n"
        "где Xn – нормативное значение данной характеристики;\n"
        "γg – коэффициент надежности по грунту.\n"
        "\n"
        "Коэффициент устанавливают по ГОСТ 20522.\n"
    ),
    (
        "13.8 Для успешного погружения опускных колодцев должны соблюдать\n"
        "следующее условие:\n"
        "G + Gп ≥ КпΣТ,\n"
        "где G – собственный вес колодца;\n"
        "Gп – дополнительная пригрузка колодца;\n"
        "ΣТ – силы трения стен колодца по грунту.\n"
    ),
]


def test_extract_clauses() -> None:
    clauses = extractors.extract_clauses(PAGES)
    nums = [c.number for c in clauses]
    assert "5.3" in nums
    assert "5.3.16" in nums
    assert "13.8" in nums
    for c in clauses:
        assert c.text
        assert c.page >= 1
        assert c.line >= 0


def test_extract_formulas_numbered() -> None:
    formulas = extractors.extract_formulas(PAGES)
    assert [f.number for f in formulas] == ["5.1"]


def test_associate_formulas_to_clauses() -> None:
    clauses = extractors.extract_clauses(PAGES)
    formulas = extractors.associate_formulas_to_clauses(
        clauses, extractors.extract_formulas(PAGES)
    )
    assert formulas[0].clause == "5.3.16"


def test_extract_formula_notation() -> None:
    clauses = extractors.extract_clauses(PAGES)
    formulas = extractors.associate_formulas_to_clauses(
        clauses, extractors.extract_formulas(PAGES)
    )
    notation = extractors.extract_formula_notation(PAGES, formulas)
    assert [n.symbol for n in notation["5.1"]] == ["Xn", "γg"]


def test_extract_unnumbered_formulas() -> None:
    clauses = extractors.extract_clauses(PAGES)
    formulas, notation = extractors.extract_unnumbered_formulas(PAGES, clauses)
    assert any(f.number.startswith("13.8#") for f in formulas)
    symbols = {s for entries in notation.values() for s in [n.symbol for n in entries]}
    assert {"G", "Gп", "ΣТ"} <= symbols


def test_extract_cross_refs() -> None:
    clauses = extractors.extract_clauses(PAGES)
    refs = extractors.extract_cross_refs(PAGES, clauses)
    assert all(r.ref_type == "gost" for r in refs)
    assert any(r.value == "ГОСТ 20522" for r in refs)
