import datetime
from io import BytesIO

from docx import Document
from docx.table import Table
from test_reporting_docx import read_back
from test_reporting_model import REQUEST, report

from app.reporting.docx_writer import render_docx
from app.reporting.format import format_date
from app.reporting.model import Report
from app.reporting.title_block import (
    CHECKER_CAPTION,
    DATE_SIZE_PT,
    SIGNATURE_COLUMNS,
    SIGNATURE_ROWS,
)
from app.schemas.report import ReportRequest, Signatory

DEVELOPER = Signatory(surname="<DEVELOPER>", date=datetime.date(2026, 9, 30))
CONTROL = Signatory(surname="<CONTROL>", date=datetime.date(2026, 10, 1))
CHECKER = Signatory(surname="<CHECKER>", date=datetime.date(2026, 10, 2))


def with_request(**changes: object) -> Report:
    model = report()
    request = REQUEST.model_copy(update={"developer": DEVELOPER, "normative_control": CONTROL} | changes)
    return model.model_copy(update={"request": ReportRequest.model_validate(request.model_dump())})


def form5(model: Report) -> Table:
    return Document(BytesIO(render_docx(model))).sections[0].first_page_footer.tables[0]


def line(table: Table, role: str) -> list[str]:
    row = SIGNATURE_ROWS[role]
    return [table.cell(row, SIGNATURE_COLUMNS[column]).text for column in ("10", "11", "12", "13")]


def test_the_date_prints_as_day_month_and_two_digit_year() -> None:
    assert format_date(datetime.date(2026, 9, 30)) == "30.09.26"
    assert format_date(datetime.date(2031, 1, 5)) == "05.01.31"


def test_the_default_fills_the_developer_and_normative_control_lines() -> None:
    table = form5(with_request())

    assert with_request().request.signature_block is True
    assert line(table, "developer") == ["Разраб.", "<DEVELOPER>", "", "30.09.26"]
    assert line(table, "normative_control") == ["Н. контр.", "<CONTROL>", "", "01.10.26"]


def test_a_checker_takes_the_row_under_the_developer() -> None:
    table = form5(with_request(checker=CHECKER))

    assert line(table, "checker") == [CHECKER_CAPTION, "<CHECKER>", "", "02.10.26"]
    assert SIGNATURE_ROWS["checker"] == SIGNATURE_ROWS["developer"] + 1


def test_without_a_checker_its_row_is_empty() -> None:
    assert line(form5(with_request()), "checker") == ["", "", "", ""]


def test_a_disabled_block_keeps_the_captions_and_prints_no_surname_or_date() -> None:
    table = form5(with_request(signature_block=False, checker=CHECKER))

    assert line(table, "developer") == ["Разраб.", "", "", ""]
    assert line(table, "checker") == ["", "", "", ""]
    assert line(table, "normative_control") == ["Н. контр.", "", "", ""]


def test_the_body_section_order_is_the_same_with_the_block_enabled_and_disabled() -> None:
    headings = {
        enabled: [text for text in read_back(render_docx(with_request(signature_block=enabled)))[0] if text[:2] in {"1 ", "2 ", "3 ", "4 "}]
        for enabled in (True, False)
    }

    assert headings[True] == headings[False] == [
        "1 Исходные данные",
        "2 Расчёт",
        "3 Заключение",
        "4 Подотчётность результата",
    ]


def test_the_date_prints_small_enough_for_column_13() -> None:
    table = form5(with_request())
    runs = table.cell(SIGNATURE_ROWS["developer"], SIGNATURE_COLUMNS["13"]).paragraphs[0].runs

    assert [(run.text, run.font.size.pt if run.font.size else None) for run in runs] == [("30.09.26", DATE_SIZE_PT)]
