import re
from collections.abc import Mapping
from io import BytesIO

from docx import Document
from docx.document import Document as DocumentObject
from docx.text.paragraph import Paragraph

from app.reporting.accountability import RESPONSIBILITY, accountability_lines
from app.reporting.format import (
    LATEX_OPERATORS,
    VERDICT_TEXTS,
    check_rounding,
    format_bound,
    format_norm_ref,
    format_parameter_source,
    latex_quantity,
)
from app.reporting.formula import FormulaError, Line, Math, omml, omml_paragraph
from app.reporting.layout import apply_sheet, fit_table
from app.reporting.model import (
    AccountabilitySection,
    ConclusionSection,
    InputSection,
    Report,
    TraceSection,
)
from app.reporting.symbols import equation, named
from app.reporting.title_block import add_title_blocks
from app.schemas.calculation import (
    BoundViolation,
    CheckStep,
    NormRef,
    RoundingRule,
    TraceStep,
)

SECTION_TITLES = {
    "inputs": "Исходные данные",
    "trace": "Расчёт",
    "conclusion": "Заключение",
    "accountability": "Подотчётность результата",
}
STEP_KINDS = {"formula": "Формула", "table": "Табличное значение", "check": "Проверка"}
REFUSED_TRACE = "Расчёт не выполнялся: входное значение вне области применения метода."

TRACE_NORM_STATUS = False
"""Печатать ли статус проверки ссылок в шагах расчёта.

В первой итерации пилота он не печатается; статус остаётся у источников границ в
заключении.
"""

ACCOUNTABILITY_SECTION = False
"""Печатать ли раздел «Подотчётность результата».

В первой итерации пилота он не печатается; нумерация остальных разделов не меняется, а
фраза об ответственности инженера печатается последним абзацем заключения. Модель отчёта
по-прежнему собирает этот раздел, так что вернуть его можно, включив флаг. Строка
источника параметров печатается там же, где фраза об ответственности, перед ней, и только
один раз (``interim-normatives-source`` design.md, решение 13).
"""

NOT_XML = re.compile("[^\t\n\r\u0020-\ud7ff\ue000-\ufffd\U00010000-\U0010ffff]")
"""Символы, которых нет в XML 1.0: в запасном тексте формулы они заменяются на U+FFFD."""


def _passed(passed: bool) -> str:
    return VERDICT_TEXTS["pass" if passed else "fail"][0]


def _comparison(step: CheckStep, rounding: Mapping[str, RoundingRule]) -> Line:
    left, right = check_rounding(step, rounding)
    sides = (
        f"{latex_quantity(step.result, left)} {LATEX_OPERATORS[step.operator]} {latex_quantity(step.right, right)}"
    )
    return (Math(sides), f" — {_passed(step.passed)}")


def _sources(references: tuple[NormRef, ...], *, status: bool) -> list[Line]:
    return [(f"Источник: {format_norm_ref(reference, status=status)}",) for reference in references]


def _substitutions(step: TraceStep, symbols: Mapping[str, str], rounding: Mapping[str, RoundingRule]) -> Line:
    first, *rest = (equation(item.symbol, item, symbols, rounding.get(item.symbol)) for item in step.substitutions)
    line: Line = ("Подстановка: ", *first)
    for item in rest:
        line += ("; ", *item)
    return line


def step_lines(
    number: int, step: TraceStep, symbols: Mapping[str, str], rounding: Mapping[str, RoundingRule]
) -> list[Line]:
    """Собирает строки, которые печатает шаг трассы.

    Это вид шага с его обозначением, выражение, подстановки, результат и источники
    без статуса проверки; выражения и значения — формулы. Значения выходов печатаются
    по их правилам округления, как на экране результата; трасса в конверте остаётся
    неокруглённой.

    Args:
        number: номер шага в отчёте.
        step: шаг трассы.
        symbols: обозначения в LaTeX по имени шага или величины.
        rounding: правила округления выходов по имени.

    Returns:
        Строки шага по порядку.
    """
    lines: list[Line] = [
        (f"{number}. {STEP_KINDS[step.kind]} ", named(step.step_id, symbols)),
        ("Выражение: ", Math(step.expression, breakable=True)),
    ]
    if step.substitutions:
        lines.append(_substitutions(step, symbols, rounding))
    if isinstance(step, CheckStep):
        lines.append(("Сравнение: ", *_comparison(step, rounding)))
    else:
        lines.append(("Результат: ", Math(latex_quantity(step.result, rounding.get(step.step_id)))))
    return lines + _sources(step.norm_refs, status=TRACE_NORM_STATUS)


