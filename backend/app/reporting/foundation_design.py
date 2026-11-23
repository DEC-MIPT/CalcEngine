from collections.abc import Mapping
from io import BytesIO

from docx import Document
from docx.document import Document as DocumentObject
from docx.shared import Mm

from app.reporting.accountability import RESPONSIBILITY
from app.reporting.docx_writer import conclusion_lines, render_docx, write_line
from app.reporting.format import latex_quantity, parameter_source_lines
from app.reporting.formula import Math
from app.reporting.foundation_figures import foundation_figure
from app.reporting.layout import apply_sheet, fit_table
from app.reporting.model import ConclusionSection, Report, build_report
from app.reporting.symbols import math_symbol
from app.reporting.title_block import add_title_blocks
from app.schemas.calculation import CalculationTypeContract, QuantityValue, RoundingRule
from app.schemas.foundation_design import FoundationContext, FoundationSelectionResult
from app.schemas.report import ReportRequest


def _pressure_rule(value: float, rule: RoundingRule | None) -> RoundingRule | None:
    return None if rule is not None and value < 0 and rule.apply(value) == 0 else rule


def _quantities(
    document: DocumentObject, values: Mapping[str, QuantityValue], *,
    report: Report | None = None, origin: str = "", diagnostic: bool = False,
) -> None:
    table = document.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.rows[0].cells[0].text = "Величина / источник"
    table.rows[0].cells[1].text = "Значение"
    for name, value in values.items():
        row = table.add_row().cells
        if report is None:
            row[0].text = f"{origin}{name}"
            row[1].text = f"{value.value} {value.unit}"
        else:
            write_line(row[0].paragraphs[0], (math_symbol(name, report.symbols),))
            rule = report.rounding.get(name, report.default_rounding) if origin == "trace:" else report.default_rounding
            if diagnostic and value.unit == "kPa":
                rule = _pressure_rule(value.value, rule)
            write_line(row[1].paragraphs[0], (Math(latex_quantity(value, rule)),))
    fit_table(table)


def append_foundation_context(
    document: DocumentObject, context: FoundationContext, report: Report | None = None,
) -> None:
    document.add_heading("Схема нагрузок и давление под подошвой", level=2)
    if report is None:
        document.add_paragraph(f"Методика: {context.methodology_version}; уровень нагрузок: {context.load_level}; учёт веса: {context.weight_mode}.")
        document.add_paragraph("Направления изменения давления: x=b, y=l; положительные Mx и Qx увеличивают давление к +x, My и Qy к +y. Нагрузки N, Mx, My, Qx, Qy приложены на верхнем срезе; плечо до подошвы h. Значения ниже взяты из сохранённых входов и шагов трассы.")
    else:
        document.add_paragraph(f"Методика: {context.methodology_version}. Явные веса. Нагрузки заданы на верхнем срезе.")
        write_line(document.add_paragraph(), (
            "Направления изменения давления: ", Math("x=b"), ", ", Math("y=l"),
            ". Значения взяты из сохранённых входов и шагов расчёта.",
        ))
    if context.pressure_state == "diagnostic":
        document.add_paragraph("Диагностическая эпюра: условие полного контакта нарушено. Перераспределение при частичном контакте не вычисляется.")
    elif context.pressure_state == "full_contact":
        document.add_paragraph("Эпюра в области полного контакта.")
    picture = document.add_picture(foundation_figure(context), width=Mm(160))
    if report is not None and context.pressure_state == "unavailable":
        picture._inline.docPr.set("descr", "Схема нагрузок на верхнем срезе и плечо до подошвы. Угловые давления отсутствуют.")
        document.add_paragraph("Схема нагрузок условная. Стрелки показывают знаки сохранённых нагрузок.")
    else:
        picture._inline.docPr.set("descr", "Слева схема верхнего среза и подошвы: N по вертикали, Qx по горизонтали, Qy по диагонали, дуги Mx слева и My справа; двусторонняя вертикальная стрелка — плечо h. Справа пространственная эпюра по четырём сохранённым угловым давлениям; серый контур — нулевое давление. Числовая альтернатива приведена в таблицах.")
        document.add_paragraph("Слева: схема нагрузок на верхнем срезе и плечо h; стрелки показывают знаки сохранённых нагрузок. Справа: эпюра четырёх угловых давлений относительно серого нулевого контура. Геометрия нагрузочной схемы условная; эпюра масштабирована по значениям таблицы.")
    input_names = ("N", "Mx", "My", "Qx", "Qy", "h", "G_fund", "G_soil", "G_other", "Mx_add_base", "My_add_base")
    if report is not None:
        document.add_heading("Нагрузки и веса", level=3)
    inputs = context.inputs if report is None else {name: context.inputs[name] for name in input_names}
    _quantities(document, inputs, report=report, origin="input:")
    if report is not None:
        document.add_heading("Размеры подошвы", level=3)
        _quantities(document, context.geometry, report=report)
    diagram_steps = {"A", "Wx", "Wy", "gamma_mt", "G_sum", "V", "Mx_base", "My_base", "p", "p_x_min", "p_x_max", "p_y_min", "p_y_max", "p_corner_pp", "p_corner_pm", "p_corner_mp", "p_corner_mm", "p_corner_min", "p_corner_max"}
    stored_steps = {name: value for name, value in context.trace_values.items() if name in diagram_steps}
    if stored_steps or report is None:
        if report is not None:
            document.add_heading("Величины по шагам расчёта", level=3)
        _quantities(document, stored_steps, report=report, origin="trace:", diagnostic=context.pressure_state == "diagnostic")
    if context.pressure_state == "unavailable":
        document.add_paragraph("Эпюра недоступна: угловые давления отсутствуют в сохранённой трассе.")
        return
    document.add_paragraph("Текстовая альтернатива эпюры: четыре угла прямоугольника с координатами и знаковыми давлениями из сохранённых шагов.")
    table = document.add_table(rows=1, cols=5)
    table.style = "Table Grid"
    for cell, text in zip(table.rows[0].cells, ("Угол", "x, м", "y, м", "p, кПа", "Шаг трассы")):
        cell.text = text
    for corner in context.corners:
        cells = table.add_row().cells
        cells[0].text, cells[4].text = corner.name, corner.step_id
        for index, value in enumerate((corner.x, corner.y, corner.pressure), start=1):
            if report is None:
                cells[index].text = str(value.value)
            else:
                rule = (report.rounding.get(corner.step_id, report.default_rounding)
                        if index == 3 else report.default_rounding)
                if index == 3 and context.pressure_state == "diagnostic":
                    rule = _pressure_rule(value.value, rule)
                number = latex_quantity(value.model_copy(update={"unit": "1"}), rule)
                write_line(cells[index].paragraphs[0], (Math(number),))
    fit_table(table)


