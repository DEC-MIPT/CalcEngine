import copy
import subprocess
from datetime import date

import pytest
import yaml

from extractcmp import cli, promote

VERIFIERS = ["Vera"]
AT = date(2026, 10, 25)


def draft():
    return {
        "formulas": [{"parameter": "R", "latex": "R=1", "page": 36, "verification": {"status": "pending"}}],
        "table_values": [
            {"parameter": "m", "value": 1.5, "page": 38, "verification": {"status": "pending"}},
            {"parameter": "n", "value": 2.5, "page": 38, "verification": {"status": "pending"}},
        ],
        "thresholds": [], "checks": [], "method_bounds": [],
    }


def mapping(d):
    def where(lst, i, items):
        return {"list": lst, "index": i, "record_digest": promote.record_digest(d[lst][i]), "items": items}

    return {
        "rec_r": where("formulas", 0, {"rec_r": "d1"}),
        "rec_m": where("table_values", 0, {"m@1": "d2", "m@2": "d3"}),
        "rec_n": where("table_values", 1, {"n": "d4"}),
    }


def item(portion, local, record, digest, verdict="верно", **over):
    base = {"item": f"{portion}/{local}", "record": record, "kind": "record", "page": "36", "shown_digest": digest,
            "verdict": verdict, "corrected": None, "by": "Vera", "at": "2026-10-25", "comment": None}
    base.update(over)
    return base


def sheet(items, portion="P1-1", by="Vera"):
    return promote.sign_sheet({"portion": portion, "items": items}, by, AT)


def test_canonical_json_and_digests():
    assert promote.canonical_json({"b": 1, "a": [True, None, "я", 2.5]}) == '{"a":[true,null,"я",2.5],"b":1.0}'
    with pytest.raises(ValueError, match="non-finite"):
        promote.canonical_json(float("inf"))
    with pytest.raises(ValueError, match="cannot be hashed"):
        promote.canonical_json({1, 2})
    record = {"x": 1, "verification": {"status": "pending"}}
    assert promote.record_digest(record) == promote.record_digest({"x": 1.0, "verification": {"status": "x"}})
    assert len(promote.record_digest(record)) == 64
    assert promote.record_digest({"x": 2}) != promote.record_digest(record)


def test_sign_and_check_sheet():
    good = sheet([item("P1-1", "rec_r", "rec_r", "d1")])
    assert promote.check_sheet(good, VERIFIERS) == []
    unsigned = {"portion": "P1-1", "items": []}
    assert promote.check_sheet(unsigned, VERIFIERS) == ["the sheet is not signed"]
    stranger = sheet([item("P1-1", "rec_r", "rec_r", "d1", by="Eve")], by="Eve")
    assert "is not in verifiers" in promote.check_sheet(stranger, VERIFIERS)[0]
    tampered = copy.deepcopy(good)
    tampered["items"][0]["verdict"] = "отклонить"
    assert "changed after it was signed" in " ".join(promote.check_sheet(tampered, VERIFIERS))
    assert "not by the signer" in " ".join(
        promote.check_sheet(sheet([item("P1-1", "r", "r", "d", by="Other")]), ["Vera", "Other"])
    )
    bad = sheet([item("P1-1", "r", "r", "d", verdict="ок", at=None)])
    text = " ".join(promote.check_sheet(bad, VERIFIERS))
    assert "not allowed" in text and "no date" in text
    needs = sheet([item("P1-1", "a", "a", "d", verdict="отклонить"), item("P1-1", "b", "b", "d", verdict="исправить")])
    text = " ".join(promote.check_sheet(needs, VERIFIERS))
    assert "a rejection needs a comment" in text and "needs the corrected fields" in text
    pending = sheet([item("P1-1", "a", "a", "d", verdict=None, by=None, at=None)])
    assert promote.check_sheet(pending, VERIFIERS) == []
    bad_date = copy.deepcopy(good)
    bad_date["signature"]["at"] = "no"
    assert any("signature date" in e for e in promote.check_sheet(bad_date, VERIFIERS))


