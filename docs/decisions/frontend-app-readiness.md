# `frontend-app`: readiness record, 2026-10-06

- Date: 2026-10-06
- Change: `openspec/changes/frontend-app/` (owner Akim, frontend and backend zones; no
  WP number).
- Reviewer: `spec-reviewer` subagent, run by Akim for task 1.2.

Russian version: `frontend-app-readiness-rus.md`.

## Verdict

**READY for DOR.** `openspec validate --all --strict` passes (20/20). The third
`spec-reviewer` pass lists no blocker and no major finding; its five minors are fixed.
`norm-traceability-checker` passes (task 1.3). The re-read against `retarget-mvp-domain` (task
1.4) found no contradiction, and Akim confirmed on 2026-10-06 that each task fits one session.

## `spec-reviewer`

| Pass | Blocker | Major | Minor | Verdict |
|---|---|---|---|---|
| 1 | 0 | 6 | 8 | NOT READY |
| 2 | 0 | 1 | 8 | NOT READY |
| 3 | 0 | 0 | 5 | READY (spec-reviewer criterion) |

Pass 1 majors, closed: a refused result's report downloads normally (and the `409` case was
added); the whole-values rule is checked in the base unit and the unit is fixed to it; the 1 s
transition time is defined (p95, 20 runs, Chromium, mocks) and has a task; keyboard, contrast
and branded Edge and Safari have Playwright or manual tasks; the safe-handling and coverage rules
are a requirement of their own; the C/C++ boundary line is in `design.md`. Its minors included
splitting the large tasks and moving a document edit out of a code task.

Pass 2 major, closed: task 8.5 runs axe over the four screens and their states. Its minors
(task numbering, coverage-table rows, language check, fixture for task 2.4, report `422`
mapping, `Content-Disposition` on a cross-origin request, task order) are fixed. The
`Content-Disposition` header is already exposed by `backend/app/main.py`, so no change to
`calculation-api` was needed.

Pass 3 minors, fixed without a fourth pass: a stale task number in 3.8; the `422` example of
task 7.2 now uses `title.designation`, and a `["body"]` entry is shown above the form (the
signatory rule of `ReportRequest` is reported by Pydantic with `["body"]` only, so the
`<role>` mapping is defensive); the collapsed-header check in 6.3; a failing-threshold check in
8.1; both missing and empty `label.ru` and `symbol` in 2.1.

## `norm-traceability-checker`

Passes: no requirement or scenario fixes a formula, coefficient, limit, tolerance or rounding rule
(0 calculation requirements). Classified as UI or test criteria, not norm values: the whole-values
rule of `phi_II`, the WCAG contrast figures, the 1 s and 95% thresholds, and the metadata
(`label`, `symbol`, `hint`, `whole_values_only`). One mention is `UNVERIFIED`: GOST R 21.101 in
`design.md`, a visual reference only; it now says "edition unverified" and points to
`calculation-core-contract`, and the report screen requirement points to that change for the
source of the signatory rules. Seen in the repository, not caused here: GOST R 21.101-2020 in
the base `report-generator` spec against 21.101-2026 in `calculation-core-contract` (noted there).

## Re-read against `retarget-mvp-domain` and the base specs (task 1.4)

Done 2026-10-06 on `develop` (no new commit on `origin/develop`). Compared: `retarget-mvp-domain`
`specs/web-platform/spec.md`, the base `web-platform` "Non-functional — integration and
latency", and the `calculation-api` "Calculation types listing".

- "Calculation input form" (WP1): `frontend-app` does not edit it. The new "Input form built from
  the type's contract" repeats on purpose its two rules, fields from the type's contract and no
  hard-coded fields (with the "different type" scenario), and refines them: the source is the
  entry of `GET /calculation-types`, and the client checks are required, finite, whole. No
  contradiction: WP1's "validated against that type's contract" is met by those checks and the
  server's `422`; `frontend-app` adds that range limits stay with the backend, which WP1 does not
  contradict. If WP1 changes that requirement again, the two must be re-read.
- "Single authorization" (WP1): not touched; authorization is a Non-goal here.
- Base "Non-functional — integration and latency": stays. Its subject is the transition
  between components; the new transition-time clause measures screen changes in the frontend
  (p95 under 1 s, Chromium, mocks). A refinement, not a conflict.
- `calculation-api` "Calculation types listing": the new requirement adds `label`, `symbol`,
  `hint`, `whole_values_only` "in addition to" the listed fields, so the listing's own list of
  fields stays true. Task 2.3 changes `InputView` and `OutputView` (`extra="forbid"` today) for it.
