"""Извлечение обозначения и года издания с титульной страницы."""

from __future__ import annotations

from normatives_pipeline.parser import text_layer


def test_extract_designation_from_title_page() -> None:
    page = (
        "МИНИСТЕРСТВО СТРОИТЕЛЬСТВА\n"
        "СВОД ПРАВИЛ  СП 22.13330.2016\n"
        "ОСНОВАНИЯ ЗДАНИЙ И СООРУЖЕНИЙ\n"
        "Москва 2016\n"
    )
    assert text_layer.extract_designation([page]) == "СП 22.13330.2016"


def test_extract_designation_missing() -> None:
    assert text_layer.extract_designation(["текст без обозначения"]) == ""


def test_extract_designation_ignores_other_codes() -> None:
    page = "СНиП 2.02.01-83*\nСП 22.13330.2016\n"
    assert text_layer.extract_designation([page]) == "СП 22.13330.2016"


def test_extract_edition_year() -> None:
    assert text_layer.extract_edition_year("СП 22.13330.2016") == "2016"
    assert text_layer.extract_edition_year("СП 24.13330.2021") == "2021"
    assert text_layer.extract_edition_year("СНиП 2.02.01-83") == ""


def test_extract_edition_year_takes_last_of_several() -> None:
    assert text_layer.extract_edition_year("СП 22.13330.2016 (2019)") == "2019"


def test_classify_text_and_scan() -> None:
    assert text_layer.classify(["x" * text_layer.MIN_TEXT_CHARS]) == "text"
    assert text_layer.classify(["мало текста"]) == "scan"
