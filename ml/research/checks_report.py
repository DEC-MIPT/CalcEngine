r"""Подсчёт ручных отметок «OK» из HTML-обзора (`verify_corpus.py --include-missed`).

Обзор пишет чекбоксы с id ``<страница>:<номер>``; кнопка «Скачать отметки» сохраняет
``<имя>_checks.json`` вида ``{file, total, ok: [...], not_ok: [...]}``. Этот скрипт
читает такие отметки и рядом лежащий ``<имя>.json`` (записи обзора), чтобы отделить
непроверенные **извлечённые формулы** от непроверенных **«не извлечено»**: именно
непроверенное — очередь на улучшение.

Запуск:

    python research/checks_report.py research/human-views/sp22_checks.json
    # --review по умолчанию: <имя>.json рядом (sp22_checks.json -> sp22.json)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _id(rec: dict) -> str:
    return f"{rec['page']}:{rec['number']}"


def report(checks_path: Path, review_path: Path | None) -> dict:
    checks = json.loads(checks_path.read_text(encoding="utf-8"))
    ok = set(checks.get("ok", []))
    review = None
    if review_path and review_path.exists():
        review = json.loads(review_path.read_text(encoding="utf-8"))
    recs = review.get("records", []) if review else []
    missed = {_id(r) for r in (review.get("missed", []) if review else [])}
    formulas = {_id(r) for r in recs}
    all_ids = ok | set(checks.get("not_ok", []))
    if recs:
        all_ids |= formulas | missed

    not_ok = sorted(all_ids - ok)
    result = {
        "checks": str(checks_path.name),
        "total": len(all_ids),
        "ok": len(ok & all_ids),
        "not_ok": len(not_ok),
        "not_ok_formulas": [i for i in not_ok if i in formulas] if recs else None,
        "not_ok_missed": [i for i in not_ok if i in missed] if recs else None,
        "ok_but_missed": [i for i in sorted(ok) if i in missed] if recs else None,
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("checks", type=Path)
    ap.add_argument("--review", type=Path, default=None)
    args = ap.parse_args()
    review = args.review or args.checks.with_name(
        args.checks.name.replace("_checks.json", ".json"))
    res = report(args.checks, review)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if res["not_ok_formulas"] is not None:
        print(f"\nНепроверенных извлечённых формул: {len(res['not_ok_formulas'])} — это очередь правок.")
        print(f"Непроверенных «не извлечено»: {len(res['not_ok_missed'])} — подтвердить, что это не формулы.")
        print(f"Отмечено OK, но помечено «не извлечено»: {len(res['ok_but_missed'])} "
              f"(ожидается 0 — иначе отметка противоречит обзору).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
