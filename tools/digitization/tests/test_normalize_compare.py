from collections import Counter

import pytest

from extractcmp import normalize as n
from extractcmp.compare import align, compare_all
from tests.conftest import a_t54, a_t55, b_t54, b_t55


def test_number_helpers():
    assert n.to_number("1,25") == 1.25
    assert n.numbers_in("0,25 < I_L ≤ 0,5") == (0.25, 0.5)
    assert n.numbers_in(None) == ()


@pytest.mark.parametrize(
    ("text", "expected"),
    [("b<10 м", ("<", 10.0)), ("b ≥ 10 м", ("≥", 10.0)), ("I_L <= 0,25", ("≤", 0.25)), ("при b 10 м", None), (None, None)],
)
def test_parse_condition(text, expected):
    assert n.parse_condition(text) == expected


def test_header_relation():
    assert n.parse_header_relation("L/H 4 и более") == ("≥", 4.0)
    assert n.parse_header_relation("L/H 1,5 и менее") == ("≤", 1.5)
    assert n.parse_header_relation("Коэффициент") is None
    assert n.parse_header_relation(None) is None


@pytest.mark.parametrize(
    ("latex", "expected"),
    [("k=1", 1.0), ("k=1{,}1", 1.1), ("k_{z}=1", 1.0), ("R=a\\cdot b", None), (None, None), ("z_{0}=8\\ \\text{м}", None)],
)
def test_latex_constant(latex, expected):
    assert n.parse_latex_constant(latex) == expected


def test_latex_tokens_ignore_grouping_and_synonyms():
    assert n.latex_tokens("a\\leq b") == n.latex_tokens("a \\le b")
    assert n.latex_tokens("\\left[x\\right]") == n.latex_tokens("[x]")
    assert n.latex_tokens("0{,}2") == ["0.2"]
    assert n.latex_tokens("x_{1}") == n.latex_tokens("x_1")


def test_clause_and_amendments():
    refs = [{"clause": "5.6.7, формула (5.7)"}, {"clause": "5.6.7, таблица 5.4"}]
    assert n.clause_key(refs) == ("5.6.7", "5.7", "5.4")
    assert n.clause_key(None) == ()
    assert n.amendment_numbers("с Изменениями N 1, 2, 5 (сводный)") == frozenset({1, 2, 5})
    assert n.amendment_numbers("2016") == frozenset()
    assert n.amendment_numbers(None) == frozenset()


def test_loaders(extracts):
    a, b = n.load_a(extracts[0]), n.load_b(extracts[1])
    assert a["r_formula_5_7"].ambiguous and a["r_formula_5_7"].status == "needs-image"
    assert a["kc"].fields["condition"] == ("<", 10.0)
    assert b["kc"].fields["value"] == 1.0
    assert b["extra1"].kind == "extra_records"
    assert b["t54_xxx"].shape == "t54row" and a["t54_bbb"].order == 1
    assert b["t55"].pages == (37, 38) and b["method_bounds_none"].pages == ()
    assert b["r_formula_5_7"].marks[0].binding == "unknown"
    assert a["thr"].amendments == frozenset({1, 2, 3, 4, 5})


def run(extracts):
    return compare_all(n.load_a(extracts[0]), n.load_b(extracts[1]))


def by_key(results):
    return {r.key: r for r in results}


def test_alignment_by_order(extracts):
    results, aliases = run(extracts)
    assert aliases == {"t54_aaa": "t54_xxx", "t54_bbb": "t54_yyy"}
    assert {"t54_xxx", "t54_yyy"} <= set(by_key(results))


