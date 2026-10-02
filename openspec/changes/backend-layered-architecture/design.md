# Design

## Context

DEC backend is a greenfield FastAPI + PostgreSQL + NumPy/SciPy service. The passport
fixes the tech stack but not the code organization. We need a layered layout that
prevents hardcoding and mixing. Local-first, with a later path to a Russian cloud host.

Scope note (2026-09-28): this change was split. It now covers the layered scaffold,
configuration, the `dec_app` database, the parameters layer for engineer-set values, and
the `Calculator` interface and registry. The normative database (`dec_normatives`) with
ingestion and search, the isolated `ml/` zone, and Docker moved to planned changes
(`tasks.md`, "Moved out of this change"). Decisions 4-6 below keep the record of what was
agreed with Egor for those parts; a decision marked "Moves with" is implemented by the
named later change, not by this one.

## Goals / Non-Goals

**Goals:**
- Fix a conventional layered backend structure with a strict dependency direction.
- Eliminate hardcoding: config via env, engineer-set values via `.yaml` (decision 3);
  formulas and coefficients the norm gives come from `dec_normatives`, not `.yaml`.
- Provide the transactional `dec_app` database session and migration tree.

**Non-Goals:**
- No ML in the calculation path (explicitly rejected by the passport).
- No normative database, ingestion, search, or NLP/RAG parsing here: the normative
  pipeline (`ml/src/normatives_pipeline/`, Egor's zone) owns parsing, and the backend's reading
  side is the planned `normative-catalog-backend`.
- No `ml/` zone and no Docker configuration here (Egor's zones).
- No cloud provisioning yet — local only.

## Decisions

1. **Layers** — `models` (SQLAlchemy), `schemas` (Pydantic DTOs), `repositories`
   (data access), `services` (business logic), `api` (FastAPI routes), `parameters`
   (YAML loading/validation), `engine` (calculation core), `reporting` (python-docx),
   `core` (config/exceptions/logging/security), `db` (session and the migration
   environment), `worker` (background jobs). The declarative `Base` lives in `models`,
   so `db` and the Alembic `env.py` can read its metadata; the Alembic tree is at
   `backend/alembic/`, outside `app`, so its `env.py` is not subject to the layer
   order.
   - Rationale: conventional separation; single responsibility per layer.
   - Alternative: a flat module-per-feature layout — rejected, mixes concerns.

2. **Dependency direction** — one total order of layers, top to bottom; layers on the
   same line are independent siblings:

   ```
   api | worker
   services
   engine | parameters | reporting
   repositories
   db
   models | schemas
   core
   ```

   A module may import only from a layer strictly below its own, or from its own
   package; siblings on one line do not import each other. Standard-library and
   third-party imports are outside the rule (`engine` may import numpy). Two rules cut
   deeper than the order:
   - `api` and `worker` do not import `repositories` or `models` (ORM objects stay
     behind `services`; `api` reaches data only through `services` and `schemas`). By
     convention `api` uses `db` only for the session dependency; the layers contract
     cannot express that, so it is checked in review.
   - `engine` imports from the application only `schemas` and `core`. It never imports
     `repositories`, `db`, `models`, `parameters`, or `reporting`: it receives resolved
     parameters as typed arguments (decision 7), so the pure function stays free of
     I/O.

   The typed values that cross layers (engineer-set values, calculation inputs, the
   result envelope, unit-carrying values) are defined in `schemas`, the one layer both
   `engine`, `parameters` and `reporting` may import. `Calculator` is generic over
   them (decision 7), so `engine` does not import them at all. `param_schemas.py` in
   `parameters` holds only the schema of the YAML file and builds the `schemas` types.

   `parameters` may import `repositories`, because it will read `dec_normatives`
   (decision 3) once `normative-catalog-backend` adds that path. The `normatives/`
   package is not placed in the order here: its location was open item 9.3, decided by
   that change. Settled 2026-10-03 (decision 5): there is no `normatives/` package with
   its own loader; the backend reads Egor's read-only views in `dec_normatives` through
   its own repository, placed by that change. `ml/` sits outside `backend/app` and has no import relationship in either
   direction (decision 6).
   - Rationale: keeps the calculation engine and data access swappable and testable, and
     gives `bootstrap-dev-environment` task 5.1 a complete contract to encode as an
     `import-linter` "layers" contract (siblings as independent layers) plus forbidden
     contracts for the two rules above.
   - Enforced by that `import-linter` contract (`bootstrap-dev-environment` task 5.1,
     updated 2026-09-28 to include the forbidden contracts) once this change is
     applied, and by code review until then, not at runtime. The `api` rule needs
     indirect imports allowed, since `api` reaches `repositories` through `services`.
     Whether the installed `import-linter` accepts the `|` sibling syntax is checked
     when that task runs; if not, the siblings are expressed as an independence
     contract.

3. **Parameters in YAML, for engineer-set values only** — `params/**/*.yaml` holds
   values the norm does not give and the engineer sets instead (rounding rules,
   validated ranges: `calculation-core-contract`'s `EngineerRule`, whose `engineer` and
   `rationale` are required). `calculation-core-contract` also allows a validated
   range's `Source` to be a `NormRef` list, for a norm-given range; that case is not
   engineer-set and has no home in this loader, the same gap as the norm-given method
   bounds below. One file per calculation type
   (`<params root>/<calculation-type>.yaml`, the root passed to the loader as an
   argument), validated by Pydantic schemas in the `parameters` layer, and passed to
   `engine` as typed arguments.
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
     Norm-given method bounds, which `calculation-core-contract` task 5.1 calls
     parameter data, are norm-given too: this loader rejects them, and they have no home
     until `normative-catalog-backend` exists.
     Task 5.1 loads only the engineer-set values. Reading formulas and coefficients from
     `dec_normatives` through the `provenance` gate, not from a static formula YAML file,
     moves with the planned `normative-catalog-backend` (old task 5.1, second half).

4. **Two PostgreSQL databases in one instance** (`dec_app` is built here; the
   `dec_normatives` parts move, see below) — `dec_app` (transactional: users,
   calculations, reports) and `dec_normatives` (documents, revisions, clauses,
   formulas, coefficients). Separate Alembic migration trees, and a role per zone.
   Update 2026-10-03 (decision 5): `dec_normatives` has no Alembic tree of the backend;
   Egor's ingestion creates its schema and the read-only views, versioned with the
   ingestion. The Alembic tree is `dec_app`'s only.
   `dec_app` is implemented here (tasks 3.1-3.2). The `dec_normatives` half moves with
   `normative-catalog-backend` (migrations) and Egor's infra change (compose, roles).
   - Rationale: isolating the document catalog from the app keeps ingestion and search
     concerns clean. `pgvector` extension enabled for future RAG embeddings.
   - Alternative: one database with schemas — rejected, weaker isolation.
   - Confirmed by Egor on 2026-09-27 (question 5 of the review file): his pipeline's
     single database (still named `dec` in `docker-compose.yml` at the time of
     writing) becomes `dec_normatives`; `dec_app` is added when the backend needs it,
     since `backend/` does not exist yet. The rename and the role per zone are old task 9.6
     (Egor, `docker-compose.yml`, moved to his infra change), not yet applied. Closes
     task 9.1. Update 2026-10-03: the compose file is now `infra/docker-compose.yml`
     (service `dec-postgres`, port 5433), still with the single database `dec`; the
     rename and the roles are still not applied. The backend's read-only role is
     `dec_normatives_reader` (`SELECT` only), Egor's
     (`docs/decisions/normative-catalog-backend-questions-akim.md`, "Answers", item 1).
   - Full-text search over `dec_normatives` uses `pg_trgm` similarity + a GIN index
     (old task 4.3, moved), confirmed over `to_tsvector` by Egor on 2026-09-27 (question 9,
     journal entry 14); his pipeline already searches this way. `pgvector` stays
     reserved for later semantic retrieval; neither side uses it today. Closes task
     9.2.

5. **Normative ingestion** (moves with `normative-catalog-backend`) — a manual `normatives/ingestion/loader.py` reads a source
   file (`.docx`/`.pdf`/`.yaml`) and populates `dec_normatives`. One pilot file for the
   MVP.
   - Rationale: matches the passport "manual monitoring for now" decision.
   - Settled 2026-10-03 (old task 9.3, the first decision of `normative-catalog-backend`;
     `docs/decisions/normative-catalog-backend-questions-akim.md`, "Answers", item 1):
     the contract between the zones is the database, not Python code. Egor's pipeline
     (`ml/src/normatives_pipeline/`, raw SQL, no Alembic) ingests into what becomes
     `dec_normatives` and owns read-only SQL views or functions there and the read-only
     role `dec_normatives_reader` (`SELECT` only), created idempotently and versioned
     with the ingestion. The backend has no `normatives/ingestion/loader.py` and no
     Alembic tree for `dec_normatives`: it reads only those views, through its own
     repository (SQLAlchemy Core, parameterized queries), with
     `DEC_NORMATIVES_DATABASE_URL`. The backend never imports `ml/`, and `ml/` never
     imports `backend/`. The manual loader of this decision is dropped; the views and the
     repository are `normative-catalog-backend`'s.

5a. **Catalog models track the pipeline's evolving schema, not a separate design**
   (task 9.4; moves with `normative-catalog-backend`). `Document`, `Revision`, `Clause`,
   `Formula`, `Coefficient` (old task 4.1)
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
     Update 2026-10-03: Egor's branch is merged into `develop` (`0184450`), but the
     fields are `normatives-formula-contract` tasks 1.4-1.7, still open.

6. **Isolated ML zone** (moves with the planned `ml-model-storage`, Egor's zone) — `ml/` at repo root with `models/` (gitignored artifacts),
   `registry.yaml` (metadata), `experiments/`, `serving/`. No imports from `backend/`,
   and none from `backend/` into `ml/` (spec "Strict dependency direction").
   - Rationale: R&D can proceed without risking the deterministic engine. A model that
     later reaches production is served by a separate service over API/queue.
   - Update 2026-10-03: `ml/` exists on `develop` as Egor's project directory
     (`pyproject.toml`, `src/normatives_pipeline/`, `configs/`, `research/`, `tests/`;
     commit `24797f7`). Its inner layout is his to decide (planned `ml-model-storage`);
     the import rule of this decision stands.

7. **Calculation engine isolation** — `engine/` defines a `Calculator` interface, generic over
   its input, parameter and result types, with one method that is a pure function:
   typed inputs plus resolved parameters in, a result out, no I/O — matching `calculation-core-contract`'s "Pure calculation
   function" requirement. The pure function itself, not the `engine/` package as a
   whole, is the C/C++ hot-swap boundary. This change delivers the `Calculator`
   interface and the registry (task 6.1). The pilot implementation and its parameter
   file (old tasks 5.2 and 6.2) are `calculation-core-contract` task 7.1's, which waits
   for `retarget-mvp-domain` (WP1) to name the `foundations-shallow` type.
   - Rationale: matches the passport's "swap hot paths to C/C++ later".
   - Confirmed 2026-09-28 (`calculation-core-contract` task 7.2's sync request): this
     decision previously named a beam-deflection implementation and did not say the
     engine is a pure function, conflicting with `calculation-core-contract`'s "Pure
     calculation function" requirement (flagged in its `design.md`, "Consistency with
     other specs"); fixed here and by moving the pilot out of `tasks.md`.

## Non-functional requirements

- Coverage: >= 95% branch coverage for the changed code, per the DOD; also the spec
  requirement "Backend coverage gate", enforced by `backend/check.sh`.
- Determinism: the calculation engine's pure functions (decision 7) produce
  bit-for-bit identical output for the same typed inputs and resolved parameters, on
  the same platform — matches `calculation-core-contract`'s "Pure calculation
  function" requirement.
- Security: database URLs and any other secret are read from environment variables
  only (decision 1, `core/config.py`), never hardcoded, logged or printed; the spec
  requirement "Secret values stay out of output" is checked by task 2.1's `repr` test.
  `.env.example` (`bootstrap-dev-environment` task 4.3) lists the required keys with
  placeholders only, no real credential.
- Performance: this change has no query workload, so it sets no latency target; a
  target for full-text search over `dec_normatives` belongs to
  `normative-catalog-backend`, once real query volume is known.
- Accessibility: not applicable, this change has no user interface.

## Risks / Trade-offs

- **Strict layering adds boilerplate** for small endpoints. Mitigation: generic base
  repository and thin routes keep it proportional.
- **Two databases increase local setup complexity**. Mitigation: Egor's infra change
  creates both in one `postgres` service; until then `dec_app` is created by hand for
  the verify clauses of tasks 3.1-3.2.
- **Engineer-set `params/` values can drift from what the norm actually allows**
  (decision 3). Mitigation: `params/` holds only values the norm does not fix
  (rounding rules, validated ranges), each recorded as an `EngineerRule`, visible in
  the envelope and the report; it never holds a formula or coefficient the norm gives,
  so there is nothing there to drift from `dec_normatives`.
- **ML zone risk of creeping into the app**. Mitigation: hard rule — no import from
  `ml/` into `backend/`; enforced by the architecture spec and code review.
