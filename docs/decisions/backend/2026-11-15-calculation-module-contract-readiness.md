# Calculation module contract readiness

## DOR, 2026-11-15

READY for the bounded backend feature. Working developer: Akim, confirmed in the
conversation and local checkout instructions. The approved implementation plan
requires a common protocol before pressure implementation.

Current independent spec-reviewer: 0 blockers, 0 major, 0 minor for both changes.
The contract is ready; pressure remains blocked by accepted contract integration.
Normative-attribution check: seven method-bearing pressure requirements UNVERIFIED,
no missing document/edition/clause, no blocker or major. The generic contract adds
no engineering formula, coefficient or limit. Attribution does not verify correctness.
Existing SP amendment and GOST edition discrepancies remain explicitly unverified;
pilot references and source statuses are unchanged.

Selected strict validation passes for both changes; all strict validation passes
22/22. Eight MODIFIED requirements retain all 32 original scenario headings. The
approved pressure reference document is byte-identical to HEAD. All functional,
non-functional, dependency, branch and acceptance criteria are recorded in tasks.

Baseline backend/check.sh passed: Ruff, mypy, five import contracts, 1430 tests,
11 skips and 100% reported branch coverage. The first sandbox run stalled at an API
test and was interrupted; the escalated rerun passed. Skips do not verify real
DB/catalog delivery. Six pre-change synthetic pilot results were captured for exact
post-change comparison; they are compatibility evidence, not independent norm oracles.

No feature GO, integration or archive is declared. No commit, merge or push is
authorized. Pressure implementation requires accepted integration and its renewed
readiness record. Code belongs on feature/calculation-module-contract/backend.

## Reviewed artifact identities

- `design.md`: `31602354e6d42bbe6427e1f5dfd3e252c7762e42545d54c9e71111c8bfc6f3cb`
- `proposal.md`: `3ead67223f3b6d28e792e7e9281764c67691d97279c9a73de92175e4a7a77103`
- `specs/calculation-engine/spec.md`: `dcdc568e885018207180f663009ef5804a374a23fb0512683c6503ca854544c9`
- `specs/calculation-module-contract/spec.md`: `6f76c111cf093cbe220d8794f29bbc95ab1fe0eab148380d2ce1c5f2a57ee6d5`
- `specs/calculation-verification/spec.md`: `dd993475df3ad66c02fee74bf763df0b3e51467de94f4eaaf2e07ffe9a9af245`
- `tasks.md`: `b29b9405c4837f75df7b6490cad7a70f5bc1989d7ac6414da9f77584ba3ce4bb`

## Backend acceptance and independent review, 2026-11-15

Tester GO for the current uncommitted backend feature. Independent architecture and
security review APPROVE after GO, with zero open blocker, major, minor or security
findings. Tasks 2.1-2.8 and 3.1 complete; progress 13/16. Actual integration,
pressure dependency confirmation and sync/archive remain open. No commit, merge
or push occurred. The full approved plan remains incomplete until pressure passes
its own implementation and acceptance after accepted contract integration.

Fresh backend/check.sh: Ruff PASS; mypy PASS (176 files); five import contracts
PASS; 1511 tests passed, 11 skipped, one existing httpx deprecation warning,
58.03 seconds, Hypothesis seed 2047857862. Coverage JSON records 674/674 actual
branches covered (100%). Changed application files: module executor 60/60,
module schemas 22/22, legacy adapter 10/10, pipeline 2/2, registry 4/4, pilot 6/6,
service 6/6. All changed-file branches are covered. 81 new tests cover structured
inputs, strict revalidation and bypasses, aliases/root models, state/diagnostic
invariants, identity precision and settings, isolation, source accounting,
registration, historical stored results and DOCX, and catalog snapshot refusal.

API schema drift check PASS without changing generated types. Six complete pilot
results match the captured pre-change outputs, hashes, sources and traces exactly.
Original golden fixtures, parameters, interim source data and approved pressure
references are unchanged. Historical results render from storage without calling
the engine. The existing 200-step DOCX timing test passed its 60-second target.
UI/UX: N/A because the public schema and interface are unchanged.

Preserved admitted pilot example via strict interim source: R=206.16 kPa,
expected 206.16 kPa, deviation 0.0 kPa, absolute tolerance 0.005 kPa; two identical
serialized runs, reproducibility 1/1=100%; normative traceability 0/9, one engineer
source. This is preservation evidence, not new methodology verification or three
complete examples of every type. Pressure example execution is still pending.

Real DB/catalog skips: calculation_result_postgres, normatives_postgres and
catalog_ingested module-level skips; one catalog_fixture postgres check; seven
verification_catalog_properties cases. DEC_TEST_APP_DATABASE_URL,
DEC_TEST_NORMATIVES_DATABASE_URL and DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL
are unset. The DB-backed median API timing benchmark was therefore skipped.
Neither a real catalog run nor DB API timing is claimed.

