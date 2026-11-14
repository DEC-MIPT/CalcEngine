# Tasks

Branch: there is no code and no branch; the documents are committed directly to `develop`
(`AGENTS.md`, Branching rules). Developer: Akim.

## 1. Record the installation

- [x] 1.1 Verify the fifteen skills against the skills CLI lock file (done 2026-09-20): the global lock file on Akim's machine lists 14 global skills, each with the recorded `source` and an `installedAt` of 2026-09-20; `.agents/skills/find-skills/SKILL.md` exists for the project-scope skill
- [x] 1.2 Write the delta spec for `development-process` with the record and the content rule
- [x] 1.3 Run `openspec validate record-installed-skills-akim --strict` (passed 2026-09-20)
- [x] 1.4 Run the `spec-reviewer` subagent on this change (2026-09-20: NOT READY, 3 major and 8 minor findings; the 3 major findings are fixed in this version)
- [ ] 1.5 Get Egor's acknowledgement, because `openspec/` is shared; recorded as a commit or comment by Egor that names this change
- [ ] 1.6 Re-run `spec-reviewer` after the fixes and resolve remaining blockers
- [ ] 1.7 `tester` issues the verdict for this change (see DOD)

## 2. Close the change

- [ ] 2.1 After 1.3-1.7 pass, confirm the final version of the change is on `develop`
- [ ] 2.2 `spec-keeper` syncs the delta into `openspec/specs/development-process/spec.md` and archives the change

## Additional Codex installation, 2026-11-05

- [x] Install Akim's requested `ub-mode` from `unclebob/ub-mode` at global Codex scope and verify the installed skill name.
- [x] Record the installation in the delta spec, with verification independent of the skills CLI lock file.
- [x] Validate the updated change with `openspec validate record-installed-skills-akim --strict` (passed 2026-11-05).

## Companion tools, 2026-11-05

- [x] Install Akim's requested `crapper`, `dryer`, and `mutator` in a separate user Python environment and expose commands on `PATH`.
- [x] Verify all three help commands, Python/TypeScript parsing, duplicate detection, and mutation-site scanning on temporary fixtures.
- [x] Verify a full Python mutation run: 12 killed, zero survived; verify dependencies with `pip check`.
- [x] Record tool sources and installed revisions in the design and record the installation in the delta spec.
- [x] Validate the updated OpenSpec change and check whitespace (strict validation and `git diff --check` passed).

## Dependencies

None. Task 2.1 needs 1.3-1.7; task 2.2 needs 2.1.

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

- GO is declared only by the `tester` agent (`AGENTS.md` section 4). The change has no
  code, so `tester` issues an explicit verdict "no code, no tests, coverage not
  applicable", and the UI/UX check does not apply. `tester` declares GO when all of
  these hold: `openspec validate --strict` passes; `spec-reviewer` reports no blockers;
  Egor has acknowledged (task 1.5); and the record check below passes.
- Record check: for every global entry the skills CLI lock file on Akim's machine holds
  the same skill with the same `source` and an `installedAt` date equal to the recorded
  date; the directory `.agents/skills/find-skills` exists for the project-scope entry;
  and every skill in the global lock file appears in the record.
- NO-GO: validation fails, an unresolved blocker, a record entry that does not match
  the lock file, or a path, token, or credential in the record.
- Archive (task 2.2) happens only after GO.
