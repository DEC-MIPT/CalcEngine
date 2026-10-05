# Tasks

Owner: Akim (frontend and backend zones). No WP number: the change was found when the frontend
became ready for coding.

Branches: two features (`AGENTS.md`, Branching rules).

- `feature/frontend-app/backend` (Akim, from `develop`): section 2, the metadata of the
  contract. It does not depend on the frontend and can merge into `develop` first.
- `feature/frontend-app/frontend` (Akim): sections 3-7 and the frontend part of 8. It branches
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
  `openspec validate --all --strict`; verify: both pass (2026-10-06, 20/20; re-run after the review fixes)
- [x] 1.2 (spec) Run `spec-reviewer` on this change until a report on the current version lists no
  blocker and no major finding; record the passes in
  `docs/decisions/frontend-app-readiness.md`
- [x] 1.3 (spec) Run `norm-traceability-checker`; verify: it confirms that no requirement of this
  change fixes a formula, coefficient or limit (the metadata of section 2 is not a norm value)
  (2026-10-06: confirmed, no calculation requirement; `docs/decisions/frontend-app-readiness.md`)
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
  `bab155f`; the baseline got three entries for the fixture's hashes by hand, not a full regeneration)
- [x] 2.5 Run `backend/check.sh` and the `postgres` module (backend); verify: `ruff`, `mypy`,
  `lint-imports` pass, branch coverage of `app` stays 100%, and the `pre-commit` hooks pass (done 2026-10-06 on `feature/frontend-app/backend`, `bab155f`)

## 3. Technical foundations (feature `frontend-app/frontend`)

- [ ] 3.1 Add `openapi-typescript`, the script `npm run gen:api`, the committed
  `frontend/src/api/schema.d.ts`, and a check in `check.sh` that the committed file is current
  (frontend); verify: regenerating from the backend of section 2 leaves no diff; a hand edit of the
  file makes the check fail
- [ ] 3.2 Add the API client over `openapi-fetch` with the base address from
  `VITE_API_BASE_URL`, and a helper that turns an error body (`code`, `message`, `fields`) into a
  typed value (frontend); verify: Vitest tests for a `422` body with `fields`, a `404`, a `503`, and a
  network failure
- [ ] 3.3a Add MSW with one set of handlers shared by the browser and Vitest, and the script
  `npm run dev:mock` (frontend); verify: `npm run dev:mock` answers `GET /calculation-types`
  from the handlers, and the Vitest setup uses the same handler module
- [ ] 3.3b Add the scenario handlers of `design.md` decision 4: pass, fail, refused, warning,
  `422`, `503`, typed by the generated schema (frontend); verify: one test per scenario reads
  the response through the client of 3.2 and gets the expected typed value
- [ ] 3.4 Add React Router with the four addresses of "User journey and screens" and empty screens
  (frontend); verify: a test per address renders its screen; an unknown address renders a "not
  found" screen
- [ ] 3.5 Add the typed `ru`/`en` dictionary with the fallback to `ru`, the language switch, and
  number formatting through `Intl.NumberFormat` (frontend); verify: tests that a missing `en` key
  shows the `ru` text, and that `172.5` shows as `172,5` in Russian and `172.5` in English
- [ ] 3.6 Add `eslint-plugin-jsx-a11y` and an axe helper for component tests (frontend); verify:
  `check.sh` runs both; a test component with an unlabelled input fails the axe helper
- [ ] 3.7 Add the `Formula` component on MathJax with the raw-text fallback and the restricted
  extensions of `design.md` decision 1 (frontend); verify: tests that a valid LaTeX string is
  typeset, that an invalid one shows its raw text, that neither throws, and that
  `\href{javascript:alert(1)}{x}` and a `\require` string create no link and run no script
- [ ] 3.8 Add Playwright with Chromium, Firefox and WebKit, used by the cross-browser scenario here and by tasks 8.6, 8.7, 8.9
  (frontend); verify: one test opens a mocked result with a trace and finds every step's formula
  typeset in each of the three engines

