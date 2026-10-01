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

- [ ] 1.1 (spec) Run `openspec validate calculation-api --strict` and
  `openspec validate --all --strict`; verify: both pass
- [ ] 1.2 (spec) Run `spec-reviewer` on this change and resolve its findings until a
  report on the current version lists no blocker and no major finding; record the passes
  in `docs/decisions/calculation-api-readiness.md`
- [ ] 1.3 (spec) Run `norm-traceability-checker`; verify: it confirms that no
  requirement of this change fixes a formula, coefficient, limit or rounding rule

## 2. Groundwork (backend)

- [ ] 2.1 Create the branch from `feature/report-generator/backend`. Add `uvicorn` to
  `backend/requirements.txt`. Add `ApiSettings` (`DEC_CORS_ORIGINS`, comma-separated,
  empty by default, no required field) and the `dec_params_root` field of `Settings`,
  defaulting to `backend/params` resolved from the package (`design.md` decision 7)
  (backend); verify: tests show an empty origin list without the variable, two origins
  from `"a,b"`, the default params root pointing at the directory that holds
  `foundations_shallow_r.yaml`, and an override from the environment
- [ ] 2.2 Add `schemas/api.py` (`ErrorBody`, `FieldError`, `CalculationTypeView` with
  its input and output views) and `ParameterSourceUnavailableError(DECError)` in
  `core/exceptions.py` (backend); verify: schema tests for every field, including
  `fields` absent outside `422`; the new exception is a `DECError`
- [ ] 2.3 Add `create_app(registry=..., sources=..., session_factory=...)` in
  `app/main.py` and `api/errors.py` with the handlers and status mapping of `design.md`
  decision 5, plus the 1 MiB body-size middleware (decision 6), keeping
  `app = create_app()` importable without `DEC_APP_DATABASE_URL` (backend); verify:
  `GET /health` still answers `{"status": "ok"}` with no database variable set; a test
  app with throwaway routes raising each mapped error gives the table's status and
  `code`; a `500` body holds none of the exception's text; a `RequestValidationError`
  body has `fields` without the input echo; a body over 1 MiB, declared or chunked, gives
  `413` before parsing; a captured log line of a `500` holds the `code` and route and no
  request value

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

## 4. Services (backend)

- [ ] 4.1 Add `services/catalog.py`: `build_registry(params_root)`, which registers the
  pilot from its `.yaml`, and `calculation_types(registry)`, which returns
  `CalculationTypeView` values; add the `ParameterSource` protocol and
  `ResolvedParameters` (`design.md` decisions 2, 3, 10) (backend); verify: the built
  registry holds `foundations_shallow_r` with the rounding rule of its `.yaml`; a missing
  or invalid `.yaml` makes `build_registry` raise a `DECError` subclass; the views list
  inputs and outputs in contract order with dimensions from the unit vocabulary
- [ ] 4.2 Extend `CalculationService` with the parameter sources and the repository:
  `submit` checks in the order of `design.md` decision 3 (registered type, contract,
  source, run, store) and returns the stored `ResultEnvelope`; `get` returns a stored
  envelope; the service returns schemas only (backend); verify: a spy shows the engine
  and the repository are not called on an unknown type, a contract mismatch, or a missing
  source; a refused calculation is stored with verdict `refused`; the stored record holds
  the fields of "Reproducible stored result", including the distinct documents and
  editions of `norm_refs`; re-running stored inputs gives the same `input_hash` and an
  envelope equal except `result_id`; no return value of the service is an instance of a
  class from `app.models` (`backend-architecture` "No layer mixing")
- [ ] 4.3 Add `CalculationService.report(result_id, report_request) -> bytes`
  (`design.md` decision 9) (backend); verify: the `.docx` read back holds the stored
  inputs, trace, conclusion and accountability block; a refused result's report states
  the refusal and names the bound; an unknown id raises `NotFoundError`; a stored result
  whose type is no longer registered raises `NotFoundError`

## 5. API (backend)

- [ ] 5.1 Add `api/dependencies.py` (session per request, service provider) and
  `GET /calculation-types` (backend); verify: `TestClient` gets `200` with the
  registry's types in contract order, and `200` with `[]` from an empty registry
