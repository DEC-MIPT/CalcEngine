"""Нормализация текста поиска: ё→е, лемматизация, чистка PUA."""

from __future__ import annotations

from types import SimpleNamespace

from normatives_pipeline.retrieval import TfidfIndex, build_formula_items, normalize_text, recall_at_k


def test_yo_normalization() -> None:
    assert normalize_text("Расчётные") == "расчетный"


def test_yo_and_ye_equal() -> None:
    assert normalize_text("расчётные") == normalize_text("расчетные")


def test_lemmatization() -> None:
    assert (
        normalize_text("Расчетные значения характеристик грунтов")
        == "расчетный значение характеристика грунт"
    )


def test_pua_stripped() -> None:
    assert "\uf067" not in normalize_text("\uf067 формула")


def test_tfidf_index_search() -> None:
    idx = TfidfIndex()
    idx.index(
        [
            {"number": "5.1", "text": "формула 5.1 расчетные значения характеристик грунтов"},
            {"number": "7.1", "text": "формула 7.1 выдергивающая сила фундамента"},
        ]
    )
    hits = idx.search("расчетные значения грунтов", k=1)
    assert hits[0].number == "5.1"


def _formula(number, clause, page, latex=""):
    return SimpleNamespace(number=number, clause=clause, page=page, latex=latex)


def _notation(page, meaning):
    return SimpleNamespace(page=page, meaning=meaning)


def _clause(number, text):
    return SimpleNamespace(number=number, text=text)


def test_build_formula_items_basic() -> None:
    formulas = [_formula("5.7", "5.7", page=10, latex="p = \\gamma h")]
    notation = [_notation(page=10, meaning="gamma — удельный вес грунта")]
    clauses = [_clause("5.7", "Расчёт давления грунта")]
    items = build_formula_items(formulas, notation, clauses)
    assert len(items) == 1
    assert items[0]["number"] == "5.7"
    assert "gamma" in items[0]["text"] or "формула" in items[0]["text"]
    assert items[0]["clause"] == "5.7"


def test_build_formula_items_no_clauses() -> None:
    formulas = [_formula("1.1", "1.1", page=1)]
    items = build_formula_items(formulas, [], clauses=None)
    assert len(items) == 1
    assert items[0]["number"] == "1.1"


def test_build_formula_items_clause_mismatch() -> None:
    formulas = [_formula("3.1", clause="3.1", page=5, latex="")]
    clauses = [_clause("9.9", "Другой пункт")]
    items = build_formula_items(formulas, [], clauses)
    assert items[0]["number"] == "3.1"
    assert "9.9" not in items[0]["text"]


def test_recall_at_k_perfect() -> None:
    idx = TfidfIndex()
    idx.index([
        {"number": "5.1", "text": "формула 5.1 давление грунта"},
        {"number": "7.1", "text": "формула 7.1 сила фундамента"},
    ])
    queries = [{"query": "давление грунта", "clause": "5.1"}]
    assert recall_at_k(idx, queries, k=1) == 1.0


def test_recall_at_k_miss() -> None:
    idx = TfidfIndex()
    idx.index([
        {"number": "5.1", "text": "формула 5.1 давление грунта"},
        {"number": "7.1", "text": "формула 7.1 сила фундамента"},
    ])
    queries = [{"query": "давление", "clause": "7.1"}]
    result = recall_at_k(idx, queries, k=1)
    assert 0.0 <= result <= 1.0
