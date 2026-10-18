# Design

## Context

`frontend/` is the WP6 skeleton: React 19.2, Vite 8, TypeScript 6, Vitest 5 with React Testing
Library and a 95% branch threshold, ESLint; `frontend/check.sh` runs `eslint`, `tsc -b` and
`vitest run --coverage`. The API is `calculation-api` (FastAPI, OpenAPI at `/openapi.json`).
One developer (Akim) writes the frontend. The choices below come from
`docs/akim/frontend-app-kickoff.md` unless a decision says otherwise.

Component boundary for C/C++ (`openspec/config.yaml`): this change touches no hot path. The backend
part adds metadata to the quantity declarations and the listing, and (section 10) the text of the
pilot's table-step expressions, the rounding rule of `R` and the report's conversion to Word
equations; the pure calculation function, its boundary (WP5 decision 7) and every computed value
are unchanged, and the report conversion runs after the calculation, outside the swap boundary.

## Decisions

1. **Math rendering: MathJax** (kickoff 1a). The `expression` of a formula step and a quantity's
   `symbol` are LaTeX strings, typeset by MathJax in a small `Formula` component. When MathJax
   cannot typeset a string, the component shows the raw LaTeX in a monospace element and the
   step stays readable; the cross-browser scenario of `web-platform` counts such a fallback as a
   failure. The strings come from the backend, so MathJax runs with the extensions that load code
   or create links (`require`, `autoload`, `html`, `href`, `unicode`) not loaded, and a string
   that needs one of them is shown as inert text (`web-platform` "Hostile symbol"). `transparent-output` already names MathJax, so its text is not amended.
   - Alternative: KaTeX (faster, smaller). Not chosen by Akim.
2. **API types: generated** (kickoff 2a). `openapi-typescript` turns the backend's
   `openapi.json` into `frontend/src/api/schema.d.ts`, committed. `npm run gen:api` regenerates
   it from a running backend or from a saved `openapi.json`; a check in `check.sh` fails when the
   committed file is not what the generator produces. No hand-written copy of an envelope or trace
   type.
3. **Client, routing and state** (a minimal set; not in the kickoff, chosen with Akim on
   2026-10-06). `openapi-fetch` over the generated types is the HTTP client; React Router gives
   each screen its address (`web-platform` "User journey and screens"); state is `useState` and
   `useReducer` inside the screens, with no global store and no request cache library. Interface
   texts are a typed `ru`/`en` dictionary object, where `ru` has every key and `en` may lack
   keys (the lookup falls back to `ru`); numbers go through `Intl.NumberFormat`. No i18n library.
   - Alternative: TanStack Query for requests; a router-less single component. Not chosen.
4. **Mocking while the pilot answers 503** (kickoff 3a). MSW holds one set of handlers used in
   the browser and in Vitest. `npm run dev:mock` starts Vite with the mock worker; `npm run dev`
   talks to the real backend at the address in `VITE_API_BASE_URL`. The handlers return, for
   `foundations_shallow_r`, a passing envelope, a failing envelope, a refused envelope, an
   envelope with a warning, a `422` body and the `503` body, so every result view of section 6
   of `tasks.md` is developed without the catalog source. The handler bodies are built from the
   generated types, so a contract change breaks `tsc`, not a test at run time. They contain no
   norm value that is not already in an example envelope of the backend tests.
