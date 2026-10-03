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
"""A4 книжной ориентации (GOST R 21.101-2026, edition unverified, приложение Ж, рисунок Ж.1 а)."""

FRAME_MM: MappingProxyType[str, int] = MappingProxyType(
    {"left": 20, "top": 5, "right": 5, "bottom": 5}
)
"""Расстояния внутренней рамки от краёв листа, как их показывает рисунок Ж.1 а) (GOST R 21.101-2026, edition unverified)."""

FRAME_LINE_EIGHTHS_PT = 12
"""Толщина линии рамки в восьмых долях пункта; выбор вёрстки, а не значение нормы."""

BODY_INDENT_MM = 5
"""На таком расстоянии текст тела держится от рамки со всех сторон; сверху и снизу —
пустой строкой этой высоты в верхнем колонтитуле и над основной надписью."""
BODY_FONT = "Arial"
BODY_SIZE_PT = 12


def line_mm(eighths_pt: int) -> float:
    """Переводит толщину линии из восьмых долей пункта в миллиметры.

    Args:
        eighths_pt: толщина в восьмых долях пункта.

    Returns:
        Толщина в миллиметрах.
    """
    return eighths_pt / 8 * 25.4 / 72


FRAME_LINE_MM = line_mm(FRAME_LINE_EIGHTHS_PT)
"""Граница страницы лежит вне области текста, поэтому каждое поле — расстояние до рамки
плюс половина этой толщины, и середина линии приходится на рамку."""

FRAME_SIDES = ("top", "left", "right")
"""Нижняя линия рамки — это нижняя линия основной надписи, которая на каждом листе
идёт по всей ширине рамки; граница страницы там легла бы под колонтитулом, рядом с этой
линией."""


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
    """Делает верхний колонтитул одной пустой строкой, которая отодвигает первую строку листа от верхней линии рамки."""
    paragraph = header.paragraphs[0]
    paragraph.paragraph_format.left_indent = paragraph.paragraph_format.right_indent = Mm(0)
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    paragraph.paragraph_format.line_spacing = Mm(BODY_INDENT_MM)


def apply_sheet(document: Document) -> None:
    """Задаёт лист A4 книжной ориентации с рамкой в виде границы страницы, линия которой по центру рамки.

    Область текста — внутренняя сторона линии рамки, поэтому граница рисуется по её
    краю. Отступ нижнего колонтитула задаёт основная надпись: её нижняя линия
    замыкает рамку. Текст тела держит небольшой отступ от рамки, сверху — за счёт
    верхнего колонтитула, который начинается на верхней линии рамки.

    Args:
        document: документ python-docx.
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
    """Удерживает таблицу тела внутри рамки: с отступом, как у текста, и колонками равной ширины.

    Args:
        table: таблица тела отчёта.
    """
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
    """Вычисляет поле страницы с одной стороны: отступ рамки плюс половина толщины её линии.

    Args:
        side: сторона листа (ключ ``FRAME_MM``).

    Returns:
        Поле в миллиметрах.
    """
    return FRAME_MM[side] + FRAME_LINE_MM / 2


def body_width_mm() -> float:
    """Вычисляет ширину текста внутри линии рамки за вычетом отступа тела с обеих сторон.

    Returns:
        Ширина в миллиметрах.
    """
    return SHEET_MM[0] - margin_mm("left") - margin_mm("right") - 2 * BODY_INDENT_MM
