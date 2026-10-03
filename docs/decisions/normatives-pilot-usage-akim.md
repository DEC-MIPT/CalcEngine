# For Akim: pilot normative → process → query a formula

- Date: 2026-09-27
- From: Egor (data engineer)
- To: Akim (frontend/backend)

## Prereqs

- Docker Postgres `dec-postgres` on port 5433 — see `normatives-postgres-storage.md`.
- The repo venv `.venv` with the package installed editable: `.venv/bin/pip install -e ".[ml]"`.
- Pilot PDFs live in `docs/normative-base/` (gitignored; full texts are not redistributed).

## 1. Get the pilot file

Pilot documents are already in `docs/normative-base/` (СП 22.13330.2016, СП 24/30/31/45.13330,
СНиП scans). New downloads fall into `docs/normative-base/` too (the collector writes there).

## 2. Process (ingest into Postgres)

```bash
cd /home/malkinte/CalcEngine
.venv/bin/python -m normatives_pipeline.ingest --force "docs/normative-base/СП 22.13330.2016.pdf"
```

Idempotent: re-running without `--force` prints `[skip] … уже в хранилище`.

## 3. Query a formula (human-readable)

```bash
.venv/bin/python -m normatives_pipeline.search "условие успешного погружения опускных колодцев"
```

## 4. Query the actual return (JSON — what the backend receives)

```bash
.venv/bin/python -m normatives_pipeline.search --json "условие успешного погружения опускных колодцев"
```

`--json` prints the exact object returned by `normatives_pipeline.search.query(...)`
(`search.query(query) -> dict`), not the console text.

## Returned contract

The output shape is config-driven: `configs/parser.toml` → `[output]`
(`formula_keys`, `norm_ref_keys`, `symbol_keys`, `default_symbol_kind`).

```json
{
  "norm_ref": {"designation": "СП 45.13330.2017", "clause": "13.8", "formula": "13.8#1"},
  "latex": "",
  "symbols": [
    {"id": "G", "latex": "G", "meaning": "собственный вес колодца …", "unit": "", "kind": "input"},
    {"id": "G_p", "latex": "G_{\\text{п}}", "meaning": "дополнительная пригрузка колодца", "unit": "", "kind": "input"}
  ],
  "expression": "",
  "cross_refs": [{"ref_type": "gost", "ref_value": "ГОСТ …", "url": ""}]
}
```

- `latex` and `symbols[].latex` are canonical LaTeX for MathJax.
- `symbols[].id` is the ASCII machine key == the SymPy symbol name the engine binds.
- `expression` is empty for now (structured extraction step); `kind` is `input` until
  output-variable detection lands.
- `cross_refs` are GOST mentions tied to the clause (URL is a later step).

## Note on the pile example

`"допускаемая нагрузка на сваю в составе фундамента"` is pile foundations = СП 24.13330,
not the shallow-foundation pilot СП 22.13330.2016. To search piles, ingest СП 24 first:

```bash
.venv/bin/python -m normatives_pipeline.ingest --force "docs/normative-base/СП 24.13330.2021.pdf"
.venv/bin/python -m normatives_pipeline.search --json "допускаемая нагрузка на сваю"
```

The mechanism is identical; the ingested corpus decides what a query can find.
