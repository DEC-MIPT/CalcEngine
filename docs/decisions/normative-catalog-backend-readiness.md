# `normative-catalog-backend` (WP9): readiness record, 2026-10-03

- Date: 2026-10-03
- Change: `openspec/changes/normative-catalog-backend/` (owners Akim, backend zone, and
  Egor, data zone).
- Reviewers: `spec-reviewer` and `norm-traceability-checker` subagents, run by Akim for
  tasks 1.2 and 1.3.

Russian version: `normative-catalog-backend-readiness-rus.md`.

## Verdict

**READY; DOR met 2026-10-04.** `openspec validate normative-catalog-backend
--strict` and `openspec validate --all --strict` pass (20/20). The last `spec-reviewer`
pass (4) lists no blocker and no major finding; its two minors are fixed.
`norm-traceability-checker` passes. Egor confirmed the read contract and his section 2
on 2026-10-04 (task 1.4, see below).

## Task 1.4: Egor's confirmation (2026-10-04)

Egor's answers in `normative-catalog-backend-contract-akim.md` ("Answers", commit
`348955c`) agree to every item without changes:

1. Decision 1: schema `catalog_read`, the role `dec_normatives_reader` and its
   privileges, the `REVOKE` on `public`, the interim database `dec`. The ingestion runs
   as the owner through `DEC_DATABASE_URL`, which he keeps (his 2026-09-29 plan to
   rename it to `DEC_NORMATIVES_DATABASE_URL` is dropped, so the two variables stay
   distinct); the reader's password comes from `DEC_NORMATIVES_READER_PASSWORD`.
2. Decision 2: no column changes; he placed each parameter of the pilot in exactly one
   view. Nothing is applied to decision 2 before task 3.1.
3. Decision 3: `latex2sympy2` output is converted into the node set at ingestion; no
   extra node kinds or functions; a formula he cannot convert is not stored as bound.
4. Section 2: agreed with the split and the verify clauses.
   `feature/normative-catalog/data` branches from `develop`, where his pipeline is.
   Section 2 is due on `develop` by the end of 2026-10-04.

`design.md` (context, decisions 1-3) and `tasks.md` (branch point, task 1.4, DOR) record
the confirmation.

## `spec-reviewer`

| Pass | Blocker | Major | Minor | Verdict |
|---|---|---|---|---|
| 1 | 0 | 5 | 13 | NOT READY |
| 2 | 0 | 1 | 8 | NOT READY |
| 3 | 0 | 1 | 4 | NOT READY |
| 4 | 0 | 0 | 2 | READY |

Majors and how they were closed:

