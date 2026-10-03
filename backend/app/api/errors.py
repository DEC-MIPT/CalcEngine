import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from starlette.exceptions import HTTPException

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

LOGGED = (422, 500, 503)


def _route(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", "unmatched")


def _response(request: Request, status: int, code: str, message: str, fields: tuple[FieldError, ...] | None) -> JSONResponse:
    if status in LOGGED:
        logger.warning("code=%s route=%s", code, _route(request))
    body = ErrorBody(code=code, message=message, fields=fields)
    return JSONResponse(body.model_dump(mode="json", exclude_none=True), status_code=status)


def _request_fields(exc: RequestValidationError) -> tuple[FieldError, ...]:
    """Собирает неверные поля запроса с их местом.

    Текст пользовательской проверки может содержать значение клиента, поэтому он
    заменяется фиксированным.

    Args:
        exc: ошибка проверки схемы запроса.

    Returns:
        По записи на каждое неверное поле.
    """
    return tuple(
        FieldError(
            location=tuple(error["loc"]) or ("body",),
            message="Invalid value." if error["type"] in ("value_error", "assertion_error") else error["msg"],
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
    return _response(request, exc.status_code, code, MESSAGES[code], None)


async def _on_database_error(request: Request, exc: Exception) -> JSONResponse:
    """Отвечает ``503 database_unavailable``, когда база не отвечает; текст драйвера может содержать URL, поэтому отбрасывается."""
    return _response(request, 503, "database_unavailable", MESSAGES["database_unavailable"], None)


async def _on_unexpected(request: Request, exc: Exception) -> JSONResponse:
    logger.error("error=%s", type(exc).__name__)
    return _response(request, 500, "internal_error", MESSAGES["internal_error"], None)


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, _on_request_validation)
    app.add_exception_handler(DECError, _on_dec_error)
    app.add_exception_handler(HTTPException, _on_http_error)
    app.add_exception_handler(OperationalError, _on_database_error)
    app.add_exception_handler(Exception, _on_unexpected)
