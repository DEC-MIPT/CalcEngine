import pytest

from app.reporting import capacity
from app.reporting.capacity import (
    SINGLE_LINE_COLUMNS,
    cell_extent_mm,
    characters_per_line,
    column_capacity,
    column_cells,
    line_count,
)
from app.reporting.title_block import (
    COLUMN_SIZES_PT,
    FORM5,
    FORM6,
    SIGNATURE_ROWS,
    row_heights_mm,
)
from app.schemas.report import MAX_LENGTH

CELLS = {
    ("1", "form5"): (120, 15.18, 3, 44),
    ("1", "form6"): (110, 15.00, 3, 41),
    ("5", "form5"): (70, 24.82, 6, 25),
    ("6", "form5"): (15, 5.00, 1, 7),
    ("9", "form5"): (50, 14.82, 5, 26),
    ("11", "form5"): (20, 5.00, 1, 11),
}
"""Ячейки графы: ширина и высота в мм, строки и символы в строке (design.md, решение 4)."""


def name(form: object) -> str:
    return "form5" if form is FORM5 else "form6"


@pytest.mark.parametrize("column", ["1", "5", "6", "9", "11"])
def test_every_cell_of_a_column_has_the_size_lines_and_characters_of_the_design(column: str) -> None:
    for form, cell in column_cells(column):
        width, height, lines, per_line = CELLS[(column, name(form))]
        size = COLUMN_SIZES_PT[column]

        assert cell_extent_mm(form, cell) == pytest.approx((width, height), abs=0.01)
        assert line_count(height, size, column in SINGLE_LINE_COLUMNS) == lines
        assert characters_per_line(width, size) == per_line


def test_the_designation_is_printed_in_both_forms_and_takes_the_smaller_capacity(monkeypatch: pytest.MonkeyPatch) -> None:
    cells = column_cells("1")
    size = COLUMN_SIZES_PT["1"]
    capacities = [
        line_count(height, size, single_line=False) * characters_per_line(width, size)
        for width, height in (cell_extent_mm(form, cell) for form, cell in cells)
    ]

    assert [name(form) for form, _ in cells] == ["form5", "form6"]
    assert capacities == [132, 123]
    assert column_capacity("1") == 123
    monkeypatch.setattr(capacity, "column_cells", lambda column: cells[::-1])
    assert column_capacity("1") == 123


def test_the_surname_cells_are_the_three_signature_rows() -> None:
    cells = column_cells("11")

    assert [cell[0] for _, cell in cells] == list(SIGNATURE_ROWS.values())
    assert {name(form) for form, _ in cells} == {"form5"}


def test_columns_6_and_11_hold_one_line_although_two_would_fit_column_11() -> None:
    _, height = cell_extent_mm(*column_cells("11")[0])

    assert SINGLE_LINE_COLUMNS == {"6", "11"}
    assert line_count(height, COLUMN_SIZES_PT["11"], single_line=False) == 2
    assert line_count(height, COLUMN_SIZES_PT["11"], single_line=True) == 1


def test_the_capacity_of_every_column() -> None:
    assert {column: column_capacity(column) for column in ("1", "5", "6", "9", "11")} == {
        "1": 123,
        "5": 150,
        "6": 7,
        "9": 130,
        "11": 11,
    }


def test_a_cell_without_a_merge_is_one_grid_cell() -> None:
    assert cell_extent_mm(FORM6, (3, 0)) == (10, row_heights_mm(FORM6)[3])


@pytest.mark.parametrize("column", ["1", "5", "6", "9", "11"])
def test_every_schema_limit_is_the_capacity_of_its_column(column: str) -> None:
    assert MAX_LENGTH[column] == column_capacity(column)
