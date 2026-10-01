# `normative-catalog-backend`: questions for Egor (2026-10-01)

- Date: 2026-10-01
- From: Akim. To: Egor.
- Context: I am finishing the backend in three changes. `calculation-api` (calculation
  types, calculations, stored results in `dec_app`, `.docx` download) and
  `user-accounts-auth` (test accounts, login, JWT) are in my zone only.
  `normative-catalog-backend` is ours together: it gives the backend read access to
  `dec_normatives`, full-text search over it, and the formulas, table values and
  thresholds a calculation needs. WP2 task 7.1c (the pilot R on catalog data) moved into
  it on 2026-10-01, so the engine branch no longer waits for it. I create the proposal
  once you answer items 1-4.

Russian version: `normative-catalog-backend-questions-akim-rus.md`.

## 1. Item 9.3: where the read code lives

Your position (`backend-layered-architecture-split-egor-ack.md`): the ingestion and
catalog code stays in `normatives_pipeline/`, with no second loader in
`backend/normatives/`. Your answer to question 8
(`normatives-formula-contract-review-egor.md`): the backend gets a read-only function and a
read-only role. WP5's spec forbids any backend import from `ml/`, where your package
moves, so the backend cannot call your Python function.

- **Proposal.** The contract between our zones is the database, not Python code. You own
  a small set of read-only SQL views or SQL functions in `dec_normatives`, created by your
  ingestion and versioned with it, and a read-only role that may only select from them.
  The backend reads only those, through its own repository (SQLAlchemy Core,
  parameterized queries), with `DEC_NORMATIVES_DATABASE_URL`. No loader is duplicated:
  you write the data, I only read the views.
- **Your side.** Agree, or name another contract that keeps both imports rules
  (backend never imports `ml/`, `ml/` never imports `backend/`).

## 2. What the views return

What the backend needs, by use:

- **Search** (`normatives-catalog` "Full-text search"): documents, clauses and formulas
  that match a query, ranked by `pg_trgm` similarity (your answer 9), each with the
  document designation, edition and clause or formula number.
- **A document and its clauses**, by id, for the catalog page.
- **One calculation type's resolved parameters**: for each formula of the method its
  expression tree (WP2 decision 11) with the unit of every symbol; for each table value
  and threshold its value and unit; and for every one of them the five `NormRef` fields
  (`document`, `edition`, `clause`, `status`, `provenance`).
- **The method's range of application** (WP2 decision 15): each bound with its quantity,
  kind, value, inclusiveness and `NormRef` list.

- **Your side.** Agree with this list, and say which part exists on
  `feature/normative-parser/ml` today. I read there: `formula` has no tree column yet, and
  `status`/`provenance` are still constants in `build_formula_payload`.

## 3. Binding a calculation type to its norms

`normatives-catalog` "Binding a normative to a calculation type" needs a record of which
formulas, table cells and bounds of which document a calculation type uses. This is not a
norm value, so it is not forbidden in `.yaml`, but it is catalog data.

- **Proposal.** The binding lives in `dec_normatives`, next to the norms it names, and is
  filled by your ingestion from a small registry that you own. The backend looks a type's
  parameters up by the type's name (`foundations_shallow_r` for the pilot).
- **Your side.** Agree, or keep the binding on the backend side (a `.yaml` per type that
  names formula numbers and table cells, never values).

## 4. Table lookup by an input value

The pilot needs `M_γ`, `M_q`, `M_c` of table 5.5 for the engineer's `φ_II`. The engine
takes one `TableValue` per symbol, so something has to pick the row. The `coefficient`
table holds `row_index` and `col_index`, not the value of the row heading.

- **Proposal.** Store the heading value of each row and column with its unit (for table
  5.5, `φ_II` in degrees), so the backend selects the row whose heading equals the input.
  An input between two rows is refused until the norm's own rule for it is recorded with
  its clause; the backend does not interpolate on its own.
- **Your side.** Agree, or say how you would key the cells.

## 5. Reminder: WP2 task 1.8

`calculation-core-contract-formula-execution-akim.md`, items 1, 3 and 4 (the amendment of
resolution 2, the expression tree you store, the `input_hash` algorithm), still waits for
your acknowledgement. It is the last item that holds back the merge of
`feature/calculation-engine/backend`.

## 6. Timing

- When do you expect `normatives-formula-contract` tasks 1.4-1.7 and the move to `ml/` on
  `develop`?
- When will `retarget-mvp-domain` task 3.1 (the in-scope list of `foundations-shallow`)
  be filled?

None of this blocks `calculation-api` or `user-accounts-auth`: until the catalog source
exists, the calculation endpoint returns a defined error for a type with no parameter
source, and its tests use synthetic parameters.
