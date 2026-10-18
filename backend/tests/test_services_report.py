import datetime
import uuid

import pytest
from sqlalchemy.orm import Session
from test_reporting_docx import plain, read_back
from test_services_submit import (
    CONTRACT,
    REF,
    FixedSource,
    SpyRepository,
    make_service,
    request,
)

from app.core.exceptions import (
    CalculationTypeNotRegisteredError,
    DECError,
    NotFoundError,
)
from app.engine.registry import CalculatorRegistry
from app.reporting.docx_writer import conclusion_lines
from app.reporting.model import ConclusionSection, build_report
from app.schemas.calculation import MethodBound
from app.schemas.report import ReportRequest, Signatory, TitleBlockData
from app.services.calculation import CalculationService

DAY = datetime.date(2026, 10, 3)
REPORT_REQUEST = ReportRequest(
    title=TitleBlockData(
        designation="<DESIGNATION>", document_name="<DOCUMENT-NAME>", organization="<ORGANIZATION>"
    ),
    developer=Signatory(surname="<DEVELOPER>", date=DAY),
    normative_control=Signatory(surname="<NORM-CONTROL>", date=DAY),
)
HEADINGS = ["1 Исходные данные", "2 Расчёт", "3 Заключение"]


@pytest.fixture
def results(sqlite_session: Session) -> SpyRepository:
    return SpyRepository(sqlite_session)


def test_the_report_holds_the_stored_inputs_trace_and_conclusion(
    results: SpyRepository, engine_calls: list[str]
) -> None:
    service = make_service(results, FixedSource())
    envelope = service.submit(request(b={"value": 1500.0, "unit": "mm"}))

    paragraphs, rows = read_back(service.report(envelope.result_id, REPORT_REQUEST))

    assert [text for text in paragraphs if text in HEADINGS] == HEADINGS
    assert ["b", "1500 мм"] in rows
    assert [row[0] for row in rows if row[0] in ("b", "d", "p")] == ["b", "d", "p"]
    assert "Выражение: y=2b" in paragraphs
    assert engine_calls == ["synthetic"]


def test_a_refused_result_s_report_states_the_refusal_and_names_the_bound(results: SpyRepository) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))
    service = make_service(results, FixedSource(method_range=(bound,)))
    envelope = service.submit(request())
    stored = service.get(envelope.result_id)
    model = build_report(CONTRACT, stored.inputs, stored.envelope, REPORT_REQUEST)
    conclusion = model.body[2]
    assert isinstance(conclusion, ConclusionSection)
    expected = [plain(line) for line in conclusion_lines(conclusion, model.symbols, model.rounding)]

    paragraphs, _ = read_back(service.report(envelope.result_id, REPORT_REQUEST))

    start = paragraphs.index("3 Заключение") + 1
    assert paragraphs[start : start + len(expected)] == expected
    assert any("b" in line and "1 м" in line for line in expected)


def test_an_unknown_result_has_no_report(results: SpyRepository) -> None:
    with pytest.raises(NotFoundError):
        make_service(results, FixedSource()).report(uuid.uuid4(), REPORT_REQUEST)


def test_a_result_whose_type_is_no_longer_registered_gives_its_own_error(results: SpyRepository) -> None:
    envelope = make_service(results, FixedSource()).submit(request())
    without_type = CalculationService(CalculatorRegistry(), results=results)

    with pytest.raises(CalculationTypeNotRegisteredError, match="'synthetic'") as raised:
        without_type.report(envelope.result_id, REPORT_REQUEST)

    assert isinstance(raised.value, DECError)
    assert not isinstance(raised.value, NotFoundError)
