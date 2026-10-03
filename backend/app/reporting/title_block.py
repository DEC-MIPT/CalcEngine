from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from docx.document import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.oxml.xmlchemy import BaseOxmlElement
from docx.section import _Footer
from docx.shared import Length, Mm, Pt, Twips
from docx.table import Table
from docx.text.paragraph import Paragraph

from app.reporting.format import format_date
from app.reporting.layout import (
    BODY_INDENT_MM,
    FRAME_LINE_EIGHTHS_PT,
    FRAME_MM,
    SHEET_MM,
    line_mm,
    margin_mm,
)
from app.schemas.report import ReportRequest, Signatory

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

SIGNATURE_ROWS: MappingProxyType[str, int] = MappingProxyType(
    {"developer": 3, "checker": 4, "normative_control": 6}
)
"""Rows of form 5 for the developer, the checker (the row under the developer) and normative control."""

SIGNATURE_COLUMNS: MappingProxyType[str, int] = MappingProxyType({"10": 0, "11": 2, "12": 4, "13": 5})
"""Grid column of columns 10 (role), 11 (surname), 12 (signature) and 13 (date) in those rows."""

CHECKER_CAPTION = "Пров."

DATE_SIZE_PT = 6
"""A date ``ДД.ММ.ГГ`` is about 3.9 em wide; at 6 pt it fits column 13 (10 mm less the cell margins)."""

FORM6_WIDTHS_MM = (10, 10, 10, 10, 15, 10, 110, 10)
"""Column widths of form 6, left to right (GOST R 21.101-2026, edition unverified, Annex E)."""

FORM6_ROW_HEIGHTS_MM = (5, 2, 3, 5)
"""Form 6 is 15 mm high: three rows of 5 mm on the left, 7 mm and 8 mm under "Лист" on
the right. One grid holds both, so its rows are 5, 2, 3 and 5 mm and cells merge across."""

FORM6_MERGES: tuple[tuple[int, int, int, int], ...] = (
    (0, 6, 3, 6),
    (0, 7, 1, 7),
    (2, 7, 3, 7),
    *((1, column, 2, column) for column in range(6)),
)

FORM6_CAPTIONS: MappingProxyType[tuple[int, int], str] = MappingProxyType(
    {
        (3, 0): "Изм.",
        (3, 1): "Кол.уч",
        (3, 2): "Лист",
        (3, 3): "№ док.",
        (3, 4): "Подп.",
        (3, 5): "Дата",
        (0, 7): "Лист",
    }
)

FORM6_COLUMNS: MappingProxyType[str, tuple[int, int]] = MappingProxyType({"1": (0, 6), "7": (2, 7)})

FORM6_CHANGE_CELLS = tuple((row, column) for row in (0, 1) for column in range(6))


@dataclass(frozen=True)
class Form:
    """The grid of one title-block form: widths, row heights, merges, captions, data columns."""

    widths_mm: tuple[int, ...]
    row_heights_mm: tuple[int, ...]
    merges: tuple[tuple[int, int, int, int], ...]
    captions: MappingProxyType[tuple[int, int], str]
    columns: MappingProxyType[str, tuple[int, int]]


FORM5 = Form(FORM5_WIDTHS_MM, (ROW_HEIGHT_MM,) * FORM5_ROWS, FORM5_MERGES, FORM5_CAPTIONS, FORM5_COLUMNS)
FORM6 = Form(FORM6_WIDTHS_MM, FORM6_ROW_HEIGHTS_MM, FORM6_MERGES, FORM6_CAPTIONS, FORM6_COLUMNS)

SHEET_FORMAT = "А4"
FORMAT_BOX_MM = (150, 40)
"""Column 26 under the lower frame line, below the right part of the form: x and width."""

TITLE_STYLE = "DEC Title Block"
TITLE_SIZE_PT = 7
LARGE_SIZE_PT = 10
"""Columns 1 and 5 print larger than the captions; a layout choice, not a norm value."""

