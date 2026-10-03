import time
from io import BytesIO

from docx import Document
from test_engine_foundations_shallow_r import inputs
from test_reporting_model import report

from app.reporting.docx_writer import conclusion_lines, render_docx, step_lines
from app.reporting.model import ConclusionSection, Report, TraceSection
from app.schemas.calculation import FormulaStep


def read_back(data: bytes) -> tuple[list[str], list[list[str]]]:
    """Тексты абзацев тела и тексты ячеек каждой строки таблиц."""
    document = Document(BytesIO(data))
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    rows = [[cell.text for cell in row.cells] for table in document.tables for row in table.rows]
    return paragraphs, rows


def test_the_docx_holds_the_body_sections_in_order() -> None:
    paragraphs, _ = read_back(render_docx(report()))

    expected = ["1 Исходные данные", "2 Расчёт", "3 Заключение", "4 Подотчётность результата"]
    assert [text for text in paragraphs if text in expected] == expected


def test_the_input_table_holds_the_inputs_in_the_declared_order() -> None:
    model = report(inputs(b=2000.0, b_unit="mm"))

    _, rows = read_back(render_docx(model))

    assert rows[0] == ["Величина", "Значение"]
    assert rows[1] == ["b", "2000 мм"]
    assert [row[0] for row in rows[1:]] == [row.quantity for row in model.body[0].rows]  # type: ignore[union-attr]


def test_the_trace_prints_each_step_with_the_model_text() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)

    paragraphs, _ = read_back(render_docx(model))

    expected = [line for number, step in enumerate(trace.steps, start=1) for line in step_lines(number, step)]
    start = paragraphs.index("2 Расчёт") + 1
    assert paragraphs[start : start + len(expected)] == expected
    assert "Результат: 172,5 кПа" in paragraphs
    assert r"Выражение: R = \mathrm{synthetic}" in paragraphs
    assert "Сравнение: 100 кПа ≤ 172,5 кПа — выполнено" in paragraphs
    assert "Подстановка: phi_II = 20°" in paragraphs


def test_the_references_print_with_their_status() -> None:
    paragraphs, _ = read_back(render_docx(report(verified_k=True)))

    sources = [text for text in paragraphs if text.startswith("Источник:")]
    assert any(text.endswith("(статус: проверено)") for text in sources)
    assert any(text.endswith("(статус: не проверено)") for text in sources)


def test_a_failed_check_prints_as_not_passed() -> None:
    paragraphs, _ = read_back(render_docx(report(inputs(p=200.0))))

    assert "Проверка не выполнена." in paragraphs
    assert "Сравнение: 200 кПа ≤ 172,5 кПа — не выполнено" in paragraphs


def test_a_refused_report_prints_the_refusal_and_the_bound() -> None:
    model = report(refused=True)
    conclusion = model.body[2]
    assert isinstance(conclusion, ConclusionSection)

    paragraphs, _ = read_back(render_docx(model))

    trace_start = paragraphs.index("2 Расчёт")
    assert paragraphs[trace_start + 1] == "Расчёт не выполнялся: входное значение вне области применения метода."
    assert paragraphs[trace_start + 2] == "3 Заключение"
    lines = conclusion_lines(conclusion)
    assert paragraphs[trace_start + 3 : trace_start + 3 + len(lines)] == lines
    assert paragraphs[trace_start + 3 + len(lines)] == "4 Подотчётность результата"
    assert "Нарушенная граница: b = 2 м, допускается не более 1 м." in paragraphs


def test_every_bound_kind_prints_its_wording() -> None:
    conclusion = report(refused=True).body[2]
    assert isinstance(conclusion, ConclusionSection) and conclusion.violation is not None
    words = []
    for kind, inclusive in [("min", True), ("min", False), ("max", True), ("max", False)]:
        bound = conclusion.violation.bound.model_copy(update={"kind": kind, "inclusive": inclusive})
        section = conclusion.model_copy(update={"violation": conclusion.violation.model_copy(update={"bound": bound})})
        words.append(conclusion_lines(section)[1].split(", допускается ")[1])

    assert words == ["не менее 1 м.", "более 1 м.", "не более 1 м.", "менее 1 м."]


def test_a_report_of_200_trace_steps_renders_in_under_a_minute() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)
    formula = next(step for step in trace.steps if isinstance(step, FormulaStep))
    steps = tuple(formula.model_copy(update={"step_id": f"s{index}"}) for index in range(200))
    long = Report(request=model.request, body=(model.body[0], trace.model_copy(update={"steps": steps}), model.body[2]))

    started = time.perf_counter()
    paragraphs, _ = read_back(render_docx(long))
    elapsed = time.perf_counter() - started

    assert elapsed < 60
    assert "200. Формула s199" in paragraphs
