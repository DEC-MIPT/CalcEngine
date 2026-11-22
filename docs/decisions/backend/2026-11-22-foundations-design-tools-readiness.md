# Foundation design tools readiness

## Current verdict

READY for backend implementation under the dated DOR record below. Backend
implementation and acceptance are active; feature GO remains pending. Frontend
implementation waits for its recorded predecessor integration. Earlier dated
entries retain their approval scope at the time they were recorded.

## Confirmed scope, 2026-11-22

Akim confirmed the prior recommendation to preserve averaged weight accounting,
clarify load semantics and add an explicit-weight alternative, then requested load
schematics, a pressure diagram and size selection analogous in function to the
competitor service. The consent concerns capabilities, not competitor constants,
a load-factor conversion, undisclosed geometry assumptions or reference admission.
See the existing pressure-source audits and Russian frontend journal.

The proposed change is [foundations-design-tools](../../../openspec/changes/foundations-design-tools/proposal.md).
Its design proposes a separate registered explicit-weight type, signed added
base moments and fixed upper-cut structural-load semantics; those detailed fields
remain pending approval. Initial candidate search is proposed for averaged weights
only, using an engineer-supplied finite list. Fixed explicit weights are not reused
while dimensions change. Diagram data come from stored backend results; the
frontend performs presentation transformations only. Legacy identities remain.

## Decisions and dependencies before DOR

The owning [design questions](../../../openspec/changes/foundations-design-tools/design.md)
and [tasks](../../../openspec/changes/foundations-design-tools/tasks.md) retain the
exact weight/moment contract, candidate objective/tie policy, technical caps and
API/persistence behavior, independent references/tolerances and predecessor gates.
The prior loads frontend remains unmerged and its browser-matrix NO-GO is not waived.
Existing uncommitted expanded-default trace work remains in its owning feature.

The feature branches are proposed, not created: feature/foundation-design/backend
and feature/foundation-design/frontend. The frontend waits for accepted predecessor
integration. No shared executor change, deployment, new coefficients or code changes
were made. No commit, merge, push or migration was performed. A later implementation
request follows completion of the recorded DOR decisions and current review.


## Engineering scope confirmation, 2026-11-22

Akim answered "Подтверждаю" to the concrete proposed initial contract in the
working conversation: named foundation/soil/other weights with additional moments
for one fixed geometry, and averaged-mode-only selection from an explicit engineer
candidate list by minimum passing area. This confirms those scope choices. It
does not approve competitor constants, automatic reuse of fixed weights across
candidates, a base-level structural-load variant, numerical reference tolerances,
a tie policy, technical limits or Git publication. Final sign/load-plane validation,
API details, reference admission and applicable predecessor gates remain before DOR.


## Candidate-policy confirmation, 2026-11-22

Akim explicitly confirmed both explained points: equal-minimum-area ties select
the first passing candidate in submitted order, and each request accepts at most
256 candidate rectangles. The cap is technical, not a dimensional or normative
limit, and requires workload verification. Oversized lists are rejected in full
before evaluation; they are not truncated. The entire candidate order is retained.
The earlier architect proposal of 128 candidates is superseded by this explicit
256-candidate decision. Task 1.1 is complete. Reference and sign/load-plane
approvals remain pending; this confirmation does not declare DOR or feature GO.


## Central reference review, 2026-11-22

Akim explicitly answered "weights-C подтверждаю" after receiving the complete
central inputs, geometry, weight sum, pressure values, R/check limits and old-mode
equivalence. Only weights-C is confirmed; weights-X, weights-XY, the new-type
manual-origin exception and output tolerances remain pending. The reference
document records the scoped review and arithmetic digest. Task 1.4 and DOR remain
open. No source status, code or Git publication changed.


## One-axis reference review, 2026-11-22

Akim explicitly confirmed weights-X after its step-by-step input, signed-transfer,
pressure and check presentation. The reference document records the scoped
approval and arithmetic digest. weights-C and weights-X are reviewed; weights-XY,
the new-type manual-origin exception and output tolerance approval remain pending.
Task 1.4 and DOR remain open. No code or Git publication changed.


## Two-axis reference review, 2026-11-22

Akim explicitly confirmed weights-XY after the complete signed-moment, corner,
contact and bearing-check presentation. All three proposed derivations are now
engineer-reviewed, with scoped arithmetic digests in reference-candidates.md.
The manual-origin exception for this new type and the per-output tolerance
decision remain pending. No reference is fully admitted and task 1.4/DOR remain
open until those decisions and current review are recorded. No code or Git action.


