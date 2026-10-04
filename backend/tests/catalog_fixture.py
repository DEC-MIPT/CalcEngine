"""Синтетический контракт каталога норм для тестов (``normative-catalog-backend`` design.md, решение 9).

Колонки повторяют решение 2 дизайна. Все данные — заглушки: документы, редакции и
пункты из ``PLACEHOLDER_DOCUMENTS`` и ``PLACEHOLDER_CLAUSES``, числа из
``PLACEHOLDER_VALUES``; ни одно значение не взято из нормы. Строки пилота при
``phi_II = 20 deg`` дают те же параметры, что ``parameters()`` из тестов движка.
"""

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from sqlalchemy import Connection, Engine, text
from test_engine_foundations_shallow_r import R_UNITS, SYNTHETIC_R, num, op, sym

SQL_FILE = Path(__file__).resolve().parent / "sql" / "catalog_contract.sql"
SCHEMA = "catalog_read"
TEST_ROLE = "dec_catalog_test_reader"
"""Роль-читатель синтетического контракта.

Не ``dec_normatives_reader``: роли общие для всего кластера ``dec-postgres``, где лежит и
база Егора ``dec``, и роль, созданная тестом, помешала бы его инжесту.
"""

PILOT = "foundations_shallow_r"
PLACEHOLDER_DOCUMENTS = ("<NORM-DOC-PLACEHOLDER>", "<NORM-DOC-PLACEHOLDER-2>")
PLACEHOLDER_CLAUSES = (
    "<CLAUSE-PLACEHOLDER>",
    "<CLAUSE-PLACEHOLDER-1>",
    "<CLAUSE-PLACEHOLDER-2>",
    "<CLAUSE-PLACEHOLDER-3>",
)
PLACEHOLDER_EDITION = "unverified"
PLACEHOLDER_VALUES = frozenset(
    {0.25, 0.5, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 7.5, 10.0, 12.5, 20.0, 30.0}
)
"""Все числа данных фикстуры, включая числа в деревьях формул и номера страниц."""

CATALOG_COLUMNS: Mapping[str, tuple[tuple[str, str], ...]] = {
    "documents": (
        ("document_id", "integer"),
        ("designation", "text"),
        ("title", "text"),
        ("edition", "text"),
        ("year", "integer"),
        ("source_url", "text"),
    ),
    "clauses": (
        ("document_id", "integer"),
        ("position", "integer"),
        ("number", "text"),
        ("title", "text"),
        ("page", "integer"),
    ),
    "type_formulas": (
        ("calculation_type", "text"),
        ("parameter", "text"),
        ("result_symbol", "text"),
        ("latex", "text"),
        ("tree", "jsonb"),
        ("units", "jsonb"),
        ("norm_refs", "jsonb"),
    ),
    "type_table_values": (
        ("calculation_type", "text"),
        ("parameter", "text"),
        ("symbol", "text"),
        ("latex", "text"),
        ("value", "numeric"),
        ("unit", "text"),
        ("heading_symbol", "text"),
        ("heading_value", "numeric"),
        ("heading_unit", "text"),
        ("norm_refs", "jsonb"),
    ),
    "type_thresholds": (
        ("calculation_type", "text"),
        ("parameter", "text"),
        ("latex", "text"),
        ("value", "numeric"),
        ("unit", "text"),
        ("norm_refs", "jsonb"),
    ),
    "type_checks": (
        ("calculation_type", "text"),
        ("parameter", "text"),
        ("norm_refs", "jsonb"),
    ),
    "type_method_bounds": (
        ("calculation_type", "text"),
        ("quantity", "text"),
        ("kind", "text"),
        ("value", "numeric"),
        ("unit", "text"),
        ("inclusive", "boolean"),
        ("norm_refs", "jsonb"),
    ),
}
"""Представления ``catalog_read`` и их колонки с типами PostgreSQL, по решению 2."""

SEARCH_COLUMNS = (
    ("kind", "text"),
    ("document_id", "integer"),
    ("designation", "text"),
    ("edition", "text"),
    ("number", "text"),
    ("title", "text"),
    ("rank", "real"),
)
"""Колонки, которые возвращает ``catalog_read.search(query, max_rows)``."""

REFS = [
    {
        "document": PLACEHOLDER_DOCUMENTS[0],
        "edition": PLACEHOLDER_EDITION,
        "clause": PLACEHOLDER_CLAUSES[0],
        "status": "unverified",
        "provenance": "machine-extracted",
    }
]


def _table_value(parameter: str, symbol: str, value: float, heading: float | None = None) -> dict[str, Any]:
    return {
        "calculation_type": PILOT,
        "parameter": parameter,
        "symbol": symbol,
        "latex": symbol,
        "value": value,
        "unit": "1",
        "heading_symbol": None if heading is None else "phi_II",
        "heading_value": heading,
        "heading_unit": None if heading is None else "deg",
        "norm_refs": REFS,
    }


def _formula(parameter: str, latex: str, tree: dict[str, Any], result: str, units: dict[str, str]) -> dict[str, Any]:
    return {
        "calculation_type": PILOT,
        "parameter": parameter,
        "result_symbol": result,
        "latex": latex,
        "tree": tree,
        "units": units,
        "norm_refs": REFS,
    }


def _bound(quantity: str, kind: str, value: float, unit: str) -> dict[str, Any]:
    return {
        "calculation_type": PILOT,
        "quantity": quantity,
        "kind": kind,
        "value": value,
        "unit": unit,
        "inclusive": True,
        "norm_refs": REFS,
    }


SELECTED = {10.0: (0.25, 2.5, 5.0), 20.0: (0.5, 5.0, 10.0), 30.0: (1.0, 7.5, 12.5)}
"""Строки синтетической таблицы: ``phi_II`` в ``deg`` → (``M_gamma``, ``M_q``, ``M_c``)."""

