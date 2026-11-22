import importlib.util
from pathlib import Path
from types import ModuleType

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text

VERSIONS = Path(__file__).parents[1] / "alembic" / "versions"


def revision(filename: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location("test_revision", VERSIONS / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_actual_migration_upgrade_downgrade_reupgrade_preserves_predecessor() -> None:
    predecessor = revision("ae350ead9bfd_calculation_result.py")
    migration = revision("20261122_foundation_design.py")
    assert migration.down_revision == predecessor.revision
    engine = create_engine("sqlite://")
    try:
        with engine.begin() as connection, Operations.context(MigrationContext.configure(connection)):
            predecessor.upgrade()
            connection.execute(text(
                "INSERT INTO calculation_result "
                "(result_id, calculation_type, engine_version, input_hash, inputs, envelope, norm_sources, created_at) "
                "VALUES ('00000000000000000000000000000001', 'pilot', 'v1', 'hash', '{}', '{}', '[]', '2026-11-22')"
            ))
            for _ in range(2):
                migration.upgrade()
                inspector = inspect(connection)
                assert {"calculation_result", "foundation_context", "foundation_selection"} == set(inspector.get_table_names())
                index = next(item for item in inspector.get_indexes("foundation_selection")
                             if item["name"] == "ix_foundation_selection_input_hash")
                assert index["column_names"] == ["input_hash"]
                for table, column in (("foundation_context", "result_id"), ("foundation_selection", "selected_result_id")):
                    foreign_keys = inspector.get_foreign_keys(table)
                    assert len(foreign_keys) == 1
                    assert foreign_keys[0]["constrained_columns"] == [column]
                    assert foreign_keys[0]["referred_table"] == "calculation_result"
                    assert foreign_keys[0]["referred_columns"] == ["result_id"]
                assert inspector.get_pk_constraint("foundation_context")["constrained_columns"] == ["result_id"]
                assert inspector.get_pk_constraint("foundation_selection")["constrained_columns"] == ["selection_id"]
                migration.downgrade()
                assert inspect(connection).get_table_names() == ["calculation_result"]
                assert connection.scalar(text("SELECT count(*) FROM calculation_result WHERE input_hash = 'hash'")) == 1
            migration.upgrade()
            assert {"foundation_context", "foundation_selection"} <= set(inspect(connection).get_table_names())
    finally:
        engine.dispose()
