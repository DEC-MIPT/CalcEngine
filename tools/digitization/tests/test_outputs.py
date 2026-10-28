from datetime import date
from pathlib import Path

import yaml

from extractcmp import checkpoints, marks, portions, report
from extractcmp.compare import compare_all
from extractcmp.normalize import load_a, load_b
from tests.conftest import a_scalar, b_scalar

TODAY = date(2026, 10, 22)
EX1 = yaml.safe_load((Path(__file__).resolve().parent.parent / "data" / "ex1.yaml").read_text(encoding="utf-8"))
PACKAGE = Path(__file__).resolve().parent.parent / "extractcmp"


def prepared(extracts):
    a, b = load_a(extracts[0]), load_b(extracts[1])
    results, aliases = compare_all(a, b)
    return a, b, results, aliases


def test_report_sections_and_counts(extracts):
    a, b, results, aliases = prepared(extracts)
    text = report.render(results, aliases, report.edition_map(a), report.edition_map(b), TODAY, "a.yaml", "b.yaml")
    for heading in ("## 1. Итоги", "### 3.1 По значению", "### 3.5 По метаданным", "## 4.", "## 6.", "## 7."):
        assert heading in text
    assert "Записей: в A 8, в B 9" in text
    assert "t54_aaa" in text and "extra1" in text
    assert "[1, 2, 3, 4, 5]" in text
    assert report.summary(results)["only-b"] == 1


def test_report_lists_differences(mutable):
    a, b = mutable
    b["thresholds"][0]["value"] = 12.0
    b["thresholds"][0]["norm_refs"][0]["edition"] = "2016 (с Изменениями N 1, 2)"
    ea, eb = load_a(a), load_b(b)
    results, aliases = compare_all(ea, eb)
    text = report.render(results, aliases, report.edition_map(ea), report.edition_map(eb), TODAY, "a", "b")
    assert "| thr | value | 10.0 | 12.0 |" in text
    assert "различаются" in text
    only = report.render([], {}, {}, {}, TODAY, "a", "b")
    assert "Таких записей нет." in only and "Таких полей нет." in only


def test_full_match_is_listed(mutable):
    a, b = mutable
    a["records"][5]["extraction_status"] = "machine-extracted"
    ea, eb = load_a(a), load_b(b)
    results, aliases = compare_all(ea, eb)
    text = report.render(results, aliases, {}, {}, TODAY, "a", "b")
    assert "### совпали полностью" in text


def test_marks_document(extracts):
    a, b = load_a(extracts[0]), load_b(extracts[1])
    text = marks.render(
        a, b, extracts[1]["amendment_marks"],
        "строка без пометки\nНа стр. 35 «Изм. N 1, 5».\n", "",
    )
    assert "Запись формулы (5.7) в A и B" in text
    assert "пометка записи: страница 37; «(Измененная редакция, Изм. № 5).»; место: после примечания 6" in text
    assert "привязка: unknown" in text
    assert "- строка 2: На стр. 35 «Изм. N 1, 5»." in text and "- нет строк." in text
    assert "Вывод" not in text.replace("Вывода нет", "")
    assert marks.normalize_mark("Изм. № 5") == "Изм. N 5"
    assert marks.report_lines("нет\nИзм.") == [(2, "Изм.")]


def test_marks_without_formula_record():
    text = marks.render({}, {}, [], "", "")
    assert text.count("записи нет.") == 2


def test_marks_many_records_are_abbreviated(extracts):
    text = marks._ids({"a", "b", "c", "d", "e"})
    assert text.startswith("5 записей:") and marks._ids(set()) == "—"


def test_control_points_never_invent_outputs(extracts):
    a, b = load_a(extracts[0]), load_b(extracts[1])
    points = checkpoints.build(EX1, a["t55"], b["t55"])
    sourced = [p for p in points if p.sourced]
    assert {p.cp_id for p in sourced} == {"CP-R-1", "CP-R-2", "CP-KZ-1", "CP-K-1", "CP-T54-1", "CP-T55-1", "CP-CHK-1"}
    allowed = {str(v["value"]) for v in EX1["inputs_r"].values()}
    allowed |= {EX1["r_initial"]["r"] + " kPa", EX1["r_refined"]["r"] + " kPa", EX1["table_54"]["gamma_c1"],
                EX1["table_54"]["gamma_c2"], EX1["check"]["outcome"], *[EX1["table_55"][k] for k in ("M_gamma", "M_q", "M_c")]}
    for p in sourced:
        assert {v for v in p.expected.values() if v is not None} <= allowed
    for p in points:
        if not p.sourced:
            assert any(v is None for v in p.expected.values())
    assert next(p for p in points if p.cp_id == "CP-R-2").expected["допуск"] is None


