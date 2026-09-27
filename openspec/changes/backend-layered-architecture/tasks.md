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

- [ ] 4.1 Add `normatives/` package with ORM models (`Document`, `Clause`, `Formula`, `Coefficient`, each carrying the `NormRef` fields `document`/`edition`/`clause`/`status`/`provenance`) and Alembic migrations for `dec_normatives`; `Revision` is deferred to `norm-source-traceability` (WP3, design.md decision 5a)
- [ ] 4.2 Add `normatives/ingestion/loader.py` and a pilot source file (beam deflection, СП 16.13330)
- [ ] 4.3 Add `normatives/search.py` with full-text search (GIN + pg_trgm)

## 5. Parameters layer

- [ ] 5.1 Add `parameters/loader.py` and `parameters/param_schemas.py`; `loader.py` reads formulas and coefficients from `dec_normatives` and applies the `provenance` gate (design.md decision 3), it does not read them from YAML
- [ ] 5.2 Add `params/normatives/beam_deflection.yaml` as the pilot parameter file, for engineer-set values only (rounding rules, validated ranges); no formula or coefficient value goes in it (design.md decision 3)

## 6. Calculation engine

- [ ] 6.1 Add `engine/base.py` (`Calculator` interface) and `engine/registry.py`
- [ ] 6.2 Add `engine/beam_deflection.py` reference implementation reading parameters from the parameters layer

## 7. ML zone

- [ ] 7.1 Create `ml/` with `models/`, `experiments/`, `serving/` and a gitignored `models/`
- [ ] 7.2 Add `ml/registry.yaml` with an example experimental model entry

## 8. Docker and local environment

- [ ] 8.1 Add `docker-compose.yml` with `postgres` (databases `dec_app` + `dec_normatives`, extensions pg_trgm + pgvector) and `backend`
- [ ] 8.2 Add `.gitignore` entries for ML artifacts and local config

## 9. Reconcile with the normative pipeline (found 2026-09-27)

Found by reading Egor's branch `feature/normative-parser/ml` (commit `6daf2ef`); details in
`docs/reports/egor-branches-analysis.md`, questions to Egor in
`docs/decisions/normatives-formula-contract-review-egor.md`. The tasks of sections 3-8 that
an item names are not implemented until Akim and Egor settle that item; the outcome may
reword those tasks. Owners: Akim and Egor together, except 9.6 (Egor). A task closes when
its outcome is recorded as a decision in this change's `design.md` and the tasks it names
are reworded to match.

- [x] 9.1 One database or two: the pipeline uses one database `dec`; decision 4 plans `dec_app` and `dec_normatives` (tasks 2.1, 3.1-3.2, 4.1, 8.1; question 5) (2026-09-27: two, confirmed by Egor; `dec` becomes `dec_normatives`, `dec_app` added when the backend needs it; rename is task 9.6, not yet applied; design.md decision 4)
- [x] 9.2 Lexical search: GIN + `pg_trgm` (task 4.3) or `to_tsvector('simple')` over lemmatized text, as the pipeline does now (question 9); `pgvector` stays for later retrieval (2026-09-27: `pg_trgm` + GIN, confirmed by Egor and already in his code; design.md decision 4)
- [ ] 9.3 Where normative ingestion and the catalog code live, and in whose zone: `normatives/` inside the backend with a manual loader (decision 5, tasks 4.1-4.3) or Egor's top-level `normatives_pipeline/` (open: not answered by questions 1-10; design.md decision 5)
- [x] 9.4 Catalog models: `Document`, `Revision`, `Clause`, `Formula`, `Coefficient` (task 4.1) against the pipeline schema (`document`, `clause`, `formula`, `notation_entry`, `cross_ref`; no revisions, no coefficient tables; questions 6-7) (2026-09-27: `Revision` deferred to WP3, confirmed by Egor; `Formula`/`Coefficient` still need `NormRef` fields the pipeline does not yet store (questions 11-13, not closed); design.md decision 5a)
- [x] 9.5 Where the formulas and coefficients used by the engine live: `params/**/*.yaml` in the parameters layer (decision 3, tasks 5.1-5.2) or the pipeline registry `formulas.toml` (question 2); settle together with `calculation-core-contract` task 7.2 (2026-09-27: `dec_normatives`, read by the parameters layer through the `provenance` gate; `params/**/*.yaml` holds only engineer-set values; `formulas.toml` stays Egor's MVP registry; design.md decision 3; mirrored in `calculation-core-contract` `design.md`, "Consistency with other specs")
- [ ] 9.6 `docker-compose.yml`: the pipeline branch already adds one with PostgreSQL only; task 8.1 extends it, and its owner is Egor (DevOps)
- [ ] 9.7 ML layout: `ml/` (decision 6, tasks 7.1-7.2) against the pipeline's `normatives_pipeline/ocr/` and its model artifacts (open: not answered by questions 1-10)