def _violation_lines(violation: BoundViolation, symbols: Mapping[str, str]) -> list[Line]:
    bound = violation.bound
    return [
        (
            "Нарушенная граница: ",
            *equation(bound.quantity, violation.value, symbols),
            ", ",
            *format_bound(bound, violation.value.unit),
            ".",
        ),
        *_sources(bound.source, status=True),
    ]


def conclusion_lines(
    section: ConclusionSection, symbols: Mapping[str, str], rounding: Mapping[str, RoundingRule]
) -> list[Line]:
    """Собирает строки заключения: вердикт и то, что его решило.

    Args:
        section: раздел заключения модели отчёта.
        symbols: обозначения в LaTeX по имени шага или величины.
        rounding: правила округления выходов по имени.

    Returns:
        Строки заключения по порядку.
    """
    lines: list[Line] = [(VERDICT_TEXTS[section.verdict][1],)]
    if section.deciding_check is not None:
        check = section.deciding_check
        lines.append(("Определяющая проверка: ", Math(check.expression), "; ", *_comparison(check, rounding), "."))
    if section.violation is not None:
        lines.extend(_violation_lines(section.violation, symbols))
    return lines


def write_line(paragraph: Paragraph, line: Line) -> None:
    """Дописывает в абзац строку отчёта: текст — прогонами, формулы — формулами Word.

    Строка из одной формулы становится выключенной формулой, прижатой влево. Формула,
    LaTeX которой не переводится, печатается своим LaTeX как обычный текст, как её
    показывает экран результата.

    Args:
        paragraph: абзац документа или ячейки таблицы.
        line: строка из текста и формул.
    """
    # python-docx has no public API for Office Math, so equations go into the paragraph's element.
    if len(line) == 1 and isinstance(line[0], Math):
        try:
            paragraph._p.append(omml_paragraph(line[0]))
            return
        except FormulaError:
            pass
    for segment in line:
        if not isinstance(segment, Math):
            paragraph.add_run(segment)
            continue
        try:
            paragraph._p.append(omml(segment))
        except FormulaError:
            paragraph.add_run(NOT_XML.sub("\ufffd", segment.latex))


def _write_lines(document: DocumentObject, lines: list[Line]) -> None:
    for line in lines:
        write_line(document.add_paragraph(), line)


def _write_inputs(document: DocumentObject, section: InputSection, symbols: Mapping[str, str]) -> None:
    table = document.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    header = table.rows[0].cells
    header[0].text, header[1].text = "Величина", "Значение"
    for row in section.rows:
        cells = table.add_row().cells
        write_line(cells[0].paragraphs[0], (named(row.quantity, symbols),))
        write_line(cells[1].paragraphs[0], (Math(latex_quantity(row.value)),))
    fit_table(table)


def _write_trace(document: DocumentObject, section: TraceSection, report: Report) -> None:
    if section.refused:
        document.add_paragraph(REFUSED_TRACE)
    for number, step in enumerate(section.steps, start=1):
        _write_lines(document, step_lines(number, step, report.symbols, report.rounding))


def render_docx(report: Report) -> bytes:
    """Записывает отчёт в ``.docx`` в памяти (design.md, решение 18).

    Args:
        report: модель отчёта.

    Returns:
        Содержимое файла ``.docx``.
    """
    document = Document()
    apply_sheet(document)
    add_title_blocks(document, report.request)
    sections = [
        section for section in report.body if ACCOUNTABILITY_SECTION or not isinstance(section, AccountabilitySection)
    ]
    for number, section in enumerate(sections, start=1):
        heading = document.add_paragraph()
        heading.add_run(f"{number} {SECTION_TITLES[section.kind]}").bold = True
        if isinstance(section, InputSection):
            _write_inputs(document, section, report.symbols)
        elif isinstance(section, TraceSection):
            _write_trace(document, section, report)
        elif isinstance(section, AccountabilitySection):
            _write_lines(document, accountability_lines(section, report.symbols))
            document.add_paragraph().add_run(RESPONSIBILITY).bold = True
        else:
            _write_lines(document, conclusion_lines(section, report.symbols, report.rounding))
            if not ACCOUNTABILITY_SECTION:
                if section.parameter_source is not None:
                    document.add_paragraph(format_parameter_source(section.parameter_source))
                document.add_paragraph().add_run(RESPONSIBILITY).bold = True
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()
