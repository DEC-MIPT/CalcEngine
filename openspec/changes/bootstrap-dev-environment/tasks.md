# Tasks

Owner: Akim (tooling commands and pre-commit, this change; Docker Compose and CI are
Egor's and not part of this change). Branch: `feature/bootstrap-dev-environment/backend` for backend and
root-level tasks, `feature/bootstrap-dev-environment/frontend` for the frontend
scaffold, both from `develop`.

Marker **[blocked: WP5]**: the task needs `backend-layered-architecture`'s layered
`backend/app` structure (its task 1.1) or its config module (its task 2.1) before it
can be implemented; until then it is not started, not stubbed as a no-op.

## 1. Spec readiness

- [x] 1.1 (spec) Write proposal, design, and spec delta for `development-process`
- [x] 1.2 (spec) Run `openspec validate bootstrap-dev-environment --strict` and `openspec validate --all --strict` (2026-09-27: both pass, 18/18)
- [x] 1.3 (spec) Run `spec-reviewer` on this change and resolve blockers and major findings (2026-09-27: 2 passes; pass 1 found 2 major and 2 minor, all fixed; pass 2: 0 blockers, 0 major, 1 minor (stale DOR checkbox, fixed); READY for DOR)
- [x] 1.4 (spec) `tester` issues the verdict for the spec change (see DOD) (2026-09-27: **GO**, spec phase; validation, spec-reviewer, no norm content, and the tester's own spec-vs-tasks consistency check all pass; implementation sections 2-7 remain open and are not covered; see `docs/decisions/bootstrap-dev-environment-readiness.md`)

## 2. Backend tooling (backend)

- [ ] 2.1 Add `backend/pyproject.toml` with `[tool.ruff]`, `[tool.mypy]`,
  `[tool.pytest.ini_options]`, `[tool.coverage.run]`/`[tool.coverage.report]`, per
  `design.md` decisions 1 and 3; verify `ruff check backend/` and `mypy backend/` run
  without a config error on an empty tree
- [ ] 2.2 Add `backend/requirements.txt` (empty for now) and
  `backend/requirements-dev.txt` (`ruff`, `mypy`, `pytest`, `pytest-cov`,
  `import-linter`); verify `pip install -r backend/requirements-dev.txt` succeeds in a
  fresh `.venv`
- [ ] 2.3 Add `backend/tests/` with one smoke test asserting the venv and pytest
  config work; verify `pytest backend/tests` collects and passes it
- [ ] 2.4 Add `backend/check.sh` running `ruff check`, `mypy`, then `pytest
  --cov=app --cov-branch --cov-fail-under=95` in order, per `design.md` decision 3;
  verify it exits 0 on a clean checkout with only the smoke test present (coverage of
  an empty `app/` package is vacuously 100%; this becomes a meaningful gate once
  `backend-layered-architecture` adds `backend/app`)

## 3. Frontend tooling (frontend)

- [ ] 3.1 Scaffold `frontend/` with Vite's `react-ts` template, per `design.md`
  decision 4; verify `npm install && npm run build` succeeds
- [ ] 3.2 Add ESLint and `tsc` configuration for the scaffold; verify `npx eslint .`
  and `npx tsc --noEmit` both run and exit 0 on the untouched scaffold
- [ ] 3.3 Add Vitest configuration and one smoke test (renders the scaffold's default
  component); verify `npx vitest run` passes
- [ ] 3.4 Add `frontend/check.sh` running `eslint`, `tsc --noEmit`, then `vitest run
  --coverage`, per `design.md` decision 3; verify it exits 0 on a clean checkout

## 4. Pre-commit and secrets (backend)

- [ ] 4.1 Add root `.pre-commit-config.yaml` with the `detect-secrets` hook, per
  `design.md` decision 5; verify `pre-commit run --all-files` passes on a clean
  checkout
- [ ] 4.2 Generate `.secrets.baseline` via `detect-secrets scan`; verify it exists and
  hand-review it for a real secret before committing
- [ ] 4.3 Add root `.env.example` listing the environment variables already known from
  `backend-layered-architecture` decision 4 (the `dec_app` and `dec_normatives`
  connection strings); verify the file lists at least these, each with a placeholder
  value, no real credential
- [ ] 4.4 [blocked: WP5] Add a local pre-commit hook comparing
  `backend/app/core/config.py`'s Pydantic settings fields against `.env.example` keys;
  verify a field missing from `.env.example` fails `pre-commit run`

## 5. Import contract (backend)

- [ ] 5.1 [blocked: WP5] Add an `[tool.importlinter]` "layers" contract to
  `backend/pyproject.toml`, naming `backend-layered-architecture`'s layer packages, and
  wire it into `backend/check.sh`; verify a test case with a deliberate upward import
  fails the check, per this change's "Import contract check" requirement

## 6. Documentation (backend)

- [ ] 6.1 Add a line to `CLAUDE.md`'s "Commands that exist today" naming
  `backend/check.sh` and `frontend/check.sh`, once both exit 0 on a clean checkout;
  remove them from the "TBD" list; show the edit as a diff before committing, per
  `CLAUDE.md`'s own "Do not change without agreement" note on shared files (this one is
  Akim's own file, no agreement needed, but still shown)
- [ ] 6.2 Record `pre-commit install` as a one-time per-machine setup step in
  `CLAUDE.md` (same section as task 6.1, next to the commands it applies to); verify
  the line is present after the edit

## 7. Close

- [ ] 7.1 `tester` issues the full verdict: both `check.sh` scripts pass, `pre-commit
  run --all-files` passes, coverage >= 95% in each zone (trivial on the smoke tests
  alone), delta spec matches the implementation (see DOD)
- [ ] 7.2 Reviewed by Egor or the orchestrator before merge to `develop`
  (`development-process` "Review before merge"; this change is not code-free)
- [ ] 7.3 `spec-keeper` syncs the delta into
  `openspec/specs/development-process/spec.md` and archives the change

## Dependencies

- None to start sections 1-4 and 6 (task 4.4 excepted). Section 5 and task 4.4 need
  `backend-layered-architecture` (WP5) tasks 1.1 and 2.1 respectively; they stay
  `[blocked: WP5]` until then and do not gate this change's own GO.
- Task 7.3 (archive) needs 7.1 and 7.2.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task 1.2)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements recorded (security: secret scan; `design.md` Risks)
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branches defined (above)
- [x] Dependencies satisfied to start: none; the two `[blocked: WP5]` tasks are named
  and do not block this change's own GO

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4). This change has
  code (config files, scripts, a frontend scaffold), so it uses the normal test and
  coverage path, not the code-free path.
- For the spec phase: `openspec validate --all --strict` passes; a `spec-reviewer`
  report on the current version of the change lists no blocker and no major finding.
- For implementation: `backend/check.sh` and `frontend/check.sh` each exit 0 on a
  clean checkout; `pre-commit run --all-files` passes; branch coverage is >= 95% in
  each zone (the smoke tests alone make this trivial, since no application code exists
  yet); the delta spec matches the implementation; reviewed before merge (task 7.2).
  Tasks 4.4 and 5.1 (`[blocked: WP5]`) are not required for this change's own GO; they
  are picked up once `backend-layered-architecture` unblocks them, in a follow-up
  change or task.
- NO-GO: validation fails; an unresolved blocker; either `check.sh` exits non-zero on a
  clean checkout; coverage below 95%; `pre-commit run --all-files` fails; a root
  `pyproject.toml`, `tests/`, or any other file in the pipeline's zone is touched.
- Archive (task 7.3) happens only after GO.
