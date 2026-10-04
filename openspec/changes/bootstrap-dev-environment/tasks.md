# Tasks

Owner: Akim (tooling commands and pre-commit, this change; Docker Compose and CI are
Egor's and not part of this change). Branch: sections 2-4.3 were done on `feature/bootstrap-dev-environment/backend` and
`feature/bootstrap-dev-environment/frontend` and are already merged into `develop`. The
remaining code (4.4, 4.5, 4.6 and 5.1) goes on `feature/dev-environment/backend`
from `develop`; documents (section 6, and the note of task 4.5) go directly to `develop`. Checkboxes in this file are ticked in `develop` as each subtask is done on the feature branch; the code reaches `develop` only when the whole feature is done (`AGENTS.md`, Branching rules).

Marker **[blocked: WP5]**: the task needs `backend-layered-architecture`'s layered
`backend/app` structure (its task 1.1) or its config module (its task 2.1) before it
can be implemented; until then it is not started, not stubbed as a no-op. Lifted
2026-10-04: both WP5 tasks are done and merged into `develop` (`53a4892`), so tasks 4.4
and 5.1 no longer carry the marker.

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
  "x: int = 1"`, exit 0; see `docs/akim/reports/WP6-code-journal.md`)
- [x] 2.2 Add `backend/requirements.txt` (empty for now) and
  `backend/requirements-dev.txt` (`ruff`, `mypy`, `pytest`, `pytest-cov`,
  `import-linter`); verify `pip install -r backend/requirements-dev.txt` succeeds in a
  fresh `.venv` (2026-09-27: all 19 packages installed in a fresh `backend/.venv`, no
  errors)
- [x] 2.3 Add `backend/tests/` with one smoke test asserting the venv and pytest
  config work; verify `pytest backend/tests` collects and passes it (2026-09-27:
  `test_smoke.py` added, `1 passed` from both the repo root and `backend/`; re-checked
  2026-10-03 on `develop` with no root `pyproject.toml`: `pytest backend/tests` from the
  root takes `backend/pyproject.toml` as its config, `32 passed`)
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
  `docs/akim/reports/WP6-code-journal.md` row 2.4

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
  `docs/akim/reports/WP6-code-journal.md`)

## 4. Pre-commit and secrets (backend)

- [x] 4.1 Add root `.pre-commit-config.yaml` with the `detect-secrets` hook, per
  `design.md` decision 5; verify `pre-commit run --all-files` passes on a clean
  checkout (2026-09-28: neither `pre-commit` nor `detect-secrets` was installed
  anywhere in the checkout — added both to `backend/requirements-dev.txt`, installed
  into `backend/.venv`; `.pre-commit-config.yaml` runs the `Yelp/detect-secrets`
  hook (`rev: v1.5.0`) against `.secrets.baseline`. `backend/.venv/bin/pre-commit run
  --all-files` → `Passed`, exit 0, once the baseline (4.2) existed. Verified the gate
  is real: a staged file with a fake AWS key not in the baseline made it fail
  (`Failed`, exit 1, "Potential secrets about to be committed"); removed after the
  check. See `docs/akim/reports/WP6-code-journal.md`)
- [x] 4.2 Generate `.secrets.baseline` via `detect-secrets scan`; verify it exists and
  hand-review it for a real secret before committing (2026-09-28:
  `backend/.venv/bin/detect-secrets scan --exclude-files 'package-lock\.json' >
  .secrets.baseline` (the lockfile's SHA-512 hashes are the one predictable noise
  source; everything else is git-tracked-only by `detect-secrets`' own default, so
  `node_modules`/`.venv`/`dist`/`coverage` never entered the scan). 11 findings across
  10 files, all hand-reviewed, none a real secret: the repeated "Basic Auth
  Credentials"/"Secret Keyword" hits are the single shared `dec:dec` local-only
  Postgres dev credential already used across `docker-compose.yml`,
  `tests/conftest.py` (now `infra/docker-compose.yml` and `ml/tests/conftest.py`, moved
  2026-10-03; see 4.5), and several `docs/decisions/`/`docs/akim/reports/` files (confirmed
  by reading each flagged line); the "Base64 High Entropy String" in
  `normatives_pipeline/research/research.ipynb` (now `ml/research/research.ipynb`) is a base64 PNG image output
  (confirmed via the notebook's own JSON); the "Hex High Entropy String" in
  `skills-lock.json` is a skill content hash. Regenerated once more after 4.3 added
  `.env.example`'s own placeholder credential (see 4.3))
- [x] 4.3 Add root `.env.example` listing the environment variables already known from
  `backend-layered-architecture` decision 4 (the `dec_app` and `dec_normatives`
  connection strings); verify the file lists at least these, each with a placeholder
  value, no real credential (2026-09-28: `backend-layered-architecture` decision 4
  names the two databases but fixes no variable name — its task 2.1 (`core/config.py`)
  is still pending — so this task picks `DEC_APP_DATABASE_URL` and
  `DEC_NORMATIVES_DATABASE_URL` as Akim's interim choice, noted in the file itself and
  in `design.md` decision 5, pending confirmation once task 2.1 lands. Both values are
  `postgresql://<user>:changeme@localhost:5433/<db>` placeholders, no real credential —
  `changeme` tripped `detect-secrets`' Basic Auth detector on the `dec_normatives` line,
  same as the team's existing `dec:dec` convention; folded into the 4.2 baseline after
  hand-review)
