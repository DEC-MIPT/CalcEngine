from io import BytesIO

from docx import Document
from docx.document import Document as DocumentObject

from app.reporting.accountability import RESPONSIBILITY, accountability_lines
from app.reporting.format import (
    OPERATORS,
    format_bound,
    format_norm_ref,
    format_quantity,
)
from app.reporting.layout import apply_sheet, fit_table
from app.reporting.model import (
    AccountabilitySection,
    ConclusionSection,
    InputSection,
    Report,
    TraceSection,
)
from app.reporting.title_block import add_title_blocks
from app.schemas.calculation import BoundViolation, CheckStep, NormRef, TraceStep

SECTION_TITLES = {
    "inputs": "Исходные данные",
    "trace": "Расчёт",
    "conclusion": "Заключение",
    "accountability": "Подотчётность результата",
}
STEP_KINDS = {"formula": "Формула", "table": "Табличное значение", "check": "Проверка"}
VERDICTS = {
    "pass": "Все проверки выполнены.",
    "fail": "Проверка не выполнена.",
    "refused": "Расчёт отклонён: входное значение вне области применения метода.",
}
REFUSED_TRACE = "Расчёт не выполнялся: входное значение вне области применения метода."


def _passed(passed: bool) -> str:
    return "выполнено" if passed else "не выполнено"


def _comparison(step: CheckStep) -> str:
    return (
        f"{format_quantity(step.result)} {OPERATORS[step.operator]} {format_quantity(step.right)}"
        f" — {_passed(step.passed)}"
    )


def _sources(references: tuple[NormRef, ...]) -> list[str]:
    return [f"Источник: {format_norm_ref(reference)}" for reference in references]


def step_lines(number: int, step: TraceStep) -> list[str]:
    """The lines a trace step prints: kind, formula, substitutions, result, sources."""
    lines = [f"{number}. {STEP_KINDS[step.kind]} {step.step_id}", f"Выражение: {step.expression}"]
    if step.substitutions:
        values = "; ".join(f"{item.symbol} = {format_quantity(item)}" for item in step.substitutions)
        lines.append(f"Подстановка: {values}")
    if isinstance(step, CheckStep):
        lines.append(f"Сравнение: {_comparison(step)}")
    else:
        lines.append(f"Результат: {format_quantity(step.result)}")
    return lines + _sources(step.norm_refs)


def _violation_lines(violation: BoundViolation) -> list[str]:
    bound = violation.bound
    allowed = format_bound(bound, violation.value.unit)
    return [
        f"Нарушенная граница: {bound.quantity} = {format_quantity(violation.value)}, {allowed}.",
        *_sources(bound.source),
    ]


def conclusion_lines(section: ConclusionSection) -> list[str]:
    lines = [VERDICTS[section.verdict]]
    if section.deciding_check is not None:
        check = section.deciding_check
        lines.append(f"Определяющая проверка {check.step_id}: {check.expression}; {_comparison(check)}.")
    if section.violation is not None:
        lines.extend(_violation_lines(section.violation))
    return lines


def _write_inputs(document: DocumentObject, section: InputSection) -> None:
    table = document.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    header = table.rows[0].cells
    header[0].text, header[1].text = "Величина", "Значение"
    for row in section.rows:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = row.quantity, format_quantity(row.value)
    fit_table(table)


def _write_trace(document: DocumentObject, section: TraceSection) -> None:
    if section.refused:
        document.add_paragraph(REFUSED_TRACE)
    for number, step in enumerate(section.steps, start=1):
        for line in step_lines(number, step):
            document.add_paragraph(line)


def render_docx(report: Report) -> bytes:
    """Write the report body to ``.docx`` in memory (design.md decision 18)."""
    document = Document()
    apply_sheet(document)
    add_title_blocks(document, report.request.title)
    for number, section in enumerate(report.body, start=1):
        heading = document.add_paragraph()
        heading.add_run(f"{number} {SECTION_TITLES[section.kind]}").bold = True
        if isinstance(section, InputSection):
            _write_inputs(document, section)
        elif isinstance(section, TraceSection):
            _write_trace(document, section)
        elif isinstance(section, AccountabilitySection):
            for line in accountability_lines(section):
                document.add_paragraph(line)
            document.add_paragraph().add_run(RESPONSIBILITY).bold = True
        else:
            for line in conclusion_lines(section):
                document.add_paragraph(line)
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()
