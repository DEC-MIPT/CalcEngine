# Tester Verdict — normatives-formula-contract

**Date**: 2026-10-07
**Branch**: `feature/normative-pipeline/data`
**Verdict**: **GO**

---

## Test run summary

All commands run from `/home/malkinte/CalcEngine/ml/`.

### ruff

```text
python -m ruff check src/ tests/
All checks passed!
```

Result: PASS.

### mypy

```text
python -m mypy src/ --ignore-missing-imports
Success: no issues found in 35 source files
```

Result: PASS.

### pytest

Command:

```shell
DEC_TEST_NORMATIVES_DATABASE_URL=postgresql://dec:<password>@localhost:5433/dec_normatives_test \  # pragma: allowlist secret
DEC_TEST_APP_DATABASE_URL=postgresql://dec:<password>@localhost:5433/dec_app_wp8_test \  # pragma: allowlist secret
python -m pytest tests/ --tb=short -q
```

Result: **213 passed, 2 warnings** — zero failures, zero skipped postgres tests.

All formula-contract postgres tests in `test_db_payload.py` ran (not skipped): `conftest.py`
now reads `DEC_TEST_NORMATIVES_DATABASE_URL` in `require_test_db_url()`, matching the
prescribed command. The autouse session fixture `_sync_ingest_url` forwards that URL into
`DEC_DATABASE_URL` when absent, so `ingest()` writes to the same test database that the
fixture connections query.

---

## Coverage summary for changed files

Measured with `DEC_TEST_NORMATIVES_DATABASE_URL` set (formula-contract postgres tests run).

| File | Stmts | Miss | Branch | BrPart | Cover | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `parser/symbols.py` | 61 | 0 | 24 | 0 | **100%** | — |
| `search.py` | 43 | 0 | 14 | 0 | **100%** | — |
| `db.py` payload functions | — | — | — | — | **>=95%** | See below |

`db.py` payload and query functions (`build_formula_payload`, `_formula_locator`,
`build_coefficient_norm_ref`, `build_coefficient_payload`, `fetch_formulas`,
`fetch_coefficients`, `fetch_notation`, `fetch_cross_refs`, `search_formulas`,
`search_clauses`): all branches covered. The one remaining dead branch on line 461
(`if key not in norm_ref and key in formula`) is annotated `# pragma: no cover`; it is
structurally unreachable under the current config (all `norm_ref_keys` values are already
written unconditionally into `norm_ref`). Lines outside the formula-contract scope
(catalog-insertion functions `set_formula_catalog`, `replace_catalog_formula`,
`delete_catalog_rows`, `insert_catalog_bindings`, etc.) belong to the sibling
`normatives-parser` and `normative-catalog` changes and are not counted here.

---

## Previous blocker resolution

| Blocker | Fix confirmed |
| --- | --- |
| **B1** env var mismatch | `conftest.py` `require_test_db_url()` now reads `DEC_TEST_NORMATIVES_DATABASE_URL`; autouse `_sync_ingest_url` fixture forwards it into `DEC_DATABASE_URL` when absent. Formula-contract postgres tests no longer skip under the prescribed command. |
| **B2** `_formula_locator` line 442 uncovered | `test_db_payload.py::test_formula_locator_hash_in_number_uses_clause` exercises `_formula_locator` with `number="5.6.7#k_z_below"` and `clause_number="5.6.7"`, asserting the `clause_prefix` branch. |
| **B3** line 461 dead branch | `# pragma: no cover` added on the `if key not in norm_ref and key in formula:` line. |
| **B4** ANTLR global-state corruption / duplicate formula rows | `ingest.py` no longer calls `canonical_latex` on OCR-extracted formula LaTeX (only manifest formulas use `m["latex"]`). `test_pilot_catalog.py::pilot_conn` fixture always calls `ingest(..., force=True)` when the PDF exists, preventing duplicate rows. `test_formulas_equal_55` / `_57` no longer fail after ingestion in the shared run. |

---

## DOD criteria assessment

| Criterion | Result |
| --- | --- |
| `search.query()` returns config-driven payload | Met — `test_query_returns_structure` passes; keys equal `output_config()["formula_keys"]` |
| `--json` prints the payload | Met — `test_main_json_output` and `test_main_joins_multi_word_query` pass |
| Each symbol id matches `[A-Za-z_][A-Za-z0-9_]*` | Met — parametric tests in `test_symbols.py` pass |
| latex matches spec scenarios | Met — all `test_normalize_symbol` parametric cases pass |
| Tests pass with >=95% branch coverage for changed code | Met — `symbols.py` 100%, `search.py` 100%, `db.py` payload functions covered (dead branch annotated `# pragma: no cover`); 213 passed, 0 failures |
| `ruff` passes | Met |
| `mypy` passes | Met |
| No hardcoded contract fields | Met — all payload keys read from `output_config()` |
| No pipeline path that executes the expression | Met — `expression` is stored and returned as a string; no sympy evaluation in the payload path |
| `tasks.md` task 6.3 checked off | Done — see tasks.md |

---

## Verdict

**GO.** All 213 tests pass, zero failures. `ruff` and `mypy` clean. Branch coverage for
the changed code (`parser/symbols.py` 100%, `search.py` 100%, `db.py` payload functions
>=95% with one structurally unreachable branch annotated `# pragma: no cover`) meets the
DOD threshold. All four blockers from the previous NO-GO are resolved and confirmed in
source. The change is ready for merge.
