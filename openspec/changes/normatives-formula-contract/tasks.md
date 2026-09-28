# Tasks

Branches: `feature/normative-formula-contract/data` (Egor),
`feature/normative-formula-contract/backend` (Akim).

## 1. Contract + config (Egor)

- [ ] 1.1 [Egor] `[output]` config section (`formula_keys`, `norm_ref_keys`, `symbol_keys`, `default_symbol_kind`)
- [ ] 1.2 [Egor] `build_formula_payload` in `db.py` driven by `[output]`
- [ ] 1.3 [Egor] `search.query(query) -> dict` returning the payload; `--json` CLI mode

## 2. Symbol normalization (Egor)

- [ ] 2.1 [Egor] `parser/symbols.py`: NFKC, greek/pua/cyr maps, subscript, prime, multi-split, garbage filter
- [ ] 2.2 [Egor] `notation_entry.latex` column + ingest writes id/latex/meaning/unit

## 3. Rename storage dir (Egor)

- [ ] 3.1 [Egor] `norm-base` → `docs/normative-base` in code + `.gitignore`; downloads land in `docs/normative-base/`

## 4. Consume (Akim)

- [ ] 4.1 [Akim] Backend consumes `search.query(...)` and binds `symbols[].id` in the engine
- [ ] 4.2 [Akim] Frontend renders `latex`/`symbols[].latex` via MathJax and builds inputs from `symbols`

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
- `normatives-collector` (downloads into `docs/normative-base/`).

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
