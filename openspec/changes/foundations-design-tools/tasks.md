# Tasks

## Feature and branch plan

| Feature | Branch | Tasks | Dependencies |
|---|---|---|---|
| Backend design tools | `feature/foundations-design-tools/backend` | Section 2 | Reviewed integrated loads backend; decisions and references below; current DOR |
| Frontend design tools | `feature/foundations-design-tools/frontend` | Section 3 | Existing loads frontend accepted, reviewed and integrated; new typed backend contract accepted |
| Demo DOCX result parity fix | `fix/foundations-design-report/backend` | Section 2A | Integrated design-tool backend and stored result presentation contract |
| Documentation | No code branch; develop only | Sections 1 and 4 | Explicit Git consent for commit/merge/push |

Every code task belongs to exactly one feature above. Backend integrates before frontend; features integrate only when all their assigned tasks, tester GO and review are complete. Do not move unfinished predecessor tasks into this change or merge their branch without explicit consent.

## 1. Engineering and readiness

- [x] 1.1 Confirm the bounded first-release scope for candidate selection: explicit list, averaged mode only, objective, tie ordering, technical count limit and no global-optimum claim; record Akim's decision without inventing normative limits.
- [x] 1.2 Confirm explicit named-weight fields, permitted signs, contribution attribution, additional base moments and proposed upper-cut-only structural-load semantics or an independently typed base-level variant; verify no double weight or shear-arm transfer.
- [x] 1.3 Finalize dedicated search request/result/persistence contract, candidate source-resolution failure, cancellation and timeout behavior; verify the current quantity-map API and historical result compatibility.
- [x] 1.4 Obtain admissible independent reference origins, three complete explicit-weight examples and per-output tolerance provenance; verify the applicable origin policy before any new manual exception or oracle admission.
- [x] 1.5 Obtain current spec-reviewer and norm-traceability-checker reports on the finalized artifacts; verify no blocker/major, complete formula/source locators and explicit pending source statuses.
- [x] 1.6 Record DOR after decisions, strict validation, review and prerequisite evidence; distinguish artifact completion from readiness and verify the predecessor branch/integration state.

## 2. Backend design tools feature

- [x] 2.1 Add typed new-type scalar declarations and versioned load-level validation; verify units, labels, mutually exclusive modes, source attribution and backward-compatible old requests.
- [x] 2.2 Implement pure explicit vertical and signed moment assembly using approved inputs; verify each weight once, no averaged allowance, cut/base equivalence and unchanged shared executor.
- [x] 2.3 Connect the new type to reviewed R/pressure source bindings and full-contact/four-check flow; verify source-mode fail-closed behavior, unchanged coefficients, output order and refusing diagnostics.
- [x] 2.4 Add new-type methodology/source identity and stored-result validation; verify historical pilot/averaged identity and absent new historical fields remain valid.
- [x] 2.5 Emit typed optional visualization context for inputs, axes, load contributions and pressure envelope; verify every physical value binds to stored input/trace and refusals cannot imply redistributed contact.
- [x] 2.6 Implement bounded averaged-mode candidate evaluation with the approved policy; verify per-candidate R resolution, no silent dimension swapping, no reused explicit weights and exhaustive small-list selection.
- [x] 2.7 Add additive search persistence schema and repository operations; verify immutable provenance, selected ordinary-result linkage, structured exhaustion/incomplete outcomes and migration reversibility on a task-specific test DB.
- [x] 2.8 Add typed search API and result retrieval with technical caps/cancellation/timeout controls; verify invalid request rejection before execution and no certified selection from an incomplete search.
- [x] 2.9 Extend DOCX for weight assembly, stored diagram evidence and candidate decision; verify complete expressions, refusal/exhaustion meaning and unchanged historical report fixtures.
- [x] 2.10 Execute the admitted explicit-weight references through runner/API/DOCX and recorded invariants; verify mode equivalence, sign/unit cases, contact boundaries and approved tolerance metrics without recapturing expected outputs.
- [x] 2.11 Run backend feature acceptance, latency/limit measurements and frozen regression; verify backend/check.sh, at least 95% branch coverage, current strict validation and explicit DB/catalog checks or skips; only tester declares backend GO.

## 2A. Demo DOCX result parity fix

- [x] 2A.1 Align explicit-weight DOCX references, rounding, formulas and result evidence with the stored result screen; retain the input record, source status and title block.
- [x] 2A.2 Verify the Office Math XML, rendered DOCX, stored-output parity, refusal and the pilot and averaged report regressions. Require a scoped tester GO with at least 95% branch coverage of the changed code and independent report review before authorized integration.

## 3. Frontend design tools feature

