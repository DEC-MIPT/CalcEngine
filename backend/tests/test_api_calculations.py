import json
import logging
import uuid
from collections.abc import Iterator
from io import BytesIO
from typing import Any

import pytest
from docx import Document
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from test_reporting_docx import read_back
from test_services_report import HEADINGS, REPORT_REQUEST
from test_services_submit import CONTRACT, REF, RULE, FixedSource, SyntheticCalculator

from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.models import Base
from app.models.calculation_result import CalculationResultRow
from app.reporting.title_block import (
    FORM5_COLUMNS,
    FORM6_COLUMNS,
    SIGNATURE_COLUMNS,
    SIGNATURE_ROWS,
)
from app.schemas.calculation import MethodBound, ValidatedBound
from app.schemas.report import MAX_LENGTH

INPUTS: dict[str, Any] = {
    "b": {"value": 1.5, "unit": "m"},
    "d": {"value": 2.0, "unit": "m"},
    "p": {"value": 200.0, "unit": "kPa"},
}


def body(**inputs: Any) -> dict[str, Any]:
    given = {name: value for name, value in (INPUTS | inputs).items() if value is not None}
    return {"calculation_type": "synthetic", "inputs": given}


@pytest.fixture
def engine() -> Iterator[Engine]:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def make_app(
    engine: Engine,
    source: FixedSource | None = None,
    validated_range: tuple[ValidatedBound, ...] = (),
    session_class: type[Session] = Session,
) -> FastAPI:
    registry = CalculatorRegistry()
    registry.register(CONTRACT, SyntheticCalculator())
    return create_app(
        registry=registry,
        sources={} if source is None else {"synthetic": source},
        validated_ranges={"synthetic": validated_range},
        session_factory=sessionmaker(bind=engine, class_=session_class),
    )


