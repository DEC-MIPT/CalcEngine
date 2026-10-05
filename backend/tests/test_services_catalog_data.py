import json
import logging
from collections.abc import Iterator
from typing import Any

import pytest
from catalog_fixture import PILOT, REFS
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, func, select, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import R_UNITS, inputs
from test_services_catalog_source import make_source, registry, with_phi

from app.core.exceptions import ParameterSourceUnavailableError
from app.main import create_app
from app.models import Base
from app.models.calculation_result import CalculationResultRow

TYPE = f"calculation_type = '{PILOT}'"
REF_JSON = json.dumps(REFS)
VERIFIED_JSON = json.dumps([{**REFS[0], "status": "verified"}])
R_IN_MPA = json.dumps({**R_UNITS, "R": "MPa"})

BREACHES: list[tuple[str, list[str], str | None]] = [
    ("missing parameter", [f"DELETE FROM catalog_read.type_thresholds WHERE {TYPE}"], "k_z_threshold"),
    (
        "undeclared parameter",
        [f"INSERT INTO catalog_read.type_checks VALUES ('{PILOT}', 'extra_check', '{REF_JSON}')"],
        "extra_check",
    ),
    (
        "parameter in two views",
        [f"INSERT INTO catalog_read.type_checks VALUES ('{PILOT}', 'k_z_threshold', '{REF_JSON}')"],
        "k_z_threshold",
    ),
    (
        "parameter in the wrong view",
        [
            f"DELETE FROM catalog_read.type_checks WHERE {TYPE}",
            f"INSERT INTO catalog_read.type_thresholds VALUES ('{PILOT}', 'check_norm_refs', 'c', 1.0, 'm', '{REF_JSON}')",
        ],
        "check_norm_refs",
    ),
    (
        "parameter twice in one view",
        [
            f"INSERT INTO catalog_read.type_formulas SELECT * FROM catalog_read.type_formulas WHERE {TYPE} AND parameter = 'k_z_below'"
        ],
        "k_z_below",
    ),
    (
        "unparsable tree",
        [f"UPDATE catalog_read.type_formulas SET tree = '{{\"kind\": \"modulo\"}}' WHERE {TYPE} AND parameter = 'r'"],
        "r",
    ),
    (
        "symbol without a unit",
        [f"UPDATE catalog_read.type_formulas SET units = '{{\"k_z\": \"1\"}}' WHERE {TYPE} AND parameter = 'k_z_from'"],
        "k_z_from",
    ),
    (
        "input symbol in another unit of its dimension",
        [
            f"UPDATE catalog_read.type_formulas SET units = '{{\"b\": \"mm\", \"k_z\": \"1\"}}' WHERE {TYPE} AND parameter = 'k_z_from'"
        ],
        "k_z_from",
    ),
    (
        "input symbol in a unit of another dimension",
        [
            f"UPDATE catalog_read.type_formulas SET units = '{{\"b\": \"kPa\", \"k_z\": \"1\"}}' WHERE {TYPE} AND parameter = 'k_z_from'"
        ],
        "k_z_from",
    ),
    (
        "output result symbol in another unit",
        [f"UPDATE catalog_read.type_formulas SET units = '{R_IN_MPA}' WHERE {TYPE} AND parameter = 'r'"],
        "r",
    ),
    (
        "unit outside the list",
        [f"UPDATE catalog_read.type_thresholds SET unit = 'furlong' WHERE {TYPE}"],
        "k_z_threshold",
    ),
    (
        "value that is not a finite number",
        [f"UPDATE catalog_read.type_table_values SET value = 1e999 WHERE {TYPE} AND parameter = 'gamma_c1'"],
        "gamma_c1",
    ),
    ("empty norm_refs", [f"UPDATE catalog_read.type_checks SET norm_refs = '[]' WHERE {TYPE}"], "check_norm_refs"),
    (
        "machine-extracted reference marked verified",
        [f"UPDATE catalog_read.type_formulas SET norm_refs = '{VERIFIED_JSON}' WHERE {TYPE} AND parameter = 'k_z_below'"],
        "k_z_below",
    ),
    (
        "duplicate headings",
        [
            f"UPDATE catalog_read.type_table_values SET heading_value = 20 WHERE {TYPE} AND parameter = 'm_q' AND heading_value = 30"
        ],
        "m_q",
    ),
    (
        "rows with and without a heading",
        [
            f"UPDATE catalog_read.type_table_values SET heading_symbol = NULL, heading_value = NULL, heading_unit = NULL WHERE {TYPE} AND parameter = 'm_gamma' AND heading_value = 10"
        ],
        "m_gamma",
    ),
    (
        "two rows without a heading",
        [
            f"INSERT INTO catalog_read.type_table_values SELECT * FROM catalog_read.type_table_values WHERE {TYPE} AND parameter = 'gamma_c1'"
        ],
        "gamma_c1",
    ),
    (
        "two heading symbols in one parameter",
        [
            f"UPDATE catalog_read.type_table_values SET heading_symbol = 'b' WHERE {TYPE} AND parameter = 'm_c' AND heading_value = 30"
        ],
        "m_c",
    ),
    (
        "heading symbol that names no input",
        [f"UPDATE catalog_read.type_table_values SET heading_symbol = 'psi' WHERE {TYPE} AND parameter = 'm_c'"],
        "m_c",
    ),
    (
        "heading unit outside the list",
        [
            f"UPDATE catalog_read.type_table_values SET heading_unit = 'grad' WHERE {TYPE} AND parameter = 'm_q' AND heading_value = 10"
        ],
        "m_q",
    ),
    (
        "heading unit of another dimension",
        [
            f"UPDATE catalog_read.type_table_values SET heading_unit = 'm' WHERE {TYPE} AND parameter = 'm_q' AND heading_value = 10"
        ],
        "m_q",
    ),
    (
        "heading whose conversion overflows",
        [
            f"UPDATE catalog_read.type_table_values SET heading_value = 1e308, heading_unit = 'rad' WHERE {TYPE} AND parameter = 'm_q' AND heading_value = 10"
        ],
        "m_q",
    ),
    (
        "bound whose quantity is not an input",
        [f"UPDATE catalog_read.type_method_bounds SET quantity = 'psi' WHERE {TYPE} AND quantity = 'b' AND kind = 'min'"],
        None,
    ),
    (
        "bound of another dimension",
        [f"UPDATE catalog_read.type_method_bounds SET unit = 'kPa' WHERE {TYPE} AND quantity = 'b' AND kind = 'min'"],
        None,
    ),
    (
        "two bounds of one kind on one quantity",
        [
            f"INSERT INTO catalog_read.type_method_bounds SELECT * FROM catalog_read.type_method_bounds WHERE {TYPE} AND quantity = 'b' AND kind = 'min'"
        ],
        None,
    ),
    (
        "empty range",
        [f"UPDATE catalog_read.type_method_bounds SET value = 50 WHERE {TYPE} AND quantity = 'b' AND kind = 'min'"],
        None,
    ),
    (
        "no binding for the type",
        [
            f"DELETE FROM catalog_read.{view} WHERE {TYPE}"
            for view in ("type_formulas", "type_table_values", "type_thresholds", "type_checks", "type_method_bounds")
        ],
        None,
    ),
]
"""Нарушение → SQL, который портит фикстуру, и параметр, который называет строка лога."""