Both selected strict validations PASS; all strict validation 22/22; whitespace
checks PASS. The sandbox baseline stalled at an API test and Node schema generation
encountered EPERM; authorized escalated runs passed. The first implementation suite
found catalog snapshots incorrectly rejected before bound refusal. The legacy-only
fix validates snapshots strictly, requires an actual method refusal, preserves the
old hash, and is covered by the final fresh run. Review findings on ignored extras,
alias/root revalidation and v1 identity enforcement are resolved and regression tested.
The runtime dependency now explicitly requires pydantic>=2.12,<3; installed 2.13.5
satisfies it without installation.

### Accepted source identities

- `backend/app/schemas/module.py`: `9e58b2ea3d61f9d873030fd3b2c7c47267bc05636502a37b7212a14a02abc93b`
- `backend/app/engine/module.py`: `672005d57dc5b0b42fbf84524a8c672c3ae5209fe98748f01f27d3de8056e946`
- `backend/app/engine/legacy_module.py`: `7218ed0c7744e2ec91c0f67e8ce3c637b62e150c862a68cc572ed57b1203f1da`
- `backend/app/engine/pipeline.py`: `269a11cbc02c6a1fe5c28351fcf810964e593d9a17c4b3535282e6325de0e2b8`
- `backend/app/engine/registry.py`: `6b09637fe1bfc3e4b0abaa0613a868f96346d9de4f970f56fde28c7f4350e8fd`
- `backend/app/engine/foundations_shallow_r.py`: `df129ef5547aeffd1508fd8d5393ab89c78560e4220863c5bc9cd43df6391544`
- `backend/app/services/calculation.py`: `e8f3e20a6620a50543615bb0205c03a2a1ecb1e138b7ffa1ae0a3d42a610a8d2`
- `backend/requirements.txt`: `fc7f03e89b98e7cb64838be7c6928603b36cb3e69e1698b08b56743901c28100`
- `backend/tests/test_engine_modules.py`: `36f84bd5120f476e5947c2b15c3c71fee9912ee433dcaf22b35c2f9e509be055`
- `backend/tests/test_module_compatibility.py`: `1a189b0cc2e7a4434b39ad3f359adbacb56f891488619072ff04cbbaf4edee94`

## Orchestrator review, 2026-11-15

REQUEST CHANGES. Current integration is not approved: 0 blockers, 1 major,
0 minor. This review supersedes the earlier clean implementation-review status
for integration. The prior tester GO, test counts and coverage remain historical
acceptance evidence; they do not resolve the finding below. Planning DOR remains
valid because the requirements already demand strict result validation.

### Major: non-strict shared outcome validation

At backend/app/engine/module.py:100, AnyModuleOutcome.model_validate(_contents(raw))
does not request strict validation. Inputs, data, options, outputs and diagnostic
details use strict schema validation, but shared trace/check/warning fields do not.
Read-only probes with the existing synthetic module and bypass-constructed values
confirmed that CheckStep.passed="false" in trace and checks is accepted as False,
and a trace QuantityValue.value=True is accepted as 1.0. Malformed module output
can silently change engineering evidence instead of raising CalculationError.
This violates task 2.1 and the existing malformed-return rejection requirement.

Closure requires strict revalidation of the entire shared outcome, regression tests
for both primitive-type cases, fresh relevant checks and tester acceptance, and
independent re-review with unchanged legacy pilot compatibility. Tasks 2.1, 2.2,
2.8 and 3.1 are reopened; current progress is 9/16. Pressure task 1.9 remains
blocked pending accepted contract integration. No implementation fix was made in
this review pass.

The orchestrator independently confirmed all ten recorded source/test hashes,
674/674 covered actual branches and the listed changed-file counts. Golden
fixtures, parameters, interim data, generated API types and approved pressure
references are unchanged. Generic/domain separation, legacy identity and snapshot
refusal otherwise match the approved scope. Real DB/catalog and DB API timing
remain unverified. No broad suite rerun or Git mutation was performed by the
reviewer. Commit, merge and push remain unauthorized.

## Strict outcome correction accepted, 2026-11-15

The orchestrator major is CLOSED. Fresh tester GO followed by orchestrator
APPROVE on the corrected source supersedes the preceding REQUEST CHANGES status.
Open findings: 0 blockers, 0 major, 0 minor. Tasks 2.1, 2.2, 2.8 and 3.1 are
complete again; current progress 13/16. Integration, pressure dependency
confirmation and sync/archive remain open and require their own gates.

The single executor correction replaces the non-strict shared-outcome call with
_validated(TypeAdapter(AnyModuleOutcome), raw). The whole outcome now receives
strict nested validation, forbidden-extra enforcement and the same alias/name
handling as the other typed boundaries, before external adaptation. No public
schema, formula, coefficient, reference value, tolerance or legacy hash changed.

