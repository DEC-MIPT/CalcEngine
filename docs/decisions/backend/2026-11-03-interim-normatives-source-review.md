# CH1 feature review

- Date: 2026-11-03
- Owner: Akim; task 9.3 of `interim-normatives-source`.
- Backend reviewed: `82c092d459bcea2c45cf8f1bc30112af075534e6`.
- Frontend reviewed: `a8fb64e5678420eceb084f5db325809854de4941`.
- Integration base: develop `f401a61`.
- Russian version: `2026-11-03-interim-normatives-source-review-rus.md`.

## Verdict

Backend: **REQUEST CHANGES**, one P2 requirement-compliance finding below.
Frontend: **APPROVE**, no findings. Independent security/data-integrity review
found no additional actionable defects. This review does not replace tester
verdicts or complete task 9.3, which also requires approved merge and checks on
develop. No merge, commit, push or source fix was performed.

## P2: Require a source page on every interim record

At backend `82c092d`, `backend/app/parameters/interim_schemas.py:133` declares
`page: int | None` with a None default. Lines 136-139 require a page only for
human-verified records. An independent loader reproduction on the exact snapshot
accepted a pending formula without page, producing `page=None`.
`backend/tests/test_interim_schemas.py:133` explicitly permits this behavior in
`test_a_pending_record_needs_no_verifier_fields_and_no_page`.

The current requirement "Interim normative data files" requires page on every
record (`openspec/changes/interim-normatives-source/specs/interim-normatives/spec.md:16`).
Design decisions 2 and 9 also require page; no waiver was found in readiness.
Draft mode can therefore consume normative records without the required page
provenance. The current 146 verified strict-pilot records have pages and are not
affected by this finding.

Require a positive page for every record, retaining the absence of verifier fields
for pending records. Update the test that permits missing page and check loader
rejection of missing page in pending/rejected records. Recheck affected digest and
profile tests; do not weaken the specification or modify signed data to pass tests.
Then obtain tester confirmation and re-review before merging backend.

## Review coverage

Backend review covered shared parameter assembly/catalog equivalence, source
selection, strict/draft grouping, status/digest handling, source propagation and
DOCX/accountability placement. Security review covered safe YAML, file/directory
symlink boundaries, sanitized errors and unchanged NormRef status/provenance.
Focused loader/schema/data/source tests on exact backend: 88 passed.

Frontend review covered all 10 changed files, source absent/null handling,
catalog/strict/draft labels, visible/accessibility digests, RU/EN strings, React
escaping and generated types. Backend application code is identical between the
frontend tip and accepted backend tip; the frontend predates later data/test
commits. The existing 9.2 browser/UI acceptance remains the behavioral evidence.

## Integration checks

Backend and frontend patches applied without conflicts to a temporary snapshot of
develop, in that order. Working branches and live services were not changed.
On that snapshot both check scripts passed using existing dependencies:

- Backend: Ruff/mypy PASS, five architecture contracts KEPT, 1338 passed,
  11 PostgreSQL checks skipped because test database URLs were not configured;
  branch coverage 100% (3154 statements, 580 branches), one existing warning.
- Frontend: API drift/ESLint/TypeScript PASS; 496 passed in 46 files;
  branch coverage 100% (634/634).

The branch diff whitespace check reports an extra blank line at EOF in
`backend/app/services/parameter_assembly.py:335`. This is a formatting observation,
not an additional behavioral finding. The shared-config questions to Egor in
`2026-10-28-shared-config-changes-to-egor.md` remain unanswered; this review does
not supply his acknowledgement.

Local logs: `/tmp/dec-ch1-integration-backend.log` and
`/tmp/dec-ch1-integration-frontend.log`; merged-tree simulation is in
`/tmp/dec-ch1-integration-review/`. Temporary artifacts are not shared deliverables.
These successful checks do not resolve the page-provenance finding, establish
normative correctness or replace post-merge checks on develop.

## Correction and re-review (2026-11-03)

The original P2 is **resolved** in the uncommitted working tree of
`feature/interim-normatives/backend`, based on `82c092d`. Independent backend
re-review: **APPROVE**, no blocker or major finding. Tester verdict: **GO** for
this correction. These results supersede the initial REQUEST CHANGES for P2;
commit and merge are still pending.

`_Record.page` is now a required integer >=1 for all five record kinds and every
verification status. The human-only page validator is removed. Regression tests
reject missing/null/zero/negative pages for all three statuses, and the loader
rejects pending/rejected records without page. Pending records still need no
verifier fields when page is present. The synthetic pending fixture has page 1.
The extra EOF blank line in parameter_assembly.py was also removed.

Full backend/check.sh: Ruff/mypy PASS, five architecture contracts KEPT,
1351 passed, 11 skipped, one existing warning; branch coverage 100%
(3149 statements, 578 branches). Both pre-commit hooks, strict CH1 validation
and whitespace checks passed. The PostgreSQL tests were skipped because test URLs
were not configured. UI/UX: N/A, internal schema correction. Strict ex1 passed.

All 146 signed records are unchanged and human-verified, with unchanged document
digest. Public OpenAPI is identical to accepted backend `82c092d` (SHA-256
`6b44f2378bbb42397eb9e4ce424ce93e221dc525f03f1b6c791e102cd4605eb2`).
Tested five-file patch SHA-256: `3f5029e6385210b172c8173eb10f0acd3f81dbab422393d1cf33799cbd47b942`.
Local evidence: `/tmp/dec-ch1-page-fix-check.log`,
`/tmp/dec-ch1-page-fix-precommit.log` and `/tmp/dec-ch1-page-fix.patch`.
The live frontend/backend processes were not changed. Task 9.3 remains open
until approved integration and checks on develop; no commit, merge or push was
performed for this correction.

## Correction committed (2026-11-03)

The tested correction is committed as `479172e` on
`feature/interim-normatives/backend`. Its five-file patch matches the tester's
SHA-256 recorded above. Commit hooks passed. Backend review is APPROVE for this
correction; frontend review remains APPROVE at `a8fb64e`. Feature merge and push
were not performed. Task 9.3 remains open for integration and develop checks.

## Feature integration, task 9.3 (2026-11-03)

Task 9.3 is **complete**. Akim explicitly requested push and merge in the
conversation. Reviewed backend `479172e` was published and merged into develop
as `2d0f7db`, followed by reviewed frontend `a8fb64e` as `cbfb634`, without
conflicts. Both feature tips are ancestors of develop; their application trees
match the reviewed versions. The P2 correction remains included.

Both check scripts passed on the actual merged develop, not only a temporary
patch simulation. Backend: Ruff/mypy PASS, five architecture contracts KEPT,
1351 passed, 11 skipped, one existing warning, 100% branch coverage
(3149 statements, 578 branches). PostgreSQL checks skipped because test URLs
were not configured. Frontend: API drift/ESLint/TypeScript PASS, 496 tests in
46 files passed, 100% branch coverage (634/634). Both pre-commit hooks passed;
strict OpenSpec validation passed (23/23). The existing unrelated
formula-extractor-fix archive-target notice remains.

Post-merge logs: `/tmp/dec-ch1-postmerge-backend.log` and
`/tmp/dec-ch1-postmerge-frontend.log` (local temporary evidence).
Live application processes were not restarted. Phase-1b data (7.5/9.3a),
requirement synchronization (1.4) and final sync/archive (9.5) remain open.
This integration does not close the entire CH1 change.
