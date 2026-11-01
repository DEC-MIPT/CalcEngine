# Tasks

Owner: Akim, repository instructions and documentation. No code and no branch.
Documents are prepared on `develop`; no commit, merge or push is authorized by this task.
Local `docs/akim/README.md` remains ignored; shared instructions contain a fallback.

## 1. Capture and plan

- [x] 1.1 Inspect Git state, instruction scopes, OpenSpec integration and task-related
  decisions and analysis. Verify: sources and preservation boundaries listed in design.
- [x] 1.2 Create proposal, design, delta spec and task plan with no-code scope and
  explicit acceptance/closure criteria.
- [x] 1.3 Run strict OpenSpec validation and obtain a current `spec-reviewer` report
  with no blocker or major finding before declaring navigation ready.

## 2. Context navigation

- [x] 2.1 Add selective entry, actual repository map, sourced commands and missing quality
  guidance to `AGENTS.md`; preserve existing team gates and section references.
- [x] 2.2 Create one local `docs/akim/README.md` with task routes and current-work pointers
  to existing records; verify report claims only to the extent needed for navigation.

## 3. Verification and review

- [x] 3.1 Check relative links, paths, command provenance, whitespace, privacy, instruction
  block preservation, unchanged Claude files and pre-existing edits. Run available
  documentation hooks and `openspec validate --all --strict`; record actual results.
- [x] 3.2 Rehearse task routes and obtain a final `spec-reviewer` review; fix blockers
  and major findings. Verify the tracked fallback without `docs/akim/` too.
- [ ] 3.3 Obtain the other developer's acknowledgement naming `codex-context-navigation`
  in a tracked commit or comment, as required by the existing no-code gate.
  Requested in question 3 of
  [the file to Egor](../../../docs/decisions/backend/2026-10-28-shared-config-changes-to-egor.md)
  and its Russian version; acknowledgement remains pending.
- [x] 3.4 `tester` records the no-code verdict with `tests: N/A`, `coverage: N/A` and
  `UI/UX: N/A`, each because there is no code. GO requires 3.1-3.3.
  Recorded in `verification.md`: NO-GO for closure, solely because 3.3 is pending.

## 4. Close

- [ ] 4.1 After GO and authorized delivery, `spec-keeper` syncs the delta and archives;
  verify `openspec validate --all --strict`. Commit/push remain subject to user consent.

## DOR

- [x] Proposal, design, specs and plan exist; scope is documentation only, no branch.
- [x] Functional scenarios and non-functional limits are explicit in the delta/design.
- [x] Tasks fit one session and identify acceptance checks; no external code dependency.
- [x] Strict validation passes and current `spec-reviewer` has no blocker or major finding.

## Acceptance and DOD / Go-No-Go

- Navigation identifies relevant requirements, actual code/tests and checks for engine,
  API, frontend, reports and specs without requiring all local reports.
- Shared instructions work when ignored local context is unavailable.
- Checks distinguish sourced commands from successful execution and facts from plans.
- Only allowed documentation changes; no secrets, private preferences or machine paths.
- GO: strict validation, clean review, verification complete, other-developer
  acknowledgement and tester N/A records. NO-GO: any failed check, open blocker/major
  or missing acknowledgement. Archive only after the existing GO and spec sync gates.