def test_outcomes_on_clean_data(extracts):
    results, _ = run(extracts)
    got = by_key(results)
    assert got["thr"].outcome == "match"
    assert got["method_bounds_none"].outcome == "not-found"
    assert got["extra1"].outcome == "only-b"
    assert got["t54_notes"].outcome == "image-only"
    assert got["r_formula_5_7"].outcome == "partial"
    assert got["kc"].outcome == "partial"
    assert got["t55"].outcome == "partial"
    assert got["t54_xxx"].outcome == "partial"
    assert not [f for r in results for f in r.findings if f.kind in ("value", "table-structure", "formula-symbols")]


def test_value_difference_in_scalar_and_table(mutable):
    a, b = mutable
    b["thresholds"][0]["value"] = 12.0
    b["table_values"][0] = b_t54("t54_xxx", values=(1.4, 1.25, 1.4))
    got = by_key(run((a, b))[0])
    assert got["thr"].outcome == "diff"
    assert {(f.kind, f.field) for f in got["thr"].findings} == {("value", "value")}
    assert [(f.field, f.a, f.b) for f in got["t54_xxx"].findings if f.kind == "value"] == [("col2.value", 1.2, 1.25)]


def test_t55_cell_and_structure_differences(mutable):
    a, b = mutable
    b["table_values"][3] = b_t55(rows=((0, (0.0, 1.0, 3.15)), (1, (0.01, 1.06, 3.23))))
    got = by_key(run((a, b))[0])["t55"]
    assert [(f.field, f.a, f.b) for f in got.findings if f.kind == "value"] == [("row[0].col3", 3.14, 3.15)]
    b["table_values"][3] = b_t55(rows=((0, (0.0, 1.0, 3.14)),))
    got = by_key(run((a, b))[0])["t55"]
    kinds = Counter(f.field for f in got.findings if f.kind == "table-structure")
    assert kinds == {"rows": 1, "selectors": 1}
    b["table_values"][3] = b_t55(rows=((0, (0.0, 1.0, 3.14)), (2, (0.01, 1.06, 3.23))))
    got = by_key(run((a, b))[0])["t55"]
    assert any(f.field == "selectors" for f in got.findings)


def test_t55_column_count_and_symbols(mutable, fresh):
    a, b = mutable
    a["records"][6]["rows"][0]["values"] = [0.0, 1.0]
    assert any(f.field == "row[0].columns" for f in by_key(run((a, b))[0])["t55"].findings)
    a2, b2 = fresh()
    a2["records"][6]["columns"][0]["symbol"] = "Mg"
    assert any(f.kind == "formula-symbols" for f in by_key(run((a2, b2))[0])["t55"].findings)
    a3, b3 = fresh()
    for c in a3["records"][6]["columns"]:
        c["symbol"] = ["M_gamma", "M_q", "M_c"][c["position"] - 1]
    assert by_key(run((a3, b3))[0])["t55"].outcome == "match"


def test_t54_structure_and_symbols(mutable, fresh):
    a, b = mutable
    b["table_values"][0]["cells"].pop()
    assert any(f.field == "columns" for f in by_key(run((a, b))[0])["t54_xxx"].findings)
    a2, b2 = fresh()
    b2["table_values"][0]["cells"][1]["heading_relation"] = "≤"
    assert any(f.field == "col2.header" for f in by_key(run((a2, b2))[0])["t54_xxx"].findings)
    a3, b3 = fresh()
    a3["records"][3]["columns"][0]["symbol"] = "g_c1"
    assert any(f.kind == "formula-symbols" for f in by_key(run((a3, b3))[0])["t54_xxx"].findings)


def test_t54_condition_numbers():
    a = n.load_a({"records": [a_t54("t54_r", condition_note="в слое 0,25", condition_status="needs-image")]})
    b = n.load_b({"table_values": [b_t54("t54_s", condition="I_L ≤ 0,25")]})
    got = compare_all(a, b)[0][0]
    assert got.outcome == "partial" and got.matched >= 5
    b2 = n.load_b({"table_values": [b_t54("t54_s", condition="I_L ≤ 0,3")]})
    assert compare_all(a, b2)[0][0].outcome == "diff"
    a3 = n.load_a({"records": [a_t54("t54_r", condition_status="needs-image")]})
    got3 = compare_all(a3, b)[0][0]
    assert any(f.field == "condition" and f.kind == "field-only-b" for f in got3.findings)


