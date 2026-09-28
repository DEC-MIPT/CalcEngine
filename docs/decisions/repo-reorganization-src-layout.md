# Repo reorganization: src-layout, configs/, infra/, formulas/ subpackage

- Date: 2026-09-28
- From: Egor (data engineer)
- To: Akim (frontend/backend), team

## Why

The pipeline lived in a flat `normatives_pipeline/` directory with configs and research
artifacts mixed in, and root-level docs/docker files were scattered. This reorganizes the
repo into a conventional src-layout so a fresh clone and a new session start from a clean,
predictable structure.

## What changed

| Before | After |
|---|---|
| `normatives_pipeline/` (code) | `src/normatives_pipeline/` |
| `normatives_pipeline/parser.toml` | `configs/parser.toml` |
| `normatives_pipeline/formulas.toml` | `configs/formulas.toml` |
| `normatives_pipeline/research/` | `research/` |
| `normatives_pipeline/{formula_ocr,enrich,validation}.py` | `src/normatives_pipeline/formulas/{detect,enrich,validation}.py` |
| `norm-docs/` (gitignored PDFs) | `docs/normative-base/` |
| `docker-compose.yml` | `infra/docker-compose.yml` |
| `verified-roadmap*.md` (repo root) | `docs/reports/verified-roadmap*.md` |

`pyproject.toml` now declares packaging: `[build-system]`, `[project]`, core dependencies
(pdfplumber, psycopg2-binary, pymorphy3, pymorphy3-dicts-ru, scikit-learn, numpy, sympy)
and `ml` extras (latex2sympy2, doclayout-yolo, pix2text). The formula config section was
renamed `[formula_ocr]` -> `[detect]` (`detect_config()`).

## Setup (changed)

```bash
pip install -e ".[ml]"                              # core + formula-extraction extras
docker compose -f infra/docker-compose.yml up -d    # Postgres (dec-postgres, port 5433)
export DEC_DATABASE_URL="postgresql://dec:dec@localhost:5433/dec"
python -m normatives_pipeline.ingest --force "docs/normative-base/СП 22.13330.2016.pdf"
python -m normatives_pipeline.formulas.enrich       # formula extraction (needs .[ml])
```

## Impact on Akim

- **Contract unchanged.** Module names (`normatives_pipeline`, `search.query()`,
  payload shape) are the same; only filesystem paths moved.
- `search.query()` / `ingest` / `formulas.enrich` entry points keep their `python -m`
  module names except `enrich`, which is now `normatives_pipeline.formulas.enrich`.
- Editable install resolves the antlr4 conflict by downgrading `omegaconf` to 2.0.6;
  `pillow` is now 12.3.0 (pdfplumber requires >=12.2.0), `pypdfium2` 5.13.0.

## Notes

- Gitignored: `packages/`, `docs/normative-base/`, `research/{pages,crops,data}/`,
  `.kilo/plans/`, `*.egg-info/`.
- Offline install: `pip download ".[ml]" -d packages/` then
  `pip install --no-index --find-links packages/ -e ".[ml]"`.
- `agent-docs/` stays at the repo root (moving it under `docs/` was reverted: it would
  have left 30+ stale references and changed the "no code" definition in OpenSpec specs).
