import logging
from typing import Annotated

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import AfterValidator, BaseModel

from app.api.errors import install_error_handlers
from app.core.exceptions import (
    AlreadyRegisteredError,
    CalculationError,
    CalculationTypeNotRegisteredError,
    CatalogUnavailableError,
    DatabaseUnavailableError,
    DECError,
    ExpressionError,
    InputValidationError,
    NotFoundError,
    ParameterSourceUnavailableError,
    ParameterValidationError,
    UnitError,
)
from app.schemas.api import FieldError

SECRET = "postgresql://user:hunter2@db/dec_app"


def _no_secret(text: str) -> str:
    raise ValueError(f"the value {text!r} is not allowed")


class Body(BaseModel):
    name: Annotated[str, AfterValidator(_no_secret)]
    count: int


FIELDS = (FieldError(location=("body", "inputs", "b"), message="missing input"),)


def make_app(error: Exception) -> FastAPI:
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/raise")
    def raise_error() -> None:
        raise error

    @app.post("/body")
    def accept(body: Body) -> None:
        return None

    return app


def call(error: Exception) -> tuple[int, dict[str, object]]:
    client = TestClient(make_app(error), raise_server_exceptions=False)
    response = client.get("/raise")
    return response.status_code, response.json()


@pytest.mark.parametrize(
    ("error", "status", "code"),
    [
        (NotFoundError(SECRET), 404, "not_found"),
        (CalculationTypeNotRegisteredError("calculation type 't' is not registered"), 409, "calculation_type_not_registered"),
        (InputValidationError(SECRET), 422, "invalid_input"),
        (UnitError(SECRET), 422, "invalid_input"),
        (ParameterSourceUnavailableError("no parameter source for calculation type 't'"), 503, "parameter_source_unavailable"),
        (DatabaseUnavailableError(SECRET), 503, "database_unavailable"),
        (CatalogUnavailableError(SECRET), 503, "catalog_unavailable"),
        (ParameterValidationError(SECRET), 500, "internal_error"),
        (ExpressionError(SECRET), 500, "internal_error"),
        (CalculationError(SECRET), 500, "internal_error"),
        (AlreadyRegisteredError(SECRET), 500, "internal_error"),
        (DECError(SECRET), 500, "internal_error"),
        (RuntimeError(SECRET), 500, "internal_error"),
    ],
)
def test_each_error_has_its_status_and_code(error: Exception, status: int, code: str) -> None:
    got_status, body = call(error)

    assert (got_status, body["code"]) == (status, code)
    assert SECRET not in str(body)
    assert ("fields" in body) == (status == 422)


def test_a_server_known_type_is_named_in_the_message() -> None:
    _, body = call(ParameterSourceUnavailableError("no parameter source for calculation type 'foundations_shallow_r'"))

    assert "foundations_shallow_r" in str(body["message"])


def test_an_unavailable_catalog_answers_its_fixed_message() -> None:
    status, body = call(CatalogUnavailableError(SECRET))

    assert (status, body) == (
        503,
        {"code": "catalog_unavailable", "message": "The normative catalog is not available."},
    )


def test_an_input_error_carries_its_fields() -> None:
    _, body = call(InputValidationError("inputs do not fit", fields=FIELDS))

    assert body["fields"] == [{"location": ["body", "inputs", "b"], "message": "missing input"}]


def test_an_input_error_without_fields_still_has_one() -> None:
    _, body = call(InputValidationError("inputs do not fit"))

    assert body["fields"] == [{"location": ["body", "inputs"], "message": "The inputs do not fit the calculation type."}]


def test_a_schema_error_names_each_field_without_the_value() -> None:
    client = TestClient(make_app(RuntimeError()))
    response = client.post("/body", json={"name": SECRET, "count": "many"})
    body = response.json()

    assert (response.status_code, body["code"]) == (422, "validation_error")
    locations = {tuple(field["location"]) for field in body["fields"]}
    assert locations == {("body", "name"), ("body", "count")}
    assert SECRET not in response.text and "many" not in response.text


def test_an_unknown_route_and_a_wrong_method() -> None:
    client = TestClient(make_app(RuntimeError()))

    unknown = client.get("/nowhere")
    wrong = client.delete("/raise")

    assert (unknown.status_code, unknown.json()["code"]) == (404, "not_found")
    assert (wrong.status_code, wrong.json()["code"]) == (405, "method_not_allowed")


def test_another_http_error_is_an_internal_error() -> None:
    from starlette.exceptions import HTTPException

    status, body = call(HTTPException(status_code=418, detail=SECRET))

    assert (status, body["code"]) == (500, "internal_error")
    assert SECRET not in str(body)


@pytest.mark.parametrize(
    ("error", "code"),
    [
        (InputValidationError(SECRET), "invalid_input"),
        (DatabaseUnavailableError(SECRET), "database_unavailable"),
        (CatalogUnavailableError(SECRET), "catalog_unavailable"),
        (RuntimeError(SECRET), "internal_error"),
    ],
)
def test_the_log_line_names_the_code_and_route_only(error: Exception, code: str, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="app.api"):
        call(error)

    text = "\n".join(record.getMessage() for record in caplog.records)
    assert f"code={code}" in text and "route=/raise" in text
    assert SECRET not in text


def test_a_schema_error_log_holds_no_request_value(caplog: pytest.LogCaptureFixture) -> None:
    client = TestClient(make_app(RuntimeError()))

    with caplog.at_level(logging.INFO, logger="app.api"):
        client.post("/body", json={"name": SECRET, "count": 1})

    text = "\n".join(record.getMessage() for record in caplog.records)
    assert "code=validation_error" in text and "route=/body" in text
    assert SECRET not in text