5. **Visual brief: "technical terminal"** (Akim, 2026-10-06). Direction only; tokens and details
   are worked out during implementation, when the `shadcn/ui` variables are set, with the frontend
   design skills. Examples of colours and faces below are recommendations, not a token list.
   - Replaces the earlier brief (kickoff 7, option A with the warning colour of C: a minimal
     drafting sheet with restrained references to construction). On 2026-10-06 Akim judged it too
     restrained and sparse for an expert tool, where generous white space reads as a demo rather
     than an instrument; the new direction is bolder but stays a serious engineering tool, neither
     aggressive nor styled like a consumer product.
   - Idea: Swiss typographic precision with a hint of a diagnostic instrument or a terminal (an
     inspection tool, a measurement readout). Numbers are the main content of a result. The result
     still sits in a frame with a title block, like the frame the `.docx` report already uses
     (`calculation-core-contract` design, report), so the screen and the document look alike.
   - Palette (intent): calm neutrals and grey rules for the whole interface; one cobalt-blue
     accent, more saturated and colder than a link blue (for example around `#1d3fd6`), used
     sparingly: the primary action, links, the focus ring and the status "method applicable,
     check passed", which carries the accent instead of a separate green. Amber for a warning and
     red for a refusal stay, always together with an icon and a text label, with dark text on a
     light amber or red fill so that contrast meets AA. The accent marks a number (a tick, a bar,
     a status mark) and never colours its digits.
   - Typography (intent): a heading face with character, for example IBM Plex Sans Condensed or
     Geist at a heavy weight; a neutral grotesque for the interface text (Geist); numbers, units,
     step values and input fields in a monospace face or with tabular figures (Geist Mono, or
     JetBrains Mono), so that digits align in columns. Every face has full Cyrillic, checked before
     it is chosen. Formulas are typeset by MathJax.
   - Structure (intent): an open grid with visible 1 px rules, square corners, no shadows or
     gradients. Drawing construction is the language of the layout, not decoration: dimension
     lines with ticks mark sections, spans and the extent of a group of values, and corner marks
     close a frame; never literal icons such as helmets, cranes or rulers.
   - Density (intent): dense rather than sparse. Label, value and unit sit in compact rows, and
     the result screen shows the inputs, the outputs and the checks with little scrolling on a
     desktop screen. Density never goes below the WCAG 2.2 AA target size (2.5.8) or the contrast
     requirement.
   - Motion (intent): precise and mechanical: short linear or stepped transitions (for example
     100-150 ms) or an instant change of state; no springs, bounces or overshoot. All motion
     follows `prefers-reduced-motion`.
   - Responsive type and feedback (Akim, 2026-10-08,
     `docs/decisions/frontend/2026-10-08-frontend-ux-improvements-kickoff.md`, after the heuristic
     review of the same day; the direction above is kept). Type is a hybrid: body text, labels,
     fields and the columns of figures stay on whole-pixel steps (the `sm:` steps of the layout),
     and only the page heading and the verdict line scale with `clamp()` between rem bounds, never
     below their present size on a phone. Figures in a column keep their fixed column and the
     tabular face (Geist Mono has one advance width at every size). Micro-interactions are quiet
     (a flash of 1 px or a colour, a stepped rule, an echo in text) except one expressive moment, the
     verdict: its frame is drawn in 120 ms and its word follows, with focus moved to it. Every such
     animation lives inside `@media (prefers-reduced-motion: no-preference)`.
   - Bold pass and the expressive moments (Akim, 2026-10-08 "code now, docs later", and 2026-10-10;
     recorded here on 2026-10-18). Where they differ, these bullets replace the motion bullet
     above (100-150 ms), the "quiet except the verdict" sentence of the bullet above, and kickoff
     answer Q4 = B of `docs/decisions/frontend/2026-10-08-frontend-ux-improvements-kickoff.md`:
     - type selection: a full-bleed cobalt hero with a large heading and a drawn dimension-grid
       motif;
     - form: the active and the invalid row get a side rule; while a calculation is sent a scan line
       traces the input rows, and the result opens no sooner than 700 ms after the submit (none
       under reduced motion; `web-platform` "Calculation in progress");
     - result: the trace plays back step by step on the first showing of a `result_id`, the stamp
       and the output values wait for the last step, and a `pass` with no warning gets an
       expressive stamp of about 1 s (`web-platform` "Trace playback on first showing");
     - report: the submit control goes idle, sending (at least 600 ms), ready; on success a
       title-block stamp strikes in 110 ms with an ink ring and a stepped 2 px jolt of the form,
       and the file is saved only from the stamp's download control (`web-platform` "Report request
       screen").
     All of them run only under `prefers-reduced-motion: no-preference`.
   - Reference directions: (1) the title block and frame of a drawing sheet under GOST R 21.101
     (edition unverified; the report's own source is in `calculation-core-contract`), as the report
     uses it; (2) the readout of an inspection or measuring instrument (a value, its unit and its
     tolerance state in one line); (3) Swiss grid layouts and terminal interfaces (flush-left
     text, one accent).
   - Tooling for the base tokens (decided with Akim on 2026-10-06, accent and statuses revised the
     same day for this brief): `shadcn/ui` is initialised (`shadcn init`) on Tailwind CSS 4 only to
     hold a small set of CSS variables (neutral background, rules, cobalt accent that also marks a
     passed check, amber warning, red refusal, a square or near-square radius, Geist and Geist Mono
     self-hosted for their Cyrillic support, a visible focus ring, reduced motion); Phosphor is the
     icon library; no component is added until a screen needs it, and there is no token set beyond
     that. Where a design skill differs from this brief, the brief wins.
6. **Metadata shape** (kickoff 9, with the whole-values flag chosen on 2026-10-06). Each input and
   output of a type has `label` (`{ru, en?}`, `ru` required) and `symbol` (LaTeX, required); an
   input also has `hint` (`{ru, en?}`, optional) and `whole_values_only` (bool). A type that lacks
   a `label.ru` or a `symbol` is not registered, so the form never has to invent a label. No
   minimum or maximum is added: the method's range stays in the parameters and in the envelope's
   warning or refusal, so there is one source for a limit and the form cannot disagree with it.
   - `whole_values_only` is checked in the input's base unit, and the form fixes the unit choice of
     such an input to its base unit (`phi_II` is whole in `deg`, although `rad` is in its unit
     list), because the pilot selects the row of `Mγ`, `Mq`, `Mc` by a whole `φII` in degrees
     (СП 22.13330.2016, table 5.5, `unverified`; the table gives no rule for values between its
     rows, `docs/decisions/formula-autoparse-limits-egor.md`). The accepted spellings are
     numbers equal to their integer part (`30`, `30.0`, `30e0`).
   - The metadata lives with the declaration of the quantities in the engine module, as the units
     do (`QuantityDeclaration`, `engine/foundations_shallow_r.py`), and is carried to the
     listing by `InputView` and `OutputView` (`schemas/api.py`).
   - It is not a norm value and not a `NormRef`: it needs no source and no Egor acknowledgement,
     and `norm-traceability-checker` has nothing to check in it.
7. **Server error handling.** Every non-success response has the body of `calculation-api` "Error
   responses": `code`, `message` and, for `422`, `fields` (each with `location`, a list, and
   `message`). The form maps an entry to an input when the last element of `location` is a
   declared input name. Other errors are shown with their `message` and `code`. In the report
   form the `location` after `body` names the field: `title.<name>` for the title block,
   `<role>.surname` or `<role>.date` for `developer`, `normative_control` and `checker`, and
   `signature_block`; an entry that matches no field is shown above the form. Pydantic reports the
   signatory completeness rule of `ReportRequest` (a model validator) with the location `["body"]`
   only, so the `<role>` mapping is defensive and the client check of task 7.1b is the main guard. The frontend
   never shows a stack trace and logs no entered value.
