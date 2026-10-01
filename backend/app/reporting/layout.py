from types import MappingProxyType

from docx.document import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.oxml.xmlchemy import BaseOxmlElement
from docx.section import _Header
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
"""The body text keeps this far off the frame on every side; at the top and bottom as
an empty line of this height in the header and above the title block."""
BODY_FONT = "Arial"
BODY_SIZE_PT = 12


def line_mm(eighths_pt: int) -> float:
    """A line width given in eighths of a point, in millimetres."""
    return eighths_pt / 8 * 25.4 / 72


FRAME_LINE_MM = line_mm(FRAME_LINE_EIGHTHS_PT)
"""A page border lies outside the text area, so each margin is the frame distance plus
half of this width, and the middle of the line falls on the frame."""

FRAME_SIDES = ("top", "left", "right")
"""The lower frame line is the lower line of the title block, which spans the frame on
every sheet; a page border there would lie under the footer, beside that line."""


def _page_borders() -> BaseOxmlElement:
    borders = OxmlElement("w:pgBorders")
    borders.set(qn("w:offsetFrom"), "text")
    for side in ("top", "left", "bottom", "right"):
        line = OxmlElement(f"w:{side}")
        line.set(qn("w:val"), "single" if side in FRAME_SIDES else "nil")
        line.set(qn("w:sz"), str(FRAME_LINE_EIGHTHS_PT))
        line.set(qn("w:space"), "0")
        line.set(qn("w:color"), "000000")
        borders.append(line)
    return borders


def _top_gap(header: _Header) -> None:
    """The header is one empty line that keeps the first line of the sheet off the top frame line."""
    paragraph = header.paragraphs[0]
    paragraph.paragraph_format.left_indent = paragraph.paragraph_format.right_indent = Mm(0)
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    paragraph.paragraph_format.line_spacing = Mm(BODY_INDENT_MM)


def apply_sheet(document: Document) -> None:
    """A4 portrait with the frame as a page border whose line is centred on the frame.

    The text area is the inside of the frame line, so the border is drawn on its edge.
    The title block sets the footer distance, since its lower line closes the frame.
    Body text keeps a small indent from the frame, at the top through the header, which
    starts on the top frame line.
    """
    section = document.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = (Mm(size) for size in SHEET_MM)
    section.left_margin = Mm(margin_mm("left"))
    section.top_margin = Mm(margin_mm("top"))
    section.right_margin = Mm(margin_mm("right"))
    section.bottom_margin = Mm(margin_mm("bottom"))
    section.header_distance = Mm(margin_mm("top"))
    section.different_first_page_header_footer = True
    for header in (section.first_page_header, section.header):
        _top_gap(header)
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


def margin_mm(side: str) -> float:
    """The page margin on one side: the frame distance and half of the frame line."""
    return FRAME_MM[side] + FRAME_LINE_MM / 2


def body_width_mm() -> float:
    """The width of the text inside the frame line, less the body indent on both sides."""
    return SHEET_MM[0] - margin_mm("left") - margin_mm("right") - 2 * BODY_INDENT_MM
