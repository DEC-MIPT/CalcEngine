import pytest
from test_engine_foundations_shallow_r import (
    ROUNDING,
    RULE,
    inputs,
    parameters,
)
from test_reporting_docx import hundredths_report, latex, plain, read_back
from test_reporting_model import REQUEST, report, service

from app.engine import foundations_shallow_r as pilot
from app.reporting import docx_writer
from app.reporting.accountability import RESPONSIBILITY, accountability_lines
from app.reporting.docx_writer import conclusion_lines, render_docx
from app.reporting.format import (
    DRAFT_CAVEAT,
    format_parameter_source,
    parameter_source_lines,
)
from app.reporting.model import (
    AccountabilitySection,
    ConclusionSection,
    Report,
    build_report,
)
from app.schemas.calculation import CATALOG_SOURCE, ParameterSourceInfo, ValidatedBound

WARNING_BOUND = ValidatedBound(quantity="b", kind="max", value=1.0, inclusive=True, source=RULE)
INTERIM = ParameterSourceInfo(kind="interim", data_sha256="0123456789abcdef" * 4, profile="strict")
SOURCE_PREFIX = "Источник нормативных параметров"


@pytest.fixture
def printed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Включает печать раздела подотчётности, выключенную в первой итерации пилота."""
    monkeypatch.setattr(docx_writer, "ACCOUNTABILITY_SECTION", True)


def sourced_report(source: ParameterSourceInfo | None) -> Report:
    """Отчёт пилота по результату, конверт которого несёт данный источник параметров."""
    given = inputs()
    result = service().run(pilot.NAME, given, parameters(), source=source)
    return build_report(pilot.contract(ROUNDING, RULE), given, result, REQUEST)


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


@pytest.mark.usefixtures("printed")
def test_the_report_states_that_the_engineer_is_responsible() -> None:
    paragraphs, _ = read_back(render_docx(report()))

    assert paragraphs[-1] == RESPONSIBILITY
    assert "инженер-проектировщик, а не система" in RESPONSIBILITY


@pytest.mark.usefixtures("printed")
def test_the_block_is_the_last_body_section_of_the_docx() -> None:
    model = report()
    paragraphs, _ = read_back(render_docx(model))

    start = paragraphs.index("4 Подотчётность результата")
    lines = accountability_lines(block(model.body[-1]), model.symbols)
    assert paragraphs[start + 1 :] == [*(plain(line) for line in lines), RESPONSIBILITY]
    assert paragraphs.count(RESPONSIBILITY) == 1


def test_the_block_is_not_printed_in_the_first_pilot_iteration() -> None:
    paragraphs, _ = read_back(render_docx(report()))

    assert not docx_writer.ACCOUNTABILITY_SECTION
    assert "4 Подотчётность результата" not in paragraphs
    assert not any(text.startswith("Идентификатор результата") for text in paragraphs)


def test_without_the_block_the_conclusion_ends_with_the_responsibility_statement() -> None:
    model = report()
    conclusion = model.body[2]
    assert isinstance(conclusion, ConclusionSection)
    paragraphs, _ = read_back(render_docx(model))

    start = paragraphs.index("3 Заключение")
    lines = conclusion_lines(conclusion, model.symbols, model.rounding)
    assert paragraphs[start + 1 :] == [*(plain(line) for line in lines), RESPONSIBILITY]
    assert paragraphs.count(RESPONSIBILITY) == 1


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


def test_an_interim_line_stands_in_the_conclusion_right_before_the_responsibility_statement() -> None:
    model = sourced_report(INTERIM)
    conclusion = model.body[2]
    assert isinstance(conclusion, ConclusionSection)
    paragraphs, _ = read_back(render_docx(model))

    start = paragraphs.index("3 Заключение")
    lines = conclusion_lines(conclusion, model.symbols, model.rounding)
    line = (
        "Источник нормативных параметров: временные нормативные данные, профиль strict,"
        f" SHA-256 данных {'0123456789abcdef' * 4}."
    )
    assert paragraphs[start + 1 :] == [*(plain(item) for item in lines), line, RESPONSIBILITY]
    assert paragraphs.count(line) == 1


@pytest.mark.usefixtures("printed")
@pytest.mark.parametrize("source", [INTERIM, CATALOG_SOURCE], ids=["interim", "catalog"])
def test_with_the_block_printed_the_source_line_moves_there_and_appears_once(source: ParameterSourceInfo) -> None:
    model = sourced_report(source)
    paragraphs, _ = read_back(render_docx(model))

    line = format_parameter_source(source)
    conclusion, accountability = paragraphs.index("3 Заключение"), paragraphs.index("4 Подотчётность результата")
    assert line not in paragraphs[conclusion:accountability]
    assert paragraphs[-2:] == [line, RESPONSIBILITY]
    assert latex(accountability_lines(block(model.body[-1]), model.symbols)[-1]) == line
    assert paragraphs.count(line) == 1


def test_a_result_without_a_source_prints_the_report_without_the_line() -> None:
    with_source, _ = read_back(render_docx(sourced_report(INTERIM)))
    without_source, _ = read_back(render_docx(sourced_report(None)))

    assert not any(text.startswith(SOURCE_PREFIX) for text in without_source)
    assert without_source == [text for text in with_source if not text.startswith(SOURCE_PREFIX)]


def test_a_result_without_a_source_has_no_line_in_the_block() -> None:
    with_source = sourced_report(INTERIM)
    without_source = sourced_report(None)

    printed_with = [latex(line) for line in accountability_lines(block(with_source.body[-1]), with_source.symbols)]
    printed_without = [latex(line) for line in accountability_lines(block(without_source.body[-1]), without_source.symbols)]

    assert printed_without[1:] == printed_with[1:-1]
    assert not any(text.startswith(SOURCE_PREFIX) for text in printed_without)


DRAFT = ParameterSourceInfo(kind="interim", data_sha256="fedcba9876543210" * 4, profile="draft")


def test_a_draft_result_prints_the_caveat_in_the_conclusion_after_the_source_line_and_once() -> None:
    model = sourced_report(DRAFT)
    paragraphs, _ = read_back(render_docx(model))

    line, caveat = parameter_source_lines(DRAFT)
    assert paragraphs[-3:] == [line, caveat, RESPONSIBILITY]
    assert paragraphs.count(caveat) == 1
    assert "не прошедших верификацию" in caveat
    assert not any(character.isdigit() for character in caveat)


@pytest.mark.parametrize("source", [INTERIM, CATALOG_SOURCE], ids=["strict", "catalog"])
def test_a_result_that_is_not_draft_prints_no_caveat(source: ParameterSourceInfo) -> None:
    paragraphs, _ = read_back(render_docx(sourced_report(source)))

    assert DRAFT_CAVEAT not in paragraphs
    assert parameter_source_lines(source) == [format_parameter_source(source)]


@pytest.mark.usefixtures("printed")
def test_a_draft_result_moves_the_caveat_with_the_source_line_into_the_block() -> None:
    model = sourced_report(DRAFT)
    paragraphs, _ = read_back(render_docx(model))

    line, caveat = parameter_source_lines(DRAFT)
    conclusion, accountability = paragraphs.index("3 Заключение"), paragraphs.index("4 Подотчётность результата")
    assert caveat not in paragraphs[conclusion:accountability]
    assert paragraphs[-3:] == [line, caveat, RESPONSIBILITY]
    assert [latex(item) for item in accountability_lines(block(model.body[-1]), model.symbols)[-2:]] == [line, caveat]
