# For Akim: fix stale paths after the src-layout reorganization

- Date: 2026-09-28
- From: Egor (data engineer)
- To: Akim (frontend/backend) and your Claude Code sessions

## Context

The pipeline moved to a src-layout and configs moved to `configs/` — see
`repo-reorganization-src-layout.md`. Your OpenSpec changes and `CLAUDE.md` still cite the
old filesystem paths. Module names and the formula contract did **not** change; only the
paths on disk did.

## Path mapping

| Old path | New path |
|---|---|
| `normatives_pipeline/` (top level) | `src/normatives_pipeline/` |
| `normatives_pipeline/ocr/` | `src/normatives_pipeline/formulas/` |
| `normatives_pipeline/formulas.toml` | `configs/formulas.toml` |
| `normatives_pipeline/parser.toml` | `configs/parser.toml` |
| `docker-compose.yml` (root) | `infra/docker-compose.yml` |
| `norm-docs/` | `docs/normative-base/` |

## Files to edit

### `openspec/changes/calculation-core-contract/`

- `design.md:220` — `normatives_pipeline/formulas.toml` -> `configs/formulas.toml`.
- `tasks.md:63` — `normatives_pipeline/formulas.toml` -> `configs/formulas.toml`.
- `design.md:196` — `docs/audit/01-recon.md:97` (this file is untracked/missing;
  restate the point inline or drop the citation — pre-existing, not caused by the move).

### `openspec/changes/backend-layered-architecture/`

- `tasks.md:41` — `docker-compose.yml` -> `infra/docker-compose.yml`.
- `tasks.md:59` — `docker-compose.yml` -> `infra/docker-compose.yml`.
- `tasks.md:56` — `normatives_pipeline/` -> `src/normatives_pipeline/`.
- `tasks.md:58` — `formulas.toml` -> `configs/formulas.toml`.
- `tasks.md:60` — `normatives_pipeline/ocr/` -> `src/normatives_pipeline/formulas/`.

### `CLAUDE.md`

- `:16` — `normatives_pipeline/formulas.toml` -> `configs/formulas.toml`.
- `:13` — the "Status" line still says `docker-compose.yml` does not exist; it now lives
  at `infra/docker-compose.yml` on the pipeline branch. Refresh when the branch merges.

## What did not change

- Module names: `normatives_pipeline`, `search.query()`, payload shape.
- Entry points, except `enrich` is now `normatives_pipeline.formulas.enrich`.
