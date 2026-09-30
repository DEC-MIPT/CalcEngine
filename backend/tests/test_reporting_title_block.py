from io import BytesIO

import pytest
from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.shared import Length, Mm
from docx.table import Table
from test_reporting_model import report

from app.reporting.docx_writer import render_docx
from app.reporting.layout import FRAME_MM, SHEET_MM
from app.reporting.model import TraceSection
from app.reporting.title_block import (
    CHANGE_CELLS,
    FORM5_CAPTIONS,
    FORM5_COLUMNS,
    FORM5_MERGES,
    FORM5_ROWS,
    FORM5_WIDTHS_MM,
    FORM6_CAPTIONS,
    FORM6_CHANGE_CELLS,
    FORM6_COLUMNS,
    FORM6_MERGES,
    FORM6_ROW_HEIGHTS_MM,
    FORM6_WIDTHS_MM,
    ROW_HEIGHT_MM,
)
from app.schemas.report import TitleBlockData


@pytest.fixture(scope="module")
def document() -> DocumentObject:
    return Document(BytesIO(render_docx(report())))


@pytest.fixture(scope="module")
def form5(document: DocumentObject) -> Table:
    tables = document.sections[0].first_page_footer.tables
    assert len(tables) == 1
    return tables[0]


def mm(length: int | None) -> float:
    assert length is not None
    return round(Length(length).mm, 1)


def test_the_first_sheet_has_its_own_footer(document: DocumentObject) -> None:
    section = document.sections[0]

    assert section.different_first_page_header_footer
    assert not section.first_page_footer.is_linked_to_previous


def test_the_column_widths_add_up_to_the_width_of_the_form(form5: Table) -> None:
    grid = [mm(int(column.get(qn("w:w"))) * 635) for column in form5._tbl.tblGrid.findall(qn("w:gridCol"))]

    assert grid == [float(width) for width in FORM5_WIDTHS_MM]
    assert sum(FORM5_WIDTHS_MM) == 185
    assert sum(FORM5_WIDTHS_MM) == SHEET_MM[0] - FRAME_MM["left"] - FRAME_MM["right"]


def test_every_row_has_the_height_of_the_figure(form5: Table) -> None:
    assert len(form5.rows) == FORM5_ROWS
    assert {(mm(row.height), row.height_rule) for row in form5.rows} == {
        (float(ROW_HEIGHT_MM), WD_ROW_HEIGHT_RULE.EXACTLY)
    }
    assert FORM5_ROWS * ROW_HEIGHT_MM == 40


def test_the_form_holds_its_captions(form5: Table) -> None:
    captions = {position: form5.cell(*position).text for position in FORM5_CAPTIONS}

    assert captions == dict(FORM5_CAPTIONS)


def test_merged_cells_cover_their_rectangles(form5: Table) -> None:
    for first_row, first_column, last_row, last_column in FORM5_MERGES:
        corner = form5.cell(first_row, first_column)._tc
        covered = {
            form5.cell(row, column)._tc
            for row in range(first_row, last_row + 1)
            for column in range(first_column, last_column + 1)
        }
        assert covered == {corner}


def test_the_data_columns_are_distinct_cells(form5: Table) -> None:
    cells = [form5.cell(*position)._tc for position in FORM5_COLUMNS.values()]

    assert len({id(cell) for cell in cells}) == len(FORM5_COLUMNS)
    assert form5.cell(0, 6)._tc is form5.cell(2, 9)._tc
    assert form5.cell(5, 7)._tc is form5.cell(7, 9)._tc


def test_columns_14_to_19_are_empty(form5: Table) -> None:
    assert [form5.cell(*position).text for position in CHANGE_CELLS] == [""] * 12


def test_column_26_holds_the_format_under_the_lower_frame_line(document: DocumentObject) -> None:
    paragraph = document.sections[0].first_page_footer.paragraphs[0]
    frame = paragraph._p.pPr.find(qn("w:framePr"))

    assert paragraph.text == "Формат А4"
    assert frame is not None
    assert (frame.get(qn("w:hAnchor")), frame.get(qn("w:vAnchor"))) == ("page", "page")
    assert int(frame.get(qn("w:y"))) == Mm(SHEET_MM[1] - FRAME_MM["bottom"]).twips


def test_the_form_text_is_not_indented_like_the_body(form5: Table) -> None:
    paragraph = form5.cell(2, 0).paragraphs[0]

    assert paragraph.style is not None and paragraph.style.name == "DEC Title Block"
    assert mm(paragraph.style.paragraph_format.left_indent) == 0.0