8. **Where a screen gets its data.** The input form reads `GET /calculation-types` once per visit
   to a form; the result screen reads `GET /calculations/{result_id}` for an address, and takes
   the response of `POST /calculations` as the same shape. Nothing is recomputed in the browser:
   the trace display consumes the envelope as it is (`transparent-output` "Trace display consumes
   typed steps and warnings").
9. **Splitting task 5.4 of `calculation-core-contract`** (kickoff 8). The requirement text was
   unchanged by the split (decision 12 later added its first-iteration clauses); the plan is three tasks in `tasks.md` section 6: a shared status component that
   carries icon, text and frame shape (so "readable without colour" is tested once), the refusal
   view, and the warning view with the result. Task 3.4 is split in two (6.1a, 6.1b) and 3.5 is kept
   whole (6.2), and the expandable steps are task 6.3.
10. **Non-goals and where they go.** The normative catalog interface is a future change, built on
    `GET /normatives/search` and `GET /normatives/documents/{document_id}` of
    `normative-catalog-backend` (WP9, branch `feature/normative-catalog/backend`). Authorization is
    the planned change `user-accounts-auth` and the `user-accounts` capability. This change shows
    no login, token or plan.
11. **Unit designations and the decimal comma** (Akim, 2026-10-06). The Russian designations of
    the units (English shows the unit code) live in a frontend map of the unit vocabulary
    (`frontend/src/i18n/units.ts`), spelled as the backend's report table (`UNIT_DESIGNATIONS`,
    `backend/app/reporting/format.py`). A designation field in `GET /calculation-types` would be
    cleaner, but it is a contract change; the map is the vocabulary shared by all types, like the
    echo factors of `web-platform` "Unit echo in the base unit", and no unit of a type is written in
    the frontend. Number fields accept a decimal comma as well as a point
    (`frontend/src/form/parseValue.ts`): the request carries the number, the field keeps the text.
