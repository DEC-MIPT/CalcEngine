# Tasks

Owner: Akim. Current work restores contracts and records DOR; it adds no code.
Planning documents belong on develop. Every later code task belongs to exactly one
feature below; each has a bounded deliverable and verification for one session.

| Feature | Branch | Owned tasks | Dependency |
|---|---|---|---|
| Backend | `feature/foundations-loads/backend` | Section 2: engine, parameters/data, schemas, API, DOCX and backend verification | Recorded DOR from section 1 |
| Frontend | `feature/foundations-loads/frontend` | Section 3: form, diagram, results/trace/refusal UI, mocks, generated API types and browser tests | Backend's reviewed typed contract; branch from backend when its unmerged code is needed |

Sections 1 and 4 are planning, review or execution of existing checks, with no code.
Backend integrates before frontend. Commits, merges and pushes require explicit
consent; completing a checkbox is not Git consent.

## 1. Recover and agree the ready contract

- [x] 1.1 Recover proposal, design, eight delta specs and this plan; verify artifact paths exist and selected/all strict validation passes.
- [x] 1.2 Reconcile full MODIFIED requirements against canonical engine, interim, API, verification, trace, report and web specs; verify all unaffected scenarios remain and all six upstream owner archives/commits exist.
- [x] 1.3 Record confirmed engineering inputs, weight/sign/range/rounding conventions, empty initial validated_range and conditional manual-reference policy; verify the conversation and signed LOADS-DB-1 evidence at 1b0ea46 without runtime or NormRef promotion.
- [x] 1.4 Recover central, one-axis and two-axis reference candidates; verify complete hand inputs/intermediates/checks with admission and numerical tolerances explicitly unapproved, distinct from P1b formula points.
- [x] 1.5 Obtain current spec-reviewer and norm-traceability-checker reports; verify no blocker/major finding and no invented source, coefficient or tolerance.
- [x] 1.6 Record DOR against actual final artifacts and current review; verify every criterion below before implementation branches or calculation code.

## 2. Backend feature

- [ ] 2.1 Extend units and typed trace/refusal schemas with engineer_formula and kind=derived; verify unit conversions, API round trips and unchanged historical steps, envelopes and input-bound refusal shapes; validate internal volume units separately from actual force/moment API inputs.
- [ ] 2.2 Extract reusable R and reconnect the pilot; verify unchanged step order/IDs, deciding check, numeric result, saved envelope and original golden fixture without rewriting it.
- [ ] 2.3 Implement pure geometry and signed transfer with engineer rules; verify A/Wx/Wy, M+Q*h signs, cancellation, h=0, equivalent units and pressure-module axis interchange.
- [ ] 2.4 Implement mean, axial extrema and four signed corner pressures from resolved data; verify central equality, biaxial sign patterns, deterministic unrounded results and existing typed error handling for non-finite intermediates.
- [ ] 2.5 Implement contact refusal before four ordered bearing checks; verify p_min=0 allowed, negative corner with nonnegative axial minima, diagnostic prefix without final outputs/bearing conclusions, each isolated check failure, limiting_corner first-tie selection and first-fail/last-pass reason.
- [ ] 2.6 Register the fifteen-input/ten-output type, engineer parameters, validated_range=[] and explicit prepared-record alias; verify b<=l, all approved ranges, exact degree rows, independent d/h/d_1, no swapping/interpolation and unchanged catalog/pilot selection.
- [ ] 2.7a Install the separate loads-only prepared d_b-bound supplement from signed LOADS-DB-1; verify inclusive bound loaded from data, source/evidence digest match, rejection rather than clamping and unchanged original document records/statuses.
- [ ] 2.7b Bind the supplement only to this type and implement its allowlisted aggregate source digest; verify canonical constituent order, change on either constituent, fail-closed missing/unusable components, unchanged envelope label shape and pilot digest.
- [ ] 2.8 Connect existing API routes and immutable storage; verify metadata order, complete/derived-refused POST and GET envelopes, source kind/profile/digest, old result retrieval and no new endpoint.
- [ ] 2.9 Render loads DOCX inputs, directions, sources, diagnostic/calculation traces and checks; verify pass/fail/refused document content and unchanged meaning of historical pilot reports.
- [ ] 2.10 Obtain engineer admission and per-output tolerance provenance for a full central reference and add its runner/API/DOCX fixture; verify immutable independent derivation rather than expected values captured from this implementation.
- [ ] 2.11 Obtain engineer admission and per-output tolerance provenance for a full one-axis reference and add its runner/API/DOCX fixture; verify signed transfer, every expected output/check and origin evidence.
- [ ] 2.12 Obtain engineer admission and per-output tolerance provenance for a full two-axis reference and add its runner/API/DOCX fixture; verify corner signs/minimum, every expected output/check and origin evidence.
- [ ] 2.13 Run backend feature acceptance with tester; verify three admitted references through runner/API/DOCX, invariants with recorded seeds, metrics/reproducibility, frozen regression including unchanged pilot, backend/check.sh and >=95% branch coverage. Record actual DB/catalog checks or skips separately; only tester declares GO.