TITLE = TitleBlockData(
    designation="<DESIGNATION>", document_name="<DOCUMENT>", documentation_kind="<KIND>", organization="<ORG>"
)


@pytest.fixture(scope="module")
def filled_document() -> DocumentObject:
    model = report()
    request = model.request.model_copy(update={"title": TITLE})
    return Document(BytesIO(render_docx(model.model_copy(update={"request": request}))))


@pytest.fixture(scope="module")
def filled(filled_document: DocumentObject) -> Table:
    return filled_document.sections[0].first_page_footer.tables[0]


def test_each_datum_is_in_its_column(filled: Table) -> None:
    texts = {column: filled.cell(*FORM5_COLUMNS[column]).text for column in ("1", "5", "6", "9")}

    assert texts == {"1": "<DESIGNATION>", "5": "<DOCUMENT>", "6": "<KIND>", "9": "<ORG>"}


def test_columns_7_and_8_hold_the_sheet_fields(filled: Table) -> None:
    instructions = {
        column: [field.get(qn("w:instr")).strip() for field in filled.cell(*FORM5_COLUMNS[column])._tc.iter(qn("w:fldSimple"))]
        for column in ("7", "8")
    }

    assert instructions == {"7": ["PAGE"], "8": ["NUMPAGES"]}


def test_an_empty_column_6_prints_nothing(form5: Table) -> None:
    assert form5.cell(*FORM5_COLUMNS["6"]).text == ""


@pytest.fixture(scope="module")
def form6(document: DocumentObject) -> Table:
    tables = document.sections[0].footer.tables
    assert len(tables) == 1
    return tables[0]


def grid_mm(table: Table) -> list[float]:
    return [mm(int(column.get(qn("w:w"))) * 635) for column in table._tbl.tblGrid.findall(qn("w:gridCol"))]


def test_form6_widths_add_up_to_the_width_of_the_form(form6: Table) -> None:
    assert grid_mm(form6) == [float(width) for width in FORM6_WIDTHS_MM]
    assert sum(FORM6_WIDTHS_MM) == 185


def test_form6_rows_make_three_rows_of_5_mm_on_the_left_and_7_and_8_mm_on_the_right(form6: Table) -> None:
    heights = [mm(row.height) for row in form6.rows]

    assert heights == [float(height) for height in FORM6_ROW_HEIGHTS_MM]
    assert (heights[0], heights[1] + heights[2], heights[3]) == (5.0, 5.0, 5.0)
    assert (heights[0] + heights[1], heights[2] + heights[3]) == (7.0, 8.0)
    assert {row.height_rule for row in form6.rows} == {WD_ROW_HEIGHT_RULE.EXACTLY}


def test_form6_holds_its_captions_and_merges(form6: Table) -> None:
    assert {position: form6.cell(*position).text for position in FORM6_CAPTIONS} == dict(FORM6_CAPTIONS)
    for first_row, first_column, last_row, last_column in FORM6_MERGES:
        covered = {
            form6.cell(row, column)._tc
            for row in range(first_row, last_row + 1)
            for column in range(first_column, last_column + 1)
        }
        assert covered == {form6.cell(first_row, first_column)._tc}


def test_form6_carries_column_1_and_the_sheet_number(filled_document: DocumentObject) -> None:
    table = filled_document.sections[0].footer.tables[0]
    fields = [field.get(qn("w:instr")).strip() for field in table.cell(*FORM6_COLUMNS["7"])._tc.iter(qn("w:fldSimple"))]

    assert table.cell(*FORM6_COLUMNS["1"]).text == "<DESIGNATION>"
    assert fields == ["PAGE"]
    assert [table.cell(*position).text for position in FORM6_CHANGE_CELLS] == [""] * 12


def test_the_following_sheets_have_column_26_too(document: DocumentObject) -> None:
    paragraph = document.sections[0].footer.paragraphs[0]

    assert paragraph.text == "Формат А4"
    assert paragraph._p.pPr.find(qn("w:framePr")) is not None


def test_a_report_of_two_sheets_or_more_renders_with_both_forms() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)
    steps = tuple(trace.steps[7].model_copy(update={"step_id": f"s{index}"}) for index in range(60))
    long = model.model_copy(update={"body": (model.body[0], trace.model_copy(update={"steps": steps}), model.body[2])})

    section = Document(BytesIO(render_docx(long))).sections[0]

    assert [len(section.first_page_footer.tables), len(section.footer.tables)] == [1, 1]
    assert len(section.footer.tables[0].columns) == len(FORM6_WIDTHS_MM)
