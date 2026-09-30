from types import MappingProxyType

from docx.document import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.oxml.xmlchemy import BaseOxmlElement
from docx.shared import Mm, Pt
from docx.table import Table

SHEET_MM = (210, 297)
"""A4 portrait (GOST R 21.101-2026, edition unverified, Annex Zh, figure Zh.1 a)."""

FRAME_MM: MappingProxyType[str, int] = MappingProxyType(
    {"left": 20, "top": 5, "right": 5, "bottom": 5}
)
"""Distances of the inner frame from the sheet edges, as figure Zh.1 a) shows them."""

FRAME_LINE_EIGHTHS_PT = 12
"""Width of the frame line in eighths of a point; a layout choice, not a norm value."""

BODY_INDENT_MM = 5
BODY_FONT = "Arial"
BODY_SIZE_PT = 12


def _page_borders() -> BaseOxmlElement:
    borders = OxmlElement("w:pgBorders")
    borders.set(qn("w:offsetFrom"), "text")
    for side in ("top", "left", "bottom", "right"):
        line = OxmlElement(f"w:{side}")
        line.set(qn("w:val"), "single")
        line.set(qn("w:sz"), str(FRAME_LINE_EIGHTHS_PT))
        line.set(qn("w:space"), "0")
        line.set(qn("w:color"), "000000")
        borders.append(line)
    return borders


def apply_sheet(document: Document) -> None:
    """A4 portrait with the page margins on the frame lines and the frame as a page border.

    The text area is the inside of the frame, so the frame is drawn on its edge; the
    title block in the footer ends on the lower frame line. Body text keeps a small
    indent from the frame.
    """
    section = document.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = (Mm(size) for size in SHEET_MM)
    section.left_margin = Mm(FRAME_MM["left"])
    section.top_margin = Mm(FRAME_MM["top"])
    section.right_margin = Mm(FRAME_MM["right"])
    section.bottom_margin = Mm(FRAME_MM["bottom"])
    section.header_distance = Mm(FRAME_MM["top"])
    section.footer_distance = Mm(FRAME_MM["bottom"])
    section._sectPr.get_or_add_pgMar().addnext(_page_borders())

    normal = document.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(BODY_SIZE_PT)
    paragraph = normal.paragraph_format
    paragraph.space_before = paragraph.space_after = Pt(0)
    paragraph.left_indent = paragraph.right_indent = Mm(BODY_INDENT_MM)


def fit_table(table: Table) -> None:
    """Keep a body table inside the frame: indented like the text, columns of equal width."""
    indent = OxmlElement("w:tblInd")
    indent.set(qn("w:w"), str(Mm(BODY_INDENT_MM).twips))
    indent.set(qn("w:type"), "dxa")
    table._tbl.tblPr.insert_element_before(
        indent, "w:tblBorders", "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook"
    )
    table.autofit = False
    width = Mm(body_width_mm() / len(table.columns))
    for column in table.columns:
        column.width = width
        for cell in column.cells:
            cell.width = width


def body_width_mm() -> float:
    """The width of the text inside the frame, less the body indent on both sides."""
    return SHEET_MM[0] - FRAME_MM["left"] - FRAME_MM["right"] - 2 * BODY_INDENT_MM
