# Tasks

> Reviewed by Egor (2026-10-05). Egor leads this change and owns the data zone;
> Akim drafted it and wrote the engine-facing scenarios.

Branch: planning phase, so the work stays on the `Specs` line (`Specs-onboarding` now,
merged into `Specs` after review). There is no application code, so no
`feature/<task>/<zone>` sub-branch applies to the spec work. If a task below turns into
code or data files, use `feature/retarget-mvp-domain/data` (Egor) or
`feature/retarget-mvp-domain/backend` (Akim).

Executor tags: **[Akim]** engine/backend zone, **[Egor]** catalog/data zone, **[PM]**,
**[Agent]** a subagent.

## 1. Draft and review

- [x] 1.1 [Akim] Draft proposal, design, and the seven spec deltas (2026-09-26)
- [x] 1.2 [Akim] Retarget the domain sentence in `openspec/config.yaml` (only domain-specific lines)
- [x] 1.3 [Egor] Review the whole draft and rewrite his parts: `normatives-catalog` delta, `foundations-shallow` lists, `design.md` decisions (2026-10-05: reviewed; `source: unverified` → `status: unverified` to match the shared `NormRef`; `foundations-shallow` lists filled in 3.1; DRAFT markers removed)
- [ ] 1.4 [PM] Approve the non-goals list, the domain order, and the B2C limit (unverified in `user-accounts`)

## 2. Engine-facing scenarios (Akim)

- [x] 2.1 [Akim] Review the `calculation-engine` delta and the `transparent-output` example; confirm they match the future `calculation-core-contract` (2026-09-27: three mismatches fixed in both deltas, `spec-reviewer` READY; see `docs/decisions/retarget-mvp-domain-akim-review.md`)
- [x] 2.2 [Akim] Review the `web-platform` and `user-accounts` dedup; confirm no requirement lost its owner (2026-09-27: no requirement lost its owner; two minor duplicates listed in the same file)

## 3. Catalog and data (Egor)

- [x] 3.1 [Egor] Fill the in-scope and out-of-scope lists in `foundations-shallow`, replacing "TBD" (2026-10-05: in-scope `foundations_shallow_r`, the type Egor and the PM confirmed in `docs/decisions/first-calculation-type-egor-pm.md`; out-of-scope is its complement, for the PM to confirm with the in-scope list)
- [x] 3.2 [Egor] Fill the milestone name for the second domain in `product-vision` (2026-10-05: `water-supply-internal`)
- [x] 3.3 [Egor] Confirm the `normatives-catalog` norm-reference marking is compatible with `NormRef` of `norm-source-traceability` (2026-10-05: aligned the marking to the shared interface `NormRef {document, edition, clause, status, provenance}`; the delta no longer uses a `source` field)

## 4. Cleanup of the placeholder domain outside this change

Found by the grep sweep on 2026-09-26. Not edited by this draft; the owner decides.

- [x] 4.1 [Egor] `openspec/changes/backend-layered-architecture/tasks.md` lines 21, 27, 32 (pilot source, pilot parameter file, reference implementation of the placeholder domain): retarget or replace by domain-neutral wording. Shared area, owned by the backend-layered-architecture change (2026-10-05: closed — the placeholder-domain wording is already gone from that file; the pilot tasks moved to `calculation-core-contract` task 7.1, and its "Follow-ups outside this change" note says to close or update these citations)
- [x] 4.2 [Egor] `openspec/changes/backend-layered-architecture/design.md` lines 62-63: reference-implementation wording. Same owner as 4.1 (2026-10-05: closed together with 4.1 — the referenced lines no longer hold placeholder wording)
- [ ] 4.3 [Agent: spec-keeper] At archive, confirm the sync removed the placeholder-domain text from `openspec/specs/product-vision`, `calculation-engine`, `normatives-catalog`, and `transparent-output`, and that `openspec/config.yaml` is clean

## 5. Validate and close

- [x] 5.1 [Akim] Run `openspec validate retarget-mvp-domain --strict` and `openspec validate --all --strict` (2026-09-27: valid; 17/17)
- [ ] 5.2 [Agent: spec-reviewer] Review the change; resolve blockers
- [ ] 5.3 [Agent: norm-traceability-checker] Confirm no norm reference is unmarked
- [x] 5.4 [Akim] Run the keyword grep over `openspec/` excluding `archive/`; expected hits only in files listed in section 4 (2026-09-27: nine hits, all in files of tasks 4.1-4.3; see `docs/decisions/retarget-mvp-domain-akim-review.md`)
- [ ] 5.5 [Agent: tester] Issue the verdict (see DOD)
- [ ] 5.6 [Egor] Merge to `Specs` after 5.1-5.5 pass
- [ ] 5.7 [Agent: spec-keeper] Sync the deltas into `openspec/specs/` and archive the change

## Dependencies

- 1.4 (PM approval) gates 5.6.
- Section 4 tasks 4.1-4.2 must finish before the grep gate in the roadmap ("0 hits outside
  archive") can pass.
- `norm-source-traceability` (planned) defines the reference field format; this change
  does not wait for it.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [ ] `openspec validate --strict` passes (task 5.1)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements: none apply (documentation only); recorded in `design.md`
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branch defined (above)
- [ ] Dependencies satisfied (PM approval pending)

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4). The change has no
  code, so `tester` issues an explicit verdict "no code, no tests, coverage not
  applicable", and the UI/UX check does not apply.
- GO when all hold: `openspec validate --all --strict` passes; `spec-reviewer` reports
  no blockers; the PM has approved the non-goals list and the B2C limit; Egor has
  reviewed the draft; the keyword grep over `openspec/` outside `archive/` returns hits
  only in files that section 4 lists as pending or none.
- NO-GO: validation fails, an unresolved blocker, a real-looking norm number without a
  checked source, or the PM has not approved.
- Archive (5.7) happens only after GO.