## 4. Screens and navigation (feature `frontend-app/frontend`)

- [ ] 4.1 Build the page shell (title, language switch, link to type selection) and the shared
  states: loading, error with `code` and `message` and a retry, and not found (frontend); verify:
  tests for each state, with the retry repeating the same request
- [ ] 4.2 Build the type selection screen from `GET /calculation-types` (frontend); verify: tests
  with two types, with an empty list, and with a `503`; choosing a type opens the form address
- [ ] 4.3 Wire the submit of the form to `POST /calculations` and the open of the stored result
  by its address, including a reload (frontend); verify: tests that a submit opens
  `/calculations/<id>` and that opening the address alone reads `GET /calculations/{result_id}`
  and runs no calculation; an unknown id shows "not found"
- [ ] 4.4 Wire the link from the result to the report screen (frontend); verify: a test follows
  the link and lands on `/calculations/<id>/report` of the same id

- [ ] 4.5 Keep entered values, response bodies and stack traces out of the console and off the
  screens (frontend); verify: a test spies on `console` during a `422`, a `404`, a `503` and a
  network failure and finds no entered value, no response body and no stack trace

## 5. Input form (feature `frontend-app/frontend`)

- [ ] 5.1a Build the form fields from one type's entry: order, `label`, `symbol` as formula,
  `hint`, language of the texts (frontend); verify: a test with two synthetic types shows different
  fields with the same component and no type name in the form code; with the interface in English
  the `label.en` and `hint.en` of the listing are shown, and `label.ru` is shown for a quantity
  that has no `en` text
- [ ] 5.1b Build the unit choice: limited to the input's `units`, preset to `base_unit`, and fixed
  to `base_unit` for an input with `whole_values_only` (frontend); verify: tests that `phi_II`
  offers `deg` only while `b` offers every listed unit
- [ ] 5.2 Add the client checks: filled, finite number, whole number for `whole_values_only`
  in the base unit, with no rounding or change of the entered value (frontend); verify: tests for
  empty, `abc`, `1e999`, `30.5` on a whole-values input (value kept, message names the rule, no
  request sent), and `30`, `30.0`, `30e0` accepted
- [ ] 5.3 Show a server `422`: each entry whose `location` ends with a declared input name marks
  that field, others show above the form, entered values are kept (frontend); verify: tests with
  a body that names one field, two fields, and no field
- [ ] 5.4 Show that a value outside the method's range is accepted by the form and decided by the
  backend (frontend); verify: with the warning and the refused mocks of 3.3b, the form sends the
  request and the result screen shows the outcome; the form code holds no limit

## 6. Result display (feature `frontend-app/frontend`; from `calculation-core-contract` 3.4, 3.5, 5.4)

- [ ] 6.1a (part of `calculation-core-contract` 3.4) Render the typed steps, with each `NormRef`
  shown with its status (frontend); verify: tests with the envelopes of 3.3b: every field of a step
  (expression, substitutions with units, result with unit, `norm_refs`) is shown, and an unverified
  `NormRef` is never shown as verified
- [ ] 6.1b (part of 3.4) Render, for each check step, its comparison, both values with units and
  whether it passed, in text, and the unverified-step summary (frontend); verify: tests that a check
  step says "passed" or "failed" in words with both values, and that the summary shows
  `unverified_step_count` when it is above zero and is absent at zero
- [ ] 6.2 (is `calculation-core-contract` 3.5) Render the envelope's `outputs` with value, unit,
  `rounding_rule` and `rounding_source`, an engineer-set rule shown with the engineer and the
  rationale (frontend); verify: tests for a `NormRef` source and for an engineer-set source
- [ ] 6.3 Make steps expandable and collapsible by pointer and keyboard with `aria-expanded`,
  collapsed on open, with expand-all and collapse-all (frontend; `transparent-output` "Expandable
  steps"); verify: tests for click, Enter, Space, the attribute, the collapsed start (each header shows its step's result with
  its unit), and the two buttons