def test_control_point_lookup_reports_extraction_rows():
    from extractcmp.normalize import load_a as la
    from extractcmp.normalize import load_b as lb
    from tests.conftest import a_t55, b_t55
    rows = ((19, (0.47, 2.89, 5.48)),)
    a, b = la({"records": [a_t55(rows)]}), lb({"table_values": [b_t55(rows)]})
    point = next(p for p in checkpoints.build(EX1, a["t55"], b["t55"]) if p.cp_id == "CP-T55-1")
    assert "A совпадает с методичкой: True; B совпадает: True" in point.note
    none = next(p for p in checkpoints.build(EX1, None, None) if p.cp_id == "CP-T55-1")
    assert "A None, B None" in none.note and "False" in none.note


def test_control_points_render(extracts):
    points = checkpoints.build(EX1, None, None)
    text = checkpoints.render(points, EX1)
    assert "из методички, редакция не подтверждена" in text
    assert "| CP-R-2 | P1 |" in text and "допуск = …" in text


def all_items(extracts):
    a, b, results, _ = prepared(extracts)
    points = checkpoints.build(EX1, a["t55"], b["t55"])
    return results, [
        *portions.record_items(results),
        portions.edition_item("A ed", "B ed"),
        *portions.control_point_items(points, EX1["label"]),
    ]


def test_every_record_and_table_row_has_an_item(extracts):
    results, items = all_items(extracts)
    records = {i.record for i in items}
    assert {r.key for r in results} <= records
    assert {"t55@phi=0", "t55@phi=1"} <= {i.item_id for i in items}
    assert len({i.item_id for i in items}) == len(items)
    assert all(i.group in portions.GROUPS for i in items)


def test_records_outside_the_pilot_file_and_their_points_are_deferred(mutable):
    a, b = mutable
    b["extra_records"].append(b_scalar("d_b_cap_2m", latex="d_{b}=2"))
    _, items = all_items((a, b))
    group = {i.item_id: i.group for i in items}
    assert group["d_b_cap_2m"] == group["CP-RULE-2"] == group["CP-D1-1"] == group["CP-K-2"] == "D"
    assert group["extra1"] == group["CP-R-1"] == "P1"
    parts = portions.split(items)
    assert parts[-1].portion_id == "D-1"
    assert "Порции D" in portions.render_index(parts, TODAY)
    assert "отложено" in portions.render_markdown(parts[-1], TODAY, "label")


def test_z0_goes_to_the_portion_of_the_k_z_formula(mutable):
    a, b = mutable
    a["records"] += [a_scalar("k_z_formula_b_from_threshold", kind="formulas"), a_scalar("z0_in_k_z")]
    b["formulas"].append(b_scalar("k_z_formula_b_from_threshold", latex="k_{z}=z_{0}/b+0{,}2"))
    b["thresholds"].append(b_scalar("z0_in_k_z"))
    results, _ = compare_all(load_a(a), load_b(b))
    items = {i.item_id: i for i in portions.record_items(results)}
    assert (items["z0_in_k_z"].record, items["z0_in_k_z"].group) == ("k_z_formula_b_from_threshold", "P1")
    assert items["thr"].group == "P3"
    parts = portions.split(list(items.values()), minutes=1)
    owner = {i.item_id: p.portion_id for p in parts for i in p.items}
    assert owner["z0_in_k_z"] == owner["k_z_formula_b_from_threshold"]


def test_z0_without_its_formula_keeps_its_group(mutable):
    a, b = mutable
    a["records"].append(a_scalar("z0_in_k_z"))
    b["thresholds"].append(b_scalar("z0_in_k_z"))
    results, _ = compare_all(load_a(a), load_b(b))
    items = {i.item_id: i for i in portions.record_items(results)}
    assert (items["z0_in_k_z"].record, items["z0_in_k_z"].group) == ("z0_in_k_z", "P3")


def test_t55_row_difference_flagged(mutable):
    a, b = mutable
    b["table_values"][3]["rows"][1]["M_q"] = 9.0
    results, _ = compare_all(load_a(a), load_b(b))
    rows = [i for i in portions.record_items(results) if i.kind == "table-row"]
    assert [i.priority for i in rows] == [2, 0]
    assert rows[1].minutes > rows[0].minutes
    first = next(i for i in rows if i.item_id == "t55@phi=0")
    assert first.a == "[0.0, 1.0, 3.14]"