1. Pass 1: an input outside the method's range and off every table row would get `422`,
   against `calculation-api` ("Input outside the method's range is not a validation
   error"). Closed: when no row matches, the source runs the engine's applicability
   check first; a refusal gives `201` through a `CatalogSnapshot` (design decision 6,
   spec scenario "An input outside the range and off every row", task 5.3).
2. Pass 1: the unit of a method bound was never used. Closed: requirement "Method range
   from the catalog", design decision 11, tasks 5.2 and 5.4.
3. Pass 1: the table selectors changed the engine contract with no engine spec. Closed:
   delta `specs/calculation-engine/spec.md`, ADDED "Table value selectors"; tasks
   5.1a-5.1b and 8.1.
4. Pass 1: database, owner and reader credentials were unspecified. Closed: the
   interim database `dec`, the owner that runs the ingestion, the reader's password
   variable and `REVOKE CREATE ON SCHEMA public` (PostgreSQL 14) in design decision 1;
   Egor confirmed on 2026-10-04 (task 1.4).
5. Pass 1: Egor's task 2.3 was too large and its re-verification unprovable. Closed:
   split into 2.3-2.5; the coefficient check ends in a dated record in
   `docs/decisions/`, and statuses stay `unverified` (WP3 owns raising them).
6. Pass 2: the source and the engine compared a heading after different conversions,
   so a valid request could end in `500`. Pass 3: one paragraph still held the old rule.
   Closed in pass 3: both convert the heading to the input's base unit with the same
   call and compare there; an input typed in the heading's unit then matches exactly
   (design decision 6, engine delta, tasks 5.1a and 5.3).

The minors (one heading per parameter, more data breaches, the dropped 15-decimal rule,
the query count, the non-functional scenarios, the role's privileges, the import scan of
`ml/`, the single reader of `DEC_NORMATIVES_DATABASE_URL`, the placement of the source
in `services`, the Russian search, the `catalog_unavailable` and `invalid_input`
extensions of `calculation-api`, the drift risk of the synthetic views, the
`check_bounds` breach, the empty validated range, the hashable snapshot, the split of
task 5.1, an overflowing conversion) were fixed in the round after the pass that found
them.

## `norm-traceability-checker`

| Pass | Verdict | Findings |
|---|---|---|
| 1 | FAIL | 2 to fix, 4 recommended |
| 2 | PASS | 3 minor |

Pass 1: task 2.3 named table 5.5 without an edition and the coefficients of the pilot
without a document or an `unverified` mark; task 1.3 claimed every reference was a
placeholder; the engine, API and performance limits were not labelled as non-norm; the
exact heading match did not say that a rule between rows comes only from the norm.
All fixed. Pass 2 minors (task 1.3 wording, the source files of the real designations,
exact matching labelled as an API rule) were fixed. The only real designations are in
tasks 2.4 and 2.5 (СП 22.13330.2016, its table 5.5, the coefficients of the pilot),
  taken from `first-calculation-type-egor-pm.md` and
  `calculation-core-contract-formula-execution-akim.md`, all marked unverified.

## Section 2: `tester` GO and review (2026-10-05)

- **`tester` GO for `feature/normative-catalog/data`** (2026-10-05): every verify clause
  of tasks 2.1-2.6 holds; `ruff` and `mypy` clean; 78 tests pass; branch coverage of
  `normatives_pipeline.pilot_catalog` is 100%. The `tester` agent's first pass (NO-GO)
  found norm values in code and test data; this was fixed by moving the pilot's
  coefficient/threshold/formula values into the data registry `ml/configs/pilot.toml`
  (ingested into `dec_normatives`, mirroring `ml/configs/formulas.toml`), deriving the
  method bounds from the extracted table 5.5 headings, and replacing real values in test
  data with synthetic placeholders. The coefficient record of task 2.5 is
  `docs/decisions/normative-catalog-pilot-coefficients-egor.md`.
- **Review (Akim): pending.** Egor merged the feature into `develop` after the GO; Akim's
  review acknowledgement is the remaining step of task 2.7 (recorded here when he gives it).

## Section 2: Akim's review (2026-10-05)

Reviewed: the merge `a01b84a` of `feature/normative-catalog/data` (commits `2e19787`,
`6775c18`, `83f0815`) against `design.md` decisions 1-3, 6, 7 and 11, the spec
`normatives-catalog` and tasks 2.1-2.6, and against the backend side on
`feature/normative-catalog/backend` (`226d44f`). Read from the code only: my local `dec`
holds no ingested data, and ingestion and the pipeline's `pytest` are Egor's to run.

**Verdict: changes requested.** Task 2.7 is not done until B1 and M1 are fixed on
`fix/normative-catalog/data` and re-reviewed. The fix does not block my section 7 setup,
but task 7.1 cannot pass on the current data.

What matches the contract: the five `type_*` views and `documents`, `clauses`, `search`
have the columns and types of decision 2, with the tie order inside `search`; the role
gets `USAGE`, `SELECT` and `EXECUTE` only, the password goes through a bound parameter and
is never printed; the eleven pilot parameters match the backend's `Parameters` field by
field and each sits in the view of its kind; the symbols of formula 5.7 match the names
the engine binds (`M_gamma`, `k_z`, `gamma_II_prime`, ...); the heading `phi_II` is stored
in `deg`, the input's base unit, so the float match of decision 6 is exact; the binding
table has no value column; `ml/` does not import `app`.

### Blocker

- **B1. Ingesting any other document rewrites the pilot's catalog onto that document.**
  `ingest.py:151` calls `pilot_catalog.sync_pilot_catalog(conn, designation)` with the
  designation of the document being ingested, not `СП 22.13330.2016`. After СП 22, an
  ingestion of СП 24 or СП 31 deletes the pilot rows and writes them again against that
  document: the bindings, the `k_z` formulas and the constants of `pilot.toml` get its
  `document_id` (so `norm_refs.document` names the wrong norm), formula `5.7` and table
  `5.5` are looked up in it. The result is either a missing parameter (`503` for the
  pilot) or, if that document has a convertible `5.7` and a table `5.5`, a wrong formula
  with wrong citations. The tests do not catch it: the fixture calls
  `sync_pilot_catalog(conn)` with the default designation, and a unit test passes
  `"X"` as the designation and expects `True`. Fix: call it without the designation
  (or only when the ingested designation is the pilot's) and add a test that ingesting a
  second document leaves the pilot rows on СП 22.

### Major

- **M1. Formula 5.7 is stored `verified` / `human-verified`.** `ingest.py:97-98` gives
  every formula found in `formulas.toml` `status = verified`, `provenance =
  human-verified`; `pilot_catalog` binds `5.7` from it. The rule comes from
  `normatives-formula-contract` task 1.6 ("`formulas.toml` entries are `human-verified`",
  code in `0310df4`), which reached `develop` unreviewed (M3). This contradicts Egor's
  answer 2b (`pipeline-open-items-questions-akim.md`, "Answers": "No pilot formula or
  coefficient gets a `human-verified` provenance") and the rule of task 2.5 that raising a
  status is WP3's gate. The backend's `NormRef` accepts that pair with a concrete edition
  and clause, so the report would show step R as verified and undercount
  `unverified_step_count`. `test_status_and_provenance_on_every_view_row` checks only that
  no `machine-extracted` row is verified. Fix: store `5.7` as `unverified` /
  `machine-extracted` (or drop `formulas.toml`, as planned) and assert in the test that no
  pilot row is `verified` or `human-verified`.
- **M2. A tree symbol with no notation entry is stored as dimensionless.**
  `pilot_catalog._bind_registry_formula` maps units with
  `unit_symbol(units_by_symbol.get(symbol, ""))`, and `UNIT_SYMBOLS[""] = "1"`. A symbol
  that the notation does not list gets unit `1` instead of the formula being refused,
  which the spec "Expression tree form in the catalog" and task 2.2 ("a formula he cannot
  convert is not stored as bound") forbid. No harm in today's data (all 14 symbols of
  `5.7` have a notation entry in `formulas.toml`), but a missing unit is then invisible to
  the backend. Fix: refuse when a tree symbol or the result symbol has no notation entry;
  keep `""` -> `1` only for an entry that exists. The same applies to
  `notation_result_symbol`, which returns `"R"` when a formula has no notation: an
  implicit default in code, refused by the same check once M2 is fixed.
  The backend has the mirror gap (Akim's follow-up, not Egor's): `CatalogParameterSource`
  checks that every symbol has a unit from the list, but not that the unit of a symbol
  naming an input or an output is that quantity's base unit (`formula_step` compares
  units exactly, so the same dimension is not enough), and decision 7 does not list this
  breach.
  Such a catalog error therefore surfaces only in `formula_step` as `UnitError`, which
  `api/errors.py` maps to `422 invalid_input`, blaming the client instead of answering
  `503 parameter_source_unavailable`. I add the breach to decision 7 and the spec
  "Expression tree form in the catalog", and the check to the source on
  `feature/normative-catalog/backend` (task 5.6). The pilot's data already meet the rule:
  every input and output symbol of formulas `5.7` and `k_z_from` is in its base unit.
- **M3. Process.** The feature was merged before this review (AGENTS.md section 2,
  lifecycle step 7: GO, then review, then merge). The merge also brought the whole
  `feature/normative-formula-contract/data` into `develop` as its base (`320b61f` is on
  the first-parent line of `develop`), although `normatives-formula-contract` shows 0/22
  tasks, an unchecked DOR and no `tester` GO; AGENTS.md section 2 says a feature built on
  an unmerged one merges after it. Neither `feature/normative-formula-contract/data` nor
  `feature/normative-catalog/data` is on `origin` (`git ls-remote`, 2026-10-05), so the
  branches cannot be compared with `develop`. I do not ask for a revert. I ask Egor to
  record this here, and to get the `tester` GO for `normatives-formula-contract` on
  `develop` and tick its tasks, or to say which of its code is not done.

### Minor

- **m1. The pilot's catalog is written in several commits.** `sync_pilot_catalog` calls
  `delete_catalog_rows`, which commits, then `replace_catalog_formula` and five
  `insert_*` calls, each with its own commit. During an ingestion the backend can read the
  pilot with no rows or with half of them and answer `503`; a failure in the middle (a
  table that does not parse, a dropped connection) leaves the pilot broken until the next
  successful ingestion of СП 22. The risk is small, as ingestion is manual and rare. Fix:
  one transaction per type, rolled back on error (part of the recommendation below).
- **m2. The pipeline's catalog tests run on the working database.**
  `test_catalog_contract.py` and `test_pilot_catalog.py` connect with `DEC_DATABASE_URL`,
  that is the working `dec`, with no check that the database name ends in `_test`. They
  set the cluster-wide role `dec_normatives_reader` to the password `test-reader`, so on
  the machine that ran them the password of `DEC_NORMATIVES_READER_PASSWORD` stops working
  until the next ingestion; they also rewrite the pilot's rows and may ingest the PDF
  themselves. Fix: a separate database whose name ends in `_test`, refused otherwise, and
  a separate test role, as the backend does (`dec_normatives_test`,
  `dec_catalog_test_reader`).
- **m3. `k_z_from` shows one formula and computes another.** The LaTeX is
  `k_z = \frac{z_0}{b} + 0.2`, the tree `8/b + 0.2`. The white-box step shows `z_0`, while
  its substitutions list only `b`, so the reader cannot see where 8 comes from; the 8 m is
  a bare number without a unit and gives the right result only because `b` reaches the
  formula in metres. Fix: the LaTeX shows `8` (`k_z = \frac{8}{b} + 0.2`). Making `z_0`
  a symbol with its own value and unit would need a new field in the pilot's
  `Parameters`, a contract change on the backend side.
- **m4. The method bounds cite the wrong place.** The bounds `phi_II` in [0 deg, 45 deg]
  are derived from the extent of table 5.5 but carry clause `5.6.7`. A refusal by the
  range then sends the engineer to clause 5.6.7, which states no range. Egor's record of
  task 2.5 itself says "clause 5.6.7, table 5.5". Fix: `NormRef.clause` = `табл. 5.5`.
- **m5. The reader role keeps `TEMP`.** In PostgreSQL 14 every role gets `CONNECT` and
  `TEMP` on a database through `PUBLIC` by default, so the reader can create a temporary
  table, and the spec scenario "The reader role cannot write" ("or to create an object in
  any schema") is not met at the role level. The backend's read-only transactions refuse
  it, so there is no practical harm. Fix: `REVOKE TEMP ON DATABASE dec FROM PUBLIC`
  during ingestion (the owner, a superuser, keeps it), or record it as an accepted
  deviation.
- **m6. `pre-commit run --all-files` fails on `develop` again.** `detect-secrets` reports
  seven findings, all from Egor's commits that arrived on 2026-10-05 (WP9 data feature,
  `normatives-formula-contract` and research). Six are the local URL with `dec:dec` and
  no `# pragma: allowlist secret`: `ml/research/make_review_html.py:14`,
  `ml/research/verify_end_to_end.py:23`,
  `ml/src/normatives_pipeline/parser/cyrillic.py:11`, `ml/research/VERIFY.md:26`,
  `docs/decisions/normatives-formula-contract-implementation-egor.md:74` and
  `docs/decisions/normatives-pipeline-end-to-end-verification-egor.md:4`. The seventh is a
  false positive, `ml/src/normatives_pipeline/catalog_contract.py:15`: a constant that
  holds the name of the reader's password variable, not a password. The hook checks only the
  files of a commit, so the commits that brought these were made without it. Under
  AGENTS.md section 2 a new finding is removed from the file or marked there as a
  placeholder, never added to the baseline in passing. Fix: mark the seven lines (or
  write the URLs without the password), then `pre-commit install` on Egor's machine. I
  did not touch these files or `.secrets.baseline`.

### Notes for the backend side (no action for Egor)

- `γc1 = 1.1`, `γc2 = 1.0` and `k = 1.0` hold for one soil row, a flexible structural
  scheme and directly tested soil properties
  (`normative-catalog-pilot-coefficients-egor.md`). The pilot has no input for these
  conditions, so its result is right only in that case. The form or the report has to
  state the conditions, or the contract needs inputs for them (Akim and PM).
- Table 5.5 has a row per whole degree, and there is no interpolation rule, so a
  non-integer `phi_II` inside [0, 45] gets `422`. The input form needs to say so.

### Recommendation before a second calculation type (Egor's zone, his decision)

The fix of B1 (call `sync_pilot_catalog(conn)` without the designation) is enough for the
pilot. It does not scale to the next types (for example deep foundations and internal
water supply): `pilot_catalog.py` hard-codes one type, one document (`DESIGNATION`,
`pilot.toml` `[document]`), the binding list, the shape of table 5.5 in
`parse_heading_rows`, and method bounds taken from that table's extent. A type may draw
on several documents, and its catalog must not depend on the order in which documents
are ingested.

I recommend splitting ingestion into two steps before a second type is added:

1. **Document ingestion** fills only the document layer (`document`, `clause`,
   `formula`, `notation_entry`, `coefficient`, ...) and knows nothing about calculation
   types, so documents can be loaded in any order.
2. **Type catalog build**, a separate command (for example
   `python -m normatives_pipeline.catalog sync [--type <name>]`), also run at the end of
   `ingest` for every type whose registry names the ingested document:
   - one registry per type in Egor's zone (for example `ml/configs/types/<type>.toml`),
     naming for each parameter its document, formula number, table with its heading
     column and value columns, threshold clause and method bounds, never a value in code
     (spec "Calculation type binding by name": "the pipeline SHALL fill it from a registry
     it owns");
   - each type rebuilt in one transaction (this also settles m1);
   - a type whose documents are not all ingested is not built, so the backend answers
     `503 parameter_source_unavailable` for that type only (scenario "A calculation type
     with no binding"); re-ingesting one document rebuilds only the types that name it.

The read contract (`catalog_read`, decision 2) does not change: the views are already
keyed by `calculation_type`, and the backend's `CatalogParameterSource` is generic. Two
limits of the contract are likely to come up with the next types and would need a change
of their own: formulas with Σ/∏ (`formula-autoparse-limits-egor.md`; Egor counts 10 such
formulas in СП 24.13330.2021, 5 of them parsed), and a table selected by two inputs,
which decision 2 does not allow.
