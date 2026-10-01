from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import PARAMS_ROOT, ApiSettings
from app.core.exceptions import DECError
from app.engine.registry import CalculatorRegistry
from app.main import create_app


@pytest.fixture(autouse=True)
def no_database_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)


def test_health_answers_without_the_database_variable() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert (response.status_code, response.json()) == (200, {"status": "ok"})


def test_the_module_app_is_importable_without_the_database_variable() -> None:
    from app.main import app

    with TestClient(app) as client:
        assert client.get("/health").status_code == 200


def test_the_lifespan_builds_the_registry_from_api_settings_only() -> None:
    application = create_app(ApiSettings.model_validate({"DEC_PARAMS_ROOT": PARAMS_ROOT}))

    with TestClient(application):
        registry = application.state.registry

    assert isinstance(registry, CalculatorRegistry)
    assert registry.contract("foundations_shallow_r").name == "foundations_shallow_r"


def test_a_given_registry_is_used_as_is() -> None:
    registry = CalculatorRegistry()
    application = create_app(registry=registry)

    with TestClient(application):
        assert application.state.registry is registry


def test_a_missing_parameter_file_stops_the_start_up(tmp_path: Path) -> None:
    application = create_app(ApiSettings.model_validate({"DEC_PARAMS_ROOT": tmp_path}))

    with pytest.raises(DECError), TestClient(application):
        pass
