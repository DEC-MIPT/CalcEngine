"""Аудит и миграция id обозначений: устранение коллизий кириллица↔латиница.

Транслит `cyr_map` (а→a, с→s, е→e, р→r, у→u, к→k) отображает кириллические омографы в
те же id, что и латинские буквы, поэтому `notation_entry.symbol` перестаёт быть однозначным
(один id — несколько разных `latex`). Скрипт находит такие группы и при `--apply` делает id
однозначным, добавляя суффикс `_cyr` каждому обозначению, в котором есть кириллица. Само
`latex` не меняется, поэтому кириллица по-прежнему отображается через `\\text{…}`.

Запуск:

    DEC_DATABASE_URL=postgresql://dec:dec@localhost:5433/dec \
      python -m normatives_pipeline.parser.cyrillic            # только отчёт
    ... python -m normatives_pipeline.parser.cyrillic --apply  # исправить id в БД
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from typing import Any

from .. import db
from .symbols import CYR_SUFFIX

_CYR = re.compile(r"[\u0400-\u04ff]")


def latex_has_cyrillic(latex: str) -> bool:
    return bool(_CYR.search(latex))


def disambiguate_id(symbol_id: str, latex: str, suffix: str = CYR_SUFFIX) -> str:
    """Делает id однозначным относительно латиницы; идемпотентно."""
    if latex_has_cyrillic(latex) and not symbol_id.endswith(suffix):
        return symbol_id + suffix
    return symbol_id


def collisions(rows: list[dict]) -> dict[str, set[str]]:
    """id → множество разных latex (>1 значит коллизия)."""
    groups: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        groups[row["symbol"]].add(row["latex"])
    return {sym: latexes for sym, latexes in groups.items() if len(latexes) > 1}


def plan(rows: list[dict]) -> list[tuple[int, str, str, str]]:
    """Список правок (id строки, новый symbol, старый symbol, latex)."""
    changes: list[tuple[int, str, str, str]] = []
    for row in rows:
        new = disambiguate_id(row["symbol"], row["latex"])
        if new != row["symbol"]:
            changes.append((row["id"], new, row["symbol"], row["latex"]))
    return changes


def _fetch(conn: Any) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, symbol, latex FROM notation_entry ORDER BY id"
        )
        return [dict(r) for r in cur.fetchall()]


def _apply(conn: Any, changes: list[tuple[int, str, str, str]]) -> None:
    with conn.cursor() as cur:
        for row_id, new, _old, _latex in changes:
            cur.execute(
                "UPDATE notation_entry SET symbol = %s WHERE id = %s", (new, row_id)
            )
    conn.commit()


def audit_and_fix(conn: Any, apply: bool = False) -> dict:
    rows = _fetch(conn)
    before = collisions(rows)
    changes = plan(rows)
    if apply and changes:
        _apply(conn, changes)
        rows = _fetch(conn)
    after = collisions(rows)
    return {
        "rows": len(rows),
        "changes": len(changes),
        "before": before,
        "after": after,
        "applied": bool(apply and changes),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="записать правки в БД")
    args = parser.parse_args(argv)

    conn = db.connect()
    try:
        report = audit_and_fix(conn, apply=args.apply)
    finally:
        conn.close()

    print(f"строк обозначений: {report['rows']}")
    print(f"коллизий до: {len(report['before'])}")
    for sym, latexes in sorted(report["before"].items(), key=lambda kv: -len(kv[1])):
        print(f"  {sym!r} -> {sorted(latexes)}")
    print(f"правок: {report['changes']}" + (" (применено)" if report["applied"] else " (dry-run)"))
    print(f"коллизий после: {len(report['after'])}")
    for sym, latexes in report["after"].items():
        print(f"  остаётся {sym!r} -> {sorted(latexes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
