# Tasks

Owner: Akim (frontend and backend zones). No WP number: the change was found when the frontend
became ready for coding.

Branches: two features (`AGENTS.md`, Branching rules).

- `feature/frontend-app/backend` (Akim, from `develop`): section 2, the metadata of the
  contract, and the backend tasks of section 10. Section 2 does not depend on the frontend.
- `feature/frontend-app/frontend` (Akim): sections 3-7, 9 and the frontend parts of 8 and 10. It branches
  from `feature/frontend-app/backend` once section 2 is done there (its `openapi.json` carries the
  metadata) and merges into `develop` after it, and only when every code task is checked off, the
  `tester` has declared GO for the feature and the review has passed.

Spec work (section 1) is committed directly to `develop`. Checkboxes are ticked in `develop` as each
subtask is done on its feature branch. Every task with code is on exactly one branch, named in its
last parentheses.

Code journal: `docs/akim/reports/frontend-app-code-journal.md` (untracked, Akim's zone), created
before task 2.1.

## 1. Spec readiness

- [x] 1.1 (spec) Run `openspec validate frontend-app --strict` and
  `openspec validate --all --strict`; verify: both pass (2026-10-06, 20/20; re-run after the review fixes; again 2026-10-18 after the spec pass of section 10, 20/20)
- [x] 1.2 (spec) Run `spec-reviewer` on this change until a report on the current version lists no
  blocker and no major finding; record the passes in
  `docs/decisions/frontend-app-readiness.md` (2026-10-06, pass 3; 2026-10-18, passes 4 and 5 on
  the spec pass of section 10: pass 4 blocker 0, major 6, minor 10, all fixed; pass 5 blocker 0,
  its one major being this record, minors fixed)
- [x] 1.3 (spec) Run `norm-traceability-checker`; verify: it confirms that no requirement of this
  change fixes a formula, coefficient or limit (the metadata of section 2 is not a norm value)
  (2026-10-06: confirmed, no calculation requirement; 2026-10-18: confirmed again, with the
  whole-degree rule of `phi_II` now sourced and the display rounding rules recorded as Akim's,
  `design.md` decisions 6 and 13; `docs/decisions/frontend-app-readiness.md`)
- [x] 1.4 (spec) Re-read `retarget-mvp-domain` `specs/web-platform/spec.md`, the base
  `web-platform` requirement "Non-functional — integration and latency" and the `calculation-api`
  types-listing requirement; verify: the requirements added here refine them on purpose (the
  input-form requirement repeats "no hard-coded fields" and the different-type scenario for the
  contract-driven part; the transition-time clause refines the base latency requirement) and
  contradict none; record the result in the readiness file (2026-10-06: done, no contradiction;
  `docs/decisions/frontend-app-readiness.md`)

## 2. Backend: input and output metadata (feature `frontend-app/backend`)

- [x] 2.1 Add `label`, `symbol`, `hint` and `whole_values_only` to the quantity declaration
  (`QuantityDeclaration`, `backend/app/schemas/calculation.py`) with the shape of `design.md`
  decision 6, and reject at registration a type whose input or output has no `label.ru` or no
  `symbol` (backend); verify: tests that a declaration with a missing or empty `label.ru`, or with a
  missing or empty `symbol`, fails and names the quantity, and that `hint` and `label.en` are
  optional (done 2026-10-06 on `feature/frontend-app/backend`, `bab155f`)
- [x] 2.2 Declare the metadata for the inputs and outputs of `foundations_shallow_r`
  (`backend/app/engine/foundations_shallow_r.py`), with `whole_values_only` true for `phi_II` and
  false for the others (backend); verify: a test reads every quantity of the pilot and finds
  `label.ru` and `symbol`; no value, formula, `NormRef` or parameter of the pilot changes (done 2026-10-06 on `feature/frontend-app/backend`, `bab155f`)
- [x] 2.3 Carry the metadata to `GET /calculation-types` through `InputView` and `OutputView`
  (`backend/app/schemas/api.py`) and the OpenAPI schema (backend); verify: a test of the endpoint
  finds the fields in the declared order, `phi_II` with `whole_values_only` true; `/openapi.json`
  documents them (done 2026-10-06 on `feature/frontend-app/backend`, `bab155f`)
- [x] 2.4 Prove that the metadata changes no calculation (backend); verify: a test that the result
  envelope, the trace, the `NormRef` list and `input_hash` of a fixed request equal the values
  in a fixture `backend/tests/fixtures/pilot_envelope_before_metadata.json`, generated on `develop`
  and committed as the first commit of the branch, before task 2.1; no file under `ml/` or `infra/` and no query to `dec_normatives`
  is added (done 2026-10-06 on `feature/frontend-app/backend`: the fixture in `b8f14c4`, the test in
  `bab155f`; the baseline got three entries for the fixture's hashes by hand, not a full regeneration;
  the merge of `develop` in `9f18cf4` re-recorded the fixture's `input_hash` values, because the
  WP9 table selectors entered the resolved parameters, and the `tester` confirmed on 2026-10-18 that
  the code of `develop` at `380e42d` gives the same hashes; task 10.7 regenerated the fixture's
  table-step expression strings in `ed6f672`, with no value, `NormRef` or `input_hash` changed)
- [x] 2.5 Run `backend/check.sh` and the `postgres` module (backend); verify: `ruff`, `mypy`,
  `lint-imports` pass, branch coverage of `app` stays 100%, and the `pre-commit` hooks pass (done 2026-10-06 on `feature/frontend-app/backend`, `bab155f`)

## 3. Technical foundations (feature `frontend-app/frontend`)

- [x] 3.1 Add `openapi-typescript`, the script `npm run gen:api`, the committed
  `frontend/src/api/schema.d.ts`, and a check in `check.sh` that the committed file is current
  (frontend); verify: regenerating from the backend of section 2 leaves no diff; a hand edit of the
  file makes the check fail (done 2026-10-06 on `feature/frontend-app/frontend`, `b0ce766`)
- [x] 3.2 Add the API client over `openapi-fetch` with the base address from
  `VITE_API_BASE_URL`, and a helper that turns an error body (`code`, `message`, `fields`) into a
  typed value (frontend); verify: Vitest tests for a `422` body with `fields`, a `404`, a `503`, and a
  network failure (done 2026-10-06 on `feature/frontend-app/frontend`, `8e1c690`)
- [x] 3.3a Add MSW with one set of handlers shared by the browser and Vitest, and the script
  `npm run dev:mock` (frontend); verify: `npm run dev:mock` answers `GET /calculation-types`
  from the handlers, and the Vitest setup uses the same handler module (done 2026-10-06 on `feature/frontend-app/frontend`, `69c7b8a`)
- [x] 3.3b Add the scenario handlers of `design.md` decision 4: pass, fail, refused, warning,
  `422`, `503`, typed by the generated schema (frontend); verify: one test per scenario reads
  the response through the client of 3.2 and gets the expected typed value (done 2026-10-07 on `feature/frontend-app/frontend`: pass, fail, `422` and `503` in `69c7b8a`, refused and warning in `cd73b2f`)
- [x] 3.4 Add React Router with the four addresses of "User journey and screens" and empty screens
  (frontend); verify: a test per address renders its screen; an unknown address renders a "not
  found" screen (done 2026-10-06 on `feature/frontend-app/frontend`, `fa41aa0`)
- [x] 3.5 Add the typed `ru`/`en` dictionary with the fallback to `ru`, the language switch, and
  number formatting through `Intl.NumberFormat` (frontend); verify: tests that a missing `en` key
  shows the `ru` text, and that `172.5` shows as `172,5` in Russian and `172.5` in English (done 2026-10-06 on `feature/frontend-app/frontend`, `c1bfaa3`; the switch is not rendered in the pilot's first iteration, task 10.1)
- [x] 3.6 Add `eslint-plugin-jsx-a11y` and an axe helper for component tests (frontend); verify:
  `check.sh` runs both; a test component with an unlabelled input fails the axe helper (done 2026-10-06 on `feature/frontend-app/frontend`, `c1bfaa3`)
- [x] 3.7 Add the `Formula` component on MathJax with the raw-text fallback and the restricted
  extensions of `design.md` decision 1 (frontend); verify: tests that a valid LaTeX string is
  typeset, that an invalid one shows its raw text, that neither throws, and that
  `\href{javascript:alert(1)}{x}` and a `\require` string create no link and run no script (done 2026-10-06 on `feature/frontend-app/frontend`, `08a5c4f`)
- [x] 3.8 Add Playwright with Chromium, Firefox and WebKit, used by the cross-browser scenario here and by tasks 8.6, 8.7, 8.9
  (frontend); verify: one test opens a mocked result with a trace and finds every step's formula
  typeset in each of the three engines (done 2026-10-06 on `feature/frontend-app/frontend`, `9512ec1`)

## 4. Screens and navigation (feature `frontend-app/frontend`)

- [x] 4.1 Build the page shell (title, language switch, link to type selection) and the shared
  states: loading, error with `code` and `message` and a retry, and not found (frontend); verify:
  tests for each state, with the retry repeating the same request (done 2026-10-06 on `feature/frontend-app/frontend`, `265b873`; the shell renders no language switch, task 10.1)
- [x] 4.2 Build the type selection screen from `GET /calculation-types` (frontend); verify: tests
  with two types, with an empty list, and with a `503`; choosing a type opens the form address (done 2026-10-06 on `feature/frontend-app/frontend`, `265b873`)
- [x] 4.3 Wire the submit of the form to `POST /calculations` and the open of the stored result
  by its address, including a reload (frontend); verify: tests that a submit opens
  `/calculations/<id>` and that opening the address alone reads `GET /calculations/{result_id}`
  and runs no calculation; an unknown id shows "not found" (done 2026-10-06 on `feature/frontend-app/frontend`, `8f37b08`)
- [x] 4.4 Wire the link from the result to the report screen (frontend); verify: a test follows
  the link and lands on `/calculations/<id>/report` of the same id (done 2026-10-06 on `feature/frontend-app/frontend`, `8f37b08`)

- [x] 4.5 Keep entered values, response bodies and stack traces out of the console and off the
  screens (frontend); verify: a test spies on `console` during a `422`, a `404`, a `503` and a
  network failure and finds no entered value, no response body and no stack trace (done 2026-10-06 on `feature/frontend-app/frontend`, `8f37b08`)

## 5. Input form (feature `frontend-app/frontend`)

- [x] 5.1a Build the form fields from one type's entry: order, `label`, `symbol` as formula,
  `hint`, language of the texts (frontend); verify: a test with two synthetic types shows different
  fields with the same component and no type name in the form code; with the interface in English
  the `label.en` and `hint.en` of the listing are shown, and `label.ru` is shown for a quantity
  that has no `en` text (done 2026-10-06 on `feature/frontend-app/frontend`, `e852137`)
- [x] 5.1b Build the unit choice: limited to the input's `units`, preset to `base_unit`, and fixed
  to `base_unit` for an input with `whole_values_only` (frontend); verify: tests that `phi_II`
  offers `deg` only while `b` offers every listed unit (done 2026-10-06 on `feature/frontend-app/frontend`, `e852137`)
- [x] 5.2 Add the client checks: filled, finite number, whole number for `whole_values_only`
  in the base unit, with no rounding or change of the entered value (frontend); verify: tests for
  empty, `abc`, `1e999`, `30.5` on a whole-values input (value kept, message names the rule, no
  request sent), and `30`, `30.0`, `30e0` accepted (done 2026-10-06 on `feature/frontend-app/frontend`, `e852137`; the decimal comma is task 10.2)
- [x] 5.3 Show a server `422`: each entry whose `location` ends with a declared input name marks
  that field, others show above the form, entered values are kept (frontend); verify: tests with
  a body that names one field, two fields, and no field (done 2026-10-06 on `feature/frontend-app/frontend`, `e852137`)
- [x] 5.4 Show that a value outside the method's range is accepted by the form and decided by the
  backend (frontend); verify: with the warning and the refused mocks of 3.3b, the form sends the
  request and the result screen shows the outcome; the form code holds no limit (done 2026-10-07 on `feature/frontend-app/frontend`: in part in `e852137`, the warning and refused mocks in `cd73b2f`)

## 6. Result display (feature `frontend-app/frontend`; from `calculation-core-contract` 3.4, 3.5, 5.4)

- [x] 6.1a (part of `calculation-core-contract` 3.4) Render the typed steps, with each `NormRef`
  shown with its status (frontend); verify: tests with the envelopes of 3.3b: every field of a step
  (expression, substitutions with units, result with unit, `norm_refs`) is shown, and an unverified
  `NormRef` is never shown as verified (done 2026-10-06 on `feature/frontend-app/frontend`, `5944519`; the status is off in the pilot's first iteration, task 10.10)
- [x] 6.1b (part of 3.4) Render, for each check step, its comparison, both values with units and
  whether it passed, in text, and the unverified-step summary (frontend); verify: tests that a check
  step says "passed" or "failed" in words with both values, and that the summary shows
  `unverified_step_count` when it is above zero and is absent at zero (done 2026-10-06 on `feature/frontend-app/frontend`, `5944519`; the summary is off in the pilot's first iteration, task 10.10)
- [x] 6.2 (is `calculation-core-contract` 3.5) Render the envelope's `outputs` with value, unit,
  `rounding_rule` and `rounding_source`, an engineer-set rule shown with the engineer and the
  rationale (frontend); verify: tests for a `NormRef` source and for an engineer-set source (done 2026-10-06 on `feature/frontend-app/frontend`, `1cde48e`; the source column was removed for the pilot's first iteration, task 10.10)
- [x] 6.3 Make steps expandable and collapsible by pointer and keyboard with `aria-expanded`, with
  expand-all and collapse-all (frontend; `transparent-output` "Expandable steps"); verify: tests for
  click, Enter, Space, the attribute, a collapsed step's header showing its result with its unit,
  and the two buttons (done 2026-10-07 on `feature/frontend-app/frontend`, `ac52775`, then
  collapsed on open; task 10.4 made steps open expanded, as the requirement now says, and its tests
  check the expanded start)
- [x] 6.4a (part of `calculation-core-contract` 5.4) Build the shared status component for a
  warning and a refusal: icon, text label and frame shape, with the meaning in text that assistive
  technology reads (frontend); verify: a test that its text is present with all styles removed,
  and an axe check; the same test is the colour-independence test for 6.4b and 6.4c (done 2026-10-07 on `feature/frontend-app/frontend`, `cd73b2f`)
- [x] 6.4b (part of 5.4) Show the refusal: the `verdict_reason` with the violated bound, the input
  value and the bound's `NormRef` list, and no result value (frontend); verify: a test with the
  refused mock finds the three items and no output value; uses 6.4a (done 2026-10-07 on `feature/frontend-app/frontend`, `cd73b2f`)
- [x] 6.4c (part of 5.4) Show the applicability warning next to the result: the input, the violated
  bound of the validated range and that bound's source, an engineer-set source shown with the engineer
  and the rationale (frontend); verify: a test with the warning mock finds the three items beside the
  outputs of 6.2; uses 6.4a (done 2026-10-07 on `feature/frontend-app/frontend`, `cd73b2f`)

## 7. Report interface (feature `frontend-app/frontend`)

- [x] 7.1a Build the title-block part of the report form and the `signature_block` switch
  (frontend); verify: tests for the required `designation`, `document_name` and `organization`, the
  optional `documentation_kind`, and the switch hiding and not sending the signatories (done 2026-10-07 on `feature/frontend-app/frontend`, `facb151`)
- [x] 7.1b Build the three signatories with the required-field rules of "Report request screen"
  (frontend); verify: tests for an empty developer date, an empty normative-control surname, and a
  checker given in part (done 2026-10-07 on `feature/frontend-app/frontend`, `facb151`)

- [x] 7.2 Download the `.docx` from `POST /calculations/{result_id}/report` under the name of the
  response's `Content-Disposition` (which the backend exposes to cross-origin pages,
  `backend/app/main.py`, `expose_headers`), and show a `422`, `404`, `409` or other error in text
  with the fields marked by the rule of `design.md` decision 7 (frontend); verify: tests with a
  mocked file response, a refused result (downloads as any other), and each error (`422` with the
  body `fields: [{location: ["body", "title", "designation"], message: "..."}]` marks the
  designation field, and an entry with `location: ["body"]`, as the backend gives for an incomplete
  signatory, is shown above the form; `404`; `409 calculation_type_not_registered`); no file is saved on an error (done 2026-10-07 on `feature/frontend-app/frontend`, `facb151`; the file is saved from the report stamp since task 10.5)

## 8. Verify and close

- [x] 8.1 Run `frontend/check.sh` (frontend); verify: `eslint`, `tsc -b` and `vitest run --coverage`
  pass with branch coverage >= 95%, and a run with the threshold of `vite.config.ts` raised above
  the measured coverage fails (done 2026-10-18 on `feature/frontend-app/frontend` at `b538708`:
  462 tests, branch coverage 100%; the branch threshold cannot be raised above 100%, so the gate was
  shown with the statements threshold raised above the measured 99.87%, which fails the run)
- [x] 8.2 `tester` GO for each feature; `ui-ux-tester` confirms the screens, keyboard operation,
  contrast, no colour-only meaning and the visual brief of `design.md` decision 5 (tester)
  (2026-10-18, first round: `ui-ux-tester` CONFIRMED, its two moderate defects fixed in `74a1ee4`;
  `tester` NO-GO for both features, for the missing test of task 10.11 (added in `4a04cca`) and the
  open tasks 8.1, 8.3 and 8.8; `docs/decisions/frontend-app-readiness.md`) (done: `tester` GO for
  the backend feature at `dd3870f` on 2026-10-18 and for the frontend feature at `c3c37c4` on
  2026-10-19, the round-one `ui-ux-tester` confirmation standing)
- [x] 8.3 Run the journey end to end against the real backend and, once WP9 is merged, a real
  catalog source: type selection, form, result, report download, with the frontend and the backend
  on different origins and `DEC_CORS_ORIGINS` set (frontend); verify: a recorded manual run in which
  the downloaded file has the name the backend gave (the `Content-Disposition` is readable
  cross-origin); until WP9 is merged the pilot's `503` is shown as in "Backend not available"
  (done 2026-10-18T19:38Z on `feature/frontend-app/frontend` at `b538708`, Chromium 153 driven by
  Playwright: frontend on `127.0.0.1:5173`, backend on `127.0.0.1:8000` with the catalog in `dec`;
  result `fc9a5f2f-9748-4fb4-a420-21e7be8e580a`, verdict `pass`, 9 steps referring to
  СП 22.13330.2016 "2016 с Изм. N 1, 2, 3, 4, 5"; the file saved as
  `dec-report-fc9a5f2f-9748-4fb4-a420-21e7be8e580a.docx`, the name of `Content-Disposition`; every
  response carried `access-control-allow-origin: http://127.0.0.1:5173` and
  `access-control-expose-headers: Location, Content-Disposition`; no console error; recorded in
  the code journal)
- [x] 8.4 (spec) After 6.1a, 6.1b, 6.2 and 6.4a-6.4c are done, tick tasks 3.4, 3.5 and 5.4 in
  `calculation-core-contract` `tasks.md` and name this change there (spec; needs Akim's word
  to edit that change) (done 2026-10-18 on `develop`, with Akim's word)
- [x] 8.5 Run the axe helper of task 3.6 over the four screens (type selection, form, result,
  report) in their states: loading, error, `422`, `503`, warning and refusal (frontend); verify:
  every run reports no violation that axe can detect in jsdom (done 2026-10-18 on
  `feature/frontend-app/frontend`, `b538708`: `frontend/src/test/screens.axe.test.tsx`, 14 tests)
- [x] 8.6 Run the keyboard journey from type selection to the downloaded report in Playwright
  (frontend); verify: the test completes it with the keyboard alone against the mocks and checks
  after each key press that the focused control has a visible indicator of at least 3:1 (done
  2026-10-18 on `feature/frontend-app/frontend`, `b538708`: `frontend/e2e/accessibility.spec.ts`;
  it found that Tab reaches the date field's own calendar button with no ring, fixed in
  `index.css` by a ring on `input[type='date']:focus-within`)
- [x] 8.7 Run an axe contrast check of every screen in Chromium (frontend); verify: no text
  below 4.5:1 (3:1 for large text), with the warning and refusal states and each interface state
  (light and dark, if both exist) in the run (done 2026-10-18 on `feature/frontend-app/frontend`,
  `b538708`: 11 screens and states, light only because the interface has no dark state; the
  `503` states are checked by 8.5, since the browser mocks cannot be overridden per test)
- [x] 8.8 Check once by hand in branded Edge and Safari that a result with a trace shows every
  formula typeset and that the journey completes (frontend); verify: a recorded manual run with the
  browser versions (done 2026-10-19 by Akim on `feature/frontend-app/frontend` at `c3c37c4`, against
  the real backend with the catalog: Edge 155.0.4283.62 and Safari 26.5.2, every formula typeset and
  the journey complete; recorded in the code journal)
- [x] 8.9 Measure the transition time of "Non-functional — language, accessibility, browsers"
  once all four screens exist (frontend); verify: a Playwright test in Chromium against the mocks
  takes 20 runs of response-to-first-render for each screen change and fails when the 95th
  percentile is 1000 ms or more (done 2026-10-18 on `feature/frontend-app/frontend`, `b538708`:
  `frontend/e2e/transition-time.spec.ts`; p95: type selection to form 11 ms, form to result 762 ms
  with the 700 ms computation trace, result by address 54 ms, report to stamp 578 ms)
- [x] 8.10 (spec) After the merge of the frontend feature, update the command lists of `AGENTS.md`
  and `CLAUDE.md` with `npm run gen:api`, `npm run dev:mock` and the Playwright command (documents,
  on `develop`; needs Akim's word to edit them) (done 2026-10-19 on `develop`, with Akim's word:
  `CLAUDE.md` "Commands that exist today" lists `npm run dev`, `npm run dev:mock`, `npm run gen:api`
  and `npm run test:e2e` with the one-time Playwright install, and its status names the merge;
  `AGENTS.md` has no command list, and its section 7 already names Vitest and Playwright, so it is
  unchanged)
- [ ] 8.11 (spec) Archive this change after both features are merged and after `calculation-api`
  and `calculation-core-contract` are archived

## 9. UX iteration (feature `frontend-app/frontend`)

From the heuristic review of 2026-10-08 and the decisions of
`docs/decisions/frontend/2026-10-08-frontend-ux-improvements-kickoff.md` (direction kept, hybrid
type, four micro-interactions, one expressive moment). Points 4, 6, 7, 8 of the review and its
P0-P2 defects are not in this section. Each task is one commit and is shown to Akim before the next.

- [x] 9.1 Scale the page heading (1.875-2.25 rem) and the verdict line (1.5-1.875 rem) with
  `clamp()` and keep the body text, labels, fields and table columns on whole-pixel steps
  (frontend); verify: a Playwright run at 1440, 1280, 1024, 768, 390 and 320 px finds no horizontal
  scroll, the right edges of the value fields and of the output values equal row by row, an integer
  computed font size in those columns, the heading at 30 px (320) and 36 px (1440), and the verdict
  line at 24 px (320) and 30 px (1440) (done 2026-10-08 on `feature/frontend-app/frontend`, `e918c89`)
- [x] 9.2a Keep the form draft per type in memory and restore it on return and on the back action
  (frontend); verify: tests that the values and units survive leaving and returning and the back
  action, and that no value reaches the console, the browser storage, the address or a screen other
  than the form's fields (the test of task 4.5 stays green, and a test reads `localStorage`,
  `sessionStorage` and the address after a send) (done 2026-10-08 on `feature/frontend-app/frontend`, `fbb9637`)
- [x] 9.2b Add "edit inputs" to the result, as the main action of a refusal, with focus and the bound
  at the input the bound names (frontend); verify: tests that the action is present after a send and
  absent for a result opened by its address and for an earlier result reached by the history after a
  newer calculation, and the refusal variant with focus in the named field, the bound in text, and
  the report link as the second action (done 2026-10-08 on `feature/frontend-app/frontend`, `fbb9637`)
- [x] 9.3 Echo the value in the base unit next to a field whose chosen unit is not the base unit,
  from a display-only table of the unit vocabulary, with a one-time flash of the field under
  `no-preference` (frontend); verify: a test that reads `backend/app/schemas/units.py` and fails
  when a factor of the table differs from the backend's or a unit of the vocabulary has none,
  tests for every unit of the mock types, no echo on the base unit, an empty field, a non-number or a
  unit with no factor, the sent request unchanged, both languages (`= 0,02 м`, `= 0.02 m`), the
  flash present under `no-preference` and absent under `reduce`, and axe (done 2026-10-08 on `feature/frontend-app/frontend`, `4922ead`)
- [x] 9.4 Move focus to the verdict once on arrival (not to a warning) and draw its frame in 120 ms
  under `prefers-reduced-motion: no-preference` (frontend); verify: tests for focus on a `pass`, a
  `fail` and a refusal and not on a warning, and a Playwright check that the animation name is set
  with `no-preference` and `none` with `reduce` (done 2026-10-08 on `feature/frontend-app/frontend`, `c4ee1ec`, `ab5889e`)
- [x] 9.5 Show the in-progress state of the form: text fields read-only and unit choices locked at
  the same text contrast, a stepped progress rule, a status message, the text after 3 and after 10
  seconds from the submit, no second request, and the fields changeable again after an error
  (frontend); verify: tests with fake timers for both messages, locked fields during the request,
  one request after two submits (the second by Enter in a field), the fields unlocked with their
  values after a `503`, a static rule under `reduce`, and axe (done 2026-10-08 on `feature/frontend-app/frontend`, `8411108`)
- [x] 9.6 Check the changed elements (frontend); verify: a Playwright pass with the keyboard shows a
  visible focus indicator of at least 3:1 on the verdict region, the "edit inputs" link, the unit
  select and value field of a form with an echo, the bound note of a refusal's field, and a
  read-only field during a request; the text pairs of the echo, the bound note, the in-progress
  message and the read-only field reach 4.5:1; and `frontend/check.sh` passes with branch coverage
  >= 95% (done 2026-10-08 on `feature/frontend-app/frontend`; the run is recorded in the code journal)

## 10. Pilot first-iteration refinements (both features)

Work Akim chose after section 9, done before its spec text; recorded here on 2026-10-18
(`design.md` decisions 5, 11-14). Each task names its feature in its last parentheses.

- [x] 10.1 Keep the interface in Russian for the pilot's first iteration: the page shell renders no
  language switch, while the `en` dictionary and the switch stay (frontend; `web-platform`
  "Non-functional — language, accessibility, browsers"); verify: a test finds no language switch
  in the shell and the switch's own tests stay green (done 2026-10-06 on
  `feature/frontend-app/frontend`, `265b873`)
- [x] 10.2 Accept a decimal comma in number fields and show unit designations from the frontend map
  of the unit vocabulary (frontend; `design.md` decision 11); verify: tests that `172,5` is sent
  as 172.5 with the field text unchanged, that each unit of the mock types shows its Russian
  designation, that English and a code outside the vocabulary keep the code, and that a
  dimensionless quantity has no designation (done 2026-10-06 on `feature/frontend-app/frontend`, `e852137`)
- [x] 10.3 Bold pass: the cobalt hero with the drawn grid on type selection, the side rule of the
  active and the invalid form row, and the computation trace across the form with the result
  opening no sooner than 700 ms after the submit (frontend; `web-platform` "Calculation in
  progress"); verify: tests with fake timers for the 700 ms minimum, an immediate open under
  reduced motion, and axe (done 2026-10-08 on `feature/frontend-app/frontend`, `105ee51`,
  `aaed3fa`, `4f23942`)
- [x] 10.4 Play the trace back on the first showing of a result, hold the stamp until the last step
  and reveal a clean `pass` expressively; open steps expanded; add the trace ruler, the stamp's link
  to the trace and the «—» of dimensionless cells (frontend; `web-platform` "Trace playback on
  first showing", `transparent-output` "Expandable steps" and "Result screen reading aids");
  verify: unit tests of the interval and the cap, skip by click, Space, Enter, Escape and Tab,
  pending steps `inert`, no playback on a second showing or under reduced motion, and the
  Playwright scenarios `trace-playback`, `verdict-flash` and `stamp-link` (done 2026-10-10 on
  `feature/frontend-app/frontend`, `0c7b873`, `d24336d`)
- [x] 10.5 Morph the report button through idle, sending and ready, stamp the title block on
  success and save the file only from the stamp (frontend; `web-platform` "Report request
  screen"); verify: tests for the 600 ms minimum, `aria-busy`, no stamp and no file on an error,
  the save from the stamp under the response's file name, and the Playwright scenario
  `report-stamp` (done 2026-10-10 on `feature/frontend-app/frontend`, `aab257c`)
- [x] 10.6 Name trace steps and substitutions by their LaTeX symbols, with `step_id` for assistive
  technology (frontend; `transparent-output` "Trace steps named by their symbols"); verify: tests of
  the three naming rules, the fallback to `step_id` as code, a name two types declare differently,
  and the mock trace expressions matching the engine (done 2026-10-18 on
  `feature/frontend-app/frontend`, `4324b78`, `3f1af73`)
- [x] 10.7 Write the selecting input of a table step by its LaTeX symbol in the trace (backend;
  `design.md` decision 13); verify: a test that the pilot's table steps name `\varphi_{II}` and
  that substitutions keep the input names; `backend/check.sh` with 100% branch coverage (done
  2026-10-18 on `feature/frontend-app/backend`, `ed6f672`)
- [x] 10.8 Round the pilot's `R` to two decimals by the engineer rule (backend;
  `backend/params/foundations_shallow_r.yaml`; engineer: Akim; rationale: hundredths of kPa for the
  pilot type until checked against the WP4 reference examples, `design.md` decision 13); verify: a
  test that the parameter file gives the rule with two decimals, half up, and an engineer and a
  rationale (done 2026-10-18 on `feature/frontend-app/backend`, `c5bbbee`)
- [x] 10.9 Show every value of an output by its rounding rule on the result screen, and a check
  unrounded when the rounded sides would read against `passed` (frontend; `transparent-output`
  "Values of an output shown by its rounding rule"); verify: tests of half up and half even, the
  step result, the substitution, both sides of a check, the stamp, and the contradicting case
  (done 2026-10-18 on `feature/frontend-app/frontend`, `70498d3`)
- [x] 10.10 Trim the result screen for the pilot's first iteration: no rounding-source column (put
  behind a setting by task 10.13), the output values held until the playback ends, and no status
  mark or unverified summary in the trace behind `SHOW_NORM_STATUS` (frontend;
  `calculation-core-contract` `transparent-output` first-iteration clauses); verify: tests for both
  states of `SHOW_NORM_STATUS`, the held outputs `inert` with the status shown, and axe (done
  2026-10-18 on `feature/frontend-app/frontend`, `f7a4bca`)
- [x] 10.11 Print every value and formula of the report body as a Word equation from LaTeX, output
  values by their rounding rule, and the step references without status behind
  `TRACE_NORM_STATUS` (backend; `calculation-core-contract` `report-generator` "Report values,
  formulas and dates" and "Automatic normative references in report"); verify: tests that read the
  equations back, left alignment, a breakable step expression only, the rounding with padded
  decimals, both states of the setting, and a render of the pilot's report in Word checked by hand
  and recorded in the code journal (done 2026-10-18 on `feature/frontend-app/backend`, `77c1892`)
- [x] 10.12 Leave the accountability section out of the report behind `ACCOUNTABILITY_SECTION` and
  close the conclusion with the engineer-responsibility statement (backend;
  `calculation-core-contract` `report-generator` "Result accountability block"); verify: tests that
  the statement is printed exactly once in both states of the setting and that the body ends with
  the conclusion while the section is off (done 2026-10-18 on `feature/frontend-app/backend`,
  `c79fe6d`)
- [x] 10.13 Put the language switch and the rounding-source column behind the settings
  `SHOW_LANGUAGE_SWITCH` and `SHOW_ROUNDING_SOURCE`, both off in the pilot's first iteration
  (frontend; `design.md` decision 12); verify: tests that the shell shows the switch only with the
  setting on and switching changes the texts, that the outputs table shows the source column only
  with the setting on (an engineer-set rule with engineer and rationale, a norm rule with its
  reference), that the result screen shows neither, and axe in both states (done 2026-10-18 on
  `feature/frontend-app/frontend`, `b538708`)
- [x] 10.14 Close the `orchestrator` review of the backend feature (2026-10-18): print a formula
  whose LaTeX cannot be converted as its LaTeX in plain text instead of failing the report; keep
  the converter's stray output out of stdout; write the degree sign as `\text{°}`; fix the output
  validator's message and the `_unbox` docstring; note the `paragraph._p` dependency (backend;
  `calculation-core-contract` `report-generator` "Report values, formulas and dates", `design.md`
  decisions 13 and 14); verify: tests that five unconvertible strings (`\frac{a}{`, `\text{a & b}`,
  `\text{x<y}`, `\text{<script>}`, 300 nested braces) raise `FormulaError`, that a single-formula
  line and a mixed line print the raw LaTeX with no equation, with characters XML 1.0 does not
  allow replaced by U+FFFD, that the pilot's report with a broken `R` expression still renders with
  that text, that MathML which makes `mathml2omml` print leaves stdout empty (its module `print`
  replaced at import, no `sys.stdout` swap), and that degrees read `20°`; `backend/check.sh` with
  100% branch coverage (done 2026-10-18 on `feature/frontend-app/backend`, `dd3870f`: 971 passed,
  coverage 100%; `orchestrator` APPROVED in its third round)
- [x] 10.15 Close the `orchestrator` review of the frontend feature (2026-10-19): typeset every
  formula through the MathJax safe handler with URLs, classes, CSS ids and styles not allowed, so
  that `\mmlToken` attributes from a server string reach no link or style (`web-platform` "Hostile
  symbol", `design.md` decision 1); show a `422` on `path.result_id` as "not found"; run
  Playwright on its own port without server reuse; keep `mockServiceWorker.js` out of a non-mock
  build and the local backend fallback out of a production build; read only `filename*` as
  percent-encoded and revoke the object URL after a delay; move focus to the first field a server
  `422` marks in both forms and keep the calculate button focusable while sending
  (`aria-disabled`); end the trace playback on a click anywhere on the page; move the Tailwind
  packages to `devDependencies` (frontend); verify: tests that the `\mmlToken` link
  (`javascript:` and `https:`), style (`position:fixed` and `color:red`), class and id payloads
  typeset with none of them and fail without the strict options, that a malformed id shows "not
  found" and other `422`s an error, that a production build has no `mockServiceWorker.js` and no
  `127.0.0.1:8000`, the file name cases, the focus moves, one request per send, and the page-wide
  skip; `frontend/check.sh` with 100% branch coverage (done 2026-10-19 on
  `feature/frontend-app/frontend`, `1e701c0` and `8fc6d40`: 478 passed, branches 100%;
  `orchestrator` APPROVED in its second round)

## Requirement coverage

| Requirement | Verified by |
|---|---|
| `web-platform` Responsive type | tasks 9.1, 9.6 |
| `web-platform` Form draft and the edit-inputs action | tasks 9.2a, 9.2b, 9.6 |
| `web-platform` Unit echo in the base unit | tasks 9.3, 9.6 |
| `web-platform` Verdict focus on arrival | tasks 9.4, 9.6 |
| `web-platform` Calculation in progress | tasks 9.5, 9.6, 10.3 |
| `web-platform` Trace playback on first showing | tasks 10.4, 10.10 |
| `web-platform` Motion follows the user's setting | tasks 9.3, 9.4, 9.5, 9.6, 10.3, 10.4, 10.5 |
| `web-platform` User journey and screens | tasks 3.4, 4.1-4.4, 6.4b, 7.2, 8.3 |
| `web-platform` Input form built from the type's contract | tasks 5.1a, 5.1b, 5.2-5.4, 6.4b, 6.4c, 10.2 |
| `web-platform` Report request screen | tasks 7.1a, 7.1b, 7.2, 8.3, 10.5 |
| `web-platform` Non-functional — language, accessibility, browsers | tasks 3.5, 3.6, 3.8, 5.1a, 8.2, 8.5-8.9, 10.1, 10.13 |
| `web-platform` Non-functional — safe handling and test coverage | tasks 3.7, 4.5, 8.1 |
| `calculation-api` Input and output metadata in the types listing | tasks 2.1-2.5 |
| `transparent-output` Expandable steps | tasks 6.3, 10.4 |
| `transparent-output` Trace steps named by their symbols | tasks 10.6, 10.7 |
| `transparent-output` Values of an output shown by its rounding rule | tasks 10.8, 10.9 |
| `transparent-output` Result screen reading aids | task 10.4 |
| `transparent-output` Trace display consumes typed steps and warnings (`calculation-core-contract`) | tasks 6.1a, 6.1b, 6.2, 6.4a-6.4c, 10.10, 10.13 |
| `transparent-output` Normative clause references (`calculation-core-contract`, first-iteration clause) | task 10.10 |
| `report-generator` Report values, formulas and dates; Automatic normative references in report (`calculation-core-contract`, first-iteration clauses) | tasks 10.11, 10.14 |
| `report-generator` GOST report structure; Result accountability block (`calculation-core-contract`, first-iteration clauses) | task 10.12 |
| `calculation-api` Report download, scenario "Download the report of a stored result" (`calculation-api`, first-iteration clause) | task 10.12 |

## DOR checklist

- [x] `proposal.md` (with "Non-goals"), `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes and a `spec-reviewer` report on the current version lists
  no blocker and no major finding (tasks 1.1, 1.2; 2026-10-06, 20/20, pass 3; 2026-10-18, 20/20,
  pass 5)
- [x] Functional requirements and scenarios recorded; each requirement is mapped to a task
  ("Requirement coverage")
- [x] Non-functional requirements recorded (`web-platform` "Non-functional — language,
  accessibility, browsers"; `design.md`, "Non-functional requirements")
- [x] Each task is small enough for one session (Akim's judgement, confirmed 2026-10-06; section 10
  records work already done, and 10.4 and 10.11 each took more than one session)
- [x] Acceptance and Go/No-Go criteria written (every task has a verify clause; section below)
- [x] Branches defined (header)
- [x] Dependencies satisfied (below): the engine, the report and `calculation-api` are merged; WP9 is
  mocked by task 3.3b and the archives are not implementation dependencies

## DOD and Go / No-Go

- GO is declared per feature by the `tester` agent, with `ui-ux-tester` confirmation (UI changed).
- Spec phase: `openspec validate --all --strict` passes; the `spec-reviewer` report lists no
  blocker and no major finding; `norm-traceability-checker` confirms that no norm value is fixed.
- Backend feature: every verify clause of section 2 and of the backend tasks of section 10
  (10.7, 10.8, 10.11, 10.12, 10.14) passes, `backend/check.sh` passes, branch coverage 100% on `app`.
- Frontend feature: every task of sections 3-7 and 9, and the frontend tasks of sections 8 and 10,
  are checked off, `frontend/check.sh` passes with branch coverage >= 95%, the axe checks and the
  Playwright scenarios pass.
- NO-GO: any of: a failed validation; an open blocker or major finding; a failed verify clause;
  coverage below the target; an accessibility violation that axe or the `ui-ux-tester` finds; the
  metadata changing a result, a `NormRef` or `input_hash` (of the two recorded exceptions, 10.7
  changes only expression text and 10.8 only the rounded output of `R`; neither changes an
  unrounded value, a `NormRef` or `input_hash`); a limit or a field of a type written in the
  frontend code; any file in Egor's zones changed.
- The five settings of `design.md` decision 12 are turned on before the pilot is first shown
  outside the team. That is Akim's step at that moment, deliberately not a GO or archive condition
  of this change, which describes both states.
- Archive only after both features are merged and after `calculation-api` and
  `calculation-core-contract` are archived.

## Dependencies

- `calculation-api` (WP8): merged into `develop` (`23318c1`); its archive is left (task 6.5).
  This change adds to its listing requirement and is archived after it.
- `calculation-core-contract` (WP2): engine and report merged; tasks 3.4, 3.5, 5.4 move here
  (section 6); its archive follows WP1. This change is archived after it.
- `retarget-mvp-domain` (WP1, Egor leads): modifies "Calculation input form"; this change does not
  edit that requirement (task 1.4).
- `normative-catalog-backend` (WP9): until it is merged the pilot answers `503`; task 3.3b mocks
  it, and task 8.3 runs the journey for real after the merge.
- `calculation-core-contract` `tasks.md`: task 8.4 ticked 3.4, 3.5 and 5.4 there on 2026-10-18
  with Akim's word; its header already names `feature/frontend-app/frontend` for them. Its
  `transparent-output` and `report-generator` requirements carry the first-iteration clauses of
  `design.md` decision 12, implemented by tasks 10.10-10.12 here.
- `user-accounts-auth` (planned, Akim) and a normative catalog interface (a future change): not
  dependencies; both are Non-goals here.
- `report-title-block-limits` (Akim, report generator; its task 3.4): its feature
  `feature/report-title-limits/backend` adds `maxLength` to five fields of the report request
  (designation 123, document name 150, documentation kind 7, organization 130, surname 11).
  Once it is merged into `develop` and `develop` is merged into this feature's branch,
  `npm run gen:api:check` in `frontend/check.sh` fails until `npm run gen:api` regenerates
  `frontend/src/api/schema.d.ts`; commit the regenerated file with that merge. No task of this
  change reads `maxLength`: the report form shows the server's `422` next to its field (task
  7.2). A later task that does should note that the server counts Unicode code points and an HTML
  `maxLength` counts UTF-16 code units, so the browser limits characters outside the Basic
  Multilingual Plane (emoji) more strictly than the server.
