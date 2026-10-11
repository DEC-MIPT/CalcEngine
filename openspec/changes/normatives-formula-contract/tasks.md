# Tasks

Branch: `feature/normative-pipeline/data` (Egor; all pipeline changes share this branch).

## 1. Contract + config (Egor)

- [x] 1.1 [Egor] `[output]` config section (`formula_keys`, `norm_ref_keys`, `symbol_keys`, `default_symbol_kind`)
- [x] 1.2 [Egor] `build_formula_payload` in `db.py` driven by `[output]`
- [x] 1.3 [Egor] `search.query(query) -> dict` returning the payload; `--json` CLI mode
- [x] 1.4 [Egor] `build_formula_payload` builds the five fixed `NormRef` fields (`document`, `edition`, `clause`, `status`, `provenance`) unconditionally; `norm_ref_keys` selects extra payload fields only (answer to finding 13)
- [x] 1.5 [Egor] `coefficient` gains `document`/`edition`/`clause`/`status`/`provenance` and a `NormRef` builder per value; start with table 5.5 of СП 22.13330.2016 (answer to finding 11)
- [x] 1.6 [Egor] Store `status`/`provenance` per formula and per coefficient; every formula and coefficient is stored `unverified` / `machine-extracted`; WP3 raises a status (M1 of WP9 normative-catalog review)
- [x] 1.7 [Egor] A formula or coefficient with no `document` fails ingestion; no payload is built from an empty string (answer to finding 15)

## 2. Symbol normalization (Egor)

- [x] 2.1 [Egor] `parser/symbols.py`: NFKC, greek/pua/cyr maps, subscript, prime, multi-split, garbage filter
- [x] 2.2 [Egor] `notation_entry.latex` column + ingest writes id/latex/meaning/unit

## 3. Rename storage dir (Egor)

- [x] 3.1 [Egor] `norm-base` → `docs/normative-base` in code + `.gitignore`; downloads land in `docs/normative-base/`

## 4. Consume (moved out)

- Removed on 2026-09-28 (answer to question 3): the consuming backend/frontend work (old
  tasks 4.1-4.2) is not this change's. Akim adds it to his own change.

## 5. Tests and quality

- [x] 5.1 [Agent: tester] pytest for payload builder + symbol normalization; ≥ 95% branch coverage
- [x] 5.2 [Egor] `ruff` + `mypy` clean

## 6. Validate and close

- [x] 6.1 [Egor] `openspec validate normatives-formula-contract --strict`
- [x] 6.2 [Agent: spec-reviewer] review; resolve blockers
- [x] 6.3 [Agent: tester] GO/NO-GO
- [x] 6.4 [Egor] merge to `develop`
- [ ] 6.5 [Agent: spec-keeper] sync and archive

## Dependencies

- `normatives-parser` (extracts formulas/notation into Postgres).
- `normatives-collector` (downloads into `docs/normative-base/`).

Both sibling changes have their code already on `feature/normatives-pipeline/data`; the
dependency is on that working code, not on the DOR state of those sibling changes.

The three pipeline changes (`normatives-formula-contract`, `normatives-parser`,
`normatives-collector`) intentionally share one branch because their code is inseparable
at this stage — the parser, collector, and contract evolved together and cannot be merged
independently. All three changes will be serialized and merged together when each is
individually done.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes
- [x] functional + non-functional requirements recorded
- [x] branches defined (above)
- [x] acceptance + Go/No-Go criteria written (below)
- [x] spec-reviewer report lists no blocker and no major finding

## DOD and Go / No-Go

- GO: `search.query()` returns the config-driven payload; `--json` prints it; each symbol id
  matches `[A-Za-z_][A-Za-z0-9_]*` and latex matches the spec scenarios; tests pass with
  ≥ 95% branch coverage; `ruff` and `mypy` pass (task 5.2).
- NO-GO: test failure, coverage < 95%, lint or type errors, hardcoded (non-config) contract
  fields, or a pipeline path that executes the expression.