FIELDS: MappingProxyType[str, str] = MappingProxyType({"7": "PAGE", "8": "NUMPAGES"})
"""Column 7 (sheet number) and column 8 (number of sheets) as Word fields."""
CELL_MARGIN_MM = 0.5
OUTER_LINE, INNER_LINE = FRAME_LINE_EIGHTHS_PT, 4
"""Line widths of the form in eighths of a point; layout choices, not norm values. The
outer line is the frame line, so that the two lie on each other."""

FRAME_SIDES = ("left", "right")
"""The sides of the form that the frame draws: a second line there, even one lying exactly
on the frame line, can round to a different pixel on screen and stick out of the frame."""

CLOSING_TWIPS = 2
"""Height of the paragraph a footer must end in, under the form."""

BODY_GAP_MM = BODY_INDENT_MM
"""Space between the body text and the form, as wide as the body text keeps off the frame."""


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
        line.set(qn("w:val"), "nil" if side in FRAME_SIDES else "single")
        line.set(qn("w:sz"), str(INNER_LINE if side.startswith("inside") else OUTER_LINE))
        line.set(qn("w:space"), "0")
        line.set(qn("w:color"), "000000")
        borders.append(line)
    margins = OxmlElement("w:tblCellMar")
    for side in ("left", "right"):
        margin = OxmlElement(f"w:{side}")
        margin.set(qn("w:w"), str(Mm(CELL_MARGIN_MM).twips))
        margin.set(qn("w:type"), "dxa")
        margins.append(margin)
    table._tbl.tblPr.insert_element_before(
        _indent(), "w:tblBorders", "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook"
    )
    table._tbl.tblPr.insert_element_before(borders, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook")
    table._tbl.tblPr.insert_element_before(margins, "w:tblLook")


def indent_mm() -> float:
    """The table indent that puts the left edge of the form on the left frame line.

    The indent counts from the text area to the text of the first cell, so the left
    edge of the form lies one cell margin to the left of it.
    """
    return FRAME_MM["left"] - margin_mm("left") + CELL_MARGIN_MM


def _indent() -> BaseOxmlElement:
    indent = OxmlElement("w:tblInd")
    indent.set(qn("w:w"), str(Mm(indent_mm()).twips))
    indent.set(qn("w:type"), "dxa")
    return indent


def row_heights_mm(form: Form) -> list[float]:
    """Row heights that put the middle of every horizontal line where the figure draws it.

    Word and LibreOffice draw a horizontal line below its row boundary, so each boundary
    lies half its line width above the figure's line: the outer lines are thicker than
    the inner ones, so the first row is longer and the last row shorter than the figure.
    """
    lines = [OUTER_LINE, *(INNER_LINE,) * (len(form.row_heights_mm) - 1), OUTER_LINE]
    return [
        height - (line_mm(lower) - line_mm(upper)) / 2
        for height, upper, lower in zip(form.row_heights_mm, lines[:-1], lines[1:], strict=True)
    ]


def footer_distance_mm() -> float:
    """The footer distance that puts the middle of the lower line of the form on the frame."""
    return FRAME_MM["bottom"] - line_mm(OUTER_LINE) / 2 - Twips(CLOSING_TWIPS).mm


def _grid(footer: _Footer, style: str, form: Form) -> Table:
    widths = [Mm(width) for width in form.widths_mm]
    table = footer.add_table(len(form.row_heights_mm), len(widths), Mm(sum(form.widths_mm)))
    table.autofit = False
    _borders(table)
    for index, width in enumerate(widths):
        table.columns[index].width = width
    for row, height in zip(table.rows, row_heights_mm(form), strict=True):
        row.height, row.height_rule = Mm(height), WD_ROW_HEIGHT_RULE.EXACTLY
        for index, cell in enumerate(row.cells):
            cell.width = widths[index]
            cell.paragraphs[0].style = style
    for first_row, first_column, last_row, last_column in form.merges:
        table.cell(first_row, first_column).merge(table.cell(last_row, last_column))
    for (row, column), caption in form.captions.items():
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


def _exact_paragraph(footer: _Footer, style: str, height: Length) -> None:
    paragraph = footer.add_paragraph(style=style)
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    paragraph.paragraph_format.line_spacing = height


def _closing_paragraph(footer: _Footer, style: str) -> None:
    """A footer must end in a paragraph; this one takes almost no height."""
    _exact_paragraph(footer, style, Twips(CLOSING_TWIPS))


def _field(paragraph: Paragraph, instruction: str) -> None:
    """A simple Word field; its cached text is ``1`` until the viewer updates it."""
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), f" {instruction} ")
    run = OxmlElement("w:r")
    text = OxmlElement("w:t")
    text.text = "1"
    run.append(text)
    field.append(run)
    paragraph._p.append(field)


