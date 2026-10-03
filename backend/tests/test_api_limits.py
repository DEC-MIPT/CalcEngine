import asyncio
from collections.abc import Iterator

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.types import Message, Receive, Scope, Send

from app.api.limits import BODY_LIMIT, BodySizeLimit
from app.main import create_app


@pytest.fixture
def seen() -> list[int]:
    return []


@pytest.fixture
def client(seen: list[int]) -> TestClient:
    app = FastAPI()
    app.add_middleware(BodySizeLimit)

    @app.post("/echo")
    async def echo(request: Request) -> dict[str, int]:
        size = len(await request.body())
        seen.append(size)
        return {"size": size}

    @app.get("/plain")
    def plain() -> dict[str, str]:
        return {"ok": "yes"}

    return TestClient(app)


def chunks(total: int, size: int = 64 * 1024) -> Iterator[bytes]:
    while total > 0:
        yield b"x" * min(size, total)
        total -= size


def test_a_declared_body_over_the_limit_is_refused_before_the_route(client: TestClient, seen: list[int]) -> None:
    response = client.post("/echo", content=b"x" * (BODY_LIMIT + 1))

    assert (response.status_code, response.json()) == (
        413,
        {"code": "payload_too_large", "message": "The request body is larger than 1 MiB."},
    )
    assert seen == []


def test_a_chunked_body_over_the_limit_is_refused_before_the_route(client: TestClient, seen: list[int]) -> None:
    response = client.post("/echo", content=chunks(BODY_LIMIT + 1))

    assert response.status_code == 413
    assert seen == []


def test_a_body_of_exactly_the_limit_passes(client: TestClient, seen: list[int]) -> None:
    declared = client.post("/echo", content=b"x" * BODY_LIMIT)
    chunked = client.post("/echo", content=chunks(BODY_LIMIT))

    assert (declared.status_code, chunked.status_code) == (200, 200)
    assert seen == [BODY_LIMIT, BODY_LIMIT]


def test_a_malformed_length_is_refused(client: TestClient, seen: list[int]) -> None:
    response = client.post("/echo", content=b"{}", headers={"content-length": "abc"})

    assert response.status_code == 413
    assert seen == []


def test_a_request_without_a_body_passes(client: TestClient) -> None:
    assert client.get("/plain").json() == {"ok": "yes"}


@pytest.mark.parametrize(
    "path", ["/health", "/calculations", "/calculations/00000000-0000-0000-0000-000000000001/report"]
)
def test_the_application_has_the_limit_on_every_route(path: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    with TestClient(create_app()) as client:
        response = client.post(path, content=b"x" * (BODY_LIMIT + 1), headers={"content-type": "application/json"})

    assert (response.status_code, response.json()["code"]) == (413, "payload_too_large")


def run_asgi(messages: list[Message], limit: int = 10) -> tuple[list[Message], list[Message]]:
    received: list[Message] = []
    sent: list[Message] = []

    async def inner(scope: Scope, receive: Receive, send: Send) -> None:
        while True:
            message = await receive()
            received.append(message)
            if message["type"] != "http.request" or not message.get("more_body", False):
                break
        await send({"type": "http.response.start", "status": 204, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    queue = list(messages)

    async def receive() -> Message:
        return queue.pop(0)

    async def send(message: Message) -> None:
        sent.append(message)

    scope: Scope = {"type": "http", "method": "POST", "path": "/", "headers": []}
    asyncio.run(BodySizeLimit(inner, limit)(scope, receive, send))
    return received, sent


def test_a_body_in_several_messages_is_counted_and_replayed() -> None:
    parts: list[Message] = [
        {"type": "http.request", "body": b"12345", "more_body": True},
        {"type": "http.request", "body": b"67890", "more_body": False},
    ]

    received, sent = run_asgi(parts)

    assert received == parts
    assert sent[0]["status"] == 204


def test_a_body_in_several_messages_over_the_limit_is_refused() -> None:
    received, sent = run_asgi(
        [
            {"type": "http.request", "body": b"123456", "more_body": True},
            {"type": "http.request", "body": b"789012", "more_body": False},
        ]
    )

    assert received == []
    assert sent[0]["status"] == 413


def test_a_disconnect_is_handed_on() -> None:
    received, _ = run_asgi([{"type": "http.disconnect"}])

    assert received == [{"type": "http.disconnect"}]
