# Readiness review: `calculation-verification` (WP4)

- Date: 2026-09-27
- Change: `openspec/changes/calculation-verification/`
- Owner: Akim. Section 4 (shared files: `tester.md`, `test-process`, `development-process`) needs Egor's agreement (task 4.1; agreed 2026-10-11, applied 2026-10-20 in `2863bc9`).
- Criteria: `openspec/specs/development-process/spec.md`, "Planning before implementation" and "Go/No-Go verdict and archive" (synced from `team-roles-update`, WP7, 2026-09-27); this change's own `tasks.md`, "DOD and Go / No-Go".

Russian version: `calculation-verification-readiness-rus.md`. The earlier drafting record for this change is `docs/reports/WP4_report.md` (2026-09-26, Russian); this file is the tracked readiness record from today's spec-phase gate.

## Final status

**GO (implementation, feature `calculation-verification-backend`) — 2026-10-20**; see section 5. The spec-phase verdict below stays as it was.

**GO (spec phase, task 1.5) — 2026-09-27**

`openspec validate --all --strict` passes, three `spec-reviewer` rounds ran today on the current text (round 3: 0 blockers, 0 major), and no norm value, tolerance, edition, or clause is fixed anywhere in the delta specs. The `tester` declared GO for the spec phase; see section 3. Implementation sections 2 and 3 remain open and are not covered by this verdict.

| DOD condition (`tasks.md`) | State | Evidence |
|---|---|---|
| `openspec validate --all --strict` passes | Met | 17/17, see section 1 |
| `spec-reviewer` report on the current version: no blocker, no major | Met | 3 rounds today; round 3: 0 blockers, 0 major, 2 pre-existing non-gating minors; see section 2 |
| `norm-traceability-checker` confirms no norm value or tolerance is fixed | Met | No dedicated checker pass ran on today's text; the three spec-reviewer rounds and the `tester`'s own independent read of both delta specs found no fixed norm value, tolerance, edition, or clause (every occurrence of `tolerance`/`tolerance_kind`/`tolerance_source` is a field, `edition` may be `unverified`); flagged as a process gap, not a defect, in section 3 |

## 1. `openspec validate --all --strict`

```
Totals: 17 passed, 0 failed (17 items)
```

Run after each of the three rounds below and after the `tester` verdict; identical result each time.

## 2. `spec-reviewer` rounds (today)

The change's spec delta (`specs/calculation-verification/spec.md`, `specs/calculation-engine/spec.md`, `specs/development-process/spec.md`) has not changed since it was drafted in commit `fec56dc`. A single reviewer pass ran near drafting time (recorded in `docs/reports/WP4_report.md`: 0 blockers, 10 major, 5 minor, fixed within the change but never re-verified by a fresh pass — flagged there as an open item). Since then `proposal.md`, `design.md`, and `tasks.md` were edited several times (task 1.4 confirmed `design.md` decisions 7 and 9; tasks 2.6 and 4.2 closed; NormRef references updated to Egor's written answers, commit `a1a896c`). Before today's spec-phase gate, no fresh full pass had confirmed the current text.

### Round 1: 1 blocker, 2 major, 1 minor

- **Blocker:** no fresh, logged `spec-reviewer` pass existed on the current text, versus `openspec/specs/development-process/spec.md`'s "Planning before implementation" requirement (synced from WP7 the same day): a report with no blocker and no major finding must exist "for the current version of the change".
- **Major (a):** `tasks.md`'s DOD line for the spec phase said only "`spec-reviewer` reports no blockers", omitting "no major finding" and "current version" — weaker than and inconsistent with the now-binding spec.
- **Major (b):** the original single pass's 10 major/5 minor findings were never itemized, only counted, so there was no per-finding trace that they were actually fixed.
- **Minor (pre-existing, non-gating):** `specs/calculation-engine/spec.md` "Calculation latency" is not yet testable because "typical calculation" is undefined; task 3.7 is already marked `[blocked: typical calculation]`.
- The reviewer's own "Checks that passed" section showed it had already done real content verification (no norm value/tolerance/edition/clause fixed; `design.md` consistency; Egor's answer genuine; task cross-references correct) — so major (b) was judged closeable once a pass is logged, not a sign of an actual undiscovered defect.

