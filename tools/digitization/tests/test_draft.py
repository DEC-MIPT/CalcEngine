import copy
from datetime import date

import pytest
import yaml

from extractcmp import cli, draft, promote
from extractcmp.normalize import load_b
from extractcmp.portions import Item

REFS = [{"document": "D", "edition": "E", "clause": "5.6.7", "status": "unverified", "provenance": "machine-extracted"}]
EXT = {"extraction": {"status": "ambiguous", "notes": []}, "norm_refs": REFS, "verification": {"status": "pending"}}


def num(value):
    return {"kind": "number", "value": value}


def sym(name):
    return {"kind": "symbol", "name": name}


def cell(column, symbol, value):
    return {"column": column, "symbol": symbol, "latex": symbol, "value": value, "unit": "1"}


def synthetic_b():
    return {
        "formulas": [
            {"id": "r_formula_5_7", "result_symbol": "R", "latex": "R=...", "page": 36, "units": {"b": "m"},
             "tree": {"kind": "mul", "left": sym("gamma_c1"), "right": {"kind": "mul", "left": sym("k_z"), "right": sym("b")}}, **EXT},
            {"id": "k_z_formula_b_below_threshold", "result_symbol": "k_z", "latex": "k_{z}=1", "page": 36,
             "units": {"k_z": "1"}, "tree": num(1.0), **EXT},
            {"id": "k_z_formula_b_from_threshold", "result_symbol": "k_z", "latex": "k_{z}=z_{0}/b+0{,}2", "page": 36,
             "units": {"k_z": "1", "z_0": "m", "b": "m"},
             "tree": {"kind": "add", "left": {"kind": "div", "left": sym("z_0"), "right": sym("b")}, "right": num(0.2)}, **EXT},
            {"id": "k_direct_tests", "result_symbol": "k", "latex": "k=1", "page": 36, "units": {"k": "1"}, "tree": num(1.0), **EXT},
        ],
        "table_values": [
            {"id": "t54_clayey_il_gt_0_5", "page": 37, "cells": [
                cell("c1", "gamma_c1", 1.1), cell("c2_ge4", "gamma_c2", 1.0), cell("c2_le15", "gamma_c2", 1.0)], **EXT},
            {"id": "t54_other", "page": 37, "cells": [cell("c1", "gamma_c1", 1.4)], **EXT},
            {"id": "t54_notes", "page": 37, "notes_read": [1], **EXT},
            {"id": "t55", "page": 38, "pages": [37, 38],
             "columns": [{"symbol": s, "latex": s, "unit": "1"} for s in ("M_gamma", "M_q", "M_c")],
             "rows": [{"phi_II": p, "M_gamma": 0.1 * p, "M_q": 1.0 + p, "M_c": 3.0 + p} for p in (0, 1)], **EXT},
        ],
        "thresholds": [
            {"id": "k_z_threshold_b", "latex": "b\\geq 10", "value": 10.0, "unit": "m", "page": 36, **EXT},
            {"id": "z0_in_k_z", "value": 8.0, "unit": "m", "page": 36, **EXT},
        ],
        "checks": [{"id": "check_p_le_R", "page": 35, "pages": [35, 36], **EXT}],
        "extra_records": [{"id": "d_b_cap_2m", "page": 36, **EXT}],
    }


def items_for(names):
    return {n: Item(n, n, "P1", "record", n, "1", "-", [], "", "", shown_digest=f"digest-{n}") for n in names}


NAMES = ["r_formula_5_7", "k_z_formula_b_below_threshold", "k_z_formula_b_from_threshold", "z0_in_k_z", "k_direct_tests",
         "t54_clayey_il_gt_0_5", "t54_other", "t54_notes", "t55@phi=0", "t55@phi=1", "k_z_threshold_b", "check_p_le_R",
         "d_b_cap_2m", "edition", "CP-R-1"]


def built(b=None):
    return draft.build(load_b(b or synthetic_b()), items_for(NAMES))


def test_lists_and_pilot_parameter_names():
    result = built()
    names = {kind: [r["parameter"] for r in rows] for kind, rows in result.type_file.items()}
    assert names["formulas"] == ["r", "k_z_below", "k_z_from"]
    assert names["table_values"] == ["gamma_c1", "gamma_c2", "k", "m_gamma", "m_gamma", "m_q", "m_q", "m_c", "m_c"]
    assert names["thresholds"] == ["k_z_threshold"] and names["checks"] == ["check_norm_refs"]
    assert result.type_file["method_bounds"] == []
    assert all(r["verification"] == {"status": "pending"} for rows in result.type_file.values() for r in rows)


def test_formula_units_and_the_z0_substitution():
    formulas = {r["parameter"]: r for r in built().type_file["formulas"]}
    assert formulas["r"]["units"] == {"R": "kPa", "b": "m", "gamma_c1": "1", "k_z": "1"}
    assert formulas["k_z_from"]["tree"]["left"]["left"] == num(8.0)
    assert "z_{0}" not in formulas["k_z_from"]["latex"] and "8/b" in formulas["k_z_from"]["latex"]
    assert "z_0" not in formulas["k_z_from"]["units"]