def test_approval_sets_status_and_digest():
    d = draft()
    sheets = [
        sheet([item("P1-1", "rec_r", "rec_r", "d1")]),
        sheet([item("P2-1", "m@1", "rec_m", "d2", comment="ok"), item("P2-1", "m@2", "rec_m", "d3")], portion="P2-1"),
    ]
    result, lines = promote.promote(d, mapping(d), sheets, VERIFIERS)
    verification = result["formulas"][0]["verification"]
    assert verification == {
        "status": "human-verified", "by": "Vera", "at": "2026-10-25", "portion": "P1-1",
        "value_digest": promote.record_digest(result["formulas"][0]),
    }
    assert result["table_values"][0]["verification"]["comment"] == "ok"
    assert result["table_values"][1]["verification"] == {"status": "pending"}
    assert d["formulas"][0]["verification"] == {"status": "pending"}
    assert "rec_n: skipped" in " ".join(lines)


def test_unsigned_or_foreign_sheet_changes_nothing():
    d = draft()
    unsigned = {"portion": "P1-1", "items": [item("P1-1", "rec_r", "rec_r", "d1")], "signature": None}
    with pytest.raises(ValueError, match="not signed"):
        promote.promote(d, mapping(d), [unsigned], VERIFIERS)
    with pytest.raises(ValueError, match="not in verifiers"):
        promote.promote(d, mapping(d), [sheet([item("P1-1", "rec_r", "rec_r", "d1", by="Eve")], by="Eve")], VERIFIERS)
    with pytest.raises(ValueError):
        promote.promote(d, mapping(d), [sheet([item("P1-1", "rec_r", "rec_r", "d1")])], [])


def test_stale_or_partial_sheets_are_skipped():
    d = draft()
    changed = copy.deepcopy(d)
    m = mapping(d)
    changed["formulas"][0]["latex"] = "R=2"
    _, lines = promote.promote(changed, m, [sheet([item("P1-1", "rec_r", "rec_r", "d1")])], VERIFIERS)
    assert "changed after it was mapped" in lines[0]
    _, lines = promote.promote(d, m, [sheet([item("P1-1", "rec_r", "rec_r", "WRONG")])], VERIFIERS)
    assert "do not cover exactly what was shown" in lines[0]
    one = sheet([item("P2-1", "m@1", "rec_m", "d2")], portion="P2-1")
    result, lines = promote.promote(d, m, [one], VERIFIERS)
    assert "rec_m: skipped" in " ".join(lines)
    assert result["table_values"][0]["verification"] == {"status": "pending"}


def test_missing_verdict_leaves_record_pending():
    d = draft()
    s = sheet([item("P2-1", "m@1", "rec_m", "d2"), item("P2-1", "m@2", "rec_m", "d3", verdict=None, by=None, at=None)],
              portion="P2-1")
    result, lines = promote.promote(d, mapping(d), [s], VERIFIERS)
    assert "left pending" in " ".join(lines)
    assert result["table_values"][0]["verification"] == {"status": "pending"}


def test_items_in_two_portions_are_not_approved():
    d = draft()
    s1 = sheet([item("P2-1", "m@1", "rec_m", "d2")], portion="P2-1")
    s2 = sheet([item("P2-2", "m@2", "rec_m", "d3")], portion="P2-2")
    result, lines = promote.promote(d, mapping(d), [s1, s2], VERIFIERS)
    assert "several portions" in " ".join(lines)
    assert result["table_values"][0]["verification"] == {"status": "pending"}


def test_rejection_and_correction():
    d = draft()
    s = sheet([
        item("P2-1", "m@1", "rec_m", "d2", verdict="отклонить", comment="wrong column"),
        item("P2-1", "m@2", "rec_m", "d3"),
        item("P2-1", "n", "rec_n", "d4", verdict="исправить", corrected={"value": 2.6}),
    ], portion="P2-1")
    result, lines = promote.promote(d, mapping(d), [s], VERIFIERS)
    assert result["table_values"][0]["verification"] == {
        "status": "rejected", "by": "Vera", "at": "2026-10-25", "comment": "wrong column"}
    assert result["table_values"][1]["value"] == 2.6
    assert result["table_values"][1]["verification"] == {"status": "pending"}
    assert "corrected, pending a new check" in " ".join(lines)


