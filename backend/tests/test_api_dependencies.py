import logging
from collections.abc import Iterator
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_session
from app.main import create_app

CLOSED = "postgresql://user:hunter2@127.0.0.1:1/dec_app"


def make_app(session_factory: sessionmaker[Session] | None = None) -> FastAPI:
    app = create_app(session_factory=session_factory)

    @app.get("/needs-database")
    def needs_database(session: Annotated[Session, Depends(get_session)]) -> dict[str, int]:
        return {"one": session.execute(text("SELECT 1")).scalar_one()}

    return app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    with TestClient(make_app(), raise_server_exceptions=False) as client:
        yield client


def test_a_missing_database_url_answers_503(client: TestClient) -> None:
    response = client.get("/needs-database")

    assert (response.status_code, response.json()["code"]) == (503, "database_unavailable")


@pytest.mark.parametrize("url", [CLOSED, "not a url"])
def test_an_unusable_database_answers_503_without_the_url(
    url: str, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv("DEC_APP_DATABASE_URL", url)

    with caplog.at_level(logging.INFO, logger="app.api"), TestClient(make_app(), raise_server_exceptions=False) as client:
        response = client.get("/needs-database")

    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert (response.status_code, response.json()["code"]) == (503, "database_unavailable")
    assert "hunter2" not in response.text and "127.0.0.1" not in response.text
    assert "hunter2" not in logged and "127.0.0.1" not in logged and "code=database_unavailable" in logged


def test_a_route_without_the_database_answers_without_the_url(client: TestClient) -> None:
    assert client.get("/health").status_code == 200


def test_a_given_session_factory_is_used_and_committed() -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    with TestClient(make_app(sessionmaker(bind=engine))) as client:
        response = client.get("/needs-database")

    assert response.json() == {"one": 1}


def test_the_factory_is_built_once(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEC_APP_DATABASE_URL", CLOSED)
    app = make_app()

    with TestClient(app, raise_server_exceptions=False) as client:
        client.get("/needs-database")
        first = app.state.session_factory
        client.get("/needs-database")

    assert first is not None and app.state.session_factory is first
