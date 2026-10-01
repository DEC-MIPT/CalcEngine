from io import BytesIO

import pytest
from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Length, Mm
from test_reporting_model import report

from app.reporting.docx_writer import render_docx
from app.reporting.layout import (
    BODY_INDENT_MM,
    FRAME_LINE_MM,
    FRAME_MM,
    SHEET_MM,
    body_width_mm,
)


@pytest.fixture(scope="module")
def document() -> DocumentObject:
    return Document(BytesIO(render_docx(report())))


def mm(length: int | None) -> float:
    assert length is not None
    return round(Length(length).mm, 1)


def exact_mm(length: int | None) -> float:
    assert length is not None
    return Length(length).mm


def test_the_sheet_is_a4_portrait(document: DocumentObject) -> None:
    section = document.sections[0]

    assert section.orientation == WD_ORIENT.PORTRAIT
    assert (mm(section.page_width), mm(section.page_height)) == SHEET_MM


def test_the_middle_of_the_frame_line_lies_on_the_frame(document: DocumentObject) -> None:
    section = document.sections[0]

    margins = {
        "left": exact_mm(section.left_margin),
        "top": exact_mm(section.top_margin),
        "right": exact_mm(section.right_margin),
        "bottom": exact_mm(section.bottom_margin),
    }
    middles = {side: margin - FRAME_LINE_MM / 2 for side, margin in margins.items()}
    assert middles == pytest.approx(dict(FRAME_MM), abs=0.01)
    assert FRAME_LINE_MM == pytest.approx(0.529, abs=0.001)
    assert exact_mm(section.header_distance) == pytest.approx(margins["top"], abs=0.01)
    assert SHEET_MM[0] - middles["left"] - middles["right"] == pytest.approx(185, abs=0.01)


def test_the_frame_is_a_page_border_on_the_edge_of_the_text_area_open_at_the_bottom(document: DocumentObject) -> None:
    properties = document.sections[0]._sectPr
    borders = properties.find(qn("w:pgBorders"))

    assert borders is not None
    assert borders.getprevious() is properties.find(qn("w:pgMar"))
    assert borders.get(qn("w:offsetFrom")) == "text"
    sides = {child.tag.split("}")[1]: (child.get(qn("w:val")), child.get(qn("w:space"))) for child in borders}
    assert sides == {"top": ("single", "0"), "left": ("single", "0"), "bottom": ("nil", "0"), "right": ("single", "0")}


def test_body_text_and_tables_keep_off_the_frame(document: DocumentObject) -> None:
    normal = document.styles["Normal"].paragraph_format
    table = document.tables[0]._tbl.tblPr
    indent = table.find(qn("w:tblInd"))

    assert (mm(normal.left_indent), mm(normal.right_indent)) == (BODY_INDENT_MM, BODY_INDENT_MM)
    assert indent is not None and int(indent.get(qn("w:w"))) == Mm(BODY_INDENT_MM).twips
    assert list(table).index(indent) < list(table).index(table.find(qn("w:tblLook")))


def test_a_body_table_is_as_wide_as_the_text_inside_the_frame(document: DocumentObject) -> None:
    table = document.tables[0]

    widths = [mm(cell.width) for cell in table.rows[1].cells]
    assert sum(widths) == pytest.approx(body_width_mm(), abs=0.2)
    assert body_width_mm() == pytest.approx(175 - FRAME_LINE_MM, abs=1e-9)


@pytest.mark.parametrize("which", ["first_page_header", "header"])
def test_an_empty_line_in_the_header_keeps_the_first_line_off_the_top_frame_line(
    document: DocumentObject, which: str
) -> None:
    header = getattr(document.sections[0], which)
    line = header.paragraphs[0].paragraph_format

    assert [paragraph.text for paragraph in header.paragraphs] == [""]
    assert not header.tables
    assert line.line_spacing_rule == WD_LINE_SPACING.EXACTLY
    assert isinstance(line.line_spacing, Length)
    assert line.line_spacing.mm == pytest.approx(BODY_INDENT_MM, abs=0.01)
    assert (mm(line.left_indent), mm(line.right_indent)) == (0.0, 0.0)
