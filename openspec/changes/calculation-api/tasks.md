# Tasks

Owner: Akim (backend zone). WP8.

Branch: one feature, `feature/calculation-api/backend` (Akim). It branches from
`feature/report-generator/backend`, which carries the engine and the report, and is
merged into `develop` only after both WP2 features and only when every code task below
is done (`AGENTS.md`, Branching rules). Spec work (section 1) is committed directly to
`develop`. Checkboxes are ticked in `develop` as each subtask is done on the feature
branch. Every task with code below is on this branch.

Code journal: `docs/akim/reports/WP8-code-journal.md`, created before task 2.1.

## 1. Spec readiness

- [x] 1.1 (spec) Run `openspec validate calculation-api --strict` and
  `openspec validate --all --strict`; verify: both pass (2026-10-02, 19/19)
- [x] 1.2 (spec) Run `spec-reviewer` on this change and resolve its findings until a
  report on the current version lists no blocker and no major finding; record the passes
  in `docs/decisions/calculation-api-readiness.md` (2026-10-02: two passes, last one
  0 blockers, 0 major, READY)
- [x] 1.3 (spec) Run `norm-traceability-checker`; verify: it confirms that no
  requirement of this change fixes a formula, coefficient, limit or rounding rule
  (2026-10-02: two passes, last one PASS)

## 2. Groundwork (backend)

- [ ] 2.1 Create the branch from `feature/report-generator/backend`. Add `uvicorn` to
  `backend/requirements.txt`. Add `ApiSettings` with `DEC_CORS_ORIGINS`
  (comma-separated, empty by default) and `DEC_PARAMS_ROOT` (default `backend/params`
  resolved from the package), with no required field (`design.md` decision 7)
  (backend); verify: tests show an empty origin list without the variable, two origins
  from `"a,b"`, the default params root pointing at the directory that holds
  `foundations_shallow_r.yaml`, an override from the environment, and `ApiSettings()`
  constructed with `DEC_APP_DATABASE_URL` unset
- [ ] 2.2 Add `schemas/api.py` (`ErrorBody`, `FieldError`, `CalculationTypeView` with
  its input and output views) and the exceptions `ParameterSourceUnavailableError`,
  `CalculationTypeNotRegisteredError` and `DatabaseUnavailableError` in
  `core/exceptions.py` (backend); verify: schema tests for every field; each new
  exception is a `DECError`
- [ ] 2.3 Add `create_app(api_settings=..., registry=..., sources=...,
  session_factory=...)` in `app/main.py`, keeping `app = create_app()` importable and
  startable without `DEC_APP_DATABASE_URL` (`design.md` decisions 1, 7) (backend);
  verify: with the variable unset, `GET /health` answers `{"status": "ok"}` and the
  lifespan builds the registry from `ApiSettings` only
- [ ] 2.4 Add `api/errors.py`: the error body and the handlers of `design.md` decision 5,
  including `404` for an unknown route and `405` for a wrong method (backend); verify: a
  test app with throwaway routes raising each mapped error gives the table's status and
  `code`; every `422` body has `fields`, without the input echo; a `500` body holds none
  of the exception's text; captured log lines of a `422`, a `503` and a `500` hold the
  `code` and the route and no request value
- [ ] 2.5 Add the 1 MiB body-size middleware (`design.md` decision 6) (backend); verify:
  a body over 1 MiB, with a declared `Content-Length` and chunked without one, gives
  `413 payload_too_large` before the route runs (a spy on the route); a body of exactly
  1 MiB passes

## 3. Storage (backend)

- [ ] 3.1 Add `models/calculation_result.py` (`design.md` decision 4) and one Alembic
  revision on top of `869e03eddcc5`, plus `tests/test_calculation_result_postgres.py`
  marked `postgres` and skipped unless `DEC_TEST_APP_DATABASE_URL` is set (register the
  marker in `backend/pyproject.toml`) (backend); verify: the metadata creates the table
  on SQLite in a test; with the variable set to a hand-made database on `dec-postgres`,
  `alembic upgrade head` creates the table with the columns of decision 4,
  `alembic downgrade 869e03eddcc5` drops it, and both run without error
- [ ] 3.2 Add `repositories/calculation_result.py` with `add` and `get` only (backend);
  verify: on SQLite, an added row reads back with every column equal; `get` of an unknown
  id returns nothing; the repository has no update or delete method; the `postgres`
  module stores and reads an envelope whose floats include `-0.0`, `1e-07` and `172.5`
  and gets the same JSON text back
- [ ] 3.3 Add the session provider of `design.md` decision 7: lazy `Settings`, a cached
  engine and session factory, and the translation of a missing or invalid
  `DEC_APP_DATABASE_URL` and of `OperationalError` into `DatabaseUnavailableError`
  (backend); verify: with the variable unset, and with a URL to a closed port, a request
  that needs the database answers `503 database_unavailable`, and neither the body nor
  the log line holds the URL or the driver's text

## 4. Services (backend)

