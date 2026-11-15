# DEC — Design Engineer's Calculator

Cloud web service for automating engineering calculations with a verified normative
base (SP/GOST/SNiP), a transparent ("white box") calculation engine, and GOST-compliant
report generation.

## Current development ownership

Akim is the sole active developer. Egor has left the team; there is no replacement
until Akim announces one. Second-human-developer confirmations are not required in
this mode. Independent agent reviews, tester verdicts, engineering verification and
the PM's product/legal authority remain in place. See
[the recorded decision](docs/decisions/backend/2026-11-15-solo-developer-document-workflow.md)
and [AGENTS.md](AGENTS.md) for the current workflow.

## Stack

- Backend: Python 3.12, FastAPI, Pydantic
- Calculation engine: Python (NumPy/SciPy), hot-swappable to C/C++ later
- Database: PostgreSQL (normative catalog `dec_normatives`)
- Frontend: React + TypeScript, MathJax
- Reports: python-docx (MVP), reportlab (later)
- Infra: Docker locally, Russian cloud later

## Repository layout

```
backend/                       # FastAPI app, calculation engine, report generator
├── app/                       # layers: api, services, engine, reporting, repositories, schemas
├── alembic/                   # migrations of the application database dec_app
├── params/                    # engineer-set values per calculation type (no norm values)
├── tests/                     # pytest
└── check.sh                   # ruff, mypy, pytest with coverage, import contracts
frontend/                      # React + TypeScript app (see frontend/README.md)
ml/                            # normative pipeline + ML
├── pyproject.toml             # normatives-pipeline project
├── src/normatives_pipeline/   # ingestion, search, retrieval, DB access, collector
│   ├── parser/                # PDF/structural text parsing
│   └── formulas/              # formula extraction: detect, enrich, validation
├── configs/                   # parser.toml, pilot.toml, sources.toml (config-driven)
├── research/                  # formula-extraction research notebook + fixtures
└── tests/                     # pytest
infra/                         # docker-compose.yml (Postgres, dec-postgres)
agent-docs/                    # domain constraints (agents read this)
docs/decisions/                # team's written channel (decisions, journals)
docs/reports/                  # WP reports, roadmap
openspec/                      # specs and changes (Spec-Driven Development)
```

## Running the application locally

The app is three processes: PostgreSQL in Docker, the backend (FastAPI on port 8000) and the
frontend (Vite dev server on port 5173). Requirements: Python 3.12, Node.js 24 with npm,
Docker. Commands run from the repository root unless stated otherwise.

### 1. Database

```bash
docker compose -f infra/docker-compose.yml up -d    # first time: creates dec-postgres, port 5433
docker start dec-postgres                           # later runs
```

The container holds two databases: `dec` (the normative catalog) and `dec_app`
(calculation results). `dec_app` is not created by the compose file; create it once:

```bash
docker exec dec-postgres createdb -U dec dec_app
```

### 2. Normative catalog

The backend computes only with norm data from the catalog. Ingest the pilot's norm once with
the pipeline (see "Normative pipeline" below), with the reader role's password set, so that
ingestion creates the role `dec_normatives_reader` the backend connects as:

```bash
export DEC_NORMATIVES_READER_PASSWORD='<reader-password>'
python -m normatives_pipeline.ingest --force "docs/normative-base/СП 22.13330.2016.pdf"
```

The PDF is not in git (`docs/normative-base/` is gitignored); get it from the team.

### 3. Backend

```bash
python3.12 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements-dev.txt
cd backend
export DEC_APP_DATABASE_URL='postgresql://dec:<password>@localhost:5433/dec_app'
export DEC_NORMATIVES_DATABASE_URL='postgresql://dec_normatives_reader:<reader-password>@localhost:5433/dec'
export DEC_CORS_ORIGINS='http://127.0.0.1:5173'
.venv/bin/alembic upgrade head                      # once, and after each new migration
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

- `--no-access-log` keeps normative search query strings out of Uvicorn access logs.
- `DEC_CORS_ORIGINS` must hold the frontend's origin exactly (comma-separated for several).
- Without `DEC_NORMATIVES_DATABASE_URL` the backend still starts, but `POST /calculations`
  answers `503 parameter_source_unavailable`.
- The variables are listed in `.env.example`; the backend reads them from the environment,
  not from a `.env` file.
- Check: `curl http://127.0.0.1:8000/calculation-types` answers `200`; the API description is
  at `http://127.0.0.1:8000/docs`.

### 4. Frontend

```bash
cd frontend
npm ci
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev -- --host 127.0.0.1 --port 5173
```

Open `http://127.0.0.1:5173/`. Without a backend, `npm run dev:mock` serves the same screens
from mock data. More commands (Playwright, `gen:api`) are in `frontend/README.md`.

### Checks of the app

```bash
backend/check.sh                                    # uses backend/.venv
frontend/check.sh
backend/.venv/bin/pre-commit install                # once per machine
pre-commit run --all-files
```

## Development

Spec-Driven Development via OpenSpec. See `AGENTS.md` for the operating manual and
`openspec/` for specs and changes. Documentation is edited, committed and pushed only
in a checkout of `develop`, including local journals and instruction-only agent/skill
definitions. Check the target checkout's branch before writing. Code stays on its
planned feature branch; reading or importing committed documents does not permit
authoring them there. Git delivery requires explicit consent; `main` stays frozen
until the MVP.

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

Full terminal verification cycle (get PDF → ingest → read → independent comparison of every
document): `ml/research/VERIFY.md`. Stack, rationale and open work: `ml/research/PIPELINE.md`.

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
