# Design

## Context

See `proposal.md` (Why) for the motivation. Two facts shape this design:

- The normative pipeline (Egor's zone) already has a working root `pyproject.toml`
  (`ruff`, `mypy`-typed code, `pytest` with branch coverage scoped to
  `normatives_pipeline`) and a root `tests/`. Neither `backend/` nor `frontend/`
  exists yet; the app code for both is other changes' work
  (`backend-layered-architecture` for the backend layout;
  `calculation-core-contract`/`calculation-verification` for calculation code; no
  change yet scaffolds a frontend project).
  Update 2026-10-03: the pipeline moved to `ml/` (commit `24797f7`), with its own
  `ml/pyproject.toml` and `ml/tests/`; the repository root has no `pyproject.toml` and no
  `tests/` any more. Wherever this design says the pipeline's or the root
  `pyproject.toml` or `tests/`, read `ml/pyproject.toml` and `ml/tests/`.
- No dependency manifest exists anywhere in the repository yet (not even for the
  pipeline): packages are installed by hand into a `.venv`. This change fixes that for
  the backend zone only; the pipeline's manifest is Egor's to add (he added it in his
  `pyproject.toml`, now `ml/pyproject.toml`).

## Goals / Non-Goals

**Goals:**
- A backend command and a frontend command each a developer or an agent can run
  locally, today, on a clean checkout, that exit 0.
- Zero risk of an edit to backend or frontend tooling ever touching the pipeline's
  `pyproject.toml` or `tests/`, or the reverse.
- A place for the import-contract check and the config/`.env.example` check to attach
  once their dependencies (`backend-layered-architecture`'s layers; `backend/app/core/
  config.py`) exist, without redesigning the command later.

**Non-Goals:**
- Docker, CI, or any change to the pipeline's tooling: see `proposal.md` (Non-goals).
- A build system for shipping the frontend (bundler production config, deployment):
  only the dev/lint/type/test path is in scope.
- The calculation engine's C/C++ hot-swap boundary is untouched: it is the pure
  function `(typed inputs, resolved parameters) -> result envelope` defined in
  `calculation-core-contract`'s `design.md` (decision 1). This change's `ruff`/`mypy`
  config applies uniformly across backend layers, including the future `engine/`
  package; it does not special-case it or otherwise touch that boundary.

## Decisions

1. **`backend/pyproject.toml`, separate from the root file.** Backend `ruff`, `mypy`,
   `pytest`, and `coverage` configuration lives in `backend/pyproject.toml`, not the
   root one. Rationale: keeps each zone's coverage number and lint pass scoped to its
   own code (a shared file and a shared number would violate `AGENTS.md`'s "code MUST
   NOT overlap across zones"), and means neither developer ever edits the other's
   tooling file. Alternative considered: one root file with per-directory
   `[tool.ruff.per-file-ignores]`-style scoping — rejected, still one shared file both
   zones must agree on, and `coverage`'s `source` list would need to name both zones or
   be run twice anyway, so the separation buys nothing.
   Update 2026-10-03: with the pipeline's file moved to `ml/pyproject.toml`, the root
   has no Python tool config; each zone keeps its own (`backend/`, `ml/`).

2. **Backend dependencies: `requirements.txt` + `requirements-dev.txt`, `.venv`.**
   Matches the pipeline's own convention (`.venv/bin/python`, no lockfile tool) instead
   of introducing `poetry` or `uv`, which the team has not used yet. Alternative
   considered: adopt `uv` for its speed and lockfile — deferred, not rejected; nothing
   in the specs or this design depends on the choice, so it can change later without a
   spec update (see Open Questions).

3. **One command per zone, as a shell script.** `backend/check.sh` runs `ruff check`,
   `mypy`, then `pytest`, in that order, and stops at the first failure. The coverage
   gate (`--cov=app --cov-branch --cov-fail-under=95`) only runs when `backend/app/`
   exists; before that, `pytest` runs plain, the same deferred pattern as the
   import-contract check (decision 6) and the config/`.env.example` check (decision 5).
   Confirmed 2026-09-27: `pytest --cov=app` against a nonexistent `app/` does not
   vacuously pass at 100% as first assumed here — `pytest-cov` reports "Module app was
   never imported" and 0% coverage, which fails the 95% gate, so an unconditional gate
   would keep `check.sh` red until `backend-layered-architecture` lands. `frontend/
   check.sh` runs `eslint`, `tsc --noEmit`, then `vitest run --coverage`. Rationale: the
   target is a single command that exits 0 on a clean checkout (this change's own goal,
   see `proposal.md`); a shell script needs no new build tool (`make`, `nox`, `tox`).
   Documented in `CLAUDE.md`'s "Commands that exist today" once it works, per that
   file's own instruction not to invent commands that are not set up yet. Confirmed
   2026-09-28: `frontend/check.sh` runs `tsc -b`, not `tsc --noEmit` as first assumed
   here — the Vite `react-ts` scaffold's root `tsconfig.json` is solution-style
   (`"files": []`, only `references`), so a bare `tsc --noEmit` silently checks
   nothing; `tsc -b` follows the references and each one already sets `noEmit: true`,
   so it type-checks without emitting.

4. **Frontend project skeleton: Vite + React + TypeScript.** `frontend/` is scaffolded
   with Vite's `react-ts` template. Rationale: Create React App is unmaintained and the
   React team no longer recommends it; the product is a single-page "unified web
   interface" (`product-vision`), not a multi-route server-rendered site, so
   Next.js-level framework weight is not needed; Vitest is designed to share Vite's
   config and transform pipeline, which keeps `frontend/check.sh` simple. This is a
   dev-tooling choice, not a spec-level behavior, so no spec text names it (see the
   "avoid library/framework choices" rule for specs); it can change later without a
   spec change.

5. **Pre-commit: the `pre-commit` framework, `detect-secrets` for the secret scan.**
   `.pre-commit-config.yaml` at the repo root (framework-level, not zone-scoped: a
   commit can touch files from either zone) runs `detect-secrets` (baseline file
   `.secrets.baseline`) and a small local hook that compares
   `backend/app/core/config.py`'s Pydantic settings fields against `.env.example` keys
   (task depends on that file existing; see Risks). Pre-commit hooks run fast checks
   only; the full `backend/check.sh`/`frontend/check.sh` (lint+types+tests) is not part
   of the pre-commit hook, since a test suite is too slow for every commit.
   `pre-commit`'s config format is shared at the repo root, but its backend-specific
   hook only inspects `backend/`, so it does not require Egor's agreement the way
   editing his `pyproject.toml` would. Confirmed 2026-09-28: neither `pre-commit` nor
   `detect-secrets` was installed anywhere in the checkout; both are added to
   `backend/requirements-dev.txt` (same reproducible path as the other backend dev
   tools) — `detect-secrets` for the bare `scan` CLI (task 4.2), `pre-commit` for the
   hook runner itself; `.pre-commit-config.yaml`'s own `detect-secrets` hook gets a
   separate, pre-commit-managed environment from the pinned `rev`. `.env.example`
   (task 4.3) names its two variables `DEC_APP_DATABASE_URL` and
   `DEC_NORMATIVES_DATABASE_URL` — Akim's own interim choice, since neither
   `backend-layered-architecture` decision 4 nor its (still pending) task 2.1 fixes a
   literal variable name for the two databases it names; task 4.4's config/`.env.example`
   cross-check, once unblocked, is what will confirm or correct this naming.

6. **Import-contract check: `import-linter`.** Added as a backend dev dependency now;
   its `[tool.importlinter]` "layers" contract, naming
   `backend-layered-architecture`'s layer packages, is written once that change's
   `backend/app` package layout exists (task recorded as blocked on it, not
   implemented as a no-op or silently skipped).

## Risks / Trade-offs

- **The `.env.example`/config cross-check has nothing to compare against until
  `backend/app/core/config.py` exists** (`backend-layered-architecture` task 2.1).
  Mitigation: the hook is written to pass trivially (nothing to check) when that file
  is absent, the same pattern as the import-contract check, and both are named in
  `tasks.md` as depending on that file rather than silently disabled forever.
- **`detect-secrets` has false positives and false negatives**; it is a baseline
  scanner, not a guarantee. Mitigation: this change's own goal is "the smallest set of
  tools that lets the first code meet the DOD", not a complete security control;
  `code-security`/`owasp-security` skills remain the review-time backstop.
- **Two Python tool configs (root, now `ml/`; `backend/`) can drift in style** (e.g. `ruff`
  target Python version, rule selection) even though they must not share a file.
  Mitigation: `backend/pyproject.toml`'s `ruff`/`mypy` settings are copied from the
  root file's values (now `ml/pyproject.toml`) where nothing zone-specific applies (e.g. Python target version),
  recorded once in this design so a future diff is a deliberate choice, not drift.

## Open Questions

- Exact `ruff` rule selection and `mypy` strictness level (`--strict` or a narrower
  set) for the backend: an implementation detail, does not change this change's
  requirements or tasks.
- Whether to adopt `uv` later instead of `requirements.txt` + `.venv` (decision 2):
  deferred; no spec or task depends on which one is used.
- ESLint flat config (`eslint.config.js`) vs the legacy `.eslintrc` format for the
  frontend: an implementation detail of task 2.1.
- **How the base `development-process` "Test gate with >= 95% branch coverage" and
  "Go/No-Go verdict and archive" requirements apply to a zone this change leaves
  without an `app/` package to measure (the backend zone, until
  `backend-layered-architecture` lands).** `backend/check.sh` (decision 3) does not run
  a coverage gate while `backend/app/` does not exist, so it produces no coverage
  number for that zone; whether that reads as satisfying the base requirements, as an
  exception the team needs to agree on, or as a reason to hold this change's own
  implementation-phase `tester` verdict until `backend/app/` exists, is not decided
  here. Not resolved by this change: needs a team decision (recorded in
  `docs/decisions/`) or a separate spec change, before task 7.1's `tester` verdict.