Fix applied: `tasks.md`'s spec-phase DOD line reworded to "a `spec-reviewer` report on the current version of the change lists no blocker and no major finding (`openspec/specs/development-process/spec.md`, "Planning before implementation")" — closes major (a).

### Round 2 (after the DOD fix): 0 blockers, 1 major, 2 minor

- **Major:** `proposal.md`'s "Why" section cited `docs/audit/03-verified-roadmap.md` as the rationale source. Per `.gitignore`, `docs/audit/` is not tracked (only `docs/decisions/` and `docs/reports/` are), so this violated `openspec/specs/development-process/spec.md`'s "Shared decisions are tracked" requirement (added by WP7, merged the same day): a rationale must cite a tracked file or restate the reasoning, not cite an untracked external document. The same pattern was noted (out of scope here) in `calculation-core-contract/proposal.md` and `retarget-mvp-domain/proposal.md`.
- **Minor (pre-existing, non-gating):** same latency-testability gap.
- **Minor (non-gating):** the original findings still not itemized; downgraded from round 1's major since the DOD now only requires a fresh pass on current text, which this round supplied.

Fix applied: the citing sentence was shortened to drop the reference to `docs/audit/03-verified-roadmap.md`, keeping the three bullets below it (labeled A3, A4+C9, E1), each of which already restates its reasoning inline with tracked evidence (concrete `spec.md` line references) — no replacement citation was needed.

### Round 3 (final, after both fixes): 0 blockers, 0 major, 2 minor (both pre-existing, non-gating)

Confirmed: the "Why" section reads coherently after the citation was dropped — the A3/A4+C9/E1 labels function as informal finding tags, not orphaned references, since each carries its own tracked evidence. A grep of the whole change directory for `docs/audit` found no remaining hits. The only other `docs/` citations in the change (`docs/decisions/normref-questions-egor.md`, `docs/decisions/reference-examples-foundations.md`) are explicitly whitelisted by `.gitignore` and confirmed tracked. The two pre-existing minors carry over unchanged and do not gate DOR (latency-testability has a blocked-task marker; the old findings are superseded by these three rounds).

**Verdict: READY for DOR.**

## 3. Tester verdict (task 1.5, spec phase only)

```
Verdict: GO (spec phase only, task 1.5)
Change: calculation-verification (WP4), develop, 2026-09-27
Conditions:
- Validation: PASS. `openspec validate calculation-verification --strict` -> valid. `openspec validate --all --strict` -> 17/17.
- spec-reviewer no blocker/major (current text): PASS. Grepped the whole change directory for `docs/audit` -- zero matches. The remaining citation to `docs/decisions/normref-questions-egor.md` (commit `a1a896c`) is confirmed tracked in git, so it satisfies "shared decisions are tracked". `tasks.md` contains the fixed DOD wording exactly as cited.
- norm-traceability-checker: PASS, with a flag. No dedicated checker pass is logged against today's text -- only the spec-reviewers' general content check. The tester independently read all three delta specs in full: every `tolerance`/`tolerance_kind`/`tolerance_source` occurrence is a field the engineer fills in later, never a fixed number; no norm edition or clause is asserted as fact. The one concrete number in the diff, the 30-second latency target, is not new -- it moved unchanged from the requirement being removed, per its own Migration note, and was already flagged as the pre-existing latency-testability minor. No genuine gap found, but the absence of a dedicated checker run is a process gap, not a blocker.
```

This verdict covers the spec phase only. Sections 2 and 3 (implementation: reference examples, regression corpus, invariant tests, metrics) remain open and are not covered. The two pre-existing minors (latency-testability; old findings not itemized) carry over as non-gating.

## 4. Open items carried forward

