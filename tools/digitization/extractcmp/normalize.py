"""Приведение записей извлечений A и B к одному виду для сравнения."""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

SHAPES = ("scalar", "t54row", "t54notes", "t55", "bound")
RELATIONS = {"<": "<", ">": ">", "≤": "≤", "≥": "≥", "<=": "≤", ">=": "≥"}
_NUMBER = r"\d+(?:[.,]\d+)?"
_CONDITION = re.compile(rf"(<=|>=|[<>≤≥])\s*({_NUMBER})")
_HEADER = re.compile(rf"({_NUMBER})\s+и\s+(более|менее)")
_CLAUSE = re.compile(r"\d+(?:\.\d+)+")
_AMENDMENTS = re.compile(r"Изменени\w*\s+N\s*([\d,\s]+)")
_LATEX_TOKEN = re.compile(r"\\[A-Za-z]+|[A-Za-z]+|\d+(?:\{,\}\d+|[.,]\d+)?|[^\sA-Za-z\d{}]")
_LATEX_SYNONYMS = {"\\leq": "\\le", "\\geq": "\\ge", "\\cdot": "*", "\\times": "*"}
_LATEX_DROPPED = {"\\left", "\\right", "\\,", "\\;", "\\!"}


@dataclass(frozen=True)
class Mark:
    """Пометка изменений, как её записало извлечение.

    Attributes:
        page: страница PDF.
        text: текст пометки.
        position: описание места пометки.
        binding: привязка к абзацу, если извлечение её указало.
    """

    page: int | None
    text: str
    position: str | None = None
    binding: str | None = None


@dataclass(frozen=True)
class Entry:
    """Запись извлечения в общем виде.

    Attributes:
        id: идентификатор записи в своём извлечении.
        source: ``A`` или ``B``.
        kind: список каталога (``formulas``, ``table_values`` и так далее).
        shape: вид сравнения из ``SHAPES``.
        order: номер записи среди записей того же вида в файле.
        status: статус извлечения: ``machine-extracted``, ``ambiguous``, ``needs-image``
            или ``not-found``.
        ambiguous: у записи есть пометка ``ambiguous`` (статус или поле ``also``).
        pages: страницы PDF.
        region: область страницы, если извлечение её указало.
        clause: числовые ключи пункта нормы.
        amendments: номера изменений из редакции записи.
        fields: сравниваемые поля.
        marks: пометки изменений, привязанные к записи.
        notes: оговорки извлечения.
    """

    id: str
    source: str
    kind: str
    shape: str
    order: int
    status: str
    ambiguous: bool
    pages: tuple[int, ...]
    region: str | None
    clause: tuple[str, ...]
    amendments: frozenset[int]
    fields: Mapping[str, Any]
    marks: tuple[Mark, ...] = ()
    notes: tuple[str, ...] = ()
    raw: Mapping[str, Any] = field(default_factory=dict, compare=False, repr=False)


def to_number(text: str) -> float:
    """Переводит число с запятой или точкой в ``float``.

    Args:
        text: запись числа, например ``1,25``.
    """
    return float(text.replace(",", "."))


def numbers_in(text: str | None) -> tuple[float, ...]:
    """Возвращает все числа текста по порядку.

    Args:
        text: исходный текст или ``None``.
    """
    if not text:
        return ()
    return tuple(to_number(m) for m in re.findall(_NUMBER, text))


def parse_condition(text: str | None) -> tuple[str, float] | None:
    """Находит в тексте первое сравнение числа, например ``b<10``.

    Args:
        text: текст условия или ``None``.

    Returns:
        Пару (знак, число) или ``None``, если сравнения нет.
    """
    if not text:
        return None
    match = _CONDITION.search(text)
    if match is None:
        return None
    return RELATIONS[match.group(1)], to_number(match.group(2))


def parse_header_relation(text: str | None) -> tuple[str, float] | None:
    """Читает из шапки столбца «N и более» или «N и менее».

    Args:
        text: текст шапки или ``None``.

    Returns:
        Пару (знак, число) или ``None``.
    """
    if not text:
        return None
    match = _HEADER.search(text)
    if match is None:
        return None
    return ("≥" if match.group(2) == "более" else "≤"), to_number(match.group(1))


def parse_latex_constant(latex: str | None) -> float | None:
    """Достаёт число из правой части ``обозначение=число``.

    Args:
        latex: запись LaTeX или ``None``.

    Returns:
        Число или ``None``, если правая часть не число.
    """
    if not latex:
        return None
    match = re.fullmatch(r".*?=\s*(-?\d+(?:\{,\}\d+|[.,]\d+)?)", latex.replace(" ", ""))
    if match is None:
        return None
    return to_number(match.group(1).replace("{,}", "."))


