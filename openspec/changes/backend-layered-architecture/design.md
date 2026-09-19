# Design

## Context

DEC backend is a greenfield FastAPI + PostgreSQL + NumPy/SciPy service. The passport
fixes the tech stack but not the code organization. We need a layered layout that
prevents hardcoding and mixing, and two isolated storages (normative documents and ML
artifacts) that must never leak into the deterministic calculation path. Local-first,
Docker, with a later path to a Russian cloud host.

## Goals / Non-Goals

**Goals:**
- Fix a conventional layered backend structure with a strict dependency direction.
- Eliminate hardcoding: config via env, normative parameters via `.yaml`.
- Provide a dedicated, searchable normative document database filled incrementally.
- Provide an isolated ML model storage for R&D only.

**Non-Goals:**
- No ML in the calculation path (explicitly rejected by the passport).
- No automated NLP/RAG parsing of norms yet — manual ingestion for the MVP.
- No cloud provisioning yet — local Docker only.

## Decisions

1. **Layers** — `models` (SQLAlchemy), `schemas` (Pydantic DTOs), `repositories`
   (data access), `services` (business logic), `api` (FastAPI routes), `parameters`
   (YAML loading/validation), `engine` (calculation core), `reporting` (python-docx),
   `core` (config/exceptions/logging/security), `db` (session/migrations), `worker`
   (background jobs).
   - Rationale: conventional separation; single responsibility per layer.
   - Alternative: a flat module-per-feature layout — rejected, mixes concerns.

2. **Dependency direction** — `api -> services -> repositories -> models`; `services`
   also uses `engine`, `parameters`, `reporting`. Enforced by import conventions and
   code review, not runtime.
   - Rationale: keeps the calculation engine and data access swappable and testable.

3. **Parameters in YAML** — normative coefficients/formulas/limits live in
   `params/**/*.yaml`, validated by Pydantic schemas in the `parameters` layer, and
   passed to `engine` as typed arguments.
   - Rationale: removes hardcoded normative values; makes the normative base editable
     without code changes.

4. **Two PostgreSQL databases in one instance** — `dec_app` (transactional: users,
   calculations, reports) and `dec_normatives` (documents, revisions, clauses,
   formulas, coefficients). Separate Alembic migration trees.
   - Rationale: isolating the document catalog from the app keeps ingestion and search
     concerns clean. `pgvector` extension enabled for future RAG embeddings.
   - Alternative: one database with schemas — rejected, weaker isolation.

5. **Normative ingestion** — a manual `normatives/ingestion/loader.py` reads a source
   file (`.docx`/`.pdf`/`.yaml`) and populates `dec_normatives`. One pilot file for the
   MVP.
   - Rationale: matches the passport "manual monitoring for now" decision.

6. **Isolated ML zone** — `ml/` at repo root with `models/` (gitignored artifacts),
   `registry.yaml` (metadata), `experiments/`, `serving/`. No imports from `backend/`.
   - Rationale: R&D can proceed without risking the deterministic engine. A model that
     later reaches production is served by a separate service over API/queue.

7. **Calculation engine isolation** — `engine/` defines a `Calculator` interface; the
   beam-deflection implementation is the reference. This is the C/C++ hot-swap boundary.
   - Rationale: matches the passport's "swap hot paths to C/C++ later".

## Risks / Trade-offs

- **Strict layering adds boilerplate** for small endpoints. Mitigation: generic base
  repository and thin routes keep it proportional.
- **Two databases increase local setup complexity**. Mitigation: a single Docker
  `postgres` service creates both databases; documented in compose.
- **YAML parameters can drift from the normative DB**. Mitigation: for MVP `params/`
  is the source of truth for calculations; later `params` are generated/validated from
  `dec_normatives`.
- **ML zone risk of creeping into the app**. Mitigation: hard rule — no import from
  `ml/` into `backend/`; enforced by the architecture spec and code review.
