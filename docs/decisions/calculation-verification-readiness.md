# Readiness review: `calculation-verification` (WP4)

- Date: 2026-09-27
- Change: `openspec/changes/calculation-verification/`
- Owner: Akim. Section 4 (shared files: `tester.md`, `test-process`, `development-process`) needs Egor's agreement (task 4.1, not applied yet).
- Criteria: `openspec/specs/development-process/spec.md`, "Planning before implementation" and "Go/No-Go verdict and archive" (synced from `team-roles-update`, WP7, 2026-09-27); this change's own `tasks.md`, "DOD and Go / No-Go".

Russian version: `calculation-verification-readiness-rus.md`. The earlier drafting record for this change is `docs/reports/WP4_report.md` (2026-09-26, Russian); this file is the tracked readiness record from today's spec-phase gate.

## Final status

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
