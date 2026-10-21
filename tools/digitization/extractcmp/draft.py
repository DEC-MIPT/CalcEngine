"""Сборка черновика файла типа ``foundations_shallow_r`` из извлечения B и сопоставление с листами."""

import copy
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from extractcmp.portions import Item
from extractcmp.promote import record_digest

PENDING = {"status": "pending"}
CASE_ROW = "t54_clayey_il_gt_0_5"
GAMMA_C1_COLUMN = "c1"
GAMMA_C2_COLUMNS = ("c2_ge4", "c2_le15")
K_RECORD = "k_direct_tests"
Z0_RECORD = "z0_in_k_z"
OUTPUT_UNITS = {"R": "kPa"}
M_PARAMETERS = {"M_gamma": "m_gamma", "M_q": "m_q", "M_c": "m_c"}
HEADING_SYMBOL = "phi_II"
HEADING_UNIT = "deg"
LISTS = ("formulas", "table_values", "thresholds", "checks", "method_bounds")
NOT_STORED = {
    "d1_formula_5_8": "формула (5.8): в пилоте d_1 — вход, формула нужна фазе 1b",
    "k_from_appendix_A": "k = 1,1: у параметра k одно значение без заголовка, берётся случай испытаний",
    "t54_notes": "примечания к таблице 5.4: вход выбора грунта появится вместе со структурированными входами (C2)",
    "note5_d1_gt_d": "правило: в схеме файла нет списка правил",
    "d_b_cap_2m": "правило: в схеме файла нет списка правил",
    "note1_b_sqrt_A": "правило: в схеме файла нет списка правил",
    "h_n_allowances": "правило: в схеме файла нет списка правил",
    "method_bounds_none": "границ метода в тексте нет (оба извлечения), список границ пуст",
    "edition": "редакция проверяется по манифесту, не по записи",
}
NOT_STORED_TABLE_54 = "строка таблицы 5.4: у γc1, γc2 одно значение без заголовка, берётся строка случая ex1"


class DraftError(ValueError):
    """Извлечение B не даёт записей, которых требует привязка пилота."""


@dataclass
class Draft:
    """Черновик файла типа, сопоставление и записи, не попавшие в файл.

    Attributes:
        type_file: словарь с пятью списками записей.
        mapping: ключ записи данных → ``list``, ``index``, ``record_digest``, ``items``.
        notes: допущения сборки, которые проверяет верификатор.
        not_stored: идентификатор проверки листа → причина, по которой записи данных нет.
    """

    type_file: dict[str, list[dict[str, Any]]]
    mapping: dict[str, dict[str, Any]]
    notes: list[str] = field(default_factory=list)
    not_stored: dict[str, str] = field(default_factory=dict)


def _raw(b: Mapping[str, Any], record_id: str) -> Mapping[str, Any]:
    try:
        return b[record_id].raw
    except KeyError:
        raise DraftError(f"no record {record_id!r} in extract B") from None


def _refs(raw: Mapping[str, Any]) -> list[dict[str, Any]]:
    return copy.deepcopy(raw["norm_refs"])


def _cell(raw: Mapping[str, Any], column: str) -> Mapping[str, Any]:
    for cell in raw["cells"]:
        if cell["column"] == column:
            return cell
    raise DraftError(f"no column {column!r} in {raw['id']!r}")


def _substitute(tree: Any, name: str, value: float) -> Any:
    if isinstance(tree, dict):
        if tree.get("kind") == "symbol" and tree.get("name") == name:
            return {"kind": "number", "value": value}
        return {k: _substitute(v, name, value) for k, v in tree.items()}
    return tree


def _tree_symbols(tree: Any) -> set[str]:
    if isinstance(tree, dict):
        found = {tree["name"]} if tree.get("kind") == "symbol" else set()
        for value in tree.values():
            found |= _tree_symbols(value)
        return found
    return set()


