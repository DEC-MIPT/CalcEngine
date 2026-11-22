# Tasks

Owner: Akim. The revised plan consumes calculation-module-contract before pressure
implementation. The DOR recorded on 2026-11-14 is historical for the prior design.
Planning documents belong on develop. Every later code task belongs to exactly one
feature below; each has a bounded deliverable and verification for one session.

| Feature | Branch | Owned tasks | Dependency |
|---|---|---|---|
| Backend | `feature/foundations-loads/backend` | Section 2: engine, parameters/data, schemas, API, DOCX and backend verification | Integrated calculation-module-contract and renewed DOR from section 1 |
| Frontend | `feature/foundations-loads/frontend` | Section 3: form, diagram, results/trace/refusal UI, mocks, generated API types and browser tests | Integrated calculation-module-contract and backend's reviewed typed contract; branch from backend when its unmerged code is needed |

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

- [x] 1.7 Reconcile the revised plan with calculation-module-contract; verify exclusive ownership of generic executor, internal trace/diagnostic/status/identity and metrics infrastructure, unchanged approved engineering inputs/sources/references/tolerances, and both strict validations.
- [x] 1.8 Obtain fresh spec-reviewer and norm-traceability-checker reviews of the revised artifacts; verify no blocker/major and preserve the previous review as historical evidence only.
- [x] 1.9 Confirm tester GO, review and actual develop integration of calculation-module-contract, then record renewed DOR on the current pressure artifacts; verify the shared executor is available before starting section 2.

## 2. Backend feature

- [x] 2.1 Add loads moment/volume units and public foundation adapter/schema variants for engineer_formula and kind=derived using the integrated internal primitives; verify module detail validation, unit conversions, API round trips, historical steps/envelopes/input-bound refusal shapes and internal volume separately from actual force/moment API inputs. Do not change the shared executor.
- [x] 2.2 Extract reusable R and reconnect the pilot; verify unchanged step order/IDs, deciding check, numeric result, saved envelope and original golden fixture without rewriting it.
- [x] 2.3 Implement pure geometry and signed transfer with engineer rules; verify A/Wx/Wy, M+Q*h signs, cancellation, h=0, equivalent units and pressure-module axis interchange.
- [x] 2.4 Implement mean, axial extrema and four signed corner pressures from resolved data; verify central equality, biaxial sign patterns, deterministic unrounded results and existing typed error handling for non-finite intermediates.
- [x] 2.5 Implement contact refusal before four ordered bearing checks; verify p_min=0 allowed, negative corner with nonnegative axial minima, diagnostic prefix without final outputs/bearing conclusions, each isolated check failure, limiting_corner first-tie selection and first-fail/last-pass reason.
- [x] 2.6 Register the fifteen-input/ten-output typed module, its diagnostic-detail validator, versioned run identity, engineer parameters, validated_range=[] and explicit prepared-record alias; verify b<=l, all approved ranges, exact degree rows, independent d/h/d_1, no swapping/interpolation and unchanged catalog/pilot selection.
- [x] 2.7a Install the separate loads-only prepared d_b-bound supplement from signed LOADS-DB-1; verify inclusive bound loaded from data, source/evidence digest match, rejection rather than clamping and unchanged original document records/statuses.
- [x] 2.7b Bind the supplement only to this type and implement its allowlisted aggregate source digest; verify canonical constituent order, change on either constituent, fail-closed missing/unusable components, unchanged envelope label shape and pilot digest.
- [x] 2.8 Connect existing API routes and immutable storage; verify metadata order, complete/derived-refused POST and GET envelopes, source kind/profile/digest, old result retrieval and no new endpoint.
- [x] 2.9 Render loads DOCX inputs, directions, sources, diagnostic/calculation traces and checks; verify pass/fail/refused document content and unchanged meaning of historical pilot reports.
- [x] 2.10 Import approved central reference C and its recorded per-output tolerance provenance into runner/API/DOCX fixtures; verify the 2026-11-14 approval and immutable independent derivation rather than values captured from this implementation.
- [x] 2.11 Import approved one-axis reference X and its recorded per-output tolerance provenance into runner/API/DOCX fixtures; verify the 2026-11-14 approval, signed transfer, every expected output/check and origin evidence.
- [x] 2.12 Import approved two-axis reference XY and its recorded per-output tolerance provenance into runner/API/DOCX fixtures; verify the 2026-11-14 approval, corner signs/minimum, every expected output/check and origin evidence.
- [x] 2.13 Run backend feature acceptance with tester; verify three admitted references through runner/API/DOCX, invariants with recorded seeds, metrics/reproducibility, frozen regression including unchanged pilot, backend/check.sh and >=95% branch coverage. Record actual DB/catalog checks or skips separately; only tester declares GO.

## 3. Frontend feature