- [ ] 6.4a (part of `calculation-core-contract` 5.4) Build the shared status component for a
  warning and a refusal: icon, text label and frame shape, with the meaning in text that assistive
  technology reads (frontend); verify: a test that its text is present with all styles removed,
  and an axe check; the same test is the colour-independence test for 6.4b and 6.4c
- [ ] 6.4b (part of 5.4) Show the refusal: the `verdict_reason` with the violated bound, the input
  value and the bound's `NormRef` list, and no result value (frontend); verify: a test with the
  refused mock finds the three items and no output value; uses 6.4a
- [ ] 6.4c (part of 5.4) Show the applicability warning next to the result: the input, the violated
  bound of the validated range and that bound's source, an engineer-set source shown with the engineer
  and the rationale (frontend); verify: a test with the warning mock finds the three items beside the
  outputs of 6.2; uses 6.4a

## 7. Report interface (feature `frontend-app/frontend`)

- [ ] 7.1a Build the title-block part of the report form and the `signature_block` switch
  (frontend); verify: tests for the required `designation`, `document_name` and `organization`, the
  optional `documentation_kind`, and the switch hiding and not sending the signatories
- [ ] 7.1b Build the three signatories with the required-field rules of "Report request screen"
  (frontend); verify: tests for an empty developer date, an empty normative-control surname, and a
  checker given in part

- [ ] 7.2 Download the `.docx` from `POST /calculations/{result_id}/report` under the name of the
  response's `Content-Disposition` (which the backend exposes to cross-origin pages,
  `backend/app/main.py`, `expose_headers`), and show a `422`, `404`, `409` or other error in text
  with the fields marked by the rule of `design.md` decision 7 (frontend); verify: tests with a
  mocked file response, a refused result (downloads as any other), and each error (`422` with the
  body `fields: [{location: ["body", "title", "designation"], message: "..."}]` marks the
  designation field, and an entry with `location: ["body"]`, as the backend gives for an incomplete
  signatory, is shown above the form; `404`; `409 calculation_type_not_registered`); no file is saved on an error

## 8. Verify and close

- [ ] 8.1 Run `frontend/check.sh` (frontend); verify: `eslint`, `tsc -b` and `vitest run --coverage`
  pass with branch coverage >= 95%, and a run with the threshold of `vite.config.ts` raised above
  the measured coverage fails
- [ ] 8.2 `tester` GO for each feature; `ui-ux-tester` confirms the screens, keyboard operation,
  contrast, no colour-only meaning and the visual brief of `design.md` decision 5 (tester)
- [ ] 8.3 Run the journey end to end against the real backend and, once WP9 is merged, a real
  catalog source: type selection, form, result, report download, with the frontend and the backend
  on different origins and `DEC_CORS_ORIGINS` set (frontend); verify: a recorded manual run in which
  the downloaded file has the name the backend gave (the `Content-Disposition` is readable
  cross-origin); until WP9 is merged the pilot's `503` is shown as in "Backend not available"
- [ ] 8.4 (spec) After 6.1a, 6.1b, 6.2 and 6.4a-6.4c are done, tick tasks 3.4, 3.5 and 5.4 in
  `calculation-core-contract` `tasks.md` and name this change there (spec; needs Akim's word
  to edit that change)
- [ ] 8.5 Run the axe helper of task 3.6 over the four screens (type selection, form, result,
  report) in their states: loading, error, `422`, `503`, warning and refusal (frontend); verify:
  every run reports no violation that axe can detect in jsdom
- [ ] 8.6 Run the keyboard journey from type selection to the downloaded report in Playwright
  (frontend); verify: the test completes it with the keyboard alone against the mocks and checks
  after each key press that the focused control has a visible indicator of at least 3:1
- [ ] 8.7 Run an axe contrast check of every screen in Chromium (frontend); verify: no text
  below 4.5:1 (3:1 for large text), with the warning and refusal states and each interface state
  (light and dark, if both exist) in the run
- [ ] 8.8 Check once by hand in branded Edge and Safari that a result with a trace shows every
  formula typeset and that the journey completes (frontend); verify: a recorded manual run with the
  browser versions