def _symbol_units(b: Mapping[str, Any]) -> dict[str, str]:
    units: dict[str, str] = {}
    for entry in b.values():
        raw = entry.raw
        for cell in raw.get("cells", []):
            units[cell["symbol"]] = cell["unit"]
        for column in raw.get("columns", []):
            if "symbol" in column and "unit" in column:
                units[column["symbol"]] = column["unit"]
        if "k_z" in raw.get("units", {}):
            units["k_z"] = raw["units"]["k_z"]
        if raw.get("id") == K_RECORD:
            units["k"] = raw["units"]["k"]
    return units


def _formula(parameter: str, raw: Mapping[str, Any], tree: Any, latex: str, units: Mapping[str, str]) -> dict[str, Any]:
    return {
        "parameter": parameter,
        "result_symbol": raw["result_symbol"],
        "latex": latex,
        "tree": tree,
        "units": dict(units),
        "norm_refs": _refs(raw),
        "page": raw["page"],
        "verification": dict(PENDING),
    }


def _table_value(parameter: str, symbol: str, latex: str, value: float, unit: str, raw: Mapping[str, Any],
                 heading: float | None = None) -> dict[str, Any]:
    return {
        "parameter": parameter,
        "symbol": symbol,
        "latex": latex,
        "value": float(value),
        "unit": unit,
        "heading_symbol": None if heading is None else HEADING_SYMBOL,
        "heading_value": None if heading is None else float(heading),
        "heading_unit": None if heading is None else HEADING_UNIT,
        "norm_refs": _refs(raw),
        "page": raw["page"],
        "verification": dict(PENDING),
    }


