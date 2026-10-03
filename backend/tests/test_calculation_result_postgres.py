import json
import math
import os
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import Engine, create_engine, inspect, sql
from sqlalchemy.orm import Session
from test_models_calculation_result import COLUMNS
from test_repositories_calculation_result import ENVELOPE, RECORD

from alembic import command
from app.db.session import as_psycopg_url
from app.repositories.calculation_result import CalculationResultRepository

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
