# Readiness review: `bootstrap-dev-environment` (WP6)

- Date: 2026-09-27
- Change: `openspec/changes/bootstrap-dev-environment/`
- Owner: Akim. No shared-file edits outside `openspec/` and `docs/` at the spec phase;
  implementation touches only `backend/`, `frontend/`, and root files not in Egor's zone
  (`.pre-commit-config.yaml`, `.env.example`, `.secrets.baseline`).
- Criteria: `openspec/specs/development-process/spec.md`, "Planning before
  implementation" and "Go/No-Go verdict and archive"; this change's own `tasks.md`,
  "DOD and Go / No-Go".

Russian version: `bootstrap-dev-environment-readiness-rus.md`.

## Final status

**GO (spec phase, task 1.4) — 2026-09-27**

`openspec validate --all --strict` passes (18/18), two `spec-reviewer` passes ran on
the current text (pass 2: 0 blockers, 0 major), and the `tester` independently
confirmed validation, the review outcome, the absence of any norm content, and that the
spec delta's four requirements map to `tasks.md` with no orphans either way. Implementation
sections 2-7 remain open and are not covered by this verdict.

| DOD condition (`tasks.md`) | State | Evidence |
|---|---|---|
| `openspec validate --all --strict` passes | Met | 18/18, see section 1 |
| `spec-reviewer` report on the current version: no blocker, no major | Met | 2 passes; pass 2: 0 blockers, 0 major, 1 minor (fixed); see section 2 |

## 1. `openspec validate --all --strict`

```
Change 'bootstrap-dev-environment' is valid
Totals: 18 passed, 0 failed (18 items)
```

Confirmed independently three times today: once by Akim's session after writing the
four artifacts, once by the tester agent for task 1.4. `spec-reviewer` pass 2 could not
run it (no shell access in that review) and noted this; Akim's session re-ran it
immediately afterward.

## 2. `spec-reviewer` passes

### Pass 1: 0 blockers, 2 major, 2 minor

Scope: the new change's four artifacts (`proposal.md`, `design.md`, `tasks.md`,
`specs/development-process/spec.md`), checked for completeness, testability, internal
consistency between the four files, OpenSpec format, and compliance with
`agent-docs/domain-constraints.md` and the "Shared decisions are tracked" requirement.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Major | The "Pre-commit secret scan and documented configuration" requirement's scenario "Config variable missing from the template" said the *backend command* fails, contradicting `design.md` decision 5 (a separate pre-commit hook) and `tasks.md` task 4.4 (verified via `pre-commit run`) | Fixed: the scenario now names the pre-commit hook, not the backend command |
| 2 | Major | The same requirement had no deferred-state scenario, unlike the parallel "Import contract check" requirement's "Layered structure not yet present" | Fixed: added scenario "Configuration model not yet present" |
| 3 | Minor | Bare "roadmap requirement N" references in `proposal.md`, `design.md`, `tasks.md`, with no tracked source named | Fixed: reworded to drop the "roadmap" framing; reasoning restated in place |
| 4 | Minor | Task 6.2's target file left ambiguous ("`CLAUDE.md` or a root `README.md` section, whichever...") | Fixed: names `CLAUDE.md` concretely, next to task 6.1 |

### Pass 2 (after the four fixes): 0 blockers, 0 major, 1 minor

Confirmed all four fixes read correctly with no new contradiction; grepped the whole
change for "roadmap" and "docs/audit" and found zero hits. One new minor: the DOR
checklist's `openspec validate --strict` line was left unchecked even though task 1.2
itself was already checked. Fixed: the checklist line is now checked too.

**Verdict: READY for DOR.**

## 3. Tester verdict (task 1.4, spec phase only)

```
Verdict: GO (spec phase only, task 1.4)
Change: bootstrap-dev-environment (WP6), branch feature/bootstrap-dev-environment/backend, 2026-09-27
Conditions:
- Validation: PASS. openspec validate bootstrap-dev-environment --strict -> valid. openspec validate --all --strict -> 18/18.
- spec-reviewer no blocker/major (current text): PASS. Confirmed the "Pre-commit secret scan and documented configuration" requirement has exactly 3 scenarios, including the pre-commit-hook wording and the deferred-state scenario. Grep for "roadmap"/"docs/audit" over the whole change directory: 0 hits. Task 6.2 names CLAUDE.md concretely. DOR checklist's validate line is checked.
- Norm content: PASS. No SP/SNiP/GOST/clause/coefficient/edition term anywhere in the four artifacts.
- Own consistency check (spec vs tasks vs proposal/design): PASS. All 4 ADDED requirements map to tasks with no orphans: Backend tooling command -> 2.1-2.4; Frontend tooling command -> 3.1-3.4; Import contract check -> 5.1 (blocked WP5); Pre-commit secret scan/.env.example -> 4.1-4.4 (4.4 blocked WP5). No contradiction between proposal.md/design.md and the final spec text.
```

This verdict covers the spec phase only. Sections 2-7 (implementation: backend and
frontend tooling, pre-commit, the deferred import-contract and config-check tasks,
documentation, close) remain open and are not covered.

## 4. Open items carried forward

| Item | Owner | Blocks |
|---|---|---|
| Task 4.4 (config/`.env.example` cross-check hook) | Akim, once `backend-layered-architecture` task 2.1 lands | Nothing in this change's own GO; picked up when WP5 unblocks it |
| Task 5.1 (`import-linter` "layers" contract) | Akim, once `backend-layered-architecture` task 1.1 lands | Same |
| Choice of `uv` vs `requirements.txt`+`.venv` (design.md, Open Questions) | Akim, deferred | Nothing; does not change the spec or task breakdown |
| ESLint flat config vs legacy format (design.md, Open Questions) | Akim, deferred | Nothing; implementation detail of task 3.2 |
| Review before merge (task 7.2): this change is not code-free, needs Egor's or the orchestrator's review | Egor / orchestrator | Task 7.1's full GO does not gate on it, but merge to `develop` does |

## 5. Passes 3-4 after Egor's move to `ml/` (2026-10-03)

Egor moved his pipeline into `ml/` (`ml/pyproject.toml`, `ml/tests/`) and the compose file
into `infra/` (commit `24797f7`). Commit `11bdca4` updated the root-path wording.

| Pass | Result |
|---|---|
| 3 | 0 blockers, 1 major, 5 minor (NOT READY). Major: the GO criterion "`pre-commit run --all-files` passes" is unmet, since `.secrets.baseline` names five files that moved and misses backend files merged after task 4.2 (confirmed by Akim on a copy of the baseline: the hook reports new findings). Fixed by the new task 4.5 (regenerate and hand-review the baseline on `feature/dev-environment/backend`, a note on Egor's files in `docs/decisions/secrets-baseline-egor-files.md`), which task 7.1 now needs. Minors fixed: stale paths in task 4.2's record, task 2.3 re-checked (`pytest backend/tests` from the root: 32 passed), the context sentence and decision 1 title, `proposal.md` wording |
| 4 | 0 blockers, 0 major, 3 minor (the note's file name and its check, the note going to `develop`, the trigger for a re-scan after a later move). All fixed. **READY for DOR** |

The baseline itself is code and is fixed by task 4.5, not by this edit. Until then,
`pre-commit run --all-files` fails on `develop`.

| Item | Owner | Blocks |
|---|---|---|
| Task 4.5 (regenerate `.secrets.baseline`) | Akim | Task 7.1 (full GO) |