- [x] 3.1 Regenerate API types and extend fixtures/mocks for both types and refusal variants; verify schema drift checks, historical fixtures and source-label rendering.
- [x] 3.2 Add type selection, fifteen labeled inputs and accessible direction/sign diagram; verify d/h/d_1 and N explanations, whole-degree behavior, correction feedback and keyboard/small-screen use without changing entered values.
- [x] 3.3 Display ten outputs, four ordered checks and deciding verdict reason; verify rounded presentation, no recomputation and pass/fail/warning/source states.
- [x] 3.4 Render engineer_formula and derived diagnostic refusal prefixes; verify no final pressure/bearing-success display, historical bound-refusal behavior, draft eligibility, correction/reveal actions and text/keyboard/reduced-motion accessibility.
- [x] 3.5 Run frontend automated and browser acceptance; verify frontend/check.sh, >=95% branch coverage, Playwright type/form/result/report journeys, zero-contact/derived-refusal interactions and unchanged pilot journeys.
- [x] 3.5a Group recognized loads traces with initially expanded step details and contiguous headings inside the existing flat ordered list; verify conservative complete typed-step signature recognition, flat expanded fallback for incomplete/unrecognized traces, all stored steps/order/anchors/results/sources retained, neutral unknown supplemental steps, keyboard/global disclosure, original-index playback/ruler behavior, immediate derived diagnostics and unchanged expanded pilot. Run frontend checks with >=95% branch coverage and focused browser/UI acceptance; bind fresh evidence to the changed revision.
- [x] 3.6 Obtain ui-ux-tester confirmation and separate tester GO; verify resolved visual/control/accessibility findings and current automated/browser evidence names the reviewed feature revision.

## 4. Review, integration and closure

- [x] 4.1 Review complete backend after tester GO; verify all section-2 tasks complete, three admitted references, unchanged-pilot evidence and no open blocker/major/security finding.
- [x] 4.2 With explicit consent, integrate reviewed backend into develop; verify actual integrated backend checks and source/pilot invariants with DB/catalog skips recorded separately; verify shared executor hashes match the integrated contract revision.
- [x] 4.3 Review complete frontend after tester GO and UI/UX confirmation; verify all section-3 tasks complete and compatibility with integrated backend.
- [x] 4.4 With explicit consent, integrate reviewed frontend after backend; verify actual integrated frontend/browser checks and both type journeys without claiming skipped checks passed.
- [x] 4.5 Complete actual-develop integrated acceptance; verify three admitted references through runner/API/DOCX, contact/sign/unit/rounding cases, unchanged pilot fixtures/reports, backend/frontend checks, Playwright and selected/all strict validation.
- [ ] 4.6 After accepted integration of both features, sync canonical specs and archive; verify no unchecked task, accurate verdict/skip records and final strict validation. Git actions retain their separate consent requirement.

## Dependencies

The calculation-module-contract backend feature must first be accepted, reviewed
and integrated into develop with explicit Git consent. This dependency is satisfied by accepted develop integration `cd204c5`, recorded
in the 2026-11-08 pressure readiness file under "Integrated dependency and renewed
DOR, 2026-11-15"; both feature rows above refer to this revision. It owns
the common executor, typed module protocol, internal state/diagnostic/trace and
versioned identity mechanisms, plus generic source metrics. This pressure change
owns only domain implementation, public foundation adaptation and presentation.

The six earlier owner changes are archived and committed: retarget-mvp-domain,
calculation-core-contract, calculation-api, interim-normatives-source,
calculation-verification and frontend-app. Prepared P1b data and signed LOADS-DB-1
exist. No new data-pipeline feature or real-catalog promotion is required.

Renewed DOR requires the engineering contract, source locators, reference approval
provenance, current clean review and integrated module-contract dependency. C, X
and XY and absolute 0.005 kPa per-output tolerances were approved on 2026-11-14;
actual runner/API/DOCX execution remains an implementation/GO gate. Generator intervals or sampled inputs
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
| Dependencies | Integrated calculation-module-contract with tester GO/review; canonical archives/source-evidence provenance and full MODIFIED reconciliation |

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

Connecting the pressure module SHALL leave the shared executor unchanged, verified
against the integrated module-contract revision. A necessary executor change exposes
a contract gap and stops pressure integration until that contract is revised.

Both features require appropriate lint/type/tests and >=95% branch coverage. Frontend
also requires Playwright and ui-ux-tester confirmation. Existing applicable API/report
performance targets remain; no typical-calculation benchmark is invented here. Real
DB/catalog checks and every skip are reported separately. No security issue or
blocking UI defect may remain. DOD additionally requires reviewed integration of
both features, matching specs and archive. Checked planning tasks or structural
validation alone do not declare DOR, feature GO or calculation correctness.

## Compact trace follow-up readiness and acceptance

The user requested a more compact trace in the working conversation on 2026-11-18
and explicitly required all steps expanded by default on 2026-11-22.
Task 3.5a refines presentation inside the existing frontend feature and branch; it
changes no calculation method, source contract or backend ownership. Proposal,
design and transparent-output delta define the bounded deliverable. Implementation
requires strict validation and a current spec-reviewer report without blocker or
major findings on these revised artifacts. Prior DOR/reviews remain evidence for
unchanged scope, not approval of the new presentation amendment.

Acceptance requires component coverage for initially expanded details in all traces,
including completed and derived-refused loads and the pilot, exact original step sequence and stable indices, complete typed
signature recognition without values/expression heuristics, flat expanded fallback
for absent/duplicate/wrong-kind signature members, unknown supplemental steps and
missing non-signature group members, individual/global keyboard disclosure, unchanged stored
field rendering, refusal immediacy and original-index playback/ruler navigation.
Browser/UI checks cover completed and derived-refused loads at desktop and 320 px,
readable MathJax on initial reveal and after reopening, no horizontal overflow, accessibility and
reduced motion, plus the historical pilot. Existing safe rendering, performance
and >=95% branch coverage gates continue to apply.

Historical task 3.5 acceptance is preserved for its recorded revision. Changed UI
requires fresh automated/browser evidence and UI/UX confirmation before task 3.6
can name the new reviewed revision. The existing full-browser compatibility
requirement and recorded NO-GO are unchanged; this follow-up grants no browser
scope waiver or whole-feature GO. Only tester declares the final feature verdict.
