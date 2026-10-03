from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.schemas.api import ErrorBody

BODY_LIMIT = 1024 * 1024
"""1 МиБ (``calculation-api`` "Non-functional — request size and latency")."""


class BodySizeLimit:
    """Отклоняет тело запроса больше лимита ответом ``413`` до того, как его разберёт маршрут.

    Объявленный ``Content-Length`` больше лимита отклоняется сразу; тело без него
    читается с подсчётом до лимита и затем передаётся дальше (design.md, решение 6).
    """

    def __init__(self, app: ASGIApp, limit: int = BODY_LIMIT) -> None:
        self.app = app
        self.limit = limit

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        declared = dict(scope["headers"]).get(b"content-length")
        if declared is not None and (not declared.isdigit() or int(declared) > self.limit):
            await _too_large(scope, receive, send)
            return
        messages: list[Message] = []
        total = 0
        while True:
            message = await receive()
            messages.append(message)
            if message["type"] != "http.request":
                break
            total += len(message.get("body", b""))
            if total > self.limit:
                await _too_large(scope, receive, send)
                return
            if not message.get("more_body", False):
                break

        async def replay() -> Message:
            return messages.pop(0) if messages else await receive()

        await self.app(scope, replay, send)


async def _too_large(scope: Scope, receive: Receive, send: Send) -> None:
    body = ErrorBody(code="payload_too_large", message="The request body is larger than 1 MiB.")
    response = JSONResponse(body.model_dump(mode="json", exclude_none=True), status_code=413)
    await response(scope, receive, send)