def test_formula_symbols_and_conditions(mutable, fresh):
    a, b = mutable
    a["records"][1]["latex"] = "R=a\\cdot c"
    a["records"][1]["extraction_status"] = "machine-extracted"
    got = by_key(run((a, b))[0])["r_formula_5_7"]
    finding = next(f for f in got.findings if f.kind == "formula-symbols")
    assert "'c'" in finding.note and "'b'" in finding.note
    a["records"][1]["latex"] = "R=a*b"
    assert by_key(run((a, b))[0])["r_formula_5_7"].outcome == "match"
    a2, b2 = fresh()
    b2["formulas"][1]["condition"] = "b ≥ 10 м"
    assert any(f.field == "condition" and f.kind == "formula-symbols" for f in by_key(run((a2, b2))[0])["kc"].findings)
    a3, b3 = fresh()
    a3["records"][2]["value"] = None
    got = by_key(run((a3, b3))[0])["kc"]
    assert any(f.kind == "field-only-b" and f.field == "value" for f in got.findings)
    a4, b4 = fresh()
    b4["formulas"][1]["latex"] = None
    got = by_key(run((a4, b4))[0])["kc"]
    assert got.outcome == "partial" and not any(f.field == "latex" for f in got.findings)


def test_one_side_only_fields(mutable):
    a, b = mutable
    a["records"][0]["unit"] = "m"
    b["thresholds"][0]["unit"] = None
    got = by_key(run((a, b))[0])["thr"]
    assert [f.kind for f in got.findings] == ["field-only-a"]
    assert got.outcome == "partial"


def test_not_found_conflict_and_notes_sides(mutable, fresh):
    a, b = mutable
    b["method_bounds"][0]["extraction"]["status"] = "machine-extracted"
    got = by_key(run((a, b))[0])["method_bounds_none"]
    assert got.outcome == "diff" and got.findings[0].kind == "status"
    a2, b2 = fresh()
    b2["table_values"][2]["notes_read"] = []
    a2["records"][5]["extraction_status"] = "machine-extracted"
    assert any(f.kind == "field-only-a" for f in by_key(run((a2, b2))[0])["t54_notes"].findings)
    a3, b3 = fresh()
    a3["records"][5]["extraction_status"] = "machine-extracted"
    assert by_key(run((a3, b3))[0])["t54_notes"].outcome == "match"


def test_metadata_page_and_clause(mutable):
    a, b = mutable
    b["thresholds"][0]["page"] = 40
    b["thresholds"][0]["norm_refs"] = [{"clause": "5.9.1", "edition": "x"}]
    got = by_key(run((a, b))[0])["thr"]
    assert {f.field for f in got.findings} == {"page", "clause"}
    assert got.outcome == "metadata-diff"


def test_only_a_and_ordering(mutable):
    a, b = mutable
    b["thresholds"] = []
    results, _ = run((a, b))
    assert by_key(results)["thr"].outcome == "only-a"
    priorities = [r.priority for r in results]
    assert priorities == sorted(priorities)
    assert results[0].priority == 0 and results[-1].priority == 2
    assert by_key(results)["thr"].flags == []


def test_align_without_t54_in_b():
    a = n.load_a({"records": [a_t54("t54_one"), a_t54("t54_two")]})
    b = n.load_b({"table_values": [b_t54("t54_x")]})
    pairs, aliases = align(a, b)
    assert aliases == {"t54_one": "t54_x"}
    assert [(k, x is not None, y is not None) for k, x, y in pairs] == [("t54_x", True, True), ("t54_two", True, False)]


def test_a_t55_helpers_exist():
    assert a_t55()["rows"][0]["selector_deg"] == 0
