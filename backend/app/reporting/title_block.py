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
    BODY_FONT,
    BODY_INDENT_MM,
    FRAME_LINE_EIGHTHS_PT,
    FRAME_MM,
    SHEET_MM,
    line_mm,
    margin_mm,
)
from app.schemas.report import ReportRequest, Signatory

FORM5_WIDTHS_MM = (10, 10, 10, 10, 15, 10, 70, 15, 15, 20)
"""Ширины граф формы 5 слева направо (GOST R 21.101-2026, edition unverified, приложение Е)."""

FORM5_ROWS = 8
ROW_HEIGHT_MM = 5
"""Форма 5 — восемь строк по 5 мм, как на её рисунке (GOST R 21.101-2026, edition unverified, приложение Е)."""

FORM5_MERGES: tuple[tuple[int, int, int, int], ...] = (
    (0, 6, 2, 9),
    (3, 6, 7, 6),
    (5, 7, 7, 9),
    *((row, 0, row, 1) for row in range(3, FORM5_ROWS)),
    *((row, 2, row, 3) for row in range(3, FORM5_ROWS)),
)
"""Объединённые ячейки формы 5 в виде (первая строка, первый столбец, последняя строка, последний столбец)."""

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
"""Подписи граф, печатаемые в форме 5, по ячейкам, в которых они стоят."""

FORM5_COLUMNS: MappingProxyType[str, tuple[int, int]] = MappingProxyType(
    {"1": (0, 6), "5": (3, 6), "6": (4, 7), "7": (4, 8), "8": (4, 9), "9": (5, 7)}
)
"""Левая верхняя ячейка каждой нумерованной графы формы 5, в которой есть данные."""

CHANGE_CELLS = tuple((row, column) for row in (0, 1) for column in range(6))
"""Графы 14–19 (изменения): в MVP пустые."""

SIGNATURE_ROWS: MappingProxyType[str, int] = MappingProxyType(
    {"developer": 3, "checker": 4, "normative_control": 6}
)
"""Строки формы 5 для разработчика, проверяющего (строка под разработчиком) и нормоконтроля."""

SIGNATURE_COLUMNS: MappingProxyType[str, int] = MappingProxyType({"10": 0, "11": 2, "12": 4, "13": 5})
"""Столбцы сетки для граф 10 (роль), 11 (фамилия), 12 (подпись) и 13 (дата) в этих строках."""

CHECKER_CAPTION = "Пров."

DATE_SIZE_PT = 6
"""Дата ``ДД.ММ.ГГ`` шириной около 3,9 em; кеглем 6 пт она помещается в графу 13 (10 мм за вычетом полей ячейки)."""

SURNAME_SIZE_PT = 6
"""Фамилия в графе 11 печатается кеглем даты, чтобы узкая графа вмещала больше символов;
выбор вёрстки, а не значение нормы (``report-title-block-limits`` design.md, решение 6)."""

FORM6_WIDTHS_MM = (10, 10, 10, 10, 15, 10, 110, 10)
"""Ширины граф формы 6 слева направо (GOST R 21.101-2026, edition unverified, приложение Е)."""

FORM6_ROW_HEIGHTS_MM = (5, 2, 3, 5)
"""Форма 6 высотой 15 мм (GOST R 21.101-2026, edition unverified, приложение Е): слева три
строки по 5 мм, справа 7 мм и 8 мм под «Лист».
Обе части держит одна сетка, поэтому её строки — 5, 2, 3 и 5 мм, а ячейки объединяются
поперёк."""

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
    """Сетка одной формы основной надписи: ширины, высоты строк, объединения, подписи граф и графы данных."""

    widths_mm: tuple[int, ...]
    row_heights_mm: tuple[int, ...]
    merges: tuple[tuple[int, int, int, int], ...]
    captions: MappingProxyType[tuple[int, int], str]
    columns: MappingProxyType[str, tuple[int, int]]


