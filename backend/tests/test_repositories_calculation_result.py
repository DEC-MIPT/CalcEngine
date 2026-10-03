import uuid
from collections.abc import Iterator
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.models import Base
from app.repositories.calculation_result import CalculationResultRepository

ENVELOPE: dict[str, Any] = {"input_hash": "a" * 64, "outputs": [{"value": -0.0}, {"value": 1e-07}, {"value": 172.5}]}
RECORD: dict[str, Any] = {
    "calculation_type": "t",
    "engine_version": "0.1.0",
    "input_hash": "a" * 64,
    "inputs": {"b": {"value": 1.5, "unit": "m"}},
    "envelope": ENVELOPE,
    "norm_sources": [{"document": "<DOC>", "edition": "unverified"}],
}


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as session:
        yield session
    engine.dispose()


def test_an_added_result_reads_back_equal(session: Session) -> None:
    repository = CalculationResultRepository(session)
    result_id = uuid.uuid4()

    repository.add(result_id=result_id, **RECORD)
    session.commit()
    session.expunge_all()
    row = repository.get(result_id)

    assert row is not None
    assert {name: getattr(row, name) for name in RECORD} == RECORD
    assert row.result_id == result_id
    assert row.created_at is not None


def test_an_unknown_id_reads_nothing(session: Session) -> None:
    assert CalculationResultRepository(session).get(uuid.uuid4()) is None


def test_the_repository_cannot_change_a_result() -> None:
    public = {name for name in dir(CalculationResultRepository) if not name.startswith("_")}

    assert public == {"add", "get"}
