# `retarget-mvp-domain` (WP1): Akim's review tasks

- Date: 2026-09-27
- From: Akim. To: Egor (leads WP1).
- Scope: the `[Akim]` tasks of `openspec/changes/retarget-mvp-domain/tasks.md`: 2.1, 2.2, 5.1, 5.4. Egor's parts (`normatives-catalog`, the `foundations-shallow` lists, `design.md` decisions) are not edited here; findings for them are listed for Egor.

Russian version: `retarget-mvp-domain-akim-review-rus.md`.

## Summary

| Task | Result |
|---|---|
| 2.1 Engine and output deltas match `calculation-core-contract` | Three mismatches found and fixed in Akim's deltas (`calculation-engine`, `transparent-output`); see section 1 |
| 2.2 `web-platform` / `user-accounts` dedup, no requirement without owner | Passed; two minor duplicates noted |
| 5.1 `openspec validate --strict` | Passed: the change is valid; `--all`: 17/17 |
| 5.4 Keyword grep over `openspec/` outside `archive/` | Passed: every hit is in a file listed in section 4 of the tasks |

## 1. Task 2.1: engine and output deltas against `calculation-core-contract`

`calculation-core-contract` (WP2) tracks verification per trace step: each step carries
`norm_refs`, a step counts as verified only when all its references are, and the result
envelope counts the others in `unverified_step_count`. Its refusal (`verdict = refused`)
is for inputs outside a method's range and names the violated bound with its `NormRef`
list. WP1 is archived before WP2, so the WP1 scenarios below describe behavior without
naming WP2 requirements or envelope fields.

| # | Delta, scenario | Mismatch | Fix |
|---|---|---|---|
| 1 | `calculation-engine`, "Unverified norm source" | Marked the whole result `source: unverified` and said the engine does not treat it as verified; WP2 has no result-level mark and the verdict does not depend on it | The calculation still runs, the step is marked unverified, the result states how many steps are unverified and is never presented as fully verified |
| 2 | `calculation-engine`, "Out-of-scope type" | Did not separate the product-scope refusal from WP2's refusal for inputs outside a method's range | Refused before any calculation runs, names the scope limit from `foundations-shallow`, separate from a method-range refusal |
| 3 | `transparent-output`, "Inspect a calculation step" | One reference per step; WP2 steps carry a list | "each normative reference the step rests on"; "Unverified reference is visible" now speaks of any reference of the step |

"Unverified reference is visible" is kept on purpose: the base requirement "Normative
clause references" has no rule on unverified references, and WP2 adds one only when it
is archived, after WP1.

Archive order: WP1, WP2, and WP4 (`calculation-verification`) touch different
requirements of `calculation-engine` and `transparent-output`, so no requirement is
modified by two of them.

`spec-reviewer` on the fix: see section 5.

## 2. Task 2.2: `web-platform` and `user-accounts` dedup

No requirement lost its owner. Authorization is owned by `user-accounts` "Single
authorization" and referenced by `web-platform` "Single authorization". Tier limits are
owned by `user-accounts` "Subscription tiers" and referenced by `product-vision`
"Subscription monetization". "Free trial", "User registration and authentication", and
"Billing deferred for MVP" stay in `user-accounts`; "Unified web interface", "Backend
API", and "Non-functional — integration and latency" stay in `web-platform`. Nothing is
removed from either spec.

Minor, not fixed (for the change owner to decide):

- The trial length "14-day" is stated in `product-vision` "Subscription monetization" and in the base `user-accounts` "Free trial". `design.md` decision 3 makes `user-accounts` the owner of trial rules.
- `user-accounts` "Billing deferred for MVP" restates the `product-vision` non-goal "billing or payment integration", and adds that subscription state is managed administratively.

## 3. Task 5.1: validation

`openspec validate retarget-mvp-domain --strict`: valid. `openspec validate --all --strict`: 17 passed, 0 failed.

## 4. Task 5.4: keyword grep

Command: `grep -rni "beam\|16\.13330" openspec/ --exclude-dir=archive`. Nine hits, all expected:

