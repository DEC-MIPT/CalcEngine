import json
from collections.abc import Iterator
from typing import Any

import pytest
from catalog_fixture import (
    CATALOG_COLUMNS,
    JSON_COLUMNS,
    PILOT,
    PLACEHOLDER_CLAUSES,
    PLACEHOLDER_DOCUMENTS,
    PLACEHOLDER_EDITION,
    PLACEHOLDER_VALUES,
    ROWS,
    SCHEMA,
    SQL_FILE,
    load_postgres,
)
from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import parameters

from app.engine import foundations_shallow_r as pilot
from app.schemas.calculation import NormRef
from app.schemas.expression import parse_expression

PARAMETER_VIEWS = ("type_formulas", "type_table_values", "type_thresholds", "type_checks")


def read(engine: Engine, view: str) -> list[dict[str, Any]]:
    with engine.connect() as connection:
        rows = connection.execute(text(f"SELECT * FROM {SCHEMA}.{view}")).mappings().all()
    return [
        {column: json.loads(value) if (view, column) in JSON_COLUMNS else value for column, value in row.items()}
        for row in rows
    ]


def leaves(value: Any) -> Iterator[tuple[str | None, Any]]:
    """Все листья вложенных словарей и списков вместе с ключом, под которым они лежат."""
    stack: list[tuple[str | None, Any]] = [(None, value)]
    while stack:
        key, item = stack.pop()
        if isinstance(item, dict):
            stack.extend(item.items())
        elif isinstance(item, list | tuple):
            stack.extend((key, element) for element in item)
        else:
            yield key, item


def test_the_sqlite_fixture_has_the_columns_and_rows_of_the_contract(catalog_sqlite: Engine) -> None:
    with catalog_sqlite.connect() as connection:
        for view, columns in CATALOG_COLUMNS.items():
            info = connection.exec_driver_sql(f"PRAGMA {SCHEMA}.table_info({view})").all()
            assert [row[1] for row in info] == [column for column, _ in columns], view
            assert len(read(catalog_sqlite, view)) == len(ROWS[view]), view


def test_json_columns_come_back_as_they_were_stored(catalog_sqlite: Engine) -> None:
    for view in CATALOG_COLUMNS:
        assert read(catalog_sqlite, view) == [dict(row) for row in ROWS[view]], view


def test_every_tree_parses_and_every_reference_is_a_norm_ref(catalog_sqlite: Engine) -> None:
    for row in read(catalog_sqlite, "type_formulas"):
        parse_expression(row["tree"])
    for view in CATALOG_COLUMNS:
        for row in read(catalog_sqlite, view):
            for ref in row.get("norm_refs", []):
                NormRef.model_validate(ref)


def test_each_pilot_parameter_is_in_exactly_one_view(catalog_sqlite: Engine) -> None:
    found = [
        (row["parameter"], view)
        for view in PARAMETER_VIEWS
        for row in read(catalog_sqlite, view)
        if row["calculation_type"] == PILOT
    ]
    views = {parameter: {view for name, view in found if name == parameter} for parameter, _ in found}

    assert set(views) == set(pilot.Parameters.model_fields)
    assert all(len(names) == 1 for names in views.values())


def test_the_selected_rows_agree_with_the_engine_tests_at_twenty_degrees(catalog_sqlite: Engine) -> None:
    expected = parameters()
    rows = read(catalog_sqlite, "type_table_values")

    for row in rows:
        entry = getattr(expected, row["parameter"])
        assert (row["symbol"], row["unit"]) == (entry.symbol, entry.value.unit)
        if row["heading_symbol"] is None or row["heading_value"] == 20.0:
            assert row["value"] == entry.value.value
    selected = [row for row in rows if row["heading_symbol"] is not None]
    assert {row["parameter"] for row in selected} == {"m_gamma", "m_q", "m_c"}
    assert {(row["heading_symbol"], row["heading_unit"]) for row in selected} == {("phi_II", "deg")}


def test_the_fixture_data_holds_only_placeholders(catalog_sqlite: Engine) -> None:
    for view in CATALOG_COLUMNS:
        for key, value in leaves(read(catalog_sqlite, view)):
            if isinstance(value, bool) or value is None:
                continue
            if isinstance(value, int | float):
                assert value in PLACEHOLDER_VALUES, (view, key, value)
            elif key in {"document", "designation"}:
                assert value in PLACEHOLDER_DOCUMENTS, (view, key, value)
            elif key == "edition":
                assert value == PLACEHOLDER_EDITION, (view, key, value)
            elif key in {"clause", "number"}:
                assert value in PLACEHOLDER_CLAUSES, (view, key, value)


def test_the_contract_sql_holds_no_data() -> None:
    sql = SQL_FILE.read_text(encoding="utf-8").upper()

    assert "INSERT" not in sql and "COPY" not in sql


def test_the_postgres_loader_refuses_a_database_not_named_test() -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    event.listen(engine, "connect", lambda connection, _: connection.create_function("current_database", 0, lambda: "dec"))

    with pytest.raises(RuntimeError, match=r"\*_test"):
        load_postgres(engine)

    with engine.connect() as connection:
        assert connection.exec_driver_sql("SELECT name FROM sqlite_master").all() == []
    engine.dispose()


@pytest.mark.postgres
def test_the_postgres_fixture_loads_the_contract(catalog_postgres: Engine) -> None:
    with catalog_postgres.connect() as connection:
        for view in CATALOG_COLUMNS:
            count: int = connection.execute(text(f"SELECT count(*) FROM {SCHEMA}.{view}")).scalar_one()
            assert count == len(ROWS[view]), view
        hits = connection.execute(
            text(f"SELECT kind, number FROM {SCHEMA}.search(:query, :max_rows)"),
            {"query": "фундамент", "max_rows": 10},
        ).all()
        role: bool = connection.execute(
            text("SELECT has_schema_privilege('dec_catalog_test_reader', 'catalog_read', 'USAGE')")
        ).scalar_one()

    assert [tuple(hit) for hit in hits] == [("clause", PLACEHOLDER_CLAUSES[2])]
    assert role is True