- [ ] 4.4 Add a local pre-commit hook comparing
  `backend/app/core/config.py`'s Pydantic settings fields against `.env.example` keys;
  verify a field missing from `.env.example` fails `pre-commit run` (2026-10-04:
  unblocked; the settings now span several classes, `Settings`, `ApiSettings` from
  `calculation-api` and `NormativesSettings` from `normative-catalog-backend` task 3.1,
  so which classes and keys the hook compares is settled when the task starts)
- [ ] 4.5 Regenerate `.secrets.baseline` (added 2026-10-03, `spec-reviewer` finding):
  after Egor's move of 2026-10-03 (`ml/`, `infra/`) the baseline names five files that
  no longer exist, and it does not cover the backend files merged after 4.2, so
  `pre-commit run --all-files` fails on `develop`. Re-run the scan of 4.2 on
  `feature/dev-environment/backend`, hand-review every finding (file, line, why it is not
  a real secret, as in 4.2), and record in `docs/decisions/secrets-baseline-egor-files.md`
  (committed to `develop`) which files of Egor's zone the baseline lists, so he knows the
  hook covers them; the baseline is Akim's file, and no file of Egor's zone is edited
  (backend); verify: `pre-commit run --all-files` exits 0 on that branch after
  `git merge develop`, a staged fake key still fails it, every path in the baseline
  exists, and the note exists on `develop`
- [ ] 4.6 Align `DEC_NORMATIVES_DATABASE_URL` in `.env.example` with the read contract
  of `normative-catalog-backend` (added 2026-10-04 from Egor's answers in
  `docs/decisions/normative-catalog-backend-contract-akim.md`): the placeholder names
  the reader role `dec_normatives_reader` and Egor's interim database `dec`
  (`postgresql://dec_normatives_reader:changeme@localhost:5433/dec`), and the file's
  comment says that `dec` holds the catalog until Egor's infrastructure change splits
  the databases and that the password is the one his ingestion sets from
  `DEC_NORMATIVES_READER_PASSWORD`. Egor's own variables (`DEC_DATABASE_URL`,
  `DEC_NORMATIVES_READER_PASSWORD`) are not listed: the file describes the backend
  (Akim, 2026-10-04). Done before 4.5, so its scan covers the changed line (backend);
  verify: the line names the reader role, the database `dec` and a placeholder password,
  no real credential, and `pre-commit run --all-files` passes after 4.5

## 5. Import contract (backend)

- [ ] 5.1 Add `[tool.importlinter]` contracts to `backend/pyproject.toml`,
  naming `backend-layered-architecture`'s layer packages and encoding its total layer
  order (`design.md` decision 2), and wire them into `backend/check.sh`: a "layers"
  contract (`api | worker`, `services`, `engine | parameters | reporting`,
  `repositories`, `db`, `models | schemas`, `core`; siblings as independent layers, or an
  independence contract if the installed `import-linter` does not accept `|`), a
  forbidden contract that `api` and `worker` do not import `repositories` or `models`
  (indirect imports allowed, since `api` reaches `repositories` through `services`), a
  forbidden contract that `engine` imports from the application only `schemas` and
  `core`, and, once `ml/` exists, the two `ml/` directions. Updated 2026-09-28 (WP5
  third `spec-reviewer` pass, finding M1): this task verifies WP5's dependency-direction
  requirement after WP5 is applied. Verify: a test case with a deliberate upward import,
  one with `api` importing `repositories`, and one with `engine` importing `parameters`
  each fail the check, per this change's "Import contract check" requirement

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

- None to start sections 1-4 and 6. Section 5 and task 4.4 needed
  `backend-layered-architecture` (WP5) tasks 1.1 and 2.1 respectively; both are merged
  (`53a4892`), so the `[blocked: WP5]` marker is lifted (2026-10-04). They still do not
  gate this change's own GO.
- Tasks 4.6, 4.4 and 5.1 come before 4.5, in that order, so that the one scan of 4.5
  covers every file the feature adds.
- Task 7.3 (archive) needs 7.1 and 7.2.
- Task 7.1 needs 4.5, since `pre-commit run --all-files` is part of the verdict. Apart from
  that order, task 4.5 needs nothing else. A later move of files in either zone makes the hook fail again on
  the moved files; that failure is the trigger, and the developer who sees it re-runs the
  scan of 4.5 (a manual step, no automation).

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task 1.2)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements recorded (security: secret scan; `design.md` Risks)
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branches defined (above)
- [x] Dependencies satisfied to start: none; the two tasks once `[blocked: WP5]` (4.4,
  5.1) are unblocked since 2026-10-04 and do not block this change's own GO

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
  Tasks 4.4 and 5.1 (unblocked since 2026-10-04) are not required for this change's
  own GO.
- NO-GO: validation fails; an unresolved blocker; either `check.sh` exits non-zero on a
  clean checkout; frontend coverage below 95%; `pre-commit run --all-files` fails; a
  file in the pipeline's zone (`ml/`, including its `pyproject.toml` and `tests/`, which
  were at the root until 2026-10-03) is touched;
  or task 7.1's open question (backend coverage applicability) is unresolved.
- Archive (task 7.3) happens only after GO.
