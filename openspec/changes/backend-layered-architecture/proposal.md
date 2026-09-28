# Proposal

## Why

Before any backend implementation, DEC needs a single, agreed layered architecture
that prevents hardcoding and layer mixing. The passport defines the tech stack
(FastAPI, PostgreSQL, NumPy/SciPy, python-docx) but not the code organization. Without
an explicit contract, business logic leaks into routes, ORM objects leak into the API,
and normative coefficients get hardcoded in Python.

## What Changes

- Introduces a new capability `backend-architecture` that fixes the layer layout and
  the dependency direction between layers.
- Layers: ORM models, schemas, repositories, services, API routes, parameters,
  calculation engine, reporting, core (config/exceptions/logging/security), db, worker.
- Engineer-set values the norm does not fix (rounding rules, validated ranges) are
  stored in `.yaml` files; formulas and coefficients the norm gives come from the
  normative database. Neither is ever hardcoded in code.
- A minimal runnable backend: `GET /health`, fail-fast configuration from environment
  variables, a `DECError` hierarchy, the `dec_app` transactional database session and
  migration tree, and the `Calculator` interface with its registry.
- Split out on 2026-09-28 into planned changes, not part of this one: the normative
  database `dec_normatives` with ingestion and full-text search, the isolated `ml/`
  zone, Docker, and the pilot calculation. See `tasks.md`, "Moved out of this change".

## Non-goals

- No ML in the calculation path (explicitly rejected by the passport).
- This change builds no normative database, no ingestion, no search, and no NLP/RAG
  parsing: the normative pipeline (`normatives_pipeline/`, Egor's zone) owns parsing,
  and the backend's reading side is a planned change (`normative-catalog-backend`).
- This change builds no `ml/` zone and no Docker configuration (Egor's zones).
- No cloud provisioning — local only.

## Capabilities

### New Capabilities
- `backend-architecture`: the layered backend layout and dependency direction, the
  engineer-set-values-in-YAML rule, the health endpoint, fail-fast configuration, the
  error hierarchy, and the calculator registry.

## Impact

- Affects: `backend/` directory layout and `params/` (engineer-set values).
- No existing code is modified; this establishes the skeleton contract for all
  backend work.
- Sections that moved out touch `docker-compose.yml`, `.gitignore` (ML artifacts), and
  the normative pipeline's zone; they are decided in their own changes.
