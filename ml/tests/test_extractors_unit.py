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


def test_extract_formulas_rejects_figure_label() -> None:
    # "d0(1)" at end of line is a figure label, not a formula number — must not match.
    page = (
        "6.3.12 Схема для расчета рассоления основания\n"
        "                                       d0(1)\n"
        "                                       d0(2)\n"
        "                                       d0(3)\n"
        "1 – граница слоёв; 2 – расчётный слой; 3 – расчётный слой\n"
    )
    formulas = extractors.extract_formulas([page])
    assert formulas == [], f"ложные позитивы: {[f.number for f in formulas]}"


def test_extract_formulas_accepts_standalone_integer_number() -> None:
    # " (1)" preceded by whitespace is a real formula number.
    page = (
        "3.1 Определение\n"
        "Величину вычисляют по формуле\n"
        "    s = a + b                                        (1)\n"
        "где a – первое слагаемое; b – второе слагаемое.\n"
    )
    formulas = extractors.extract_formulas([page])
    assert any(f.number == "1" for f in formulas), f"номер не найден: {[f.number for f in formulas]}"


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


def test_extract_notation() -> None:
    entries = extractors.extract_notation(["X – нормативное значение характеристики\n"])
    assert [e.symbol for e in entries] == ["X"]


def test_extract_table_refs() -> None:
    assert extractors.extract_table_refs("по таблице 5.5 и таблицы 7.2") == ["5.5", "7.2"]


def test_caption_search_and_line() -> None:
    assert extractors._caption_search("см. Таблица 5.5 ниже") == "5.5"
    assert extractors._caption_search("нет подписи") == ""
    assert extractors._caption_line("Таблица 7.2") == "7.2"
    assert extractors._caption_line("см. Таблица 7.2") == ""
    assert extractors._caption_line("шапка\nТаблица 7.2\n") == "7.2"


class _Crop:
    def __init__(self, text: str) -> None:
        self._text = text

    def extract_text(self) -> str:
        return self._text


class _Page:
    width = 100
    height = 200

    def __init__(self, text: str) -> None:
        self._text = text

    def within_bbox(self, bbox: tuple) -> _Crop:
        return _Crop(self._text)


def test_table_caption_from_page_and_previous_page() -> None:
    assert extractors._table_caption(_Page("Таблица 5.5"), (0, 50, 100, 100)) == "5.5"
    without = _Page("без подписи")
    assert extractors._table_caption(without, (0, 50, 100, 100)) == ""
    assert (
        extractors._table_caption(without, (0, 50, 100, 100), _Page("хвост\nТаблица 7.2"))
        == "7.2"
    )


def test_table_caption_negative_top_returns_empty() -> None:
    page = _Page("Таблица 5.5")
    assert extractors._table_caption(page, (0, -30.6, 595, 200)) == ""
    assert extractors._table_caption(page, (0, 0.0, 595, 200)) == ""


def test_unnumbered_skips_non_formula_lines() -> None:
    pages = ["где X – значение\n", ("а" * 200) + "\nгде Y – значение\n"]
    clauses = extractors.extract_clauses(pages)
    formulas, _ = extractors.extract_unnumbered_formulas(pages, clauses)
    assert formulas == []