- [ ] 4.1 Add `services/catalog.py`: `build_registry(params_root)`, which registers the
  pilot from its `.yaml`, and `calculation_types(registry)`, which returns
  `CalculationTypeView` values; add the `ParameterSource` protocol and
  `ResolvedParameters` (`design.md` decisions 2, 3, 10) (backend); verify: the built
  registry holds `foundations_shallow_r` with the rounding rule of its `.yaml` and that
  rule's engineer and rationale as `rounding_source`; a missing `.yaml`, an invalid one,
  or a rounding rule without its engineer or rationale makes `build_registry` raise a
  `DECError` subclass naming the file and the value (the output quantity of the rule); the views list inputs and outputs in contract
  order with dimensions from the unit vocabulary
- [ ] 4.2 Change `CalculationRequest.check_against` to collect every offending input
  into one `InputValidationError` carrying their names (`design.md` decision 5), and
  extend `CalculationService.submit` with the parameter sources and the repository,
  checking in the order of decision 3 (registered type, contract, source, run, store)
  (backend); verify: the WP2 request tests still pass; two missing and one undeclared
  input give one error naming all three; a spy shows the engine and the repository are
  not called on an unknown type, a contract mismatch, or a missing source; a refused
  calculation is stored with verdict `refused`
- [ ] 4.3 Add `CalculationService.get` and the stored-record fields of "Reproducible
  stored result" (backend); verify: the stored record holds the calculation type, the
  request inputs with units, the envelope, `engine_version`, `input_hash`, the storage
  time, and the distinct documents and editions of `norm_refs` in first-use order;
  re-running stored inputs with the same `.yaml` and the same synthetic source gives the
  same `input_hash` and an envelope equal except `result_id`; `get` of an unknown id
  raises `NotFoundError`; no return value of the service is an instance of a class from
  `app.models` (`backend-architecture` "No layer mixing")
- [ ] 4.4 Add `CalculationService.report(result_id, report_request) -> bytes`
  (`design.md` decision 9) (backend); verify: the `.docx` read back holds the stored
  inputs, trace, conclusion and accountability block; a refused result's report states
  the refusal and names the bound; an unknown id raises `NotFoundError`; a stored result
  whose type is no longer registered raises `CalculationTypeNotRegisteredError`

## 5. API (backend)

- [ ] 5.1 Add `api/dependencies.py` (session per request, service provider) and
  `GET /calculation-types` (backend); verify: `TestClient` gets `200` with the
  registry's types in contract order, and `200` with `[]` from an empty registry; with
  `DEC_APP_DATABASE_URL` unset, `GET /calculation-types` still answers `200` (the session
  is opened only by routes that need it)
- [ ] 5.2 Add `POST /calculations` (`201`, `Location`) (backend); verify, on SQLite with
  a synthetic source through `dependency_overrides`: every scenario of "Run a
  calculation", "Calculation request validation over HTTP" and "Calculation parameter
  source" (`404`, both `422` codes with their `fields`, `503` without a source, nothing
  stored on any rejection, client-supplied parameters rejected as unknown fields, a unit
  outside the vocabulary rejected as `validation_error`)
- [ ] 5.3 Add `GET /calculations/{result_id}` (backend); verify: the `GET` body equals
  the `POST` body; `404` for an unknown UUID; `422` for `abc`; `PUT`, `PATCH` and
  `DELETE` give `405 method_not_allowed` and the stored result is unchanged
- [ ] 5.4 Add `POST /calculations/{result_id}/report` (backend); verify: `200` with the
  `.docx` media type and an `attachment` file name `dec-report-<result_id>.docx`; the
  body opens with python-docx and holds the stored result; `422` on an invalid report
  request; `404` on an unknown id; `409 calculation_type_not_registered` for a stored
  result of a type missing from the test registry
- [ ] 5.5 Add the CORS middleware from `ApiSettings` and declare every error response of
  each route in the OpenAPI description (backend); verify: a preflight from a configured
  origin is allowed and one from another origin is not; with no origin configured none is
  allowed; `/openapi.json` lists the four endpoints with their request schemas, success
  responses, the `ErrorBody` schema, and the `404`, `409`, `422` and `503` responses where
  the spec defines them

## 6. Verification and close

- [ ] 6.1 Add the latency check to the `postgres` module: one warm-up request, then 20
  sequential `POST /calculations` for the pilot with a synthetic in-process source; the
  median is at most 1 second (backend); verify: the test passes against the hand-made
  `dec_app`, and the measured median is recorded in the code journal
- [ ] 6.2 Manual run: `uvicorn app.main:app --host 127.0.0.1` with `DEC_APP_DATABASE_URL`
  pointing at a migrated `dec_app`; check `/health`, `/docs`, `GET /calculation-types`,
  and that `POST /calculations` for the pilot answers `503 parameter_source_unavailable`
  (no catalog source exists yet); then stop the database and check `503
  database_unavailable`; record the commands and the answers in the code journal
  (backend); verify: the recorded answers match the spec
