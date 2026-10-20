"""Синтетические данные временного источника для тестов: синтетика, не норматив.

Ссылки, обозначения и значения — заглушки ``catalog_fixture``; ни одно из них не взято из
нормы (``agent-docs/domain-constraints.md``).
"""

from pathlib import Path
from typing import Any

import yaml
from catalog_fixture import PLACEHOLDER_DOCUMENTS, PLACEHOLDER_EDITION, REFS

VERIFIER = "<VERIFIER>"
PENDING: dict[str, Any] = {"status": "pending"}


def manifest(**changes: Any) -> dict[str, Any]:
    return {
        "document": PLACEHOLDER_DOCUMENTS[0],
        "edition": PLACEHOLDER_EDITION,
        "sunset": {"date": "2099-12-31", "event": "<SUNSET-EVENT>"},
        "verifiers": [VERIFIER],
    } | changes


def formula(parameter: str = "x", **changes: Any) -> dict[str, Any]:
    return {
        "parameter": parameter,
        "result_symbol": "x",
        "latex": "x = 2",
        "tree": {"kind": "number", "value": 2.0},
        "units": {"x": "1"},
        "norm_refs": REFS,
        "page": 1,
        "verification": PENDING,
    } | changes


def table_value(parameter: str = "a", **changes: Any) -> dict[str, Any]:
    return {
        "parameter": parameter,
        "symbol": parameter,
        "latex": parameter,
        "value": 1.0,
        "unit": "1",
        "norm_refs": REFS,
        "page": 1,
        "verification": PENDING,
    } | changes


def type_file(**lists: Any) -> dict[str, Any]:
    return {"formulas": [], "table_values": [], "thresholds": [], "checks": [], "method_bounds": []} | lists


def write(path: Path, data: object) -> Path:
    """Пишет данные YAML-файлом, создавая каталоги."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path
