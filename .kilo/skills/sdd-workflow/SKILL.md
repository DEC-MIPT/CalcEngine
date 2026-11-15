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
4. Implement -> code on the feature branch; all document edits, commits and pushes only on `develop`
5. Test -> tester runs tests (>= 95% branch coverage), GO/NO-GO
6. UI/UX check -> ui-ux-tester verifies visuals/controls (when UI changed)
7. Review & merge -> change reviewed under the current AGENTS roster and merged to develop
8. Archive -> spec-keeper syncs specs and archives

Before editing any documentation, verify `git branch --show-current` is `develop`.
This includes plans, OpenSpec tasks and code journals during a code feature. Preserve
existing work and use an authorized safe switch or a `develop` checkout; stop if
the switch is unsafe. Do not prepare document edits on a feature branch for later
delivery to `develop`.

Akim is the sole active developer; do not wait for a second-human-developer
acknowledgement or assume a replacement before Akim announces one. The current
roster in `AGENTS.md` governs human ownership. Independent agent review, tester
verdicts, UI/UX confirmation where applicable, security and correctness gates remain.

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

For a change with no code, use the current code-free gate in `AGENTS.md`: strict
validation, a clean current spec review, document checks and a tester verdict with
`tests: N/A`, `coverage: N/A` and `UI/UX: N/A`, each with its no-code reason.
Second-human acknowledgement is waived while Akim is the sole active developer.
Code-only coverage and UI gates above apply where code or UI changed.

## Rules

- English for all specs, agents, skills, commits.
- Conventional Commits (`feat:`, `fix:`, `chore:`, `test:`, `docs:`).
- Commits, merges and pushes require Akim's explicit consent.
- No code comments unless required.