FORM5 = Form(FORM5_WIDTHS_MM, (ROW_HEIGHT_MM,) * FORM5_ROWS, FORM5_MERGES, FORM5_CAPTIONS, FORM5_COLUMNS)
FORM6 = Form(FORM6_WIDTHS_MM, FORM6_ROW_HEIGHTS_MM, FORM6_MERGES, FORM6_CAPTIONS, FORM6_COLUMNS)

SHEET_FORMAT = "А4"
FORMAT_BOX_MM = (150, 40)
"""Графа 26 под нижней линией рамки, ниже правой части формы: координата x и ширина;
выбор вёрстки, а не значение нормы."""

TITLE_STYLE = "DEC Title Block"
TITLE_SIZE_PT = 7
"""Кегль подписей граф и текстов граф 6 и 9; выбор вёрстки, а не значение нормы."""
LARGE_SIZE_PT = 10
"""Графы 1 и 5 печатаются крупнее подписей; выбор вёрстки, а не значение нормы."""

COLUMN_SIZES_PT: MappingProxyType[str, int] = MappingProxyType(
    {"1": LARGE_SIZE_PT, "5": LARGE_SIZE_PT, "6": TITLE_SIZE_PT, "9": TITLE_SIZE_PT, "11": SURNAME_SIZE_PT}
)
"""Кегль текста запроса в каждой заполняемой графе."""

FIELDS: MappingProxyType[str, str] = MappingProxyType({"7": "PAGE", "8": "NUMPAGES"})
"""Графа 7 (номер листа) и графа 8 (число листов) как поля Word."""
CELL_MARGIN_MM = 0.5
OUTER_LINE, INNER_LINE = FRAME_LINE_EIGHTHS_PT, 4
"""Толщины линий формы в восьмых долях пункта; выбор вёрстки, а не значения нормы.
Внешняя линия — это линия рамки, чтобы они совпадали друг с другом."""

FRAME_DRAWN_SIDES = ("left", "right")
"""Стороны формы, которые рисует рамка: вторая линия там, даже лежащая точно на линии
рамки, на экране может округлиться до другого пикселя и выступить из рамки."""

CLOSING_TWIPS = 2
"""Высота абзаца под формой, которым должен заканчиваться колонтитул."""

BODY_GAP_MM = BODY_INDENT_MM
"""Промежуток между текстом тела и формой, равный отступу текста тела от рамки."""


