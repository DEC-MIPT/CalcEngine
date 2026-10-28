"""Порции верификатора: записи, расхождения первыми, по часу работы."""

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from extractcmp.checkpoints import ControlPoint
from extractcmp.compare import Comparison
from extractcmp.normalize import Entry

VERDICTS = ("верно", "исправить", "отклонить")
PORTION_MINUTES = 60.0
MINUTES = {
    "scalar": 2.0,
    "formula": 5.0,
    "t54row": 3.0,
    "t54notes": 6.0,
    "t55row": 0.8,
    "bound": 2.0,
    "edition": 3.0,
    "control-point": 3.0,
    "control-point-empty": 4.0,
}
DIFF_EXTRA_MINUTES = 3.0
GROUP_TITLES = {
    "P1": "формулы, их коэффициенты, правила, редакция и контрольные точки формул",
    "P2": "таблицы 5.4 и 5.5 и их контрольные точки",
    "P3": "порог k_z, границы метода, ссылка проверки p ≤ R",
    "D": "отложено: правила и формулы вне R пилота (фаза 1b, структурированные входы C2)",
}
GROUPS = ("P1", "P2", "P3", "D")
"""Порядок групп порций; ``D`` идёт последней и в задачи 7.3a–7.4 не входит."""
DEFERRED = frozenset({
    "d_b_cap_2m", "h_n_allowances", "note1_b_sqrt_A", "note5_d1_gt_d", "d1_formula_5_8", "k_from_appendix_A",
})
"""Записи, которых нет в файле типа пилота: их проверка отложена в группу ``D``.

Решение Akim 2026-10-27: P1 проверяет только данные R пилота. Контрольные точки этих
записей отнесены к ``D`` в ``checkpoints.py``.
"""
_GROUP_BY_KIND = {
    "formulas": "P1",
    "extra_records": "P1",
    "table_values": "P2",
    "thresholds": "P3",
    "checks": "P3",
    "method_bounds": "P3",
}
CHECKED_WITH = {"z0_in_k_z": "k_z_formula_b_from_threshold"}
"""Проверка → проверка, с которой она идёт в одну порцию.

Черновик собирает их в одну запись каталога (z_0 подставлен в формулу k_z), а ``promote``
переносит запись, только если все её проверки лежат в одной порции.
"""


@dataclass
class Item:
    """Одна проверка верификатора.

    Attributes:
        item_id: уникальный идентификатор внутри порции.
        record: идентификатор записи (общий для A и B) или точки.
        group: ``P1``, ``P2``, ``P3`` или отложенная ``D``.
        kind: ``record``, ``table-row``, ``control-point`` или ``edition``.
        title: короткое название.
        page: страницы PDF.
        region: область страницы по B.
        flags: статус расхождения и пометки ``ambiguous``/``needs-image``.
        a: значение из A.
        b: значение из B.
        notes: оговорки извлечений.
        priority: 0 расхождение, 1 ambiguous или needs-image, 2 остальное, 3 точки.
        minutes: оценка времени проверки.
        shown_digest: SHA-256 того, что показано верификатору.
    """

    item_id: str
    record: str
    group: str
    kind: str
    title: str
    page: str
    region: str
    flags: list[str]
    a: str
    b: str
    notes: list[str] = field(default_factory=list)
    priority: int = 2
    minutes: float = 0.0
    shown_digest: str = ""


@dataclass
class Portion:
    """Порция работы верификатора.

    Attributes:
        portion_id: например ``P1-1``.
        group: ``P1``, ``P2``, ``P3`` или ``D``.
        items: проверки в порядке «расхождения и ambiguous первыми».
    """

    portion_id: str
    group: str
    items: list[Item]

    @property
    def minutes(self) -> float:
        """Суммарная оценка времени."""
        return sum(i.minutes for i in self.items)


def _fmt(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_fmt(v) for v in value) + "]"
    return str(value)


