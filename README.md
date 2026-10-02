# DEC — Design Engineer's Calculator

Cloud web service for automating engineering calculations with a verified normative
base (SP/GOST/SNiP), a transparent ("white box") calculation engine, and GOST-compliant
report generation.

## Stack

- Backend: Python 3.12, FastAPI, Pydantic
- Calculation engine: Python (NumPy/SciPy), hot-swappable to C/C++ later
- Database: PostgreSQL (normative catalog `dec_normatives`)
- Frontend: React + TypeScript, MathJax
- Reports: python-docx (MVP), reportlab (later)
- Infra: Docker locally, Russian cloud later

## Repository layout

```
ml/                            # Egor's zone: normative pipeline + ML
├── pyproject.toml             # normatives-pipeline project
├── src/normatives_pipeline/   # ingestion, search, retrieval, DB access, collector
│   ├── parser/                # PDF/structural text parsing
│   └── formulas/              # formula extraction: detect, enrich, validation
├── configs/                   # parser.toml, formulas.toml, sources.toml (config-driven)
├── research/                  # formula-extraction research notebook + fixtures
└── tests/                     # pytest
infra/                         # docker-compose.yml (Postgres, dec-postgres)
agent-docs/                    # domain constraints (agents read this)
docs/decisions/                # team's written channel (decisions, journals)
docs/reports/                  # WP reports, roadmap
openspec/                      # specs and changes (Spec-Driven Development)
```

## Development

Spec-Driven Development via OpenSpec. See `AGENTS.md` for the operating manual and
`openspec/` for specs and changes. All work happens on `develop` and its task
sub-branches; `main` stays frozen until the MVP.

### Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e "./ml[ml]"       # core pipeline + formula-extraction extras (project in ml/)
docker compose -f infra/docker-compose.yml up -d   # Postgres (dec-postgres, port 5433)
export DEC_DATABASE_URL="postgresql://dec:dec@localhost:5433/dec"
```

### Normative pipeline

```bash
python -m normatives_pipeline.ingest --force "docs/normative-base/СП 22.13330.2016.pdf"
python -m normatives_pipeline.search --json "условие успешного погружения опускных колодцев"
python -m normatives_pipeline.formulas.enrich   # formula extraction (needs .[ml])
```

### Checks

```bash
cd ml
pytest -q                       # branch coverage >= 95% (testpaths = tests/)
ruff check src
mypy src/normatives_pipeline
cd ..
```

### Offline install (vendored wheels)

```bash
pip download ".[ml]" -d packages/
pip install --no-index --find-links packages/ -e ".[ml]"
```

`packages/`, `docs/normative-base/`, and `ml/research/{pages,crops,data}/` are gitignored.