def test_table_rows_carry_the_heading():
    rows = [r for r in built().type_file["table_values"] if r["parameter"] == "m_q"]
    assert [(r["heading_symbol"], r["heading_value"], r["heading_unit"], r["value"]) for r in rows] == [
        ("phi_II", 0.0, "deg", 1.0), ("phi_II", 1.0, "deg", 2.0)]
    gamma = built().type_file["table_values"][0]
    assert gamma["value"] == 1.1 and gamma["heading_symbol"] is None and gamma["page"] == 37
    k = next(r for r in built().type_file["table_values"] if r["parameter"] == "k")
    assert (k["value"], k["symbol"], k["latex"]) == (1.0, "k", "k")


def test_mapping_points_at_records_and_shared_items():
    result = built()
    for key, where in result.mapping.items():
        record = result.type_file[where["list"]][where["index"]]
        assert where["record_digest"] == promote.record_digest(record), key
    assert result.mapping["table_values/m_q@phi=1"]["items"] == {"t55@phi=1": "digest-t55@phi=1"}
    assert result.mapping["table_values/m_c@phi=1"]["items"] == result.mapping["table_values/m_q@phi=1"]["items"]
    assert set(result.mapping["formulas/k_z_from"]["items"]) == {"k_z_formula_b_from_threshold", "z0_in_k_z"}


def test_not_stored_items_are_explained():
    result = built()
    assert set(result.not_stored) == {"t54_other", "t54_notes", "d_b_cap_2m", "edition"}
    assert "таблицы 5.4" in result.not_stored["t54_other"] and "примечания" in result.not_stored["t54_notes"]


def test_unlisted_item_is_an_error():
    with pytest.raises(draft.DraftError, match="neither stored nor listed"):
        draft.build(load_b(synthetic_b()), items_for([*NAMES, "mystery"]))


def test_missing_records_and_differing_gamma_c2():
    b = synthetic_b()
    b["formulas"].pop(0)
    with pytest.raises(draft.DraftError, match="no record 'r_formula_5_7'"):
        built(b)
    b = synthetic_b()
    b["table_values"][0]["cells"][2]["value"] = 1.2
    with pytest.raises(draft.DraftError, match="columns differ"):
        built(b)
    b = synthetic_b()
    b["table_values"][0]["cells"].pop(0)
    with pytest.raises(draft.DraftError, match="no column 'c1'"):
        built(b)


def test_render_notes_lists_everything():
    text = draft.render_notes(built(), "2026-10-22")
    assert "formulas: 3" in text and "z_0" in text and "| d_b_cap_2m |" in text


def test_promote_with_shared_items_and_record_keyed_corrections():
    result = built()
    d = copy.deepcopy(result.type_file)
    mapping = {k: result.mapping[k] for k in ("table_values/m_q@phi=1", "table_values/m_c@phi=1")}
    item = {"item": "P2-1/t55@phi=1", "record": "t55", "kind": "table-row", "page": "38",
            "shown_digest": "digest-t55@phi=1", "verdict": "исправить",
            "corrected": {"table_values/m_q@phi=1": {"value": 2.5}}, "by": "Vera", "at": "2026-10-25", "comment": None}
    sheet = promote.sign_sheet({"portion": "P2-1", "items": [item]}, "Vera", date(2026, 10, 25))
    out, lines = promote.promote(d, mapping, [sheet], ["Vera"])
    q, c = (out["table_values"][mapping[k]["index"]] for k in mapping)
    assert q["value"] == 2.5 and c["value"] == 4.0
    assert q["verification"] == c["verification"] == {"status": "pending"}
    assert len(lines) == 2


def test_cli_draft(tmp_path):
    b = synthetic_b()
    (tmp_path / "b.yaml").write_text(yaml.safe_dump(b, allow_unicode=True), encoding="utf-8")
    a = {"records": []}
    (tmp_path / "a.yaml").write_text(yaml.safe_dump(a), encoding="utf-8")
    code = cli.main(["draft", "--a", str(tmp_path / "a.yaml"), "--b", str(tmp_path / "b.yaml"), "--out", str(tmp_path / "t.yaml"),
                     "--mapping-out", str(tmp_path / "m.yaml"), "--notes-out", str(tmp_path / "n.md"), "--date", "2026-10-22"])
    assert code == 0
    written = yaml.safe_load((tmp_path / "t.yaml").read_text(encoding="utf-8"))
    assert [r["parameter"] for r in written["formulas"]] == ["r", "k_z_below", "k_z_from"]
    assert "formulas/r" in yaml.safe_load((tmp_path / "m.yaml").read_text(encoding="utf-8"))
    assert (tmp_path / "n.md").exists()