| Item | Owner | Blocks |
|---|---|---|
| `specs/calculation-engine/spec.md` "Calculation latency": "typical calculation" undefined | Engineer (Akim, or the engineer who fills `reference-examples-foundations.md`) | Task 3.7 only; already marked `[blocked: typical calculation]` |
| Section 4 shared-file edits (`tester.md`, `test-process`, `development-process`) need Egor's agreement | Egor | Task 4.1; not part of this GO |
| ~~`input_hash` algorithm in `calculation-core-contract` is still "a proposal, open for review"~~ Closed 2026-10-03: accepted by Egor with no change (`calculation-core-contract` task 1.8, `a01af6f`) | Akim/Egor, via that change | Nothing now (was: regression corpus, tasks 3.2-3.3) |
| Reference examples, invariants, and the definition of "typical calculation" for `foundations-shallow` | Akim (engineer) | Sections 2-3; see `docs/decisions/reference-examples-foundations.md` |
| A dedicated `norm-traceability-checker` pass on the current text was never run (only the spec-reviewers' and tester's content checks) | — | Nothing today; noted for the next content edit |

## Re-review after Egor's answers (2026-10-03)

Two `spec-reviewer` passes on the current text after commit `11bdca4` (task 1.8 of
`calculation-core-contract` closed with the `input_hash` algorithm unchanged; Egor's
pipeline moved to `ml/` and `infra/`). First pass: 0 blockers, 0 major, wording minors
(task 1.8 passages in the present tense, paths, the open-points paragraph), all fixed.
Second pass: 0 blockers, 0 major, no finding. **READY for DOR.**

## 5. Tester verdict (implementation, 2026-10-20)

The `tester` ran on `feature/calculation-verification/backend` at `7271240` (`develop`
merged in). Task 3.7 (latency test) had been moved to a follow-up by Akim the same day
(`0fb0825`, `tasks.md` section 5). Open before this verdict: 6.1 and 6.2 only.

```
Verdict: GO (implementation phase, feature calculation-verification-backend)
Change: calculation-verification (WP4), 2026-10-20
Feature/branch/commit: calculation-verification-backend, feature/calculation-verification/backend, 7271240
Conditions:
- Tests: PASS. `./check.sh` exits 0: ruff clean; mypy "no issues found in 154 source files"; lint-imports "5 kept, 0 broken" (including "verification imports from the application only engine, schemas and core"); pytest "1155 passed, 11 skipped", hypothesis seed 2271787898. All 11 skips are environment skips (catalog and app database variables not set in that run).
- Coverage: PASS. Total 100.00% branch (2755 statements, 504 branches); every module of app/verification at 100%.
- Catalog run: PASS. `pytest -m postgres tests/test_verification_catalog_properties.py tests/test_catalog_ingested.py` with DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL set: 10 passed, seed 4026219359; repeated with seed 20261020: 10 passed. Each of the 7 catalog property tests: 100 passing, 0 failing, 0 invalid.
- Invariant completeness: PASS, resting on the catalog run. The pilot has 11 invariants (2 shared, 3 formula-independent, 6 formula-dependent), each with a registered property test; the 6 formula-dependent ones and the k_z threshold test passed on the catalog under both seeds. Controls on a synthetic R run in the default suite, and the threshold test is shown to catch a drop.
- Correctness gate: DOES NOT APPLY (development-process delta, scenario "Change without calculation code"). `git diff --name-only develop...HEAD` touches nothing under backend/app/engine, backend/app/services, backend/app/parameters or backend/params; the feature adds the verification framework, tests, an import contract and the Hypothesis dev dependency. The framework's reports (SuiteReport, GoReport with the three metrics, the regression runner) are exercised on a synthetic type only: no calculation type has real reference examples or a stored corpus yet.
- Validation: PASS. `openspec validate --all --strict`: 21 passed, 0 failed.
- Delta vs implementation: PASS (spot-check). Each requirement and scenario of the calculation-verification delta has named tests (reference examples, regression corpus, invariant tests, metrics), and "Calculation accuracy" of the calculation-engine delta is held by the per-quantity deviation. Not covered by design: ">= 3 examples per type" for foundations_shallow_r (non-goal, follow-up), a real frozen corpus recomputed on every change (design.md decision 18, open), "Calculation latency" (follow-up, former task 3.7). The development-process gate is applied in tester.md and the test-process skill (2863bc9).
- UI/UX: N/A, the feature changes no UI.
- Security: PASS. `pre-commit run --all-files` passes; no credential, eval/exec, subprocess or unsafe loader in the diff. The reader URL was used only on the command line.
```