def render_foundation_docx(report: Report, context: FoundationContext) -> bytes:
    document = Document(BytesIO(render_docx(report)))
    append_foundation_context(document, context, report if report.default_rounding is not None else None)
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def render_selection_docx(selection: FoundationSelectionResult, request: ReportRequest, contract: CalculationTypeContract, context: FoundationContext | None) -> bytes:
    selected = None if selection.selected_candidate_index is None else selection.outcomes[selection.selected_candidate_index].envelope
    if selected is not None and selection.selected_candidate_index is not None:
        candidate = selection.request.candidates[selection.selected_candidate_index]
        inputs = selection.request.common_inputs | {"b": candidate.b, "l": candidate.l}
        document = Document(BytesIO(render_docx(build_report(contract, inputs, selected, request))))
    else:
        document = Document()
        apply_sheet(document)
        add_title_blocks(document, request)
    document.add_heading("Подбор подошвы фундамента", level=1)
    document.add_paragraph(f"Статус: {selection.status}")
    document.add_paragraph(f"Политика: {selection.request.policy_version}; минимум площади среди прошедших проверку, при равенстве — первый исходный индекс.")
    document.add_paragraph(f"Идентификатор подбора: {selection.selection_id}; хеш: {selection.input_hash}")
    document.add_paragraph(f"Причина остановки: {selection.stop_reason or 'нет'}; выбранный индекс: {selection.selected_candidate_index}; результат: {selection.selected_result_id}")
    document.add_heading("Общие исходные данные", level=2)
    _quantities(document, selection.request.common_inputs)
    for outcome in selection.outcomes:
        document.add_heading(f"Кандидат {outcome.index + 1}", level=2)
        _quantities(document, {"b": outcome.candidate.b, "l": outcome.candidate.l})
        document.add_paragraph(f"Статус: {outcome.status}; причина: {outcome.reason or 'нет'}")
        if outcome.envelope is None:
            continue
        candidate_report = build_report(contract, selection.request.common_inputs | {"b": outcome.candidate.b, "l": outcome.candidate.l}, outcome.envelope, request)
        for section in candidate_report.body:
            if isinstance(section, ConclusionSection):
                for line in conclusion_lines(section, candidate_report.symbols, candidate_report.rounding):
                    write_line(document.add_paragraph(), line)
        document.add_paragraph(f"Результат: {outcome.envelope.result_id}; движок: {outcome.envelope.engine_version}; хеш: {outcome.envelope.input_hash}")
        if outcome.envelope.parameter_source is not None:
            for text in parameter_source_lines(outcome.envelope.parameter_source):
                document.add_paragraph(text)
        _quantities(document, {output.quantity: output for output in outcome.envelope.outputs})
    if context is not None:
        append_foundation_context(document, context)
    if selected is None:
        document.add_paragraph("Подтверждённый размер не выбран. Обычный успешный результат не сформирован.")
    document.add_paragraph(RESPONSIBILITY)
    output = BytesIO()
    document.save(output)
    return output.getvalue()
