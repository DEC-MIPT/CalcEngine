"""Нормализация текста поиска: ё→е, лемматизация, чистка PUA."""

from __future__ import annotations

from normatives_pipeline.retrieval import TfidfIndex, normalize_text


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
