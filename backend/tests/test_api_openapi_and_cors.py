from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.config import ApiSettings
from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.schemas.report import MAX_LENGTH

DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
ERROR_BODY = "#/components/schemas/ErrorBody"

ENDPOINTS = {
    ("/calculation-types", "get"): set(),
    ("/calculations", "post"): {"404", "413", "422", "503"},
    ("/calculations/{result_id}", "get"): {"404", "422", "503"},
    ("/calculations/{result_id}/report", "post"): {"404", "409", "413", "422", "503"},
}


@pytest.fixture(autouse=True)
def no_database_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)


@pytest.fixture(scope="module")
def openapi() -> dict[str, Any]:
    with TestClient(create_app(registry=CalculatorRegistry())) as client:
        document: dict[str, Any] = client.get("/openapi.json").json()
    return document


def operation(openapi: dict[str, Any], path: str, method: str) -> dict[str, Any]:
    found: dict[str, Any] = openapi["paths"][path][method]
    return found


def test_the_four_endpoints_are_described(openapi: dict[str, Any]) -> None:
    described = {(path, method) for path, methods in openapi["paths"].items() for method in methods}

    assert set(ENDPOINTS) <= described


@pytest.mark.parametrize(("path", "method"), list(ENDPOINTS))
def test_each_endpoint_lists_its_error_responses_with_the_error_body(
    openapi: dict[str, Any], path: str, method: str
) -> None:
    responses = operation(openapi, path, method)["responses"]
    errors = {status for status in responses if status.startswith(("4", "5"))}

    assert errors == ENDPOINTS[(path, method)]
    for status in errors:
        assert responses[status]["content"]["application/json"]["schema"] == {"$ref": ERROR_BODY}


def test_the_request_schemas_are_described(openapi: dict[str, Any]) -> None:
    def body_ref(path: str) -> str:
        ref: str = operation(openapi, path, "post")["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        return ref

    assert body_ref("/calculations").endswith("/CalculationRequest")
    assert body_ref("/calculations/{result_id}/report").endswith("/ReportRequest")
    parameters = operation(openapi, "/calculations/{result_id}", "get")["parameters"]
    assert [(p["name"], p["in"], p["schema"]["format"]) for p in parameters] == [("result_id", "path", "uuid")]


def test_the_report_text_limits_are_published_as_max_length(openapi: dict[str, Any]) -> None:
    schemas = openapi["components"]["schemas"]
    title = schemas["TitleBlockData"]["properties"]

    assert {field: title[field]["maxLength"] for field in ("designation", "document_name", "documentation_kind", "organization")} == {
        "designation": MAX_LENGTH["1"],
        "document_name": MAX_LENGTH["5"],
        "documentation_kind": MAX_LENGTH["6"],
        "organization": MAX_LENGTH["9"],
    }
    assert schemas["Signatory"]["properties"]["surname"]["maxLength"] == MAX_LENGTH["11"]


def test_the_success_responses_are_described(openapi: dict[str, Any]) -> None:
    def success(path: str, method: str, status: str) -> dict[str, Any]:
        content: dict[str, Any] = operation(openapi, path, method)["responses"][status]["content"]
        return content

    listing = success("/calculation-types", "get", "200")["application/json"]["schema"]
    assert listing["type"] == "array" and listing["items"]["$ref"].endswith("/CalculationTypeView")
    assert success("/calculations", "post", "201")["application/json"]["schema"]["$ref"].endswith("/ResultEnvelope")
    assert success("/calculations/{result_id}", "get", "200")["application/json"]["schema"]["$ref"].endswith(
        "/ResultEnvelope"
    )
    assert DOCX in success("/calculations/{result_id}/report", "post", "200")


def test_the_error_body_schema_is_published(openapi: dict[str, Any]) -> None:
    schema = openapi["components"]["schemas"]["ErrorBody"]

    assert set(schema["properties"]) == {"code", "message", "fields"}
    assert "HTTPValidationError" not in str(
        [operation(openapi, path, method)["responses"] for path, method in ENDPOINTS]
    )


def app_with(origins: str | None) -> TestClient:
    settings = ApiSettings.model_validate({} if origins is None else {"DEC_CORS_ORIGINS": origins})
    return TestClient(create_app(settings, registry=CalculatorRegistry()))


def preflight(client: TestClient, origin: str, method: str = "POST") -> Any:
    return client.options(
        "/calculations",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "content-type",
        },
    )


def test_a_preflight_from_a_configured_origin_is_allowed() -> None:
    with app_with("http://localhost:5173,https://dec.example") as client:
        response = preflight(client, "https://dec.example")

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://dec.example"
    assert "access-control-allow-credentials" not in response.headers


def test_a_preflight_from_another_origin_is_not_allowed() -> None:
    with app_with("http://localhost:5173") as client:
        response = preflight(client, "https://elsewhere.example")

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_no_origin_is_allowed_when_none_is_configured() -> None:
    with app_with(None) as client:
        options = preflight(client, "http://localhost:5173")
        simple = client.get("/calculation-types", headers={"Origin": "http://localhost:5173"})

    assert "access-control-allow-origin" not in options.headers
    assert simple.status_code == 200 and "access-control-allow-origin" not in simple.headers


def test_a_method_that_changes_a_result_is_not_allowed_across_origins() -> None:
    with app_with("http://localhost:5173") as client:
        response = preflight(client, "http://localhost:5173", method="DELETE")

    assert response.status_code == 400


def test_a_simple_request_exposes_location_and_content_disposition() -> None:
    with app_with("http://localhost:5173") as client:
        response = client.get("/calculation-types", headers={"Origin": "http://localhost:5173"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    exposed = {name.strip().lower() for name in response.headers["access-control-expose-headers"].split(",")}
    assert exposed == {"location", "content-disposition"}
