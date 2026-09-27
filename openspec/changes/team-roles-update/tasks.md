# Tasks

Branch: planning phase, so the work stays on the `Specs` line (`Specs-onboarding` now,
merged into `Specs` after review). There is no code, so no `feature/<task>/<zone>`
sub-branch applies. Author: Akim. Second developer (acknowledges): Egor.

Part A is the spec delta: Akim drafts it and Egor reviews it as the second developer.
Part B edits shared files and is applied together, by hand, only after both agree; it
is not done by `/opsx:apply`.

## A. Spec delta (Akim drafts, Egor reviews)

### A1. Draft and validate

- [x] A1.1 Write `proposal.md`, `design.md`, and the delta spec for `development-process`
- [x] A1.2 Run `openspec validate team-roles-update --strict` and `openspec validate --all --strict` (passed 2026-09-26, 14/14; re-run 2026-09-27 after the "no code" path list edit, 17/17; see `docs/decisions/team-roles-update-readiness.md`, section 9)
- [x] A1.3 Run the `spec-reviewer` subagent and resolve blockers and major findings (2026-09-26: three passes, the third with 0 blockers and 0 major; 2026-09-27: pass 4 after the "no code" path list edit, 2 major, fixed; pass 5: 0 blockers, 0 major, READY for DOR; see `docs/decisions/team-roles-update-readiness.md`, section 9)
- [ ] A1.4 Get Egor's acknowledgement as second developer (a commit or comment by Egor that names this change)

### A2. Close

- [ ] A2.1 `tester` issues the verdict; this change has no code, so it records tests, coverage, and UI/UX as N/A with the reason (it is the first change to use the path it defines)
- [ ] A2.2 Merge to `Specs` after A1.2-A1.4 and A2.1 pass
- [ ] A2.3 After Part B is applied (B8 passed) or Egor has recorded in a tracked commit or comment that Part B is deferred and until when, `spec-keeper` syncs the delta into `openspec/specs/development-process/spec.md` and archives the change

## B. Shared files follow-up (applied together after both agree)

Requires Egor's agreement before each edit. The exact current and target text is in
`proposal.md`, section "Follow-up changes to shared files".

- [ ] B1 Get Egor's agreement on the list of shared-file edits
- [ ] B2 `openspec/config.yaml:36-38`: "two developers" becomes a three-person team with the PM role
- [ ] B3 `openspec/config.yaml`: add the note that `openspec validate` is structural and the DOR needs a `spec-reviewer` report
- [ ] B4 `AGENTS.md` section 5: three-person team, PM row in the zone table, PM has no agent
- [ ] B5 `AGENTS.md` section 3: add the `spec-reviewer` item to the DOR and the "validate is structural" sentence
- [ ] B6 `AGENTS.md` section 4 and section 2 step 7: add the code-free GO path and the second developer's acknowledgement as review
- [ ] B7 `CLAUDE.md:69`: reword the stale "`docs/` is untracked by design" line (show as a diff)
- [ ] B8 Run `openspec validate --all --strict` after the edits

## C. Follow-ups after archive (hand-off, not tasks of this change)

These are not checkboxes of this change. They do not gate GO or archive and do not count
toward "all tasks checked" in the DOD. Each has an owner outside this change.

### C1. Replace untracked "passport" citations (owner: `backend-layered-architecture`)

The `.gitignore` part of the same finding is already done (commit `d62999d`). This
change does not edit that change. Its owner replaces each citation with a tracked
source (for example `docs/decisions/` or `docs/reports/`) or with the restated
reasoning:

- `openspec/changes/backend-layered-architecture/proposal.md:6` ("The passport defines the tech stack")
- `openspec/changes/backend-layered-architecture/design.md:5` ("The passport ...")
- `openspec/changes/backend-layered-architecture/design.md:20` ("explicitly rejected by the passport")
- `openspec/changes/backend-layered-architecture/design.md:55` ("matches the passport 'manual monitoring for now' decision")
- `openspec/changes/backend-layered-architecture/design.md:64` ("matches the passport's 'swap hot paths to C/C++ later'")
- Check: `grep -rn -i passport openspec/` shows no rationale citation afterward

### C2. `record-installed-skills-akim` (owner: Akim)

After this change is archived, in the order set in `design.md`: Egor's acknowledgement
(task 1.5), then `spec-reviewer` (task 1.6), then the `tester` verdict with the fields
`tests: N/A`, `coverage: N/A`, `UI/UX: N/A` and the reason (task 1.7). Akim also
aligns, in that change: its DOD wording ("no code, no tests, coverage not
applicable", which lacks the UI/UX field and the reason), its "no blockers" (to "no
blocker and no major finding"), and its "Dependencies: None" line. Its record check
stays as an extra condition.

### C3. Other changes (owners: their authors)

- `retarget-mvp-domain` and `calculation-core-contract` may cite the new DOR requirement; both already carry a DOR checklist and use `spec-reviewer`.
- The future WP3 change cites the DOR requirement when it is created.

## Dependencies

- A1.2-A1.3 need A1.1. A1.4 needs the review to have no blocker and no major finding.
- A2.1 (`tester` verdict) needs A1.2-A1.4. A2.2 (merge to `Specs`) needs A2.1.
- A2.3 (archive) needs A2.2 and either B8 or Egor's recorded deferral of Part B. If Part B is deferred, B2-B8 move to a follow-up change and leave this list.
- Part B needs B1 (Egor's agreement). Section C needs the archive (A2.3) and does not gate it.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task A1.2)
- [x] `spec-reviewer` report with no blocker and no major finding (task A1.3)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements: not applicable (process change, no code); recorded here
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branch defined (above); no zone sub-branch needed
- [x] Dependencies listed; the open ones are the tasks above, not outside changes

## DOD and Go / No-Go

This change has no code, so it uses the code-free path it defines.

- GO is declared by the `tester` agent when: `openspec validate --strict` passes;
  `spec-reviewer` reports no blocker and no major finding; Egor has acknowledged (task A1.4); and the
  `tester` records tests, coverage, and UI/UX as N/A with the reason.
- NO-GO: validation fails, an open blocker, no acknowledgement, or a missing N/A record.
- Part B is not part of GO for the spec delta; it needs its own agreement (task B1). It does gate archive (task A2.3), so `AGENTS.md` and the specs do not stay contradictory. Section C does not gate GO or archive.
- Archive (task A2.3) happens only after GO.
