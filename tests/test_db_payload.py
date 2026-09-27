"""Контракт формулы: build_formula_payload и query (нужен PostgreSQL)."""

from __future__ import annotations

import pytest

from normatives_pipeline import db
from normatives_pipeline.config import output_config
from normatives_pipeline.search import query


@pytest.fixture(scope="module")
def conn():
    try:
        c = db.connect()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"нет БД: {exc}")
    db.init_schema(c)
    yield c
    c.close()


def test_build_formula_payload_shape(conn) -> None:
    designation = "TEST-ПАЙЛОАД"
    db.delete_document(conn, designation)
    doc_id = db.upsert_document(conn, designation, title="test")
    db.insert_formulas(conn, doc_id, [("5.1", "5.3", "x = y", "x*y", "raw", 1, "формула 5.1 тест")])
    db.insert_notation(conn, doc_id, [("5.1", "gamma_c1", "\\gamma_{c1}", "коэффициент", "", "input")])
    db.insert_cross_refs(conn, doc_id, [("5.3", "gost", "ГОСТ 20522", "")])

    formula = {
        "document_id": doc_id,
        "designation": designation,
        "number": "5.1",
        "clause_number": "5.3",
        "latex": "x = y",
        "expression": "x*y",
    }
    payload = db.build_formula_payload(conn, formula)

    assert list(payload.keys()) == output_config()["formula_keys"]
    assert payload["norm_ref"] == {
        "document": designation,
        "edition": "unverified",
        "clause": "форм. (5.1)",
        "status": "unverified",
        "provenance": "machine-extracted",
    }
    assert payload["formula_id"] == "5.1"
    assert payload["symbols"][0]["id"] == "gamma_c1"
    assert payload["symbols"][0]["latex"] == "\\gamma_{c1}"
    assert payload["symbols"][0]["kind"] == "input"
    assert payload["expression"] == "x*y"
    assert payload["cross_refs"][0]["ref_value"] == "ГОСТ 20522"

    db.delete_document(conn, designation)


def test_query_returns_structure(conn) -> None:
    result = query("нагрузка")
    assert set(result) == {"query", "lemmas", "formulas", "clauses"}
    assert isinstance(result["formulas"], list)
    assert isinstance(result["clauses"], list)


def test_coefficients_roundtrip(conn) -> None:
    designation = "TEST-КОЭФФ"
    db.delete_document(conn, designation)
    doc_id = db.upsert_document(conn, designation, title="test")
    db.insert_coefficients(conn, doc_id, [("5.5", 42, 2, 1, "0,01")])

    rows = db.fetch_coefficients(conn, doc_id, "5.5")
    assert len(rows) == 1
    assert rows[0]["table_number"] == "5.5"
    assert rows[0]["page"] == 42
    assert rows[0]["row_index"] == 2
    assert rows[0]["col_index"] == 1
    assert rows[0]["value"] == "0,01"

    db.delete_document(conn, designation)
