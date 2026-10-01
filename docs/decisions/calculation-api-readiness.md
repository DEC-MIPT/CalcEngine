# `calculation-api` (WP8): readiness record, 2026-10-02

- Date: 2026-10-02
- Change: `openspec/changes/calculation-api/` (owner Akim, backend zone).
- Reviewers: `spec-reviewer` and `norm-traceability-checker` subagents, run by Akim for
  tasks 1.2 and 1.3.

Russian version: `calculation-api-readiness-rus.md`.

## Verdict

**READY for DOR.** `openspec validate calculation-api --strict` and
`openspec validate --all --strict` pass (19/19). The last `spec-reviewer` pass lists no
blocker and no major finding; its three minors are fixed. `norm-traceability-checker`
passes: the change fixes no formula, coefficient, limit, tolerance or rounding rule, and
names no norm document or edition.

## `spec-reviewer`

| Pass | Blocker | Major | Minor | Verdict |
|---|---|---|---|---|
| 1 | 0 | 6 | 7 | NOT READY |
| 2 | 0 | 0 | 3 | READY |

Pass 1 majors and how they were closed:

1. The server could not start without `DEC_APP_DATABASE_URL`, since the params root sat
   in `Settings`. Closed: `DEC_PARAMS_ROOT` moved to `ApiSettings` (no required field);
   `Settings` is read lazily; a missing or unreachable database gives
   `503 database_unavailable` (design decision 7, task 3.3).
2. The status mapping lacked `413`, the unknown route and the wrong method. Closed: the
   requirement "Error responses" holds the full table (404, 405, 409, 413, 422, 503, 500)
   with scenarios.
3. "Naming the input" had no shape. Closed: every `422` has `fields`; `invalid_input`
   uses the location `["body", "inputs", "<input name>"]`, one entry per input.
4. A report of a result whose type is no longer registered was `404` in the design only.
   Closed: `409 calculation_type_not_registered` in the spec, the design and tasks 4.4,
   5.4.
5. Tasks 2.3, 4.2 and 5.2 were larger than one session. Closed: split into 2.3-2.5,
   3.3, 4.2-4.4 and 5.2-5.5.
6. The DOR item "Dependencies satisfied" was open without reasoning. Closed: the WP2
   tasks used are named and implemented on the start branch; WP2 task 6.2 (Egor's task
   1.8) affects only the merge order.

Pass 1 minors 7-13 (re-run wording, measurable latency, relation to the `web-platform`
requirements, `405` on change methods, log checks for `422` and `503`, open questions,
the WP2 origin of "Applicability check with three outcomes") were fixed in the same
round. Pass 2 minors (the code of an unknown unit, the error naming the value in task
4.1, `GET /calculation-types` without the database URL in task 5.1) were fixed after
pass 2.

## `norm-traceability-checker`

| Pass | Blocker | Major | Minor | Verdict |
|---|---|---|---|---|
| 1 | 0 | 0 | 2 | pass with minors |
| 2 | 0 | 0 | 0 | PASS |

Pass 1 minors: an example in design decision 3 named a norm table without its document
and edition (made generic), and the requirement did not say that an engineer-set
rounding rule carries its source (added, with a scenario and a check in task 4.1).

## Decisions taken by Akim during the review

- The calculation engine and the report generator stay synchronous; background jobs in
  `worker` remain a non-goal (2026-10-02).
