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

## Task 8.2, second round (2026-10-18)

**`tester`: GO for the backend feature** `feature/frontend-app/backend` at `4a04cca`. In a worktree of
that tip: `backend/check.sh` exit 0 (ruff clean; mypy "no issues found in 137 source files";
lint-imports "4 kept, 0 broken"; 960 passed, 4 skipped (the `postgres` tests, no test database
variable); coverage 100%, 2308 statements, 454 branches) and `pre-commit run --all-files` passed.
The new test of task 10.11 was checked by breaking the code three times: the trace status forced off
fails it, the status forced on fails the existing off-state test, and a broken "verified" label fails
it. Every verify clause of section 2 and of tasks 10.7, 10.8, 10.11 and 10.12 is backed by a test.
Not re-run this round: the `postgres` module (the only commit since round one adds a unit test and
touches no migration or repository) and the manual Word render of 10.11 (recorded in the code
journal).

The frontend feature stays NO-GO until task 8.8 (branded Edge and Safari by hand). Next for the
backend feature: the review (AGENTS.md section 2, step 7).

## `orchestrator` review of the backend feature (2026-10-18)

Three rounds on `feature/frontend-app/backend`; the fixes are task 10.14, commit `dd3870f`.

- Round 1 at `4a04cca`: CHANGES REQUESTED, blocker 0, major 1, minor 7. M1: a step whose LaTeX
  could not be converted to a Word equation made every report of that stored result fail with
  `500`; the impact is denial of the report, not injection (`mathml2omml` escapes what it writes,
  `parse_xml` resolves no entities). Minor: `mathml2omml` unmaintained and printing to stdout;
  rounding looked up by the substitution's symbol; degrees printed as U+2218; a validator message;
  a missing `Args:`; the `paragraph._p` dependency; unpushed branches.
- Round 2: CHANGES REQUESTED. M1 and m3-m6 closed, m2 accepted as an assumption recorded in design
  decision 13. New N1 (major): the `redirect_stdout` fix of m1 swapped the process-wide `sys.stdout`
  and raced across request threads. N2: the plain-text fallback failed on characters XML 1.0 does
  not allow. N3: a wording slip.
- Round 3: **APPROVED.** N1 closed by replacing the module `print` of `mathml2omml` once at import;
  N2 by replacing such characters with U+FFFD; N3 reworded. `backend/check.sh`: 971 passed, coverage
  100%; `openspec validate --all --strict` 20/20. Left to Akim: pushing the branch and the local
  `develop` commits before the merge (m7), and a short `tester` confirmation of GO on `dd3870f`.

## Task 8.2, backend GO confirmed at `dd3870f` (2026-10-18)

**`tester`: GO for the backend feature** at `dd3870f`, the only commit after the second-round GO at
`4a04cca` (task 10.14, the `orchestrator` fixes). `backend/check.sh` exit 0: ruff clean, mypy "no
issues found in 137 source files", lint-imports "4 kept, 0 broken", 971 passed, 4 skipped (the
`postgres` tests), coverage 100% (2325 statements, 454 branches; every changed module at 100%);
`pre-commit run --all-files` passed. Each item of task 10.14's verify clause and the scenario "A
formula that cannot be converted" are backed by tests; the stdout test fails if the builtin
`print` of `mathml2omml` is restored. UI/UX: N/A for the backend feature. With the `orchestrator`
approval, the backend feature is ready to merge into `develop`.

## Task 8.2, frontend feature final round (2026-10-19)

**`tester`: GO for the frontend feature** `feature/frontend-app/frontend` at `c3c37c4`: the
round-one tip `b538708` plus `74a1ee4` (the two `ui-ux-tester` fixes), the backend feature's
`4a04cca` and `dd3870f`, and the merges `2a4489e` and `c3c37c4`. `frontend/check.sh` exit 0
(`gen:api:check`, eslint and `tsc -b` clean; 463 passed in 45 files; branch coverage 100%, 605/605;
statements 99.87%). `backend/check.sh` exit 0: ruff clean, mypy "no issues found in 137 source
files", lint-imports "4 kept, 0 broken", 971 passed, 4 skipped (the `postgres` tests); coverage 100%
(2325 statements, 454 branches). `pre-commit run --all-files` passed with no change to
`.secrets.baseline`. Playwright against its own mock server: Chromium 34 passed; `formulas.spec.ts`
passed in Firefox and in WebKit.

Task 8.8 was done by hand by Akim on 2026-10-19: branded Edge 155.0.4283.62 and Safari 26.5.2 typeset
every formula of a result with a trace and the journey completes; its tick is committed with this
record. Every frontend-feature task is done except the post-merge spec tasks 8.10 and 8.11.

