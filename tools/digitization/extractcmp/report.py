"""Отчёт сравнения извлечений A и B в формате Markdown."""

from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import date

from extractcmp.compare import DIFF_KINDS, METADATA, Comparison, Finding
from extractcmp.normalize import Entry

OUTCOME_TITLES = {
    "match": "совпали полностью",
    "partial": "совпали по всем сравнимым полям; часть полей прочитал только один",
    "image-only": "сравнить нечего: содержимое прочитал только один",
    "metadata-diff": "значения без расхождений, расходятся метаданные",
    "diff": "расхождения по значению, структуре или символам",
    "not-found": "обе стороны: not-found",
    "only-a": "есть только в A",
    "only-b": "есть только в B",
}
OUTCOME_ORDER = tuple(OUTCOME_TITLES)


def summary(results: Sequence[Comparison]) -> Counter[str]:
    """Считает записи по итогам сравнения.

    Args:
        results: результаты сравнения.
    """
    return Counter(r.outcome for r in results)


def _short(value: object, limit: int = 90) -> str:
    text = str(value).replace("|", "\\|").replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _findings(results: Sequence[Comparison], kinds: Sequence[str]) -> list[tuple[Comparison, Finding]]:
    return [(r, f) for r in results for f in r.findings if f.kind in kinds]


def _table(rows: Sequence[Sequence[object]], header: Sequence[str]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(_short(c) for c in row) + " |" for row in rows]
    return lines


def _finding_section(title: str, results: Sequence[Comparison], kinds: Sequence[str]) -> list[str]:
    found = _findings(results, kinds)
    lines = [f"### {title}", ""]
    if not found:
        return lines + ["Расхождений нет.", ""]
    rows = [(r.key, f.field, f.a, f.b, f.note) for r, f in found]
    return lines + _table(rows, ("Запись", "Поле", "A", "B", "Пояснение")) + [""]


def _has(entry: Entry, pick: str) -> bool:
    return entry.ambiguous if pick == "ambiguous" else entry.status == pick


def _entry_list(title: str, results: Sequence[Comparison], pick: str) -> list[str]:
    lines = [f"### {title}", ""]
    rows = []
    for r in results:
        sides = [
            f"{e.source}: {e.status}" + (" + ambiguous" if e.ambiguous and e.status != "ambiguous" else "")
            for e in (r.a, r.b)
            if e is not None and _has(e, pick)
        ]
        if sides:
            page = min(r.entry.pages, default="—")
            rows.append((r.key, page, "; ".join(sides)))
    if not rows:
        return lines + ["Записей нет.", ""]
    return lines + _table(rows, ("Запись", "Страница", "Статус")) + [""]


