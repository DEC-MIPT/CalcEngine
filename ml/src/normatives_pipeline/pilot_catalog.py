"""Пилотный каталог: привязка типа `foundations_shallow_r` (WP9, раздел 2).

Реестр типа живёт в зоне данных. Для каждого параметра модели `Parameters` пилота он
называет источник — формулу, таблицу с заголовком, порог, проверку, границу диапазона
метода, — но никогда значение: значения берутся из извлечённых данных (`coefficient`)
или из текста пункта. Backend читает только представления `catalog_read`.

Все записи `machine-extracted`/`unverified`; статус поднимается через WP3.

Единицы значений переводятся из единиц реестра/текста в символы словаря backend
(`app/schemas/units.py`); единица вне словаря не даёт сохранить привязку.
"""

from __future__ import annotations

from typing import Any

from . import config, db
from .formulas import expression_tree

CALCULATION_TYPE = "foundations_shallow_r"
DESIGNATION = "СП 22.13330.2016"
CLAUSE = "5.6.7"
TABLE_M = "5.5"
TABLE_GAMMA = "5.4"

UNIT_SYMBOLS = {
    "": "1",
    "м": "m",
    "кН/м³": "kN/m3",
    "кПа": "kPa",
    "°": "deg",
}

_TABLE_LATEX = {
    "M_gamma": r"M_{\gamma}",
    "M_q": "M_q",
    "M_c": "M_c",
}

_M_PARAMETERS = (("m_gamma", "M_gamma"), ("m_q", "M_q"), ("m_c", "M_c"))

_BINDINGS: tuple[dict[str, str], ...] = (
    {"parameter": "gamma_c1", "kind": "table_value", "table_number": TABLE_GAMMA},
    {"parameter": "gamma_c2", "kind": "table_value", "table_number": TABLE_GAMMA},
    {"parameter": "k", "kind": "table_value"},
    {
        "parameter": "m_gamma", "kind": "table_value",
        "table_number": TABLE_M, "heading_symbol": "phi_II",
    },
    {
        "parameter": "m_q", "kind": "table_value",
        "table_number": TABLE_M, "heading_symbol": "phi_II",
    },
    {
        "parameter": "m_c", "kind": "table_value",
        "table_number": TABLE_M, "heading_symbol": "phi_II",
    },
    {"parameter": "k_z_threshold", "kind": "threshold"},
    {
        "parameter": "k_z_below", "kind": "formula",
        "formula_number": f"{CLAUSE}#k_z_below",
    },
    {
        "parameter": "k_z_from", "kind": "formula",
        "formula_number": f"{CLAUSE}#k_z_from",
    },
    {"parameter": "r", "kind": "formula", "formula_number": "5.7"},
    {"parameter": "check_norm_refs", "kind": "check"},
)


class PilotCatalogError(ValueError):
    """Данные пилота не переводятся в контракт каталога."""


def unit_symbol(unit: str) -> str:
    """Переводит единицу реестра/текста в символ словаря backend.

    Raises:
        PilotCatalogError: единица вне словаря.
    """
    try:
        return UNIT_SYMBOLS[unit]
    except KeyError as exc:
        raise PilotCatalogError(f"единица {unit!r} вне словаря") from exc


def _to_float(text: str) -> float:
    return float(text.replace(",", ".").strip())


def _is_number(text: str) -> bool:
    try:
        _to_float(text)
        return True
    except ValueError:
        return False


def parse_heading_rows(cells: list[dict]) -> list[tuple[float, list[float]]]:
    """Разбирает сетку таблицы в строки «заголовок → коэффициенты».

    Заголовком считается ячейка-целое, за которой стоят три числовые ячейки; так
    разбираются обе половины таблицы 5.5 (заголовок `phi_II` в градусах). Строки
    шапки пропускаются: их первая ячейка не целое.
    """
    grid: dict[int, dict[int, str]] = {}
    for cell in cells:
        grid.setdefault(cell["row_index"], {})[cell["col_index"]] = cell["value"]
    rows: list[tuple[float, list[float]]] = []
    for row_index in sorted(grid):
        columns = grid[row_index]
        width = max(columns) + 1 if columns else 0
        index = 0
        while index < width:
            head = (columns.get(index) or "").strip()
            if head.isdigit():
                parts = [(columns.get(index + k) or "").strip() for k in (1, 2, 3)]
                if all(_is_number(part) for part in parts):
                    rows.append((float(head), [_to_float(part) for part in parts]))
                    index += 4
                    continue
            index += 1
    return rows


def m_table_rows(cells: list[dict]) -> list[tuple]:
    """Строит строки `table_value` для `m_gamma`/`m_q`/`m_c` из сетки таблицы 5.5."""
    rows: list[tuple] = []
    for heading, values in parse_heading_rows(cells):
        for (parameter, symbol), value in zip(_M_PARAMETERS, values):
            rows.append(
                (
                    CALCULATION_TYPE, parameter, f"табл. {TABLE_M}", symbol,
                    _TABLE_LATEX[symbol], value, "1", "phi_II", heading, "deg",
                )
            )
    return rows


