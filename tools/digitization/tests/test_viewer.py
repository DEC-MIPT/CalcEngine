import shutil
from datetime import date

import pytest
import yaml

from extractcmp import cli, viewer
from extractcmp.checkpoints import ControlPoint
from extractcmp.portions import Item

TODAY = date(2026, 10, 27)
TREE = {"kind": "add", "left": {"kind": "div", "left": {"kind": "number", "value": 8.0},
                                "right": {"kind": "symbol", "name": "b"}},
        "right": {"kind": "number", "value": 0.2}}


def item(item_id, kind="record", page="36", region="≈ y 100-120", flags=("итог: совпало",), notes=()):
    return Item(item_id, item_id, "P1", kind, f"T {item_id}", page, region, list(flags), "a-text <A>", "b-text",
                list(notes))


def draft():
    return {
        "formulas": [{"parameter": "k_z_from", "result_symbol": "k_z", "latex": "k_{z}=8/b+0{,}2", "tree": TREE,
                      "units": {"k_z": "1", "b": "m"}, "page": 36, "verification": {"status": "pending"},
                      "norm_refs": [{"document": "СП", "edition": "E", "clause": "5.6.7", "status": "unverified"}]}],
        "table_values": [
            {"parameter": "m", "symbol": "M", "latex": "M", "value": 0.47, "unit": "1", "heading_symbol": "phi",
             "heading_value": 19.0, "heading_unit": "deg", "page": 38},
            {"parameter": "n", "symbol": "N", "value": 2.89, "unit": "1", "heading_value": None},
        ],
    }


MAPPING = {
    "formulas/k_z_from": {"list": "formulas", "index": 0, "items": {"kz": "d", "z0": "d"}},
    "table_values/m": {"list": "table_values", "index": 0, "items": {"t55@phi=19": "d"}},
    "table_values/n": {"list": "table_values", "index": 1, "items": {"t55@phi=19": "d"}},
}
POINTS = [
    ControlPoint("CP-1", "P1", ("kz",), "k_z при b = 20", {"b": "20"}, {"k_z": "0.6"}, True),
    ControlPoint("CP-2", "P1", ("kz",), "пустая", {"b": None}, {"k_z": None}),
    ControlPoint("CP-3", "P1", ("t55@phi=19",), "таблица", {"phi": "19"}, {"M": "0.47"}),
]


def entry(portion, local, **over):
    return {"item": f"{portion}/{local}", "verdict": None, "by": None, "at": None, "corrected": None,
            "comment": None, **over}


class FakeRender:
    def __init__(self):
        self.calls = []

    def __call__(self, page, top, height):
        self.calls.append((page, top, height))
        return b"PNG"


def test_pages_of():
    assert viewer.pages_of("36") == [36]
    assert viewer.pages_of("37, 38") == [37, 38]
    assert viewer.pages_of("—") == []


def test_crops_band_and_box():
    (c,) = viewer.crops("верх страницы (≈ x 550-1190, y 85-145 из 1240×1755 при 150 dpi)", [36])
    assert c == viewer.Crop(36, 45, 140, (550, 85, 1190, 145))
    (top,) = viewer.crops("≈ y 10-30", [36])
    assert (top.top, top.box) == (0, (0, 10, viewer.PAGE_WIDTH, 30))
    (bottom,) = viewer.crops("≈ y 1700-1750", [36])
    assert bottom.top + bottom.height == viewer.PAGE_HEIGHT


def test_crops_split_by_page_mentions():
    region = "заголовок — низ стр. 37 (≈ y 1605-1625); строки — стр. 38, ≈ x 60-880, y 65-1600"
    first, second = viewer.crops(region, [37, 38])
    assert (first.page, first.box) == (37, (0, 1605, viewer.PAGE_WIDTH, 1625))
    assert (second.page, second.box) == (38, (60, 65, 880, 1600))
    region = "стр. 35, абзац (≈ y 1600-1680); продолжение — вверху стр. 36"
    one, whole = viewer.crops(region, [35, 36])
    assert (one.page, whole.page, whole.top, whole.height) == (35, 36, 0, viewer.PAGE_HEIGHT)


def test_crops_without_coordinates():
    assert viewer.crops("титульный лист", []) == []
    pages = [c.page for c in viewer.crops("где-то", [35, 36])]
    assert pages == [35, 36]
    assert all(c.height == viewer.PAGE_HEIGHT for c in viewer.crops("см. стр. 36", [35]))


def test_evaluate_and_infix():
    assert viewer.evaluate(TREE, {"b": "20"}) == pytest.approx(0.6)
    assert viewer.evaluate(TREE, {"b": 10}) == pytest.approx(1.0)
    assert viewer.evaluate(TREE, {"b": "1,6"}) == pytest.approx(5.2)
    for bad in ({}, {"b": None}, {"b": True}, {"b": "x"}, {"b": 0}):
        assert viewer.evaluate(TREE, bad) is None
    sub = {"kind": "sub", "left": {"kind": "neg", "operand": {"kind": "symbol", "name": "a"}},
           "right": {"kind": "mul", "left": {"kind": "number", "value": 2}, "right": {"kind": "symbol", "name": "a"}}}
    assert viewer.evaluate(sub, {"a": 3.0}) == -9.0
    assert viewer.evaluate({"kind": "neg", "operand": {"kind": "symbol", "name": "a"}}, {}) is None
    assert viewer.evaluate({"kind": "call", "name": "min", "args": []}, {}) is None
    assert viewer.infix(TREE) == "((8 / b) + 0.2)"
    assert viewer.infix(sub) == "(−a − (2 · a))"
    assert viewer.infix({"kind": "call"}) == "<call>"


