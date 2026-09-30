from test_engine_foundations_shallow_r import (
    ROUNDING,
    RULE,
    inputs,
    parameters,
)
from test_reporting_docx import read_back
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
    section = block(report().body[-1])
    envelope = section.envelope

    lines = accountability_lines(section)

    assert lines[:3] == [
        f"Идентификатор результата (result_id): {envelope.result_id}",
        f"Версия движка (engine_version): {envelope.engine_version}",
        f"Хеш входных данных (input_hash): {envelope.input_hash}",
    ]
    assert (
        "— R = 172,5 кПа; округление: 1 знак(а) после запятой, половина — от нуля;"
        " источник правила: решение инженера <ENGINEER>: <RATIONALE>"
    ) in lines
    references = lines[lines.index("Нормативные ссылки (norm_refs):") + 1]
    assert references.startswith("— <NORM-DOC-PLACEHOLDER>") and references.endswith("(статус: не проверено)")
    assert "— решение инженера <ENGINEER>: <RATIONALE>" in lines
    assert "Вердикт (verdict): выполнено; основание (verdict_reason): определяющая проверка p_le_R" in lines
    assert "Предупреждения (warnings): нет" in lines
    assert lines[-1] == "Шагов с непроверенными ссылками (unverified_step_count): 9"


def test_the_report_states_that_the_engineer_is_responsible() -> None:
    paragraphs, _ = read_back(render_docx(report()))

    assert paragraphs[-1] == RESPONSIBILITY
    assert "инженер-проектировщик, а не система" in RESPONSIBILITY


def test_the_block_is_the_last_body_section_of_the_docx() -> None:
    model = report()
    paragraphs, _ = read_back(render_docx(model))

    start = paragraphs.index("4 Подотчётность результата")
    assert paragraphs[start + 1 :] == [*accountability_lines(block(model.body[-1])), RESPONSIBILITY]


def test_a_warning_prints_with_the_input_the_bound_and_its_source() -> None:
    given = inputs()
    result = service().run(pilot.NAME, given, parameters(), validated_range=(WARNING_BOUND,))

    lines = accountability_lines(block(build_report(pilot.contract(ROUNDING, RULE), given, result, REQUEST).body[-1]))

    assert "Предупреждения (warnings):" in lines
    assert (
        "— b = 2 м вне проверенного диапазона, допускается не более 1 м;"
        " источник: решение инженера <ENGINEER>: <RATIONALE>"
    ) in lines


def test_a_refused_result_names_the_bound_and_its_norm_references() -> None:
    lines = accountability_lines(block(report(refused=True).body[-1]))

    verdict = next(line for line in lines if line.startswith("Вердикт"))
    assert verdict.startswith(
        "Вердикт (verdict): расчёт отклонён; основание (verdict_reason): нарушенная граница"
        " области применения метода: b = 2 м, допускается не более 1 м; источник: <NORM-DOC-PLACEHOLDER>"
    )
    assert "Выходные величины (outputs): нет" in lines
    assert lines[-1] == "Шагов с непроверенными ссылками (unverified_step_count): 0"
