# Repository layout: one project directory per zone (proposal for Egor)

- Date: 2026-09-28
- From: Akim. To: Egor.
- Reviewed: `origin/feature/normative-parser/ml` (commit `a28cf0a`), not merged into
  `develop` yet: `pyproject.toml`, `src/normatives_pipeline/`, `configs/`, `infra/`,
  `research/`, `tests/`, `README.md`.

Russian version: `repo-layout-symmetric-zones-egor-rus.md`.

## What changed on your branch

The pipeline moved to a src-layout with its own root project: `pyproject.toml` (project
`normatives-pipeline`, pinned dependencies, `[project.optional-dependencies] ml`),
`src/normatives_pipeline/{parser,formulas}/`, `configs/{parser,formulas}.toml`,
`infra/docker-compose.yml`, `research/`, and a root `tests/`. The old
`normatives_pipeline/ocr/` package is gone; OCR enrichment is
`src/normatives_pipeline/formulas/formula_ocr.py` now. src-layout, the `ml` extra kept
separate from the core dependencies, and `infra/` for compose are all sound; I have no
issue with the code itself.

## Why I'm asking for a change

The layout puts your project's manifest, source root, and test root at the repository
root, next to `backend/` and `frontend/` in their own directories. That makes three
problems for the zones `AGENTS.md` keeps non-overlapping:

1. **One shared `.venv`, two sets of pins.** `backend/requirements.txt` will carry
   NumPy/SciPy for the calculation engine. Your root `pyproject.toml` pins
   `numpy==2.5.3`, `scikit-learn==1.9.1`, `psycopg2-binary==2.9.13`, and an `ml` extra
   with `doclayout-yolo`, `pix2text`. Installed into one venv, these two sets can drift
   apart or conflict; installing your `[ml]` extra would also pull ML dependencies into a
   backend environment that should have none (`agent-docs/domain-constraints.md`: "No ML
   in the calculation path").
2. **Root `tests/` reads as the repository's test suite, but it is only the pipeline's.**
   There is no directory left for tests that cross zones (a future engine-vs-pipeline
   integration check).
3. **The backend/frontend import boundary has nothing to check it against.** WP6 task 5.1
   plans `import-linter` inside `backend/`, but nothing stops `backend/` from importing
   `normatives_pipeline` at the root the way it could import any other top-level package.

`README.md`'s "Repository layout" also does not mention `backend/` or `frontend/` yet, and
still says "task sub-branches" (old branching model, see
`docs/decisions/branching-model-update-egor.md`).

## Proposal (variant B)

Move your project into its own directory, `normatives/`, so every zone's code lives in a
symmetric project directory with its own manifest:

```
backend/        app/, alembic/, params/, tests/, pyproject.toml, requirements*.txt, check.sh
frontend/       src/, e2e/, package.json, check.sh
normatives/     pyproject.toml, src/normatives_pipeline/, configs/, tests/, research/
infra/          docker-compose.yml
tests/          cross-zone tests only (empty for now)
```

Root keeps only what is genuinely shared: `.pre-commit-config.yaml`, `.editorconfig`,
`AGENTS.md`, `CLAUDE.md`, `openspec/`, `docs/`, `agent-docs/`, `infra/`.

This is your project and your root `pyproject.toml` (`AGENTS.md`, "Do not change without
agreement" also names it as shared with me), so the move and its exact shape are your
call. What I'm asking is that the pipeline gets its own directory and its own venv,
separate from `backend/`'s.

## What Akim asks of Egor

1. Agree to variant B (move `normatives_pipeline` under `normatives/` with its own
   `pyproject.toml`), or propose the alternative you prefer, as long as it keeps a
   separate manifest and a separate venv from `backend/`.
2. If you agree, say when: before this branch merges into `develop` (cheapest, nothing
   depends on the paths yet) or after, as a follow-up.
3. Update `README.md`'s "Repository layout" and setup commands for the new paths, and
   drop the "task sub-branches" line per the branching-model note.
4. Confirm the root `tests/` (or `normatives/tests/` under variant B) stays yours; I will
   not add files there.

Not asked here: anything about `ml-model-storage` or the infra change, both still yours
and still not created.
