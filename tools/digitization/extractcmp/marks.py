"""Выписка пометок изменений сводного текста, как их видят извлечения A и B."""

import re
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from extractcmp.normalize import Entry

FORMULA_ID = "r_formula_5_7"


def normalize_mark(text: str) -> str:
    """Приводит текст пометки к виду для группировки.

    Args:
        text: текст пометки, например ``(Измененная редакция, Изм. № 5).``
    """
    return re.sub(r"\s+", " ", text.replace("№", "N")).strip()


def report_lines(text: str) -> list[tuple[int, str]]:
    """Находит в отчёте извлечения строки, где говорится об изменениях.

    Args:
        text: содержимое отчёта ``extract-?.report.md``.

    Returns:
        Пары (номер строки, строка) для строк со словом «Изм».
    """
    return [(n, line.rstrip()) for n, line in enumerate(text.splitlines(), start=1) if "Изм" in line]


def _group(entries: Mapping[str, Entry]) -> dict[tuple[int | None, str], dict[str, set[str]]]:
    groups: dict[tuple[int | None, str], dict[str, set[str]]] = defaultdict(
        lambda: {"records": set(), "positions": set(), "bindings": set()}
    )
    for entry in entries.values():
        for mark in entry.marks:
            bucket = groups[(mark.page, normalize_mark(mark.text))]
            bucket["records"].add(entry.id)
            if mark.position:
                bucket["positions"].add(mark.position)
            if mark.binding:
                bucket["bindings"].add(mark.binding)
    return groups


def _record_lines(entry: Entry | None, label: str) -> list[str]:
    if entry is None:
        return [f"- {label}: записи нет."]
    lines = [f"- {label}: статус `{entry.status}`, страница {', '.join(map(str, entry.pages)) or '—'}."]
    for mark in entry.marks:
        parts = [f"страница {mark.page}", f"«{mark.text}»"]
        if mark.position:
            parts.append(f"место: {mark.position}")
        if mark.binding:
            parts.append(f"привязка: {mark.binding}")
        lines.append("  - пометка записи: " + "; ".join(parts))
    for note in entry.notes:
        lines.append(f"  - оговорка: {note}")
    return lines


def render(
    a: Mapping[str, Entry],
    b: Mapping[str, Entry],
    b_top_level: Sequence[Mapping[str, Any]],
    a_report: str,
    b_report: str,
) -> str:
    """Формирует документ с пометками изменений для верификатора.

    Выводов о том, менялась ли формула (5.7), документ не делает.

    Args:
        a: записи A.
        b: записи B.
        b_top_level: список ``amendment_marks`` из файла B.
        a_report: текст отчёта A.
        b_report: текст отчёта B.

    Returns:
        Текст Markdown.
    """
    out = [
        "# Пометки изменений сводного текста и формула (5.7)",
        "",
        "Материал для верификатора (порция P1: ответить, менялась ли формула (5.7) "
        "Изменением № 5). Здесь только то, что записали извлечения A и B. Вывода нет: ни "
        "один из файлов не определяет, к какому абзацу относится пометка.",
        "",
        "## 1. Запись формулы (5.7) в A и B",
        "",
        *_record_lines(a.get(FORMULA_ID), "A"),
        *_record_lines(b.get(FORMULA_ID), "B"),
        "",
        "## 2. Все пометки в записях",
        "",
        "| Страница | Текст пометки | Записи A | Записи B | Место по A | Место и привязка по B |",
        "|---|---|---|---|---|---|",
    ]
    groups_a, groups_b = _group(a), _group(b)
    for key in sorted(set(groups_a) | set(groups_b), key=lambda k: (k[0] or 0, k[1])):
        ga = groups_a.get(key, {"records": set(), "positions": set(), "bindings": set()})
        gb = groups_b.get(key, {"records": set(), "positions": set(), "bindings": set()})
        place_b = "; ".join(sorted(gb["positions"] | gb["bindings"])) or "—"
        out.append(
            f"| {key[0]} | {key[1]} | {_ids(ga['records'])} | {_ids(gb['records'])} | "
            f"{'; '.join(sorted(ga['positions'])) or '—'} | {place_b} |"
        )
    out += [
        "",
        "## 3. Список пометок верхнего уровня в B (`amendment_marks`)",
        "",
        "| Страница | Текст | Область | Привязка |",
        "|---|---|---|---|",
    ]
    for mark in b_top_level:
        out.append(
            f"| {mark.get('page')} | {normalize_mark(str(mark.get('text', '')))} | "
            f"{mark.get('region', '—')} | {mark.get('binding', '—')} |"
        )
    out += ["", "## 4. Строки отчётов извлечений об изменениях (дословно)", "", "### Отчёт A", ""]
    out += [f"- строка {n}: {line}" for n, line in report_lines(a_report)] or ["- нет строк."]
    out += ["", "### Отчёт B", ""]
    out += [f"- строка {n}: {line}" for n, line in report_lines(b_report)] or ["- нет строк."]
    out += [
        "",
        "## 5. Что остаётся верификатору",
        "",
        "- Открыть страницы PDF 36 и 37 и определить, к какому абзацу относится пометка "
        "«Изм. № 5» после примечания 6 к 5.6.7, и затрагивает ли она формулу (5.7).",
        "- Записать ответ в порцию P1 и в файл готовности `interim-normatives-source`.",
    ]
    return "\n".join(out) + "\n"


def _ids(ids: set[str]) -> str:
    if not ids:
        return "—"
    shown = sorted(ids)
    if len(shown) > 4:
        return f"{len(shown)} записей: " + ", ".join(f"`{i}`" for i in shown[:3]) + ", …"
    return ", ".join(f"`{i}`" for i in shown)