UI/UX: the round-one confirmation stands. The backend commits change no screen; `74a1ee4` was checked
at 375, 320 and 1280 px (the title, `lang="ru"`, the signatory captions visible only below `sm`, no
overflow, 0 axe violations).

Not blocking: the round-one notes on `npm audit` and `coverage.include` stay; a
`StarletteDeprecationWarning` from the test client; the `postgres` tests were not run.

Next: the review (AGENTS.md section 2, step 7) and the merge into `develop`, then tasks 8.10 and
8.11. The branch is pushed at `c3c37c4`.

## `orchestrator` review of the frontend feature (2026-10-19)

Two rounds on `feature/frontend-app/frontend`; the fixes are task 10.15, commits `1e701c0` and
`8fc6d40`.

- Round 1 at `c3c37c4`: CHANGES REQUESTED, blocker 0, major 1, minor 7. Scope: the diff over
  `origin/develop`, which is `frontend/` plus one `.secrets.baseline` entry (`69c7b8a`, the MSW
  worker's integrity checksum, a false positive reviewed by hand on the feature branch, AGENTS.md
  section 2). `frontend/check.sh` exit 0 (463 passed, branches 100%); `git merge-tree` against
  `origin/develop` has no conflict. Verified: the production build holds no mock code; no
  `dangerouslySetInnerHTML`; `rounding.ts` matches `RoundingRule.apply` on 2.675, 2.665, -2.5,
  1e-7, 1.5e21 and -0.004; `@xmldom/xmldom` comes only through `mathjax-full` →
  `speech-rule-engine`, and the bundle contains no code from either.
  - M1 (major): the base TeX package keeps `\mmlToken`, whose `href` and `style` attributes
    reached the SVG output: `\mmlToken{mi}[href="javascript:alert(1)"]{x}` yielded
    `<a href="javascript:alert(1)">`, against "Hostile symbol" and design decision 1.
  - Minor: m1 a malformed `result_id` (`422` on `["path","result_id"]`) showed a retry, not "not
    found"; m2 Playwright could reuse a non-mock server on 5173; m3 `mockServiceWorker.js` shipped
    in `dist/`; m4 the `127.0.0.1:8000` fallback was built into production; m5 `fileNameFrom`
    decoded a plain `filename=` and could throw, and the object URL was revoked at once; m6 no
    focus move after a server `422`, and `disabled` on the calculate button dropped focus; m7 only
    a click on the trace ended the playback, while the requirement says "a pointer click". Nit:
    the Tailwind packages were in `dependencies`.
- Round 2 at `1e701c0`: **APPROVED.** M1 closed by the MathJax `SafeHandler` (URLs, classes, CSS
  ids and styles `none`), with tests that the `\mmlToken` link, style, class and id payloads
  typeset with none of them; m1 by treating a `422` whose every field is `path.result_id` as not
  found; m2 by port 5179 without server reuse; m3 by a build plugin that removes
  `mockServiceWorker.js` from a non-mock `dist/` (checked in both modes); m4 by the
  development-only fallback to `127.0.0.1:8000` (same origin otherwise); m5 by decoding only
  `filename*`, with a fallback, and revoking the object URL after 40 s; m6 by focusing the first
  field marked by a `422` and `aria-disabled` on the calculate button (one request, focus kept);
  m7 by a `document` click listener inside `useTracePlayback`. The Tailwind packages moved to
  `devDependencies` (the lockfile gains six optional `oxide-wasm32-wasi` entries); `npm audit
  --omit=dev` no longer reports `source-map-js`. `frontend/check.sh`: 476 passed, branches 100%
  (616/616). Not blocking: `download.test.ts` turned fake timers off inside the test body.
- After round 2, `8fc6d40` changes two test files only: cases `href="https://example.com"` and
  `style="color:red"`, which fail without the strict safe options, and `vi.useRealTimers()` moved
  into `afterEach`.

## Task 8.2, frontend feature confirmed at `8fc6d40` (2026-10-19)

**`tester`: GO for the frontend feature** at `8fc6d40`. Since the final-round GO at `c3c37c4` there
are two commits: `1e701c0` (task 10.15, the `orchestrator` review fixes, `frontend/` only) and
`8fc6d40` (two test files).

At `1e701c0`: Playwright on its own server at port 5179, Chromium 34 passed and `formulas.spec.ts`
passed in Firefox and WebKit; a production build has no `mockServiceWorker.js` and no
`127.0.0.1:8000`; each fix was broken by hand, and M1, m1, m4, m5, m6 (both focus moves and
`aria-disabled`) and m7 each fail at least one test.

