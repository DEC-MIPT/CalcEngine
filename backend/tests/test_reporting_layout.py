from io import BytesIO

import pytest
from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.shared import Length, Mm
from test_reporting_model import report

from app.reporting.docx_writer import render_docx
from app.reporting.layout import BODY_INDENT_MM, FRAME_MM, SHEET_MM, body_width_mm


@pytest.fixture(scope="module")
def document() -> DocumentObject:
    return Document(BytesIO(render_docx(report())))


def mm(length: int | None) -> float:
    assert length is not None
    return round(Length(length).mm, 1)


def test_the_sheet_is_a4_portrait(document: DocumentObject) -> None:
    section = document.sections[0]

    assert section.orientation == WD_ORIENT.PORTRAIT
    assert (mm(section.page_width), mm(section.page_height)) == SHEET_MM


def test_the_margins_and_the_footer_lie_on_the_frame_lines(document: DocumentObject) -> None:
    section = document.sections[0]

    margins = {
        "left": mm(section.left_margin),
        "top": mm(section.top_margin),
        "right": mm(section.right_margin),
        "bottom": mm(section.bottom_margin),
    }
    assert margins == dict(FRAME_MM)
    assert (mm(section.header_distance), mm(section.footer_distance)) == (FRAME_MM["top"], FRAME_MM["bottom"])
    assert mm(section.page_width) - margins["left"] - margins["right"] == 185


def test_the_frame_is_a_page_border_on_the_edge_of_the_text_area(document: DocumentObject) -> None:
    properties = document.sections[0]._sectPr
    borders = properties.find(qn("w:pgBorders"))

    assert borders is not None
    assert borders.getprevious() is properties.find(qn("w:pgMar"))
    assert borders.get(qn("w:offsetFrom")) == "text"
    sides = {child.tag.split("}")[1]: (child.get(qn("w:val")), child.get(qn("w:space"))) for child in borders}
    assert sides == {side: ("single", "0") for side in ("top", "left", "bottom", "right")}


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
    assert body_width_mm() == 175