def latex_tokens(latex: str) -> list[str]:
    """Разбивает LaTeX на токены без скобок группировки и пробелов.

    Args:
        latex: запись LaTeX.
    """
    tokens = []
    for token in _LATEX_TOKEN.findall(latex):
        if token in _LATEX_DROPPED:
            continue
        token = _LATEX_SYNONYMS.get(token, token)
        tokens.append(token.replace("{,}", "."))
    return tokens


def clause_key(refs: object) -> tuple[str, ...]:
    """Собирает числовые ключи пунктов из ссылок на норму записи.

    Args:
        refs: список ссылок ``norm_refs``.
    """
    keys: list[str] = []
    for ref in refs if isinstance(refs, list) else []:
        keys.extend(_CLAUSE.findall(str(ref.get("clause", ""))))
    return tuple(dict.fromkeys(keys))


def amendment_numbers(text: str | None) -> frozenset[int]:
    """Находит номера изменений в строке редакции.

    Args:
        text: строка редакции или ``None``.
    """
    if not text:
        return frozenset()
    match = _AMENDMENTS.search(text)
    if match is None:
        return frozenset()
    return frozenset(int(n) for n in re.findall(r"\d+", match.group(1)))


def _amendments_of(refs: object) -> frozenset[int]:
    numbers: set[int] = set()
    for ref in refs if isinstance(refs, list) else []:
        numbers |= amendment_numbers(ref.get("edition"))
    return frozenset(numbers)


def _shape(record_id: str, kind: str) -> str:
    if record_id == "t55":
        return "t55"
    if record_id == "t54_notes":
        return "t54notes"
    if record_id.startswith("t54_"):
        return "t54row"
    if kind == "method_bounds":
        return "bound"
    return "scalar"


def _marks(items: object) -> tuple[Mark, ...]:
    marks = []
    for item in items if isinstance(items, list) else []:
        marks.append(
            Mark(
                page=item.get("page"),
                text=str(item.get("mark") or item.get("text") or ""),
                position=item.get("position") or item.get("region"),
                binding=item.get("binding"),
            )
        )
    return tuple(marks)


def _scalar_a(rec: Mapping[str, Any]) -> dict[str, Any]:
    value = rec.get("value")
    if value is None and rec.get("value_in_layer") is not None:
        value = to_number(str(rec["value_in_layer"]))
    condition = parse_condition(rec.get("raw_in_layer")) if rec.get("kind") == "formulas" else None
    return {
        "parameter": rec.get("parameter"),
        "result_symbol": rec.get("result_symbol"),
        "value": None if value is None else float(value),
        "unit": rec.get("unit"),
        "latex": rec.get("latex"),
        "condition": condition,
    }


def _scalar_b(rec: Mapping[str, Any], kind: str) -> dict[str, Any]:
    value = rec.get("value")
    if value is None and kind == "formulas":
        value = parse_latex_constant(rec.get("latex"))
    condition = parse_condition(rec.get("condition")) if kind == "formulas" else None
    return {
        "parameter": rec.get("parameter"),
        "result_symbol": rec.get("result_symbol"),
        "value": None if value is None else float(value),
        "unit": rec.get("unit") if kind != "formulas" else None,
        "latex": rec.get("latex"),
        "condition": condition,
    }


def _t54_a(rec: Mapping[str, Any]) -> dict[str, Any]:
    columns = [
        {
            "value": float(c["value"]),
            "symbol": c.get("symbol"),
            "header": parse_header_relation(c.get("header_in_layer")),
        }
        for c in rec.get("columns", [])
    ]
    return {
        "parameter": rec.get("parameter"),
        "columns": columns,
        "condition_numbers": numbers_in(rec.get("condition_note")) or None,
        "condition_lost": rec.get("condition_status") == "needs-image",
    }


def _t54_b(rec: Mapping[str, Any]) -> dict[str, Any]:
    columns = []
    for cell in rec.get("cells", []):
        relation = cell.get("heading_relation")
        header = None
        if relation is not None and cell.get("heading_value") is not None:
            header = (RELATIONS[relation], float(cell["heading_value"]))
        columns.append({"value": float(cell["value"]), "symbol": cell.get("symbol"), "header": header})
    return {
        "parameter": rec.get("parameter"),
        "columns": columns,
        "condition_numbers": numbers_in(rec.get("condition")) or None,
        "condition_lost": False,
    }


