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
- Eliminate hardcoding: config via env, engineer-set values via `.yaml` (decision 3);
  formulas and coefficients the norm gives come from `dec_normatives`, not `.yaml`.
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

3. **Parameters in YAML, for engineer-set values only** — `params/**/*.yaml` holds
   values the norm does not give and the engineer sets instead (rounding rules,
   validated ranges: `calculation-core-contract`'s `EngineerRule`), validated by
   Pydantic schemas in the `parameters` layer, and passed to `engine` as typed
   arguments.
   - Rationale: removes hardcoded normative values; makes the engineer-set base
     editable without code changes.
   - Formulas and coefficients the norm does give do not go in `params/**/*.yaml`;
     they come from `dec_normatives` through the `parameters` layer's `provenance`
     gate. The path, the registry that feeds it, and its owner are decided in
     `calculation-core-contract`'s `design.md` ("Consistency with other specs" and
     resolution 2), not restated here — that file is the source of truth, this
     decision only says `params/**/*.yaml` is not where formulas or coefficients live.
     Settled 2026-09-27 (question 2 of
     `docs/decisions/normatives-formula-contract-review-egor.md`); closes task 9.5.
     Tasks 5.1-5.2 read from `dec_normatives` through the parameters layer, not from a
     static formula YAML file, once that reading path exists.

4. **Two PostgreSQL databases in one instance** — `dec_app` (transactional: users,
   calculations, reports) and `dec_normatives` (documents, revisions, clauses,
   formulas, coefficients). Separate Alembic migration trees, and a role per zone.
   - Rationale: isolating the document catalog from the app keeps ingestion and search
     concerns clean. `pgvector` extension enabled for future RAG embeddings.
   - Alternative: one database with schemas — rejected, weaker isolation.
   - Confirmed by Egor on 2026-09-27 (question 5 of the review file): his pipeline's
     single database (still named `dec` in `docker-compose.yml` at the time of
     writing) becomes `dec_normatives`; `dec_app` is added when the backend needs it,
     since `backend/` does not exist yet. The rename and the role per zone are task 9.6
     (Egor, `docker-compose.yml`), not yet applied. Closes task 9.1.
   - Full-text search over `dec_normatives` uses `pg_trgm` similarity + a GIN index
     (task 4.3), confirmed over `to_tsvector` by Egor on 2026-09-27 (question 9,
     journal entry 14); his pipeline already searches this way. `pgvector` stays
     reserved for later semantic retrieval; neither side uses it today. Closes task
     9.2.

5. **Normative ingestion** — a manual `normatives/ingestion/loader.py` reads a source
   file (`.docx`/`.pdf`/`.yaml`) and populates `dec_normatives`. One pilot file for the
   MVP.
   - Rationale: matches the passport "manual monitoring for now" decision.
   - Open (task 9.3): Egor's pipeline already ingests into what becomes
     `dec_normatives` with its own code (`normatives_pipeline/`, raw SQL, no Alembic),
     not this manual loader. Whether the backend still needs its own
     `normatives/ingestion/loader.py` and Alembic migrations for a database the
     pipeline already owns and populates, or reads it read-only instead (see decision
     3), is not settled by any of Egor's answers so far and needs a joint decision
     with him.

5a. **Catalog models track the pipeline's evolving schema, not a separate design**
   (task 9.4). `Document`, `Revision`, `Clause`, `Formula`, `Coefficient` (task 4.1)
   correspond to the pipeline's `document`, `clause`, `formula`, `notation_entry` (for
   symbols), `cross_ref`, `coefficient` tables. Two gaps, both open:
   - `Revision` does not exist in the pipeline yet. Egor confirmed on 2026-09-27
     (question 6): the current schema is provisional, and revisions (`Revision` with
     `amendment_no`, stored additively per his `NormRef` answer 7) land in
     `norm-source-traceability` (WP3), not created here.
   - `Formula` and `Coefficient` need fields that match the agreed `NormRef`
     (`document`, `edition`, `clause`, `status`, `provenance`). The pipeline's
     `coefficient` table (added 2026-09-27, `b44d6f3`) has none of them yet; this is
     tracked as questions 11-13 of
     `docs/decisions/normatives-formula-contract-review-egor.md`, not closed here.

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
- **Engineer-set `params/` values can drift from what the norm actually allows**
  (decision 3). Mitigation: `params/` holds only values the norm does not fix
  (rounding rules, validated ranges), each recorded as an `EngineerRule`, visible in
  the envelope and the report; it never holds a formula or coefficient the norm gives,
  so there is nothing there to drift from `dec_normatives`.
- **ML zone risk of creeping into the app**. Mitigation: hard rule — no import from
  `ml/` into `backend/`; enforced by the architecture spec and code review.
