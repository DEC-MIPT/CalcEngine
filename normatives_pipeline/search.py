"""CLI поиска по готовому хранилищу: лемматизируется только строка запроса."""

from __future__ import annotations

import json
import sys

from . import db
from .retrieval import normalize_text


def query(query: str, k: int = 5) -> dict:
    lemmas = normalize_text(query)
    tokens = lemmas.split()
    if not tokens:
        return {"query": query, "lemmas": "", "formulas": [], "clauses": []}

    conn = db.connect()
    try:
        db.init_schema(conn)
        formulas = db.search_formulas(conn, lemmas, k=k)
        clauses = db.search_clauses(conn, lemmas, k=k)
        payloads = [db.build_formula_payload(conn, f) for f in formulas]
        return {
            "query": query,
            "lemmas": lemmas,
            "formulas": payloads,
            "clauses": clauses,
        }
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    json_out = "--json" in args
    args = [a for a in args if a != "--json"]
    if not args:
        print('использование: python -m normatives_pipeline.search ["--json"] "<запрос>"')
        return 1
    query_text = " ".join(args)

    result = query(query_text)

    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"[запрос] {result['query']}")
    print(f"[леммы] {result['lemmas']}\n")

    print("=== Формулы ===")
    for f in result["formulas"]:
        nr = f["norm_ref"]
        clause = nr["clause"] or "—"
        print(
            f"  {nr['designation']} формула {nr['formula']} (пункт {clause})"
        )
        for s in f["symbols"]:
            print(f"       {s['latex']} — {s['meaning']}")
        for r in f["cross_refs"]:
            print(f"       ref: {r['ref_type']} {r['ref_value']}")

    print("\n=== Пункты ===")
    for c in result["clauses"]:
        print(f"  {c['rank']:.3f}  {c['designation']} {c['number']} {c['title'][:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
