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

## Answers

- Date: 2026-10-03
- From: Akim. To: Egor.

Done, on `develop`, against the layout you merged on 2026-10-03 (`24797f7`), so the paths
are `ml/...`, not the `src/` and `configs/` of the mapping above.

1. **`calculation-core-contract`** (`80a684a`, `a984b28`): `formulas.toml` is cited as
   `ml/configs/formulas.toml`, marked "to be deleted" (your answer A3). The citation of
   `docs/audit/01-recon.md:97` is replaced by its content in `design.md` and in
   `proposal.md`. `tasks.md` had no path of yours left.
2. **`backend-layered-architecture`** (`80a684a`, `a984b28`): `infra/docker-compose.yml`
   in the section 3 note and the DOR; `ml/src/normatives_pipeline/` in `design.md` and
   `proposal.md`; the OCR row of "Moved out" names `ml/` as it is now; `formulas.toml` as
   above.
3. **`CLAUDE.md`** (`277fcc7`): the "Status" section is rewritten for the merged layout
   (`ml/`, `infra/`, no root `pyproject.toml` or `tests/`), and the pipeline commands use
   `pip install -e "./ml[ml]"` and `infra/docker-compose.yml`.

Also changed for the same move: `bootstrap-dev-environment` (the pipeline's tooling is
`ml/pyproject.toml`) and `calculation-api` (`infra/docker-compose.yml`), in `11bdca4` and
`a984b28`. Old paths remain in my changes only as dated history ("at the time of writing", "now `ml/...`").
