# Tasks

Lead: Akim (moved from Egor 2026-09-28, since `backend/` is Akim's responsibility zone
per `AGENTS.md` section 5; see `docs/decisions/backend-layered-architecture-lead-change.md`).

Scope (split 2026-09-28, see `docs/decisions/backend-layered-architecture-split-egor.md`):
this change is only what Akim decides and implements inside `backend/` with no wait on
Egor or WP1 — the layered scaffold, config, the `dec_app` database session and
migrations, the parameters layer for engineer-set values, and the `Calculator`
interface and registry. The normative catalog and ingestion (old section 4 and the
`dec_normatives` half of old task 5.1), the ML zone (old section 7), Docker (old
section 8), the open items 9.3, 9.6, 9.7, and the pilot tasks 5.2 and 6.2 moved out; see
"Moved out of this change" at the end. Section numbers 4, 7, 8 are not reused, so that
references to sections 1-3, 5, 6 and 9 stay valid.

Branch: `feature/backend-core/backend` (Akim, from `develop`), merged only when the whole feature is done. Checkboxes in this file are ticked in `develop` as each subtask is done on the feature branch; the code reaches `develop` only when the whole feature is done (`AGENTS.md`, Branching rules).

## 1. Scaffold layered directory structure

- [x] 1.1 Create `backend/app` with empty `api`, `schemas`, `models`, `repositories`, `services`, `parameters`, `engine`, `reporting`, `core`, `db`, `worker` packages (backend), branch `feature/backend-core/backend`; verify: each package has an `__init__.py`, and `python -c "import app"` (from `backend/`) raises no import error (2026-09-28: twelve empty `__init__.py` files created; `python -c "import app"` and individual imports of all eleven layers succeed; `pythonpath = ["."]` added to `backend/pyproject.toml`'s `[tool.pytest.ini_options]` so `pytest` resolves `app` the same way; `backend/tests/test_scaffold.py` added (existence + import per layer); `backend/check.sh` passes, 100% branch coverage. Code is on `feature/backend-core/backend`, not `develop`, per the branching model; see `docs/akim/reports/WP5-code-journal.md`)
- [ ] 1.2 Create `backend/app/main.py` with a minimal FastAPI instance and a health endpoint (backend), branch `feature/backend-core/backend`; the endpoint is `GET /health`, returning `200` with body `{"status": "ok"}` and touching no database (spec "Health endpoint"); verify: a request to it returns exactly that with no database running

- [ ] 1.3 Add the runtime dependencies to `backend/requirements.txt` (currently empty, owned by `bootstrap-dev-environment` task 2.2, also Akim's): `fastapi`, `pydantic-settings`, `sqlalchemy`, `alembic`, `pyyaml`, a PostgreSQL driver (`psycopg`), and `httpx` (test client) to `backend/requirements-dev.txt`, pinned the same way as the existing dev dependencies (backend), branch `feature/backend-core/backend`; verify: `pip install -r backend/requirements.txt -r backend/requirements-dev.txt` succeeds in a clean virtual environment and `python -c "import fastapi, pydantic_settings, sqlalchemy, alembic, yaml"` raises no error

## 2. Core and configuration

- [ ] 2.1 Add `core/config.py` with pydantic-settings reading `DEC_APP_DATABASE_URL` (required) and `DEC_NORMATIVES_DATABASE_URL` (optional until `normative-catalog-backend` reads it) from the environment; the URLs are held so that `repr`/`str` of the settings do not show the credential (`SecretStr` or equivalent) (backend), branch `feature/backend-core/backend`; names match `bootstrap-dev-environment` task 4.3's `.env.example` interim choice, now confirmed by this task, not renamed by it; Egor's pipeline reads `DEC_DATABASE_URL` for the database that becomes `dec_normatives`, and reconciling the two names belongs to `normative-catalog-backend` and the infra change; verify: a `Settings` instance reads what is set from the environment; instantiating it with `DEC_APP_DATABASE_URL` unset raises a validation error naming that variable; `repr(Settings(...))` and `str(...)` of an instance with a URL carrying a password do not contain that password (spec "Fail-fast configuration", "Secret values stay out of output"; no silent default for the required URL)
- [ ] 2.2 Add `core/exceptions.py`, `core/logging.py` stubs (backend), branch `feature/backend-core/backend`; `exceptions.py` defines a base `DECError` and at least one subclass (spec "Common error hierarchy"); `logging.py` configures one stdlib logger; verify: both import without error, the subclass is an instance of `DECError`, and a call to the configured logger emits a line

## 3. Database setup (transactional app DB)

`dec_app` does not exist in `docker-compose.yml` yet (Egor's zone, task 8.1 moved to his change). Until it does, the verify clauses below run against a throwaway database created by hand on the existing `dec-postgres` service (port 5433, the same credentials as the service in `docker-compose.yml`): create it with `CREATE DATABASE dec_app;`, point `DEC_APP_DATABASE_URL` at it, and drop it with `DROP DATABASE dec_app;` after the run, so every run starts from a fresh database. This edits nothing in `docker-compose.yml`.

- [ ] 3.1 Add `db/session.py` (SQLAlchemy engine + session factory for `dec_app`) (backend), branch `feature/backend-core/backend`; verify: the engine/session factory connects to a running `dec_app` database using `DEC_APP_DATABASE_URL`
- [ ] 3.2 Add an initial Alembic migration tree for `dec_app`, ready to autogenerate revisions once `models/` has ORM classes: the tree lives at `backend/alembic/` (outside `app`, so its `env.py` is not subject to the layer order), `env.py` reads `DEC_APP_DATABASE_URL` through `core.config` and takes the declarative `Base` metadata from `models` (`Base` is defined in `models`); one empty initial revision, no table content is invented here because `models/` is still empty (task 1.1) (backend), branch `feature/backend-core/backend`; verify: `alembic upgrade head` on a fresh `dec_app` database exits 0 and leaves an `alembic_version` table holding the initial revision id, which shows `env.py` used the database named by `DEC_APP_DATABASE_URL`

## 5. Parameters layer

- [ ] 5.1 Add `parameters/loader.py`, `parameters/param_schemas.py`, and the typed engineer-set value types in `schemas/parameters.py`; `loader.py` takes a calculation-type name and a `params/` root directory (an argument, not a settings field), reads `<root>/<calculation-type>.yaml`, and validates it against the Pydantic schema in `param_schemas.py`, returning the typed values from `schemas` (rounding rules, validated ranges; each carries `calculation-core-contract`'s `EngineerRule` fields `engineer` and `rationale`, both required); the value types live in `schemas` so `engine` and `reporting` can import them under design.md decision 2; it has no path to formulas or coefficients the norm gives (design.md decision 3; their source is the normative catalog, moved out) (backend), branch `feature/backend-core/backend`; verify: given a calculation-type name and a `.yaml` test fixture directory, it returns the typed values; a fixture with an unknown key (for example a formula or coefficient) is rejected by the schema (extra keys forbidden), and a value without `engineer` or `rationale` is rejected, each with a `DECError` subclass; a missing file for the calculation type also raises a `DECError` subclass

## 6. Calculation engine

- [ ] 6.1 Add `engine/base.py` (`Calculator` interface) and `engine/registry.py` (backend), branch `feature/backend-core/backend`; the interface declares one method taking typed inputs and resolved parameters and returning a result, matching `calculation-core-contract`'s pure-function contract, and is generic over the input, parameter and result types, so `engine` imports none of them (the concrete types are defined in `schemas`: engineer-set values by task 5.1, inputs and the result envelope by `calculation-core-contract` tasks 2.1 and 4.1); this task owns the registry, and `calculation-core-contract` tasks 2.1 and 4.3 extend it; verify: a dummy `Calculator` subclass can be registered in `registry.py` and looked up by calculation-type name, and looking up an unregistered name raises a `DECError` subclass (spec "Calculator registry")

## 9. Reconciliation with the normative pipeline (closed items)

Found 2026-09-27 by reading Egor's branch `feature/normative-parser/ml` (commit `6daf2ef`); details in `docs/akim/reports/egor-branches-analysis.md` (untracked, Akim's own zone), questions to Egor in `docs/decisions/normatives-formula-contract-review-egor.md`. The open items 9.3, 9.6, 9.7 moved out (below); the closed ones stay here as the record of what Egor confirmed.

- [x] 9.1 One database or two: the pipeline uses one database `dec`; decision 4 plans `dec_app` and `dec_normatives` (question 5) (2026-09-27: two, confirmed by Egor; `dec` becomes `dec_normatives`, `dec_app` added when the backend needs it; the rename is old task 9.6, moved out; design.md decision 4)
- [x] 9.2 Lexical search: GIN + `pg_trgm` or `to_tsvector('simple')` over lemmatized text, as the pipeline does now (question 9); `pgvector` stays for later retrieval (2026-09-27: `pg_trgm` + GIN, confirmed by Egor and already in his code; design.md decision 4; implemented by the normative-catalog change, moved out)
- [x] 9.4 Catalog models: `Document`, `Revision`, `Clause`, `Formula`, `Coefficient` against the pipeline schema (questions 6-7) (2026-09-27: `Revision` deferred to WP3, confirmed by Egor; 2026-09-28: Egor agreed to questions 11-13 (`NormRef` fields for `Formula`/`Coefficient`, stored `status`/`provenance`, fixed fields in code), applied on `feature/normative-parser/ml`, not merged into `develop` yet; design.md decision 5a; implemented by the normative-catalog change, moved out)
- [x] 9.5 Where the formulas and coefficients used by the engine live: `params/**/*.yaml` or the pipeline registry `formulas.toml` (question 2) (2026-09-27: `dec_normatives`, read by the parameters layer through the `provenance` gate; `params/**/*.yaml` holds only engineer-set values; `formulas.toml` stays Egor's MVP registry; design.md decision 3; mirrored in `calculation-core-contract` `design.md`, "Consistency with other specs")

## Moved out of this change (2026-09-28)

Each moves to a change that does not exist yet ("planned, not created", like `norm-source-traceability`). Names are proposals. Nothing below is implemented by this change, and none of it gates this change's GO.

| Old task | Content | Goes to | Owner |
|---|---|---|---|
| 4.1, 4.2, 4.3 | `normatives/` package: ORM models with `NormRef` fields, Alembic tree for `dec_normatives`, manual loader with pilot source, full-text search (GIN + `pg_trgm`) | planned `normative-catalog-backend` | Akim and Egor |
| 5.1 (second half) | `parameters` layer reads formulas and coefficients from `dec_normatives` through the `provenance` gate | same | Akim and Egor |
| 9.3 | Where normative ingestion and catalog code live: `backend/normatives/` with a manual loader, or Egor's `normatives_pipeline/` (open; design.md decision 5; Egor's position, 2026-09-28: it stays in his pipeline package, which already ingests into `dec_normatives`, owns `formulas.toml`, and does search — a second loader in `backend/normatives/` would duplicate it; not a decision, still the first item of that change) | same, first decision of that change | Akim and Egor |
| 5.2, 6.2 | Pilot parameter file and pilot reference implementation | `calculation-core-contract` task 7.1 (it already names the pilot for the contract tests, and waits for the same `foundations-shallow` list from WP1) | Akim |
| 7.1, 7.2, 9.7 | `ml/` layout, registry, `.gitignore` for artifacts, and its layout against the OCR code (2026-09-28: no `normatives_pipeline/ocr/` package any more; OCR enrichment is `normatives_pipeline/formulas/formula_ocr.py`, check the planned layout against that) | planned `ml-model-storage` | Egor |
| 8.1, 8.2, 9.6 | `docker-compose.yml` with `dec_app` + `dec_normatives`, extensions, the `backend` service, `.gitignore` entries; the `dec` -> `dec_normatives` rename and a role per zone | Egor's infra change (his to name) | Egor |

## Requirement coverage

Which task or check verifies each requirement of the spec delta. Requirements marked "after apply" have no task in this change and are verified by another change once this one is applied; they are not verified by this change's own GO.

| Requirement | Verified by |
|---|---|
| Layered architecture | task 1.1 (the eleven packages exist) |
| Strict dependency direction | after apply: `bootstrap-dev-environment` task 5.1 (`import-linter`: a "layers" contract with siblings as independent layers, forbidden contracts for `api`/`worker` and for `engine`, with indirect imports allowed for the `api` rule since it reaches `repositories` only through `services`, and the `ml/` rule once `ml/` exists); the text of that task is updated to say so (2026-09-28) |
| No layer mixing | after apply: no code in this change can violate it (no endpoint returns data); the first endpoint that returns data carries the ORM-isolation test |
| No hardcoding | tasks 2.1 (database URL) and 5.1 (a formula or coefficient key is rejected) |
| Engineer-set parameters stored in YAML | task 5.1 |
| Health endpoint | task 1.2 |
| Fail-fast configuration | task 2.1 |
| Secret values stay out of output | task 2.1 |
| Common error hierarchy | task 2.2 |
| Calculator registry | task 6.1 |
| Transactional application database | tasks 3.1, 3.2 |
| Backend coverage gate | `backend/check.sh` (`bootstrap-dev-environment` design.md decision 3), turned on once `backend/app` exists (task 1.1) |

## Follow-ups outside this change

Stale text in files this change does not own; listed for their owners, not edited here.

- `openspec/specs/normatives-catalog/spec.md` (Purpose) says `dec_normatives` is implemented per the `backend-architecture` capability; after the split that capability does not specify it. Point it at `normative-catalog-backend` when that change exists.
- `retarget-mvp-domain` tasks 4.1 and 4.2 (owner Egor) cite lines of this change's old `tasks.md` and `design.md` for the placeholder pilot; those lines are gone. Close or update them.
- `bootstrap-dev-environment` `design.md` decision 5 says task 2.1 "fixes no literal name"; task 2.1 here now confirms the names.
- `CLAUDE.md` status text still describes this change as "not yet retargeted" with sections 4, 7, 8 and items 9.3, 9.6, 9.7 to decide.
- `calculation-core-contract` task 5.1 calls method bounds "parameter data", but the engineer-set loader here forbids norm-given values; those bounds have no home until `normative-catalog-backend` exists. Decide in that change or in `calculation-core-contract` before its task 5.1.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist, including a "Non-goals" section on `proposal.md`
- [x] `openspec validate --strict` passes and a `spec-reviewer` report on the current version lists no blocker and no major finding (2026-09-28: fourth pass, 0 blockers, 0 major, 3 minor, verdict READY for DOR; recorded in `docs/decisions/backend-layered-architecture-readiness.md`)
- [x] Functional requirements and scenarios recorded, consistent with `design.md`; each requirement is mapped to a task or a named later check ("Requirement coverage" above)
- [x] Non-functional requirements recorded explicitly (`design.md`, "Non-functional requirements"; the secrets and coverage requirements are also in the spec)
- [x] Each task is small enough for one session (Akim's own judgement, 2026-09-28; not a reviewer confirmation)
- [x] Acceptance and Go/No-Go criteria written (this section; every task has a "verify" clause)
- [x] Branch naming defined (header: `feature/backend-core/backend`, restated per task)
- [x] Dependencies, if any, are listed and satisfied (Dependencies below: none open)

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4). This change has code, so it uses the normal test and coverage path, not the code-free path.
- Spec phase: `openspec validate --all --strict` passes; a `spec-reviewer` report on the current version lists no blocker and no major finding (status: see the DOR checklist).
- Implementation: every task in this file is checked off; each task's own verify clause passes; `ruff` and `mypy` pass on `backend/app`; >= 95% branch coverage on changed code; no known security issue introduced (database URLs only from the environment, never logged, printed or hardcoded; no secret in `.env.example`); the delta spec matches the implementation for every requirement not marked "after apply" in "Requirement coverage"; reviewed before merge.
- NO-GO: any of: `openspec validate` fails; an unresolved blocker or major finding from the current `spec-reviewer` report; a task's own verify clause fails; coverage < 95%; a security finding; a root `pyproject.toml`, `tests/`, or any file in Egor's zones (normative pipeline, ML, DevOps, `docker-compose.yml`) touched without his agreement.
- Archive happens only after GO for both the spec phase and implementation.

## Dependencies

- None open. Sections 1-3, 5, 6 need no decision from Egor and no list from WP1.
- Order with `calculation-core-contract`: this change is applied first. Its task 7.1 (the pilot, moved there from this change's old 5.2 and 6.2) needs this change's `parameters/param_schemas.py`, `schemas/parameters.py` and the calculator registry (task 6.1); its tasks 2.1 and 4.3 extend that registry. This change needs nothing from `calculation-core-contract`, because `Calculator` is generic over the types it will receive. Its task 7.2 (sync) is therefore mostly done here.
- `bootstrap-dev-environment` tasks 4.4 and 5.1 (`[blocked: WP5]`) unblock once this change is applied; task 5.1 verifies the layering requirements marked "after apply".
- Task 1.3 edits `backend/requirements.txt` and `backend/requirements-dev.txt`, created by `bootstrap-dev-environment` task 2.2 (also Akim's).
- Task 3.x uses the existing `dec-postgres` service of `docker-compose.yml` read-only (a hand-made `dec_app` database, created and dropped per run), and edits nothing in it.
- Egor acknowledged the split on 2026-09-28 (`docs/decisions/backend-layered-architecture-split-egor-ack.md`): the sections in his zones (ML, Docker/DevOps) and open items 9.3, 9.6, 9.7 are confirmed to live outside WP5, and he owns the ML and infra changes. Nothing he confirmed on 2026-09-27 (`design.md` decisions 4-6) is reopened.