ROWS: Mapping[str, Sequence[Mapping[str, Any]]] = {
    "documents": (
        {
            "document_id": 1,
            "designation": PLACEHOLDER_DOCUMENTS[0],
            "title": "Синтетический документ об основаниях",
            "edition": PLACEHOLDER_EDITION,
            "year": None,
            "source_url": None,
        },
        {
            "document_id": 2,
            "designation": PLACEHOLDER_DOCUMENTS[1],
            "title": "Второй синтетический документ",
            "edition": PLACEHOLDER_EDITION,
            "year": None,
            "source_url": None,
        },
    ),
    "clauses": (
        {"document_id": 1, "position": 1, "number": PLACEHOLDER_CLAUSES[1], "title": "Синтетический пункт об основаниях", "page": 1},
        {"document_id": 1, "position": 2, "number": PLACEHOLDER_CLAUSES[2], "title": "Синтетический пункт о фундаментах", "page": 2},
        {"document_id": 1, "position": 3, "number": PLACEHOLDER_CLAUSES[3], "title": None, "page": None},
        {"document_id": 2, "position": 1, "number": PLACEHOLDER_CLAUSES[1], "title": "Синтетический пункт о грунтах", "page": None},
    ),
    "type_formulas": (
        _formula("k_z_below", r"k_z = \kappa", num(3.0), "k_z", {"k_z": "1"}),
        _formula("k_z_from", r"k_z = b / 4", op("div", sym("b"), num(4.0)), "k_z", {"b": "m", "k_z": "1"}),
        _formula("r", r"R = \mathrm{synthetic}", SYNTHETIC_R, "R", dict(R_UNITS)),
    ),
    "type_table_values": (
        _table_value("gamma_c1", "gamma_c1", 2.0),
        _table_value("gamma_c2", "gamma_c2", 3.0),
        _table_value("k", "k", 4.0),
        *(
            _table_value(parameter, symbol, values[index], heading)
            for index, (parameter, symbol) in enumerate((("m_gamma", "M_gamma"), ("m_q", "M_q"), ("m_c", "M_c")))
            for heading, values in SELECTED.items()
        ),
    ),
    "type_thresholds": (
        {
            "calculation_type": PILOT,
            "parameter": "k_z_threshold",
            "latex": "b_0",
            "value": 5.0,
            "unit": "m",
            "norm_refs": REFS,
        },
    ),
    "type_checks": ({"calculation_type": PILOT, "parameter": "check_norm_refs", "norm_refs": REFS},),
    "type_method_bounds": (
        _bound("b", "min", 1.0, "m"),
        _bound("b", "max", 10.0, "m"),
        _bound("phi_II", "min", 10.0, "deg"),
        _bound("phi_II", "max", 30.0, "deg"),
    ),
}
"""Строки каждого представления; ``jsonb`` — как объекты Python."""

JSON_COLUMNS = frozenset(
    (view, column) for view, columns in CATALOG_COLUMNS.items() for column, kind in columns if kind == "jsonb"
)

SQLITE_TYPES = {"integer": "INTEGER", "text": "TEXT", "jsonb": "JSON", "numeric": "NUMERIC", "boolean": "BOOLEAN"}


def _encoded(view: str, row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        column: json.dumps(value) if (view, column) in JSON_COLUMNS else value
        for column, value in row.items()
    }


def _insert(connection: Connection, view: str, *, cast_json: bool) -> None:
    columns = [column for column, _ in CATALOG_COLUMNS[view]]
    values = ", ".join(
        f"CAST(:{column} AS jsonb)" if cast_json and (view, column) in JSON_COLUMNS else f":{column}"
        for column in columns
    )
    statement = text(f"INSERT INTO {SCHEMA}.{view} ({', '.join(columns)}) VALUES ({values})")
    connection.execute(statement, [_encoded(view, row) for row in ROWS[view]])


def load_sqlite(engine: Engine) -> None:
    """Подключает к SQLite базу ``catalog_read`` в памяти и заполняет её таблицами-представлениями.

    ``ATTACH`` действует на одно соединение, поэтому движок должен держать одно
    соединение (``StaticPool``).

    Args:
        engine: движок SQLite в памяти со ``StaticPool``.
    """
    with engine.begin() as connection:
        connection.exec_driver_sql(f"ATTACH DATABASE ':memory:' AS {SCHEMA}")
        for view, columns in CATALOG_COLUMNS.items():
            body = ", ".join(f"{column} {SQLITE_TYPES[kind]}" for column, kind in columns)
            connection.exec_driver_sql(f"CREATE TABLE {SCHEMA}.{view} ({body})")
            _insert(connection, view, cast_json=False)


def load_postgres(engine: Engine) -> None:
    """Создаёт синтетический контракт в тестовой базе PostgreSQL и заполняет его.

    Схема ``catalog_read`` пересоздаётся, поэтому база обязана называться ``*_test``:
    URL, по ошибке указывающий на ``dec`` Егора, не сотрёт его схему.

    Args:
        engine: движок тестовой базы под её владельцем.

    Raises:
        RuntimeError: если имя базы не оканчивается на ``_test``.
    """
    with engine.begin() as connection:
        database: str = connection.exec_driver_sql("SELECT current_database()").scalar_one()
        if not re.fullmatch(r"\w+_test", database):
            raise RuntimeError("the synthetic catalog is loaded only into a database named *_test")
        connection.exec_driver_sql(SQL_FILE.read_text(encoding="utf-8"))
        for view in CATALOG_COLUMNS:
            _insert(connection, view, cast_json=True)
