# Tasks

> Reviewed by Egor (2026-10-05). Egor leads this change and owns the data zone;
> Akim drafted it and wrote the engine-facing scenarios.

Branch: none. The change has no code, so its documents are committed directly to
`develop` (branching model of 2026-09-28, AGENTS.md section 2; the `Specs` line is
historical), and no `feature/<feature>/<zone>` branch applies to the spec work. If a
task below turns into code or data files, use `feature/retarget-mvp-domain/data` (Egor) or
`feature/retarget-mvp-domain/backend` (Akim).

Executor tags: **[Akim]** engine/backend zone, **[Egor]** catalog/data zone, **[PM]**,
**[Agent]** a subagent.

## 1. Draft and review

- [x] 1.1 [Akim] Draft proposal, design, and the seven spec deltas (2026-09-26)
- [x] 1.2 [Akim] Retarget the domain sentence in `openspec/config.yaml` (only domain-specific lines)
- [x] 1.3 [Egor] Review the whole draft and rewrite his parts: `normatives-catalog` delta, `foundations-shallow` lists, `design.md` decisions (2026-10-05: reviewed; `source: unverified` → `status: unverified` to match the shared `NormRef`; `foundations-shallow` lists filled in 3.1; DRAFT markers removed)
- [x] 1.4 [PM] Record approval of the non-goals, domain order, first-domain MVP outcome
  and B2C limit. Akim reported the 2026-10-19 PM decision in the 2026-11-08 conversation;
  see [the product record](../../../docs/decisions/product/2026-11-08-mvp-scope-and-b2c-consent.md). The required MVP outcome is the full
  second-limit-state foundation workflow; R is the delivered pilot. Internal water
  supply follows after MVP. This checkpoint records scope approval, not implementation GO.

The 2026-10-05 review and completed scope-fill tasks below concern the earlier draft.
The 2026-11-08 amendment requires current-version review and acknowledgement.

## 2. Engine-facing scenarios (Akim)

- [x] 2.1 [Akim] Review the `calculation-engine` delta and the `transparent-output` example; confirm they match the future `calculation-core-contract` (2026-09-27: three mismatches fixed in both deltas, `spec-reviewer` READY; see `docs/decisions/retarget-mvp-domain-akim-review.md`)
- [x] 2.2 [Akim] Review the `web-platform` and `user-accounts` dedup; confirm no requirement lost its owner (2026-09-27: no requirement lost its owner; two minor duplicates listed in the same file)

## 3. Catalog and data (Egor)

- [x] 3.1 [Egor] Fill the in-scope and out-of-scope lists in `foundations-shallow`, replacing "TBD" (2026-10-05: in-scope `foundations_shallow_r`, the type Egor and the PM confirmed in `docs/decisions/first-calculation-type-egor-pm.md`; out-of-scope is its complement, for the PM to confirm with the in-scope list)
- [x] 3.2 [Egor] Fill the milestone name for the second domain in `product-vision` (2026-10-05: `water-supply-internal`)
- [x] 3.3 [Egor] Confirm the `normatives-catalog` norm-reference marking is compatible with `NormRef` of `norm-source-traceability` (2026-10-05: aligned the marking to the shared interface `NormRef {document, edition, clause, status, provenance}`; the delta no longer uses a `source` field)

The R-only boundary in the historical task 3.1 record is superseded by the
2026-11-08 PM scope amendment. The delivered R type remains named; the full MVP
release gate and future engineering contracts are stated in `foundations-shallow`.

## 4. Cleanup of the placeholder domain outside this change

Found by the grep sweep on 2026-09-26. Not edited by this draft; the owner decides.

