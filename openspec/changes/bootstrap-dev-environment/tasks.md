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

- [x] 2.1 Add `backend/pyproject.toml` with `[tool.ruff]`, `[tool.mypy]`,
  `[tool.pytest.ini_options]`, `[tool.coverage.run]`/`[tool.coverage.report]`, per
  `design.md` decisions 1 and 3; verify `ruff check backend/` and `mypy backend/` run
  without a config error on an empty tree (2026-09-27: `ruff check backend/` passes,
  exit 0; `mypy backend/` exits 2 for "no .py files", not a config error — config
  validity confirmed separately via `mypy --config-file=backend/pyproject.toml -c
  "x: int = 1"`, exit 0; see `docs/reports/WP6-code-journal.md`)
- [x] 2.2 Add `backend/requirements.txt` (empty for now) and
  `backend/requirements-dev.txt` (`ruff`, `mypy`, `pytest`, `pytest-cov`,
  `import-linter`); verify `pip install -r backend/requirements-dev.txt` succeeds in a
  fresh `.venv` (2026-09-27: all 19 packages installed in a fresh `backend/.venv`, no
  errors)
- [x] 2.3 Add `backend/tests/` with one smoke test asserting the venv and pytest
  config work; verify `pytest backend/tests` collects and passes it (2026-09-27:
  `test_smoke.py` added, `1 passed` from both the repo root and `backend/`)
- [x] 2.4 Add `backend/check.sh` running `ruff check`, `mypy`, then `pytest`, per
  `design.md` decision 3; verify it exits 0 on a clean checkout with only the smoke
  test present. The coverage gate (`--cov=app --cov-branch --cov-fail-under=95`) only
  runs when `backend/app/` exists — confirmed 2026-09-27 that an unconditional gate
  against a nonexistent `app/` reports 0% coverage and fails, not "vacuously 100%" as
  first assumed here; `check.sh` runs plain `pytest` until `backend-layered-architecture`
  adds `backend/app`, then the gate becomes active with no further script change.
  Verified: `backend/check.sh` exits 0 on the current tree (`ruff check .` →
  `All checks passed!`; `mypy .` → `Success: no issues found in 1 source file`;
  `pytest` → `1 passed`); a deliberate unused-import violation made it exit 1
  (`ruff` F401), confirming the gate is real. Evidence:
  `docs/reports/WP6-code-journal.md` row 2.4

## 3. Frontend tooling (frontend)

- [x] 3.1 Scaffold `frontend/` with Vite's `react-ts` template, per `design.md`
  decision 4; verify `npm install && npm run build` succeeds (2026-09-28: `npm create
  vite@latest frontend -- --template react-ts`, then `npm install && npm run build`;
  builds `dist/` cleanly, exit 0)
- [x] 3.2 Add ESLint and `tsc` configuration for the scaffold; verify `npx eslint .`
  and `npx tsc --noEmit` both run and exit 0 on the untouched scaffold (2026-09-28:
  current `create-vite react-ts` ships `oxlint`, not ESLint, by default — removed it
  (`.oxlintrc.json`, the `oxlint` dependency) and added `eslint`/`typescript-eslint`/
  `eslint-plugin-react-hooks`/`eslint-plugin-react-refresh` with a flat
  `eslint.config.js`, per `design.md`'s own open question that the config format is an
  implementation detail; `npx eslint .` exits 0. `npx tsc --noEmit` also exits 0 but
  was found to silently no-op: the scaffold's root `tsconfig.json` is solution-style
  (`"files": []`, only `references`), so plain `tsc --noEmit` checks nothing — confirmed
  by appending a deliberate type error and getting exit 0 anyway. `npx tsc -b` (build
  mode, which follows the references; each referenced config already sets
  `noEmit: true`) does real checking — confirmed catching the same deliberate error,
  exit 2. `frontend/check.sh` (3.4) and this task's own verification use `tsc -b`, not
  the literal `tsc --noEmit` in this task's own text)
- [x] 3.3 Add Vitest configuration and one smoke test (renders the scaffold's default
  component); verify `npx vitest run` passes (2026-09-28: `vitest`,
  `@vitest/coverage-v8`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom`
  added; `vite.config.ts` gets a `test` block (`jsdom`, setup file, v8 coverage,
  branches threshold 95 per the DOD's frontend coverage gate); `src/test/setup.ts`
  imports `@testing-library/jest-dom/vitest`; `src/App.test.tsx` renders `<App />` and
  asserts the "Get started" heading; `npx vitest run` — 1 passed, exit 0)
- [x] 3.4 Add `frontend/check.sh` running `eslint`, `tsc --noEmit`, then `vitest run
  --coverage`, per `design.md` decision 3; verify it exits 0 on a clean checkout
  (2026-09-28: script runs `eslint .`, `tsc -b` (see 3.2 on why `-b` not
  `--noEmit`), `vitest run --coverage`, `set -euo pipefail` so it stops at the first
  failure; exits 0 on the current tree — coverage 100% branches on the smoke test
  alone; a deliberate unused-var violation made it exit 1 at the `eslint` step,
  confirming the stop-at-first-failure behavior. Evidence:
  `docs/reports/WP6-code-journal.md`)

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
  run --all-files` passes, frontend coverage >= 95% (trivial on the smoke test alone);
  the delta spec matches the implementation. Backend coverage is not gated while
  `backend/app/` does not exist (`design.md` decision 3), so `backend/check.sh` produces
  no coverage number to check — how this reads against the base "Test gate" and
  "Go/No-Go verdict" requirements is an open question (`design.md`, Open Questions),
  not resolved by this change; resolve it (team decision recorded in
  `docs/decisions/`, or a follow-up spec change) before this task is checked off
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
  clean checkout; `pre-commit run --all-files` passes; frontend branch coverage is
  >= 95% (the smoke test alone makes this trivial, since no application code exists
  yet); the delta spec matches the implementation; reviewed before merge (task 7.2).
  Backend coverage is not gated while `backend/app/` does not exist (`design.md`
  decision 3); whether that is acceptable for this change's own GO, or holds the GO
  until `backend/app/` exists, is the open question in `design.md` and must be
  resolved before task 7.1 is checked off — this DOD does not presuppose an answer.
  Tasks 4.4 and 5.1 (`[blocked: WP5]`) are not required for this change's own GO; they
  are picked up once `backend-layered-architecture` unblocks them, in a follow-up
  change or task.
- NO-GO: validation fails; an unresolved blocker; either `check.sh` exits non-zero on a
  clean checkout; frontend coverage below 95%; `pre-commit run --all-files` fails; a
  root `pyproject.toml`, `tests/`, or any other file in the pipeline's zone is touched;
  or task 7.1's open question (backend coverage applicability) is unresolved.
- Archive (task 7.3) happens only after GO.
