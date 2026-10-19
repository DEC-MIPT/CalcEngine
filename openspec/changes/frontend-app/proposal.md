# Proposal

Owner: Akim (frontend and backend zones). No task of this change is in Egor's zones. A new
change found when the frontend became ready for coding; it is not one of WP1-WP8.

## Why

The only frontend part that is specified is the display of a result (`calculation-core-contract`
tasks 3.4, 3.5, 5.4, requirement "Trace display consumes typed steps and warnings"), and it has no
technical decision. `frontend/` is the WP6 skeleton (React 19, Vite, Vitest, no screens). The gaps:

- **No user journey.** `web-platform` "Unified web interface" names the flow in one sentence; no
  screen, no transition and no URL is specified.
- **No input form that is built from the contract.** `retarget-mvp-domain` fixes that the form
  takes its fields from the type's contract (`web-platform` "Calculation input form"), and
  `calculation-api` task 5.2a lists the units, but no change has a task for the form. The listing
  has no human label, no LaTeX symbol, no hint, and no mark for an input that takes whole values
  only (the pilot input `phi_II` selects a table row by whole degrees), so a form cannot be built
  without a hard-coded copy of the type.
- **No report screen.** The `.docx` endpoint exists (`calculation-api` "Report download") and needs a
  title-block request (`ReportRequest`); nothing asks the user for it.
- **Expandable steps have no task.** `transparent-output` "Expandable steps" is in the base spec and
  in no task list.
- **Task 5.4 is coarse.** It covers a shared colour-independent cue, the refusal view and the
  warning view in one line.
- **No non-functional requirements** for language, accessibility and browsers, although
  `transparent-output` requires "all supported browsers".
- **No technical decisions**: math rendering, API types, mocks while the pilot answers `503`
  (`calculation-core-contract` is merged, the catalog source is not), routing, state.

The decisions are in `docs/akim/frontend-app-kickoff.md` (Akim's own zone, not tracked); the
choices made are restated in `design.md`.

## What Changes

- `web-platform`: requirements for the user journey and screens (type selection, input form,
  result, report request), the input form built from the type's contract, the report request
  screen, and non-functional requirements (interface language, accessibility, browsers).
- `calculation-api`: one added requirement, label, LaTeX symbol, hint and a whole-values mark in
  the listing of each input and output. Metadata only: it does not change a calculation, a
  `NormRef`, a parameter, the result envelope or `input_hash`, and it reads nothing from
  `dec_normatives`.
- `transparent-output`: "Expandable steps" gets keyboard and state scenarios, and steps open
  expanded; three added requirements (steps named by their symbols, output values shown by their
  rounding rule, result screen reading aids); task 5.4 of `calculation-core-contract` is split
  into three tasks here.
- Added on 2026-10-18, after the work of `tasks.md` section 10 (`design.md` decisions 11-14):
  `web-platform` requirements for the trace playback, the computation trace and the report stamp;
  the settings of the pilot's first iteration; and edits made directly in
  `calculation-core-contract` (its own change, not archived): `transparent-output` "Normative
  clause references" and "Trace display consumes typed steps and warnings", and `report-generator`
  "GOST report structure", "Automatic normative references in report", "Result accountability
  block" and "Report values, formulas and dates" (settings `SHOW_NORM_STATUS`,
  `SHOW_ROUNDING_SOURCE`, `TRACE_NORM_STATUS`, `ACCOUNTABILITY_SECTION`; Word equations; output
  values by their rounding rule).
- Code on two feature branches (`tasks.md`): `feature/frontend-app/backend` (the metadata and the
  backend tasks of section 10) and `feature/frontend-app/frontend` (the interface).

## Capabilities

### New Capabilities

None added by this change beyond what other active changes create.

### Modified Capabilities

- `web-platform`: ADDED requirements. "Calculation input form" (modified by
  `retarget-mvp-domain`) is not edited here; the new requirement "Input form built from the type's
  contract" refines it and does not contradict it.
- `calculation-api`: ADDED requirement "Input and output metadata in the types listing". It is
  ADDED, not MODIFIED, because the requirements of `calculation-api` and
  `calculation-core-contract` are still in their active changes and not in `openspec/specs/`.
- `transparent-output`: MODIFIED "Expandable steps"; ADDED "Trace steps named by their symbols",
  "Values of an output shown by its rounding rule" and "Result screen reading aids".
- `transparent-output` and `report-generator` requirements of `calculation-core-contract`: edited
  in that change, not by a delta here, for the same archive-order reason.

## Non-goals

- **The normative catalog interface.** `GET /normatives/search` and
  `GET /normatives/documents/{document_id}` exist on the WP9 branch
  (`normative-catalog-backend`); a screen for them is a separate future change.
- **Authorization, accounts, tiers and the trial.** The planned change `user-accounts-auth`
  (Akim) and the `user-accounts` capability own them; no login screen and no token handling here.
- Changes to a calculation, a `NormRef`, a parameter file or the engine; range limits in the
  contract (the method's range stays a server-side warning or refusal). Two exceptions were made
  on 2026-10-18 and are recorded in `tasks.md` section 10: the text of the pilot's table-step
  expressions names the selecting input by its LaTeX symbol (task 10.7; no value changes), and the
  engineer rule of the pilot's `R` rounds to two decimals (task 10.8, `design.md` decision 13).
- A design system with tokens and Storybook (`design.md`, decision 5). Playwright was set up by
  task 3.8 after all.

## Impact

- `backend/app/schemas/calculation.py`, `backend/app/schemas/api.py`,
  `backend/app/engine/foundations_shallow_r.py` (metadata for the pilot's inputs and outputs).
- Section 10: `backend/app/engine/steps.py` and `foundations_shallow_r.py` (table-step text),
  `backend/params/foundations_shallow_r.yaml` (rounding of `R`), `backend/app/reporting/`
  (Word equations, rounding, the two report settings), `backend/requirements.txt`
  (`latex2mathml`, `mathml2omml`), `backend/app/schemas/calculation.py` (`RoundingRule.apply`).
- `frontend/` (all of it).
- No change in `ml/`, `infra/` or `dec_normatives`; no Egor acknowledgement is needed because
  no file of his zone or his contract is touched.
