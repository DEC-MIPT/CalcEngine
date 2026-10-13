"""Аудит/миграция id обозначений: кириллица не должна коллидировать с латиницей."""

from __future__ import annotations

from typing import Self

from normatives_pipeline.parser import cyrillic


class _Cur:
    def __init__(self, store: list[dict]) -> None:
        self._store = store
        self._rows: list[dict] = []

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def execute(self, sql: str, params: tuple | None = None) -> None:
        if sql.strip().upper().startswith("SELECT"):
            self._rows = [dict(r) for r in self._store]
        elif sql.strip().upper().startswith("UPDATE"):
            new, rid = params  # type: ignore[misc]
            for r in self._store:
                if r["id"] == rid:
                    r["symbol"] = new

    def fetchall(self) -> list[dict]:
        return self._rows


class _Conn:
    def __init__(self, rows: list[dict]) -> None:
        self.store = rows

    def cursor(self) -> _Cur:
        return _Cur(self.store)

    def commit(self) -> None:
        pass

    def close(self) -> None:
        pass


def test_latex_has_cyrillic() -> None:
    assert cyrillic.latex_has_cyrillic("\\gamma_{\\text{с}}")
    assert not cyrillic.latex_has_cyrillic("\\gamma_{s}")


def test_disambiguate_id() -> None:
    assert cyrillic.disambiguate_id("s", "\\text{с}") == "s_cyr"
    assert cyrillic.disambiguate_id("s", "s") == "s"
    assert cyrillic.disambiguate_id("s_cyr", "\\text{с}") == "s_cyr"


def test_collisions() -> None:
    rows = [
        {"symbol": "s", "latex": "s"},
        {"symbol": "s", "latex": "\\text{с}"},
        {"symbol": "g", "latex": "g"},
    ]
    assert cyrillic.collisions(rows) == {"s": {"s", "\\text{с}"}}
    assert cyrillic.collisions([{"symbol": "g", "latex": "g"}]) == {}


def test_plan() -> None:
    rows = [
        {"id": 1, "symbol": "s", "latex": "s"},
        {"id": 2, "symbol": "s", "latex": "\\text{с}"},
    ]
    assert cyrillic.plan(rows) == [(2, "s_cyr", "s", "\\text{с}")]


def test_audit_and_fix_dry_run() -> None:
    conn = _Conn([{"id": 1, "symbol": "s", "latex": "\\text{с}"}])
    report = cyrillic.audit_and_fix(conn, apply=False)
    assert report["changes"] == 1
    assert report["applied"] is False
    assert conn.store[0]["symbol"] == "s"


def test_main_dry_run(monkeypatch, capsys) -> None:
    conn = _Conn(
        [
            {"id": 1, "symbol": "s", "latex": "s"},
            {"id": 2, "symbol": "s", "latex": "\\text{с}"},
        ]
    )
    monkeypatch.setattr(cyrillic.db, "connect", lambda: conn)
    assert cyrillic.main([]) == 0
    out = capsys.readouterr().out
    assert "коллизий до: 1" in out
    assert "правок: 1 (dry-run)" in out
    assert {r["symbol"] for r in conn.store} == {"s"}


def test_main_apply(monkeypatch, capsys) -> None:
    conn = _Conn(
        [
            {"id": 1, "symbol": "s", "latex": "s"},
            {"id": 2, "symbol": "s", "latex": "\\text{с}"},
        ]
    )
    monkeypatch.setattr(cyrillic.db, "connect", lambda: conn)
    assert cyrillic.main(["--apply"]) == 0
    out = capsys.readouterr().out
    assert "применено" in out
    assert "коллизий после: 0" in out


def test_audit_and_fix_applies_and_clears_collisions() -> None:
    conn = _Conn(
        [
            {"id": 1, "symbol": "s", "latex": "s"},
            {"id": 2, "symbol": "s", "latex": "\\text{с}"},
        ]
    )
    assert cyrillic.audit_and_fix(conn, apply=False)["before"] == {"s": {"s", "\\text{с}"}}
    report = cyrillic.audit_and_fix(conn, apply=True)
    assert report["applied"] is True
    assert report["after"] == {}
    assert {r["symbol"] for r in conn.store} == {"s", "s_cyr"}
