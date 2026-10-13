"""Тесты CLI-интерфейса `search.py`: main() и пустой запрос."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from normatives_pipeline import search


def test_query_empty_returns_early_without_db(monkeypatch) -> None:
    monkeypatch.setattr(
        search.db, "connect",
        lambda: pytest.fail("не должно подключаться к БД для пустого запроса"),
    )
    result = search.query("   ")
    assert result["formulas"] == []
    assert result["clauses"] == []
    assert result["lemmas"] == ""


def test_main_no_args_prints_usage_and_returns_1(capsys) -> None:
    assert search.main([]) == 1
    assert "использование" in capsys.readouterr().out


def test_main_json_output(monkeypatch, capsys) -> None:
    fake: dict = {"query": "нагрузка", "lemmas": "нагрузк", "formulas": [], "clauses": []}
    monkeypatch.setattr(search, "query", lambda *_: fake)
    assert search.main(["--json", "нагрузка"]) == 0
    assert json.loads(capsys.readouterr().out) == fake


def test_main_text_output_with_results(monkeypatch, capsys) -> None:
    fake: dict = {
        "query": "нагрузка",
        "lemmas": "нагрузк",
        "formulas": [
            {
                "norm_ref": {
                    "document": "СП 22",
                    "clause": "5.1",
                    "status": "unverified",
                    "provenance": "machine-extracted",
                },
                "symbols": [{"latex": r"\gamma", "meaning": "коэффициент", "kind": "input"}],
                "cross_refs": [{"ref_type": "гост", "ref_value": "ГОСТ 1"}],
            }
        ],
        "clauses": [
            {"rank": 0.85, "designation": "СП 22", "number": "5.1", "title": "Область применения"}
        ],
    }
    monkeypatch.setattr(search, "query", lambda *_: fake)
    assert search.main(["нагрузка"]) == 0
    out = capsys.readouterr().out
    assert "Формулы" in out
    assert "Пункты" in out
    assert "СП 22" in out


def test_main_text_output_empty_results(monkeypatch, capsys) -> None:
    fake: dict = {"query": "xyz", "lemmas": "xyz", "formulas": [], "clauses": []}
    monkeypatch.setattr(search, "query", lambda *_: fake)
    assert search.main(["xyz"]) == 0
    assert "Формулы" in capsys.readouterr().out


def test_main_joins_multi_word_query(monkeypatch) -> None:
    received: dict = {}
    monkeypatch.setattr(
        search, "query",
        lambda q: received.update(q=q) or {"query": q, "lemmas": "", "formulas": [], "clauses": []},
    )
    search.main(["расчёт", "нагрузки"])
    assert received["q"] == "расчёт нагрузки"


def test_query_non_empty_calls_db(monkeypatch) -> None:
    conn = MagicMock()
    payload = {
        "norm_ref": {"document": "СП 22", "clause": "5.1", "status": "unverified", "provenance": "machine-extracted"},
        "symbols": [],
        "cross_refs": [],
    }
    monkeypatch.setattr(search.db, "connect", lambda: conn)
    monkeypatch.setattr(search.db, "search_formulas", lambda *_, **__: [{"id": 1}])
    monkeypatch.setattr(search.db, "search_clauses", lambda *_, **__: [])
    monkeypatch.setattr(search.db, "build_formula_payload", lambda *_: payload)

    result = search.query("нагрузка")

    assert result["query"] == "нагрузка"
    assert result["formulas"] == [payload]
    assert result["clauses"] == []
    conn.close.assert_called_once()
