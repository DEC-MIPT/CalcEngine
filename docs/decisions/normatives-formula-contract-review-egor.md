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

**Answer.** Agree to all eight. My payload diverges from the `NormRef` I already agreed to. Fix: `norm_ref` carries `document`, `edition`, `clause` (one locator, canonical grammar), `status`, `provenance`; the parser emits `provenance = "machine-extracted"` and `status = "unverified"` (with `edition = "unverified"` until checked); the internal id `13.8#1` moves to a separate payload field (`formula_id`) outside `NormRef`; `designation` is renamed to `document`; missing values become the literal `unverified` (never an empty string); the `NormRef` fields are fixed in the spec, and config selects only extra fields. (Finding 9, empty `unit`: keep it visible as missing; the engineer fills it before a type is registered.)

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

**Answer.** Agree. The pipeline writes formulas into `dec_normatives`; the parameters layer reads them, applies the `provenance` gate, and passes resolved parameters to the engine; the backend does not import pipeline code. The hand-entered registry `normatives_pipeline/formulas.toml` stays the MVP path for executable expressions, and I (Egor, data zone) own it.

### 3. Tasks 4.1 and 4.2 are in Akim's zone

They assign backend and frontend work to Akim and name the branch
`feature/normative-formula-contract/backend`. Akim has not agreed to them yet. Proposal:
leave them out of this change until question 2 is settled; Akim adds the consuming side
to his own change.

**Answer.** Agree. Remove tasks 4.1 and 4.2 from this change. Akim adds the consuming side to his own change.

### 4. Merge to `develop`

The change and its documents for Akim (`normatives-pilot-usage-akim.md`,
`normatives-postgres-storage.md`) are only on your branch. `AGENTS.md` asks that no-code
documents be merged into `develop` as soon as they are ready. Can you merge them after
answering questions 1-3?

**Answer.** Yes. I merge the change and the Akim-facing documents (`normatives-pilot-usage-akim.md`, `normatives-postgres-storage.md`) into `develop` after these answers.

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

**Answer.** `dec` becomes `dec_normatives`. The compose file should create both `dec_app` and `dec_normatives` in one instance with a role per zone; for the MVP I keep `dec_normatives` and add `dec_app` when the backend needs it.

### 6. Revisions

`document.designation` is UNIQUE and there is no revision table. In answers 7 and 8 you
agreed that revisions are stored additively (an old `Revision` stays readable after a new
one appears) and that `amendment_no` lives in `Revision`. `backend-layered-architecture`
plans the models `Document`, `Revision`, `Clause`, `Formula`, `Coefficient`.

- **Your side.** Is the current schema provisional until `norm-source-traceability`
  (WP3)? When will revisions appear?

**Answer.** Yes, the current schema is provisional until `norm-source-traceability` (WP3). Revisions (`Revision` with `amendment_no`, additive storage) appear in WP3.

### 7. Coefficient tables

Tables are extracted (`extract_tables`, `pdfplumber`, first 15 pages in entry 13) but
not stored. The candidate first type, R by formula 5.7 of СП 22.13330.2016 (from
`formulas.toml`), takes `M_γ`, `M_q`, `M_c` from table 5.5.

- **Your side.** When and in what form will coefficient tables be stored, each value with
  its `NormRef`? Without them the pilot cannot run R.

**Answer.** `extract_tables` already extracts tables; I add persistence now (this iteration), starting with table 5.5 of СП 22.13330.2016, each value with its own `NormRef` (`document`, `edition`, `clause` = the table cell, `status = "unverified"`, `provenance = "machine-extracted"` until checked). Until then the R pilot can take `M_γ`, `M_q`, `M_c` from a manually verified table 5.5 in the registry.

### 8. A read-only query API for the backend

`search.query()` calls `db.init_schema` on every call, so each query runs `CREATE TABLE`
and `ALTER TABLE`. `db.py` also falls back to `postgresql://dec:dec@localhost:5433/dec`
when `DEC_DATABASE_URL` is not set.

- **Proposal.** Schema changes run only at ingestion; the backend gets a read-only
  function and a read-only role; a missing `DEC_DATABASE_URL` is an error, not a silent
  fallback.
- **Your side.** Agree, or propose another split.

**Answer.** Agree. Schema changes run only at ingestion; the backend gets a read-only function and a read-only role; a missing `DEC_DATABASE_URL` is an error, not a silent localhost fallback.

### 9. Lexical search: `pg_trgm` or `tsvector`?

Journal entry 14 chooses `pg_trgm` for MVP search, and `backend-layered-architecture`
(task 4.3) plans GIN + `pg_trgm`. The code uses `to_tsvector('simple', search_text)` over
pre-lemmatized text.

- **Your side.** Which one is the decision? The other spec needs to follow it.

**Answer.** `pg_trgm` is the decision (journal entry 14). I align the spec and the code to `pg_trgm` + GIN and drop the `tsvector` path.

### 10. Locator of a formula without a number

In СП 45.13330.2017 many formulas have no number (entry 19). You suggest taking the
clause number or a synthetic number. A `NormRef` locator must not look like a formula
number printed in the document (no invented clause or formula numbers).

- **Proposal.** Locate such a formula by its clause in your canonical grammar, and never
  write a number the document does not print; if an internal id is needed, keep it
  outside `NormRef`.
- **Your side.** Agree, or give the syntax you want.

**Answer.** Agree. Locate a formula without a number by its clause in the canonical grammar; never invent a number the document does not print. The internal id stays outside `NormRef`.

## For information (no answer needed)

- Both of your branches edit the same `.gitignore` line differently (`norm-base/` on
  `feature/normative-collector/data`, `norm-docs/` on `feature/normative-parser/ml`), so
  merging the second one will conflict.