At `8fc6d40`: `frontend/check.sh` exit 0, 478 passed, branch coverage 100% (616/616);
`pre-commit run --all-files` passed. With `safeOptions` removed from `typeset.ts`, three cases fail:
MathJax's default safe filter keeps an `https` link, `color: red`, and the `background:red` of the
`position:fixed` case as `background-color: red` (it drops `position` and `inset`). So the stricter
options of M1 are covered by tests.

UI/UX: the round-one confirmation stands. The `aria-disabled` styles copy the `disabled` ones, and
the axe and keyboard e2e tests pass.

Not blocking: `vite.config.ts` is outside coverage; a production build checks its plugin instead.

Next: the merge into `develop` (the `orchestrator` review is approved, section above), then tasks
8.10 and 8.11.

## `fix/frontend-app/frontend`: frontend README (2026-10-19)

**`tester`: GO for `fix/frontend-app/frontend`** at `6cc8baa`. Its one commit changes only
`frontend/README.md`: the mocks section (the four envelopes and how they are picked, their ids, the
`report.docx` stub, the `503` note, `mockServiceWorker.js` dropped outside mock mode), the `dev` and
`test:e2e` rows, and the source layout. `frontend/check.sh` exit 0: 478 passed, branch coverage 100%
(616/616). Every factual claim in the new text was checked against the code at that tip and holds.
UI/UX and Playwright: N/A, because no executable file changed. Review: Akim confirmed the diff
(no executable change, so no `orchestrator` round). Not blocking: an unchanged sentence says
`fixtures.ts` was generated from the backend; the refused and warning envelopes were added later
(`cd73b2f`, tasks 6.4a-6.4c) and their origin is not stated.

## Synchronization readiness after core and API archives (2026-11-09)

Only task 8.11 remains open. The required core and API archives exist, committed
at 1c4f829 and fd41cd6. Source proposal/design/deltas are unchanged since frontend
integration c252375. Read-only closure review verified exact-tip integrations:
backend dd3870f is the second parent of 57abe06 and frontend 8fc6d40 is the second
parent of c252375; both merges are ancestors of current develop.

Existing backend tester GO records 971 passed, 4 PostgreSQL skips and 100% branch
coverage. Existing final frontend GO records 478 tests and 100% branch coverage.
The UI/UX confirmation at b538708, subsequent fixes checked at 320/375/1280 px
with zero axe violations, and the confirmation retained at 8fc6d40 remain
recorded. Akim's manual Edge/Safari acceptance is recorded in task 8.8. Later
interim UI changes have their own acceptance records; current frontend code is
not claimed byte-identical to 8fc6d40. This is no new tester GO or browser run.

The three-main-spec preview adds sixteen requirements and modifies Expandable
steps. Existing Purposes, untouched requirements, all original scenarios and
the interim-source labels are preserved. The spec-reviewer reports 0 blockers,
0 major and 0 minor findings and readiness for the synchronization/archive choice.
Selected strict validation passed; all actual specs/active changes passed 21/21;
the isolated main-spec tree with candidates passed 15/15. The existing unrelated
formula-extractor-fix archive-target information remains informational.

Task 8.11 stays open pending the workflow choice. No frontend source artifacts,
main specs or archive were changed. No application, database or browser checks
were rerun. Activation of pilot settings before an external demonstration remains
the separate accepted follow-up, not an archive gate. The preceding verification
sync/archive remains uncommitted and was preserved. No commit, merge or push
was performed for this assessment.

## Main specs synchronized and change archived (2026-11-09)

Akim explicitly authorized synchronization and archive in the user conversation.
Three canonical specs now match their reviewed preview SHA-256 values: calculation-api,
transparent-output and web-platform. All sixteen ADDED requirements and the one
MODIFIED requirement were compared with the active deltas before moving the change.
Existing Purposes, unaffected requirements/scenarios and interim-source labels remain
preserved. The fetched specs instruction snapshot was reused without another lookup.

Selected strict validation passed before archive; actual main specs passed 15/15.
The entire directory, including .openspec.yaml, was moved to
`openspec/changes/archive/2026-11-09-frontend-app/`. All strict validation after
archive passed 20/20. Task 8.11 is complete; no task checkbox remains open. The
count decreases by one because an active change was archived without adding a new
main capability. The unrelated formula-extractor-fix archive-target information remains.

Existing feature GO/review/integration and UI/UX acceptance records cited above
remain the closure basis. No new tester GO, application tests, database or browser
checks are claimed for this documentation-only operation. Pilot-setting activation
before external demonstration remains the accepted follow-up. The preceding
verification synchronization/archive is preserved and also remains uncommitted.
No commit, merge or push was performed. The next loads-contract work is reconciliation
against the synchronized canonical specs and a current DOR review; archive completion
alone does not declare the new calculation ready or verified.
