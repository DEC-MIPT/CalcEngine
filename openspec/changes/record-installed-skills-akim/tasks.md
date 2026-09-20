# Tasks

Branch: planning phase, so the work stays on the `Specs` line (`Specs-onboarding` now,
merged into `Specs` after review). There is no code, so no `feature/<task>/<zone>`
sub-branch applies. Developer: Akim.

## 1. Record the installation

- [x] 1.1 Verify on disk that the seven skills are installed and visible to Claude Code (done 2026-09-20)
- [x] 1.2 Write the delta spec for `development-process` with the record and the content rule
- [x] 1.3 Run `openspec validate record-installed-skills-akim --strict` (passed 2026-09-20)
- [ ] 1.4 Run the `spec-reviewer` subagent on this change and resolve blockers
- [ ] 1.5 Get Egor's acknowledgement, because `openspec/` is shared

## 2. Close the change

- [ ] 2.1 Merge to `Specs` after 1.3-1.5 pass
- [ ] 2.2 `spec-keeper` syncs the delta into `openspec/specs/development-process/spec.md` and archives the change

## Dependencies

None. Task 2.2 needs 1.3-1.5.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task 1.3)
- [x] Functional requirement and scenarios recorded
- [x] Non-functional requirement recorded (record content); performance, accessibility, coverage marked not applicable in `design.md`
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branch defined (above); no zone sub-branch needed
- [x] Dependencies listed and satisfied

## DOD and Go / No-Go

- GO: all tasks checked, `openspec validate --strict` passes, `spec-reviewer` reports no
  blockers, Egor has acknowledged, and the delta matches what is installed.
- Test coverage: not applicable, no code is changed.
- NO-GO: validation fails, an unresolved blocker, or a path, token, or credential in
  the record.