def spoil(engine: Engine, statements: list[str]) -> None:
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def lines(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.name == "app.services.catalog_source"]


def expected_line(parameter: str | None) -> str:
    named = "" if parameter is None else f" parameter={parameter}"
    return f"code=catalog_data_invalid type={PILOT}{named}"


@pytest.mark.parametrize(
    ("statements", "parameter"),
    [pytest.param(statements, parameter, id=name) for name, statements, parameter in BREACHES],
)
@pytest.mark.parametrize("phi", [20.0, 40.0], ids=["on a row", "outside the range"])
def test_a_breach_makes_the_type_unavailable_with_one_log_line(
    catalog_sqlite: Engine,
    caplog: pytest.LogCaptureFixture,
    statements: list[str],
    parameter: str | None,
    phi: float,
) -> None:
    spoil(catalog_sqlite, statements)

    with caplog.at_level(logging.INFO), pytest.raises(ParameterSourceUnavailableError) as exc_info:
        make_source(catalog_sqlite).resolve(PILOT, with_phi(phi))

    assert str(exc_info.value) == f"The catalog data of the calculation type '{PILOT}' are not usable."
    assert exc_info.value.__cause__ is None and exc_info.value.__suppress_context__
    assert lines(caplog) == [expected_line(parameter)]


def test_every_breach_listed_in_tasks_5_4_and_5_6_has_a_case() -> None:
    assert len(BREACHES) == len({name for name, _, _ in BREACHES}) == 27


@pytest.fixture
def client(catalog_sqlite: Engine, monkeypatch: pytest.MonkeyPatch) -> Iterator[tuple[TestClient, Engine]]:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    results = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(results)
    app = create_app(
        registry=registry(),
        sources={PILOT: make_source(catalog_sqlite)},
        validated_ranges={PILOT: ()},
        session_factory=sessionmaker(bind=results),
    )
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client, results
    results.dispose()


def test_a_breach_answers_503_naming_the_type_and_stores_nothing(
    catalog_sqlite: Engine, client: tuple[TestClient, Engine], caplog: pytest.LogCaptureFixture
) -> None:
    test_client, results = client
    spoil(catalog_sqlite, [f"UPDATE catalog_read.type_thresholds SET value = 1e999 WHERE {TYPE}"])
    given: dict[str, Any] = {name: value.model_dump() for name, value in inputs().items()}

    with caplog.at_level(logging.INFO):
        response = test_client.post("/calculations", json={"calculation_type": PILOT, "inputs": given})

    body = response.json()
    assert (response.status_code, body["code"]) == (503, "parameter_source_unavailable")
    assert PILOT in body["message"] and "inf" not in response.text.lower()
    assert lines(caplog) == [expected_line("k_z_threshold")]
    assert not any("inf" in message.lower() for message in (record.getMessage() for record in caplog.records))
    with Session(results) as session:
        assert session.scalar(select(func.count()).select_from(CalculationResultRow)) == 0
