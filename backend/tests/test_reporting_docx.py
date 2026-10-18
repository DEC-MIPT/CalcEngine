import time
from io import BytesIO

import pytest
from docx import Document
from docx.oxml.ns import qn
from docx.oxml.xmlchemy import BaseOxmlElement
from test_engine_foundations_shallow_r import RULE, inputs, parameters
from test_reporting_model import REQUEST, report

from app.engine import foundations_shallow_r as pilot
from app.engine.registry import CalculatorRegistry
from app.reporting import docx_writer
from app.reporting.accountability import RESPONSIBILITY
from app.reporting.docx_writer import (
    TRACE_NORM_STATUS,
    conclusion_lines,
    render_docx,
    step_lines,
)
from app.reporting.formula import Line, Math, omml
from app.reporting.model import ConclusionSection, Report, TraceSection, build_report
from app.schemas.calculation import FormulaStep, RoundingRule
from app.services.calculation import CalculationService


def visible_text(element: BaseOxmlElement) -> str:
    """Текст прогонов и формул элемента так, как его видит читатель, с обычными пробелами."""
    return "".join(node.text or "" for node in element.iter(qn("w:t"), qn("m:t"))).replace("\xa0", " ")


def read_back(data: bytes) -> tuple[list[str], list[list[str]]]:
    """Видимые тексты абзацев тела и ячеек каждой строки таблиц, вместе с формулами."""
    document = Document(BytesIO(data))
    paragraphs = [visible_text(paragraph._p) for paragraph in document.paragraphs]
    rows = [[visible_text(cell._tc) for cell in row.cells] for table in document.tables for row in table.rows]
    return paragraphs, rows


def plain(line: Line) -> str:
    """Видимый текст строки отчёта, как его вернёт ``read_back``."""
    return "".join(segment if isinstance(segment, str) else visible_text(omml(segment)) for segment in line)


def latex(line: Line) -> str:
    """Строка отчёта с формулами в виде ``$LaTeX$``, для проверок по исходному LaTeX."""
    return "".join(segment if isinstance(segment, str) else f"${segment.latex}$" for segment in line)


def formulas(data: bytes) -> list[BaseOxmlElement]:
    """Все формулы Word в теле документа."""
    return list(Document(BytesIO(data)).element.body.iter(qn("m:oMath")))


def test_the_docx_holds_the_body_sections_in_order() -> None:
    paragraphs, _ = read_back(render_docx(report()))

    expected = ["1 Исходные данные", "2 Расчёт", "3 Заключение"]
    assert [text for text in paragraphs if text in expected] == expected


def test_the_input_table_holds_the_inputs_in_the_declared_order() -> None:
    model = report(inputs(b=2000.0, b_unit="mm"))

    _, rows = read_back(render_docx(model))

    assert rows[0] == ["Величина", "Значение"]
    assert rows[1] == ["b", "2000 мм"]
    assert rows[5] == ["γII′", "20 кН/м³"]
    assert [row[0] for row in rows[1:]] == [
        visible_text(omml(Math(model.symbols[row.quantity])))
        for row in model.body[0].rows  # type: ignore[union-attr]
    ]


def test_the_input_cells_hold_formulas_set_flush_left() -> None:
    document = Document(BytesIO(render_docx(report())))
    cell = document.tables[0].cell(1, 1)._tc

    (paragraph,) = cell.iter(qn("m:oMathPara"))
    justification = paragraph.find(f"{qn('m:oMathParaPr')}/{qn('m:jc')}")
    assert justification is not None and justification.get(qn("m:val")) == "left"
    assert len(list(paragraph.iter(qn("m:oMath")))) == 1


def test_the_trace_prints_each_step_with_the_model_text() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)

    paragraphs, _ = read_back(render_docx(model))

    expected = [
        plain(line) for number, step in enumerate(trace.steps, start=1) for line in step_lines(number, step, model.symbols, model.rounding)
    ]
    start = paragraphs.index("2 Расчёт") + 1
    assert paragraphs[start : start + len(expected)] == expected
    assert "Результат: 172,5 кПа" in paragraphs
    assert "Сравнение: 100 кПа≤172,5 кПа — выполнено" in paragraphs
    assert "Подстановка: φII=20°" in paragraphs