def describe(entry: Entry | None) -> str:
    """Описывает значение записи для верификатора.

    Args:
        entry: запись извлечения или ``None``.

    Returns:
        Строку вида ``поле: значение; ...``; ``нет записи``, если записи нет.
    """
    if entry is None:
        return "нет записи"
    f = entry.fields
    if entry.shape == "t54row":
        values = [c["value"] for c in f["columns"]]
        symbols = [c["symbol"] or "—" for c in f["columns"]]
        parts = [f"значения: {_fmt(values)}", f"обозначения столбцов: {_fmt(symbols)}"]
        if f["condition_numbers"]:
            parts.append(f"числа условия: {_fmt(list(f['condition_numbers']))}")
        return "; ".join(parts)
    if entry.shape == "t54notes":
        return "примечания прочитаны" if f["content"] else "не прочитаны (needs-image)"
    if entry.shape == "t55":
        return f"строк: {len(f['rows'])}; столбцы: {_fmt(f['symbols'])}"
    parts = []
    for name in ("parameter", "result_symbol", "latex", "value", "unit", "condition"):
        if f.get(name) is not None:
            parts.append(f"{name}: {_fmt(f[name])}")
    if not parts:
        parts.append(f"содержимого нет (статус {entry.status})")
    return "; ".join(parts)


def _digest(*parts: object) -> str:
    text = json.dumps(parts, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=list)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _group(entry: Entry) -> str:
    return _GROUP_BY_KIND.get(entry.kind, "P1")


def _flags(cmp: Comparison) -> list[str]:
    return [f"итог: {cmp.outcome}", *cmp.flags]


def _minutes(cmp: Comparison, entry: Entry) -> float:
    has_latex = any(e is not None and e.fields.get("latex") for e in (cmp.a, cmp.b))
    base = MINUTES["formula"] if has_latex else MINUTES.get(entry.shape, MINUTES["scalar"])
    if cmp.outcome in ("diff", "metadata-diff", "only-a", "only-b"):
        base += DIFF_EXTRA_MINUTES
    return base


def _notes(cmp: Comparison) -> list[str]:
    return [f"{e.source}: {n}" for e in (cmp.a, cmp.b) if e is not None for n in e.notes]


def _t55_items(cmp: Comparison) -> list[Item]:
    a = cmp.a.fields["rows"] if cmp.a else {}
    b = cmp.b.fields["rows"] if cmp.b else {}
    entry = cmp.entry
    region = entry.region or "—"
    items = []
    for selector in sorted(set(a) | set(b)):
        differs = a.get(selector) != b.get(selector)
        flags = ["итог: расхождение"] if differs else ["итог: совпало"]
        items.append(
            Item(
                item_id=f"t55@phi={selector}",
                record="t55",
                group="P2",
                kind="table-row",
                title=f"Таблица 5.5, φ_II = {selector}°",
                page=", ".join(map(str, entry.pages)),
                region=region,
                flags=flags,
                a=_fmt(list(a[selector])) if selector in a else "нет строки",
                b=_fmt(list(b[selector])) if selector in b else "нет строки",
                priority=0 if differs else 2,
                minutes=MINUTES["t55row"] + (DIFF_EXTRA_MINUTES if differs else 0.0),
                shown_digest=_digest("t55", selector, a.get(selector), b.get(selector)),
            )
        )
    return items


def record_items(results: Iterable[Comparison]) -> list[Item]:
    """Строит проверки по сравнениям: каждая запись и каждая строка таблицы 5.5.

    Args:
        results: результаты сравнения.

    Returns:
        Проверки; для каждой записи A и B есть хотя бы одна. Проверка из `CHECKED_WITH`
        получает запись и группу своей пары, чтобы ``split`` положил их в одну порцию.
    """
    items: list[Item] = []
    for cmp in results:
        entry = cmp.entry
        if entry.shape == "t55":
            items.extend(_t55_items(cmp))
            continue
        minutes = _minutes(cmp, entry)
        a_text, b_text = describe(cmp.a), describe(cmp.b)
        items.append(
            Item(
                item_id=cmp.key,
                record=cmp.key,
                group="D" if cmp.key in DEFERRED else _group(entry),
                kind="record",
                title=cmp.key,
                page=", ".join(map(str, entry.pages)) or "—",
                region=(cmp.b.region if cmp.b and cmp.b.region else "—"),
                flags=_flags(cmp),
                a=a_text,
                b=b_text,
                notes=_notes(cmp),
                priority=cmp.priority,
                minutes=minutes,
                shown_digest=_digest(a_text, b_text, cmp.key),
            )
        )
    by_id = {i.item_id: i for i in items}
    for item_id, partner in CHECKED_WITH.items():
        if item_id in by_id and partner in by_id:
            by_id[item_id].record = partner
            by_id[item_id].group = by_id[partner].group
    return items


