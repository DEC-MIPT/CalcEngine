"""Синтетические данные временного источника для тестов: синтетика, не норматив.

Ссылки, обозначения и значения — заглушки ``catalog_fixture``; ни одно из них не взято из
нормы (``agent-docs/domain-constraints.md``).
"""

from datetime import date
from pathlib import Path
from typing import Any

import yaml
from catalog_fixture import PLACEHOLDER_DOCUMENTS, PLACEHOLDER_EDITION, REFS, ROWS

from app.parameters.interim_schemas import (
    InterimCheck,
    InterimFormula,
    InterimManifest,
    InterimMethodBound,
    InterimTableValue,
    InterimThreshold,
)
from app.services.interim_data import record_digest, sunset_passed

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


def assert_before_sunset(path: Path, today: date) -> None:
    """Напоминание о сроке временного источника (design.md, решение 8).

    Тест реального манифеста (задача 7.1) вызывает его с сегодняшней датой и падает после
    даты отключения, пока дату не продлят коммитом или данные не удалят.

    Args:
        path: путь ``manifest.yaml``.
        today: сегодняшняя дата.
    """
    found = InterimManifest.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    assert not sunset_passed(found, today), (
        f"the interim source of {found.document} passed its sunset {found.sunset.date.isoformat()}: "
        f"extend the date by a commit or remove the data ({found.sunset.event})"
    )


KINDS: dict[str, tuple[str, type[InterimFormula | InterimTableValue | InterimThreshold | InterimCheck | InterimMethodBound]]] = {
    "type_formulas": ("formulas", InterimFormula),
    "type_table_values": ("table_values", InterimTableValue),
    "type_thresholds": ("thresholds", InterimThreshold),
    "type_checks": ("checks", InterimCheck),
    "type_method_bounds": ("method_bounds", InterimMethodBound),
}
"""Представление каталога → список файла типа и модель его записи."""


def verified(record: dict[str, Any], list_name: str) -> dict[str, Any]:
    """Запись, какой её оставил бы верификатор: с ``value_digest`` её текущего значения."""
    model = next(model for name, model in KINDS.values() if name == list_name)
    digest = record_digest(model.model_validate(record))
    return record | {
        "verification": {"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "portion": "P1", "value_digest": digest}
    }


def rejected(record: dict[str, Any]) -> dict[str, Any]:
    return record | {"verification": {"status": "rejected", "by": VERIFIER, "at": "2026-10-21", "comment": "<REASON>"}}


def from_catalog(calculation_type: str, rows: Any = ROWS, checked: bool = True) -> dict[str, Any]:
    """Файл типа с теми же данными, что строки каталога этого типа в ``catalog_fixture``.

    Args:
        calculation_type: тип расчёта.
        rows: строки представлений каталога.
        checked: ``True`` — каждая запись ``human-verified``, иначе ``pending``.

    Returns:
        Содержимое файла типа.
    """
    lists: dict[str, list[dict[str, Any]]] = {}
    for view, (name, _) in KINDS.items():
        records = [
            {key: value for key, value in row.items() if key != "calculation_type"} | {"page": 1, "verification": PENDING}
            for row in rows[view]
            if row["calculation_type"] == calculation_type
        ]
        lists[name] = [verified(record, name) for record in records] if checked else records
    return type_file(**lists)
