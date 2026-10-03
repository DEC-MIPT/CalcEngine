from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool

from app.models import Base
from app.models.calculation_result import CalculationResultRow

COLUMNS = {
    "result_id",
    "calculation_type",
    "engine_version",
    "input_hash",
    "inputs",
    "envelope",
    "norm_sources",
    "created_at",
}


def test_the_metadata_creates_the_table_on_sqlite() -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    assert {column["name"] for column in inspector.get_columns("calculation_result")} == COLUMNS
    assert inspector.get_pk_constraint("calculation_result")["constrained_columns"] == ["result_id"]
    assert [index["column_names"] for index in inspector.get_indexes("calculation_result")] == [["input_hash"]]
    assert CalculationResultRow.__tablename__ == "calculation_result"