- [ ] 6.3 `tester` issues the GO for `feature/calculation-api/backend`: `backend/check.sh`
  passes (`ruff`, `mypy`, `pytest`, ≥ 95% branch coverage), and the `postgres` module
  passes against a hand-made `dec_app` (backend)
- [ ] 6.4 Review by the orchestrator or Egor, then merge into `develop` after both WP2
  features (backend)
- [ ] 6.5 (spec) `spec-keeper` syncs the delta into `openspec/specs/calculation-api/` and
  archives the change after `calculation-core-contract` is archived

## Requirement coverage

| Requirement | Verified by |
|---|---|
| Calculation types listing | tasks 4.1, 5.1 |
| Run a calculation | tasks 4.2, 5.2 |
| Calculation request validation over HTTP | tasks 4.2, 5.2 |
| Stored result retrieval | tasks 3.2, 4.3, 5.3 |
| Reproducible stored result | tasks 3.2, 4.3, 5.3 (`405` on change methods) |
| Report download | tasks 4.4, 5.4 |
| Error responses | tasks 2.4 (mapping, bodies, logs), 2.5 (`413`), 3.3 (`503` database); tasks 5.1-5.4 (per route) |
| Calculation parameter source | tasks 4.1 (engineer-set sources), 4.2, 5.2 |
| API documentation | task 5.5 |
| Cross-origin requests | tasks 2.1, 5.5 |
| Non-functional — request size and latency | tasks 2.5 (size), 6.1 (latency) |
| `backend-architecture` "No layer mixing" (verified here as the first endpoint that returns data) | task 4.3 |

## DOR checklist

- [x] `proposal.md` (with "Non-goals"), `specs/calculation-api/spec.md`, `design.md`,
  `tasks.md` exist
- [x] `openspec validate --strict` passes and a `spec-reviewer` report on the current
  version lists no blocker and no major finding (tasks 1.1, 1.2;
  `docs/decisions/calculation-api-readiness.md`)
- [x] Functional requirements and scenarios recorded; each requirement is mapped to a
  task ("Requirement coverage")
- [x] Non-functional requirements recorded (spec "Non-functional — request size and
  latency"; `design.md`, "Non-functional requirements")
- [x] Each task is small enough for one session (Akim's judgement, 2026-10-02; tasks
  2.3, 4.2 and 5.2 of the first draft split after `spec-reviewer` pass 1)
- [x] Acceptance and Go/No-Go criteria written (every task has a verify clause; section
  below)
- [x] Branch defined (header)
- [x] Dependencies satisfied (below): every WP2 part this change uses is implemented on
  `feature/report-generator/backend`; the open WP2 items (task 6.2 waiting for Egor's
  task 1.8) decide only the merge order, not the start of this change (2026-10-03: task
  1.8 closed and 6.2 checked off, the hash algorithm unchanged)

## DOD and Go / No-Go

- GO is declared only by the `tester` agent. This change has code, so it takes the
  normal test and coverage path.
- Spec phase: `openspec validate --all --strict` passes; the current `spec-reviewer`
  report lists no blocker and no major finding; `norm-traceability-checker` confirms that
  no norm value is fixed.
- Implementation: every task is checked off; every verify clause passes; `ruff` and
  `mypy` pass; branch coverage ≥ 95%; the `postgres` module passes; no secret, input
  value or stack trace appears in a response or a log line.
- NO-GO: any of: a failed validation; an open blocker or major finding; a failed verify
  clause; coverage < 95%; a security finding; a norm value added in code, configuration
  or non-test data; any file in Egor's zones changed.
- Archive only after GO and after `calculation-core-contract` is archived.

## Dependencies

- `backend-layered-architecture` (WP5): applied and merged into `develop` (settings,
  session, Alembic tree, parameters layer, registry). Satisfied.
- `calculation-core-contract` (WP2): this change uses its `CalculationRequest`,
  `ResultEnvelope`, `CalculationService`, the pilot type and its registration (engine
  tasks 2.1-6.1b, 7.1a, 7.1b), and `build_report` and `render_docx` (report tasks
  6.2a-6.4). All are implemented on `feature/report-generator/backend`, which this
  branch starts from, so the change can start now. This branch merges after
  `feature/calculation-engine/backend` and `feature/report-generator/backend`. The
  engine's task 6.2 (`input_hash`) waits only for Egor's acknowledgement (task 1.8); if
  his answer changes the hash algorithm, the stored `input_hash` follows the engine, and
  no stored data exists before the merge. Update 2026-10-03: Egor acknowledged task 1.8
  with no change to the algorithm (`a01af6f`), and task 6.2 is checked off; only the merge
  order is left.
- `normative-catalog-backend` (planned, Akim and Egor): implements `ParameterSource` for
  the catalog. This change does not wait for it; until it exists, a real request for the
  pilot answers `503`.
- `user-accounts-auth` (planned, Akim): protects these endpoints and ties results to
  users. It builds on this branch.
- `bootstrap-dev-environment` task 5.1 (`import-linter`, its own branch) checks the layer
  order that this change follows; not a dependency of this change's GO.