- `normatives-postgres-storage.md` says the compose file is not in the repository, but
  `docker-compose.yml` is on the same branch.
- The search rules of entries 16-17 (lower case, ё→е in query and document,
  lemmatization) are product behavior; they could become a requirement of
  `normatives-catalog` or `normatives-parser`.

## Check of commit `b44d6f3` (2026-09-27)

Akim checked the code on `develop` (merge `02a33de`) against your answers above:
`normatives_pipeline/db.py`, `parser.toml` `[output]`, `search.py`, `docker-compose.yml`,
and the spec and tasks of `normatives-formula-contract`. Tests were not run by Akim (your
zone).

Closed:

- Findings 1-3, 6: `norm_ref` carries `document`, `edition`, `clause`, `status`,
  `provenance`; parser output is `status = "unverified"`, `provenance =
  "machine-extracted"`; an unknown edition is `unverified`.
- Finding 4 and question 10: one locator per reference (`форм. (N)`, or `п. X` for a
  formula without a number); the internal id is the payload field `formula_id`; an
  unknown clause is `unverified`.
- Finding 8: the spec requires the agreed `NormRef` and has a scenario for `formula_id`.
- Question 8 (part): `search.query()` no longer runs DDL; a missing `DEC_DATABASE_URL`
  raises an error.
- Question 9: search uses `pg_trgm` (`similarity`).
- Question 7 (part): a `coefficient` table stores table cells, with the table number taken
  from the caption.

Still open:

| # | What | Evidence | Why it matters | Proposal |
|---|---|---|---|---|
| 11 | Coefficients have no `NormRef` | `coefficient` holds `table_number`, `page`, `row_index`, `col_index`, `value`; no edition, status, or provenance, and no function builds a `NormRef` for a value | Your answer to question 7: "each value with its own `NormRef`". The engine and the report need it for every coefficient of R | Build a `NormRef` per value (`document`, `edition`, `clause` = the table in your grammar, `status`, `provenance`), the same way as for formulas |
| 12 | Verification state is not stored | `status` and `provenance` are constants in `build_formula_payload`; no column holds them; formulas from the hand-entered registry `formulas.toml` also come out `machine-extracted` | The parameters layer rejects `machine-extracted` (your answer 2), so nothing, including the pilot R and its table, can pass the gate. There is no place to record that a person checked a formula or a value | Store `status` and `provenance` per formula and per coefficient, and define the step that sets `human-verified` (who, how it is recorded) |
| 13 | `NormRef` keys still come from config | `build_formula_payload` filters by `norm_ref_keys` from `parser.toml` | Finding 5: one config line can drop `status` or `provenance`; the spec now fixes the five fields, the code does not | Build the five fields unconditionally; keep config for extra payload fields only |
| 14 | Tasks 4.1 and 4.2 are still in the change | `openspec/changes/normatives-formula-contract/tasks.md`, section 4 | Your answer to question 3: "I remove tasks 4.1 and 4.2" | Remove them; Akim adds the consuming side to his own change |
| 15 | `document` can be an empty string | `formula.get("designation", "")` | A `NormRef` without a document is not a reference (answer 4) | Treat a missing document as an ingestion error |

Expected and not a finding: the database is still `dec` with one user (question 5: you
move to `dec_normatives` and add `dec_app` when the backend needs it); a read-only role
does not exist yet (question 8).

**Answer (11-15).**

Agreed to all five.

- **11 — a `NormRef` per coefficient value.** Agreed. Every stored coefficient value gets
  its own `NormRef` with the five agreed fields: `document`, `edition`, `clause` (the table
  locator in the canonical grammar, e.g. `табл. 5.5`), `status`, `provenance`. The
  `coefficient` table gains those fields; a value that a person has not checked is
  `status = "unverified"`, `provenance = "machine-extracted"`. I start with table 5.5 of
  СП 22.13330.2016 for the R pilot. A coefficient with no `document` is an ingestion error,
  the same rule as 15.
- **12 — verification state is stored.** Agreed. `status` and `provenance` become stored
  values for every formula and every coefficient, and `build_formula_payload` reads them
  instead of using constants. The step that writes `human-verified` is the user-side
  verification action (the engineer marks "верно"/"косяк"), which is the open product/UI
  decision in `formula-verification-akim.md`; I do not invent it here. Until that is
  settled the pipeline stores `provenance = "machine-extracted"`, `status = "unverified"`
  for OCR output. Entries of the hand registry `formulas.toml` are the verified subset
  (research journal, entry 10) and are stored as `human-verified`; the value comes from the
  stored column, not from a constant. This makes `human-verified` reachable for the pilot R
  and its table 5.5, so the `provenance` gate is not empty.
- **13 — fix the five fields in code.** Agreed. `build_formula_payload` builds `document`,
  `edition`, `clause`, `status`, `provenance` unconditionally; `norm_ref_keys` no longer
  decides the fixed set, and config selects only extra payload fields.
- **14 — remove tasks 4.1, 4.2.** Agreed. Removed from
  `openspec/changes/normatives-formula-contract/tasks.md` with this answer; the consuming
  side goes to your change.
- **15 — missing `document`.** Agreed. A formula or coefficient without a document is an
  ingestion error; the payload is never built from an empty string.

Note on 11-12: the OCR direction (research journal, entries 10-12) makes OCR the primary
source and the hand registry the verified subset. That is exactly why the verification
state has to be a stored value and not a constant, and why `human-verified` is written by
the verification action, not by ingestion.

Applied on `feature/normative-parser/ml`; answers 1-10 above stay as they were.