Seven new regressions reject string check results, boolean trace quantities,
boolean substitutions and comparison operands, boolean warning quantities,
string bound inclusivity and list-valued normative-reference containers. The
previous behavior was reproduced in memory with no source rollback: all seven
regressions failed under that behavior and pass with the correction. Tests also
ensure malformed outcomes never reach external adaptation. Independent reviewer
probes confirm both originally reported cases now raise CalculationError and a
valid typed run still completes.

Fresh backend/check.sh PASS: Ruff, mypy (176 files), five import contracts,
1518 passed, 11 skipped, one existing httpx deprecation warning, 57.26 seconds,
Hypothesis seed 302677009. Coverage JSON at
/tmp/dec-module-contract-strict-outcome-coverage.json records 674/674 actual
branches covered, 100%. Changed-file branch counts remain executor 60/60,
schemas 22/22, legacy adapter 10/10, pipeline 2/2, registry 4/4, pilot 6/6 and
service 6/6. All 88 feature regression/compatibility cases pass, including the
seven added for this correction.

Six complete pre-change pilot cases match again: pass, fail, wide footing, unit
conversion, validated-range warning and method refusal. Existing golden, API,
storage, historical DOCX, admitted pilot ex1 and 200-step DOCX timing checks pass.
Golden fixtures, parameters, interim data, generated API types and approved
pressure references are unchanged. Fresh API schema drift PASS; both selected
strict validations PASS; all strict 22/22; whitespace PASS.

The same 11 DB/catalog skips remain: three module-level skips, one catalog fixture
check and seven catalog property cases. All three DEC_TEST_*DATABASE_URL settings
are unset. Real DB/catalog behavior and DB-backed API timing remain unverified.
UI/UX: N/A because public schemas and interface are unchanged.

The orchestrator re-reviewed the fix after this fresh tester GO and confirmed the
accepted hashes below. The earlier test/review entries remain historical evidence.
No commit, merge or push occurred. Pressure task 1.9 remains blocked pending
accepted contract integration; no pressure implementation is claimed.

### Corrected source identities

- `backend/app/engine/module.py`: `c4655444c36bb50d174e081f28a49d9b04eac9044d03bf8f644a30684188485c`
- `backend/tests/test_engine_modules.py`: `b6cd720e9a190f6ad0ffcced1c62673f639b131c8775c478b1a319b1664f6a3d`

The other eight source/test identities in the earlier acceptance record are unchanged.


## Accepted develop integration, 2026-11-15

Tester GO for actual integrated develop at `cd204c5`. Akim explicitly requested
integration and verification in the conversation. Merge parents are `c686ad8`
(develop) and `a081a0d` (feature, including accepted code `9bd6b45`); no conflicts.
Required fetch and fast-forward pull completed before merge. The merge adds exactly
the ten accepted backend files. Application directories are byte-identical to the
accepted feature code, so the recorded orchestrator APPROVE covers this code.

Fresh backend/check.sh PASS: Ruff, mypy (176 files), five import contracts,
1518 passed, 11 skipped, one existing httpx deprecation warning, 55.89 seconds;
Hypothesis seed 3475109852. Coverage with backend configuration: 674/674 actual
branches and 3454/3454 lines covered, 100%. Changed-file branch counts remain
60/22/10/2/4/6/6 for executor/schemas/legacy adapter/pipeline/registry/pilot/service.
API schema drift PASS. Selected strict validation PASS; all strict validation
23/23. Fixtures, parameters, interim sources, approved pressure references and
generated API types are unchanged. Compatibility/reference and historical DOCX
checks are included in the fresh suite; no new methodology is admitted.

The same 11 DB/catalog skips remain: three module-level skips, one catalog-fixture
check and seven catalog-property cases. All three DEC_TEST_*DATABASE_URL settings
are unset. Real DB/catalog behavior and DB-backed API timing remain unverified.
UI/UX: N/A because no UI or public schema changed.

The initial API schema attempt hit sandbox spawnSync EPERM. The successful
parent-run escalated retry returned exit 0 and is the execution evidence accepted
by the tester; the earlier aborted approval-wait retry is not a passing check.
Coverage JSON was exported from backend so its configured exclusions apply.
Check log and configured coverage JSON are local temporary evidence; this record
retains the verdict and totals independently of those temporary files.

Tasks 3.2 and 3.3 are complete; progress 15/16. Accepted dependency and renewed
pressure DOR are recorded in the paired pressure readiness files. Pressure
implementation and its own GO are not claimed. Task 3.4, spec synchronization and
archive, remains open. This local merge is not published to origin/develop;
no additional documentation commit or push was performed in this integration step.

Final integration-document review: 0 blocker, 0 major, 0 minor. Paired readiness,
renewed pressure DOR, task states, local index and journal are consistent with the
actual merged revision and tester GO. Targeted document hooks PASS (detect-secrets);
settings-example hook skipped because no matching file changed. Post-record
selected strict validation and whitespace checks PASS. No source edits followed GO.
