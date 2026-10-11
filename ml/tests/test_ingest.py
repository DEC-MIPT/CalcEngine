"""Ingestion: идемпотентность (нужен PostgreSQL)."""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import require_test_db_url

from normatives_pipeline import db
from normatives_pipeline.ingest import ingest

REPO = Path(__file__).resolve().parents[2]
DOC = REPO / "docs/normative-base" / "СП 31.13330.2021.pdf"
DESIGNATION = "СП 31.13330.2021"


@pytest.fixture(scope="module")
def conn():
    url = require_test_db_url()
    c = db.connect(url)
    db.init_schema(c)
    yield c
    c.close()


def test_ingest_missing_file() -> None:
    assert ingest(Path("no-such-file.pdf")) == 1


def test_ingest_without_designation_raises(monkeypatch) -> None:
    from normatives_pipeline import ingest as ingest_mod

    monkeypatch.setattr(ingest_mod.text_layer, "read_pages", lambda path: ["нет обозначения"])
    with pytest.raises(RuntimeError):
        ingest_mod.ingest(Path(__file__))


def test_ingest_without_edition_raises(monkeypatch) -> None:
    from normatives_pipeline import ingest as ingest_mod

    monkeypatch.setattr(ingest_mod.text_layer, "read_pages", lambda path: ["СП 22.13330"])
    with pytest.raises(RuntimeError):
        ingest_mod.ingest(Path(__file__))


def test_main_parses_force_and_path(monkeypatch) -> None:
    from normatives_pipeline import ingest as ingest_mod

    calls: dict = {}

    def fake_ingest(path: Path, force: bool = False) -> int:
        calls.update(path=path, force=force)
        return 0

    monkeypatch.setattr(ingest_mod, "ingest", fake_ingest)
    assert ingest_mod.main(["--force", "x.pdf"]) == 0
    assert calls == {"path": Path("x.pdf"), "force": True}
    assert ingest_mod.main([]) == 0
    assert calls["path"] == ingest_mod.DEFAULT_PILOT


def test_ingest_idempotent(conn) -> None:
    if not DOC.exists():
        pytest.skip(f"нет файла: {DOC}")

    db.delete_document(conn, DESIGNATION)
    assert ingest(DOC, force=False) == 0
    assert db.document_exists(conn, DESIGNATION)

    assert ingest(DOC, force=False) == 0  # skip path
    assert db.document_exists(conn, DESIGNATION)

    assert ingest(DOC, force=True) == 0  # force path re-ingests
    assert db.document_exists(conn, DESIGNATION)

    db.delete_document(conn, DESIGNATION)
    assert not db.document_exists(conn, DESIGNATION)


def test_ingest_manifest_formula_is_unverified_when_catalog_bound(conn) -> None:
    doc = REPO / "docs/normative-base" / "СП 22.13330.2016.pdf"
    if not doc.exists():
        pytest.skip(f"нет файла: {doc}")
    designation = "СП 22.13330.2016"
    db.delete_document(conn, designation)
    assert ingest(doc, force=False) == 0

    with conn.cursor() as cur:
        cur.execute(
            "SELECT f.status, f.provenance FROM formula f "
            "JOIN document d ON d.id = f.document_id "
            "WHERE d.designation = %s AND f.number = %s",
            (designation, "5.7"),
        )
        row = cur.fetchone()
    assert row == {"status": "unverified", "provenance": "machine-extracted"}

    db.delete_document(conn, designation)