def render(
    results: Sequence[Comparison],
    aliases: Mapping[str, str],
    a_edition: Mapping[str, frozenset[int]],
    b_edition: Mapping[str, frozenset[int]],
    today: date,
    a_path: str,
    b_path: str,
) -> str:
    """Формирует отчёт сравнения.

    Args:
        results: результаты сравнения в порядке приоритета.
        aliases: сопоставление идентификаторов строк таблицы 5.4 из A в B.
        a_edition: номера изменений в редакциях записей A по идентификаторам.
        b_edition: то же для B.
        today: дата отчёта.
        a_path: путь к файлу A.
        b_path: путь к файлу B.

    Returns:
        Текст Markdown.
    """
    counts = summary(results)
    cells = sum(r.matched for r in results)
    by_kind = Counter(f.kind for r in results for f in r.findings)
    paired = sum(1 for r in results if r.a and r.b)
    editions = {frozenset(v) for v in (*a_edition.values(), *b_edition.values()) if v}
    out = [
        "# Отчёт сравнения извлечений A и B: СП 22.13330.2016, расчёт R",
        "",
        f"Дата: {today.isoformat()}. Сформирован скриптом `tools/digitization` "
        f"(`python -m extractcmp build`) из `{a_path}` и `{b_path}`. Сравнивает код, не человек.",
        "",
        "Совпадение A и B ничего не подтверждает: оба читали один и тот же PDF и могли "
        "одинаково ошибиться. Верификатор проверяет 100% записей, совпавшие тоже "
        "(`interim-normatives-source`, design.md, решение 11).",
        "",
        "## 1. Итоги",
        "",
        f"Записей: в A {sum(1 for r in results if r.a)}, в B {sum(1 for r in results if r.b)}, "
        f"сопоставлено пар {paired}.",
        "",
        *_table(
            [(OUTCOME_TITLES[o], counts.get(o, 0)) for o in OUTCOME_ORDER] + [("Всего", len(results))],
            ("Итог по записи", "Записей"),
        ),
        "",
        f"Сравнений полей и ячеек, давших совпадение: {cells}. Различий по виду: "
        + ", ".join(f"{k} {by_kind.get(k, 0)}" for k in (*DIFF_KINDS, METADATA))
        + f"; полей, прочитанных одной стороной: A {by_kind.get('field-only-a', 0)}, "
        f"B {by_kind.get('field-only-b', 0)}.",
        "",
        "## 2. Допущения сравнения",
        "",
        "- Записи сопоставлены по идентификатору. Строки таблицы 5.4 названы в A и B по-разному, "
        "поэтому они сопоставлены по порядку в файле (допущение; названия ниже, "
        "проверьте глазами):",
        *[f"  - A `{k}` ↔ B `{v}`" for k, v in aliases.items()],
        "- Числа сравниваются на точное равенство после перевода запятой в точку. Допуска нет.",
        "- LaTeX сравнивается по токенам. Численная эквивалентность формул на случайных входах "
        "не проверялась: в A у всех формул `latex` и `tree` пусты (`needs-image`), сравнивать "
        "нечего.",
        "- Постоянные k, k_z=1 в B записаны в LaTeX (`k=1,1`); число взято из правой части. "
        "Условие `b<10` в A взято из `raw_in_layer`.",
        "- Страницы совпадают, если страница A входит в страницы B (или наоборот).",
        "- Пункт нормы сопоставляется по числовым ключам (`5.6.7`, `5.7`, `5.4`), не по словам.",
        "- Редакции: номера изменений "
        + (
            f"одинаковы во всех записях обоих извлечений ({sorted(next(iter(editions)))})."
            if len(editions) == 1
            else f"различаются: {sorted(sorted(e) for e in editions)}."
        ),
        "- Независимость: по отчёту B, значения k, порога и z₀ у k_z автор B видел в отчёте A "
        "до чтения страниц; по этим записям сравнение не полностью независимое.",
        "",
        "## 3. Расхождения",
        "",
        *_finding_section("3.1 По значению", results, ("value",)),
        *_finding_section("3.2 По структуре таблицы", results, ("table-structure",)),
        *_finding_section("3.3 По символам формулы и условию", results, ("formula-symbols",)),
        *_finding_section("3.4 По статусу (одна сторона not-found)", results, ("status",)),
        *_finding_section("3.5 По метаданным (имя параметра, страница, пункт)", results, (METADATA,)),
        "## 4. Записи, которые есть только в одном извлечении",
        "",
    ]
    only = [r for r in results if r.outcome in ("only-a", "only-b")]
    if only:
        out += _table(
            [(r.key, "A" if r.outcome == "only-a" else "B", r.entry.kind, r.entry.pages) for r in only],
            ("Запись", "Где", "Список", "Страницы"),
        )
    else:
        out.append("Таких записей нет.")
    out += [
        "",
        "## 5. Поля, прочитанные одной стороной",
        "",
        "Это не расхождения: в A поле потеряно (растровая картинка в PDF), в B прочитано "
        "с изображения. Значения B стоят в порциях верификатора.",
        "",
    ]
    one = [(r, f) for r, f in _findings(results, ("field-only-a", "field-only-b"))]
    grouped: dict[tuple[str, str], list[str]] = {}
    for r, f in one:
        grouped.setdefault((r.key, f.kind), []).append(f.field)
    if grouped:
        out += _table(
            [(k, "только B" if kind == "field-only-b" else "только A", ", ".join(fields)) for (k, kind), fields in grouped.items()],
            ("Запись", "Кто прочитал", "Поля"),
        )
    else:
        out.append("Таких полей нет.")
    out += [
        "",
        "## 6. Записи `needs-image`, `ambiguous`, `not-found`",
        "",
        *_entry_list("6.1 needs-image", results, "needs-image"),
        *_entry_list("6.2 ambiguous", results, "ambiguous"),
        *_entry_list("6.3 not-found", results, "not-found"),
        "## 7. Совпавшие записи",
        "",
    ]
    if not counts.get("match"):
        out += ["Полностью совпавших записей нет.", ""]
    for outcome in ("match", "partial"):
        rows = [(r.key, r.matched, ", ".join(f.field for f in r.findings) or "—")
                for r in results if r.outcome == outcome]
        if rows:
            out += [f"### {OUTCOME_TITLES[outcome]}", "", *_table(rows, ("Запись", "Совпавших полей", "Прочитано одной стороной")), ""]
    return "\n".join(out) + "\n"


def edition_map(entries: Mapping[str, Entry]) -> dict[str, frozenset[int]]:
    """Собирает номера изменений по записям.

    Args:
        entries: записи одного извлечения.
    """
    return {k: e.amendments for k, e in entries.items()}
