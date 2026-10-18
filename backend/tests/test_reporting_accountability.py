from test_engine_foundations_shallow_r import (
    ROUNDING,
    RULE,
    inputs,
    parameters,
)
from test_reporting_docx import hundredths_report, latex, plain, read_back
from test_reporting_model import REQUEST, report, service

from app.engine import foundations_shallow_r as pilot
from app.reporting.accountability import RESPONSIBILITY, accountability_lines
from app.reporting.docx_writer import render_docx
from app.reporting.model import AccountabilitySection, build_report
from app.schemas.calculation import ValidatedBound

WARNING_BOUND = ValidatedBound(quantity="b", kind="max", value=1.0, inclusive=True, source=RULE)


def block(section: object) -> AccountabilitySection:
    assert isinstance(section, AccountabilitySection)
    return section


def test_the_block_shows_every_field_of_the_envelope() -> None:
    model = report()
    section = block(model.body[-1])
    envelope = section.envelope

    lines = [latex(line) for line in accountability_lines(section, model.symbols)]

    assert lines[:3] == [
        f"Идентификатор результата (result_id): {envelope.result_id}",
        f"Версия движка (engine_version): {envelope.engine_version}",
        f"Хеш входных данных (input_hash): {envelope.input_hash}",
    ]
    assert (
        r"— $R = 172{,}5\ \text{кПа}$; округление: 1 знак(а) после запятой, половина — от нуля;"
        " источник правила: решение инженера <ENGINEER>: <RATIONALE>"
    ) in lines
    references = lines[lines.index("Нормативные ссылки (norm_refs):") + 1]
    assert references.startswith("— <NORM-DOC-PLACEHOLDER>") and references.endswith("(статус: не проверено)")
    assert "— решение инженера <ENGINEER>: <RATIONALE>" in lines
    assert r"Вердикт (verdict): выполнено; основание (verdict_reason): определяющая проверка $p \le R$" in lines
    assert "Предупреждения (warnings): нет" in lines
    assert lines[-1] == "Шагов с непроверенными ссылками (unverified_step_count): 9"


def test_an_output_prints_with_exactly_the_decimals_of_its_rule() -> None:
    model = hundredths_report()

    lines = [latex(line) for line in accountability_lines(block(model.body[-1]), model.symbols)]

    assert any(line.startswith(r"— $R = 172{,}50\ \text{кПа}$; округление: 2 знак(а)") for line in lines)


def test_the_report_states_that_the_engineer_is_responsible() -> None:
    paragraphs, _ = read_back(render_docx(report()))

    assert paragraphs[-1] == RESPONSIBILITY
    assert "инженер-проектировщик, а не система" in RESPONSIBILITY


def test_the_block_is_the_last_body_section_of_the_docx() -> None:
    model = report()
    paragraphs, _ = read_back(render_docx(model))

    start = paragraphs.index("4 Подотчётность результата")
    lines = accountability_lines(block(model.body[-1]), model.symbols)
    assert paragraphs[start + 1 :] == [*(plain(line) for line in lines), RESPONSIBILITY]


def test_a_warning_prints_with_the_input_the_bound_and_its_source() -> None:
    given = inputs()
    result = service().run(pilot.NAME, given, parameters(), validated_range=(WARNING_BOUND,))

    model = build_report(pilot.contract(ROUNDING, RULE), given, result, REQUEST)

    lines = [latex(line) for line in accountability_lines(block(model.body[-1]), model.symbols)]

    assert "Предупреждения (warnings):" in lines
    assert (
        r"— $b = 2\ \text{м}$ вне проверенного диапазона, допускается не более $1\ \text{м}$;"
        " источник: решение инженера <ENGINEER>: <RATIONALE>"
    ) in lines


def test_a_refused_result_names_the_bound_and_its_norm_references() -> None:
    model = report(refused=True)

    lines = [latex(line) for line in accountability_lines(block(model.body[-1]), model.symbols)]

    verdict = next(line for line in lines if line.startswith("Вердикт"))
    assert verdict.startswith(
        "Вердикт (verdict): расчёт отклонён; основание (verdict_reason): нарушенная граница"
        r" области применения метода: $b = 2\ \text{м}$, допускается не более $1\ \text{м}$;"
        " источник: <NORM-DOC-PLACEHOLDER>"
    )
    assert "Выходные величины (outputs): нет" in lines
    assert lines[-1] == "Шагов с непроверенными ссылками (unverified_step_count): 0"