EDITION_REGION = "раздел «Предисловие», последний абзац (перечень изменений); страницу указывает верификатор"
"""Где искать редакцию по умолчанию: изменения СП перечислены в «Предисловии» (Akim, 2026-10-28)."""


def edition_item(a_edition: str, b_edition: str, page: str = "—", region: str = EDITION_REGION) -> Item:
    """Строит проверку редакции документа.

    Args:
        a_edition: редакция, как её записало извлечение A.
        b_edition: редакция, как её записало извлечение B.
        page: страница PDF с перечнем изменений, если она известна.
        region: область этой страницы.
    """
    return Item(
        item_id="edition", record="edition", group="P1", kind="edition",
        title="Редакция документа как напечатана", page=page, region=region,
        flags=["итог: проверка редакции"], a=a_edition, b=b_edition, priority=1,
        minutes=MINUTES["edition"], shown_digest=_digest(a_edition, b_edition),
    )


def control_point_items(points: Sequence[ControlPoint], label: str) -> list[Item]:
    """Строит проверки по контрольным точкам.

    Args:
        points: контрольные точки.
        label: пометка источника значений из методички.
    """
    items = []
    for p in points:
        empty = any(v is None for v in p.expected.values())
        inputs = "; ".join(f"{k} = {v if v is not None else '…'}" for k, v in p.inputs.items())
        expected = "; ".join(f"{k} = {v if v is not None else '…'}" for k, v in p.expected.items())
        items.append(
            Item(
                item_id=p.cp_id, record=p.cp_id, group=p.group, kind="control-point", title=p.title,
                page="—", region="—", flags=["контрольная точка"],
                a=f"вход: {inputs}",
                b=f"ожидаемый выход: {expected}" + (f" [{label}]" if p.sourced else " [пусто, заполняет верификатор]"),
                notes=[p.note] if p.note else [], priority=3,
                minutes=MINUTES["control-point-empty" if empty else "control-point"],
                shown_digest=_digest(p.cp_id, dict(p.inputs), dict(p.expected)),
            )
        )
    return items


def split(items: Sequence[Item], minutes: float = PORTION_MINUTES) -> list[Portion]:
    """Делит проверки на порции примерно по часу.

    Записи не рвутся: все строки одной записи лежат в одной порции. Внутри порции и между
    порциями группы идут в порядке «расхождения, ambiguous и needs-image, остальные, точки».

    Args:
        items: все проверки.
        minutes: предел времени порции.

    Returns:
        Порции P1-1, P1-2, …, P2-1, …, D-1 в порядке `GROUPS`.
    """
    portions: list[Portion] = []
    for group in GROUPS:
        records: dict[str, list[Item]] = {}
        for item in items:
            if item.group == group:
                records.setdefault(item.record, []).append(item)
        ordered = sorted(
            records.values(),
            key=lambda r: (min(i.priority for i in r), r[0].page, r[0].record),
        )
        current: list[Item] = []
        for record in ordered:
            size = sum(i.minutes for i in record)
            if current and sum(i.minutes for i in current) + size > minutes:
                portions.append(Portion(f"{group}-{len(portions_of(portions, group)) + 1}", group, current))
                current = []
            current.extend(record)
        if current:
            portions.append(Portion(f"{group}-{len(portions_of(portions, group)) + 1}", group, current))
    return portions


def portions_of(portions: Sequence[Portion], group: str) -> list[Portion]:
    """Выбирает порции одной группы.

    Args:
        portions: порции.
        group: ``P1``, ``P2``, ``P3`` или ``D``.
    """
    return [p for p in portions if p.group == group]


def render_sheet(portion: Portion, today: date, source_files: Mapping[str, str]) -> dict[str, Any]:
    """Строит лист проверки порции для записи вердиктов.

    Args:
        portion: порция.
        today: дата формирования.
        source_files: пути файлов A и B.

    Returns:
        Словарь для YAML. Вердикты, ``by``, ``at``, ``comment`` и ``signature`` пусты.
    """
    return {
        "portion": portion.portion_id,
        "generated": today.isoformat(),
        "sources": dict(source_files),
        "verdicts_allowed": list(VERDICTS),
        "items": [
            {
                "item": f"{portion.portion_id}/{i.item_id}",
                "record": i.record,
                "kind": i.kind,
                "page": i.page,
                "shown_digest": i.shown_digest or None,
                "verdict": None,
                "corrected": None,
                "by": None,
                "at": None,
                "comment": None,
            }
            for i in portion.items
        ],
        "signature": None,
    }


