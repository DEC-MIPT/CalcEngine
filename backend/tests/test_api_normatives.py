import logging
import sqlite3
from collections.abc import Iterator
from typing import Any

import pytest
from catalog_fixture import (
    PILOT,
    PLACEHOLDER_CLAUSES,
    PLACEHOLDER_DOCUMENTS,
    load_sqlite,
)
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import inputs
from test_services_catalog_source import registry

from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.models import Base
from app.repositories.normatives import NormativesRepository
from app.schemas.normatives import SearchHit

CLOSED = "postgresql://dec_normatives_reader:hunter2@127.0.0.1:1/dec"
UNAVAILABLE = {"code": "catalog_unavailable", "message": "The normative catalog is not available."}

HITS = tuple(
    SearchHit.model_validate(
        {
            "kind": kind,
            "document_id": document,
            "designation": PLACEHOLDER_DOCUMENTS[document - 1],
            "edition": "unverified",
            "number": number,
            "title": None,
        }
    )
    for kind, document, number in (
        ("document", 2, None),
        ("clause", 1, PLACEHOLDER_CLAUSES[1]),
        ("clause", 1, PLACEHOLDER_CLAUSES[2]),
    )
)
"""Совпадения в порядке ранга, как их отдала бы функция каталога."""


def app_lines(caplog: pytest.LogCaptureFixture) -> str:
    """Строки логов приложения; ``httpx`` в ``TestClient`` пишет URL запроса сам."""
    return "\n".join(record.getMessage() for record in caplog.records if record.name.startswith("app"))


@pytest.fixture(autouse=True)
def no_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)


@pytest.fixture
def searched(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, int]]:
    """Аргументы каждого вызова поиска репозитория; SQLite не выполняет функцию ``search``."""
    calls: list[tuple[str, int]] = []

    def search(self: NormativesRepository, query: str, max_rows: int) -> tuple[SearchHit, ...]:
        calls.append((query, max_rows))
        return HITS[:max_rows] if query != "ничего" else ()

    monkeypatch.setattr(NormativesRepository, "search", search)
    return calls