- [ ] 8.9 Measure the transition time of "Non-functional — language, accessibility, browsers"
  once all four screens exist (frontend); verify: a Playwright test in Chromium against the mocks
  takes 20 runs of response-to-first-render for each screen change and fails when the 95th
  percentile is 1000 ms or more
- [ ] 8.10 (spec) After the merge of the frontend feature, update the command lists of `AGENTS.md`
  and `CLAUDE.md` with `npm run gen:api`, `npm run dev:mock` and the Playwright command (documents,
  on `develop`; needs Akim's word to edit them)
- [ ] 8.11 (spec) Archive this change after both features are merged and after `calculation-api`
  and `calculation-core-contract` are archived

## Requirement coverage

| Requirement | Verified by |
|---|---|
| `web-platform` User journey and screens | tasks 3.4, 4.1-4.4, 6.4b, 7.2, 8.3 |
| `web-platform` Input form built from the type's contract | tasks 5.1a, 5.1b, 5.2-5.4, 6.4b, 6.4c |
| `web-platform` Report request screen | tasks 7.1a, 7.1b, 7.2, 8.3 |
| `web-platform` Non-functional — language, accessibility, browsers | tasks 3.5, 3.6, 3.8, 5.1a, 8.2, 8.5-8.9 |
| `web-platform` Non-functional — safe handling and test coverage | tasks 3.7, 4.5, 8.1 |
| `calculation-api` Input and output metadata in the types listing | tasks 2.1-2.5 |
| `transparent-output` Expandable steps | task 6.3 |
| `transparent-output` Trace display consumes typed steps and warnings (`calculation-core-contract`) | tasks 6.1a, 6.1b, 6.2, 6.4a-6.4c |

## DOR checklist

- [x] `proposal.md` (with "Non-goals"), `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes and a `spec-reviewer` report on the current version lists
  no blocker and no major finding (tasks 1.1, 1.2; 2026-10-06, 20/20, pass 3)
- [x] Functional requirements and scenarios recorded; each requirement is mapped to a task
  ("Requirement coverage")
- [x] Non-functional requirements recorded (`web-platform` "Non-functional — language,
  accessibility, browsers"; `design.md`, "Non-functional requirements")
- [x] Each task is small enough for one session (Akim's judgement, confirmed 2026-10-06)
- [x] Acceptance and Go/No-Go criteria written (every task has a verify clause; section below)
- [x] Branches defined (header)
- [x] Dependencies satisfied (below): the engine, the report and `calculation-api` are merged; WP9 is
  mocked by task 3.3b and the archives are not implementation dependencies

## DOD and Go / No-Go

- GO is declared per feature by the `tester` agent, with `ui-ux-tester` confirmation (UI changed).
- Spec phase: `openspec validate --all --strict` passes; the `spec-reviewer` report lists no
  blocker and no major finding; `norm-traceability-checker` confirms that no norm value is fixed.
- Backend feature: every verify clause of section 2 passes, `backend/check.sh` passes, branch
  coverage 100% on `app`.
- Frontend feature: every task of sections 3-7 is checked off, `frontend/check.sh` passes with
  branch coverage >= 95%, the axe checks and the Playwright scenario pass.
- NO-GO: any of: a failed validation; an open blocker or major finding; a failed verify clause;
  coverage below the target; an accessibility violation that axe or the `ui-ux-tester` finds; the
  metadata changing a result, a `NormRef` or `input_hash`; a limit or a field of a type written in
  the frontend code; any file in Egor's zones changed.
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
- `calculation-core-contract` `tasks.md` (task 8.4 ticks 3.4, 3.5, 5.4 there and may correct its
  sentence that this feature branches from `feature/calculation-engine/backend`; the engine is
  merged and this feature branches from `feature/frontend-app/backend`): editing that file needs
  Akim's word.
- `user-accounts-auth` (planned, Akim) and a normative catalog interface (a future change): not
  dependencies; both are Non-goals here.