def git(cwd, *args, **env):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, env={**__import__("os").environ, **env})


def commit_as(repo, name):
    git(repo, "add", "-A")
    git(repo, "-c", f"user.name={name}", "-c", "user.email=x@example.com", "commit", "-qm", "sheet")


def test_check_committed(tmp_path):
    path = tmp_path / "s.yaml"
    path.write_text("x: 1\n", encoding="utf-8")
    git(tmp_path, "init", "-q")
    assert "uncommitted" in promote.check_committed(path, "Vera")[0]
    commit_as(tmp_path, "Vera")
    assert promote.check_committed(path, "Vera") == []
    assert "not by 'Eve'" in promote.check_committed(path, "Eve")[0]
    path.write_text("x: 2\n", encoding="utf-8")
    assert "uncommitted" in promote.check_committed(path, "Vera")[0]


def test_check_committed_outside_a_repo(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))
    path = tmp_path / "s.yaml"
    path.write_text("x: 1\n", encoding="utf-8")
    assert promote.check_committed(path, "Vera") == ["the sheet is not in a git working tree"]


def test_cli_build_sign_promote(tmp_path, extracts):
    a, b = extracts
    (tmp_path / "extract-a.yaml").write_text(yaml.safe_dump(a, allow_unicode=True), encoding="utf-8")
    (tmp_path / "extract-b.yaml").write_text(yaml.safe_dump(b, allow_unicode=True), encoding="utf-8")
    (tmp_path / "extract-a.report.md").write_text("Изм. N 5 здесь\n", encoding="utf-8")
    out = tmp_path / "out"
    code = cli.main(["build", "--a", str(tmp_path / "extract-a.yaml"), "--b", str(tmp_path / "extract-b.yaml"),
                     "--out-dir", str(out), "--date", "2026-10-22"])
    assert code == 0
    for name in ("diff-report.md", "amendment-marks.md", "control-points.md", "portions/index.md", "portions/P1-1.yaml"):
        assert (out / name).exists()
    sheet_path = out / "portions" / "P1-1.yaml"
    filled = yaml.safe_load(sheet_path.read_text(encoding="utf-8"))
    first = filled["items"][0]
    first.update(verdict="верно", by="Vera", at="2026-10-25")
    sheet_path.write_text(yaml.safe_dump(filled, allow_unicode=True), encoding="utf-8")
    git(out, "init", "-q")
    commit_as(out, "Vera")
    assert cli.main(["sign", str(sheet_path), "--by", "Vera", "--at", "2026-10-25"]) == 0
    signed = yaml.safe_load(sheet_path.read_text(encoding="utf-8"))
    assert signed["signature"]["by"] == "Vera"
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"verifiers": ["Vera"]}), encoding="utf-8")
    d = draft()
    local = first["item"].split("/", 1)[1]
    m = {first["record"]: {"list": "formulas", "index": 0, "record_digest": promote.record_digest(d["formulas"][0]),
                           "items": {local: first["shown_digest"]}}}
    (tmp_path / "draft.yaml").write_text(yaml.safe_dump(d), encoding="utf-8")
    (tmp_path / "map.yaml").write_text(yaml.safe_dump(m, allow_unicode=True), encoding="utf-8")
    args = ["promote", "--draft", str(tmp_path / "draft.yaml"), "--mapping", str(tmp_path / "map.yaml"),
            "--manifest", str(manifest), "--out", str(tmp_path / "result.yaml"), str(sheet_path)]
    assert cli.main(args) == 1
    assert not (tmp_path / "result.yaml").exists()
    commit_as(out, "Vera")
    manifest.write_text(yaml.safe_dump({"verifiers": ["Someone"]}), encoding="utf-8")
    assert cli.main(args) == 1
    assert not (tmp_path / "result.yaml").exists()
    manifest.write_text(yaml.safe_dump({"verifiers": ["Vera"]}), encoding="utf-8")
    assert cli.main(args) == 0
    result = yaml.safe_load((tmp_path / "result.yaml").read_text(encoding="utf-8"))
    assert result["formulas"][0]["verification"]["status"] == "human-verified"
