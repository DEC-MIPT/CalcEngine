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


def test_extract_edition_text_with_changes() -> None:
    page = (
        "СП 22.13330.2016 Основания зданий и сооружений. "
        "Актуализированная редакция СНиП 2.02.01-83* "
        "(с Изменениями N 1, 2, 3, 4, 5)\n"
        "Применяется с 17.06.2017 взамен СП 22.13330.2011\n"
    )
    result = text_layer.extract_edition_text([page], "СП 22.13330.2016")
    assert result == "2016 с Изм. N 1, 2, 3, 4, 5"


def test_extract_edition_text_no_changes() -> None:
    page = "СП 22.13330.2016 Основания зданий и сооружений.\n"
    result = text_layer.extract_edition_text([page], "СП 22.13330.2016")
    assert result == "2016"


def test_classify_text_and_scan() -> None:
    assert text_layer.classify(["x" * text_layer.MIN_TEXT_CHARS]) == "text"
    assert text_layer.classify(["мало текста"]) == "scan"


def test_extract_amendments_plural() -> None:
    page = "СП 22.13330.2016\nс Изменениями N 1, 2, 3, 4, 5\nМосква 2016\n"
    assert text_layer.extract_amendments([page]) == ["1", "2", "3", "4", "5"]


def test_extract_amendments_singular() -> None:
    page = "с Изменением N 1\n"
    assert text_layer.extract_amendments([page]) == ["1"]


def test_extract_amendments_none() -> None:
    page = "СВОД ПРАВИЛ  СП 22.13330.2016\nМосква 2016\n"
    assert text_layer.extract_amendments([page]) == []


def test_extract_amendments_searches_up_to_page_5() -> None:
    pages = ["", "", "", "", "с Изменениями N 2, 3\n"]
    assert text_layer.extract_amendments(pages) == ["2", "3"]


def test_extract_amendments_ignores_page_6_and_beyond() -> None:
    pages = [""] * 5 + ["с Изменениями N 1, 2\n"]
    assert text_layer.extract_amendments(pages) == []
