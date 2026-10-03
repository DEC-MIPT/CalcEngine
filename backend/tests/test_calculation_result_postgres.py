import json
import math
import os
import statistics
import time
import uuid
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, inspect, sql
from sqlalchemy.orm import Session, sessionmaker
from test_engine_foundations_shallow_r import FixedSource as PilotSource
from test_engine_foundations_shallow_r import inputs as pilot_inputs
from test_models_calculation_result import COLUMNS
from test_repositories_calculation_result import ENVELOPE, RECORD
from test_services_submit import FixedSource, make_service, request

from alembic import command
from app.core.config import PARAMS_ROOT
from app.db.session import as_psycopg_url
from app.engine import foundations_shallow_r as pilot
from app.main import create_app
from app.repositories.calculation_result import CalculationResultRepository
from app.services.catalog import build_registry, load_validated_ranges

pytestmark = pytest.mark.postgres

URL = os.environ.get("DEC_TEST_APP_DATABASE_URL")
BACKEND = Path(__file__).resolve().parents[1]
INITIAL = "869e03eddcc5"

if URL is None:
    pytest.skip("DEC_TEST_APP_DATABASE_URL is not set", allow_module_level=True)


@pytest.fixture(scope="module")
def database() -> Iterator[tuple[Config, Engine]]:
    assert URL is not None
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DEC_APP_DATABASE_URL", URL)
        config = Config(str(BACKEND / "alembic.ini"))
        engine = create_engine(as_psycopg_url(URL))
        command.upgrade(config, "head")
        yield config, engine
        command.downgrade(config, INITIAL)
        engine.dispose()


def test_the_migration_creates_the_table(database: tuple[Config, Engine]) -> None:
    _, engine = database
    inspector = inspect(engine)

    assert {column["name"] for column in inspector.get_columns("calculation_result")} == COLUMNS
    types = {column["name"]: str(column["type"]) for column in inspector.get_columns("calculation_result")}
    assert (types["envelope"], types["inputs"], types["norm_sources"]) == ("JSON", "JSON", "JSON")


def test_the_downgrade_drops_the_table_and_the_upgrade_restores_it(database: tuple[Config, Engine]) -> None:
    config, engine = database

    command.downgrade(config, INITIAL)
    assert not inspect(engine).has_table("calculation_result")
    command.upgrade(config, "head")
    assert inspect(engine).has_table("calculation_result")


def test_a_stored_envelope_reads_back_as_the_same_json_text(database: tuple[Config, Engine]) -> None:
    _, engine = database
    result_id = uuid.uuid4()

    with Session(engine) as session:
        CalculationResultRepository(session).add(result_id=result_id, **RECORD)
        session.commit()
    with Session(engine) as session:
        row = CalculationResultRepository(session).get(result_id)
        text: str = session.execute(
            sql.text("SELECT envelope::text FROM calculation_result WHERE result_id = :id"), {"id": result_id}
        ).scalar_one()

    assert row is not None and row.envelope == ENVELOPE
    assert math.copysign(1.0, row.envelope["outputs"][0]["value"]) == -1.0
    assert text == json.dumps(ENVELOPE)


def test_the_service_reads_back_a_stored_result_with_its_storage_time(database: tuple[Config, Engine]) -> None:
    _, engine = database

    with Session(engine) as session:
        envelope = make_service(CalculationResultRepository(session), FixedSource()).submit(request())
        session.commit()
    with Session(engine) as session:
        stored = make_service(CalculationResultRepository(session)).get(envelope.result_id)

    assert stored.envelope == envelope
    assert stored.created_at.tzinfo is not None


def test_the_median_calculation_time_is_at_most_one_second(
    database: tuple[Config, Engine], record_property: Callable[[str, object], None]
) -> None:
    _, engine = database
    registry = build_registry(PARAMS_ROOT)
    application = create_app(
        registry=registry,
        sources={pilot.NAME: PilotSource()},
        validated_ranges=load_validated_ranges(registry, PARAMS_ROOT),
        session_factory=sessionmaker(bind=engine),
    )
    body = {
        "calculation_type": pilot.NAME,
        "inputs": {name: value.model_dump() for name, value in pilot_inputs().items()},
    }

    durations: list[float] = []
    with TestClient(application) as client:
        assert client.post("/calculations", json=body).status_code == 201
        for _ in range(20):
            started = time.perf_counter()
            response = client.post("/calculations", json=body)
            durations.append(time.perf_counter() - started)
            assert response.status_code == 201

    median = statistics.median(durations)
    record_property("median_seconds", median)
    print(f"\nPOST /calculations median over 20: {median * 1000:.1f} ms; max {max(durations) * 1000:.1f} ms")
    assert median <= 1.0