@pytest.fixture
def client(catalog_sqlite: Engine) -> Iterator[TestClient]:
    app = create_app(registry=CalculatorRegistry(), catalog_session_factory=sessionmaker(bind=catalog_sqlite))
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def hits(response: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = response.json()["hits"]
    return found


def test_the_search_answers_the_ranked_hits_with_20_by_default(
    client: TestClient, searched: list[tuple[str, int]]
) -> None:
    response = client.get("/normatives/search", params={"q": "Синтетический"})

    assert response.status_code == 200
    assert hits(response) == [hit.model_dump() for hit in HITS]
    assert searched == [("Синтетический", 20)]


def test_the_search_is_capped_by_limit(client: TestClient, searched: list[tuple[str, int]]) -> None:
    response = client.get("/normatives/search", params={"q": "Синтетический", "limit": 2})

    assert hits(response) == [hit.model_dump() for hit in HITS[:2]]
    assert searched == [("Синтетический", 2)]


@pytest.mark.parametrize(
    ("given", "sent"),
    [
        ("грунтах", "грунтах"),
        ("  пункт о грунтах\t", "пункт о грунтах"),
        ("x'); DROP TABLE catalog_read.documents; --", "x'); DROP TABLE catalog_read.documents; --"),
    ],
    ids=["russian", "trimmed", "sql"],
)
def test_the_query_reaches_the_repository_as_written(
    client: TestClient, searched: list[tuple[str, int]], caplog: pytest.LogCaptureFixture, given: str, sent: str
) -> None:
    with caplog.at_level(logging.INFO):
        response = client.get("/normatives/search", params={"q": given})

    assert response.status_code == 200
    assert searched == [(sent, 20)]
    assert sent not in app_lines(caplog)


def test_a_search_without_matches_answers_no_hits(client: TestClient, searched: list[tuple[str, int]]) -> None:
    response = client.get("/normatives/search", params={"q": "ничего"})

    assert (response.status_code, response.json()) == (200, {"hits": []})


@pytest.mark.parametrize(
    ("params", "parameter", "value"),
    [
        ({}, "q", None),
        ({"q": "Ж"}, "q", "Ж"),
        ({"q": " Ж "}, "q", "Ж"),
        ({"q": "   "}, "q", None),
        ({"q": "Щ" * 201}, "q", "ЩЩ"),
        ({"q": "грунт", "limit": 0}, "limit", None),
        ({"q": "грунт", "limit": 51}, "limit", "51"),
        ({"q": "грунт", "limit": "семь"}, "limit", "семь"),
    ],
    ids=["missing", "short", "short-trimmed", "blank", "long", "limit-0", "limit-51", "limit-text"],
)
def test_a_query_outside_its_limits_answers_422_without_the_value(
    client: TestClient,
    searched: list[tuple[str, int]],
    caplog: pytest.LogCaptureFixture,
    params: dict[str, Any],
    parameter: str,
    value: str | None,
) -> None:
    with caplog.at_level(logging.INFO):
        response = client.get("/normatives/search", params=params)

    body = response.json()
    assert (response.status_code, body["code"]) == (422, "validation_error")
    assert [field["location"] for field in body["fields"]] == [["query", parameter]]
    if value is not None:
        assert value not in response.text
        assert value not in app_lines(caplog)
    assert searched == []


def test_a_document_has_its_clauses_in_document_order(client: TestClient) -> None:
    response = client.get("/normatives/documents/1")

    assert response.status_code == 200
    assert response.json() == {
        "document_id": 1,
        "designation": PLACEHOLDER_DOCUMENTS[0],
        "title": "Синтетический документ об основаниях",
        "edition": "unverified",
        "year": None,
        "source_url": None,
        "clauses": [
            {"number": PLACEHOLDER_CLAUSES[1], "title": "Синтетический пункт об основаниях", "page": 1},
            {"number": PLACEHOLDER_CLAUSES[2], "title": "Синтетический пункт о фундаментах", "page": 2},
            {"number": PLACEHOLDER_CLAUSES[3], "title": None, "page": None},
        ],
    }


def test_an_unknown_document_answers_404(client: TestClient) -> None:
    response = client.get("/normatives/documents/99")

    assert (response.status_code, response.json()["code"]) == (404, "not_found")


@pytest.mark.parametrize(
    ("given", "message"),
    [
        ("0", "Input should be greater than 0"),
        ("-37", "Input should be greater than 0"),
        ("abc", "Input should be a valid integer, unable to parse string as an integer"),
        ("1.5", "Input should be a valid integer, unable to parse string as an integer"),
    ],
)
def test_an_invalid_document_id_answers_422_without_the_value(client: TestClient, given: str, message: str) -> None:
    response = client.get(f"/normatives/documents/{given}")

    body = response.json()
    assert (response.status_code, body["code"]) == (422, "validation_error")
    assert body["fields"] == [{"location": ["path", "document_id"], "message": message}]


@pytest.mark.parametrize(
    ("url", "path"),
    [
        (None, "/normatives/search?q=грунт"),
        (None, "/normatives/documents/1"),
        (CLOSED, "/normatives/search?q=грунт"),
        (CLOSED, "/normatives/documents/1"),
    ],
    ids=["search-no-variable", "document-no-variable", "search-closed-port", "document-closed-port"],
)
def test_an_unusable_catalog_answers_503_without_the_url(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture, url: str | None, path: str
) -> None:
    if url is not None:
        monkeypatch.setenv("DEC_NORMATIVES_DATABASE_URL", url)
    app = create_app(registry=CalculatorRegistry())

    with caplog.at_level(logging.INFO), TestClient(app, raise_server_exceptions=False) as test_client:
        response = test_client.get(path)

    logged = app_lines(caplog)
    assert (response.status_code, response.json()) == (503, UNAVAILABLE)
    assert "code=catalog_unavailable" in logged
    for secret in ("hunter2", "127.0.0.1", "dec_normatives_reader"):
        assert secret not in response.text and secret not in logged


def test_the_application_starts_without_the_catalog_and_serves_it_once_it_is_back() -> None:
    down = True

    def connect() -> sqlite3.Connection:
        if down:
            raise sqlite3.OperationalError("unable to open database file")
        return sqlite3.connect(":memory:", check_same_thread=False)

    catalog = create_engine("sqlite://", creator=connect, poolclass=StaticPool)
    results = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(results)
    app = create_app(
        registry=registry(),
        validated_ranges={PILOT: ()},
        session_factory=sessionmaker(bind=results),
        catalog_session_factory=sessionmaker(bind=catalog),
    )
    calculation = {"calculation_type": PILOT, "inputs": {name: value.model_dump() for name, value in inputs().items()}}

    with TestClient(app, raise_server_exceptions=False) as test_client:
        health = test_client.get("/health")
        types = test_client.get("/calculation-types")
        document_down = test_client.get("/normatives/documents/1")
        calculation_down = test_client.post("/calculations", json=calculation)
        down = False
        load_sqlite(catalog)
        document_back = test_client.get("/normatives/documents/1")
        calculation_back = test_client.post("/calculations", json=calculation)

    catalog.dispose()
    results.dispose()
    assert (health.status_code, types.status_code) == (200, 200)
    assert (document_down.status_code, document_down.json()) == (503, UNAVAILABLE)
    assert (calculation_down.status_code, calculation_down.json()["code"]) == (503, "parameter_source_unavailable")
    assert (document_back.status_code, document_back.json()["document_id"]) == (200, 1)
    assert calculation_back.status_code == 201


def test_the_real_application_starts_without_the_catalog_variable() -> None:
    with TestClient(create_app(), raise_server_exceptions=False) as test_client:
        health = test_client.get("/health")
        types = test_client.get("/calculation-types")
        search = test_client.get("/normatives/search", params={"q": "грунт"})

    assert (health.status_code, types.status_code) == (200, 200)
    assert (search.status_code, search.json()["code"]) == (503, "catalog_unavailable")
