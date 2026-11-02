---
name: sdd-workflow
description: Spec-Driven Development workflow for DEC. Enforces DOR (Definition of Ready), DOD (Definition of Done), and Go/No-Go rules via OpenSpec. Use when planning, implementing, testing, or archiving any task in this project.
---

# SDD Workflow (Spec-Driven Development)

Every task in DEC follows this lifecycle through OpenSpec. No code without a change
proposal.

## Lifecycle

1. Capture -> OpenSpec change proposal (`openspec new change <name>`)
2. Plan -> business-analyst writes proposal + DOR
3. Design -> architect writes design.md
4. Implement -> developer on the feature branch (documents go straight to `develop`)
5. Test -> tester runs tests (>= 95% branch coverage), GO/NO-GO
6. UI/UX check -> ui-ux-tester verifies visuals/controls (when UI changed)
7. Review & merge -> change reviewed (other developer or orchestrator) and merged to develop
8. Archive -> spec-keeper syncs specs and archives

## DOR — Definition of Ready (all must hold)

- [ ] Change proposal exists: `proposal.md`, `specs/…`, `design.md`, `tasks.md`
- [ ] `openspec validate` passes
- [ ] Functional requirements recorded as OpenSpec requirements/scenarios
- [ ] Non-functional requirements recorded (performance, security, accessibility, coverage)
- [ ] Plan complete; each task in `tasks.md` completable in one session
- [ ] Acceptance criteria and Go/No-Go criteria written
- [ ] Feature branch defined (`feature/<feature>/<zone>`), or the change states it has no code
- [ ] Dependencies listed and satisfied

## DOD — Definition of Done (all must hold)

- [ ] All tasks in `tasks.md` checked off
- [ ] Automated test coverage >= 95% (branch) for changed code
- [ ] All tests pass (tester)
- [ ] ui-ux-tester confirmed visuals/controls (when UI changed)
- [ ] No known security issues introduced
- [ ] `openspec validate` passes; delta spec matches implementation
- [ ] spec-keeper synced specs and archived the change

## Go / No-Go

- **GO** — tests pass with >= 95% coverage, UI/UX check passed, validation passed.
- **NO-GO** — test failure, coverage < 95%, unvalidated OpenSpec artifacts,
  UI/UX defects blocking the user flow, or security findings.
- Only the tester (with ui-ux-tester confirmation) declares GO.

## Rules

- English for all specs, agents, skills, commits.
- Conventional Commits (`feat:`, `fix:`, `chore:`, `test:`, `docs:`).
- No code comments unless required.
