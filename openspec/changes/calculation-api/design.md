# Design

## Context

See `proposal.md` (Why). Current state on `feature/report-generator/backend`, which
carries the engine:

- `app/main.py` builds `FastAPI()` at import time and mounts only `GET /health`.
- `CalculationService` (`app/services/calculation.py`) checks a `CalculationRequest`
  against the type's contract (`CalculationRequest.check_against`) and runs the pure
  function `calculate` (`app/engine/pipeline.py`). It takes the resolved parameters,
  `method_range` and `validated_range` as arguments and stores nothing.
- `CalculatorRegistry` (`app/engine/registry.py`) holds `(contract, calculator)` pairs.
  The pilot `foundations_shallow_r.register(registry, rounding_rule, rounding_source)`
  needs its rounding rule from `params/foundations_shallow_r.yaml`, loaded by
  `load_parameters` (`app/parameters/loader.py`).
- The report is `build_report(contract, inputs, envelope, request)`
  (`app/reporting/model.py`), followed by `render_docx(report) -> bytes`
  (`app/reporting/docx_writer.py`).
- `Settings` (`app/core/config.py`) requires `DEC_APP_DATABASE_URL`. `db/session.py`
  builds the engine for `postgresql+psycopg`. The only Alembic revision, `869e03eddcc5`,
  is empty. `models` has the declarative `Base` and no table.
- The layer order (`backend-architecture` "Strict dependency direction"): `api` cannot
  import `repositories` or `models`. `engine` imports only `schemas` and `core`.