- `openspec/changes/backend-layered-architecture/tasks.md:21, 27, 32` and `design.md:63`: tasks 4.1 and 4.2 (Egor).
- `openspec/specs/product-vision/spec.md:39, 44`, `calculation-engine/spec.md:15, 16`, `normatives-catalog/spec.md:33`, `transparent-output/spec.md:17`: each is in a requirement that a delta of this change removes or replaces, so the sync at archive removes it (task 4.3).

## 5. Review of the fix

`spec-reviewer` on the fixed deltas: 0 blockers, 0 major, 3 minor; verdict READY. It
confirmed that the three scenarios agree with WP2 "Typed trace step" and "Applicability
check with three outcomes", that no WP1 scenario names a WP2-only field, that only the
synthetic placeholder is used, and that no requirement name is touched by two of WP1,
WP2, and WP4. Minors: "never presented as fully verified" had no observable point (now
"no label or conclusion shown with the result claims that it is fully verified"); "not
listed in `foundations-shallow`" did not say which list (now "not on the in-scope
list"); the closing sentence of "Out-of-scope type" is explanatory, not a separate check
(kept).

## 6. For Egor

- `normatives-catalog` "Norm reference status", scenario "Reference checked": "is no longer marked `unverified`". WP2 resolution 7 keeps a `NormRef` pinned in a stored result immutable; a checked reference is a new version for new runs. Consider saying so (task 3.3).
- `tasks.md` of this change still names the historical `Specs` branch (lines 5-6 and task 5.6). The other changes now say that spec work is merged into `develop` as soon as it is ready, and close with "confirm the final version of the change is on `develop`".
- The two minor duplicates of section 2.

## 7. Egor's answer (2026-09-28)

Answers section 6.

- **`NormRef` immutability against "Reference checked" (task 3.3).** Agreed. I reword the
  `normatives-catalog` scenario: a checked reference is a new version of the reference for
  new runs; a `NormRef` already pinned in a stored result stays immutable, so that result
  keeps the edition it was run with and is never re-labelled `verified`. A newly checked
  edition applies to new runs only.
- **Historical `Specs` branch in `tasks.md`.** Agreed. I replace the `Specs` branch
  references (the branch header and task 5.6) with the current rule — spec work is merged
  into `develop` as soon as it is ready — and close the change with "confirm the final
  version of the change is on `develop`".
- **The two minor duplicates.** Make `user-accounts` the sole owner, per `design.md`
  decision 3: "Free trial" holds the trial length and `product-vision` "Subscription
  monetization" references it; "Billing deferred for MVP" references the `product-vision`
  non-goal instead of restating it.

These are WP1 edits, which I lead; I apply them in WP1 (tasks 3.3 and 5.6) rather than
leaving them as open findings.

## PM scope revision applied and checked (2026-11-08)

Akim approved the prepared eight-file revision in this conversation. It is applied
to the actual `develop` worktree based on `be22290`, with the paired
[PM decision record](product/2026-11-08-mvp-scope-and-b2c-consent.md). The required
MVP outcome is the full second-limit-state shallow-foundation workflow; R remains
the delivered stage, and water supply follows after MVP. The natural-base boundary
is preserved. Engineering methods and verification contracts remain separate work.

Current selected and all strict OpenSpec validation passed (22/22). The current
spec-reviewer report is READY with 0 blockers, 0 major and 0 minor findings.
The norm-traceability checker passed task 5.3: no concrete normative formula,
coefficient or engineering limit was introduced. The two reference examples remain
synthetic and explicitly unverified; product limits are outside that check.

The fresh sweep used `rg -n -i 'beam|балк|SP\s*16|СП\s*16' openspec --glob '!**/archive/**'`.
It found six normative placeholder hits, all owned by archive cleanup task 4.3:

| Main spec | Lines at this checkpoint | Hits |
|---|---|---:|
| `product-vision/spec.md` | 39, 44 | 2 |
| `calculation-engine/spec.md` | 15, 16 | 2 |
| `normatives-catalog/spec.md` | 33 | 1 |
| `transparent-output/spec.md` | 17 | 1 |

Paths above are under `openspec/specs/`. A seventh hit is the historical audit row
at `openspec/changes/codex-context-navigation/verification.md:33`; it records an
earlier finding and is preserved. The DOD now explicitly separates historical audit
mentions from requirement/scenario placeholders. Task 4.3 must still remove all
six placeholders from synchronized main contracts; this clarification waives none.
The sweep and ownership record complete task 5.4a.

