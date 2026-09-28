# Tasks

Branch: `feature/normative-formula-contract/data` (Egor).

## 1. Contract + config (Egor)

- [ ] 1.1 [Egor] `[output]` config section (`formula_keys`, `norm_ref_keys`, `symbol_keys`, `default_symbol_kind`)
- [ ] 1.2 [Egor] `build_formula_payload` in `db.py` driven by `[output]`
- [ ] 1.3 [Egor] `search.query(query) -> dict` returning the payload; `--json` CLI mode
- [ ] 1.4 [Egor] `build_formula_payload` builds the five fixed `NormRef` fields (`document`, `edition`, `clause`, `status`, `provenance`) unconditionally; `norm_ref_keys` selects extra payload fields only (answer to finding 13)
- [ ] 1.5 [Egor] `coefficient` gains `document`/`edition`/`clause`/`status`/`provenance` and a `NormRef` builder per value; start with table 5.5 of СП 22.13330.2016 (answer to finding 11)
- [ ] 1.6 [Egor] Store `status`/`provenance` per formula and per coefficient; `formulas.toml` entries are `human-verified`, OCR output is `machine-extracted`/`unverified` (answer to finding 12)
- [ ] 1.7 [Egor] A formula or coefficient with no `document` fails ingestion; no payload is built from an empty string (answer to finding 15)

## 2. Symbol normalization (Egor)

- [ ] 2.1 [Egor] `parser/symbols.py`: NFKC, greek/pua/cyr maps, subscript, prime, multi-split, garbage filter
- [ ] 2.2 [Egor] `notation_entry.latex` column + ingest writes id/latex/meaning/unit

## 3. Rename storage dir (Egor)

- [ ] 3.1 [Egor] `norm-base` → `norm-docs` in code + `.gitignore`; downloads land in `norm-docs/`

## 4. Consume (moved out)

- Removed on 2026-09-28 (answer to question 3): the consuming backend/frontend work (old
  tasks 4.1-4.2) is not this change's. Akim adds it to his own change.

## 5. Tests and quality

- [ ] 5.1 [Agent: tester] pytest for payload builder + symbol normalization; ≥ 95% branch coverage
- [ ] 5.2 [Egor] `ruff` + `mypy` clean

## 6. Validate and close

- [ ] 6.1 [Egor] `openspec validate normatives-formula-contract --strict`
- [ ] 6.2 [Agent: spec-reviewer] review; resolve blockers
- [ ] 6.3 [Agent: tester] GO/NO-GO
- [ ] 6.4 [Egor] merge to `develop`
- [ ] 6.5 [Agent: spec-keeper] sync and archive

## Dependencies

- `normatives-parser` (extracts formulas/notation into Postgres).
- `normatives-collector` (downloads into `norm-docs/`).

## DOR checklist

- [ ] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [ ] `openspec validate --strict` passes
- [ ] functional + non-functional requirements recorded
- [ ] branches defined (above)
- [ ] acceptance + Go/No-Go criteria written (below)

## DOD and Go / No-Go

- GO: `search.query()` returns the config-driven payload; `--json` prints it; symbols are
  normalized LaTeX; tests pass with ≥ 95% branch coverage.
- NO-GO: test failure, coverage < 95%, hardcoded (non-config) contract fields, or a pipeline
  path that executes the expression.
