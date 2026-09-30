from types import MappingProxyType

from docx.document import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.section import _Footer
from docx.shared import Mm, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph

from app.reporting.layout import FRAME_MM, SHEET_MM

FORM5_WIDTHS_MM = (10, 10, 10, 10, 15, 10, 70, 15, 15, 20)
"""Column widths of form 5, left to right (GOST R 21.101-2026, edition unverified, Annex E)."""

FORM5_ROWS = 8
ROW_HEIGHT_MM = 5
"""Form 5 is eight rows of 5 mm, as its figure gives them."""

FORM5_MERGES: tuple[tuple[int, int, int, int], ...] = (
    (0, 6, 2, 9),
    (3, 6, 7, 6),
    (5, 7, 7, 9),
    *((row, 0, row, 1) for row in range(3, FORM5_ROWS)),
    *((row, 2, row, 3) for row in range(3, FORM5_ROWS)),
)
"""Merged cells of form 5 as (first row, first column, last row, last column)."""

FORM5_CAPTIONS: MappingProxyType[tuple[int, int], str] = MappingProxyType(
    {
        (2, 0): "Изм.",
        (2, 1): "Кол.уч",
        (2, 2): "Лист",
        (2, 3): "№ док.",
        (2, 4): "Подп.",
        (2, 5): "Дата",
        (3, 0): "Разраб.",
        (6, 0): "Н. контр.",
        (3, 7): "Вид док.",
        (3, 8): "Лист",
        (3, 9): "Листов",
    }
)
"""The captions printed in form 5, by the cell they stand in."""

FORM5_COLUMNS: MappingProxyType[str, tuple[int, int]] = MappingProxyType(
    {"1": (0, 6), "5": (3, 6), "6": (4, 7), "7": (4, 8), "8": (4, 9), "9": (5, 7)}
)
"""The top-left cell of each numbered column of form 5 that carries data."""

CHANGE_CELLS = tuple((row, column) for row in (0, 1) for column in range(6))
"""Columns 14-19 (changes): empty in the MVP."""

SHEET_FORMAT = "А4"
FORMAT_BOX_MM = (150, 40)
"""Column 26 under the lower frame line, below the right part of the form: x and width."""

TITLE_STYLE = "DEC Title Block"
TITLE_SIZE_PT = 7
CELL_MARGIN_MM = 0.5
OUTER_LINE, INNER_LINE = "12", "4"
"""Line widths of the form in eighths of a point; layout choices, not norm values."""


def _title_style(document: Document) -> str:
    style = document.styles.add_style(TITLE_STYLE, WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = "Arial"
    style.font.size = Pt(TITLE_SIZE_PT)
    paragraph = style.paragraph_format
    paragraph.space_before = paragraph.space_after = Pt(0)
    paragraph.left_indent = paragraph.right_indent = Mm(0)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return TITLE_STYLE


def _borders(table: Table) -> None:
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        line = OxmlElement(f"w:{side}")
        line.set(qn("w:val"), "single")
        line.set(qn("w:sz"), INNER_LINE if side.startswith("inside") else OUTER_LINE)
        line.set(qn("w:space"), "0")
        line.set(qn("w:color"), "000000")
        borders.append(line)
    margins = OxmlElement("w:tblCellMar")
    for side in ("left", "right"):
        margin = OxmlElement(f"w:{side}")
        margin.set(qn("w:w"), str(Mm(CELL_MARGIN_MM).twips))
        margin.set(qn("w:type"), "dxa")
        margins.append(margin)
    table._tbl.tblPr.insert_element_before(borders, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook")
    table._tbl.tblPr.insert_element_before(margins, "w:tblLook")


def _grid(footer: _Footer, style: str) -> Table:
    widths = [Mm(width) for width in FORM5_WIDTHS_MM]
    table = footer.add_table(FORM5_ROWS, len(widths), Mm(sum(FORM5_WIDTHS_MM)))
    table.autofit = False
    _borders(table)
    for index, width in enumerate(widths):
        table.columns[index].width = width
    for row in table.rows:
        row.height, row.height_rule = Mm(ROW_HEIGHT_MM), WD_ROW_HEIGHT_RULE.EXACTLY
        for index, cell in enumerate(row.cells):
            cell.width = widths[index]
            cell.paragraphs[0].style = style
    for first_row, first_column, last_row, last_column in FORM5_MERGES:
        table.cell(first_row, first_column).merge(table.cell(last_row, last_column))
    for (row, column), caption in FORM5_CAPTIONS.items():
        table.cell(row, column).paragraphs[0].text = caption
    return table


def _format_box(paragraph: Paragraph, style: str) -> None:
    """Column 26: a frame anchored to the page, under the lower frame line."""
    paragraph.style = style
    x, width = FORMAT_BOX_MM
    frame = OxmlElement("w:framePr")
    for name, value in (
        ("w:w", Mm(width).twips),
        ("w:h", Mm(FRAME_MM["bottom"]).twips),
        ("w:x", Mm(x).twips),
        ("w:y", Mm(SHEET_MM[1] - FRAME_MM["bottom"]).twips),
    ):
        frame.set(qn(name), str(value))
    frame.set(qn("w:hRule"), "exact")
    frame.set(qn("w:hAnchor"), "page")
    frame.set(qn("w:vAnchor"), "page")
    paragraph._p.get_or_add_pPr().append(frame)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.text = f"Формат {SHEET_FORMAT}"


def _closing_paragraph(footer: _Footer, style: str) -> None:
    """A footer must end in a paragraph; this one takes almost no height."""
    closing = footer.add_paragraph(style=style)
    closing.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    closing.paragraph_format.line_spacing = Pt(1)


def add_form5(document: Document) -> Table:
    """Form 5 in the first-page footer: its grid, captions, column 26 and empty columns 14-19."""
    section = document.sections[0]
    section.different_first_page_header_footer = True
    footer = section.first_page_footer
    style = _title_style(document)
    _format_box(footer.paragraphs[0], style)
    table = _grid(footer, style)
    _closing_paragraph(footer, style)
    return table
