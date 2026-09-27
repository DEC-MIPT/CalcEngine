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
- No dependency manifest exists anywhere in the repository yet (not even for the
  pipeline): packages are installed by hand into a `.venv`. This change fixes that for
  the backend zone only; the pipeline's manifest is Egor's to add.

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

2. **Backend dependencies: `requirements.txt` + `requirements-dev.txt`, `.venv`.**
   Matches the pipeline's own convention (`.venv/bin/python`, no lockfile tool) instead
   of introducing `poetry` or `uv`, which the team has not used yet. Alternative
   considered: adopt `uv` for its speed and lockfile — deferred, not rejected; nothing
   in the specs or this design depends on the choice, so it can change later without a
   spec update (see Open Questions).

3. **One command per zone, as a shell script.** `backend/check.sh` runs `ruff check`,
   `mypy`, then `pytest --cov=app --cov-branch --cov-fail-under=95`, in that order, and
   stops at the first failure. `frontend/check.sh` runs `eslint`, `tsc --noEmit`, then
   `vitest run --coverage`. Rationale: the target is a single command that exits 0 on a
   clean checkout (this change's own goal, see `proposal.md`); a shell script needs no
   new build tool (`make`, `nox`, `tox`).
   Documented in `CLAUDE.md`'s "Commands that exist today" once it works, per that
   file's own instruction not to invent commands that are not set up yet.

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
   editing his `pyproject.toml` would.

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
- **Two Python tool configs (root, `backend/`) can drift in style** (e.g. `ruff`
  target Python version, rule selection) even though they must not share a file.
  Mitigation: `backend/pyproject.toml`'s `ruff`/`mypy` settings are copied from the
  root file's values where nothing zone-specific applies (e.g. Python target version),
  recorded once in this design so a future diff is a deliberate choice, not drift.

## Open Questions

- Exact `ruff` rule selection and `mypy` strictness level (`--strict` or a narrower
  set) for the backend: an implementation detail, does not change this change's
  requirements or tasks.
- Whether to adopt `uv` later instead of `requirements.txt` + `.venv` (decision 2):
  deferred; no spec or task depends on which one is used.
- ESLint flat config (`eslint.config.js`) vs the legacy `.eslintrc` format for the
  frontend: an implementation detail of task 2.1.
