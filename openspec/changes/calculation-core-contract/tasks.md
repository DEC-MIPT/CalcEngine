# Tasks

Owner: Akim. Egor confirms `NormRef` only.

Branch: spec work is committed directly to `develop` (`AGENTS.md`, Branching rules). Code
is done on feature branches from `develop`, each merged only when its whole feature is done:
`feature/calculation-engine/backend` (engine: every backend task of sections 2-5, tasks
6.1-6.2, and 7.1a-7.1c), `feature/report-generator/backend` (report, tasks 6.2a-6.2f and 6.3-6.4) and
`feature/frontend-app/frontend` (transparent output, tasks 3.4, 3.5, 5.4), all Akim's zone.
Checkboxes in this file are ticked in `develop` as each subtask is done on the feature branch; the code reaches `develop` only when the whole feature is done (`AGENTS.md`, Branching rules).

The `NormRef` shape is agreed with Egor (task 1.3), so no task waits for it.

## 1. Spec readiness

- [x] 1.1 Write proposal, design, and spec deltas for `calculation-engine`, `transparent-output`, `report-generator`, `security` (2026-09-26)
- [x] 1.1a Resolve the first review pass of `spec-reviewer` and `norm-traceability-checker` (2026-09-26; see `docs/decisions/calculation-core-contract-readiness.md`)
- [x] 1.2 Run `openspec validate calculation-core-contract --strict` and `openspec validate --all --strict` (passed 2026-09-26, 13/13)
- [x] 1.3 Egor confirms the `NormRef` shape and answers the open questions in `design.md` (section "NormRef"); recorded in `design.md` (2026-09-26, accepted on Akim's word; Egor confirmed all eight answers in writing on 2026-09-27 in `docs/decisions/normref-questions-egor.md`, commit `a1a896c`)
- [x] 1.3a Sync `design.md` resolutions into the delta specs and tasks: `norm_refs` list on a step, `Source` (`NormRef` list or `EngineerRule`), `engineer_rules` in the envelope (2026-09-26)
- [x] 1.4 Run `spec-reviewer` on this change and resolve blockers (2026-09-26, four passes, 0 blockers, re-run after the `NormRef` sync: 0 blockers, 2 major (warning structure fixed; written confirmation, since given in commit `a1a896c`); see `docs/decisions/calculation-core-contract-readiness.md`)
- [x] 1.5 Run `norm-traceability-checker` and confirm that no requirement fixes a norm value (2026-09-26, two passes, no norm value fixed)
- [x] 1.6 `tester` issues the verdict for the spec change (see DOD) (2026-09-27: **GO**, spec phase; validation, spec-reviewer pass 8 (0 blockers, 0 major, 1 minor fixed), norm-traceability-checker re-check, and Egor's written NormRef agreement all pass; implementation sections 2-6 remain open and are not covered; see `docs/decisions/calculation-core-contract-readiness.md`, section "Tester verdict")
- [x] 1.7 (spec) Resolve the implementation audit of 2026-09-29: `design.md` decisions 11-17, refinements of decisions 3-7, the amendment of resolution 2, the requirement "Formula evaluation from data", and the changes to "Pure calculation function", "Typed trace step", "Explicit units at the boundary", "Applicability check with three outcomes", "Result envelope", "Automatic correctness validation", and the `transparent-output` and `report-generator` scenarios for check steps; re-run `openspec validate --all --strict`, `spec-reviewer` and `norm-traceability-checker` until they report no blocker and no major finding; record the result in `docs/decisions/calculation-core-contract-readiness.md` (2026-09-29: validate 18/18; `spec-reviewer` passes 9-11, last one 0 blockers, 0 major, READY; `norm-traceability-checker` two passes, 0 blockers, 0 major; see section 8 of that file)
- [ ] 1.8 (spec) Egor acknowledges in writing the amendment of resolution 2, decision 11 (the expression tree he stores) and decision 6 (the `input_hash` algorithm), in `docs/decisions/calculation-core-contract-formula-execution-akim.md`
- [x] 1.9 (spec) Resolve the report amendment of 2026-09-30: `design.md` decision 10 refined and decision 18 added, the `report-generator` requirement "GOST report structure" changed (the signature block is the rows of columns 10-13 of the title block of form 5), tasks 6.2a-6.2f added, the requirement "Report values, formulas and dates" added, and tasks 6.3 and 6.4 reworded; re-run `openspec validate --all --strict`, `spec-reviewer` and `norm-traceability-checker` until they report no blocker and no major finding; record the result in `docs/decisions/calculation-core-contract-readiness.md` (2026-09-30: validate 18/18; `spec-reviewer` passes 12-14, last one 0 blockers, 0 major, READY; `norm-traceability-checker` three passes, 0 blockers, 0 major; see section 9 of that file)

## 2. Requirement 1: pure calculation function (backend)

- [x] 2.1 Define the calculation function signature `(typed inputs, resolved parameters) -> calculation result` (`CalculationResult`, `design.md` decision 12) and specify what the calculation type registry must hold; the registry itself (`Calculator` interface and lookup by calculation-type name) is `backend-layered-architecture` task 6.1, which this task extends, not redefines (done 2026-09-29 on `feature/calculation-engine/backend`, `ff8e423`) (backend)
- [x] 2.2 Test: run a calculation with the filesystem and the network patched to raise; it completes and returns a `CalculationResult` (done 2026-09-30 on `feature/calculation-engine/backend`, `8ee3038`) (backend)
- [x] 2.3 Test: two runs with identical inputs and resolved parameters give `CalculationResult` values that are equal and serialize to identical JSON (done 2026-09-30 on `feature/calculation-engine/backend`, `12d1cec`) (backend)
- [x] 2.4 Assign `result_id` in the service layer: a service calls the engine and builds the `ResultEnvelope` from its `CalculationResult` with a new UUID (`design.md` decision 12); test that two envelopes built from identical results have different `result_id` values and are otherwise equal to the result. Storing the envelope in `dec_app` is a later change (done 2026-09-30 on `feature/calculation-engine/backend`, `d749eb9`) (backend)
- [x] 2.5 Implement the expression-tree interpreter of `design.md` decision 11 in the engine, with the tree types in `schemas`; tests: a tree of allowed nodes gives its value; a node kind or a function outside the allowed set fails with a `DECError` before any node is evaluated (checked with a spy on evaluation); a tree over the depth or node limit fails the same way; a symbol without a value fails with a `DECError` naming it; a non-finite value (division by zero) fails with a `DECError` naming the step; a scan of the module finds no `eval`, `exec`, `sympify`, `parse_expr`, or `lambdify`. Tests use synthetic formulas only, never a real formula of a norm (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)

## 3. Requirement 2: typed trace step

- [x] 3.1 Define the typed trace step models (formula, table, and check step, `design.md` decision 16) with `step_id`, `expression`, `substitutions` (`{symbol, value, unit}`), `result`, `norm_refs` (a list of at least one `NormRef`), and for a check step `operator`, `right` and `passed`; define `NormRef` with both invariants (verified implies concrete `edition` and `clause`; `machine-extracted` implies `unverified`) and `Source`; tests: each invariant rejects its violation, and an empty `norm_refs` is rejected (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)
- [x] 3.2 Test: every step of a completed calculation has all fields of its kind, none null (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)
- [x] 3.3 Test: a step with any unverified `NormRef` in its `norm_refs` is marked and counted in the envelope (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)
- [ ] 3.4 Render typed steps and the unverified-step summary; show each `NormRef` with its status, and for each check step its comparison, both values with units, and whether it passed, in text (frontend)
- [ ] 3.5 Render the envelope's `outputs` with value, unit, `rounding_rule`, and `rounding_source` (frontend)
- [x] 3.6 Declare checks in the calculation type contract and derive the verdict ("Automatic correctness validation", `design.md` decision 16); tests: a contract without a check cannot be registered; two checks with the second failed give `fail` naming the second; two passed checks give `pass` naming the last (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)

## 4. Requirement 3: explicit units at the boundary (backend)

- [x] 4.1 Add unit-carrying value types, the closed unit vocabulary of `design.md` decision 13 (symbol, dimension, factor to the base unit; `1` for dimensionless) and the base-unit declaration per quantity in the calculation type contract; test that a contract whose base unit is not in the vocabulary is invalid (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`)
- [x] 4.2 Add boundary conversion of inputs and outputs in the engine; tests: a non-base input shows in the trace in its base unit; an output leaves in its base unit; calling the engine directly with an unknown unit or a unit of another dimension raises a `DECError` before any step runs (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`)
- [x] 4.3 Add the `rounding_rule` type (decimal places and mode `half_up` or `half_even`) and `rounding_source` (a `Source`) per output quantity in the contract; test that a type without them cannot be registered (this extends the registry of `backend-layered-architecture` task 6.1). Split the `RoundingRule` schema of `backend-layered-architecture` task 5.1 into the rule and its `EngineerRule` source, keeping its parameter-file validation and tests (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`)
- [x] 4.4 Round the values of the envelope's `outputs` with `Decimal(repr(value))` and `quantize` in the rule's mode (`design.md` decision 14), and return each with its unit, rule and source; tests: a tie value rounds differently in `half_up` and `half_even`; a check whose outcome would change on the rounded value uses the unrounded value (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`)

## 5. Requirement 4: applicability check with three outcomes

- [x] 5.1 Define the bound type `{quantity, kind, value, inclusive, source}` for the method's range (source: `NormRef` list) and the validated range (source: `Source`) in `schemas`, as resolved-parameter data (`design.md` decision 15); replace WP5's `ValidatedRange` (`min_value`, `max_value`) by bounds whose source is an `EngineerRule` in the parameter file, keeping its validation tests. Loading norm-given bounds from `dec_normatives` belongs to `normative-catalog-backend`; tests use synthetic bounds (done 2026-09-30 on `feature/calculation-engine/backend`, `911ff71`) (backend)
- [x] 5.2 Implement the check with three tests, one per outcome: run; refuse naming the bound and its `NormRef` list; run with a warning; plus tests of an input equal to an inclusive and to an exclusive bound of each range, and of two violated bounds refused by the one declared first (done 2026-09-30 on `feature/calculation-engine/backend`, `6f70d9c`) (backend)
- [x] 5.3 Define the request schema `CalculationRequest` (calculation type name, inputs as values with units, `design.md` decision 12) and test, on the schema and the service of task 2.4 without HTTP, that a malformed request, an unknown unit, or a unit of another dimension is rejected and the engine is never called (a spy on the engine). The HTTP scenarios of `security` "Input validation" are tested by the change that adds the endpoint (done 2026-09-30 on `feature/calculation-engine/backend`, `a70189b`) (backend)
- [ ] 5.4 Show the warning and the refusal in the UI, readable without colour (frontend)

## 6. Requirement 5: result envelope and accountability

- [x] 6.1 Define `CalculationResult`, `ResultEnvelope` (`design.md` decision 12) and the typed `verdict_reason` (decision 16) with `result_id`, `engine_version`, `input_hash`, `norm_refs`, `engineer_rules`, `verdict`, `verdict_reason`, `warnings`, `trace`, `unverified_step_count`, `outputs`; tests: no field of a completed or a refused envelope is null; the refused envelope has empty `trace` and `outputs`, `unverified_step_count` 0, `verdict_reason` naming the bound, `norm_refs` with the bound's `NormRef` list and every warning's `NormRef`, and `engineer_rules` with every warning's `EngineerRule` (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)
- [x] 6.1a Set `engine_version` from the constant `ENGINE_VERSION` of the engine package (`design.md` decision 7); test that it equals the version in `backend/pyproject.toml` (done 2026-09-30 on `feature/calculation-engine/backend`, `9c268c6`) (backend)
- [x] 6.1b Order and deduplicate the envelope's lists (`design.md` decision 17); tests: a `NormRef` used by two steps appears once at its first use; an `EngineerRule` used by a rounding source and a warning appears once; `outputs` follow the declared order of output quantities and `warnings` the declared order of the validated range's bounds (done 2026-09-30 on `feature/calculation-engine/backend`, `4a8a1eb`) (backend)
- [ ] 6.2 Implement `input_hash` per `design.md` decision 6; test that identical inputs and parameters give identical hashes, that a different input, calculation type, or resolved parameter set each gives a different hash, and that an integer and the equal float give the same hash. Checked off only after task 1.8 (implemented 2026-09-30 on `feature/calculation-engine/backend`, `ae096cd`; waits for task 1.8) (backend)
- [ ] 6.2a Report model (`design.md` decision 18): the report request schema (title-block data of columns 1, 5, 6 and 9; the signature-block setting, default enabled; the signatories with surname and date) and a pure function that builds the typed report model from the `ResultEnvelope`, the request inputs and the request, with the body sections input-data table (declared order of inputs), trace, and conclusion. Tests on the model: the sections are in this order; a check step carries its comparison, both values with units and whether it passed; each `NormRef` of a step is carried with its status, an unverified one marked unverified; a refused envelope keeps the sections, its trace section states the refusal and holds no step, and its conclusion names the bound, the input value with its unit and the bound's `NormRef` list; the request is rejected with the block enabled and a missing developer or normative control surname or date, with a checker without a surname or a date, and with a control character in any text ("GOST report structure"). Synthetic data only (backend)
- [ ] 6.2b Render the report body to `.docx` with python-docx, in memory (`design.md` decision 18), with numbers, units and formulas as "Report values, formulas and dates" gives them. Tests: the `.docx` read back with python-docx holds the body sections in order with the model's text; the value 172.5 `kPa` prints as `172,5 кПа`, 1e-07 `m` as `0,0000001 м`, and 2.0 `1` as `2`; every unit of the unit vocabulary (`design.md` decision 13) has a Russian designation; a LaTeX `expression` prints unchanged; rendering a synthetic envelope of 200 trace steps finishes in under 1 minute (base "Non-functional — generation time") (backend)
- [ ] 6.2c Sheet frame: A4 portrait, margins and page border as Annex Zh, figure Zh.1 a) of GOST R 21.101-2026 (edition unverified) shows. Tests: the section is A4 portrait, has a page border, and its margins equal the figure's frame (backend)
- [ ] 6.2d Grid of the form-5 title block in the first-page footer (Annex E, form 5 of GOST R 21.101-2026, edition unverified): the column widths and row heights of the figure, the column captions, the sheet format in column 26, columns 14-19 empty. Tests: the first-page footer holds a table with the form's captions; its column widths add up to the width of the form in the figure; every row has the figure's height; column 26 holds the format; the cells of columns 14-19 are empty (backend)
- [ ] 6.2e Data of the form-5 title block (Annex E, form 5 of GOST R 21.101-2026, edition unverified): the title-block data in columns 1, 5, 6 and 9 (corrected 2026-09-30: form 5 has no columns 2 and 3, so the report request drops them), and the sheet number and the number of sheets as the Word fields `PAGE` and `NUMPAGES` (columns 7 and 8). Tests: each datum is in its column; the field codes `PAGE` and `NUMPAGES` are in columns 7 and 8 (backend)
- [ ] 6.2f Title block of form 6 in the footer of the following sheets (Annex E, form 6 of GOST R 21.101-2026, edition unverified): column 1 and the sheet number field. Tests: the document uses a separate first-page footer; the other footer holds form 6 with its captions, column 1 and the field code `PAGE`; its column widths add up to the width of the form in the figure; a report long enough for two sheets renders without error (backend)
- [ ] 6.3 Print the result accountability block and the engineer responsibility statement after the conclusion ("Result accountability block"). Tests: the block shows `result_id`, `engine_version`, `input_hash`, the `outputs` with their rounding rule and its source, the `norm_refs` with their status, the `engineer_rules` with engineer and rationale, `verdict` and `verdict_reason`, the warnings, and `unverified_step_count`; it states that the design engineer is responsible for the result; an envelope with an applicability warning prints the warning with the input, the violated bound and that bound's source; the block is the last body section, in the model and in the rendered `.docx` (backend)
- [ ] 6.4 Fill the signature block, the rows of columns 10-13 of the form-5 title block ("GOST report structure"; GOST R 21.101-2026, edition unverified, Annex E, instructions for columns 10-13 and note 2): when the setting is enabled (the default), the developer (Разраб.) and normative control (Н. контр.) lines carry their surname (column 11) and date (column 13, `ДД.ММ.ГГ`), and the optional checker (Пров.) takes the row under the developer line; column 12 stays empty; when disabled, the role captions stay and columns 11 and 13 are empty. Tests: the default fills both lines; with a checker the row under the developer line holds Пров., the surname and the date, without one its caption, surname and date cells are empty; the date 2026-09-30 prints as `30.09.26`; with the block disabled and surnames and dates given, columns 11 and 13 are empty and the body section order is the same as with it enabled (backend)
- [x] 6.5 (backend, no code) Check GOST R 21.101 (edition unverified) from its primary source text and decide the default of the signature-block setting; the edition stays `unverified` until the normative pipeline confirms it (2026-09-27; checked against GOST R 21.101-2026, clause 4.1.7 and Annex E; default enabled; see `design.md` decision 10)

## 7. Pilot and sync

- [ ] 7.1 Use one in-scope calculation type of `foundations-shallow` (from WP1) as the pilot for the contract tests (backend). Tasks 7.1a and 7.1b use the working name of the candidate type agreed by Egor and the PM (`docs/decisions/first-calculation-type-egor-pm.md`, question 2) with synthetic data, and do not wait for WP1 to list it; task 7.1c waits for WP1 task 3.1. Since 2026-09-28 this also carries WP5's old tasks 5.2 and 6.2 (moved here when `backend-layered-architecture` was split). Split on 2026-09-29 (`design.md` decision 11):
  - [x] 7.1a The pilot's engineer-set parameter file under `params/`, validated by WP5's `parameters/param_schemas.py`; verify: the file validates against the engineer-set schema and contains no formula or coefficient key (done 2026-09-30 on `feature/calculation-engine/backend`, `5825cb6`) (backend)
  - [ ] 7.1b The pilot under `engine/` as a pure function holding only the order of the method's steps, receiving typed inputs and resolved parameters (formulas as expression trees, coefficients and branch thresholds with their `NormRef` list), registered in WP5's `Calculator` registry with at least one check. Tests use synthetic formulas and coefficients with placeholder `NormRef`, never a real formula or value of the norm; verify: a scan of the module's syntax tree finds no numeric literal other than `0` and `1`, calling the implementation with the same inputs and resolved parameters always returns the same result, and the module has no I/O-performing import (file, network, database client). The literal scan is a partial check (a constant written as `1 + x` in code would pass it); the review of the task compares the module's arithmetic against the expression trees it evaluates (backend)
  - [ ] 7.1c Run the pilot on the formula, its expression tree, its coefficients and thresholds read from `dec_normatives`; waits for the items in "Dependencies" (backend)
- [ ] 7.2 (spec) Remaining sync with `backend-layered-architecture` (WP5) after apply of this change: fix the safe parsing of `expression` named in `design.md` "Risks", and the pipeline verification state for the `provenance` gate (`normatives-formula-contract-review-egor.md`, questions 5-10, 12). Done 2026-09-28 in WP5: the engine is a pure function receiving typed arguments (former B5, its task 6.2 moved to task 7.1 above), decision 7 names the pure function as the C/C++ boundary, and "formulas in YAML vs in code" is settled (`dec_normatives` through the `provenance` gate; `params/**/*.yaml` holds only engineer-set values, WP5 `design.md` decision 3). The change owners (Akim and Egor) edit it; this change does not. Update 2026-09-29: the safe parsing of `expression` is settled by `design.md` decision 11 (no string parsing in the engine), and the `provenance` gate by the amendment of resolution 2; what remains is the read path from `dec_normatives`, which belongs to `normative-catalog-backend`
- [x] 7.3 (spec) Record for WP3 that `report-generator` names GOST R 21.101-2020 with an unchecked edition (2026-09-27; `design.md`, section "NormRef", "Handoff to WP3")

## 8. Close

- [ ] 8.1 (spec) After 1.2-1.9 pass, confirm the final version of the change is on `develop`
- [x] 8.2 (spec) Confirm WP1 task 2.1 (`retarget-mvp-domain`) is closed: the WP1 engine and output deltas match this contract (2026-09-27; `docs/decisions/retarget-mvp-domain-akim-review.md`)
- [ ] 8.3 (spec) `spec-keeper` syncs the deltas and archives the change, after `retarget-mvp-domain` is archived

## Dependencies

- `retarget-mvp-domain` (WP1) archives first; this change needs only its domain name.
- Task 1.3 (`NormRef` agreed with Egor) is closed; no task waits for it.
- `backend-layered-architecture` (WP5) is applied first: task 7.1 needs its `parameters/param_schemas.py`, `schemas/parameters.py` and the calculator registry (its task 6.1), and tasks 2.1, 3.6 and 4.3 extend that registry. WP5 needs nothing from this change, since `Calculator` is generic over the types.
- Task 7.2 runs after this change is applied.
- Inside this change: tasks 7.1a and 7.1b need tasks 4.3 and 5.1 (the parameter file's `RoundingRule` and bound schemas change there), and 7.1b also needs 2.5 and 3.6.
- `feature/report-generator/backend` (tasks 6.2a-6.2f and 6.3-6.4) and `feature/frontend-app/frontend` (tasks 3.4, 3.5, 5.4) consume the `ResultEnvelope` and trace types of `feature/calculation-engine/backend`. Each branches from `feature/calculation-engine/backend` once tasks 3.1, 3.6, 4.4, 6.1 and 6.1b are done there, and merges into `develop` after it (`AGENTS.md`, Branching rules).
- Inside `feature/report-generator/backend` (added 2026-09-30): tasks 6.2a to 6.2f run in that order; task 6.3 needs 6.2b, task 6.4 needs 6.2e. Task 1.9 is done before task 6.2a starts. Every report test uses synthetic envelopes, so no report task waits for task 7.1.
- Follow-up, not in this change (added 2026-09-30; owner Akim, a later `report-generator` change): length limits per title-block column, since a text longer than its cell is cut (`design.md` decision 18, "Risk").
- Task 1.8 (Egor's acknowledgement, added 2026-09-29): task 6.2 is checked off only after it. Task 2.5 may start before it; a change to the node set from Egor's answer is then applied to the interpreter.
- Task 7.1c (added 2026-09-29) waits for: `normatives-formula-contract` tasks 1.4-1.7
  merged into `develop` (Egor); the expression-tree field and the symbol binding on stored
  formulas (Egor, task 1.8); a named source for every coefficient of the pilot formula
  (Egor); `retarget-mvp-domain` task 3.1 (Egor); and the read path from `dec_normatives`
  in the planned `normative-catalog-backend` (Akim and Egor; not created yet). Tasks 7.1a
  and 7.1b wait for none of these.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task 1.2; re-run for task 1.7 on 2026-09-29)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements recorded (`design.md`, "Non-functional requirements")
- [x] Each task is small enough for one session (re-checked 2026-09-29: tasks 4.3, 6.1 and 7.1a split; 2026-09-30: the report tasks split into 6.2a-6.2f)
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branches defined (above)
- [ ] Dependencies satisfied: `NormRef` agreed with Egor (task 1.3; his written agreement is in `docs/decisions/normref-questions-egor.md`, commit `a1a896c`); open since 2026-09-29: task 1.7 (review of the audit changes) for every implementation task, task 1.8 for task 6.2, and the items of "Dependencies" for task 7.1c; open since 2026-09-30: task 1.9 for tasks 6.2a-6.4

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4).
- For the spec phase: `openspec validate --all --strict` passes; `spec-reviewer` reports
  no blockers; `norm-traceability-checker` confirms no norm value is fixed; Egor's
  agreement is recorded in his own words in `docs/decisions/normref-questions-egor.md`
  (commit `a1a896c`). Since 2026-09-29 also: task 1.7 is done with no blocker and no
  major finding, and Egor's acknowledgement of task 1.8 is recorded. Since 2026-09-30
  also: task 1.9 is done with no blocker and no major finding.
- For implementation: all tests of sections 2-6 pass with >= 95% branch coverage;
  `ui-ux-tester` confirms the frontend tasks 3.4, 3.5, and 5.4; the delta specs match the
  implementation.
- NO-GO: validation fails; an unresolved blocker; a norm value, tolerance, or clause
  number fixed in a spec; a `NormRef` field that can be null; a test failure or coverage
  below 95%.
- Archive (8.3) happens only after GO.
