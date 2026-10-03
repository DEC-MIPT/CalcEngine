"""Ingestion: идемпотентность (нужен PostgreSQL)."""

from __future__ import annotations

from pathlib import Path

import pytest

from normatives_pipeline import db
from normatives_pipeline.ingest import ingest

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs/normative-base" / "СП 31.13330.2021.pdf"
DESIGNATION = "СП 31.13330.2021"


@pytest.fixture(scope="module")
def conn():
    try:
        c = db.connect()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"нет БД: {exc}")
    db.init_schema(c)
    yield c
    c.close()


def test_ingest_idempotent(conn) -> None:
    if not DOC.exists():
        pytest.skip(f"нет файла: {DOC}")

    db.delete_document(conn, DESIGNATION)
    assert ingest(DOC, force=False) == 0
    assert db.document_exists(conn, DESIGNATION)

    assert ingest(DOC, force=False) == 0  # skip path
    assert db.document_exists(conn, DESIGNATION)

    db.delete_document(conn, DESIGNATION)
    assert not db.document_exists(conn, DESIGNATION)
