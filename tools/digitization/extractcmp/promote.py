"""Перенос вердиктов верификатора в данные: единственное место, где ставится ``human-verified``."""

import copy
import hashlib
import json
import math
import subprocess
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
from typing import Any

from extractcmp.portions import VERDICTS

APPROVED, FIX, REJECT = VERDICTS
HUMAN_VERIFIED = "human-verified"
LISTS = ("formulas", "table_values", "thresholds", "checks", "method_bounds")


def _normalized(data: Any) -> Any:
    if isinstance(data, bool) or data is None or isinstance(data, str):
        return data
    if isinstance(data, (int, float)):
        number = float(data)
        if not math.isfinite(number):
            raise ValueError("a non-finite number cannot be hashed")
        return number
    if isinstance(data, (list, tuple)):
        return [_normalized(v) for v in data]
    if isinstance(data, Mapping):
        return {str(k): _normalized(v) for k, v in data.items()}
    raise ValueError(f"{type(data).__name__} cannot be hashed")


def canonical_json(data: Any) -> str:
    """Сериализует данные так же, как ``canonical_json`` бэкенда.

    Ключи отсортированы, пробелов нет, все числа ``float``, не-ASCII не экранируется.

    Args:
        data: словари, списки, строки, числа, ``bool`` и ``None``.

    Raises:
        ValueError: если есть не конечное число или неподдерживаемый тип.
    """
    return json.dumps(_normalized(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def record_digest(record: Mapping[str, Any]) -> str:
    """Считает SHA-256 записи без её ``verification`` (design.md, решение 3).

    Args:
        record: запись каталога.

    Returns:
        Шестнадцатеричная строка из 64 символов.
    """
    body = {k: v for k, v in record.items() if k != "verification"}
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


def sheet_digest(sheet: Mapping[str, Any]) -> str:
    """Считает SHA-256 содержимого листа без подписи.

    Args:
        sheet: лист проверки порции.
    """
    body = {k: v for k, v in sheet.items() if k != "signature"}
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


def sign_sheet(sheet: Mapping[str, Any], by: str, at: date) -> dict[str, Any]:
    """Добавляет подпись верификатора в лист.

    Подпись фиксирует содержимое листа: любая правка после неё делает подпись
    недействительной. Это не защита от того, кто выполнил команду; кто подписал, проверяют
    список ``verifiers`` и автор коммита (``check_committed``).

    Args:
        sheet: заполненный лист.
        by: имя верификатора.
        at: дата подписи.

    Returns:
        Копия листа с блоком ``signature``.
    """
    signed = copy.deepcopy(dict(sheet))
    signed["signature"] = {"by": by, "at": at.isoformat(), "digest": sheet_digest(signed)}
    return signed


def check_sheet(sheet: Mapping[str, Any], verifiers: Sequence[str]) -> list[str]:
    """Проверяет лист и подпись.

    Args:
        sheet: лист проверки порции.
        verifiers: имена из ``verifiers`` манифеста.

    Returns:
        Список ошибок; пустой, если подписанному листу можно доверять.
    """
    signature = sheet.get("signature")
    if not isinstance(signature, Mapping):
        return ["the sheet is not signed"]
    errors = []
    if signature.get("by") not in verifiers:
        errors.append(f"the signer {signature.get('by')!r} is not in verifiers")
    if signature.get("digest") != sheet_digest(sheet):
        errors.append("the sheet changed after it was signed")
    try:
        date.fromisoformat(str(signature.get("at")))
    except ValueError:
        errors.append("the signature date is not a date")
    for item in sheet.get("items", []):
        if item.get("verdict") is None:
            continue
        name = item.get("item")
        if item["verdict"] not in VERDICTS:
            errors.append(f"{name}: the verdict {item['verdict']!r} is not allowed")
        if item.get("by") != signature.get("by"):
            errors.append(f"{name}: the item is not by the signer")
        try:
            date.fromisoformat(str(item.get("at")))
        except ValueError:
            errors.append(f"{name}: no date")
        if item["verdict"] == REJECT and not item.get("comment"):
            errors.append(f"{name}: a rejection needs a comment")
        if item["verdict"] == FIX and not isinstance(item.get("corrected"), Mapping):
            errors.append(f"{name}: a correction needs the corrected fields as a mapping")
    return errors


def check_committed(path: Path, by: str) -> list[str]:
    """Проверяет, что лист закоммичен и последний коммит сделан подписавшим.

    Args:
        path: путь к листу.
        by: имя верификатора из подписи.

    Returns:
        Список ошибок; пустой, если лист чист и автор последнего коммита равен ``by``.
    """
    cwd = path.resolve().parent

    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        return ["the sheet is not in a git working tree"]
    if git("status", "--porcelain", "--", path.name).stdout.strip():
        return ["the sheet has uncommitted changes or is untracked"]
    author = git("log", "-1", "--format=%an", "--", path.name).stdout.strip()
    if author != by:
        return [f"the last commit of the sheet is by {author!r}, not by {by!r}"]
    return []


def _items_by_local(sheets: Sequence[Mapping[str, Any]]) -> dict[str, tuple[str, Mapping[str, Any]]]:
    items: dict[str, tuple[str, Mapping[str, Any]]] = {}
    for sheet in sheets:
        for item in sheet.get("items", []):
            local = str(item["item"]).split("/", 1)[1]
            items[local] = (str(sheet["portion"]), {**item, "_local": local})
    return items


def _locate(draft: Mapping[str, Any], where: Mapping[str, Any]) -> dict[str, Any]:
    return draft[where["list"]][where["index"]]


def promote(
    draft: Mapping[str, Any],
    mapping: Mapping[str, Mapping[str, Any]],
    sheets: Sequence[Mapping[str, Any]],
    verifiers: Sequence[str],
) -> tuple[dict[str, Any], list[str]]:
    """Переносит вердикты подписанных листов в черновик данных.

    ``human-verified`` ставится записи, только если: каждый лист подписан верификатором из
    ``verifiers`` и не менялся после подписи; все проверки записи (по ``mapping``) лежат в
    листах одной порции и имеют вердикт «верно»; запись в черновике не менялась после
    сопоставления (``record_digest``); показанное верификатору совпало с сопоставлением
    (``shown_digest``). «Отклонить» ставит ``rejected``. «Исправить» применяет поля из
    ``corrected`` и оставляет ``pending``: исправление проверяют заново (порция P4).
    Остальные записи не меняются.

    Args:
        draft: черновик файла типа с пятью списками записей.
        mapping: для каждой записи данных (ключ вида ``formulas/r``): ``list``, ``index``,
            ``record_digest`` и ``items`` (локальный идентификатор проверки в листах →
            ``shown_digest``). Одна проверка может стоять у нескольких записей, например
            строка таблицы 5.5 у трёх коэффициентов.
        sheets: листы проверки.
        verifiers: имена из манифеста.

    Returns:
        Новый черновик и строки отчёта. Исходный черновик не меняется.

    Raises:
        ValueError: если лист не принимается.
    """
    problems = [f"{s.get('portion')}: {e}" for s in sheets for e in check_sheet(s, verifiers)]
    if problems:
        raise ValueError("; ".join(problems))
    result = copy.deepcopy(dict(draft))
    available = _items_by_local(sheets)
    report: list[str] = []
    for record_id, where in mapping.items():
        record = _locate(result, where)
        got = {local: available[local] for local in where["items"] if local in available}
        if record_digest(record) != where["record_digest"]:
            report.append(f"{record_id}: skipped, the record changed after it was mapped")
            continue
        if set(got) != set(where["items"]) or any(
            got[k][1].get("shown_digest") != v for k, v in where["items"].items()
        ):
            report.append(f"{record_id}: skipped, the sheets do not cover exactly what was shown")
            continue
        verdicts = {local["verdict"] for _, local in got.values()}
        if None in verdicts:
            report.append(f"{record_id}: left pending, not every item has a verdict")
        elif REJECT in verdicts:
            report.append(_reject(record, record_id, got))
        elif FIX in verdicts:
            report.append(_fix(record, record_id, got))
        else:
            report.append(_approve(record, record_id, got))
    return result, report


def _who(got: Mapping[str, tuple[str, Mapping[str, Any]]]) -> tuple[str, str, set[str], str]:
    items = [local for _, local in got.values()]
    by = str(items[0]["by"])
    at = max(str(i["at"]) for i in items)
    portions = {portion for portion, _ in got.values()}
    comment = "; ".join(sorted({str(i["comment"]) for i in items if i.get("comment")}))
    return by, at, portions, comment


def _approve(record: dict[str, Any], record_id: str, got: Mapping[str, tuple[str, Mapping[str, Any]]]) -> str:
    by, at, portions, comment = _who(got)
    if len(portions) != 1:
        return f"{record_id}: skipped, the items lie in several portions"
    verification: dict[str, Any] = {
        "status": HUMAN_VERIFIED, "by": by, "at": at, "portion": next(iter(portions)),
        "value_digest": record_digest(record),
    }
    if comment:
        verification["comment"] = comment
    record["verification"] = verification
    return f"{record_id}: {HUMAN_VERIFIED} by {by}"


def _reject(record: dict[str, Any], record_id: str, got: Mapping[str, tuple[str, Mapping[str, Any]]]) -> str:
    by, at, _, _ = _who(got)
    reasons = "; ".join(sorted({str(l["comment"]) for _, l in got.values() if l["verdict"] == REJECT}))
    record["verification"] = {"status": "rejected", "by": by, "at": at, "comment": reasons}
    return f"{record_id}: rejected by {by}"


def _fix(record: dict[str, Any], record_id: str, got: Mapping[str, tuple[str, Mapping[str, Any]]]) -> str:
    for _, local in got.values():
        if local["verdict"] != FIX:
            continue
        corrected = local["corrected"]
        if any("/" in str(key) for key in corrected):
            corrected = corrected.get(record_id, {})
        record.update(corrected)
    record["verification"] = {"status": "pending"}
    return f"{record_id}: corrected, pending a new check"