- The norm-given parameters of the pilot (formulas, table values, thresholds, the
  method's range) have no source yet. Their source is the planned
  `normative-catalog-backend`.

## Goals / Non-Goals

**Goals:**
- One composition root that wires settings, the registry, the parameter sources, the
  session and the services, so that tests can replace each of them.
- Every error leaves the API through one handler, in one body shape.
- The stored envelope reads back equal to the returned one, bit for bit.
- The test suite runs without a database server; one integration module checks
  PostgreSQL.

**Non-Goals:**
- Async I/O. The engine and python-docx are synchronous and CPU-bound, so the routes are
  plain `def` and run in FastAPI's thread pool.
- A generic repository or service framework. One table, one repository.

## Decisions

1. **Modules per layer.**
   - `api/calculations.py`: the routes.
   - `api/errors.py`: the error body and the exception handlers.
   - `api/dependencies.py`: the providers that `Depends` uses.
   - `services/calculation.py`: `CalculationService` grows storage, the parameter
     source and the report.
   - `services/catalog.py`: builds the registry and the list of calculation types.
   - `repositories/calculation_result.py`, `models/calculation_result.py`.
   - `schemas/api.py`: the response and error schemas.

   `app/main.py` holds `create_app()` and stays the composition root outside the layers.
   `api` reaches the database only through `services`. It may import `db` for the
   session provider, since `db` is below `services` in the order.
   - Alternative: a provider module in `services` that opens the session itself. It was
     rejected because the request-scoped session belongs to the HTTP request's
     lifetime, which `api` owns.

2. **The registry is built once, at start-up.** `services/catalog.py` has
   `build_registry(params_root)`. For each known calculation type it loads the type's
   `.yaml` through `load_parameters` and calls the type's `register`. The pilot is the
   only type today. A missing or invalid `.yaml` stops the application at start-up
   (fail-fast, like `Settings`), not at the first request. FastAPI's lifespan builds the
   registry, and tests pass their own.

3. **Parameter source as a port.** `services` defines a protocol `ParameterSource` with
   one method:

   ```
   resolve(calculation_type, inputs) -> ResolvedParameters(parameters, method_range)
   ```

   It receives `inputs` because a table value can depend on an input: an input selects
   the row of a norm's table. The service reads `validated_range` from the type's `.yaml`.
   - The application holds a mapping from calculation type to source.
   - This change configures no source. A registered type with no source raises
     `ParameterSourceUnavailableError` (a `DECError`), which gives `503`.
   - Order of checks in `POST /calculations`:
     1. schema (FastAPI);
     2. registered type (`404`);
     3. `check_against` (`422`);
     4. source configured (`503`);
     5. run;
     6. store.

     So nothing is stored on any rejection.
   - `normative-catalog-backend` adds the catalog implementation. Tests add a synthetic
     one through `app.dependency_overrides`.
   - Alternatives rejected:
     - Parameters in the request body: this would make the client a source of norm
       values, which "Calculation parameter source" forbids.
     - A development source with synthetic values in `app/`: this would be a formula
       literal in code, which "No hardcoding" forbids.

4. **Storage.** One table, `calculation_result`, in `dec_app`:
   - `result_id`: UUID, primary key;
   - `calculation_type`;
   - `engine_version`;
   - `input_hash`: 64 characters, indexed;
   - `inputs`: JSON, the request's inputs with units;
   - `envelope`: JSON;
   - `norm_sources`: JSON, the distinct `(document, edition)` of the envelope's
     `norm_refs`, in first-use order;
   - `created_at`: timezone-aware, set by the database.

   The column type is the generic SQLAlchemy `JSON`, which is PostgreSQL `json`, not
   `jsonb`. `json` keeps the text as written. `jsonb` turns numbers into `numeric`,
   which drops the sign of `-0.0` and rewrites exponents, so a read-back envelope could
   differ from the returned one.

   The repository has `add` and `get` only. A stored result is never updated, which is
   the requirement "Reproducible stored result". The service turns rows into
   `ResultEnvelope` and plain dicts, so no ORM object leaves `services`
   (`backend-architecture` "No layer mixing").

   One Alembic revision on top of `869e03eddcc5` creates the table, and its downgrade
   drops it.

5. **Errors.** `api/errors.py` registers handlers for `RequestValidationError`,
   `DECError` subclasses, `HTTPException` and `Exception`. Body:

   ```
   {"code": str, "message": str, "fields": [{"location": [...], "message": str}]}
   ```

   `fields` is present for `422` only, and always present there.

   | Error | Status | `code` |
   |---|---|---|
   | `NotFoundError`; `HTTPException` 404 (no route) | 404 | `not_found` |
   | `HTTPException` 405 | 405 | `method_not_allowed` |
   | `CalculationTypeNotRegisteredError` (report of a stored result) | 409 | `calculation_type_not_registered` |
   | body over the limit | 413 | `payload_too_large` |
   | `RequestValidationError` | 422 | `validation_error` |
   | `InputValidationError`, `UnitError` | 422 | `invalid_input` |

   A unit outside the vocabulary never reaches `UnitError` through the API: the request
   schema types each unit as a symbol of the vocabulary, so it is a
   `RequestValidationError` (`validation_error`). `UnitError` stays mapped for a unit
   error raised behind the schema.
   | `ParameterSourceUnavailableError` | 503 | `parameter_source_unavailable` |
   | `DatabaseUnavailableError` | 503 | `database_unavailable` |
   | `ParameterValidationError`, `ExpressionError`, `CalculationError`, `AlreadyRegisteredError`, any other | 500 | `internal_error` |

   - `fields` is present in every `422` body. For `invalid_input`, the location of each
     offending input is `["body", "inputs", "<input name>"]`, the same prefix pydantic
     uses for the body. `CalculationRequest.check_against` changes to collect every
     missing, undeclared, or wrong-dimension input and raise one `InputValidationError`
     carrying their names, instead of stopping at the first. The message text keeps
     naming the inputs, so the WP2 tests stay valid.
   - New `DECError` subclasses in `core/exceptions.py`:
     `ParameterSourceUnavailableError`, `CalculationTypeNotRegisteredError` and
     `DatabaseUnavailableError`.

   A broken `.yaml` or a bad expression tree is a fault of the server's data, not of the
   request, so it is `500`, not `422`.
   - The `500` message is fixed text. The log line holds the `code`, the route and the
     exception type, and never the request body or the exception's arguments (they may
     carry input values).
   - `RequestValidationError` messages are rebuilt from the field locations and pydantic
     message texts, without the `input` echo that pydantic adds by default.

6. **Request size.** A small ASGI middleware rejects a declared `Content-Length` over
   1 MiB at once. It also counts the bytes of a body without one and stops at the
   limit. Both give `413` with the error body before anything is parsed.

7. **Settings.**
   - A second settings class, `ApiSettings`, with no required field, holds what the
     application needs to start:
     - `DEC_CORS_ORIGINS`: comma-separated origins, empty by default;
     - `DEC_PARAMS_ROOT`: a path whose default is `backend/params` resolved from the
       package, so it is not a literal machine path.

     `create_app` and the lifespan (`build_registry`) read only `ApiSettings`.
   - `Settings` keeps only the database URLs and its fail-fast rule
     (`backend-architecture` "Fail-fast configuration"). It is read lazily, at the first
     request that needs `dec_app`. So the server starts, and `GET /health`,
     `GET /calculation-types` and `/docs` answer, without `DEC_APP_DATABASE_URL`.
   - The session provider turns a missing or invalid `DEC_APP_DATABASE_URL` (the
     pydantic-settings validation error, not a `DECError`) and a connection failure
     (SQLAlchemy `OperationalError`) into `DatabaseUnavailableError`, which gives `503`.
     The original error is logged by type only, never with its text, since that text
     can hold the URL.

   The engine and the session factory are created lazily and cached by the provider.