Findings, none blocking:

1. The next change that adds a calculation (for example `foundations-pressure-from-loads`)
   cannot get GO under the gate without at least 3 real reference examples: a short suite
   is invalid, so NO-GO. Today no type has any. The engineer's examples and the parameter
   source of design decision 14 are to be planned before or with that change.
2. The real regression corpus was not listed as a follow-up. It is added to `tasks.md`
   section 5 together with this record, as task 6.2 asks for open items before the
   archive.
3. Invariant completeness counts a registered test even when it is skipped, so
   `check.sh` alone would show GO with the 6 formula-dependent invariants skipped. A GO for
   a later change that touches the pilot's formula or catalog quotes a run with
   `DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL` set, as this one does.
4. The catalog run used the interim database `dec` through the read-only role
   `dec_normatives_reader` (ingested 2026-10-13), not a `_test` database. Acceptable,
   because the role only reads.
5. The `StarletteDeprecationWarning` (httpx with `starlette.testclient`) predates this
   feature.

Next: the `orchestrator` review of the feature (AGENTS.md section 2, step 7, chosen by
Akim), then the merge into `develop`, then 6.1-6.2 (`spec-keeper` sync and archive).

## 6. Orchestrator review (2026-10-21)

Reviewer: the `orchestrator` agent, chosen by Akim instead of Egor (AGENTS.md section 2,
step 7). Scope: the diff `develop...feature/calculation-verification/backend` at
`7271240`, against the proposal, design decisions 1-18, the three delta specs and
`tasks.md`. Run in a throwaway worktree: the verification tests (182 passed, 7 skipped
without a database, `app/verification` 100% branch), a probe of the seed wiring, and
mutation probes. Not run: database tests, the whole `check.sh`, `openspec validate` (the
`tester` ran them, section 5).

**Verdict: changes requested** (one major finding), with a merge without a new `tester`
round once finding 1 is fixed, because the fix does not touch the gate logic.

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | major | `within_tolerance` compares in binary floating point, so a decimal value on the edge is outside (245.2 against 245.3 with 0.1 gives `0.10000000000002274`; 0.33 against 0.3 with a relative 0.1 likewise); the edge tests used values exact in binary | Fixed in `361aa97`: a slack of 4 units in the last place (`FLOAT_SLACK_ULPS`), and six decimal edge tests. Instead of the suggested `Decimal` from `repr`, because a value converted to another unit carries `float` noise that `repr` keeps. `design.md` decision 15 records the slack |
| 2 | minor | Repeated `example_id` values count towards the minimum of 3 | Fixed in `361aa97`: reason `DuplicateExampleId`; the minimum counts distinct ids |
| 3 | minor | `run_suite([])` and `go_report` of it give GO | Fixed in `361aa97`: an empty run is NO-GO; `Reproducibility.verdict` without examples is NO-GO |
| 4 | minor | Three tests pass with the behaviour broken: (a) a declaration's `old` is not checked, (b) the unit in the regression comparison, (c) `unit_change_holds` without the conversion | Fixed in `361aa97`: a test for each; (c) is a negative control with a stand-in `calculate` that sees the units |
| 5 | minor | `CorpusEntry.outputs` accepts one quantity twice, and the last one wins | Fixed in `361aa97`: a validator of unique quantities |
| 6 | note | The parser of declared differences is lenient (header row, rows without a leading pipe, `#` in a code block, `""` and `-` as "no output"); all fail safe | Follow-up, `tasks.md` section 5 |
| 7 | note | An errored example counts as "not reproduced" and is missing from `failures` | Follow-up, `tasks.md` section 5 |
| 8 | note | For the real corpus: the build recomputes the corpus of the base branch and reads the declarations of the change | Added to the "real regression corpus" follow-up, `tasks.md` section 5 |
| 9 | note | Nothing enforces that `app/verification` does not import Hypothesis | Follow-up, `tasks.md` section 5 |
| 10 | note | Pilot tests repeat the bounds of `PILOT_RANGES` and the length units | Follow-up, `tasks.md` section 5 |
| 11 | note | The seed header is not shown under `pytest -q` (`check.sh` does not use `-q`) | Follow-up, `tasks.md` section 5 |