- [x] 3.1 Regenerate API types and extend mocks with the new type, optional visualization context and search outcomes; verify schema/fixture drift and unchanged old envelopes.
- [x] 3.2 Add labelled weight-type controls and the approved fixed load-level explanation with scalar weights/moments; verify raw drafts/units, explicit mode changes, no hidden reverse load-factor conversion and clear d/h/d_1 explanations.
- [x] 3.3 Render the load schematic from stored context with signs, dimensions and load-plane distinction; verify keyboard/text alternatives, 320 px layout and no physical client recomputation.
- [x] 3.4 Render stored pressure envelopes and tables with labelled extrema/corners; verify pass/fail/diagnostic states, no false contact-area redistribution and exact source-value bindings.
- [x] 3.5 Add approved finite-candidate entry and search controls; verify bounds/policy visibility, explicit-weight search rejection, progress/cancellation/errors and no global-optimum language.
- [x] 3.6 Render immutable candidate comparisons and selected-result navigation; verify failed/refused/incomplete/exhausted distinctions, original inputs and report links.
- [x] 3.7 Add weight/selection trace context while retaining all steps initially expanded and manual disclosure; verify source labels, playback, derived refusal and historical draft eligibility.
- [x] 3.8 Run frontend automated and browser acceptance; verify frontend/check.sh, at least 95% branch coverage, keyboard/diagram/report journeys, reduced motion, all applicable browser requirements and unchanged pilot.
- [x] 3.9 Obtain ui-ux-tester confirmation and separate tester GO for the full reviewed frontend revision; verify no unresolved visual/control/accessibility finding and accurate check/skip evidence.

- [x] 3.10 Add a separate registry entry for the editable `weights-C` synthetic example; verify draft isolation, explicit submission, edit-return navigation and supported browser behavior.

## 4. Review, integration and closure

- [x] 4.1 Review the completed backend after tester GO; verify all section-2 tasks complete, independent references, unchanged executor/pilot and no open blocker/major/security finding.
- [x] 4.2 With explicit consent, integrate accepted backend and verify actual develop DB/API/report/source behavior, recording every unavailable catalog check separately.
- [x] 4.3 Review the completed frontend after tester GO/UI confirmation; verify all section-3 tasks complete, correct backend compatibility and no open blocker/major/security finding.
- [ ] 4.4 With explicit consent, integrate accepted frontend and run actual-develop integrated checks, candidate and check-only journeys, report verification and strict validation.
- [ ] 4.5 After all features are accepted and integrated, sync canonical specs and archive this change; verify no unchecked task, accurate provenance/limits and final strict validation.

## Current readiness

READY for backend implementation, recorded 2026-11-22 after the approved positive-resultant rule, admitted manual references and tolerances, finalized API, current spec review with no findings, current source traceability without gaps, and selected/all strict validation (25/25). Reviewed loads backend integration 2a401c5 is an ancestor of current develop 6269bae. The shared executor is unchanged. The [preceding loads frontend integration](../../../docs/decisions/backend/2026-11-08-foundations-pressure-from-loads-readiness.md#integrated-frontend-acceptance-2026-11-23) satisfies the frontend predecessor dependency. The design tools frontend remains subject to the acceptance gates below. Commit, merge, push and actual database migration remain separately authorized actions.

## DOR checklist

- [x] Proposal, all named delta specs, design and session-sized tasks exist and selected/all strict validation passes.
- [x] Akim confirmed candidate domain, objective, deterministic tie policy and the explicit-weight/load-plane contract.
- [x] Technical limits, search API/persistence, incomplete/cancellation behavior and performance measurement boundary are fixed.
- [x] Functional and non-functional requirements cover compatibility, security, privacy, accessibility, determinism and coverage.
- [x] Independent complete references, source locators and tolerance provenance meet the applicable origin/admission policy.
- [x] Current spec-reviewer has no blocker/major and norm-traceability review reports complete citations without source promotion.
- [x] Backend and frontend feature branches and exact task ownership are defined; applicable predecessor integrations are confirmed before that feature starts.
- [x] Acceptance and Go/No-Go criteria are complete and tied to an actual reviewed revision.

## Acceptance and Go/No-Go

Only tester declares GO per complete feature, with UI/UX confirmation where UI changed. Backend requires admitted independent calculations through runner/API/DOCX, source-aware metrics/reproducibility, exhaustive small candidate-set controls and unchanged frozen pilot/averaged results. A new type retains the applicable at-least-three-reference gate; no coefficient, expected value, tolerance or manual-origin exception is inferred from this proposal.

The new mode must conserve assembled vertical force and signed moments, include each contribution once, preserve unit equivalence, refuse contact loss and retain all four ordered bearing checks. Search may select only complete passing candidates under the approved finite policy; source failure, interruption and no solution cannot produce a pass. Old results retain identity, retrieval and report meaning.

All feature suites, required lint/types/import boundaries and branch coverage at least 95% must pass. Frontend requires responsive diagram/text parity, keyboard and reduced-motion behavior, applicable WCAG/browser checks and reviewed screenshots. Existing browser support requirements remain in force. For `bd99244` only, the web-platform delta defines the approved evidence exception; unsupported or skipped matrix checks remain visible in the evidence. Real DB/catalog checks and skips are distinct from mock or unit evidence. Applicable existing API/report targets remain, and bounded search is measured with named candidate counts and environment.

NO-GO includes any unresolved blocker/major/security issue, unapproved methodology or source, missing independent reference, failing test, insufficient coverage, blocking UI defect, incomplete search represented as success, regression identity change, or unvalidated/currently unreviewed artifacts. DOD requires reviewed, consented, verified integration of all code features, matching canonical specs and archive. No Git operation is implied by satisfying a task.
