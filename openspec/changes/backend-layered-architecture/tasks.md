# Tasks

## 1. Scaffold layered directory structure

- [ ] 1.1 Create `backend/app` with empty `api`, `schemas`, `models`, `repositories`, `services`, `parameters`, `engine`, `reporting`, `core`, `db`, `worker` packages
- [ ] 1.2 Create `backend/app/main.py` with a minimal FastAPI instance and a health endpoint

## 2. Core and configuration

- [ ] 2.1 Add `core/config.py` with pydantic-settings reading environment variables (app DB URL, normative DB URL)
- [ ] 2.2 Add `core/exceptions.py`, `core/logging.py` stubs

## 3. Database setup (transactional app DB)

- [ ] 3.1 Add `db/session.py` (SQLAlchemy engine + session factory for `dec_app`)
- [ ] 3.2 Add Alembic migrations for `dec_app`

## 4. Normative database and ingestion

- [ ] 4.1 Add `normatives/` package with ORM models (`Document`, `Revision`, `Clause`, `Formula`, `Coefficient`) and Alembic migrations for `dec_normatives`
- [ ] 4.2 Add `normatives/ingestion/loader.py` and a pilot source file (beam deflection, СП 16.13330)
- [ ] 4.3 Add `normatives/search.py` with full-text search (GIN + pg_trgm)

## 5. Parameters layer

- [ ] 5.1 Add `parameters/loader.py` and `parameters/param_schemas.py`
- [ ] 5.2 Add `params/normatives/beam_deflection.yaml` as the pilot parameter file

## 6. Calculation engine

- [ ] 6.1 Add `engine/base.py` (`Calculator` interface) and `engine/registry.py`
- [ ] 6.2 Add `engine/beam_deflection.py` reference implementation reading parameters from the parameters layer

## 7. ML zone

- [ ] 7.1 Create `ml/` with `models/`, `experiments/`, `serving/` and a gitignored `models/`
- [ ] 7.2 Add `ml/registry.yaml` with an example experimental model entry

## 8. Docker and local environment

- [ ] 8.1 Add `docker-compose.yml` with `postgres` (databases `dec_app` + `dec_normatives`, extensions pg_trgm + pgvector) and `backend`
- [ ] 8.2 Add `.gitignore` entries for ML artifacts and local config