Checked and found in order by the reviewer: the tolerance edge and the unit of the
comparison (decision 15), the suite verdict and its invalidity reasons, the three metrics
against their definitions, the GO report, the regression comparison, the seed of decision
16, no norm value in code or tests, purity and layering, and the Russian Google-style
docstrings.

After the fixes (`361aa97`): each new test fails when its fix is reverted (9 of 9
mutations caught); `check.sh`: ruff, mypy, lint-imports clean, 1169 passed, 11 skipped,
100% branch coverage. Next: the merge of the feature into `develop`, then 6.1-6.2.

## Final revision and synchronization readiness (2026-11-09)

Task 6.1 is complete. The accepted final verification revision 361aa97 is the exact
second parent of merge 38f9185, an ancestor of current develop at 5a59fcc. All
tracked verification application/test files, including pilot_invariants.py, remain
byte-identical to that revision. The change artifacts and readiness record were
unchanged since integration before this closure assessment.

Acceptance evidence remains tester GO at 7271240, followed by the orchestrator's
explicit permission to merge after the required fix without another tester round.
The fixes at 361aa97 and the recorded full check (1169 passed, 11 skipped, 100%
branch coverage) are preserved in section 6. No later or fresh tester GO is inferred.
UI/UX remains N/A because this feature changes no UI. The skipped database checks
are not represented as fresh checks; the historical catalog test runs in section 5
remain evidence for their recorded revision.

A three-main-spec preview applies seven ADDED and one REMOVED requirement to
calculation-engine, calculation-verification (new main spec) and development-process.
It preserves existing Purposes and untouched requirements/scenarios. The one
active-delta lifecycle correction references the canonical foundations-shallow
capability rather than a not-yet-archived retarget delta; origin, tolerance and
correctness policies are unchanged. Read-only current review reports 0 blockers,
0 major and 0 minor findings and readiness for the sync/archive choice.

Selected strict validation passed; all actual specs/active changes passed 21/21.
An isolated main-spec tree with the candidates passed 15/15. The existing unrelated
formula-extractor-fix archive-target message remains informational. Main specs and
the active change directory are unchanged; task 6.2 remains open pending the
archive workflow's synchronization/archive choice. No commit, merge or push was
performed for this assessment, and application tests were not rerun.

The real references, real frozen corpus/build integration and typical-calculation
latency definition remain accepted follow-ups in tasks section 5. Framework archive
does not establish correctness of a calculation type or supply the three admitted
reference examples required for the future loads type's GO.

## Main specs synchronized and framework change archived (2026-11-09)

Akim explicitly authorized synchronization and archive in the user conversation.
Three canonical specs now match their reviewed preview SHA-256 values: calculation-engine,
calculation-verification and development-process. All seven ADDED requirements and
the one REMOVED requirement were verified against the active deltas before moving
the change. Existing main Purposes, unaffected requirements and scenarios remain
preserved; the new capability Purpose matches its delta. The previously fetched
specs instruction snapshot was reused.

Selected change strict validation passed with explicit --type change; actual main
specs passed 15/15. The whole directory, including .openspec.yaml, was moved to
`openspec/changes/archive/2026-11-09-calculation-verification/`. All strict
validation after archive passed 21/21. Task 6.2 is complete; no task checkbox remains
open. The total is unchanged because one main spec was added and one active change
was archived. The unrelated formula-extractor-fix archive-target information remains.

The existing framework acceptance evidence cited above remains the basis for
closure; no new tester GO or application/database/catalog test execution is claimed.
This operation changed documentation only. Real references, the real regression
corpus/build integration and typical-calculation latency definition remain the
explicit accepted follow-ups in task section 5. Archive does not establish
calculation correctness or the future loads type's three-reference GO gate.
No commit, merge or push was performed. The remaining upstream canonical owner
to assess for the loads contract is frontend-app.
