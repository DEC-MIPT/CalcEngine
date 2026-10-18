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

## Spec pass of 2026-10-18 (tasks 8.4, section 10)

The implementation had run ahead of the spec in 13 places. Akim chose to edit each requirement in
the change that holds it (`frontend-app`, and directly in `calculation-core-contract` and
`calculation-api`, both unarchived) and to describe the temporary simplifications of the pilot's
first iteration as full behaviour plus five named settings (`frontend-app` design.md, decision 12:
the first iteration lasts while the pilot is shown only inside the team). Sections 3-7 and 9 were
ticked with their commits, section 10 records the work done outside the earlier tasks, and task
10.13 (the two settings added during this pass) stays open until its commit.

- `openspec validate --all --strict`: 20/20.
- `spec-reviewer` pass 4: blocker 0, major 6, minor 10 (an outdated `calculation-api` scenario on
  the accountability block; no named decision and exit criterion for the first iteration; the
  table-step text and the rounding of `R` against the change's "engine unchanged" statements; no
  engineer named for that rounding; scenarios tied to no testable state, with two simplifications
  not behind a setting; a stale DOR record), all fixed.
- `spec-reviewer` pass 5: blocker 0, major 1 (this DOR record, closed by it), minor 6, fixed or
  answered: turning the settings back on is Akim's step before the first outside showing, stated in
  the DOD and deliberately not a GO or archive condition.
- `norm-traceability-checker`: no requirement fixes a norm formula, coefficient or limit. Fixed
  after it: the whole-degree rule of `phi_II` now names СП 22.13330.2016 table 5.5 (`unverified`,
  design decision 6); the "unrounded check" display rule is recorded as Akim's with its reason
  (decision 13); the example values of the rounding scenarios are marked illustrative. Unchanged
  and already marked `unverified`: GOST R 21.101-2026 for the report layout and dates, the unit
  designations; the XML 1.0 character rule is a format rule, not a norm.

## Task 8.2, first round (2026-10-18)

**`ui-ux-tester`: CONFIRMED** on `feature/frontend-app/frontend` at `b538708`, mock server, Chromium,
1280, 375 and 320 px, reduced motion on and off. axe (WCAG 2.0-2.2 A/AA and best practice,
including contrast and target size): 0 violations on every screen and state. The keyboard journey
to the downloaded report works at both widths with a visible 2 px focus ring on all 38 stops;
meaning is never carried by colour alone; the visual brief of design decision 5 and the
first-iteration state of decision 12 hold. Two moderate defects, both WCAG level A, fixed in
`74a1ee4`: the page title was "frontend" (2.4.2; now the app title, following the interface
language, and `index.html` says `lang="ru"`), and the signatory fields had no visible caption below
the `sm` breakpoint (3.3.2; now «Фамилия» and «Дата» above each field). Cosmetic, left as they are:
an empty trace ruler on a refusal, a taller header on the report screen in mock mode (the demo badge
wraps), and the signature-block checkbox announced as a switch.

**`tester`: NO-GO for both features.** All automated runs passed: `backend/check.sh` on both tips
(959 passed, coverage 100%), `pre-commit run --all-files`, `frontend/check.sh` (462 passed, branches
100%), the coverage gate of 8.1, Playwright in Chromium (34 passed) and `formulas.spec.ts` in Firefox
and WebKit. Blocking: no test of task 10.11 set `TRACE_NORM_STATUS` on (added in `4a04cca`:
`backend/check.sh` 960 passed, coverage 100%); tasks 8.1 and 8.3 were not ticked (8.1 had its note
but no tick; both ticked now); task 8.8 (branded Edge and Safari by hand) is open and needs a person.
Not blocking: the 2.4 note now records that `9f18cf4` re-recorded the fixture's `input_hash`
values; `npm audit --omit=dev` reports `@xmldom/xmldom` (high) through `mathjax-full`, not reachable
from the app's imports, and `source-map-js` (build time, already on `develop`); `vite.config.ts` has
no `coverage.include`; the `postgres`-marked tests were not run.

Next: a second `tester` round for the backend feature at `4a04cca`; the frontend feature gets its
GO after task 8.8.
