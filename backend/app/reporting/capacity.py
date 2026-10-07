import math

from app.reporting.title_block import (
    CELL_MARGIN_MM,
    COLUMN_SIZES_PT,
    FORM5,
    FORM6,
    SIGNATURE_COLUMNS,
    SIGNATURE_ROWS,
    Form,
    row_heights_mm,
)

LINE_HEIGHT_EM = 2355 / 2048
"""Высота строки одинарного интервала Arial в em: ascender 1854 + descender 434 + line gap 67
таблицы ``hhea`` Liberation Sans Regular 2.1.5 (метрически совместим с Arial) при 2048
единицах на em (``report-title-block-limits`` design.md, решение 3)."""

REFERENCE_WIDTH_EM = 0.753
"""Расчётная ширина символа в em: наименьшая с шагом 0,001 em, при которой эталонный текст
каждой графы на её лимите помещается в ячейку (design.md, решение 3); средняя ширина
прописных А–Я без Ё — 0,726 em. Выбор вёрстки, а не значение нормы."""

SINGLE_LINE_COLUMNS = frozenset({"6", "11"})
"""Графы, текст которых держится в одной строке: вид документа и фамилия (design.md, решение 5)."""

PT_MM = 25.4 / 72


def cell_extent_mm(form: Form, cell: tuple[int, int]) -> tuple[float, float]:
    """Вычисляет ширину и высоту ячейки формы с учётом объединения.

    Args:
        form: сетка формы.
        cell: левая верхняя ячейка (строка, столбец).

    Returns:
        Ширина — сумма ширин столбцов, высота — сумма высот строк из ``row_heights_mm``, в мм.
    """
    last_row, last_column = cell
    for first_row, first_column, merge_row, merge_column in form.merges:
        if (first_row, first_column) == cell:
            last_row, last_column = merge_row, merge_column
    width = sum(form.widths_mm[cell[1] : last_column + 1])
    height = sum(row_heights_mm(form)[cell[0] : last_row + 1])
    return width, height


def line_count(height_mm: float, size_pt: int, single_line: bool) -> int:
    """Вычисляет, сколько строк текста одинарного интервала помещается по высоте ячейки.

    Args:
        height_mm: высота ячейки.
        size_pt: кегль текста.
        single_line: графа держит текст в одной строке.

    Returns:
        Число строк.
    """
    if single_line:
        return 1
    return math.floor(height_mm / (size_pt * PT_MM * LINE_HEIGHT_EM))


def characters_per_line(width_mm: float, size_pt: int) -> int:
    """Вычисляет, сколько символов расчётной ширины помещается в строку ячейки за вычетом её полей.

    Args:
        width_mm: ширина ячейки.
        size_pt: кегль текста.

    Returns:
        Число символов.
    """
    return math.floor((width_mm - 2 * CELL_MARGIN_MM) / (size_pt * PT_MM * REFERENCE_WIDTH_EM))


def column_cells(column: str) -> tuple[tuple[Form, tuple[int, int]], ...]:
    """Перечисляет ячейки, в которых печатается текст графы, во всех формах.

    Args:
        column: номер графы: ``"1"``, ``"5"``, ``"6"``, ``"9"`` или ``"11"``.

    Returns:
        Пары (форма, левая верхняя ячейка).
    """
    if column == "11":
        return tuple((FORM5, (row, SIGNATURE_COLUMNS["11"])) for row in SIGNATURE_ROWS.values())
    return tuple((form, form.columns[column]) for form in (FORM5, FORM6) if column in form.columns)


def column_capacity(column: str) -> int:
    """Вычисляет лимит символов графы: наименьшую вместимость её ячеек (design.md, решения 2-5).

    Args:
        column: номер графы из ``COLUMN_SIZES_PT``.

    Returns:
        Строки, умноженные на символы в строке, для самой тесной ячейки графы.
    """
    size = COLUMN_SIZES_PT[column]
    capacities = []
    for form, cell in column_cells(column):
        width, height = cell_extent_mm(form, cell)
        capacities.append(line_count(height, size, column in SINGLE_LINE_COLUMNS) * characters_per_line(width, size))
    return min(capacities)