def test_a_step_prints_its_symbol_expression_and_values_as_latex() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)
    steps = {step.step_id: step for step in trace.steps}

    table = [latex(line) for line in step_lines(4, steps["M_gamma"], model.symbols, model.rounding)]
    check = [latex(line) for line in step_lines(9, steps["p_le_R"], model.symbols, model.rounding)]

    assert table[:4] == [
        "4. Табличное значение $M_gamma$",
        r"Выражение: $M_gamma = M_gamma\left(\varphi_{II}\right)$",
        r"Подстановка: $\varphi_{II} = 20\text{°}$",
        "Результат: $0{,}5$",
    ]
    assert check[:4] == [
        r"9. Проверка $p \le R$",
        r"Выражение: $p \le R$",
        r"Подстановка: $p = 100\ \text{кПа}$; $R = 172{,}5\ \text{кПа}$",
        r"Сравнение: $100\ \text{кПа} \le 172{,}5\ \text{кПа}$ — выполнено",
    ]


def hundredths_report() -> Report:
    rule = RoundingRule(decimals=2, mode="half_up")
    registry = CalculatorRegistry()
    pilot.register(registry, rule, RULE)
    given = inputs()
    result = CalculationService(registry).run(pilot.NAME, given, parameters())
    return build_report(pilot.contract(rule, RULE), given, result, REQUEST)


def test_the_values_of_an_output_print_by_its_rounding_rule() -> None:
    model = hundredths_report()
    trace, conclusion = model.body[1], model.body[2]
    assert isinstance(trace, TraceSection) and isinstance(conclusion, ConclusionSection)
    steps = {step.step_id: step for step in trace.steps}

    r = [latex(line) for line in step_lines(8, steps["R"], model.symbols, model.rounding)]
    check = [latex(line) for line in step_lines(9, steps["p_le_R"], model.symbols, model.rounding)]
    deciding = latex(conclusion_lines(conclusion, model.symbols, model.rounding)[1])

    assert r[3] == r"Результат: $172{,}50\ \text{кПа}$"
    assert check[2] == r"Подстановка: $p = 100\ \text{кПа}$; $R = 172{,}50\ \text{кПа}$"
    assert check[3] == r"Сравнение: $100\ \text{кПа} \le 172{,}50\ \text{кПа}$ — выполнено"
    assert deciding == r"Определяющая проверка: $p \le R$; $100\ \text{кПа} \le 172{,}50\ \text{кПа}$ — выполнено."
    assert steps["R"].result.value == 172.5


def test_only_the_step_expression_may_break_across_lines() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)

    lines = [line for number, step in enumerate(trace.steps, start=1) for line in step_lines(number, step, model.symbols, model.rounding)]

    breakable = {line[0] for line in lines for segment in line if isinstance(segment, Math) and segment.breakable}
    assert breakable == {"Выражение: "}


def test_a_step_without_a_symbol_prints_its_name() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)
    formula = next(step for step in trace.steps if isinstance(step, FormulaStep) and step.substitutions)
    unnamed = formula.model_copy(update={"step_id": "s1", "substitutions": formula.substitutions[:1]})

    lines = [latex(line) for line in step_lines(1, unnamed, {}, {})]

    assert lines[0] == "1. Формула s1"
    assert lines[2] == "Подстановка: gamma_c1 = $2$"


def test_the_trace_references_print_without_their_status() -> None:
    paragraphs, _ = read_back(render_docx(report(verified_k=True)))

    trace = paragraphs[paragraphs.index("2 Расчёт") : paragraphs.index("3 Заключение")]
    sources = [text for text in trace if text.startswith("Источник:")]
    assert not TRACE_NORM_STATUS
    assert sources and not any("статус" in text for text in sources)


