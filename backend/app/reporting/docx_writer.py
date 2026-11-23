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
    compact_norm_refs,
    comparison_rule,
    format_bound,
    format_norm_ref,
    format_rounding,
    format_source,
    latex_quantity,
    parameter_source_lines,
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
from app.reporting.symbols import (
    check_expression,
    equation,
    math_symbol,
    named,
    rationale_line,
)
from app.reporting.title_block import add_title_blocks
from app.schemas.calculation import (
    BoundViolation,
    CheckStep,
    DerivedViolation,
    EngineerFormulaStep,
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
STEP_KINDS = {"formula": "Формула", "table": "Табличное значение", "check": "Проверка", "engineer_formula": "Инженерная формула"}
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


def _comparison(step: CheckStep, rounding: Mapping[str, RoundingRule], default: RoundingRule | None) -> Line:
    left, right = check_rounding(step, rounding, default)
    sides = (
        f"{latex_quantity(step.result, left)} {LATEX_OPERATORS[step.operator]} {latex_quantity(step.right, right)}"
    )
    return (Math(sides), f" — {_passed(step.passed)}")


def _sources(
    references: tuple[NormRef, ...], *, status: bool, compact: bool = False, overall: bool = False,
) -> list[Line]:
    refs = compact_norm_refs(references, status=status) if compact else (
        format_norm_ref(ref, status=status) for ref in references
    )
    heading = "Нормативные ссылки расчёта" if overall else "Источник"
    return [(f"{heading}: {ref}",) for ref in refs]


def _substitutions(
    step: TraceStep, symbols: Mapping[str, str], rounding: Mapping[str, RoundingRule], default: RoundingRule | None,
) -> Line:
    if default is None:
        items = [equation(item.symbol, item, symbols, rounding.get(item.symbol)) for item in step.substitutions]
    else:
        items = [(Math(f"{math_symbol(item.symbol, symbols).latex} = {latex_quantity(item, rounding.get(item.symbol, default))}"),)
                 for item in step.substitutions]
    first, *rest = items
    line: Line = ("Подстановка: ", *first)
    for item in rest:
        line += ("; ", *item)
    return line


def step_lines(
    number: int, step: TraceStep, symbols: Mapping[str, str], rounding: Mapping[str, RoundingRule],
    default: RoundingRule | None = None,
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
    expression = step.expression
    label = named(step.step_id, symbols)
    if default is not None:
        if isinstance(step, CheckStep):
            expression = check_expression(step, symbols)
            label = Math(expression)
        else:
            label = math_symbol(step.step_id, symbols)
            if expression == step.step_id:
                expression = label.latex
    lines: list[Line] = [
        (f"{number}. {STEP_KINDS[step.kind]} ", label),
        ("Выражение: ", Math(expression, breakable=True)),
    ]
    if step.substitutions:
        lines.append(_substitutions(step, symbols, rounding, default))
    if isinstance(step, CheckStep):
        lines.append(("Сравнение: ", *_comparison(step, rounding, default)))
    else:
        lines.append(("Результат: ", Math(latex_quantity(step.result, rounding.get(step.step_id, default)))))
    if isinstance(step, EngineerFormulaStep):
        if default is not None:
            return lines + [("Обоснование инженерной формулы: ", *rationale_line(step.source.rationale, symbols))]
        return lines + [(f"Источник: {format_source(step.source)}",)]
    return lines + _sources(step.norm_refs, status=TRACE_NORM_STATUS, compact=default is not None)


def _violation_lines(
    violation: BoundViolation, symbols: Mapping[str, str], default: RoundingRule | None,
) -> list[Line]:
    bound = violation.bound
    operator = ("ge" if bound.inclusive else "gt") if bound.kind == "min" else ("le" if bound.inclusive else "lt")
    rule = comparison_rule(operator, violation.value.value, bound.value, default)
    return [
        (
            "Нарушенная граница: ",
            *equation(bound.quantity, violation.value, symbols, rule),
            ", ",
            *format_bound(bound, violation.value.unit, rule),
            ".",
        ),
        *_sources(bound.source, status=True, compact=default is not None),
    ]


def derived_violation_lines(
    violation: DerivedViolation, symbols: Mapping[str, str], default: RoundingRule | None = None,
    norm_refs: tuple[NormRef, ...] = (),
) -> list[Line]:
    rule = comparison_rule(violation.operator, violation.value.value, violation.limit.value, default)
    source = [(f"Источник: {format_source(violation.source)}",)] if default is None else [
        (f"Основание отказа (инженерное условие): {violation.source.rationale}",),
        *_sources(norm_refs, status=True, compact=True, overall=True),
    ]
    return [
        ("Расчёт отклонён: условие полного контакта подошвы не выполнено. Проверки несущей способности не выполнялись.",),
        (f"Условие: {violation.check_id}; диагностический шаг: {violation.step_id}; определяющий угол: {violation.limiting_corner}.",),
        (
            "Получено: ", *equation(violation.quantity, violation.value, symbols, rule),
            "; требуется ", Math(LATEX_OPERATORS[violation.operator]), " ",
            Math(latex_quantity(violation.limit, rule)), ".",
        ),
        *source,
        (f"Связанные входы: {', '.join(violation.related_inputs)}.",),
    ]


def conclusion_lines(
    section: ConclusionSection, symbols: Mapping[str, str], rounding: Mapping[str, RoundingRule],
    default: RoundingRule | None = None, norm_refs: tuple[NormRef, ...] = (),
) -> list[Line]:
    """Собирает строки заключения: вердикт и то, что его решило.

    Args:
        section: раздел заключения модели отчёта.
        symbols: обозначения в LaTeX по имени шага или величины.
        rounding: правила округления выходов по имени.

    Returns:
        Строки заключения по порядку.
    """
    if section.derived_violation is not None:
        return derived_violation_lines(section.derived_violation, symbols, default, norm_refs)
    lines: list[Line] = [(VERDICT_TEXTS[section.verdict][1],)]
    if section.deciding_check is not None:
        check = section.deciding_check
        expression = check.expression if default is None else check_expression(check, symbols)
        lines.append(("Определяющая проверка: ", Math(expression), "; ", *_comparison(check, rounding, default), "."))
    if section.violation is not None:
        lines.extend(_violation_lines(section.violation, symbols, default))
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
    for text in section.guidance:
        document.add_paragraph(text)
    _write_lines(document, list(section.math_guidance))


def _write_trace(document: DocumentObject, section: TraceSection, report: Report) -> None:
    if section.refused:
        document.add_paragraph(
            "Диагностическая трасса до отказа по условию полного контакта."
            if section.steps else REFUSED_TRACE
        )
    if report.norm_refs and section.steps and not section.refused:
        _write_lines(document, _sources(report.norm_refs, status=TRACE_NORM_STATUS, compact=True, overall=True))
    for number, step in enumerate(section.steps, start=1):
        _write_lines(document, step_lines(number, step, report.symbols, report.rounding, report.default_rounding))
    if report.outputs:
        document.add_heading("Выходные величины", level=2)
        _write_lines(document, [
            (Math(f"{math_symbol(output.quantity, report.symbols).latex} = {latex_quantity(output, output.rounding_rule)}"),
             f"; {format_rounding(output.rounding_rule)}.")
            for output in report.outputs
        ])


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
            _write_lines(document, conclusion_lines(section, report.symbols, report.rounding, report.default_rounding, report.norm_refs))
            if not ACCOUNTABILITY_SECTION:
                if section.parameter_source is not None:
                    for text in parameter_source_lines(section.parameter_source):
                        document.add_paragraph(text)
                document.add_paragraph().add_run(RESPONSIBILITY).bold = True
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()