8. **CORS.** Starlette's `CORSMiddleware` is set with `allow_origins` from
   `ApiSettings`: no wildcard, and no credentials until `user-accounts-auth` decides how
   the token travels.

9. **Report endpoint.**
   - The route is `POST`, because the report request has a body.
   - The service loads the stored record and takes the contract from the registry. A
     stored result whose type is no longer registered raises
     `CalculationTypeNotRegisteredError` (`409`): the result exists, so `404` would
     mislead. It then calls `build_report` with the stored inputs and envelope and
     `render_docx`, and returns the bytes.
   - The file name is `dec-report-<result_id>.docx`, ASCII only, so no header encoding
     is needed.

10. **Calculation types view.** The service maps each contract to a schema
    `CalculationTypeView`:
    - `name`;
    - `inputs`: name, base unit, dimension from the unit vocabulary;
    - `outputs`: name, base unit.

    Rounding rules, checks and sources stay out of the listing. They belong to a result,
    not to the input form.

11. **Testing.**
    - API tests use `TestClient(create_app(...))` with a SQLite in-memory engine
      (`StaticPool`) from the same models, a test registry, and a synthetic parameter
      source. SQLite's `JSON` stores text the same way, so equality tests hold.
    - `tests/test_calculation_result_postgres.py` is marked `postgres`. It is skipped
      unless `DEC_TEST_APP_DATABASE_URL` is set. It runs `alembic upgrade head` on that
      database, stores and reads an envelope, and runs `alembic downgrade` back to
      `869e03eddcc5`. It runs against a hand-made database on `dec-postgres`, as the WP5
      task 3.x verify clauses do.
    - `check.sh` stays database-free and keeps the 95% branch gate.

12. **C/C++ boundary.** Unchanged: the pure function `calculate` of the engine
    (`calculation-core-contract` design.md decision 7). The API, storage and report
    delivery sit outside it and never enter a hot path.

## Non-functional requirements

- **Latency.** `POST /calculations` for the pilot type, with a synthetic in-process
  source and a local `dec_app`, has a median of at most 1 second over 20 sequential
  requests after one warm-up (spec "Non-functional — request size and latency"). The
  target is indicative for a developer laptop, and it is checked in the `postgres`
  module, which is part of the implementation GO, not of `check.sh`. The report endpoint stays within
  `report-generator` "Non-functional — generation time" (under 1 minute; WP2 measured
  200 steps).
- **Security.** Database URLs only from the environment, never logged or returned.
  Every query goes through the ORM with bound parameters. Error bodies hold no stack
  trace, SQL, path or configuration value. Request bodies are limited to 1 MiB. CORS is
  closed by default. The endpoints are open until `user-accounts-auth`, so the server
  is run bound to `127.0.0.1` only (Risks).
- **Coverage.** At least 95% branch coverage of `backend/app` in `check.sh`.
- **Accessibility.** Not applicable: no UI in this change.

## Risks / Trade-offs

- **[Open endpoints until `user-accounts-auth`]** → The change is not deployed. The run
  command in `tasks.md` binds `127.0.0.1`, and `user-accounts-auth` is the next change
  on the same branch line.
- **[No real calculation until the catalog source exists]** → Every real request for the
  pilot answers `503` until `normative-catalog-backend`. The API contract, the storage
  and the report are still tested end to end with a synthetic source in tests. The
  frontend tests mock the API.
- **[SQLite in unit tests differs from PostgreSQL]** → Only generic column types are
  used. The `postgres` integration module runs the real migration and a round trip, and
  its run is part of the implementation GO.
- **[A stored result's type later unregistered]** → The report endpoint answers `409`
  `calculation_type_not_registered` for it; the result itself stays readable. Stored rows
  are never deleted by this change.
- **[`json` instead of `jsonb` costs indexing and querying inside the envelope]** → No
  requirement queries inside the envelope. `input_hash` and `calculation_type` are real
  columns.

## Migration Plan

- `alembic upgrade head` on `dec_app` adds `calculation_result`.
- Rollback: `alembic downgrade 869e03eddcc5` drops it. No data exists before this
  change.

## Open Questions

None that change the specs or the tasks. Decided here: a missing or unreachable
application database gives `503 database_unavailable` (decision 7), and a report of a
result whose type is unregistered gives `409` (decision 9). The token transport for CORS
credentials is decided in `user-accounts-auth`.