def _title_style(document: Document) -> str:
    style = document.styles.add_style(TITLE_STYLE, WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = BODY_FONT
    style.font.size = Pt(TITLE_SIZE_PT)
    paragraph = style.paragraph_format
    paragraph.space_before = paragraph.space_after = Pt(0)
    paragraph.line_spacing = 1.0
    paragraph.left_indent = paragraph.right_indent = Mm(0)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return TITLE_STYLE


def _borders(table: Table) -> None:
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        line = OxmlElement(f"w:{side}")
        line.set(qn("w:val"), "nil" if side in FRAME_DRAWN_SIDES else "single")
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
    """Вычисляет отступ таблицы, при котором левый край формы лежит на левой линии рамки.

    Отступ отсчитывается от области текста до текста первой ячейки, поэтому левый край
    формы лежит на одно поле ячейки левее него.

    Returns:
        Отступ в миллиметрах.
    """
    return FRAME_MM["left"] - margin_mm("left") + CELL_MARGIN_MM


def _indent() -> BaseOxmlElement:
    indent = OxmlElement("w:tblInd")
    indent.set(qn("w:w"), str(Mm(indent_mm()).twips))
    indent.set(qn("w:type"), "dxa")
    return indent


def row_heights_mm(form: Form) -> list[float]:
    """Вычисляет высоты строк, при которых середина каждой горизонтальной линии лежит там, где её рисует чертёж.

    Word и LibreOffice рисуют горизонтальную линию под границей её строки, поэтому
    каждая граница лежит на половину толщины линии выше линии чертежа. Внешние линии
    толще внутренних, поэтому первая строка длиннее, а последняя короче, чем на
    чертеже.

    Args:
        form: сетка формы.

    Returns:
        Высоты строк в миллиметрах.
    """
    lines = [OUTER_LINE, *(INNER_LINE,) * (len(form.row_heights_mm) - 1), OUTER_LINE]
    return [
        height - (line_mm(lower) - line_mm(upper)) / 2
        for height, upper, lower in zip(form.row_heights_mm, lines[:-1], lines[1:], strict=True)
    ]


def footer_distance_mm() -> float:
    """Вычисляет отступ нижнего колонтитула, при котором середина нижней линии формы лежит на рамке.

    Returns:
        Отступ в миллиметрах.
    """
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
    """Заполняет графу 26: рамку, привязанную к странице, под нижней линией рамки листа."""
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
    """Добавляет закрывающий абзац: колонтитул должен заканчиваться абзацем, этот почти не занимает высоты."""
    _exact_paragraph(footer, style, Twips(CLOSING_TWIPS))


def _field(paragraph: Paragraph, instruction: str) -> None:
    """Вставляет простое поле Word; его кэшированный текст — ``1``, пока программа просмотра его не обновит."""
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
    texts: Mapping[str, str],
    fields: Mapping[str, str],
) -> None:
    for column, text in texts.items():
        cell = table.cell(*form.columns[column])
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(text).font.size = Pt(COLUMN_SIZES_PT[column])
    for column, instruction in fields.items():
        _field(table.cell(*form.columns[column]).paragraphs[0], instruction)


def _footer_form(footer: _Footer, style: str, form: Form) -> Table:
    """Собирает колонтитул: графа 26, пустая строка, отодвигающая текст тела от формы, сама форма и закрывающий абзац."""
    _format_box(footer.paragraphs[0], style)
    _exact_paragraph(footer, style, Mm(BODY_GAP_MM))
    table = _grid(footer, style, form)
    _closing_paragraph(footer, style)
    return table


def _sign(table: Table, row: int, signatory: Signatory) -> None:
    table.cell(row, SIGNATURE_COLUMNS["11"]).paragraphs[0].add_run(signatory.surname).font.size = Pt(
        COLUMN_SIZES_PT["11"]
    )
    date = format_date(signatory.date) if signatory.date else ""
    table.cell(row, SIGNATURE_COLUMNS["13"]).paragraphs[0].add_run(date).font.size = Pt(DATE_SIZE_PT)


def _signatures(table: Table, request: ReportRequest) -> None:
    """Заполняет графы 10–13 формы 5, только пока блок подписей включён; графа 12 остаётся пустой."""
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
    """Добавляет форму 5 в колонтитул первой страницы и форму 6 — в колонтитул следующих листов.

    Форма 5 несёт графы 1, 5, 6 и 9, поля листов в графах 7 и 8 и блок подписей в
    графах 10–13; форма 6 — графу 1 и номер листа. У обеих графа 26 под рамкой и пустые
    графы 14–19. Нижняя линия каждой формы — нижняя линия рамки, поэтому отступ
    колонтитула задаётся здесь.

    Args:
        document: документ python-docx.
        request: данные основной надписи и подписей.

    Returns:
        Таблицы формы 5 и формы 6.
    """
    title = request.title
    section = document.sections[0]
    section.footer_distance = Mm(footer_distance_mm())
    style = _title_style(document)
    first = _footer_form(section.first_page_footer, style, FORM5)
    _fill(
        first,
        FORM5,
        {
            "1": title.designation,
            "5": title.document_name,
            "6": title.documentation_kind,
            "9": title.organization,
        },
        FIELDS,
    )
    _signatures(first, request)
    following = _footer_form(section.footer, style, FORM6)
    _fill(following, FORM6, {"1": title.designation}, {"7": FIELDS["7"]})
    return first, following