def test_page_shows_crops_records_points_and_rows():
    render = FakeRender()
    ctx = viewer.context(draft(), MAPPING, POINTS, render)
    items = {i.item_id: i for i in [
        item("kz", region="≈ x 700-1110, y 375-395", notes=["оговорка"]),
        item("z0", region="≈ x 1000-1110, y 375-395"),
        item("rule", region="—"),
        item("edition", kind="edition", page="—", region="титульный лист"),
        item("CP-1", kind="control-point", page="—", region="—"),
        item("CP-2", kind="control-point", page="—", region="—"),
        item("CP-3", kind="control-point", page="—", region="—"),
        item("t55@phi=19", kind="table-row", page="37, 38", region="низ стр. 37 (≈ y 1605-1625)"),
    ]}
    sheet = {"portion": "P1-1", "items": [
        entry("P1-1", "kz", verdict="исправить", by="Vera", at="2026-10-27", corrected={"value": 1}, comment="c"),
        entry("P1-1", "z0"), entry("P1-1", "rule"), entry("P1-1", "edition"),
        entry("P1-1", "CP-1"), entry("P1-1", "CP-2"), entry("P1-1", "CP-3"),
        entry("P1-1", "t55@phi=19", verdict="верно", by="Vera", at="2026-10-27"),
    ]}
    page = viewer.render_page(ctx, sheet, items, TODAY, {"PDF": "norm.pdf"})
    assert page.startswith("<!doctype html>") and "<title>Порция P1-1</title>" in page
    assert render.calls == [(36, 335, 100), (36, 335, 100), (36, 0, viewer.PAGE_HEIGHT), (37, 1565, 100)]
    assert 'data:image/png;base64,UE5H' in page
    assert "left:56.45%" in page and "стр. 36 целиком" in page
    assert "a-text &lt;A&gt;" in page and "<li>оговорка</li>" in page
    assert page.count("<h4>Запись каталога <code>formulas/k_z_from</code></h4>") == 2
    assert 'data-tex="k_{z}=8/b+0{,}2"' in page and "((8 / b) + 0.2)" in page
    assert "k_z: 1, b: m" in page and "СП, E, 5.6.7 (unverified)" in page and "pending" in page
    assert "Записи в черновике нет" in page
    assert "k_z = 0.6 " in page and page.count("По дереву черновика") == 1
    assert "<b>исправить</b> · Vera · 2026-10-27 · исправление: <code>{&#x27;value&#x27;: 1}</code> · c" in page
    assert "<td>19</td>" in page and "<td>[0.47, 2.89]</td>" in page and "<b>верно</b>" in page
    assert "Вердикта нет" in page


def test_record_without_heading_or_tree():
    ctx = viewer.context(draft(), MAPPING, [], FakeRender())
    sheet = {"portion": "P2-1", "items": [entry("P2-1", "n-only")]}
    mapping = {"table_values/n": {"list": "table_values", "index": 1, "items": {"n-only": "d"}}}
    ctx = viewer.context(draft(), mapping, [], FakeRender())
    page = viewer.render_page(ctx, sheet, {"n-only": item("n-only", region="—", page="—")}, TODAY, {})
    assert "N = 2.89 [1]</td>" in page and "<th>ссылка</th><td>—</td>" in page
    assert "<th>статус</th><td>—</td>" in page and "дерево" not in page


MINIMAL_PDF_OBJECTS = [
    "<< /Type /Catalog /Pages 2 0 R >>",
    "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>",
]


def minimal_pdf(path):
    out, offsets = b"%PDF-1.4\n", []
    for number, body in enumerate(MINIMAL_PDF_OBJECTS, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(offsets) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets)
    out += f"trailer\n<< /Size {len(offsets) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(out)


@pytest.mark.skipif(shutil.which("pdftoppm") is None, reason="pdftoppm is not installed")
def test_pdftoppm_renders_a_band(tmp_path):
    pdf = tmp_path / "one.pdf"
    minimal_pdf(pdf)
    png = viewer.pdftoppm(pdf)(1, 100, 50)
    assert png.startswith(b"\x89PNG")


def test_cli_html(tmp_path, extracts, monkeypatch):
    a, b = extracts
    for name, data in (("extract-a.yaml", a), ("extract-b.yaml", b)):
        (tmp_path / name).write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    sheets = tmp_path / "sheets"
    assert cli.main(["build", "--a", str(tmp_path / "extract-a.yaml"), "--b", str(tmp_path / "extract-b.yaml"),
                     "--out-dir", str(tmp_path), "--sheets-dir", str(sheets), "--date", "2026-10-27"]) == 0
    (tmp_path / "draft.yaml").write_text(yaml.safe_dump({"formulas": []}), encoding="utf-8")
    (tmp_path / "map.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    monkeypatch.setattr(viewer, "pdftoppm", lambda pdf: FakeRender())
    out = tmp_path / "html"
    code = cli.main(["html", "--a", str(tmp_path / "extract-a.yaml"), "--b", str(tmp_path / "extract-b.yaml"),
                     "--draft", str(tmp_path / "draft.yaml"), "--mapping", str(tmp_path / "map.yaml"),
                     "--pdf", str(tmp_path / "x.pdf"), "--out-dir", str(out), "--date", "2026-10-27",
                     str(sheets / "P1-1.yaml")])
    assert code == 0
    page = (out / "P1-1.html").read_text(encoding="utf-8")
    assert "Порция P1-1" in page and "Сформировано 2026-10-27" in page
