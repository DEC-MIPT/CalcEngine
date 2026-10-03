# Proposal

## Why

The normatives parser extracts formulas, notation, and cross-references from downloaded СП
into PostgreSQL. Akim's backend and frontend must consume those formulas to compute and
render them, but today there is no fixed, versioned data contract between the pipeline and
the engine — the shape lives only in code and in ad-hoc terminal output. Without a contract
every consumer re-implements a different mapping.

## What Changes

- New capability `normatives-formula-contract`: the structured formula payload handed to
  the backend — `norm_ref`, `latex`, `symbols` (id/latex/meaning/unit/kind), `expression`,
  `cross_refs` — with the shape driven by config (`parser.toml` → `[output]`).
- A query API returning that payload (`normatives_pipeline.search.query`) with a `--json`
  CLI mode for inspection.
- Symbol normalization to LaTeX (`src/normatives_pipeline/parser/symbols.py`): Unicode math
  alphanumerics, Greek, a PUA stopgap map, subscript, multi-symbol split, garbage filter.

## Non-goals

- No production calculation: `expression` is carried, never executed by the pipeline.
- No expression derivation from LaTeX (`parse_latex` is unreliable — see journal Entry 13).
- No full-text redistribution; `docs/normative-base/` is gitignored.
- No ML in the calculation path.

## Capabilities

### New Capabilities

- `normatives-formula-contract`: the config-driven structured formula payload consumed by
  the backend and frontend.

## Impact

- New config keys (`[output]`), a payload builder in `src/normatives_pipeline/db.py`, and
  `src/normatives_pipeline/parser/symbols.py`. Akim's backend consumes `search.query()`; no
  change to the engine beyond the contract.