## 3. Frontend feature

- [ ] 3.1 Regenerate API types and extend fixtures/mocks for both types and refusal variants; verify schema drift checks, historical fixtures and source-label rendering.
- [ ] 3.2 Add type selection, fifteen labeled inputs and accessible direction/sign diagram; verify d/h/d_1 and N explanations, whole-degree behavior, correction feedback and keyboard/small-screen use without changing entered values.
- [ ] 3.3 Display ten outputs, four ordered checks and deciding verdict reason; verify rounded presentation, no recomputation and pass/fail/warning/source states.
- [ ] 3.4 Render engineer_formula and derived diagnostic refusal prefixes; verify no final pressure/bearing-success display, historical bound-refusal behavior, draft eligibility, correction/reveal actions and text/keyboard/reduced-motion accessibility.
- [ ] 3.5 Run frontend automated and browser acceptance; verify frontend/check.sh, >=95% branch coverage, Playwright type/form/result/report journeys, zero-contact/derived-refusal interactions and unchanged pilot journeys.
- [ ] 3.6 Obtain ui-ux-tester confirmation and separate tester GO; verify resolved visual/control/accessibility findings and current automated/browser evidence names the reviewed feature revision.

## 4. Review, integration and closure

- [ ] 4.1 Review complete backend after tester GO; verify all section-2 tasks complete, three admitted references, unchanged-pilot evidence and no open blocker/major/security finding.
- [ ] 4.2 With explicit consent, integrate reviewed backend into develop; verify actual integrated backend checks and source/pilot invariants with DB/catalog skips recorded separately.
- [ ] 4.3 Review complete frontend after tester GO and UI/UX confirmation; verify all section-3 tasks complete and compatibility with integrated backend.
- [ ] 4.4 With explicit consent, integrate reviewed frontend after backend; verify actual integrated frontend/browser checks and both type journeys without claiming skipped checks passed.
- [ ] 4.5 Complete actual-develop integrated acceptance; verify three admitted references through runner/API/DOCX, contact/sign/unit/rounding cases, unchanged pilot fixtures/reports, backend/frontend checks, Playwright and selected/all strict validation.
- [ ] 4.6 After accepted integration of both features, sync canonical specs and archive; verify no unchecked task, accurate verdict/skip records and final strict validation. Git actions retain their separate consent requirement.

## Dependencies

The six owner changes are archived and committed: retarget-mvp-domain,
calculation-core-contract, calculation-api, interim-normatives-source,
calculation-verification and frontend-app. Prepared P1b data and signed LOADS-DB-1
exist. No new data-pipeline feature or real-catalog promotion is required.

DOR requires the engineering contract, source locators, reference admission process
and current clean review. Actual admission of three full examples and numerical
tolerances remains an implementation/GO gate. Generator intervals or sampled inputs
do not establish a validated application range; later bounds need a separate
engineer decision supported by actual runs.

## DOR checklist

| Criterion | Required evidence |
|---|---|
| Complete artifacts | Proposal/design/specs/tasks and selected/all strict PASS |
| Current review | spec-reviewer reports no blocker or major on current artifacts |
| Engineering contract | Ordered inputs/units/ranges/signs, no duplicate weight, full-corner contact, outputs/checks and sources |
| Reference policy | Manual origin only for this type after Akim's check; no candidate/tolerance admission inferred; pilot unchanged |
| Explicit functional/non-functional scope | Pure deterministic unit-explicit engine; API/result compatibility; report/UI; existing applicable latency targets; safe formula execution; keyboard/text accessibility; >=95% branch coverage |
| Ready plan | Session-sized tasks, each code task in exactly one feature, tester GO and UI/UX gates |
| Dependencies | Canonical archives/source-evidence provenance and full MODIFIED reconciliation |

## Acceptance and Go/No-Go

Only tester declares GO per feature. Backend requires three admitted independent
full-type references (central, one-axis, biaxial), every expected output/check and
approved per-output tolerance provenance, executed through runner/API/DOCX. Agent
candidates or signed P1b formula points alone cannot meet this gate. Manual examples
are admissible only after Akim's check and admission record; the pilot keeps its
textbook policy. Never derive an oracle from this implementation or invent a tolerance.

Correctness evidence includes contact/sign/unit/rounding/check boundaries, registered
invariants with seeds, per-output deviation, reproducibility of 100%, traceability
completeness with engineer sources counted separately, and a frozen corpus with no
undeclared difference. NormRef status stays unchanged; human verification of a source
record does not make its normative reference verified. Initially validated_range=[]
and later bounds require an evidence-based engineer decision.

Both features require appropriate lint/type/tests and >=95% branch coverage. Frontend
also requires Playwright and ui-ux-tester confirmation. Existing applicable API/report
performance targets remain; no typical-calculation benchmark is invented here. Real
DB/catalog checks and every skip are reported separately. No security issue or
blocking UI defect may remain. DOD additionally requires reviewed integration of
both features, matching specs and archive. Checked planning tasks or structural
validation alone do not declare DOR, feature GO or calculation correctness.