12. **The pilot's first iteration and its settings** (decided by Akim on 2026-10-07 for the language
    and on 2026-10-18 for the rest). "The pilot's first iteration" is the period while the pilot is
    shown only inside the team: the two developers and the PM. It ends before the pilot is first
    shown to anyone else (users, a review board, a thesis committee); then all five settings below
    are turned on again, and the requirements apply in full. During it each setting hides something
    the requirements still describe in full; each is one constant, turned back by one edit, with
    tests for both states:
    - `SHOW_LANGUAGE_SWITCH = false` (`frontend/src/components/AppShell.tsx`): no language switch;
      the `en` dictionary, `I18nProvider` and `LanguageSwitch` stay;
    - `SHOW_NORM_STATUS = false` (`frontend/src/screens/ResultScreen.tsx`): the trace shows no
      status mark at its references and no unverified-step summary (`Trace normStatus`,
      `NormRefList showStatus`); the refusal and the warnings keep the status;
    - `SHOW_ROUNDING_SOURCE = false` (same file): the outputs table has no rounding-source column
      (`Outputs source`); the source stays in the envelope and in the report;
    - `TRACE_NORM_STATUS = False` (`backend/app/reporting/docx_writer.py`): the report's trace steps
      print their references without status;
    - `ACCOUNTABILITY_SECTION = False` (same file): the report's section 4 is not printed, and the
      engineer-responsibility statement closes the conclusion instead. The report then carries no
      `result_id` (it stays in the file name), `engine_version`, `input_hash`, warnings or step
      statuses; Akim accepted this for reports read inside the team.
    The output values held until the trace playback ends are not a setting of the first iteration:
    they belong to the playback (`web-platform` "Trace playback on first showing").