def _constants_rows(manifest: dict) -> list[tuple]:
    """Одиночные табличные значения без заголовка из реестра данных (`pilot.toml`).

    Пилот не имеет входа выбора грунта, поэтому у типа одно значение на параметр;
    выбор случая зафиксирован в реестре данных и в записи 2.5, не в коде.
    """
    return [
        (
            CALCULATION_TYPE, entry["parameter"], entry["clause"], entry["symbol"],
            entry["latex"], entry["value"], entry["unit"], "", None, "",
        )
        for entry in manifest.get("coefficient", [])
    ]


def _threshold_rows(manifest: dict) -> list[tuple]:
    return [
        (
            CALCULATION_TYPE, entry["parameter"], entry["clause"], entry["latex"],
            entry["value"], entry["unit"],
        )
        for entry in manifest.get("threshold", [])
    ]


def _check_rows() -> list[tuple]:
    return [(CALCULATION_TYPE, "check_norm_refs", CLAUSE)]


def _bound_rows(cells: list[dict]) -> list[tuple]:
    """Границы диапазона метода — min/max заголовков извлечённой таблицы 5.5."""
    headings = [heading for heading, _ in parse_heading_rows(cells)]
    if not headings:
        return []
    table_ref = f"табл. {TABLE_M}"
    return [
        (CALCULATION_TYPE, "phi_II", table_ref, "min", min(headings), "deg", True),
        (CALCULATION_TYPE, "phi_II", table_ref, "max", max(headings), "deg", True),
    ]


def binding_rows(available_formulas: set[str]) -> list[tuple]:
    """Строки привязки, по одной на параметр; формула без дерева не привязывается."""
    rows: list[tuple] = []
    for entry in _BINDINGS:
        if entry["kind"] == "formula" and entry.get("formula_number") not in available_formulas:
            continue
        rows.append(
            (
                CALCULATION_TYPE,
                entry["parameter"],
                entry["kind"],
                entry.get("formula_number", ""),
                entry.get("table_number", ""),
                entry.get("heading_symbol", ""),
                CLAUSE,
            )
        )
    return rows


def _write_synthetic_formulas(
    conn: Any, doc_id: int, manifest: dict, commit: bool = True
) -> set[str]:
    written: set[str] = set()
    for spec in manifest.get("formula", []):
        tree = expression_tree.build_tree(
            spec["expression"], spec["units"].keys()
        )
        expression_tree.validate_tree(tree)
        db.replace_catalog_formula(
            conn,
            doc_id,
            spec["number"],
            CLAUSE,
            spec["latex"],
            spec["expression"],
            spec["result_symbol"],
            tree,
            spec["units"],
            commit=commit,
        )
        written.add(spec["number"])
    return written


def _bind_registry_formula(
    conn: Any, doc_id: int, number: str, commit: bool = True
) -> bool:
    """Строит дерево и единицы формулы реестра; не переводимая формула не привязывается."""
    row = db.fetch_formula_by_number(conn, doc_id, number)
    if row is None or not row["expression"]:
        return False
    notation = db.fetch_notation(conn, doc_id, number)
    units_by_symbol = {entry["symbol"]: entry["unit"] for entry in notation}
    try:
        tree = expression_tree.build_tree(
            row["expression"], units_by_symbol.keys()
        )
        tree_symbols = expression_tree.tree_symbols(tree)
    except expression_tree.ExpressionTreeError:
        return False
    result_symbol = notation_result_symbol(notation)
    if result_symbol is None:
        return False
    all_symbols = {*tree_symbols, result_symbol}
    if not all_symbols <= units_by_symbol.keys():
        return False
    try:
        units = {
            symbol: unit_symbol(units_by_symbol[symbol])
            for symbol in all_symbols
        }
    except PilotCatalogError:
        return False
    db.set_formula_catalog(conn, row["id"], result_symbol, tree, units, commit=commit)
    return True


def notation_result_symbol(notation: list[dict]) -> str | None:
    """Возвращает id символа-результата по виду `output` (иначе первый; None если нет)."""
    for entry in notation:
        if entry.get("kind") == "output":
            return entry["symbol"]
    return notation[0]["symbol"] if notation else None


def sync_pilot_catalog(conn: Any) -> bool:
    """Заполняет каталог данными пилота идемпотентно в одной транзакции.

    Returns:
        ``True``, если документ найден и данные записаны; иначе ``False``.
    """
    doc_id = db.fetch_document_id(conn, DESIGNATION)
    if doc_id is None:
        return False

    manifest = config.pilot_manifest()
    try:
        db.delete_catalog_rows(conn, CALCULATION_TYPE, commit=False)
        available = _write_synthetic_formulas(conn, doc_id, manifest, commit=False)
        if "5.7" not in available and _bind_registry_formula(conn, doc_id, "5.7", commit=False):
            available.add("5.7")
        db.insert_catalog_bindings(conn, doc_id, binding_rows(available), commit=False)
        cells = db.fetch_coefficients(conn, doc_id, TABLE_M)
        db.insert_table_values(
            conn, doc_id, _constants_rows(manifest) + m_table_rows(cells), commit=False
        )
        db.insert_threshold_values(conn, doc_id, _threshold_rows(manifest), commit=False)
        db.insert_check_refs(conn, doc_id, _check_rows(), commit=False)
        db.insert_method_bounds(conn, doc_id, _bound_rows(cells), commit=False)
    except Exception:
        conn.rollback()
        raise
    conn.commit()
    return True