def _t55_a(rec: Mapping[str, Any]) -> dict[str, Any]:
    rows = {int(r["selector_deg"]): tuple(float(v) for v in r["values"]) for r in rec.get("rows", [])}
    selectors = [int(r["selector_deg"]) for r in rec.get("rows", [])]
    symbols = [c.get("symbol") for c in rec.get("columns", [])]
    return {"parameter": rec.get("parameter"), "rows": rows, "selectors": selectors, "symbols": symbols}


def _t55_b(rec: Mapping[str, Any]) -> dict[str, Any]:
    names = [c["symbol"] for c in rec.get("columns", [])]
    rows = {
        int(r["phi_II"]): tuple(float(r[n]) for n in names) for r in rec.get("rows", [])
    }
    selectors = [int(r["phi_II"]) for r in rec.get("rows", [])]
    return {"parameter": rec.get("parameter"), "rows": rows, "selectors": selectors, "symbols": names}


def _entry(
    rec: Mapping[str, Any],
    source: str,
    kind: str,
    order: int,
    status: str,
    ambiguous: bool,
    pages: tuple[int, ...],
    fields: Mapping[str, Any],
    notes: tuple[str, ...],
    marks: tuple[Mark, ...],
) -> Entry:
    shape = _shape(rec["id"], kind)
    return Entry(
        id=rec["id"],
        source=source,
        kind=kind,
        shape=shape,
        order=order,
        status=status,
        ambiguous=ambiguous,
        pages=pages,
        region=rec.get("region"),
        clause=clause_key(rec.get("norm_refs")),
        amendments=_amendments_of(rec.get("norm_refs")),
        fields=fields,
        marks=marks,
        notes=notes,
        raw=rec,
    )


def _fields_a(shape: str, rec: Mapping[str, Any]) -> Mapping[str, Any]:
    builders = {"scalar": _scalar_a, "bound": _scalar_a, "t54row": _t54_a, "t55": _t55_a}
    if shape == "t54notes":
        return {"content": rec.get("extraction_status") != "needs-image"}
    return builders[shape](rec)


def _fields_b(shape: str, rec: Mapping[str, Any], kind: str) -> Mapping[str, Any]:
    if shape == "t54notes":
        return {"content": bool(rec.get("notes_read"))}
    if shape == "t54row":
        return _t54_b(rec)
    if shape == "t55":
        return _t55_b(rec)
    return _scalar_b(rec, kind)


def load_a(data: Mapping[str, Any]) -> dict[str, Entry]:
    """Читает извлечение A.

    Args:
        data: содержимое ``extract-a.yaml``.

    Returns:
        Записи по идентификаторам в порядке файла.
    """
    entries: dict[str, Entry] = {}
    counters: dict[str, int] = {}
    for rec in data["records"]:
        kind = rec["kind"]
        shape = _shape(rec["id"], kind)
        order = counters.get(shape, 0)
        counters[shape] = order + 1
        status = rec["extraction_status"]
        ambiguous = status == "ambiguous" or "ambiguous" in rec.get("also", [])
        notes = tuple(str(rec[k]) for k in ("note", "condition_note") if rec.get(k))
        marks = _marks(rec.get("change_marks")) + _marks(rec.get("nearby_marks"))
        entries[rec["id"]] = _entry(
            rec, "A", kind, order, status, ambiguous,
            (rec["page"],), _fields_a(shape, rec), notes, marks,
        )
    return entries


def load_b(data: Mapping[str, Any]) -> dict[str, Entry]:
    """Читает извлечение B.

    Args:
        data: содержимое ``extract-b.yaml``.

    Returns:
        Записи по идентификаторам в порядке файла; записи ``extra_records`` отмечены
        видом ``extra_records``.
    """
    entries: dict[str, Entry] = {}
    counters: dict[str, int] = {}
    for kind in ("formulas", "table_values", "thresholds", "checks", "method_bounds", "extra_records"):
        for rec in data.get(kind, []):
            shape = _shape(rec["id"], kind)
            order = counters.get(shape, 0)
            counters[shape] = order + 1
            extraction = rec.get("extraction", {})
            status = extraction.get("status", "machine-extracted")
            pages = tuple(rec.get("pages") or ([rec["page"]] if rec.get("page") else []))
            notes = tuple(str(n) for n in extraction.get("notes", []))
            marks = _marks(rec.get("nearby_marks"))
            entries[rec["id"]] = _entry(
                rec, "B", kind, order, status, status == "ambiguous",
                pages, _fields_b(shape, rec, kind), notes, marks,
            )
    return entries