def test_the_trace_references_print_with_their_status_when_the_setting_is_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(docx_writer, "TRACE_NORM_STATUS", True)
    paragraphs, _ = read_back(render_docx(report(verified_k=True)))

    trace = paragraphs[paragraphs.index("2 Расчёт") : paragraphs.index("3 Заключение")]
    sources = [text for text in trace if text.startswith("Источник:")]
    assert sources and all("(статус:" in text for text in sources)
    assert any(text.endswith("(статус: проверено)") for text in sources)
    assert any(text.endswith("(статус: не проверено)") for text in sources)


def test_a_failed_check_prints_as_not_passed() -> None:
    paragraphs, _ = read_back(render_docx(report(inputs(p=200.0))))

    assert "Проверка не выполнена." in paragraphs
    assert "Сравнение: 200 кПа≤172,5 кПа — не выполнено" in paragraphs
    assert "Определяющая проверка: p≤R; 200 кПа≤172,5 кПа — не выполнено." in paragraphs


def test_a_refused_report_prints_the_refusal_and_the_bound() -> None:
    model = report(refused=True)
    conclusion = model.body[2]
    assert isinstance(conclusion, ConclusionSection)

    paragraphs, _ = read_back(render_docx(model))

    trace_start = paragraphs.index("2 Расчёт")
    assert paragraphs[trace_start + 1] == "Расчёт не выполнялся: входное значение вне области применения метода."
    assert paragraphs[trace_start + 2] == "3 Заключение"
    lines = conclusion_lines(conclusion, model.symbols, model.rounding)
    assert paragraphs[trace_start + 3 : trace_start + 3 + len(lines)] == [plain(line) for line in lines]
    assert paragraphs[trace_start + 3 + len(lines) :] == [RESPONSIBILITY]
    assert latex(lines[1]) == r"Нарушенная граница: $b = 2\ \text{м}$, допускается не более $1\ \text{м}$."
    assert plain(lines[2]).endswith("(статус: не проверено)")


def test_every_bound_kind_prints_its_wording() -> None:
    conclusion = report(refused=True).body[2]
    assert isinstance(conclusion, ConclusionSection) and conclusion.violation is not None
    words = []
    for kind, inclusive in [("min", True), ("min", False), ("max", True), ("max", False)]:
        bound = conclusion.violation.bound.model_copy(update={"kind": kind, "inclusive": inclusive})
        section = conclusion.model_copy(update={"violation": conclusion.violation.model_copy(update={"bound": bound})})
        words.append(plain(conclusion_lines(section, {}, {})[1]).split(", допускается ")[1])

    assert words == ["не менее 1 м.", "более 1 м.", "не более 1 м.", "менее 1 м."]


def test_a_report_of_200_trace_steps_renders_in_under_a_minute() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)
    formula = next(step for step in trace.steps if isinstance(step, FormulaStep))
    steps = tuple(formula.model_copy(update={"step_id": f"s{index}"}) for index in range(200))
    long = Report(
        request=model.request,
        body=(model.body[0], trace.model_copy(update={"steps": steps}), model.body[2], model.body[3]),
        symbols=model.symbols,
        rounding=model.rounding,
    )

    started = time.perf_counter()
    paragraphs, _ = read_back(render_docx(long))
    elapsed = time.perf_counter() - started

    assert elapsed < 60
    assert "200. Формула s199" in paragraphs
    assert "3 Заключение" in paragraphs


def test_a_report_whose_step_latex_cannot_be_converted_still_renders() -> None:
    model = report()
    trace = model.body[1]
    assert isinstance(trace, TraceSection)
    broken = r"R = \frac{\gamma_{c1}}{"
    steps = tuple(step.model_copy(update={"expression": broken}) if step.step_id == "R" else step for step in trace.steps)
    damaged = Report(
        request=model.request,
        body=(model.body[0], trace.model_copy(update={"steps": steps}), *model.body[2:]),
        symbols=model.symbols,
        rounding=model.rounding,
    )

    paragraphs, _ = read_back(render_docx(damaged))

    assert f"Выражение: {broken}" in paragraphs
    assert "3 Заключение" in paragraphs
