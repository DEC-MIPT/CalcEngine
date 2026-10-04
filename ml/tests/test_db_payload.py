"""Контракт формулы и коэффициента: payload, NormRef, хранение статуса (нужен PostgreSQL)."""

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
    doc_id = db.upsert_document(conn, designation, title="test", edition="2016")
    db.insert_formulas(
        conn,
        doc_id,
        [("5.1", "5.3", "x = y", "x*y", "raw", 1, "формула 5.1 тест", "verified", "human-verified")],
    )
    db.insert_notation(conn, doc_id, [("5.1", "gamma_c1", "\\gamma_{c1}", "коэффициент", "", "input")])
    db.insert_cross_refs(conn, doc_id, [("5.3", "gost", "ГОСТ 20522", "")])

    formula = {
        "document_id": doc_id,
        "designation": designation,
        "number": "5.1",
        "clause_number": "5.3",
        "latex": "x = y",
        "expression": "x*y",
        "edition": "2016",
        "status": "verified",
        "provenance": "human-verified",
    }
    payload = db.build_formula_payload(conn, formula)

    assert list(payload.keys()) == output_config()["formula_keys"]
    assert payload["norm_ref"] == {
        "document": designation,
        "edition": "2016",
        "clause": "форм. (5.1)",
        "status": "verified",
        "provenance": "human-verified",
    }
    assert payload["formula_id"] == "5.1"
    assert payload["symbols"][0]["id"] == "gamma_c1"
    assert payload["symbols"][0]["latex"] == "\\gamma_{c1}"
    assert payload["symbols"][0]["kind"] == "input"
    assert payload["expression"] == "x*y"
    assert payload["cross_refs"][0]["ref_value"] == "ГОСТ 20522"

    db.delete_document(conn, designation)


def test_formula_status_provenance_roundtrip(conn) -> None:
    designation = "TEST-СТАТУС"
    db.delete_document(conn, designation)
    doc_id = db.upsert_document(conn, designation, title="test")
    db.insert_formulas(
        conn,
        doc_id,
        [("5.1", "5.3", "x = y", "x*y", "raw", 1, "формула 5.1 тест", "verified", "human-verified")],
    )
    rows = db.fetch_formulas(conn, doc_id)
    assert len(rows) == 1
    assert rows[0]["status"] == "verified"
    assert rows[0]["provenance"] == "human-verified"

    db.delete_document(conn, designation)


def test_build_formula_payload_missing_document_raises(conn) -> None:
    formula = {
        "document_id": 1,
        "designation": "",
        "number": "5.1",
        "clause_number": "5.3",
    }
    with pytest.raises(RuntimeError):
        db.build_formula_payload(conn, formula)


def test_query_returns_structure(conn) -> None:
    result = query("нагрузка")
    assert set(result) == {"query", "lemmas", "formulas", "clauses"}
    assert isinstance(result["formulas"], list)
    assert isinstance(result["clauses"], list)


def test_coefficients_roundtrip(conn) -> None:
    designation = "TEST-КОЭФФ"
    db.delete_document(conn, designation)
    doc_id = db.upsert_document(conn, designation, title="test")
    db.insert_coefficients(
        conn,
        doc_id,
        [("5.5", 42, 2, 1, "0,01", "unverified", "табл. 5.5", "unverified", "machine-extracted")],
    )

    rows = db.fetch_coefficients(conn, doc_id, "5.5")
    assert len(rows) == 1
    assert rows[0]["designation"] == designation
    assert rows[0]["table_number"] == "5.5"
    assert rows[0]["page"] == 42
    assert rows[0]["row_index"] == 2
    assert rows[0]["col_index"] == 1
    assert rows[0]["value"] == "0,01"
    assert rows[0]["edition"] == "unverified"
    assert rows[0]["clause"] == "табл. 5.5"
    assert rows[0]["status"] == "unverified"
    assert rows[0]["provenance"] == "machine-extracted"

    norm_ref = db.build_coefficient_norm_ref(rows[0])
    assert norm_ref == {
        "document": designation,
        "edition": "unverified",
        "clause": "табл. 5.5",
        "status": "unverified",
        "provenance": "machine-extracted",
    }

    payload = db.build_coefficient_payload(rows[0])
    assert payload == {
        "table_number": "5.5",
        "page": 42,
        "row_index": 2,
        "col_index": 1,
        "value": "0,01",
        "norm_ref": norm_ref,
    }

    db.delete_document(conn, designation)


def test_build_coefficient_norm_ref_missing_document_raises() -> None:
    with pytest.raises(RuntimeError):
        db.build_coefficient_norm_ref({"designation": ""})


def test_update_formula_latex_expression(conn) -> None:
    designation = "TEST-ОБНОВЛЕНИЕ"
    db.delete_document(conn, designation)
    doc_id = db.upsert_document(conn, designation, title="test")
    db.insert_formulas(
        conn,
        doc_id,
        [("5.1", "5.3", "old", "old", "raw", 1, "s", "unverified", "machine-extracted")],
    )
    formula_id = db.fetch_formulas(conn, doc_id)[0]["id"]
    db.update_formula(conn, formula_id, "x = y", "x*y")
    with conn.cursor() as cur:
        cur.execute("SELECT latex, expression FROM formula WHERE id = %s", (formula_id,))
        row = cur.fetchone()
    assert row is not None
    assert row["latex"] == "x = y"
    assert row["expression"] == "x*y"
    db.delete_document(conn, designation)