- [x] 4.1 [Egor] `openspec/changes/backend-layered-architecture/tasks.md` lines 21, 27, 32 (pilot source, pilot parameter file, reference implementation of the placeholder domain): retarget or replace by domain-neutral wording. Shared area, owned by the backend-layered-architecture change (2026-10-05: closed — the placeholder-domain wording is already gone from that file; the pilot tasks moved to `calculation-core-contract` task 7.1, and its "Follow-ups outside this change" note says to close or update these citations)
- [x] 4.2 [Egor] `openspec/changes/backend-layered-architecture/design.md` lines 62-63: reference-implementation wording. Same owner as 4.1 (2026-10-05: closed together with 4.1 — the referenced lines no longer hold placeholder wording)
- [ ] 4.3 [Agent: spec-keeper] At archive, confirm the sync removed the placeholder-domain text from `openspec/specs/product-vision`, `calculation-engine`, `normatives-catalog`, and `transparent-output`, and that `openspec/config.yaml` is clean

## 5. Validate and close

- [x] 5.1 [Akim] Run `openspec validate retarget-mvp-domain --strict` and `openspec validate --all --strict` (2026-09-27: valid; 17/17)
- [x] 5.1a [Akim] Validate the current PM-scope revision and all OpenSpec artifacts;
  verify: selected/all strict validation passes and its current result is recorded.
- [x] 5.2 [Agent: spec-reviewer] Review the current PM-scope revision; resolve all blocker
  and major findings, including consistency of the full-workflow release gate with
  the delivered R stage and post-MVP water-supply milestone.
- [x] 5.3 [Agent: norm-traceability-checker] Confirm no norm reference is unmarked
- [x] 5.4 [Akim] Run the keyword grep over `openspec/` excluding `archive/`; expected hits only in files listed in section 4 (2026-09-27: nine hits, all in files of tasks 4.1-4.3; see `docs/decisions/retarget-mvp-domain-akim-review.md`)
- [x] 5.4a [Akim] Repeat the placeholder-domain sweep for the current revision;
  verify: expected remaining hits and their owners are recorded before final GO.
- [x] 5.6 [Egor] After 1.4 and current-version 5.1a, 5.2, 5.3 and 5.4a pass, record
  acknowledgement of this revision by the developer who did not author the amendment,
  in a tracked commit or comment naming `retarget-mvp-domain`. The earlier review is
  historical and does not acknowledge this amendment. This acknowledgement precedes
  final tester GO 5.5; no document merge is required.
- [ ] 5.5 [Agent: tester] After 5.6, issue the current-version verdict (see DOD), with
  explicit `tests: N/A`, `coverage: N/A` and `UI/UX: N/A`, each because this change has no code.
- [ ] 5.7 [Agent: spec-keeper] Sync the deltas into `openspec/specs/` and archive the change

## Dependencies

- PM approval is recorded by 1.4. Current-version validation, review and traceability
  gates plus 5.6 acknowledgement precede final tester GO 5.5; archive 5.7 follows GO.
- Delivering the expanded calculation is not a task of this documentation change.
  Each future implementation change must define its engineering contract and release
  acceptance before code; the MVP release gate still requires all of that delivery.
- Section 4 tasks 4.1-4.2 must finish before the grep gate in the roadmap ("0 hits outside
  archive") can pass.
- `norm-source-traceability` (planned) defines the reference field format; this change
  does not wait for it.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] Current-revision selected/all strict validation passes (task 5.1a)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements: none apply (documentation only); recorded in `design.md`
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branch defined (above)
- [x] PM scope approval recorded (task 1.4); no-code closure still requires the
  current review and second-developer acknowledgement listed above

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4). The change has no
  code, so `tester` issues an explicit verdict "no code, no tests, coverage not
  applicable", and the UI/UX check does not apply.
- GO when all hold: current selected/all strict validation passes; `spec-reviewer`
  reports no blocker or major finding; the PM approval is recorded; current-version
  traceability review passes; the second-developer acknowledgement is recorded before
  tester GO; and the placeholder-domain sweep over `openspec/` outside `archive/`
  leaves requirement/scenario hits only in section 4's pending files, or none.
  Historical audit mentions are reported separately and preserved. Task 4.3 verifies
  removal from the synchronized normative contracts.
- NO-GO: validation fails, an unresolved blocker, a real-looking norm number without a
  checked source, or the PM has not approved.
- Archive (5.7) happens only after GO.
