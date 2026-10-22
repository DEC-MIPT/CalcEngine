"""Тесты пилотного каталога `foundations_shallow_r` (WP9 2.1-2.5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import require_test_db_url

from normatives_pipeline import catalog_contract, db, pilot_catalog
from normatives_pipeline.ingest import ingest

CT = pilot_catalog.CALCULATION_TYPE
PILOT_PARAMETERS = {
    "gamma_c1", "gamma_c2", "k", "m_gamma", "m_q", "m_c",
    "k_z_threshold", "k_z_below", "k_z_from", "r", "check_norm_refs",
}
PILOT_INPUTS = {
    "b", "d_1", "d_b", "gamma_II", "gamma_II_prime", "c_II", "phi_II", "p",
}
REPO = Path(__file__).resolve().parents[2]
PILOT_PDF = REPO / "docs" / "normative-base" / "СП 22.13330.2016.pdf"

_TWO_HALF_CELLS = [
    {"row_index": 0, "col_index": 0, "value": "Заголовок"},
    {"row_index": 0, "col_index": 4, "value": "Заголовок"},
    {"row_index": 1, "col_index": 1, "value": "A"},
    {"row_index": 1, "col_index": 2, "value": "B"},
    {"row_index": 1, "col_index": 3, "value": "C"},
    {"row_index": 2, "col_index": 0, "value": "1"},
    {"row_index": 2, "col_index": 1, "value": "0,25"},
    {"row_index": 2, "col_index": 2, "value": "0,5"},
    {"row_index": 2, "col_index": 3, "value": "1,0"},
    {"row_index": 2, "col_index": 4, "value": "5"},
    {"row_index": 2, "col_index": 5, "value": "2,0"},
    {"row_index": 2, "col_index": 6, "value": "2,5"},
    {"row_index": 2, "col_index": 7, "value": "3,0"},
]


@pytest.fixture(scope="module")
def pilot_conn():
    require_test_db_url()
    conn = db.connect()
    db.init_schema(conn)
    catalog_contract.ensure_catalog_read(conn)
    if not PILOT_PDF.exists() and db.fetch_document_id(conn, pilot_catalog.DESIGNATION) is None:
        conn.close()
        pytest.skip("СП 22.13330.2016 не ингестирован и файла нет")
    if PILOT_PDF.exists():
        ingest(PILOT_PDF, force=True)
    pilot_catalog.sync_pilot_catalog(conn)
    yield conn
    conn.close()


def _rows(conn, sql: str, params: tuple = ()) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]


def _load(value):
    return json.loads(value) if isinstance(value, str) else value


def test_unit_symbol_maps_and_rejects_unknown() -> None:
    assert pilot_catalog.unit_symbol("кПа") == "kPa"
    assert pilot_catalog.unit_symbol("") == "1"
    with pytest.raises(pilot_catalog.PilotCatalogError):
        pilot_catalog.unit_symbol("фунт")


def test_parse_heading_rows_reads_two_halves() -> None:
    assert pilot_catalog.parse_heading_rows(_TWO_HALF_CELLS) == [
        (1.0, [0.25, 0.5, 1.0]),
        (5.0, [2.0, 2.5, 3.0]),
    ]


def test_m_table_rows_map_columns_and_heading() -> None:
    rows = pilot_catalog.m_table_rows(_TWO_HALF_CELLS)
    assert [(r[1], r[3], r[5], r[8], r[9]) for r in rows] == [
        ("m_gamma", "M_gamma", 0.25, 1.0, "deg"),
        ("m_q", "M_q", 0.5, 1.0, "deg"),
        ("m_c", "M_c", 1.0, 1.0, "deg"),
        ("m_gamma", "M_gamma", 2.0, 5.0, "deg"),
        ("m_q", "M_q", 2.5, 5.0, "deg"),
        ("m_c", "M_c", 3.0, 5.0, "deg"),
    ]
    assert all(r[7] == "phi_II" for r in rows)


def test_binding_rows_one_per_parameter_and_formula_without_tree_is_dropped() -> None:
    full = pilot_catalog.binding_rows(
        {"5.6.7#k_z_below", "5.6.7#k_z_from", "5.7"}
    )
    assert sorted(r[1] for r in full) == sorted(PILOT_PARAMETERS)
    dropped = pilot_catalog.binding_rows({"5.6.7#k_z_below", "5.6.7#k_z_from"})
    assert len(dropped) == len(PILOT_PARAMETERS) - 1
    assert all(row[1] != "r" for row in dropped)


def test_notation_result_symbol_prefers_output() -> None:
    notation = [
        {"symbol": "x", "kind": "input"},
        {"symbol": "R", "kind": "output"},
    ]
    assert pilot_catalog.notation_result_symbol(notation) == "R"


def test_notation_result_symbol_falls_back_and_is_empty_safe() -> None:
    assert pilot_catalog.notation_result_symbol([{"symbol": "x", "kind": "input"}]) == "x"
    assert pilot_catalog.notation_result_symbol([]) is None


def test_parse_heading_rows_skips_non_numeric_tail() -> None:
    cells = [
        {"row_index": 0, "col_index": 0, "value": "5"},
        {"row_index": 0, "col_index": 1, "value": "текст"},
        {"row_index": 0, "col_index": 2, "value": "2"},
        {"row_index": 0, "col_index": 3, "value": "3"},
    ]
    assert pilot_catalog.parse_heading_rows(cells) == []


def test_bind_registry_formula_without_row_returns_false(monkeypatch) -> None:
    monkeypatch.setattr(pilot_catalog.db, "fetch_formula_by_number", lambda *a, **k: None)
    assert pilot_catalog._bind_registry_formula(object(), 1, "9.9") is False


def test_bind_registry_formula_with_unconvertible_expression_returns_false(monkeypatch) -> None:
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_formula_by_number",
        lambda *a, **k: {"id": 1, "expression": "x!"},
    )
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_notation",
        lambda *a, **k: [{"symbol": "x", "unit": "", "kind": "input"}],
    )
    assert pilot_catalog._bind_registry_formula(object(), 1, "9.9") is False


def test_bind_registry_formula_with_unknown_unit_returns_false(monkeypatch) -> None:
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_formula_by_number",
        lambda *a, **k: {"id": 1, "expression": "x"},
    )
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_notation",
        lambda *a, **k: [{"symbol": "x", "unit": "фунт", "kind": "output"}],
    )
    assert pilot_catalog._bind_registry_formula(object(), 1, "9.9") is False


def test_bind_registry_formula_with_empty_notation_returns_false(monkeypatch) -> None:
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_formula_by_number",
        lambda *a, **k: {"id": 1, "expression": "x"},
    )
    monkeypatch.setattr(pilot_catalog.db, "fetch_notation", lambda *a, **k: [])
    assert pilot_catalog._bind_registry_formula(object(), 1, "9.9") is False


def test_sync_uses_pilot_designation_by_default(monkeypatch) -> None:
    called_with: dict = {}
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_document_id",
        lambda conn, desig: called_with.update(designation=desig) or None,
    )
    pilot_catalog.sync_pilot_catalog(object())
    assert called_with["designation"] == pilot_catalog.DESIGNATION


def test_sync_skips_r_binding_when_formula_unconvertible(monkeypatch) -> None:
    from types import SimpleNamespace

    fake_conn = SimpleNamespace(commit=lambda: None, rollback=lambda: None)
    monkeypatch.setattr(pilot_catalog.db, "fetch_document_id", lambda *a, **k: 1)
    monkeypatch.setattr(pilot_catalog.db, "delete_catalog_rows", lambda *a, **k: None)
    monkeypatch.setattr(pilot_catalog.db, "fetch_coefficients", lambda *a, **k: [])
    monkeypatch.setattr(
        pilot_catalog, "_write_synthetic_formulas",
        lambda conn, doc, manifest, commit=True: set(),
    )
    monkeypatch.setattr(
        pilot_catalog, "_bind_registry_formula",
        lambda conn, doc, number, commit=True: False,
    )
    for name in (
        "insert_table_values", "insert_threshold_values", "insert_check_refs",
        "insert_method_bounds",
    ):
        monkeypatch.setattr(pilot_catalog.db, name, lambda *a, **k: None)
    captured: dict = {}
    monkeypatch.setattr(
        pilot_catalog.db, "insert_catalog_bindings",
        lambda conn, doc, rows, commit=True: captured.update(rows=rows),
    )
    assert pilot_catalog.sync_pilot_catalog(fake_conn) is True
    assert all(row[1] != "r" for row in captured["rows"])


def test_sync_without_document_is_noop(monkeypatch) -> None:
    monkeypatch.setattr(pilot_catalog.db, "fetch_document_id", lambda *_a, **_k: None)
    assert pilot_catalog.sync_pilot_catalog(object()) is False


def test_sync_pilot_catalog_rolls_back_on_error(monkeypatch) -> None:
    from types import SimpleNamespace

    calls: list[str] = []
    fake_conn = SimpleNamespace(
        commit=lambda: calls.append("commit"),
        rollback=lambda: calls.append("rollback"),
    )
    monkeypatch.setattr(pilot_catalog.db, "fetch_document_id", lambda *_a, **_k: 1)
    monkeypatch.setattr(pilot_catalog.db, "delete_catalog_rows", lambda *_a, **_k: None)
    monkeypatch.setattr(
        pilot_catalog, "_write_synthetic_formulas", lambda *_a, **_k: set()
    )
    monkeypatch.setattr(
        pilot_catalog, "_bind_registry_formula", lambda *_a, **_k: False
    )

    def _boom(*_a: object, **_k: object) -> None:
        raise RuntimeError("simulated db error")

    monkeypatch.setattr(pilot_catalog.db, "insert_catalog_bindings", _boom)

    with pytest.raises(RuntimeError, match="simulated db error"):
        pilot_catalog.sync_pilot_catalog(fake_conn)

    assert "rollback" in calls, "conn.rollback() must be called on failure"
    assert "commit" not in calls, "conn.commit() must not be called on failure"


def test_binding_one_row_per_parameter_and_no_value_column(pilot_conn) -> None:
    rows = _rows(
        pilot_conn,
        "SELECT parameter FROM catalog_binding WHERE calculation_type = %s",
        (CT,),
    )
    assert sorted(row["parameter"] for row in rows) == sorted(PILOT_PARAMETERS)
    columns = _rows(
        pilot_conn,
        "SELECT column_name FROM information_schema.columns"
        " WHERE table_name = 'catalog_binding'",
    )
    assert "value" not in {column["column_name"] for column in columns}


def test_bound_formula_trees_and_units_cover_every_symbol(pilot_conn) -> None:
    from normatives_pipeline.formulas import expression_tree

    rows = _rows(
        pilot_conn,
        "SELECT parameter, result_symbol, tree, units FROM catalog_read.type_formulas"
        " WHERE calculation_type = %s",
        (CT,),
    )
    assert {row["parameter"] for row in rows} == {"k_z_below", "k_z_from", "r"}
    for row in rows:
        tree = _load(row["tree"])
        expression_tree.validate_tree(tree)
        units = _load(row["units"])
        symbols = set(expression_tree.tree_symbols(tree)) | {row["result_symbol"]}
        assert symbols <= set(units)


def test_status_and_provenance_on_every_view_row(pilot_conn) -> None:
    views = (
        "type_formulas", "type_table_values", "type_thresholds",
        "type_checks", "type_method_bounds",
    )
    for view in views:
        rows = _rows(
            pilot_conn,
            f"SELECT norm_refs FROM catalog_read.{view} WHERE calculation_type = %s",
            (CT,),
        )
        assert rows, view
        for row in rows:
            refs = _load(row["norm_refs"])
            assert refs
            for ref in refs:
                assert ref["status"] == "unverified", view
                assert ref["provenance"] == "machine-extracted", view


def test_table_headings_unique_and_bounds_name_inputs(pilot_conn) -> None:
    rows = _rows(
        pilot_conn,
        "SELECT parameter, heading_symbol, heading_value, heading_unit"
        " FROM catalog_read.type_table_values"
        " WHERE calculation_type = %s AND heading_symbol IS NOT NULL",
        (CT,),
    )
    assert {row["parameter"] for row in rows} == {"m_gamma", "m_q", "m_c"}
    headings_by_param: dict[str, list[float]] = {}
    for parameter in ("m_gamma", "m_q", "m_c"):
        headings = [float(row["heading_value"]) for row in rows if row["parameter"] == parameter]
        assert headings
        assert len(headings) == len(set(headings))
        assert all(
            row["heading_symbol"] == "phi_II" and row["heading_unit"] == "deg"
            for row in rows
            if row["parameter"] == parameter
        )
        headings_by_param[parameter] = headings
    bounds = _rows(
        pilot_conn,
        "SELECT quantity, kind, value FROM catalog_read.type_method_bounds"
        " WHERE calculation_type = %s ORDER BY kind",
        (CT,),
    )
    assert bounds and {row["quantity"] for row in bounds} <= PILOT_INPUTS
    by_kind = {row["kind"]: float(row["value"]) for row in bounds}
    all_headings = sorted({h for hs in headings_by_param.values() for h in hs})
    assert by_kind["min"] == all_headings[0]
    assert by_kind["max"] == all_headings[-1]


def test_method_bounds_clause_names_table(pilot_conn) -> None:
    rows = _rows(
        pilot_conn,
        "SELECT norm_refs FROM catalog_read.type_method_bounds WHERE calculation_type = %s",
        (CT,),
    )
    assert rows
    for row in rows:
        refs = _load(row["norm_refs"])
        assert refs[0]["clause"] == f"табл. {pilot_catalog.TABLE_M}"


def test_coefficients_and_thresholds_are_stored(pilot_conn) -> None:
    constants = _rows(
        pilot_conn,
        "SELECT parameter, unit, heading_symbol FROM catalog_read.type_table_values"
        " WHERE calculation_type = %s AND heading_symbol IS NULL",
        (CT,),
    )
    assert {row["parameter"] for row in constants} == {"gamma_c1", "gamma_c2", "k"}
    assert all(row["unit"] == "1" and row["heading_symbol"] is None for row in constants)
    thresholds = _rows(
        pilot_conn,
        "SELECT parameter, unit FROM catalog_read.type_thresholds"
        " WHERE calculation_type = %s",
        (CT,),
    )
    assert [(row["parameter"], row["unit"]) for row in thresholds] == [
        ("k_z_threshold", "m"),
    ]


def test_bind_registry_formula_with_missing_notation_symbol_returns_false(monkeypatch) -> None:
    """M2: символ дерева без notation entry → отказ, set_formula_catalog не вызывается."""
    called: list = []
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_formula_by_number",
        lambda *_: {"id": 1, "expression": "x + y"},
    )
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_notation",
        # только x есть в notation; y — символ дерева без записи
        lambda *_: [{"symbol": "x", "unit": "м", "kind": "output"}],
    )
    monkeypatch.setattr(pilot_catalog.db, "set_formula_catalog", lambda *_, **k: called.append(1))
    assert pilot_catalog._bind_registry_formula(object(), 1, "9.9") is False
    assert not called


def test_bind_registry_formula_with_all_symbols_present_calls_set_formula_catalog(monkeypatch) -> None:
    """M2 зеркало: все символы в notation → bind успешен, set_formula_catalog вызван."""
    called: list = []
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_formula_by_number",
        lambda *_: {"id": 1, "expression": "x"},
    )
    monkeypatch.setattr(
        pilot_catalog.db, "fetch_notation",
        lambda *_: [{"symbol": "x", "unit": "м", "kind": "output"}],
    )
    monkeypatch.setattr(pilot_catalog.db, "set_formula_catalog", lambda *_, **k: called.append(1))
    assert pilot_catalog._bind_registry_formula(object(), 1, "9.9") is True
    assert called


def test_ingesting_second_document_leaves_pilot_catalog_on_sp22(pilot_conn) -> None:
    """B1: инжестирование постороннего документа не перепривязывает каталог пилота."""
    before = _rows(
        pilot_conn,
        "SELECT document_id FROM catalog_binding WHERE calculation_type = %s",
        (CT,),
    )
    assert before, "pilot catalog must be populated"
    pilot_doc_id = before[0]["document_id"]

    fake_designation = "ТЕСТ-ФЕЙК-00.00000.0000"
    db.delete_document(pilot_conn, fake_designation)
    fake_doc_id = db.upsert_document(pilot_conn, fake_designation, title="fake", edition="2000")
    pilot_catalog.sync_pilot_catalog(pilot_conn)

    after = _rows(
        pilot_conn,
        "SELECT document_id FROM catalog_binding WHERE calculation_type = %s",
        (CT,),
    )
    assert all(row["document_id"] == pilot_doc_id for row in after), (
        "pilot catalog must remain bound to СП 22, not to the fake document"
    )
    db.delete_document(pilot_conn, fake_designation)
    _ = fake_doc_id
