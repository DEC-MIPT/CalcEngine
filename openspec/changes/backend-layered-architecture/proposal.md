# Proposal

## Why

Before any backend implementation, DEC needs a single, agreed layered architecture
that prevents hardcoding and layer mixing. The passport defines the tech stack
(FastAPI, PostgreSQL, NumPy/SciPy, python-docx) but not the code organization. Without
an explicit contract, business logic leaks into routes, ORM objects leak into the API,
and normative coefficients get hardcoded in Python.

We also need two dedicated storages that must stay isolated from the calculation path:
(1) a normative document database we fill incrementally as we work with SP/GOST/SNiP
documents, and (2) an ML model storage used only to study how ML could later enter the
project (document parsing/RAG), never inside the calculation path.

## What Changes

- Introduces a new capability `backend-architecture` that fixes the layer layout and
  the two storages.
- Layers: ORM models, schemas, repositories, services, API routes, parameters,
  calculation engine, reporting, core (config/exceptions/logging/security), db, worker.
- Normative parameters are stored in `.yaml` files, never hardcoded in code.
- A dedicated normative database `dec_normatives` (separate from the transactional
  `dec_app`) holds documents, revisions, clauses, formulas, and coefficients, with
  full-text search and a manual ingestion loader for the MVP.
- An isolated `ml/` zone holds model artifacts and a registry for R&D, with no import
  relationship to the application and no role in the calculation path.

## Capabilities

### New Capabilities
- `backend-architecture`: the layered backend layout, parameter-as-YAML rule, the
  normative document database, and the isolated ML model storage.

## Impact

- Affects: `backend/` directory layout, Docker/PostgreSQL setup (two databases),
  `.gitignore` (ML artifacts), and future implementation structure.
- No existing code is modified; this establishes the skeleton contract for all
  backend work.
