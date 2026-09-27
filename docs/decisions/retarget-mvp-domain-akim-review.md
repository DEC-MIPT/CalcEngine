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
