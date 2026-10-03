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

## Re-review after Egor's answers (2026-10-03)

Two `spec-reviewer` passes on the current text after commit `11bdca4` (task 1.8 of
`calculation-core-contract` closed with the `input_hash` algorithm unchanged; Egor's
pipeline moved to `ml/` and `infra/`). First pass: 0 blockers, 0 major, wording minors
(task 1.8 passages in the present tense, paths, the open-points paragraph), all fixed.
Second pass: 0 blockers, 0 major, no finding. **READY for DOR.**

## Amendment: units of each input in the types listing (2026-10-03)

Before task 5.3, a check of the client side showed that the input form (`web-platform`
"Calculation input form", modified in the WP1 delta: fields from the type's contract, no
hard-coded fields) has no task in any change, and that `GET /calculation-types` gave the
form no list of allowed units, so the form would need its own copy of the unit
vocabulary. Akim's decision: list, for each input, the units of the vocabulary with its
dimension. Edited: the requirement "Calculation types listing" and a new scenario "Units
a form can offer"; `design.md` decision 10; task 5.2a (after 5.2) and the coverage row;
task 2.2's verify clause; one proposal bullet. The form itself stays outside this change.

| Check | Result |
|---|---|
| `openspec validate --all --strict` | 19/19 |
| `spec-reviewer`, first pass | 0 blockers, 2 major (the claim "a client can build the form from this listing alone" was not checkable; the task's verify used `POST /calculations` before task 5.2), 5 minor. Fixed: the claim narrowed to units that pass the dimension check; the task moved after 5.2 as 5.2a; unit order in the requirement and the scenario; "is not rejected with `422`"; exact lists in the verify clause |
| `spec-reviewer`, second pass | 0 blockers, 0 major, 3 minor (one fixed: task 2.2 verifies every field except `units`; two accepted: order checked on the pilot's two inputs, the vocabulary order is the one of `schemas/units.py` named in decision 10). **READY for DOR** |

## Implementation verdict (task 6.3), 2026-10-03

`tester`, on `feature/calculation-api/backend` at `2b3edc8` (tasks 2.1-6.2 done; commits
`dc2eca4`, `8ef5678`, `82fc8ac`, `0b7545e`, `2b3edc8`):

**GO.**

| Item | Result |
|---|---|
| tests | `backend/check.sh`: 612 passed, 1 skipped (the `postgres` module without its variable); `postgres` module against a hand-made `dec_app_wp8_test` on `dec-postgres`: 5/5 |
| coverage | 100% branch coverage of `app` (54 files), gate 95% |
| lint and types | `ruff`: no finding; `mypy`: no issue in 109 source files |
| latency | `POST /calculations`, pilot with a synthetic in-process source: median 3.7 ms, max 4.3 ms over 20 sequential requests after a warm-up (target: median at most 1 s) |
| spec coverage | every scenario of the delta mapped to at least one test |
| zones | the branch changes only `backend/` |
| UI/UX | N/A: the change has no UI (HTTP endpoints, storage, services only) |

No blocker, no major finding. Minor findings, closed by tests in `8ebf870` (619 passed,
coverage 100%): a validated-range bound without its engineer stops the start-up naming the
file and the value; on the real `POST /calculations`, a `422` body and its log line hold
no client value; `413 payload_too_large` with its code on every route of the assembled
application. The fourth minor (tasks unticked on `develop`) is closed by this record's
commit.

Task 6.2 (manual run, recorded in the code journal): `uvicorn` on `127.0.0.1` with a
migrated `dec_app_wp8_test` answered `/health`, `/docs` and `GET /calculation-types` with
`200`, and `POST /calculations` for the pilot with `503 parameter_source_unavailable`;
with `dec-postgres` stopped, `GET /calculations/{result_id}` answered
`503 database_unavailable` and recovered after the restart without restarting `uvicorn`;
the log held no URL or password.

Open: task 6.4 (review by the orchestrator, then the merge after
`feature/calculation-engine/backend` and `feature/report-generator/backend`) and task 6.5
(sync and archive after `calculation-core-contract`).

## Docstring pass and GO reconfirmed (2026-10-03)

`cc70f7d` translated 160 docstrings (module, class, function and attribute docstrings) in
39 files under `backend/app` and `backend/tests` into Russian, Google style, under Akim's
local rule; section keywords (`Args:`, `Returns:`, `Raises:`, `Attributes:`, `Yields:`)
stay English. It is on this branch because `calculation-engine` ⊂ `report-generator` ⊂
`calculation-api`: the lower branches merge into `develop` with their English
docstrings, and this branch's merge brings the translation for all three.

`tester` on `cc70f7d`: **GO**, no finding.

| Item | Result |
|---|---|
| docstrings only | AST of all 39 changed files compared with every string expression replaced by `pass`: 0 differences; no comment line edited |
| tests | `backend/check.sh`: 619 passed, 1 skipped; `postgres` module: 5/5, median 3.6 ms |
| coverage | 100% branch coverage of `app` |
| lint and types | `ruff` and `mypy`: no finding |
| docstring content | every `Args:` entry of 65 functions names a real parameter; `Attributes:` match the fields; norm citations, `design.md` decisions and requirement names kept |
| UI/UX | N/A: no UI |
