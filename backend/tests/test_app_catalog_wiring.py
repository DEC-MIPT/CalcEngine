from collections.abc import Iterator

import pytest
from catalog_fixture import PILOT, REFS
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from test_api_calculations import CONTRACT, SyntheticCalculator
from test_engine_foundations_shallow_r import inputs
from test_services_catalog_source import registry

from app.db.catalog import CatalogSessions
from app.main import create_app
from app.models import Base
from app.services.catalog_source import CatalogParameterSource, catalog_sources


@pytest.fixture
def results() -> Iterator[Engine]:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def test_an_application_without_sources_answers_the_pilot_from_the_catalog(
    catalog_sqlite: Engine, results: Engine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)
    app = create_app(
        registry=registry(),
        validated_ranges={PILOT: ()},
        session_factory=sessionmaker(bind=results),
        catalog_session_factory=sessionmaker(bind=catalog_sqlite),
    )
    given = {name: value.model_dump() for name, value in inputs().items()}

    with TestClient(app) as client:
        response = client.post("/calculations", json={"calculation_type": PILOT, "inputs": given})

    trace = response.json()["trace"]
    assert response.status_code == 201
    assert trace and all(step["norm_refs"] == REFS for step in trace)


def test_every_registered_type_with_a_model_shares_one_catalog_source(catalog_sqlite: Engine) -> None:
    found = registry()
    found.register(CONTRACT, SyntheticCalculator())
    app = create_app(registry=found, catalog_session_factory=sessionmaker(bind=catalog_sqlite))

    with TestClient(app):
        sources = app.state.sources

    assert list(sources) == [PILOT]
    assert isinstance(sources[PILOT], CatalogParameterSource)


def test_catalog_sources_skip_a_type_without_a_model() -> None:
    assert catalog_sources(registry(), CatalogSessions(), models={}) == {}


def test_given_sources_replace_the_catalog() -> None:
    given = {PILOT: CatalogParameterSource(CatalogSessions(), registry())}
    app = create_app(registry=registry(), sources=given)

    with TestClient(app):
        assert app.state.sources == given
