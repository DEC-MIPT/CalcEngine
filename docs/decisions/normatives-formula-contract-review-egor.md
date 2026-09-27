# `normatives-formula-contract` against the agreed `NormRef`: review for Egor

- Date: 2026-09-27
- From: Akim. To: Egor (author of `normatives-formula-contract`).
- Reviewed: `openspec/changes/normatives-formula-contract/` and its implementation on `feature/normative-parser/ml` (commit `6daf2ef`): `normatives_pipeline/parser.toml` `[output]`, `normatives_pipeline/db.py` `build_formula_payload`, the example in `docs/decisions/normatives-pilot-usage-akim.md`. The change is not on `develop` yet.
- Compared with: the `NormRef` you agreed to in `docs/decisions/normref-questions-egor.md` (commit `a1a896c`), recorded in `openspec/changes/calculation-core-contract/design.md`, section "NormRef".
- Purpose: the formula payload is the handoff from your pipeline to the engine, so its norm reference must be the agreed `NormRef`. Nothing here is final until you answer.

Russian version: `normatives-formula-contract-review-egor-rus.md`.

## The two shapes

Agreed `NormRef`:

```
NormRef { document, edition, clause, status, provenance }
```

Payload `norm_ref` today (`parser.toml`: `norm_ref_keys = ["designation", "clause", "formula"]`):

```json
{"designation": "СП 45.13330.2017", "clause": "13.8", "formula": "13.8#1"}
```

## Findings

| # | Sev. | Finding | Why it matters | Proposal |
|---|---|---|---|---|
| 1 | Major | No `provenance` | You agreed that the parameters layer rejects `machine-extracted` values (answer 2). Formulas come from the parser, with an ML fallback (`pix2tex`, `normatives-parser` proposal). Without `provenance` the gate cannot tell a checked formula from an extracted one, and an ML-extracted formula could reach the engine, against "no ML in the calculation path" | Carry `provenance`; every parser output is `machine-extracted` until a person checks it |
| 2 | Major | No `status` | The engine counts steps whose references are not verified (`unverified_step_count`); a verified reference needs a concrete edition and clause | Carry `status`; parser output is `unverified` |
| 3 | Major | No `edition` | You set `edition` as `<YYYY>` or `<YYYY>+<N>` (answer 8). The designation string holds the year but not the amendment, so a result cannot be pinned to one exact text version (answer 7) | Carry `edition` separately, in your syntax |
| 4 | Major | Two locators in one reference: `clause` "13.8" and `formula` "13.8#1" | You agreed one locator per `NormRef` (answer 5) and set the canonical grammar (clause, table, formula). "13.8#1" is an internal id, not that grammar | One locator per reference, in your canonical grammar; keep the internal formula id as a separate payload field if needed |
| 5 | Major | Reference keys are set by config (`norm_ref_keys`), and the NO-GO forbids hard-coded contract fields | A shared interface that a config line can change can silently drop `status` or `provenance` from what the engine receives | Fix the `NormRef` fields in the spec as the agreed interface; let config choose optional extra fields only |
| 6 | Minor | `designation` instead of `document` | Same meaning (answer 6), different name; the engine, the report, and `dec_app` columns use `document` | Rename to `document` |
| 7 | Minor | Missing values become empty strings (`formula.get("designation", "")`, `clause_number or ""`) | No field may be null, and an unknown edition or clause is the literal `unverified` (answer 4); an empty string is neither | Write `unverified` for an unknown edition or clause; a formula with no document does not enter the payload |
| 8 | Minor | The spec scenario is titled "NormRef" but lists other fields | Two meanings of one name across the specs | Make the scenario require the agreed `NormRef` |
| 9 | Info | `symbols[].unit` can be empty (example: `"unit": ""`) | Every input and output carries a unit (`agent-docs/domain-constraints.md`; WP2 "Explicit units at the boundary"); the engine cannot register a quantity without one | Keep the empty value visible as missing; the engineer fills it before a type is registered |

## Questions

### 1. Do you agree to findings 1-8?

**Answer.**

### 2. Where does the engine get formulas from?

The contract's task 4.1 has the backend call `search.query(...)` and bind `symbols[].id` in
the engine. In `calculation-core-contract`, the engine is a pure function that receives
resolved parameters from the caller, and the parameters layer is the only point where
values enter the engine (your answer 2). This is also the open question "formulas in YAML
vs in code" (`calculation-core-contract` task 7.2, WP5).

- **Proposal.** The pipeline delivers formulas into `dec_normatives`; the parameters layer
  reads them, applies the `provenance` gate, and passes resolved parameters to the engine.
  The backend does not import pipeline code, so the zones stay apart.