13. **Trace symbols and display rounding** (Akim, 2026-10-18). The display is frontend only; the
    engine contract fixes `expression` as a LaTeX string and is unchanged, while the text the
    pilot writes into its table steps changes (below). Step headers, ruler ticks and substitutions are typeset by symbols found in the
    steps and in the types listing (`frontend/src/lib/stepSymbol.ts`, `NamedSymbol`), with
    `step_id` kept for assistive technology (`transparent-output` "Trace steps named by their
    symbols"). Values of an output are shown by its `rounding_rule` with the same half-up and
    half-even rule as the backend (`frontend/src/lib/rounding.ts`, backend `RoundingRule.apply`);
    the report does the same (`calculation-core-contract` `report-generator` "Report values,
    formulas and dates"). On the backend feature:
    - table steps write the selecting input by its LaTeX symbol (`\varphi_{II}`, not `phi_II`;
      task 10.7). No value, `NormRef` or `input_hash` changes; the fixture of task 2.4 was
      regenerated in the same commit (`ed6f672`) for the table-step expression strings only, so its test
      still proves that the metadata changes no result;
    - the engineer rule for the pilot's `R` went from 1 to 2 decimals (task 10.8,
      `backend/params/foundations_shallow_r.yaml`). Engineer: Akim; rationale (as in the file):
      rounding to hundredths of kPa for the pilot type, replacing the WP2 decision of 2026-09-30
      (tenths), until checked against the WP4 reference examples. It is an `EngineerRule`, not a
      norm value (`agent-docs/domain-constraints.md`: rounding from the norm, or set by the
      engineer with a rationale); the test of task 2.4 uses its own rule and is not affected.
      The rule belongs to the type's contract, not to the hashed parameter set
      (`backend/app/engine/boundary.py`: `input_hash` covers the type, the inputs, the resolved
      parameters and the two ranges), so `input_hash` does not change; new results carry `R`
      rounded to two decimals, and the unrounded value and the trace are unchanged.
    - showing a check unrounded when its rounded sides would read against `passed` is a display
      rule chosen by Akim, not a norm rounding: it keeps the comparison on the screen and in the
      report consistent with the engine's verdict, as the engine itself decides a check on
      unrounded values (`calculation-core-contract` design.md, decision 14).
14. **Report values and formulas as Word equations** (Akim, 2026-10-18; on the backend feature).
    LaTeX goes to MathML with `latex2mathml` and to Office Math with `mathml2omml` (pinned
    `0.0.2`, no type stubs, a mypy override), both pure Python and listed in
    `backend/requirements.txt`. A paragraph that holds only an equation is a left-aligned
    `m:oMathPara`, otherwise Word centres it; the top box that `mathml2omml` wraps around a
    formula is kept so that Word does not break an equation, and removed only for a step's
    expression so that a long formula can wrap at its operators.

## Non-functional requirements

Recorded as two `web-platform` requirements. "Non-functional — language, accessibility,
browsers": Russian and English (Russian complete), WCAG 2.2 AA, the last two versions of Chrome,
Firefox, Edge and Safari, and a 95th-percentile transition time under 1 second (measured in
Chromium over 20 runs against the mocks, from the arrival of the response to the first render).
"Non-functional — safe handling and test coverage": no entered value, response body or stack trace
in the console or on a screen, no code or link executed from a backend LaTeX string, and branch
coverage of `frontend/src` at or above 95% (the threshold already in `vite.config.ts`). The
backend part keeps the backend's own rule of 100% branch coverage on `app`. Colour contrast and
the keyboard journey cannot be detected by axe in jsdom, so they are checked in Chromium by
Playwright (tasks 8.6, 8.7).

## Risks and notes

- **Archive order.** `calculation-api` and `calculation-core-contract` hold requirements this
  change extends by name; their deltas are not in `openspec/specs/` yet, so this change adds
  instead of modifying and is archived after both.
- **`retarget-mvp-domain` overlap.** It modifies "Calculation input form"; this change adds a
  requirement that refines it. If WP1 changes that requirement again, the new requirement here
  must still agree with it.
- **Browsers.** The kickoff names Edge and Safari; the automated check uses Playwright's
  Chromium (Edge's engine), Firefox and WebKit (Safari's engine). A branded Edge or Safari is
  checked by hand once before GO (task 8.8).
- **Latency requirement overlap.** The base `web-platform` requirement "Non-functional —
  integration and latency" stays; the transition-time clause here only fixes how the frontend part
  is measured.
- **Stale sentence in another change.** `calculation-core-contract` `tasks.md` says the frontend
  feature branches from `feature/calculation-engine/backend`; the engine is merged, and this change
  states the branching (from `feature/frontend-app/backend`). Resolved: that header now names
  `feature/frontend-app/frontend` for tasks 3.4, 3.5 and 5.4, which task 8.4 ticked on 2026-10-18.
- **Playwright is not set up.** Task 3.8 adds it; it is used for the cross-browser formula
  scenario, the keyboard journey, the contrast check and the transition time (tasks 3.8, 8.6,
  8.7, 8.9).
- **MSW and the real backend can drift.** The handlers are typed from the generated schema;
  an end-to-end run against the real backend, with a catalog source, is part of GO once WP9 is
  merged (`tasks.md` task 8.3).
- **Design skills.** Visual details are not fixed here; the `ui-ux-tester` judges the result against
  decision 5 and the accessibility requirement.
- **Unit map drift.** The designations of decision 11 are a second copy of the backend's report
  table; a backend unit added without a frontend designation shows its code. A test that reads the
  backend table, as the echo factors have (task 9.3), would close this; it is not written yet.
- **The report without section 4 loses fields.** While `ACCOUNTABILITY_SECTION` is off, the report
  carries no `result_id` (it stays in the file name), `engine_version`, `input_hash`, warnings or
  status of the step references; a report shown outside the team should have it turned back on.
