import threading
import time
from collections.abc import Iterator
from typing import Any
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.db.catalog as catalog_module
from app.core.exceptions import CatalogUnavailableError
from app.db.catalog import READ_ONLY_OPTIONS, CatalogSessions, get_catalog_engine
from app.engine.registry import CalculatorRegistry
from app.main import create_app

URL = "postgresql://dec_normatives_reader:hunter2@127.0.0.1:1/dec"  # pragma: allowlist secret


@pytest.fixture
def built(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[Engine]]:
    """Движки, которые построил ``CatalogSessions``; вместо PostgreSQL — SQLite в памяти."""
    engines: list[Engine] = []

    def fake(url: str) -> Engine:
        time.sleep(0.05)
        engine = create_engine("sqlite://", poolclass=StaticPool)
        engines.append(engine)
        return engine

    monkeypatch.setenv("DEC_NORMATIVES_DATABASE_URL", URL)
    monkeypatch.setattr(catalog_module, "get_catalog_engine", fake)
    yield engines
    for engine in engines:
        engine.dispose()


def test_the_engine_reads_only_and_hides_parameters(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []
    real = catalog_module.create_engine

    def spy(url: Any, **kwargs: Any) -> Engine:
        calls.append({"url": url, **kwargs})
        return real(url, **kwargs)

    monkeypatch.setattr(catalog_module, "create_engine", spy)

    engine = get_catalog_engine(URL)

    (call,) = calls
    assert call["url"].drivername == "postgresql+psycopg"
    assert call["connect_args"] == {"options": READ_ONLY_OPTIONS}
    assert READ_ONLY_OPTIONS == "-c default_transaction_read_only=on"
    assert call["isolation_level"] == "REPEATABLE READ"
    assert call["hide_parameters"] is True and call["pool_pre_ping"] is True
    assert engine.hide_parameters is True
    engine.dispose()


def test_an_unset_variable_raises_without_a_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)

    with pytest.raises(CatalogUnavailableError) as exc_info:
        CatalogSessions().factory()

    assert str(exc_info.value) == "the normative catalog is not configured"


@pytest.mark.parametrize("url", ["not a url", "postgresql://dec_normatives_reader:hunter2@127.0.0.1:port/dec"])  # pragma: allowlist secret
def test_an_unparsable_url_raises_without_the_url(url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEC_NORMATIVES_DATABASE_URL", url)

    with pytest.raises(CatalogUnavailableError) as exc_info:
        CatalogSessions().factory()

    assert str(exc_info.value) == "the normative catalog is not configured"
    assert exc_info.value.__cause__ is None and exc_info.value.__suppress_context__


def test_a_failure_is_not_remembered(monkeypatch: pytest.MonkeyPatch, built: list[Engine]) -> None:
    sessions = CatalogSessions()
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL")
    with pytest.raises(CatalogUnavailableError):
        sessions.factory()

    monkeypatch.setenv("DEC_NORMATIVES_DATABASE_URL", URL)

    assert sessions.factory().kw["bind"] is built[0]


def test_nothing_is_built_before_the_first_use(built: list[Engine]) -> None:
    with TestClient(create_app(registry=CalculatorRegistry())) as client:
        assert client.get("/health").status_code == 200

    assert built == []


def test_two_concurrent_first_uses_build_one_engine(built: list[Engine]) -> None:
    sessions = CatalogSessions()
    barrier = threading.Barrier(2)
    factories: list[sessionmaker[Any]] = []

    def first_use() -> None:
        barrier.wait()
        factories.append(sessions.factory())

    threads = [threading.Thread(target=first_use) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(built) == 1
    assert factories[0] is factories[1] and factories[0].kw["bind"] is built[0]


def test_shutdown_disposes_the_engine_the_application_built(
    monkeypatch: pytest.MonkeyPatch, built: list[Engine]
) -> None:
    app = create_app(registry=CalculatorRegistry())
    disposed: list[Engine] = []

    with TestClient(app):
        app.state.catalog.factory()
        engine = built[0]
        real = engine.dispose

        def dispose() -> None:
            disposed.append(engine)
            real()

        monkeypatch.setattr(engine, "dispose", dispose)

    assert disposed == [engine]


def test_shutdown_leaves_a_given_factory_alone(built: list[Engine]) -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    given = sessionmaker(bind=engine)
    app = create_app(registry=CalculatorRegistry(), catalog_session_factory=given)

    with mock.patch.object(engine, "dispose") as dispose, TestClient(app):
        assert app.state.catalog.factory() is given

    dispose.assert_not_called()
    assert built == []
    engine.dispose()


def test_a_disposed_factory_is_built_again(built: list[Engine]) -> None:
    sessions = CatalogSessions()
    first = sessions.factory()

    sessions.dispose()
    sessions.dispose()

    assert sessions.factory() is not first and len(built) == 2
