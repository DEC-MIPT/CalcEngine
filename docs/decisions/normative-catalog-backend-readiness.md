# `normative-catalog-backend` (WP9): readiness record, 2026-10-03

- Date: 2026-10-03
- Change: `openspec/changes/normative-catalog-backend/` (owners Akim, backend zone, and
  Egor, data zone).
- Reviewers: `spec-reviewer` and `norm-traceability-checker` subagents, run by Akim for
  tasks 1.2 and 1.3.

Russian version: `normative-catalog-backend-readiness-rus.md`.

## Verdict

**Content READY; DOR waits for task 1.4.** `openspec validate normative-catalog-backend
--strict` and `openspec validate --all --strict` pass (20/20). The last `spec-reviewer`
pass (4) lists no blocker and no major finding; its two minors are fixed.
`norm-traceability-checker` passes. The change becomes ready for implementation when
Egor confirms the read contract and his section 2 (task 1.4,
`normative-catalog-backend-contract-akim.md`).

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
   Egor confirms in task 1.4.
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
