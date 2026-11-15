# Tasks

Owner: Akim (backend).
Planning documents belong on develop. Every code task belongs to the single backend
feature; each task states a bounded deliverable and verification. Checked tasks are
evidence only for the work described, not consent to commit, merge or push.

| Feature | Branch | Owned tasks | Dependency |
|---|---|---|---|
| Calculation module contract | `feature/calculation-module-contract/backend` | Section 2: neutral schemas, executor, identity, trusted registry, internal source helpers, legacy adapter/wiring and backend verification | Current reviewed DOR from section 1 |

Sections 1 and 3 contain documentation, review and execution of existing checks.
There is no frontend feature. The public R schema stays unchanged; pressure public
schema/rendering extensions belong to `foundations-pressure-from-loads`.

## 1. Agree the bounded contract

- [x] 1.1 Record proposal, design, three delta specs and feature tasks; verify actual engine boundaries and complete MODIFIED scenario preservation against canonical specs.
- [x] 1.2 Reconcile pressure artifacts to depend on accepted integration of this change and transfer shared mechanism ownership; verify its formulas, signs, inputs, approved references/tolerances and source identities are unchanged.
- [x] 1.3 Obtain current spec-reviewer and normative-attribution reviews for both revised changes; verify no blocker/major finding, no invented coefficient/source/tolerance and selected/all strict validation passes.
- [x] 1.4 Record DOR on current artifact versions; verify every checklist criterion below before creating implementation code.

## 2. Backend feature

- [x] 2.1 Add internal module metadata, typed outcome/diagnostic and engineer_formula schemas; verify state/stop-stage combinations, strict nested validation, independent checks, unique step identifiers and invalid diagnostic references without changing public OpenAPI.
- [x] 2.2 Add pure generic execution and trusted startup registration; verify structured model execution, duplicate/unknown registration, schema validation before/after normalization, module diagnostic validation and malformed returns failing before adaptation.
- [x] 2.3 Add versioned new-module run identity and explicit legacy identity support; verify normalized-equivalence, key order independence, sequence-order preservation, exact adjacent integers above 2**53, explicit int/float distinction, string-only object keys, metadata/source/options sensitivity and rejection of unsupported/non-finite values against unchanged pilot hashes.
- [x] 2.4 Add shared internal engineer-step/source accounting and normative metrics; verify disjoint source fields, first-use deduplication, engineer exclusion from normative counts/ratios and zero denominator as N/A without changing pilot metrics.
- [x] 2.5 Add the R compatibility module and reconnect pipeline/registry callers; verify original calculator/helpers remain in use, complete golden corpus and trace/check/source/hash equivalence, preflight bound refusals and unchanged fixture files.
- [x] 2.6 Verify execution isolation and extension using synthetic typed modules; exercise no I/O, repeated/interleaved determinism, caller mutation protection, early and later stops, wrong output/details schemas and no domain branches or executor edits for module registration.
- [x] 2.7 Verify existing API/storage/DOCX compatibility; run existing schema drift, API and report checks, retrieve historical payloads and render them without recomputation, and confirm source-label/digest and public schema equivalence.
- [x] 2.8 Obtain tester acceptance for the complete backend feature; verify backend/check.sh passes with >=95% branch coverage, unchanged independent pilot reference/corpus checks, selected/all strict validation and actual database/catalog checks or explicit skips.

## 3. Review and integration

- [x] 3.1 Obtain independent review after tester GO; verify all section-2 tasks complete, no blocker/major/security finding, exact pilot compatibility evidence and no public-schema or frontend scope expansion.
- [x] 3.2 With separate explicit Git consent, integrate the accepted feature into develop; verify actual integrated backend and API schema checks, compatibility evidence and accurate database/catalog skips.
- [x] 3.3 Record accepted contract integration in the pressure readiness record; verify both its backend/frontend dependencies name the actual integrated contract and pressure implementation may start without executor edits.
- [ ] 3.4 After accepted integration, synchronize specs and archive this change; verify no unchecked task remains, the delta matches implementation and strict selected/main/all validation passes.

## Dependencies

The current canonical calculation-engine, calculation-verification, calculation-api
and report-generator requirements and integrated R implementation are the baseline.
The prior core/API/verification/frontend/interim changes are archived; current
`foundations-pressure-from-loads` is a dependent consumer, not a prerequisite.
No source-record change, database migration, data-zone feature or package installation
is required. No downstream pressure engineering decision is implied by this contract.

## DOR checklist

| Criterion | Required evidence |
|---|---|
| Complete artifacts | Proposal/design/three deltas/tasks exist; selected/all strict validation passes |
| Current review | Current spec-reviewer has no blocker/major; normative attribution covers changed calculation requirements |
| Bounded protocol | Typed models/options, state table, source/diagnostic validation, versioned identity and legacy compatibility are observable scenarios |
| Plan | One named backend branch, session-sized deliverables, explicit dependencies, tester and review gates |
| Non-functional scope | Pure isolated execution, strict schemas, existing performance/security/layer constraints, unchanged UI/schema accessibility scope, >=95% branch coverage |
| Ownership reconciliation | Pressure retains domain rules and approved engineering evidence, shares no generic mechanism ownership and waits for accepted contract integration |

## DOD and Go/No-Go

Only tester declares feature GO. GO requires all section-2 tasks complete, passing
lint/type/import/tests and >=95% branch coverage, exact pilot regression/source/hash
compatibility, historical saved-result/report checks, public schema drift checks and
current strict OpenSpec validation. Generic execution tests cover isolated calls,
structured models, stop stages, impossible states, details schemas and identity.
UI/UX is N/A because this feature changes no UI; public schema or required frontend
changes are a scope-resolution gate rather than an unreviewed exception. Real DB
and catalog checks must be named as executed or skipped; skips never prove delivery.

No known security issue or open blocker/major may remain. An altered fixture,
pilot expected value, source identity or tolerance cannot be used to obtain GO.
Review and accepted integration precede pressure implementation. DOD additionally
requires all tasks complete, matching canonical specs and archive after integration.
The overall approved plan is not complete until pressure executes through this
contract without an executor edit and its separate feature acceptance gates pass.
