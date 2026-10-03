# Proposal

## Why

No lint, type-check, or test command exists yet for either zone: `CLAUDE.md`
("Commands that exist today") lists only `openspec` commands and says explicitly that
none of `pytest`, `ruff`, `mypy`, `eslint`, `tsc`, or `docker` is set up, and that none
should be invented or run. `calculation-core-contract` (WP2) and `calculation-verification`
(WP4) already have GO verdicts for their spec phase and open implementation tasks
requiring >= 95% branch coverage per `development-process`'s "Test gate" requirement, but
that requirement names no tool and no command a developer or an agent can actually run to
check it. The normative pipeline (Egor's zone) already has a working command set (`ruff`,
`mypy`-typed code, `pytest` with branch coverage), in `ml/` (at the repository root until
2026-10-03); Akim's zones
(backend, frontend) have none. This change wires up the smallest command set that lets
the first backend and frontend code meet the DOD, without touching Egor's zone.

## What Changes

- Adds a single backend command that runs lint (`ruff`), type checks, and tests,
  exiting 0 on a clean checkout; the tests gate on branch coverage once `backend/app/`
  exists to measure, per `design.md` decision 3. The type checker is `mypy`, not `ty`
  (`AGENTS.md` section 7 and `openspec/config.yaml` already name `mypy`; the pipeline's
  code already carries `mypy`-specific annotations).
- Adds a single frontend command that runs `eslint`, `tsc`, and `vitest` the same way.
- Adds the import contract from `backend-layered-architecture` (WP5) as part of the
  backend command, once that change defines the layered directory structure. Until then
  the check has nothing to run against; its task is recorded as blocked on WP5, not
  implemented as a no-op.
- Adds a pre-commit hook that scans staged changes for secrets, and requires
  `.env.example` to list every variable the backend's configuration reads.
- Backend tooling gets its own `backend/pyproject.toml`, separate from the pipeline's
  `ml/pyproject.toml` (at the repository root until 2026-10-03): each zone's lint, type,
  and coverage configuration and command
  stays scoped to its own code, so neither zone's coverage number or lint pass mixes
  with the other's, and edits to one zone's tooling never touch the other's file.

## Non-goals

- Docker Compose and CI: Egor's zone, not part of this change.
- Choosing `ty` over `mypy`: settled above, not reopened here.
- The application code the tooling checks: `backend-layered-architecture` (WP5) owns
  the backend's layered structure; `calculation-core-contract` (WP2) and
  `calculation-verification` (WP4) own the calculation code. This change adds only the
  minimal scaffolding (package files, one smoke test per zone) needed for its own
  commands to run and exit 0 on a clean checkout, not the application itself.
- Editing the pipeline's `pyproject.toml` or its `tests/` (at the root then, in `ml/`
  since 2026-10-03): out of scope, Egor's zone.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `development-process`: adds requirements naming the concrete backend and frontend
  tooling commands, the deferred import-contract check, and the pre-commit secret scan
  with the `.env.example` requirement. The existing "Test gate with >= 95% branch
  coverage" and "Go/No-Go verdict and archive" requirements are referenced, not
  restated or changed: this change supplies the command that lets the gate be checked,
  it does not redefine the gate itself. How that gate reads on this change's own
  backend zone — which this change deliberately leaves without an `app/` package to
  measure (see Non-goals) — is not resolved here; see `design.md`'s Open Questions.

## Impact

- New files: `backend/pyproject.toml`, `backend/tests/` (one smoke test), a frontend
  project skeleton with its own lint/type/test config and one smoke test, root
  `.pre-commit-config.yaml`, root `.env.example`.
- No change to Egor's zone: the pipeline, its `pyproject.toml` and its `tests/` (at the
  root then, all under `ml/` since 2026-10-03).
- Once merged, `calculation-core-contract` (WP2) and `calculation-verification` (WP4)
  can start their backend implementation tasks against a real coverage gate instead of
  an unenforceable one.