- **The formula registry.** Your journal (entries 20-21) makes the hand-entered registry
  `normatives_pipeline/formulas.toml` the MVP path for formulas, because OCR of formulas
  is not reliable yet. `backend-layered-architecture` plans parameter files under
  `params/` in the parameters layer (backend). Which one holds the formulas the engine
  runs, and who owns it?
- **Your side.** Agree, or describe the path you intended, and name the owner of the
  registry.

**Answer.**

### 3. Tasks 4.1 and 4.2 are in Akim's zone

They assign backend and frontend work to Akim and name the branch
`feature/normative-formula-contract/backend`. Akim has not agreed to them yet. Proposal:
leave them out of this change until question 2 is settled; Akim adds the consuming side
to his own change.

**Answer.**

### 4. Merge to `develop`

The change and its documents for Akim (`normatives-pilot-usage-akim.md`,
`normatives-postgres-storage.md`) are only on your branch. `AGENTS.md` asks that no-code
documents be merged into `develop` as soon as they are ready. Can you merge them after
answering questions 1-3?

**Answer.**

## Storage and search

Added 2026-09-27 after reading the rest of `feature/normative-parser/ml` (commit
`6daf2ef`). Summary for Akim: `docs/reports/egor-branches-analysis.md`.

### 5. One database or two?

`docker-compose.yml` starts one PostgreSQL database `dec` with one user `dec`.
`backend-layered-architecture` (decision 4) plans two databases in one instance,
`dec_app` (users, calculations, reports) and `dec_normatives` (documents, revisions,
clauses, formulas, coefficients), with separate Alembic trees; the roadmap (WP5,
requirement 5) adds separate database roles per zone.

- **Your side.** Is `dec` meant to become `dec_normatives`? Can the compose file create
  both databases and a role per zone?

**Answer.**

### 6. Revisions

`document.designation` is UNIQUE and there is no revision table. In answers 7 and 8 you
agreed that revisions are stored additively (an old `Revision` stays readable after a new
one appears) and that `amendment_no` lives in `Revision`. `backend-layered-architecture`
plans the models `Document`, `Revision`, `Clause`, `Formula`, `Coefficient`.

- **Your side.** Is the current schema provisional until `norm-source-traceability`
  (WP3)? When will revisions appear?

**Answer.**

### 7. Coefficient tables

Tables are extracted (`extract_tables`, `pdfplumber`, first 15 pages in entry 13) but
not stored. The candidate first type, R by formula 5.7 of СП 22.13330.2016 (from
`formulas.toml`), takes `M_γ`, `M_q`, `M_c` from table 5.5.

- **Your side.** When and in what form will coefficient tables be stored, each value with
  its `NormRef`? Without them the pilot cannot run R.

**Answer.**

### 8. A read-only query API for the backend

`search.query()` calls `db.init_schema` on every call, so each query runs `CREATE TABLE`
and `ALTER TABLE`. `db.py` also falls back to `postgresql://dec:dec@localhost:5433/dec`
when `DEC_DATABASE_URL` is not set.

- **Proposal.** Schema changes run only at ingestion; the backend gets a read-only
  function and a read-only role; a missing `DEC_DATABASE_URL` is an error, not a silent
  fallback.
- **Your side.** Agree, or propose another split.

**Answer.**

### 9. Lexical search: `pg_trgm` or `tsvector`?

Journal entry 14 chooses `pg_trgm` for MVP search, and `backend-layered-architecture`
(task 4.3) plans GIN + `pg_trgm`. The code uses `to_tsvector('simple', search_text)` over
pre-lemmatized text.

- **Your side.** Which one is the decision? The other spec needs to follow it.

**Answer.**

### 10. Locator of a formula without a number

In СП 45.13330.2017 many formulas have no number (entry 19). You suggest taking the
clause number or a synthetic number. A `NormRef` locator must not look like a formula
number printed in the document (no invented clause or formula numbers).

- **Proposal.** Locate such a formula by its clause in your canonical grammar, and never
  write a number the document does not print; if an internal id is needed, keep it
  outside `NormRef`.
- **Your side.** Agree, or give the syntax you want.

**Answer.**

## For information (no answer needed)

- Both of your branches edit the same `.gitignore` line differently (`norm-base/` on
  `feature/normative-collector/data`, `norm-docs/` on `feature/normative-parser/ml`), so
  merging the second one will conflict.
- `normatives-postgres-storage.md` says the compose file is not in the repository, but
  `docker-compose.yml` is on the same branch.
- The search rules of entries 16-17 (lower case, ё→е in query and document,
  lemmatization) are product behavior; they could become a requirement of
  `normatives-catalog` or `normatives-parser`.
