# Proposal

WP8. Owner: Akim (backend zone). No task of this change is in Egor's zones.

## Why

The calculation engine and the report generator (`calculation-core-contract`, WP2) are
implemented, but nothing outside the backend can reach them: the only endpoint is
`GET /health`. WP2 left the missing pieces to "a later change" that does not exist yet:

- **The calculation endpoint and the stored result.** WP2 `design.md` decision 12: "Storing
  the envelope in `dec_app` and the calculation endpoint belong to a later change", and the
  HTTP scenarios of `security` "Input validation" "are tested by the change that adds the
  endpoint".
- **The report download.** WP2 `design.md` decision 18: "the download endpoint belongs to
  the change that adds the API".
- **ORM isolation.** `backend-layered-architecture` (WP5) "No layer mixing" is verified "by
  the first endpoint that returns data"; no such endpoint exists.
- **Reproducibility.** `agent-docs/domain-constraints.md`: a stored result records its
  inputs, norm document and norm edition, so that it can be re-run and compared. Nothing
  stores a result today.

The frontend (WP2 tasks 3.4, 3.5, 5.4, feature `frontend-app`) needs this API to show a
calculation, and MVP testing needs it to run one end to end.

## What Changes

- A new capability `calculation-api`: the HTTP contract of calculations.
  - `GET /calculation-types`: the registered calculation types with their declared
    inputs and outputs.
  - `POST /calculations`: runs a `CalculationRequest` and returns the stored
    `ResultEnvelope`; a refusal by the method's range is a stored result, not an error.
  - `GET /calculations/{result_id}`: returns a stored envelope.
  - `POST /calculations/{result_id}/report`: returns the `.docx` report of a stored
    result for a `ReportRequest`.
  - One error body for every error response, and a fixed mapping of backend errors to
    HTTP status codes.
  - An OpenAPI description of every endpoint above.
  - Cross-origin requests accepted only from origins named in configuration.
- Storage of each result in `dec_app`: the request inputs, the envelope, the calculation
  type, `engine_version`, `input_hash`, and the norm documents with their editions.
- A parameter source per calculation type behind one interface. The engineer-set values
  come from the type's `.yaml` file, as WP5 specifies. The norm-given values (formulas,
  table values, thresholds, the method's range) come from the normative catalog, through
  the planned change `normative-catalog-backend`. Until that change exists, a type with
  no catalog source answers with a defined error, and tests use a synthetic source.

## Capabilities

### New Capabilities

- `calculation-api`: the HTTP contract of calculation types, calculations, stored
  results, and report download; the error body and status mapping; storage of results in
  `dec_app`; the parameter source interface; allowed cross-origin requests.

### Modified Capabilities

None. `security` "Input validation" is already modified by `calculation-core-contract`;
this change references that requirement by name and adds its HTTP scenarios in
`calculation-api`, so the two changes do not edit the same requirement.

## Non-goals

- Authentication and accounts. The planned change `user-accounts-auth` adds login and
  JWT, protects these endpoints, and ties each stored result to its user. Until then the
  endpoints are open and run only on a developer machine.
- Reading `dec_normatives`, normative search, and the catalog parameter source: planned
  change `normative-catalog-backend` (Akim and Egor). This change defines only the
  interface that source implements.
- Any norm value: no formula, coefficient, threshold, bound, or rounding rule is added in
  code, configuration, or test data other than synthetic placeholders.
- A list of a user's results, deleting a result, or editing one; pagination.
- PDF output (a `product-vision` non-goal before the defense).
- Background jobs in `worker`: a calculation and its report run within the request
  (`report-generator` "Non-functional — generation time": under 1 minute).
- Docker, the `dec_app` database in `infra/docker-compose.yml`, and deployment (Egor's
  infrastructure change).
- The `import-linter` contracts that check the layer order (`bootstrap-dev-environment`
  task 5.1, its own feature branch).

## Impact

- Code (backend zone): `backend/app/api` (routes, error handlers), `backend/app/services`
  (calculation service with storage and report), `backend/app/models` and
  `backend/app/repositories` (the stored result), `backend/app/schemas` (response
  schemas), `backend/app/core` (settings for allowed origins and the params root),
  `backend/alembic/versions` (one migration), `backend/app/main.py`.
- Dependencies: `uvicorn` in `backend/requirements.txt`, to run the server.
- Feature branch: `feature/calculation-api/backend`, from
  `feature/report-generator/backend` (which carries the engine), merged after the WP2
  features.
- Consumers: `frontend-app` (WP2 tasks 3.4, 3.5, 5.4); `user-accounts-auth` and
  `normative-catalog-backend` build on this change.
