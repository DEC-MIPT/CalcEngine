import asyncio
import logging
import threading
import time
import uuid
from collections.abc import Iterator
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.types import Message, Receive, Scope, Send
from test_api_calculations import body, make_app
from test_services_submit import FixedSource

from app.api import dependencies
from app.api.errors import UnexpectedErrors
from app.core.config import ApiSettings, Settings
from app.db.session import get_engine
from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.models import Base

SENTINEL = "client-value-5d1e"
ORIGIN = "http://localhost:5173"
CLOSED = "postgresql://user:hunter2@127.0.0.1:1/dec_app"


@pytest.fixture(autouse=True)
def no_database_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)


@pytest.fixture
def engine() -> Iterator[Engine]:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def logged(caplog: pytest.LogCaptureFixture) -> str:
    return "\n".join(record.getMessage() for record in caplog.records)


def test_an_unexpected_error_is_answered_and_not_raised_further(caplog: pytest.LogCaptureFixture) -> None:
    application = create_app(
        ApiSettings.model_validate({"DEC_CORS_ORIGINS": ORIGIN}), registry=CalculatorRegistry()
    )

    @application.get("/boom")
    def boom() -> None:
        raise RuntimeError(f"[SQL: INSERT INTO t] [parameters: {SENTINEL}]")

    with caplog.at_level(logging.DEBUG), TestClient(application, raise_server_exceptions=True) as client:
        response = client.get("/boom", headers={"Origin": ORIGIN})

    assert (response.status_code, response.json()["code"]) == (500, "internal_error")
    assert response.headers["access-control-allow-origin"] == ORIGIN
    assert SENTINEL not in response.text and SENTINEL not in logged(caplog)
    assert "error=RuntimeError" in logged(caplog) and "code=internal_error route=/boom" in logged(caplog)


def test_a_statement_error_with_client_inputs_does_not_reach_the_log(
    engine: Engine, caplog: pytest.LogCaptureFixture
) -> None:
    class FailingSource(FixedSource):
        def resolve(self, calculation_type: str, inputs: Any) -> Any:
            raise StatementError("failed", "INSERT INTO t VALUES (:b)", {"b": SENTINEL}, Exception("x"))

    application = make_app(engine, FailingSource())

    with caplog.at_level(logging.DEBUG), TestClient(application, raise_server_exceptions=True) as client:
        response = client.post("/calculations", json=body())

    assert (response.status_code, response.json()["code"]) == (500, "internal_error")
    assert SENTINEL not in logged(caplog)


def run_boundary(inner: Any, scope_type: str = "http") -> list[Message]:
    sent: list[Message] = []

    async def receive() -> Message:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    scope: Scope = {"type": scope_type, "method": "GET", "path": "/", "headers": [], "query_string": b""}
    asyncio.run(UnexpectedErrors(inner)(scope, receive, send))
    return sent


def test_an_error_after_the_response_started_is_swallowed_without_a_second_response() -> None:
    async def inner(scope: Scope, receive: Receive, send: Send) -> None:
        await send({"type": "http.response.start", "status": 200, "headers": []})
        raise RuntimeError(SENTINEL)

    sent = run_boundary(inner)

    assert [message["type"] for message in sent] == ["http.response.start"]


def test_a_scope_other_than_http_passes_through() -> None:
    calls: list[str] = []

    async def inner(scope: Scope, receive: Receive, send: Send) -> None:
        calls.append(scope["type"])

    assert run_boundary(inner, scope_type="lifespan") == []
    assert calls == ["lifespan"]


def test_the_application_engine_hides_statement_parameters(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEC_APP_DATABASE_URL", CLOSED)

    assert get_engine(Settings()).hide_parameters is True  # type: ignore[call-arg]


def test_a_405_names_the_allowed_methods() -> None:
    with TestClient(create_app(registry=CalculatorRegistry())) as client:
        response = client.delete(f"/calculations/{uuid.uuid4()}")

    assert (response.status_code, response.json()["code"]) == (405, "method_not_allowed")
    assert response.headers["allow"] == "GET"


def test_a_uuid_error_does_not_echo_the_path_value(engine: Engine) -> None:
    with TestClient(make_app(engine, FixedSource())) as client:
        response = client.get(f"/calculations/{SENTINEL}")

    (field,) = response.json()["fields"]
    assert response.status_code == 422
    assert field == {"location": ["path", "result_id"], "message": "Invalid value."}
    assert SENTINEL not in response.text


def test_a_static_pydantic_message_is_kept(engine: Engine) -> None:
    with TestClient(make_app(engine, FixedSource())) as client:
        response = client.post("/calculations", json={"inputs": {}})

    assert response.json()["fields"] == [
        {"location": ["body", "calculation_type"], "message": "Field required"}
    ]


def test_two_first_requests_at_once_build_one_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEC_APP_DATABASE_URL", CLOSED)
    built: list[Engine] = []

    def slow_engine(settings: Settings) -> Engine:
        time.sleep(0.05)
        engine = create_engine("sqlite://")
        built.append(engine)
        return engine

    monkeypatch.setattr(dependencies, "get_engine", slow_engine)
    state = SimpleNamespace(session_factory=None, owns_session_factory=False)
    request: Any = SimpleNamespace(app=SimpleNamespace(state=state))
    threads = [threading.Thread(target=dependencies._session_factory, args=(request,)) for _ in range(2)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(built) == 1
    assert state.owns_session_factory is True


def dispose_calls(monkeypatch: pytest.MonkeyPatch) -> list[Engine]:
    disposed: list[Engine] = []
    original = Engine.dispose

    def spy(self: Engine, close: bool = True) -> None:
        disposed.append(self)
        original(self, close)

    monkeypatch.setattr(Engine, "dispose", spy)
    return disposed


def test_an_engine_the_application_built_is_disposed_at_shutdown(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEC_APP_DATABASE_URL", CLOSED)
    disposed = dispose_calls(monkeypatch)
    application = create_app(registry=CalculatorRegistry())

    with TestClient(application, raise_server_exceptions=False) as client:
        client.get(f"/calculations/{uuid.uuid4()}")
        built = application.state.session_factory.kw["bind"]

    assert disposed == [built]


def test_a_given_session_factory_is_not_disposed(monkeypatch: pytest.MonkeyPatch) -> None:
    disposed = dispose_calls(monkeypatch)
    given = create_engine("sqlite://", poolclass=StaticPool)

    with TestClient(create_app(registry=CalculatorRegistry(), session_factory=sessionmaker(bind=given))):
        pass

    assert disposed == []
    given.dispose()