@pytest.fixture
def client(engine: Engine, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    with TestClient(make_app(engine, FixedSource()), raise_server_exceptions=False) as client:
        yield client


def stored(engine: Engine) -> int:
    with Session(engine) as session:
        return session.scalar(select(func.count()).select_from(CalculationResultRow)) or 0


def test_a_completed_calculation_answers_201_with_location_and_is_stored(
    client: TestClient, engine: Engine, engine_calls: list[str]
) -> None:
    response = client.post("/calculations", json=body())

    envelope = response.json()
    assert response.status_code == 201
    assert response.headers["location"] == f"/calculations/{envelope['result_id']}"
    assert envelope["verdict"] == "pass"
    assert engine_calls == ["synthetic"]
    with Session(engine) as session:
        row = session.get(CalculationResultRow, uuid.UUID(envelope["result_id"]))
        assert row is not None and row.envelope == envelope


def test_a_refused_calculation_is_201_names_the_bound_and_is_stored(engine: Engine) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    with TestClient(make_app(engine, FixedSource(method_range=(bound,)))) as client:
        response = client.post("/calculations", json=body())

    envelope = response.json()
    assert response.status_code == 201
    assert envelope["verdict"] == "refused"
    assert envelope["verdict_reason"]["bound"]["quantity"] == "b"
    assert stored(engine) == 1


def test_two_posts_of_one_request_differ_only_in_result_id(client: TestClient) -> None:
    first = client.post("/calculations", json=body()).json()
    second = client.post("/calculations", json=body()).json()

    assert first["result_id"] != second["result_id"]
    assert first["input_hash"] == second["input_hash"]
    assert {**first, "result_id": None} == {**second, "result_id": None}


@pytest.mark.parametrize(
    "data",
    [
        {"inputs": INPUTS},
        {"calculation_type": 7, "inputs": INPUTS},
        body() | {"comment": "extra"},
        body(b={"value": "one and a half", "unit": "m"}),
        body(b={"value": 1.5, "unit": "furlong"}),
        body() | {"parameters": {"k": 1.0}},
        body() | {"formulas": ["R = 2 b"], "rounding_rules": {"y": {"decimals": 2}}},
        body(b={"value": 1.5, "unit": "m", "bound": 3.0}),
    ],
    ids=[
        "missing-field",
        "wrong-type",
        "unknown-field",
        "value-not-a-number",
        "unit-outside-vocabulary",
        "client-parameters",
        "client-formulas-and-rounding",
        "client-bound-on-input",
    ],
)
def test_a_malformed_request_is_422_validation_error_and_nothing_runs(
    client: TestClient, engine: Engine, engine_calls: list[str], data: dict[str, Any]
) -> None:
    response = client.post("/calculations", json=data)

    assert (response.status_code, response.json()["code"]) == (422, "validation_error")
    assert response.json()["fields"]
    assert (engine_calls, stored(engine)) == ([], 0)


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_a_non_finite_number_is_422_validation_error(
    client: TestClient, engine: Engine, engine_calls: list[str], token: str
) -> None:
    raw = json.dumps(body()).replace("1.5", token)

    response = client.post("/calculations", content=raw, headers={"content-type": "application/json"})

    assert (response.status_code, response.json()["code"]) == (422, "validation_error")
    assert (engine_calls, stored(engine)) == ([], 0)


def test_an_unknown_calculation_type_is_404_and_nothing_is_stored(
    client: TestClient, engine: Engine, engine_calls: list[str]
) -> None:
    response = client.post("/calculations", json=body() | {"calculation_type": "missing"})

    assert (response.status_code, response.json()["code"]) == (404, "not_found")
    assert (engine_calls, stored(engine)) == ([], 0)


def test_inputs_that_do_not_fit_are_422_invalid_input_with_one_field_each(
    client: TestClient, engine: Engine, engine_calls: list[str]
) -> None:
    data = body(d=None, z={"value": 1.0, "unit": "m"}, p={"value": 1.0, "unit": "m"})

    response = client.post("/calculations", json=data)

    payload = response.json()
    assert (response.status_code, payload["code"]) == (422, "invalid_input")
    assert [field["location"] for field in payload["fields"]] == [
        ["body", "inputs", "d"],
        ["body", "inputs", "p"],
        ["body", "inputs", "z"],
    ]
    assert (engine_calls, stored(engine)) == ([], 0)


def test_a_type_without_a_source_is_503_naming_the_type(
    engine: Engine, engine_calls: list[str]
) -> None:
    with TestClient(make_app(engine)) as client:
        response = client.post("/calculations", json=body())

    payload = response.json()
    assert (response.status_code, payload["code"]) == (503, "parameter_source_unavailable")
    assert "'synthetic'" in payload["message"]
    assert (engine_calls, stored(engine)) == ([], 0)


def test_the_engine_gets_the_yaml_range_and_the_source_parameters(engine: Engine) -> None:
    source = FixedSource()
    bound = ValidatedBound(quantity="b", kind="max", value=1.0, inclusive=True, source=RULE)

    with TestClient(make_app(engine, source, validated_range=(bound,))) as client:
        response = client.post("/calculations", json=body())

    envelope = response.json()
    assert response.status_code == 201
    assert [warning["bound"]["value"] for warning in envelope["warnings"]] == [1.0]
    assert envelope["trace"][0]["expression"] == "y = 2 b"
    assert [call[0] for call in source.calls] == ["synthetic"]


def test_a_failed_commit_is_not_answered_201(engine: Engine) -> None:
    class FailingCommit(Session):
        def commit(self) -> None:
            raise OperationalError("COMMIT", {}, Exception("connection lost"))

    with TestClient(make_app(engine, FixedSource(), session_class=FailingCommit)) as client:
        response = client.post("/calculations", json=body())

    assert (response.status_code, response.json()["code"]) == (503, "database_unavailable")
    assert stored(engine) == 0


def test_every_unit_the_listing_offers_passes_the_unit_check(client: TestClient) -> None:
    listing = client.get("/calculation-types").json()
    (synthetic,) = listing

    for item in synthetic["inputs"]:
        for unit in item["units"]:
            value = {"value": INPUTS[item["name"]]["value"], "unit": unit}
            response = client.post("/calculations", json=body(**{item["name"]: value}))
            assert response.status_code == 201, (item["name"], unit, response.json())


def test_get_returns_the_body_that_post_returned(client: TestClient) -> None:
    created = client.post("/calculations", json=body(b={"value": 1500.0, "unit": "mm"}))

    response = client.get(created.headers["location"])

    assert response.status_code == 200
    assert response.json() == created.json()


def test_get_returns_a_refused_result_unchanged(engine: Engine) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    with TestClient(make_app(engine, FixedSource(method_range=(bound,)))) as client:
        created = client.post("/calculations", json=body())
        response = client.get(created.headers["location"])

    assert response.json() == created.json()
    assert response.json()["verdict"] == "refused"


def test_an_unknown_result_id_is_404(client: TestClient) -> None:
    response = client.get(f"/calculations/{uuid.uuid4()}")

    assert (response.status_code, response.json()["code"]) == (404, "not_found")


def test_a_result_id_that_is_not_a_uuid_is_422(client: TestClient) -> None:
    response = client.get("/calculations/abc")

    payload = response.json()
    assert (response.status_code, payload["code"]) == (422, "validation_error")
    assert [field["location"] for field in payload["fields"]] == [["path", "result_id"]]


@pytest.mark.parametrize("method", ["PUT", "PATCH", "DELETE"])
def test_a_stored_result_cannot_be_changed_or_deleted(
    client: TestClient, engine: Engine, method: str
) -> None:
    created = client.post("/calculations", json=body())
    location = created.headers["location"]

    response = client.request(method, location, json=body(b={"value": 9.0, "unit": "m"}))

    assert (response.status_code, response.json()["code"]) == (405, "method_not_allowed")
    assert client.get(location).json() == created.json()
    assert stored(engine) == 1


DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
REPORT_BODY = REPORT_REQUEST.model_dump(mode="json")


def test_the_report_is_a_docx_attachment_of_the_stored_result(client: TestClient) -> None:
    created = client.post("/calculations", json=body(b={"value": 1500.0, "unit": "mm"})).json()

    response = client.post(f"/calculations/{created['result_id']}/report", json=REPORT_BODY)

    assert response.status_code == 200
    assert response.headers["content-type"] == DOCX
    assert response.headers["content-disposition"] == (
        f'attachment; filename="dec-report-{created["result_id"]}.docx"'
    )
    paragraphs, rows = read_back(response.content)
    assert [text for text in paragraphs if text in HEADINGS] == HEADINGS
    assert ["b", "1500 мм"] in rows
    assert any(created["result_id"] in text for text in paragraphs)


def test_the_report_of_a_refused_result_names_the_bound(engine: Engine) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    with TestClient(make_app(engine, FixedSource(method_range=(bound,)))) as client:
        created = client.post("/calculations", json=body()).json()
        response = client.post(f"/calculations/{created['result_id']}/report", json=REPORT_BODY)

    paragraphs, _ = read_back(response.content)
    start = paragraphs.index("3 Заключение") + 1
    assert response.status_code == 200
    assert any("b" in text and "1 м" in text for text in paragraphs[start:])


@pytest.mark.parametrize(
    "report",
    [
        REPORT_BODY | {"developer": None},
        REPORT_BODY | {"developer": {"surname": "", "date": "2026-10-03"}},
        REPORT_BODY | {"title": {"designation": "<D>"}},
        REPORT_BODY | {"extra": True},
    ],
    ids=["no-developer", "empty-surname", "incomplete-title", "unknown-field"],
)
def test_an_invalid_report_request_is_422_and_no_document(
    client: TestClient, report: dict[str, Any]
) -> None:
    created = client.post("/calculations", json=body()).json()

    response = client.post(f"/calculations/{created['result_id']}/report", json=report)

    assert (response.status_code, response.json()["code"]) == (422, "validation_error")
    assert response.headers["content-type"] == "application/json"


def test_the_report_of_an_unknown_result_is_404(client: TestClient) -> None:
    response = client.post(f"/calculations/{uuid.uuid4()}/report", json=REPORT_BODY)

    assert (response.status_code, response.json()["code"]) == (404, "not_found")


def test_the_report_of_a_result_whose_type_is_gone_is_409(engine: Engine) -> None:
    with TestClient(make_app(engine, FixedSource())) as client:
        created = client.post("/calculations", json=body()).json()
    without_type = create_app(
        registry=CalculatorRegistry(), session_factory=sessionmaker(bind=engine)
    )

    with TestClient(without_type) as client:
        response = client.post(f"/calculations/{created['result_id']}/report", json=REPORT_BODY)
        unchanged = client.get(f"/calculations/{created['result_id']}")

    payload = response.json()
    assert (response.status_code, payload["code"]) == (409, "calculation_type_not_registered")
    assert "'synthetic'" in payload["message"]
    assert unchanged.json() == created


SENTINEL = "client-value-7f3a"


@pytest.mark.parametrize(
    "data",
    [
        body(b={"value": SENTINEL, "unit": "m"}),
        body(b={"value": 1.5, "unit": SENTINEL}),
        body() | {SENTINEL: SENTINEL},
        body(b={"value": 1.5, "unit": "m", "note": SENTINEL}),
    ],
    ids=["value", "unit", "unknown-field", "extra-input-field"],
)
def test_a_422_on_the_real_route_echoes_no_client_value(
    client: TestClient, caplog: pytest.LogCaptureFixture, data: dict[str, Any]
) -> None:
    with caplog.at_level(logging.INFO, logger="app.api"):
        response = client.post("/calculations", json=data)

    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert response.status_code == 422
    for field in response.json()["fields"]:
        assert SENTINEL not in field["message"]
    assert SENTINEL not in response.json()["message"]
    assert SENTINEL not in logged and "code=validation_error" in logged


@pytest.mark.parametrize("character", [chr(0xFFFE), chr(0xFFFF)], ids=["fffe", "ffff"])
def test_a_report_request_with_a_character_xml_does_not_allow_is_422(
    client: TestClient, character: str
) -> None:
    created = client.post("/calculations", json=body()).json()
    report = REPORT_BODY | {"title": REPORT_BODY["title"] | {"designation": f"ПР-{character}"}}

    response = client.post(f"/calculations/{created['result_id']}/report", json=report)

    assert (response.status_code, response.json()["code"]) == (422, "validation_error")
    assert [field["location"] for field in response.json()["fields"]] == [["body", "title", "designation"]]


LIMITED_FIELDS = [
    (("title", "designation"), "1"),
    (("title", "document_name"), "5"),
    (("title", "documentation_kind"), "6"),
    (("title", "organization"), "9"),
    (("developer", "surname"), "11"),
    (("checker", "surname"), "11"),
    (("normative_control", "surname"), "11"),
]


def report_with(path: tuple[str, str], text: str) -> dict[str, Any]:
    group, field = path
    signatory = {"surname": "<SURNAME>", "date": "2026-10-07"}
    current = REPORT_BODY.get(group) or signatory
    return REPORT_BODY | {group: current | {field: text}}


@pytest.mark.parametrize(("path", "column"), LIMITED_FIELDS, ids=[".".join(path) for path, _ in LIMITED_FIELDS])
def test_a_report_text_over_its_limit_is_422_naming_the_limit_and_echoing_no_text(
    client: TestClient, caplog: pytest.LogCaptureFixture, path: tuple[str, str], column: str
) -> None:
    created = client.post("/calculations", json=body()).json()
    text = "Щ" * (MAX_LENGTH[column] + 1)

    with caplog.at_level(logging.INFO, logger="app.api"):
        response = client.post(f"/calculations/{created['result_id']}/report", json=report_with(path, text))

    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert (response.status_code, response.json()["code"]) == (422, "validation_error")
    assert response.json()["fields"] == [
        {"location": ["body", *path], "message": f"String should have at most {MAX_LENGTH[column]} characters"}
    ]
    assert text not in response.text and text not in logged
    assert "code=validation_error" in logged


def test_a_report_with_every_text_at_its_limit_prints_each_text_whole(client: TestClient) -> None:
    created = client.post("/calculations", json=body()).json()
    sent = {path: f"{path[0][:3]}-" + "ж" * (MAX_LENGTH[column] - 4) for path, column in LIMITED_FIELDS}
    report: dict[str, Any] = {"title": REPORT_BODY["title"], "signature_block": True}
    for (group, field), text in sent.items():
        defaults = {} if group == "title" else {"date": "2026-10-07"}
        report[group] = defaults | report.get(group, {}) | {field: text}

    response = client.post(f"/calculations/{created['result_id']}/report", json=report)

    assert response.status_code == 200
    footers = Document(BytesIO(response.content)).sections[0]
    form5, form6 = footers.first_page_footer.tables[0], footers.footer.tables[0]
    printed = {
        ("title", "designation"): form5.cell(*FORM5_COLUMNS["1"]).text,
        ("title", "document_name"): form5.cell(*FORM5_COLUMNS["5"]).text,
        ("title", "documentation_kind"): form5.cell(*FORM5_COLUMNS["6"]).text,
        ("title", "organization"): form5.cell(*FORM5_COLUMNS["9"]).text,
        **{
            (role, "surname"): form5.cell(SIGNATURE_ROWS[role], SIGNATURE_COLUMNS["11"]).text
            for role in ("developer", "checker", "normative_control")
        },
    }
    assert printed == sent
    assert [len(sent[path]) for path, _ in LIMITED_FIELDS] == [MAX_LENGTH[column] for _, column in LIMITED_FIELDS]
    assert form6.cell(*FORM6_COLUMNS["1"]).text == sent[("title", "designation")]