def build(b: Mapping[str, Any], items: Mapping[str, Item]) -> Draft:
    """Собирает черновик файла типа из записей B.

    Привязка и выбор случая — как в пилоте: параметры модели ``Parameters`` типа
    ``foundations_shallow_r``, ``γc1`` и ``γc2`` берутся из строки случая ``ex1`` таблицы
    5.4, ``k`` из случая испытаний. Все записи ``pending``.

    Args:
        b: записи извлечения B (``Entry`` с полем ``raw``).
        items: проверки листов по идентификатору.

    Returns:
        Черновик, сопоставление и список записей, не попавших в файл.

    Raises:
        DraftError: если в B нет записи, которой требует привязка, или значения γc2 двух
            столбцов различаются.
    """
    lists: dict[str, list[dict[str, Any]]] = {name: [] for name in LISTS}
    mapping: dict[str, dict[str, Any]] = {}
    notes: list[str] = []
    units = _symbol_units(b)

    def store(kind: str, key: str, record: dict[str, Any], local: Sequence[str]) -> None:
        mapping[f"{kind}/{key}"] = {
            "list": kind,
            "index": len(lists[kind]),
            "record_digest": record_digest(record),
            "items": {name: items[name].shown_digest for name in local},
        }
        lists[kind].append(record)

    r_raw = _raw(b, "r_formula_5_7")
    symbols = _tree_symbols(r_raw["tree"])
    r_units = {**units, **r_raw["units"], **OUTPUT_UNITS}
    store("formulas", "r", _formula("r", r_raw, r_raw["tree"], r_raw["latex"],
                                    {s: r_units[s] for s in sorted(symbols | set(OUTPUT_UNITS))}), ["r_formula_5_7"])
    notes.append("r: единица R (kPa) добавлена сборкой, на странице она не напечатана (B, notes); "
                 "единицы безразмерных символов взяты из ячеек таблиц и k_z в B")
    below = _raw(b, "k_z_formula_b_below_threshold")
    store("formulas", "k_z_below", _formula("k_z_below", below, below["tree"], below["latex"], below["units"]),
          ["k_z_formula_b_below_threshold"])
    frm = _raw(b, "k_z_formula_b_from_threshold")
    z0 = float(_raw(b, Z0_RECORD)["value"])
    tree = _substitute(frm["tree"], "z_0", z0)
    latex = frm["latex"].replace("z_{0}", f"{z0:g}")
    store("formulas", "k_z_from", _formula("k_z_from", frm, tree, latex,
                                           {k: v for k, v in frm["units"].items() if k != "z_0"}),
          ["k_z_formula_b_from_threshold", Z0_RECORD])
    notes.append(f"k_z_from: символ z_0 заменён числом {z0:g} в дереве и в LaTeX (запись {Z0_RECORD}, «здесь z_0 = 8 м»); "
                 "в B символ оставлен")
    row = _raw(b, CASE_ROW)
    c1 = _cell(row, GAMMA_C1_COLUMN)
    store("table_values", "gamma_c1", _table_value("gamma_c1", c1["symbol"], c1["latex"], c1["value"], c1["unit"], row), [CASE_ROW])
    c2 = [_cell(row, name) for name in GAMMA_C2_COLUMNS]
    if len({c["value"] for c in c2}) != 1:
        raise DraftError(f"{CASE_ROW}: the two gamma_c2 columns differ")
    store("table_values", "gamma_c2", _table_value("gamma_c2", c2[0]["symbol"], c2[0]["latex"], c2[0]["value"], c2[0]["unit"], row), [CASE_ROW])
    notes.append(f"gamma_c1, gamma_c2: строка {CASE_ROW} таблицы 5.4 (случай ex1); в обоих столбцах γc2 значение одно")
    k_raw = _raw(b, K_RECORD)
    store("table_values", "k", _table_value("k", "k", "k", float(k_raw["latex"].split("=")[1]), k_raw["units"]["k"], k_raw), [K_RECORD])
    notes.append("k: случай прочностных характеристик из испытаний; значение взято из LaTeX записи B")
    t55 = _raw(b, "t55")
    columns = {c["symbol"]: c for c in t55["columns"]}
    for symbol, parameter in M_PARAMETERS.items():
        for row55 in t55["rows"]:
            phi = row55["phi_II"]
            store("table_values", f"{parameter}@phi={phi}",
                  _table_value(parameter, symbol, columns[symbol]["latex"], row55[symbol], columns[symbol]["unit"], t55, phi),
                  [f"t55@phi={phi}"])
    thr = _raw(b, "k_z_threshold_b")
    store("thresholds", "k_z_threshold", {
        "parameter": "k_z_threshold", "latex": thr["latex"], "value": float(thr["value"]), "unit": thr["unit"],
        "norm_refs": _refs(thr), "page": thr["page"], "verification": dict(PENDING),
    }, ["k_z_threshold_b"])
    chk = _raw(b, "check_p_le_R")
    store("checks", "check_norm_refs", {
        "parameter": "check_norm_refs", "norm_refs": _refs(chk), "page": chk["page"], "verification": dict(PENDING),
    }, ["check_p_le_R"])
    covered = {name for entry in mapping.values() for name in entry["items"]}
    not_stored = {}
    for name in items:
        if name in covered:
            continue
        if name in NOT_STORED:
            not_stored[name] = NOT_STORED[name]
        elif name.startswith("t54_") and name in b:
            not_stored[name] = NOT_STORED_TABLE_54
        elif name.startswith("CP-"):
            continue
        else:
            raise DraftError(f"{name}: neither stored nor listed as not stored")
    return Draft(lists, mapping, notes, not_stored)


def render_notes(draft: Draft, today: str) -> str:
    """Формирует заметки к черновику для верификатора.

    Args:
        draft: результат ``build``.
        today: дата в виде ГГГГ-ММ-ДД.
    """
    out = [
        "# Черновик foundations_shallow_r: допущения сборки",
        "",
        f"Дата: {today}. Файл собран кодом из извлечения B (A не читает формулы и обозначения). "
        "Все записи `pending`. Что в файле:",
        "",
        *[f"- {name}: {len(draft.type_file[name])}" for name in LISTS],
        "",
        "## Допущения (проверяет верификатор)",
        "",
        *[f"- {note}" for note in draft.notes],
        "- method_bounds пуст: обе выписки не нашли границ в тексте.",
        "- Имена параметров — как в модели пилота (`Parameters`), не как в B; у A они совпадают с моделью.",
        "",
        "## Проверки листов без записи в файле",
        "",
        "| Проверка | Причина |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(draft.not_stored.items())],
    ]
    return "\n".join(out) + "\n"
