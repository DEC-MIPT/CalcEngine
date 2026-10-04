import logging
from collections.abc import Iterator
from typing import Any

import pytest
from catalog_fixture import PILOT
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, func, select, text
from sqlalchemy.exc import InterfaceError, ProgrammingError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import inputs
from test_services_catalog_source import make_source, registry

from app.core.exceptions import ParameterSourceUnavailableError
from app.db.catalog import CatalogSessions
from app.main import create_app
from app.models import Base
from app.models.calculation_result import CalculationResultRow
from app.repositories.normatives import NormativesRepository
from app.services.catalog_source import CatalogParameterSource

CLOSED = "postgresql://dec_normatives_reader:hunter2@127.0.0.1:1/dec"
MESSAGE = f"The normative catalog is not available for the calculation type '{PILOT}'."
LINE = f"code=catalog_unavailable type={PILOT}"


def source_lines(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.name == "app.services.catalog_source"]


@pytest.fixture
def results() -> Iterator[Engine]:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def post(results: Engine, sessions: CatalogSessions) -> Any:
    app = create_app(
        registry=registry(),
        sources={PILOT: CatalogParameterSource(sessions, registry())},
        validated_ranges={PILOT: ()},
        session_factory=sessionmaker(bind=results),
    )
    given = {name: value.model_dump() for name, value in inputs().items()}
    with TestClient(app, raise_server_exceptions=False) as client:
        return client.post("/calculations", json={"calculation_type": PILOT, "inputs": given})


def stored(results: Engine) -> int:
    with Session(results) as session:
        return session.scalar(select(func.count()).select_from(CalculationResultRow)) or 0


@pytest.mark.parametrize("url", [None, CLOSED], ids=["no variable", "closed port"])
def test_an_unusable_catalog_answers_503_without_the_url(
    results: Engine, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture, url: str | None
) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    if url is None:
        monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)
    else:
        monkeypatch.setenv("DEC_NORMATIVES_DATABASE_URL", url)
    sessions = CatalogSessions()

    with caplog.at_level(logging.INFO):
        response = post(results, sessions)
    sessions.dispose()

    body = response.json()
    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert (response.status_code, body["code"], body["message"]) == (503, "parameter_source_unavailable", MESSAGE)
    assert source_lines(caplog) == [LINE]
    for secret in ("hunter2", "127.0.0.1", "dec_normatives_reader"):
        assert secret not in response.text and secret not in logged
    assert stored(results) == 0


def test_a_missing_view_makes_the_catalog_unavailable(catalog_sqlite: Engine, caplog: pytest.LogCaptureFixture) -> None:
    with catalog_sqlite.begin() as connection:
        connection.execute(text("DROP TABLE catalog_read.type_checks"))

    with caplog.at_level(logging.INFO), pytest.raises(ParameterSourceUnavailableError) as exc_info:
        make_source(catalog_sqlite).resolve(PILOT, inputs())

    assert str(exc_info.value) == MESSAGE
    assert exc_info.value.__cause__ is None and exc_info.value.__suppress_context__
    assert source_lines(caplog) == [LINE]


@pytest.mark.parametrize("error", [ProgrammingError, InterfaceError])
def test_a_driver_error_on_the_contract_makes_the_catalog_unavailable(
    catalog_sqlite: Engine, monkeypatch: pytest.MonkeyPatch, error: type[Exception]
) -> None:
    def refuse(self: NormativesRepository, calculation_type: str) -> Any:
        raise error("SELECT 1", {}, Exception(CLOSED))

    monkeypatch.setattr(NormativesRepository, "thresholds", refuse)

    with pytest.raises(ParameterSourceUnavailableError) as exc_info:
        make_source(catalog_sqlite).resolve(PILOT, inputs())

    assert str(exc_info.value) == MESSAGE and "hunter2" not in str(exc_info.value)
    assert exc_info.value.__suppress_context__