def _fill(
    table: Table,
    form: Form,
    texts: Mapping[str, tuple[str, int]],
    fields: Mapping[str, str],
) -> None:
    for column, (text, size) in texts.items():
        cell = table.cell(*form.columns[column])
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(text).font.size = Pt(size)
    for column, instruction in fields.items():
        _field(table.cell(*form.columns[column]).paragraphs[0], instruction)


def _footer_form(footer: _Footer, style: str, form: Form) -> Table:
    """Column 26, an empty line that keeps the body text off the form, the form, the closing paragraph."""
    _format_box(footer.paragraphs[0], style)
    _exact_paragraph(footer, style, Mm(BODY_GAP_MM))
    table = _grid(footer, style, form)
    _closing_paragraph(footer, style)
    return table


def _sign(table: Table, row: int, signatory: Signatory) -> None:
    table.cell(row, SIGNATURE_COLUMNS["11"]).paragraphs[0].add_run(signatory.surname)
    date = format_date(signatory.date) if signatory.date else ""
    table.cell(row, SIGNATURE_COLUMNS["13"]).paragraphs[0].add_run(date).font.size = Pt(DATE_SIZE_PT)


def _signatures(table: Table, request: ReportRequest) -> None:
    """Columns 10-13 of form 5: filled only while the signature block is enabled; column 12 stays empty."""
    if not request.signature_block:
        return
    for role in ("developer", "checker", "normative_control"):
        signatory = getattr(request, role)
        if signatory is None:
            continue
        if role == "checker":
            table.cell(SIGNATURE_ROWS[role], SIGNATURE_COLUMNS["10"]).paragraphs[0].add_run(CHECKER_CAPTION)
        _sign(table, SIGNATURE_ROWS[role], signatory)


def add_title_blocks(document: Document, request: ReportRequest) -> tuple[Table, Table]:
    """Form 5 in the first-page footer and form 6 in the footer of the following sheets.

    Form 5 carries columns 1, 5, 6 and 9, the sheet fields of columns 7 and 8, and the
    signature block in columns 10-13; form 6 carries column 1 and the sheet number. Both
    have column 26 under the frame and empty columns 14-19. The lower line of each form
    is the lower frame line, so the footer distance is set here.
    """
    title = request.title
    section = document.sections[0]
    section.different_first_page_header_footer = True
    section.footer_distance = Mm(footer_distance_mm())
    style = _title_style(document)
    first = _footer_form(section.first_page_footer, style, FORM5)
    _fill(
        first,
        FORM5,
        {
            "1": (title.designation, LARGE_SIZE_PT),
            "5": (title.document_name, LARGE_SIZE_PT),
            "6": (title.documentation_kind, TITLE_SIZE_PT),
            "9": (title.organization, TITLE_SIZE_PT),
        },
        FIELDS,
    )
    _signatures(first, request)
    following = _footer_form(section.footer, style, FORM6)
    _fill(following, FORM6, {"1": (title.designation, LARGE_SIZE_PT)}, {"7": FIELDS["7"]})
    return first, following
