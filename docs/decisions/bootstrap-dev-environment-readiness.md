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

**GO (implementation, task 7.1) — 2026-10-04**, for `feature/dev-environment/backend`;
see section 6. Merge waits for the review (task 7.2), archive for 7.2 and 7.3.

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

## 6. Implementation verdict (task 7.1, 2026-10-04)

Tasks 4.6, 4.4, 5.1 and 4.5 were done in that order on `feature/dev-environment/backend`
(`9dca91e`); the note on Egor's files is on `develop` (`8526040`), tasks 6.1-6.2 too
(`40096fc`). The `tester` ran on `9dca91e` with `origin/develop` merged in, uncommitted
(a temporary worktree, removed afterwards), as the verify clause of task 4.5 asks.

**Verdict: GO** for the feature and for task 7.1. UI/UX: N/A, the frontend is unchanged
(`git diff --stat origin/develop -- frontend` is empty).

| Criterion | Evidence | Result |
|---|---|---|
| `backend/check.sh` | exit 0; ruff and mypy clean; `lint-imports`: 4 kept, 0 broken; pytest 685 passed, 1 skipped (the postgres module, no `DEC_TEST_APP_DATABASE_URL`) | pass |
| Backend branch coverage | `app`: 1637 statements, 320 branches, 100.00%. `backend/scripts/check_env_example.py`, outside the gate, measured by the `tester`: 97% branch (only the `__main__` guard, run in a subprocess) | pass |
| `frontend/check.sh` | exit 0; branches 100% (0 of 0), the only threshold in `vite.config.ts`; statements 50%, functions 33.33%, lines 66.66% | pass under the project rule (branch coverage) |
| `pre-commit run --all-files` | exit 0, both hooks passed | pass |
| 4.5 | a staged fake AWS key fails `detect-secrets`; all 22 paths of the baseline exist; a fresh scan gives the same findings | pass |
| 4.4 | removing `# DEC_PARAMS_ROOT=` or `DEC_APP_DATABASE_URL=` fails the hook, naming the variable | pass |
| 5.1 | `test_import_contracts.py` 5 passed; end to end, an `engine` import of `parameters` stops `check.sh` at `lint-imports` and names the import | pass |
| 4.6 | `.env.example` names `dec_normatives_reader`, database `dec`, a placeholder password | pass |
| OpenSpec | `validate bootstrap-dev-environment --strict` and `--all --strict` (20/20) pass | pass |
| Egor's zone | no file under `ml/` or `infra/` changed | pass |

### Decision: the open question on the backend coverage gate

- Question (`design.md`, "Open Questions", last item; task 7.1): how the base
  `development-process` requirements "Test gate with >= 95% branch coverage" and
  "Go/No-Go verdict and archive" apply while `backend/app/` does not exist and
  `backend/check.sh` produces no coverage number.
- Resolution: moot. `backend/app/` exists since `backend-layered-architecture` (WP5) was
  merged (`53a4892`); since then `backend/check.sh` runs
  `pytest --cov=app --cov-branch --cov-fail-under=95`, so the backend zone is gated like
  any other. No team exception to the 95% rule was needed and none is granted. This
  closes the item in "Open Questions" and the condition of task 7.1 and the DOD.
- Evidence: the verdict above, `check.sh` exit 0, branch coverage 100.00%.
- The `else pytest` branch of `check.sh` and the spec's "not yet present" scenarios no
  longer apply on `develop`; they stay as written, and `spec-keeper` decides at task 7.3
  whether to trim them.
- Gate scope: `app` only. Scripts under `backend/scripts/` are covered by their tests
  in `check.sh` and their coverage is measured by the `tester` at each verdict.
- Decided by Akim on 2026-10-04, on the `tester`'s GO.

### Minor findings, none blocking

1. The scenario "Config variable missing from the template" says the check runs as a
   pre-commit hook, not in the backend command; `test_check_env_example.py` also
   enforces it in `check.sh`. Stricter than the spec; `spec-keeper` rewords or notes it
   at task 7.3.
2. `backend/scripts/` is outside the automatic coverage gate (see the decision above).
3. The `engine` contract is a deny-list of today's top-level packages; a new top-level
   `app.*` package has to be added to it.
4. `check_env_example.py` reads only constant `validation_alias`/`alias`, classes based on
   the name `BaseSettings`, and only `backend/app/core/config.py`; `env_prefix`,
   `AliasChoices`, settings subclasses or settings in another module would need an
   update. None applies to the current code or the WP9 branch.
5. The frontend threshold covers branches only and is met with 0 of 0 branches; the
   `frontend-app` feature decides on statement, function and line thresholds.
6. Tasks 4.4-4.6, 5.1 and 6.1-6.2 are not ticked in `tasks.md` yet (deferred batch);
   they are ticked before the archive.

| Item | Owner | Blocks |
|---|---|---|
| Task 7.2: review before merge (Egor or the orchestrator) | Egor / orchestrator | Merge of `feature/dev-environment/backend` |
| Re-run the scan of task 4.5 after WP9 is merged (its tests add placeholder passwords) | Akim | `pre-commit run --all-files` on `develop` after that merge |
| Task 7.3: sync and archive | `spec-keeper` | Needs 7.1 and 7.2 |
