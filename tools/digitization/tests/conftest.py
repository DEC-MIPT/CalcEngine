import copy

import pytest

EDITION = "с Изменениями N 1, 2, 3, 4, 5 (сводный текст)"


def ref(clause: str, edition: str = EDITION) -> list[dict]:
    return [{"document": "DOC", "edition": edition, "clause": clause, "status": "unverified",
             "provenance": "machine-extracted"}]


def a_scalar(rec_id: str, **over) -> dict:
    rec = {
        "id": rec_id, "kind": "thresholds", "extraction": "text-layer",
        "extraction_status": "machine-extracted", "page": 36, "norm_refs": ref("5.6.7"),
        "parameter": "p", "latex": None, "value": 10, "unit": "m",
        "verification": {"status": "pending"},
    }
    rec.update(over)
    return rec


def b_scalar(rec_id: str, **over) -> dict:
    rec = {
        "id": rec_id, "parameter": "p", "latex": "x=10", "value": 10.0, "unit": "m", "page": 36,
        "region": "reg", "norm_refs": ref("5.6.7", "2016 (с Изменениями N 1, 2, 3, 4, 5)"),
        "extraction": {"method": "image", "status": "machine-extracted", "notes": ["n"]},
        "verification": {"status": "pending"},
    }
    rec.update(over)
    return rec


def a_t54(rec_id: str, values=(1.4, 1.2, 1.4), **over) -> dict:
    headers = ["Коэффициент", "жесткой, L/H 4 и более", "жесткой, L/H 1,5 и менее"]
    rec = {
        "id": rec_id, "kind": "table_values", "extraction": "text-layer",
        "extraction_status": "machine-extracted", "page": 37, "norm_refs": ref("5.6.7, таблица 5.4"),
        "parameter": "g", "condition_status": "text-layer",
        "columns": [
            {"position": i + 1, "header_in_layer": headers[i], "symbol": None, "value": v}
            for i, v in enumerate(values)
        ],
        "verification": {"status": "pending"},
    }
    rec.update(over)
    return rec


def b_t54(rec_id: str, values=(1.4, 1.2, 1.4), **over) -> dict:
    cells = [
        {"column": "c1", "symbol": "gamma_c1", "value": values[0]},
        {"column": "c2", "symbol": "gamma_c2", "value": values[1], "heading_relation": "≥", "heading_value": 4.0},
        {"column": "c3", "symbol": "gamma_c2", "value": values[2], "heading_relation": "≤", "heading_value": 1.5},
    ]
    rec = {
        "id": rec_id, "parameter": "g", "page": 37, "region": "row", "cells": cells,
        "norm_refs": ref("5.6.7, таблица 5.4", "2016 (с Изменениями N 1, 2, 3, 4, 5)"),
        "extraction": {"status": "ambiguous", "notes": []}, "verification": {"status": "pending"},
    }
    rec.update(over)
    return rec


def a_t55(rows=((0, (0.0, 1.0, 3.14)), (1, (0.01, 1.06, 3.23)))) -> dict:
    return {
        "id": "t55", "kind": "table_values", "extraction_status": "machine-extracted", "page": 38,
        "norm_refs": ref("5.6.7, таблица 5.5"), "parameter": "m",
        "columns": [{"position": i, "symbol": None} for i in (1, 2, 3)],
        "rows": [{"selector_deg": s, "values": list(v), "raw": []} for s, v in rows],
        "verification": {"status": "pending"},
    }


def b_t55(rows=((0, (0.0, 1.0, 3.14)), (1, (0.01, 1.06, 3.23)))) -> dict:
    return {
        "id": "t55", "parameter": "m", "page": 38, "pages": [37, 38], "region": "tbl",
        "norm_refs": ref("5.6.7, таблица 5.5", "2016 (с Изменениями N 1, 2, 3, 4, 5)"),
        "columns": [{"symbol": "M_gamma", "position": 1}, {"symbol": "M_q", "position": 2},
                    {"symbol": "M_c", "position": 3}],
        "rows": [{"phi_II": s, "M_gamma": v[0], "M_q": v[1], "M_c": v[2]} for s, v in rows],
        "extraction": {"status": "machine-extracted", "notes": []}, "verification": {"status": "pending"},
    }


MARK_A = {"page": 37, "mark": "(Измененная редакция, Изм. № 5).", "position": "после примечания 6"}
MARK_B = {"page": 37, "text": "(Измененная редакция, Изм. № 5).", "region": "y 345", "binding": "unknown"}


@pytest.fixture
def extracts() -> tuple[dict, dict]:
    a = {"source": {"edition_as_printed": "(с Изменениями N 1, 2, 3, 4, 5)"}, "records": [
        a_scalar("thr"),
        a_scalar("r_formula_5_7", kind="formulas", extraction_status="needs-image", also=["ambiguous"],
                 parameter="r", value=None, unit=None, change_marks=[MARK_A], note="картинка"),
        a_scalar("kc", kind="formulas", value=1, unit=None, parameter="k", raw_in_layer="равным единице при b<10 м"),
        a_t54("t54_aaa"), a_t54("t54_bbb", values=(1.3, 1.1, 1.3)),
        a_scalar("t54_notes", kind="table_values", extraction_status="needs-image", value=None, unit=None, page=37,
                norm_refs=ref("5.6.7, таблица 5.4")),
        a_t55(),
        a_scalar("method_bounds_none", kind="method_bounds", extraction_status="not-found", value=None, unit=None),
    ]}
    b = {"meta": {"edition": {"printed_header": "СП (с Изменениями N 1, 2, 3, 4, 5)"}},
         "amendment_marks": [{"page": 37, "text": "(Измененная редакция, Изм. N 5).", "region": "r", "binding": "unknown"}],
         "formulas": [
             b_scalar("r_formula_5_7", parameter="r", value=None, unit=None, latex="R=a\\cdot b", nearby_marks=[MARK_B],
                      extraction={"method": "image", "status": "ambiguous", "notes": []}),
             b_scalar("kc", parameter="k", value=None, unit=None, latex="k=1", condition="b < 10 м"),
         ],
         "table_values": [b_t54("t54_xxx"), b_t54("t54_yyy", values=(1.3, 1.1, 1.3)),
                          {"id": "t54_notes", "notes_read": [{"note": 1}], "page": 37, "region": "n",
                           "norm_refs": ref("5.6.7, таблица 5.4"),
                           "extraction": {"status": "ambiguous", "notes": []}}, b_t55()],
         "thresholds": [b_scalar("thr", latex=None)],
         "checks": [],
         "method_bounds": [b_scalar("method_bounds_none", value=None, unit=None, latex=None,
                                   extraction={"status": "not-found", "notes": []}, page=None, region=None)],
         "extra_records": [b_scalar("extra1", latex="d=2")]}
    return a, b


@pytest.fixture
def fresh(extracts):
    return lambda: copy.deepcopy(extracts)


@pytest.fixture
def mutable(fresh):
    return fresh()