## Final manual-reference admission, 2026-11-22

Akim stated "Ручные эталоны и допуск 0,005 кПа подтверждаю" after separately
confirming weights-C, weights-X and weights-XY. The three full manual references
are admitted for foundations_shallow_weights, with absolute 0.005 kPa per R/pressure
output. The final reference record pins the reviewed arithmetic and expectations
to a SHA-256 digest. Their reviewed cut/base signs and one-time load assembly
form the new type's contract; no automatic base-load variant is inferred. Tasks
1.2 and 1.4 are complete. Runner/API/DOCX and current API/spec review remain
implementation/readiness gates. No code, coefficients, old reference or Git action changed.


## Positive-resultant decision, 2026-11-22

Akim confirmed the proposal that foundations_shallow_weights requires N_base>0,
and N_base<=0 is invalid_input before calculation, regardless of moments. The
new rule is engineer-defined, names the contributing inputs and prevents undefined
eccentricity. No zero-pressure exception or new base-load variant was approved.
Historical averaged calculations remain unchanged. The major review finding is
addressed in the engine delta and design; current re-review remains required.


## Backend DOR recorded, 2026-11-22

READY for backend implementation of foundations-design-tools. The positive-resultant
major and stale-approval minor are closed; current spec-reviewer reports zero
blocker, major and minor. Current source traceability reports four UNVERIFIED
normative requirements plus one engineer-sourced restriction, with zero missing
locators and no source promotion. Selected/all strict validation passes, 25/25.
Akim has approved the input assembly, three complete manual references and absolute
0.005 kPa output tolerances, first-input equal-area ties, 256-candidate cap and
N_base>0. The API unit-of-work, cancellation and technical budgets are recorded.

Reviewed pressure backend integration 2a401c5 is an ancestor of develop 6269bae;
the generic executor remains unchanged. Tasks 1.3, 1.5 and 1.6 complete readiness.
Only the backend feature may start. Section 3 still waits for accepted predecessor
frontend integration and this feature's reviewed backend contract. GO, runtime
correctness execution, database/catalog checks, commit, push and merge are not
implied by DOR. The existing dirty trace files are preserved in their own checkout.

## Backend acceptance in progress, 2026-11-22

The backend feature is implemented in its separate worktree and remains uncommitted.
The explicit-weight contract passes 22 focused tests, and 130 focused legacy
engine/source/API tests pass. The first full suite reports 1704 passed, 12 failed
and 11 skipped; aggregate coverage is 98.65%. This is a failed acceptance run.
The new search/context code still requires its own changed-code coverage check.

Review identified inconsistent area ordering after float unit normalization.
The service and DTO must share exact decimal area comparison before that major
finding can close. Full-suite findings also cover report assertions, registered-type
verification and the requirement to reject a missing repository before engine execution.
Corrections require a fresh full run and independent review.

No DEC_TEST_APP_DATABASE_URL, DEC_TEST_NORMATIVES_DATABASE_URL or
DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL is configured in this session.
Production PostgreSQL migration and catalog behavior remain unverified.
The Russian execution journal owns detailed checks and limitations:
[backend journal](../../akim/reports/foundations-design-tools-backend-code-journal.md).

## Backend verification update, 2026-11-22

The corrected backend passes `backend/check.sh`: Ruff, mypy, import-linter and
1753 pytest tests pass. Eleven PostgreSQL-dependent tests skip because the three
DEC_TEST database variables are unset. Combined coverage is 99.89%; branch
coverage is 99.49% (971/976), above the 95% gate. The focused backend
design-tool acceptance has 133 passing tests.

The exact-decimal area comparison now selects the first submitted candidate for
equal physical areas across units. Isolated SQLite migration upgrade, downgrade
and re-upgrade pass. The measured 256-candidate request takes 2.845036 seconds
including SQLite persistence and response serialization on i7-13700KF, WSL2 and
Python 3.12.3. This measurement is a local technical observation.

DOCX artifacts for selected, explicit, refused and no-winner outcomes were
rendered to PDF. The refused report page was inspected and had no clipping.
The API, persistence, context and reporting reviews have no remaining blocker
or major finding. The tester issued GO for the backend feature. PostgreSQL
migration and catalog integration remain unverified and are recorded as
environment-dependent skips. Orchestrator review and integration into `develop`
passed with no blocker, major or security finding. Integration into `develop`,
commit and push remain pending explicit consent.
