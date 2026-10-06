# Design

## Context

`frontend/` is the WP6 skeleton: React 19.2, Vite 8, TypeScript 6, Vitest 5 with React Testing
Library and a 95% branch threshold, ESLint; `frontend/check.sh` runs `eslint`, `tsc -b` and
`vitest run --coverage`. The API is `calculation-api` (FastAPI, OpenAPI at `/openapi.json`).
One developer (Akim) writes the frontend. The choices below come from
`docs/akim/frontend-app-kickoff.md` unless a decision says otherwise.

Component boundary for C/C++ (`openspec/config.yaml`): this change touches no hot path. The backend
part only adds metadata to the quantity declarations and the listing; the pure calculation
function, its boundary (WP5 decision 7) and the engine are unchanged.

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
     list), because the pilot selects the table row by whole degrees. The accepted spellings are
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
9. **Splitting task 5.4 of `calculation-core-contract`** (kickoff 8). The requirement text is
   unchanged; the plan is three tasks in `tasks.md` section 6: a shared status component that
   carries icon, text and frame shape (so "readable without colour" is tested once), the refusal
   view, and the warning view with the result. Task 3.4 is split in two (6.1a, 6.1b) and 3.5 is kept
   whole (6.2), and the expandable steps are task 6.3.
10. **Non-goals and where they go.** The normative catalog interface is a future change, built on
    `GET /normatives/search` and `GET /normatives/documents/{document_id}` of
    `normative-catalog-backend` (WP9, branch `feature/normative-catalog/backend`). Authorization is
    the planned change `user-accounts-auth` and the `user-accounts` capability. This change shows
    no login, token or plan.

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
  states the branching (from `feature/frontend-app/backend`). Task 8.4 may correct it.
- **Playwright is not set up.** Task 3.8 adds it; it is used for the cross-browser formula
  scenario, the keyboard journey, the contrast check and the transition time (tasks 3.8, 8.6,
  8.7, 8.9).
- **MSW and the real backend can drift.** The handlers are typed from the generated schema;
  an end-to-end run against the real backend, with a catalog source, is part of GO once WP9 is
  merged (`tasks.md` task 8.3).
- **Design skills.** Visual details are not fixed here; the `ui-ux-tester` judges the result against
  decision 5 and the accessibility requirement.