def test_describe_variants(extracts):
    a, b = load_a(extracts[0]), load_b(extracts[1])
    assert portions.describe(None) == "нет записи"
    assert "значения: [1.4, 1.2, 1.4]" in portions.describe(a["t54_aaa"])
    assert "обозначения столбцов: [gamma_c1, gamma_c2, gamma_c2]" in portions.describe(b["t54_xxx"])
    assert portions.describe(a["t54_notes"]) == "не прочитаны (needs-image)"
    assert portions.describe(b["t54_notes"]) == "примечания прочитаны"
    assert portions.describe(a["t55"]).startswith("строк: 2")
    bare = dict(extracts[0]["records"][7], parameter=None)
    assert portions.describe(load_a({"records": [bare]})["method_bounds_none"]) == "содержимого нет (статус not-found)"
    assert "latex: R=a\\cdot b" in portions.describe(b["r_formula_5_7"])


def test_split_keeps_records_whole_and_orders_by_priority(extracts):
    _, items = all_items(extracts)
    parts = portions.split(items, minutes=10)
    assert [p.portion_id for p in parts[:2]] == ["P1-1", "P1-2"]
    seen = {}
    for p in parts:
        for i in p.items:
            seen.setdefault(i.record, set()).add(p.portion_id)
    assert all(len(v) == 1 for v in seen.values())
    p1 = [i for p in parts for i in p.items if i.group == "P1"]
    assert [i.priority for i in p1] == sorted(i.priority for i in p1)
    assert sum(len(p.items) for p in parts) == len(items)
    assert portions.portions_of(parts, "P2")


def test_sheet_and_markdown_carry_no_verdicts(extracts):
    _, items = all_items(extracts)
    portion = portions.split(items)[0]
    sheet = portions.render_sheet(portion, TODAY, {"a": "a.yaml", "b": "b.yaml"})
    assert sheet["signature"] is None
    assert all(i["verdict"] is None and i["by"] is None and i["at"] is None for i in sheet["items"])
    assert sheet["verdicts_allowed"] == ["верно", "исправить", "отклонить"]
    assert all(i["item"].startswith(portion.portion_id + "/") for i in sheet["items"])
    text = portions.render_markdown(portion, TODAY, EX1["label"])
    assert "☐ верно  ☐ исправить  ☐ отклонить" in text
    p2 = next(p for p in portions.split(items) if p.group == "P2")
    assert "| φ_II | A | B |" in portions.render_markdown(p2, TODAY, EX1["label"])
    index = portions.render_index(portions.split(items), TODAY)
    assert "≈" in index and "гипотеза" in index


def test_generated_text_never_contains_the_verified_status(extracts):
    _, items = all_items(extracts)
    parts = portions.split(items)
    texts = [portions.render_markdown(p, TODAY, "x") + yaml.safe_dump(portions.render_sheet(p, TODAY, {}), allow_unicode=True)
             for p in parts]
    assert not any("human-verified" in t for t in texts)


def test_only_promote_module_knows_the_verified_status():
    offenders = [p.name for p in PACKAGE.glob("*.py") if p.name != "promote.py" and "human-verified" in p.read_text(encoding="utf-8")]
    assert offenders == []


def test_every_item_has_a_shown_digest(extracts):
    _, items = all_items(extracts)
    assert all(len(i.shown_digest) == 64 for i in items)


def test_the_edition_is_looked_for_in_the_foreword(extracts, tmp_path, monkeypatch):
    from extractcmp import cli, viewer

    a, b, results, _ = prepared(extracts)
    points = checkpoints.build(EX1, a["t55"], b["t55"])
    edition = next(i for i in cli._items(extracts[0], extracts[1], results, points, EX1) if i.kind == "edition")
    assert edition.page == "2" and "Предисловие" in edition.region
    assert [(c.page, c.box[1], c.box[3]) for c in viewer.crops(edition.region, [2])] == [(2, 60, 220)]
    monkeypatch.setattr(cli, "DOCUMENT", tmp_path / "missing.yaml")
    default = next(i for i in cli._items(extracts[0], extracts[1], results, points, EX1) if i.kind == "edition")
    assert (default.page, default.region) == ("—", portions.EDITION_REGION)
    assert default.shown_digest == edition.shown_digest
