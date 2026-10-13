"""Тесты `formulas/enrich.py`: enrichment CLI и граничные случаи без ML."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from normatives_pipeline.formulas import enrich as enrich_mod


def test_enrich_missing_file(tmp_path) -> None:
    assert enrich_mod.enrich(tmp_path / "nope.pdf") == 1


def test_enrich_document_not_in_db(monkeypatch, tmp_path) -> None:
    p = tmp_path / "ТЕСТ.pdf"
    p.write_bytes(b"x")
    conn = MagicMock()
    conn.cursor.return_value.__enter__.return_value.fetchone.return_value = None
    monkeypatch.setattr(enrich_mod.db, "connect", lambda: conn)
    assert enrich_mod.enrich(p) == 1


def test_main_uses_default_pilot_without_args(monkeypatch) -> None:
    called: dict = {}
    monkeypatch.setattr(enrich_mod, "enrich", lambda p: called.update(p=p) or 0)
    enrich_mod.main([])
    assert called["p"] == enrich_mod.DEFAULT_PILOT


def test_main_uses_given_path(monkeypatch, tmp_path) -> None:
    p = tmp_path / "test.pdf"
    called: dict = {}
    monkeypatch.setattr(enrich_mod, "enrich", lambda path: called.update(p=path) or 0)
    enrich_mod.main([str(p)])
    assert called["p"] == p


def test_enrich_document_found_builds_by_page(monkeypatch, tmp_path) -> None:
    """Строки 33-38: doc найден, by_page строится; detect_config прерывает (no cover ≥ line 40)."""
    p = tmp_path / "СП22.pdf"
    p.write_bytes(b"x")

    conn = MagicMock()
    conn.cursor.return_value.__enter__.return_value.fetchone.return_value = {"id": 1}

    monkeypatch.setattr(enrich_mod.db, "connect", lambda: conn)
    monkeypatch.setattr(
        enrich_mod.db,
        "fetch_formulas",
        lambda *_: [{"page": 1, "id": 10}, {"page": 2, "id": 11}],
    )
    monkeypatch.setattr(
        enrich_mod, "detect_config", MagicMock(side_effect=RuntimeError("stop-here"))
    )

    with pytest.raises(RuntimeError, match="stop-here"):
        enrich_mod.enrich(p)