def render_markdown(portion: Portion, today: date, label: str) -> str:
    """Формирует читаемую порцию в Markdown.

    Args:
        portion: порция.
        today: дата формирования.
        label: пометка источника контрольных точек.

    Returns:
        Текст Markdown.
    """
    out = [
        f"# Порция {portion.portion_id}: {GROUP_TITLES[portion.group]}",
        "",
        f"Дата: {today.isoformat()}. Проверок: {len(portion.items)}. Оценка: около {portion.minutes:.0f} мин "
        "(гипотеза, допущения в `index.md`).",
        "",
        "Вердикт записывается в лист `" + f"{portion.portion_id}.yaml`" + " (поля `verdict`, `by`, `at`, `comment`); "
        "значения: верно / исправить / отклонить. При «исправить» исправленное значение пишется в `corrected`. "
        "Совпадение A и B проверку не снимает.",
        "",
    ]
    compact = [i for i in portion.items if i.kind == "table-row"]
    for number, item in enumerate((i for i in portion.items if i.kind != "table-row"), start=1):
        out += [
            f"## {number}. {item.title}",
            "",
            f"- Лист: `{portion.portion_id}/{item.item_id}`",
            f"- Страница PDF: {item.page}; область: {item.region}",
            f"- Статус: {'; '.join(item.flags)}",
            f"- A: {item.a}",
            f"- B: {item.b}",
        ]
        out += [f"- Оговорка {n}" for n in item.notes]
        out += ["- Вердикт: ☐ верно  ☐ исправить  ☐ отклонить", "- Кто / когда / комментарий: ______", ""]
    if compact:
        out += [
            "## Строки таблицы 5.5",
            "",
            "A и B: значения столбцов M_γ, M_q, M_c по порядку. Лист: `" + f"{portion.portion_id}/t55@phi=<φ>`.",
            "",
            "| φ_II | A | B | Статус | Вердикт | Кто | Когда | Комментарий |",
            "|---|---|---|---|---|---|---|---|",
        ]
        out += [f"| {i.item_id.split('=')[1]} | {i.a} | {i.b} | {i.flags[0]} | ☐ | | | |" for i in compact]
        out.append("")
    return "\n".join(out)


def render_index(portions: Sequence[Portion], today: date) -> str:
    """Формирует оглавление порций с оценкой часов.

    Args:
        portions: порции.
        today: дата формирования.
    """
    total = sum(p.minutes for p in portions)
    out = [
        "# Порции верификатора: оглавление",
        "",
        f"Дата: {today.isoformat()}. Порций: {len(portions)}, проверок: {sum(len(p.items) for p in portions)}, "
        f"оценка: {total:.0f} мин ≈ {total / 60:.1f} ч (гипотеза).",
        "",
        "| Порция | Содержание | Проверок | Оценка, мин |",
        "|---|---|---|---|",
    ]
    out += [
        f"| {p.portion_id} | {GROUP_TITLES[p.group]} | {len(p.items)} | {p.minutes:.0f} |" for p in portions
    ]
    out += [
        "",
        "## Допущения оценки",
        "",
        "Минуты на проверку (константы `MINUTES` в `portions.py`; мои допущения, не замеры): "
        + ", ".join(f"{k} {v:g}" for k, v in MINUTES.items())
        + f"; расхождение или запись одной стороны +{DIFF_EXTRA_MINUTES:g}. Верификатор открывает PDF "
        "на нужной странице и сверяет значение с A и B. Не включены: чтение инструкции, перерывы, "
        "ответ на вопрос об Изм. № 5, назначение допуска ex1. Порция ограничена "
        f"{PORTION_MINUTES:g} мин; запись из нескольких строк (таблица 5.5) не делится.",
        "",
        "Разбиение на P1–P3 следует `interim-normatives-source`, задачи 7.3a–7.3c; порядок внутри "
        "группы: расхождения и ambiguous первыми. Так порции P1 с формулой (5.7) идут первыми.",
        "",
        "Порции D — проверки записей, которых нет в файле типа пилота (`DEFERRED` в `portions.py`), "
        "и их контрольные точки. Они нужны фазе 1b и структурированным входам C2 и в задачи "
        "7.3a–7.4 не входят (решение Akim 2026-10-27).",
    ]
    return "\n".join(out) + "\n"
