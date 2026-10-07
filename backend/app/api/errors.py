import logging
from collections.abc import Mapping

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from starlette.exceptions import HTTPException
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.exceptions import (
    CalculationTypeNotRegisteredError,
    DatabaseUnavailableError,
    DECError,
    InputValidationError,
    NotFoundError,
    ParameterSourceUnavailableError,
    UnitError,
)
from app.schemas.api import ErrorBody, FieldError

logger = logging.getLogger("app.api")

DEC_ERRORS: tuple[tuple[type[DECError], int, str], ...] = (
    (NotFoundError, 404, "not_found"),
    (CalculationTypeNotRegisteredError, 409, "calculation_type_not_registered"),
    (InputValidationError, 422, "invalid_input"),
    (UnitError, 422, "invalid_input"),
    (ParameterSourceUnavailableError, 503, "parameter_source_unavailable"),
    (DatabaseUnavailableError, 503, "database_unavailable"),
)
"""Таблица ``calculation-api`` "Error responses"; любая другая ошибка — ``500 internal_error``."""

HTTP_CODES = {404: "not_found", 405: "method_not_allowed"}

MESSAGES = {
    "not_found": "The requested resource does not exist.",
    "method_not_allowed": "The method is not allowed for this resource.",
    "validation_error": "The request does not match its schema.",
    "invalid_input": "The inputs do not fit the calculation type.",
    "database_unavailable": "The application database is not available.",
    "internal_error": "Internal server error.",
}
"""Фиксированные тексты, чтобы ни одно сообщение не повторяло значение, присланное клиентом."""

SERVER_NAMED = ("calculation_type_not_registered", "parameter_source_unavailable")
"""Коды, сообщение которых называет известный серверу тип расчёта, а не значение клиента."""

LOGGED = (422, 503)
"""Коды, для которых ``_response`` пишет строку лога; ``500`` пишет одну свою строку с типом исключения."""

STATIC_MESSAGE_TYPES = frozenset(
    {
        "missing",
        "extra_forbidden",
        "string_type",
        "string_too_short",
        "string_too_long",
        "float_type",
        "float_parsing",
        "finite_number",
        "dict_type",
        "model_type",
        "model_attributes_type",
        "json_invalid",
        "uuid_type",
        "date_type",
        "date_from_datetime_parsing",
        "bool_type",
    }
)
"""Типы ошибок pydantic, текст которых не содержит значения клиента; у остальных — фиксированный текст."""


def _route(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", "unmatched")


def _log_internal_error(request: Request, exc: BaseException) -> None:
    logger.error("code=internal_error route=%s error=%s", _route(request), type(exc).__name__)


def _response(
    request: Request,
    status: int,
    code: str,
    message: str,
    fields: tuple[FieldError, ...] | None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    if status in LOGGED:
        logger.warning("code=%s route=%s", code, _route(request))
    body = ErrorBody(code=code, message=message, fields=fields)
    return JSONResponse(body.model_dump(mode="json", exclude_none=True), status_code=status, headers=headers)


def _request_fields(exc: RequestValidationError) -> tuple[FieldError, ...]:
    """Собирает неверные поля запроса с их местом.

    Текст pydantic передаётся, только если его тип из ``STATIC_MESSAGE_TYPES``: у
    остальных (пользовательские проверки, разбор UUID и т. п.) текст может содержать
    значение клиента, поэтому он заменяется фиксированным.

    Args:
        exc: ошибка проверки схемы запроса.

    Returns:
        По записи на каждое неверное поле.
    """
    return tuple(
        FieldError(
            location=tuple(error["loc"]) or ("body",),
            message=error["msg"] if error["type"] in STATIC_MESSAGE_TYPES else "Invalid value.",
        )
        for error in exc.errors()
    )


def _input_fields(exc: DECError) -> tuple[FieldError, ...]:
    fields = getattr(exc, "fields", ())
    return tuple(fields) or (FieldError(location=("body", "inputs"), message=MESSAGES["invalid_input"]),)


async def _on_request_validation(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    return _response(request, 422, "validation_error", MESSAGES["validation_error"], _request_fields(exc))


async def _on_dec_error(request: Request, exc: Exception) -> JSONResponse:
    for error_type, status, code in DEC_ERRORS:
        if isinstance(exc, error_type):
            assert isinstance(exc, DECError)
            message = str(exc) if code in SERVER_NAMED else MESSAGES[code]
            return _response(request, status, code, message, _input_fields(exc) if status == 422 else None)
    return await _on_unexpected(request, exc)


async def _on_http_error(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, HTTPException)
    code = HTTP_CODES.get(exc.status_code)
    if code is None:
        return await _on_unexpected(request, exc)
    return _response(request, exc.status_code, code, MESSAGES[code], None, exc.headers)


async def _on_database_error(request: Request, exc: Exception) -> JSONResponse:
    """Отвечает ``503 database_unavailable``, когда база не отвечает; текст драйвера может содержать URL, поэтому отбрасывается."""
    return _response(request, 503, "database_unavailable", MESSAGES["database_unavailable"], None)


async def _on_unexpected(request: Request, exc: Exception) -> JSONResponse:
    _log_internal_error(request, exc)
    return _response(request, 500, "internal_error", MESSAGES["internal_error"], None)


class UnexpectedErrors:
    """Отвечает ``500 internal_error`` на любое необработанное исключение и не пробрасывает его.

    Обработчик ``Exception`` у Starlette после ответа снова бросает исключение, и сервер
    пишет полный traceback с текстом ошибки, где может быть SQL с параметрами, то есть
    данные клиента (``calculation-api`` "Error responses", design.md, решение 5). Эта
    прослойка стоит внутри CORS, поэтому ответ ``500`` получает заголовки CORS, а в лог
    попадает одна строка с кодом, маршрутом и типом исключения — и тогда, когда ответ
    уже начат.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        started = False

        async def tracked(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self.app(scope, receive, tracked)
        except Exception as exc:  # noqa: BLE001 - the boundary catches everything by design
            request = Request(scope)
            _log_internal_error(request, exc)
            if not started:
                response = _response(request, 500, "internal_error", MESSAGES["internal_error"], None)
                await response(scope, receive, send)


def install_error_handlers(app: FastAPI) -> None:
    """Подключает обработчики ошибок и прослойку ``UnexpectedErrors``.

    Args:
        app: приложение FastAPI.
    """
    app.add_exception_handler(RequestValidationError, _on_request_validation)
    app.add_exception_handler(DECError, _on_dec_error)
    app.add_exception_handler(HTTPException, _on_http_error)
    app.add_exception_handler(OperationalError, _on_database_error)
    app.add_middleware(UnexpectedErrors)