- [ ] 5.2 Add `POST /calculations` (`201`, `Location`) and `GET /calculations/{result_id}`
  (backend); verify, on SQLite with a synthetic source through `dependency_overrides`:
  every scenario of "Run a calculation", "Calculation request validation over HTTP",
  "Stored result retrieval" and "Calculation parameter source" (`404`, `422` cases,
  `503` without a source, nothing stored on any rejection, client-supplied parameters
  rejected as unknown fields); the `GET` body equals the `POST` body
- [ ] 5.3 Add `POST /calculations/{result_id}/report` (backend); verify: `200` with the
  `.docx` media type and an `attachment` file name `dec-report-<result_id>.docx`; the
  body opens with python-docx and holds the stored result; `422` on an invalid report
  request; `404` on an unknown id
- [ ] 5.4 Add the CORS middleware from `ApiSettings` and declare every error response of
  each route in the OpenAPI description (backend); verify: a preflight from a configured
  origin is allowed and one from another origin is not; with no origin configured none is
  allowed; `/openapi.json` lists the four endpoints with their request schemas, success
  responses, the `ErrorBody` schema, and the `404`, `422` and `503` responses where the
  spec defines them

## 6. Verification and close

- [ ] 6.1 Add the latency check to the `postgres` module: after one warm-up request,
  `POST /calculations` for the pilot with a synthetic in-process source answers within
  1 second (backend); verify: the test passes against the hand-made `dec_app`
- [ ] 6.2 Manual run: `uvicorn app.main:app --host 127.0.0.1` with `DEC_APP_DATABASE_URL`
  pointing at a migrated `dec_app`; check `/health`, `/docs`, `GET /calculation-types`,
  and that `POST /calculations` for the pilot answers `503 parameter_source_unavailable`
  (no catalog source exists yet); record the commands and the answers in the code journal
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
| Stored result retrieval | tasks 3.2, 4.2, 5.2 |
| Reproducible stored result | tasks 3.2, 4.2 |
| Report download | tasks 4.3, 5.3 |
| Error responses | task 2.3 (mapping, bodies, logs); tasks 5.1-5.3 (per route) |
| Calculation parameter source | tasks 4.1, 4.2, 5.2 |
| API documentation | task 5.4 |
| Cross-origin requests | tasks 2.1, 5.4 |
| Non-functional — request size and latency | task 2.3 (size), task 6.1 (latency) |
| `backend-architecture` "No layer mixing" (verified here as the first endpoint that returns data) | task 4.2 |

## DOR checklist

- [x] `proposal.md` (with "Non-goals"), `specs/calculation-api/spec.md`, `design.md`,
  `tasks.md` exist
- [ ] `openspec validate --strict` passes and a `spec-reviewer` report on the current
  version lists no blocker and no major finding (tasks 1.1, 1.2)
- [x] Functional requirements and scenarios recorded; each requirement is mapped to a
  task ("Requirement coverage")
- [x] Non-functional requirements recorded (spec "Non-functional — request size and
  latency"; `design.md`, "Non-functional requirements")
- [x] Each task is small enough for one session (Akim's judgement, 2026-10-02)
- [x] Acceptance and Go/No-Go criteria written (every task has a verify clause; section
  below)
- [x] Branch defined (header)
- [ ] Dependencies satisfied (below)

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
- `calculation-core-contract` (WP2): this branch starts from
  `feature/report-generator/backend` and merges after `feature/calculation-engine/backend`
  and `feature/report-generator/backend`. Open: the engine's task 6.2 waits for Egor's
  task 1.8.
- `normative-catalog-backend` (planned, Akim and Egor): implements `ParameterSource` for
  the catalog. This change does not wait for it; until it exists, a real request for the
  pilot answers `503`.
- `user-accounts-auth` (planned, Akim): protects these endpoints and ties results to
  users. It builds on this branch.
- `bootstrap-dev-environment` task 5.1 (`import-linter`, its own branch) checks the layer
  order that this change follows; not a dependency of this change's GO.
