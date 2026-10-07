"""Вписывание эталонного текста в графы основной надписи (``report-title-block-limits``).

Текст раскладывается по ширинам глифов Liberation Sans 2.1.5, метрически совместимого с
Arial, жадным переносом по пробелам, как Word и LibreOffice переносят абзац без расстановки
переносов: слово, не влезающее в остаток строки, уходит на следующую, а слово длиннее строки
рвётся внутри (design.md, решение 3).
"""

import json
from pathlib import Path

import pytest

from app.reporting import capacity
from app.reporting.capacity import (
    LINE_HEIGHT_EM,
    PT_MM,
    SINGLE_LINE_COLUMNS,
    cell_extent_mm,
    column_capacity,
    column_cells,
    line_count,
)
from app.reporting.title_block import CELL_MARGIN_MM, COLUMN_SIZES_PT

METRICS = json.loads((Path(__file__).parent / "fixtures" / "liberation_sans_metrics.json").read_text(encoding="utf-8"))
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
COLUMNS = ("1", "5", "6", "9", "11")
WORD_LENGTHS = range(5, 15)


def reference_text(limit: int, word_length: int, single_line: bool) -> str:
    """Строит эталонный текст графы по правилу решения 3 design.md."""
    if single_line:
        return "".join(ALPHABET[index % len(ALPHABET)] for index in range(limit)).capitalize()
    words: list[str] = []
    while len(" ".join(words)) < limit:
        start = len(words) * word_length
        letters = "".join(ALPHABET[(start + index) % len(ALPHABET)] for index in range(word_length))
        words.append(letters.capitalize())
    return " ".join(words)[:limit].rstrip(" ")


def advance_mm(character: str, size_pt: int) -> float:
    return METRICS["advance_widths"][character] / METRICS["units_per_em"] * size_pt * PT_MM


def lines_needed(text: str, width_mm: float, size_pt: int) -> int:
    """Считает строки, которые займёт текст в строке ширины ``width_mm`` при жадном переносе."""
    lines, used = 1, 0.0
    for word in text.split(" "):
        word_mm = sum(advance_mm(character, size_pt) for character in word)
        space_mm = advance_mm(" ", size_pt)
        if used and used + space_mm + word_mm <= width_mm:
            used += space_mm + word_mm
            continue
        if used:
            lines, used = lines + 1, 0.0
        for character in word:
            character_mm = advance_mm(character, size_pt)
            if used and used + character_mm > width_mm:
                lines, used = lines + 1, 0.0
            used += character_mm
    return lines


def overflows() -> list[tuple[str, int, int]]:
    """Перечисляет (графа, длина слова, ячейка) эталонных текстов, не влезших в ячейку на лимите."""
    found: list[tuple[str, int, int]] = []
    for column in COLUMNS:
        size, single = COLUMN_SIZES_PT[column], column in SINGLE_LINE_COLUMNS
        limit = column_capacity(column)
        for word_length in WORD_LENGTHS:
            text = reference_text(limit, word_length, single)
            for index, (form, cell) in enumerate(column_cells(column)):
                width, height = cell_extent_mm(form, cell)
                if lines_needed(text, width - 2 * CELL_MARGIN_MM, size) > line_count(height, size, single):
                    found.append((column, word_length, index))
    return found


def test_the_fixture_is_the_font_of_the_design() -> None:
    assert METRICS["font"] == "Liberation Sans"
    assert METRICS["version"] == "Version 2.1.5"
    assert set(METRICS["advance_widths"]) == {" ", *ALPHABET, *ALPHABET.upper()}


def test_the_line_height_is_the_hhea_sum_of_the_font() -> None:
    hhea = METRICS["hhea"]

    assert LINE_HEIGHT_EM == (hhea["ascender"] + hhea["descender"] + hhea["line_gap"]) / METRICS["units_per_em"]


def test_the_reference_text_follows_the_rule_of_the_design() -> None:
    assert reference_text(30, 5, single_line=False).startswith("Абвгд Ежзий Клмно Прсту Фхцчш")
    assert reference_text(7, 5, single_line=True) == "Абвгдеж"
    assert reference_text(11, 5, single_line=True) == "Абвгдежзийк"
    assert reference_text(12, 5, single_line=False) == "Абвгд Ежзий"


@pytest.mark.parametrize("column", COLUMNS)
def test_the_reference_text_at_the_limit_fits_every_cell_of_the_column(column: str) -> None:
    assert [overflow for overflow in overflows() if overflow[0] == column] == []


def test_the_reference_width_is_the_smallest_that_fits(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(capacity, "REFERENCE_WIDTH_EM", capacity.REFERENCE_WIDTH_EM - 0.001)

    assert overflows() != []


def test_a_word_longer_than_the_line_is_broken_inside() -> None:
    assert lines_needed("Абвгдежзийклмнопрстуфхцчшщъыьэюя", width_mm=10, size_pt=10) > 1
    assert lines_needed("Абв где", width_mm=100, size_pt=10) == 1
