"""Тесты `formulas/source.py`: выбор источника LaTeX по типу PDF."""

from __future__ import annotations

from pathlib import Path

from normatives_pipeline.formulas import source
from normatives_pipeline.parser import text_layer
from normatives_pipeline.parser.models import Formula


def _formula(**kwargs) -> Formula:
    defaults = {"number": "5.1", "raw_text": "", "page": 1, "line": 1, "latex": ""}
    return Formula(**{**defaults, **kwargs})


def test_classify_pdf_text() -> None:
    assert source.classify_pdf(["x" * text_layer.MIN_TEXT_CHARS]) == "text"


def test_classify_pdf_scan() -> None:
    assert source.classify_pdf(["мало текста"]) == "scan"


def test_fill_latex_scan_returns_formulas_unchanged(monkeypatch) -> None:
    monkeypatch.setattr(source, "classify_pdf", lambda _: "scan")
    f = _formula(latex="orig")
    result = source.fill_latex(Path("x.pdf"), [f], [])
    assert result == [f]


def test_fill_latex_scan_empty_list(monkeypatch) -> None:
    monkeypatch.setattr(source, "classify_pdf", lambda _: "scan")
    assert source.fill_latex(Path("x.pdf"), [], []) == []


def test_fill_latex_text_fills_from_reconstruct(monkeypatch) -> None:
    monkeypatch.setattr(source, "classify_pdf", lambda _: "text")
    monkeypatch.setattr(
        source.latex_reconstruct,
        "reconstruct_document",
        lambda _path: {1: {"5.1": r"x + y"}},
    )
    f = _formula(number="5.1", page=1, latex="")
    result = source.fill_latex(Path("x.pdf"), [f], [])
    assert result[0].latex == r"x + y"


def test_fill_latex_text_keeps_formula_without_match(monkeypatch) -> None:
    monkeypatch.setattr(source, "classify_pdf", lambda _: "text")
    monkeypatch.setattr(
        source.latex_reconstruct,
        "reconstruct_document",
        lambda _path: {},
    )
    f = _formula(latex="orig")
    result = source.fill_latex(Path("x.pdf"), [f], [])
    assert result[0].latex == "orig"


def test_fill_latex_text_partial_match(monkeypatch) -> None:
    monkeypatch.setattr(source, "classify_pdf", lambda _: "text")
    monkeypatch.setattr(
        source.latex_reconstruct,
        "reconstruct_document",
        lambda _path: {1: {"5.1": r"A = B"}},
    )
    f1 = _formula(number="5.1", page=1)
    f2 = _formula(number="5.2", page=1, latex="keep")
    result = source.fill_latex(Path("x.pdf"), [f1, f2], [])
    assert result[0].latex == r"A = B"
    assert result[1].latex == "keep"
