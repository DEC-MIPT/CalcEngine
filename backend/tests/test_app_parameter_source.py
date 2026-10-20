from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from catalog_fixture import PILOT
from fastapi.testclient import TestClient
from interim_fixture import from_catalog, manifest, type_file, write
from pydantic import ValidationError
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import inputs
from test_services_catalog_source import make_source, registry

from app.core.config import INTERIM_ROOT, ApiSettings, ParameterSourceSettings
from app.core.exceptions import ParameterValidationError
from app.main import create_app
from app.models import Base
from app.schemas.calculation import CATALOG_SOURCE
from app.services.catalog_source import CatalogParameterSource
from app.services.interim_source import InterimParameterSource

FIXTURES = Path(__file__).parent / "fixtures" / "params"
VARIABLES = ("DEC_PARAMETER_SOURCE", "DEC_INTERIM_PROFILE", "DEC_INTERIM_ROOT")


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (*VARIABLES, "DEC_APP_DATABASE_URL", "DEC_NORMATIVES_DATABASE_URL"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def results() -> Iterator[Engine]:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def interim_root(root: Path, **files: dict[str, Any]) -> Path:
    write(root / "doc" / "manifest.yaml", manifest())
    for calculation_type, data in files.items():
        write(root / "doc" / f"{calculation_type}.yaml", data)
    return root


def application(results: Engine, settings: ParameterSourceSettings | None = None, **extra: Any) -> Any:
    return create_app(
        registry=registry(),
        validated_ranges={PILOT: ()},
        session_factory=sessionmaker(bind=results),
        source_settings=settings,
        **extra,
    )


def post(client: TestClient) -> Any:
    given = {name: value.model_dump() for name, value in inputs().items()}
    return client.post("/calculations", json={"calculation_type": PILOT, "inputs": given})


def interim(root: Path, profile: str = "strict") -> ParameterSourceSettings:
    return ParameterSourceSettings.model_validate(
        {"DEC_PARAMETER_SOURCE": "interim", "DEC_INTERIM_PROFILE": profile, "DEC_INTERIM_ROOT": str(root)}
    )


def test_the_default_setting_is_the_catalog_with_the_strict_profile_and_the_backend_root() -> None:
    settings = ParameterSourceSettings()

    assert (settings.dec_parameter_source, settings.dec_interim_profile) == ("catalog", "strict")
    assert settings.dec_interim_root == INTERIM_ROOT
    assert INTERIM_ROOT.parent.name == "backend" and INTERIM_ROOT.name == "interim_normatives"


def test_the_settings_are_read_from_the_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("DEC_PARAMETER_SOURCE", "interim")
    monkeypatch.setenv("DEC_INTERIM_PROFILE", "draft")
    monkeypatch.setenv("DEC_INTERIM_ROOT", str(tmp_path))

    settings = ParameterSourceSettings()

    assert (settings.dec_parameter_source, settings.dec_interim_profile, settings.dec_interim_root) == ("interim", "draft", tmp_path)


def test_without_a_setting_every_type_reads_the_catalog(results: Engine, catalog_sqlite: Engine) -> None:
    app = application(results, catalog_session_factory=sessionmaker(bind=catalog_sqlite))

    with TestClient(app) as client:
        response = post(client)
        source = app.state.sources[PILOT]

    assert isinstance(source, CatalogParameterSource)
    assert response.status_code == 201
    assert source.resolve(PILOT, inputs()).source == CATALOG_SOURCE


def test_interim_chosen_reads_the_interim_file(results: Engine, tmp_path: Path) -> None:
    app = application(results, interim(interim_root(tmp_path, **{PILOT: from_catalog(PILOT)})))

    with TestClient(app) as client:
        response = post(client)
        source = app.state.sources[PILOT]

    assert isinstance(source, InterimParameterSource)
    assert response.status_code == 201
    resolved = source.resolve(PILOT, inputs())
    assert resolved.source is not None
    assert (resolved.source.kind, resolved.source.profile) == ("interim", "strict")


def test_interim_chosen_and_a_type_without_a_file_answers_503(results: Engine, tmp_path: Path) -> None:
    app = application(results, interim(interim_root(tmp_path)))

    with TestClient(app) as client:
        response = post(client)

    assert app.state.sources == {}
    assert (response.status_code, response.json()["code"]) == (503, "parameter_source_unavailable")


def test_interim_mode_computes_a_type_without_catalog_bindings(results: Engine, tmp_path: Path) -> None:
    app = application(results, interim(interim_root(tmp_path, **{PILOT: from_catalog(PILOT)})))

    with TestClient(app) as client:
        response = post(client)

    assert response.status_code == 201
    assert response.json()["verdict"] in {"pass", "fail"}


def test_catalog_mode_and_a_type_with_interim_data_only_answers_503_and_reads_no_file(
    results: Engine, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = interim_root(tmp_path, **{PILOT: from_catalog(PILOT)})
    write(root / "doc" / "broken.yaml", type_file(notes=[]))
    monkeypatch.setenv("DEC_INTERIM_ROOT", str(root))
    app = application(results, ParameterSourceSettings())

    with TestClient(app) as client:
        response = post(client)

    assert isinstance(app.state.sources[PILOT], CatalogParameterSource)
    assert (response.status_code, response.json()["code"]) == (503, "parameter_source_unavailable")


def test_invalid_interim_data_stop_the_start_in_interim_mode(results: Engine, tmp_path: Path) -> None:
    root = interim_root(tmp_path)
    write(root / "doc" / "broken.yaml", type_file(notes=[]))

    with pytest.raises(ParameterValidationError, match=r"^doc/broken\.yaml: notes: "), TestClient(application(results, interim(root))):
        pass


def test_passed_sources_keep_priority_over_the_setting(results: Engine, catalog_sqlite: Engine, tmp_path: Path) -> None:
    passed = {PILOT: make_source(catalog_sqlite)}
    app = application(results, interim(tmp_path / "missing"), sources=passed)

    with TestClient(app) as client:
        response = post(client)

    assert app.state.sources == passed
    assert response.status_code == 201


@pytest.mark.parametrize(("variable", "value"), [("DEC_PARAMETER_SOURCE", "file"), ("DEC_INTERIM_PROFILE", "loose")])
def test_an_unknown_setting_value_stops_the_start_naming_the_variable(
    monkeypatch: pytest.MonkeyPatch, variable: str, value: str
) -> None:
    monkeypatch.setenv(variable, value)

    with pytest.raises(ValidationError, match=variable):
        create_app()


@pytest.mark.parametrize("source", ["catalog", "interim"])
def test_a_norm_value_in_params_is_rejected_whatever_the_source(tmp_path: Path, source: str) -> None:
    params = tmp_path / "params"
    params.mkdir()
    (params / f"{PILOT}.yaml").write_text((FIXTURES / "unknown_key.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    settings = ParameterSourceSettings.model_validate(
        {"DEC_PARAMETER_SOURCE": source, "DEC_INTERIM_ROOT": str(interim_root(tmp_path / "interim"))}
    )
    app = create_app(api_settings=ApiSettings.model_validate({"DEC_PARAMS_ROOT": str(params)}), source_settings=settings)

    with pytest.raises(ParameterValidationError, match="formulas"), TestClient(app):
        pass