PM input task 1.4, current validation 5.1a, review 5.2, traceability 5.3 and sweep
5.4a are complete. Current Egor acknowledgement 5.6, final tester GO 5.5, sync/archive
5.7 and its cleanup check 4.3 remain open. The old Egor review does not acknowledge
this amendment. No implementation, commit, merge, push or archive was performed.

## Oral acknowledgement reported by Akim (2026-11-08)

Akim reports in the current conversation that Egor orally confirmed the current
`retarget-mvp-domain` revision and requested the final tester check. The revision
is the applied scope amendment based on `be22290`: the full second-limit-state
foundation workflow is required for MVP, R is the delivered stage, water supply
is post-MVP, and the confirmed non-goals and B2C limit remain in force.

This records Akim's account of Egor's oral acknowledgement. It is not a direct
written comment from Egor or a committed acknowledgement of this revision.
The working-tree record is not yet committed. Task 5.6 remains unchecked until
the tester assesses the written-record requirement in AGENTS.md section 4.
No acknowledgement authorship, final GO or Git consent is inferred.

## Final tester check before document commits (2026-11-08)

The `tester` issued **NO-GO** for final task 5.5 at the current uncommitted state.
The sole missing gate is the durable current-version acknowledgement required by
AGENTS.md section 4 and `development-process` "Review before merge".
The latter places acknowledgement after the document commit.
The amendment and its acknowledgement record are still uncommitted.

Passed checks: selected strict validation, all-artifact strict validation (22/22),
whitespace and the classified placeholder sweep. Current spec review is READY
with 0 blockers, 0 major and 0 minor findings; normative traceability passed.

- tests: N/A, because this change has no code.
- coverage: N/A, because this change has no code.
- UI/UX: N/A, because this change has no code.

An attributed record of Akim's report of Egor's oral confirmation can document
the acknowledgement; no rule requires inventing a direct Egor-authored comment.
The record must name `retarget-mvp-domain`, identify the approved document revision
and be committed or recorded as a tracked comment after that document commit.
After the written-record gate is satisfied, the tester must issue a fresh verdict.
Tasks 5.6 and 5.5 remain open. No commit, merge, push or archive was performed.

## Current-version acknowledgement recorded after the document commit (2026-11-08)

The approved document revision of `retarget-mvp-domain` is commit `8f9d187`
(`docs: record approved MVP scope and PM decision`). This acknowledgement record
is added after that commit. Akim reports that Egor orally confirmed this current
revision in the conversation recorded above. The substantive approved scope has
not changed since that confirmation. This is Akim's attributed record, not a
direct written statement or a commit authored by Egor.

This subsequent commit records the acknowledgement required by AGENTS.md section 4
and `development-process` "Review before merge", and completes task 5.6.
Task 5.5 remains open pending the tester's fresh verdict on the committed record.

## Final tester GO on the committed revision (2026-11-08)

The `tester` issued **GO** for `retarget-mvp-domain` task 5.5 at `830159b`.
It verified that approved document/PM revision `8f9d187` precedes acknowledgement
commit `830159b`, which names the change and exact revision and truthfully
attributes Egor's oral confirmation to Akim's report. The substantive approved
artifacts have not changed. This resolves the earlier uncommitted-state NO-GO.

Fresh checks passed: selected strict validation, all strict validation (22/22),
committed-diff whitespace and documentation-only scope (14 paths against
`be22290`). Current spec review is READY with 0 blockers, 0 major and 0 minor
findings; normative traceability passed and the PM decision is committed.
The sweep still has six normative placeholders assigned to cleanup task 4.3
and one preserved historical audit mention.

- tests: N/A, because this change has no code.
- coverage: N/A, because this change has no code.
- UI/UX: N/A, because this change has no code.

No application tests were required or run. The existing unrelated
`formula-extractor-fix` archive-target information does not fail validation.
Tasks 5.6 and 5.5 are complete. Tasks 4.3 (cleanup verification during sync)
and 5.7 (sync/archive) remain open. This GO covers the documentation change;
it does not verify delivery of the expanded MVP calculations. No archive or push
was performed.
