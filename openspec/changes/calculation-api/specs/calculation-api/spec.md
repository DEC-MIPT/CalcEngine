# Spec Delta

## Purpose
Defines the HTTP contract through which clients list calculation types, run a
calculation, read a stored result, and download its `.docx` report. It also defines the
error responses, how results are stored for reproducibility, and where a calculation's
parameters come from.

## ADDED Requirements

### Requirement: Calculation types listing
The system SHALL expose `GET /calculation-types`, which returns every registered
calculation type with its name, its declared inputs (each with its name, base unit and
the unit's dimension), and its declared outputs (each with its name and base unit), in
the order the type's contract declares them.

#### Scenario: List the registered types
- **WHEN** a client sends `GET /calculation-types`
- **THEN** the response is `200` with one entry per registered calculation type, and
  each entry lists the type's inputs and outputs as its contract declares them

#### Scenario: No type registered
- **WHEN** no calculation type is registered and a client sends `GET /calculation-types`
- **THEN** the response is `200` with an empty list

### Requirement: Run a calculation
The system SHALL expose `POST /calculations`, which takes a calculation request (a
calculation type name and each input as a value with its unit), runs the calculation,
stores its result envelope, and returns that envelope with status `201` and a `Location`
header naming the stored result. A calculation that the method's range refuses
(`calculation-engine` "Applicability check with three outcomes") SHALL be stored and
returned the same way, with the verdict `refused`; a refusal is a result, not an error.

#### Scenario: Calculation completes
- **WHEN** a client posts a valid request for a registered type whose inputs are inside
  the method's range
- **THEN** the response is `201`, its body is the result envelope with a new
  `result_id`, and `Location` is `/calculations/{result_id}`

#### Scenario: Calculation refused by the method's range
- **WHEN** a client posts a valid request with an input outside the method's range
- **THEN** the response is `201`, the envelope's verdict is `refused`, its
  `verdict_reason` names the violated bound, and the result is stored

#### Scenario: Two runs of one request
- **WHEN** a client posts the same request twice
- **THEN** both responses are `201` with different `result_id` values, the same
  `input_hash`, and envelopes that are otherwise equal

### Requirement: Calculation request validation over HTTP
The system SHALL validate a calculation request at the API boundary, as `security`
"Input validation" requires, and SHALL reject an invalid request before the calculation
engine runs and before anything is stored. A request whose calculation type is not
registered SHALL be rejected with `404`. A request that is malformed, carries a
non-finite number, names a unit outside the unit vocabulary, misses a declared input,
adds an undeclared input, or gives an input in a unit of another dimension SHALL be
rejected with `422`.

#### Scenario: Malformed request
- **WHEN** a client posts a body that is not a calculation request (a missing field, a
  wrong type, an unknown field, or a non-finite number)
- **THEN** the response is `422` with the error body, the engine does not run, and
  nothing is stored

#### Scenario: Unknown calculation type
- **WHEN** a client posts a request whose calculation type is not registered
- **THEN** the response is `404` with the error body, and nothing is stored

#### Scenario: Inputs do not fit the type's contract
- **WHEN** a client posts a request with a missing or undeclared input, or with an input
  in a unit of another dimension than the declared one
- **THEN** the response is `422` with the error body naming the input, the engine does
  not run, and nothing is stored

#### Scenario: Input outside the method's range is not a validation error
- **WHEN** a client posts a well-formed request whose input lies outside the method's
  range
- **THEN** the request passes validation and the engine refuses the calculation under
  "Run a calculation"; the response is not `422`

### Requirement: Stored result retrieval
The system SHALL expose `GET /calculations/{result_id}`, which returns the stored result
envelope with `200`, unchanged from the envelope that `POST /calculations` returned. An
unknown `result_id` SHALL give `404`, and a `result_id` that is not a UUID SHALL give
`422`.

#### Scenario: Read a stored result
- **WHEN** a client sends `GET /calculations/{result_id}` for a result it created
- **THEN** the response is `200` and its body equals the body of the `201` response that
  created the result

#### Scenario: Unknown result
- **WHEN** a client sends `GET /calculations/{result_id}` with a UUID that names no
  stored result
- **THEN** the response is `404` with the error body

#### Scenario: Not a UUID
- **WHEN** a client sends `GET /calculations/abc`
- **THEN** the response is `422` with the error body

### Requirement: Reproducible stored result
The system SHALL store, for each result, the calculation type, the inputs as the request
gave them, the result envelope, `engine_version`, `input_hash`, the time it was stored,
and the document and edition of every `NormRef` in the envelope, so that the result can
be re-run and compared later (`agent-docs/domain-constraints.md`, "Reproducibility"). A
stored result SHALL NOT be changed after it is stored.

#### Scenario: Stored fields
- **WHEN** a calculation completes or is refused
- **THEN** its stored record holds the calculation type, the request inputs with their
  units, the envelope, `engine_version`, `input_hash`, the storage time, and each
  document with its edition from the envelope's `norm_refs`

#### Scenario: Re-run from the stored record
- **WHEN** the stored inputs of a result are posted again for the same type, with the
  same parameters and the same `engine_version`
- **THEN** the new envelope has the same `input_hash` and is equal to the stored one
  except for `result_id`

### Requirement: Report download
The system SHALL expose `POST /calculations/{result_id}/report`, which takes a report
request (the title-block data, the signature-block setting and the signatories) and
returns the `.docx` report of the stored result with `200`, the media type
`application/vnd.openxmlformats-officedocument.wordprocessingml.document`, and a
`Content-Disposition` header of type `attachment` with a file name that ends in `.docx`.
The report SHALL be built from the stored inputs and the stored envelope only, so the
client does not send the calculation again. An unknown `result_id` SHALL give `404`, and
an invalid report request SHALL give `422`. The report follows `report-generator`; this
requirement adds only its delivery.

#### Scenario: Download the report of a stored result
- **WHEN** a client posts a valid report request for a stored result
- **THEN** the response is `200` with the `.docx` media type and an attachment file name
  ending in `.docx`, and the document read back holds the stored result's inputs, trace,
  conclusion and accountability block

#### Scenario: Report of a refused result
- **WHEN** a client posts a valid report request for a stored result whose verdict is
  `refused`
- **THEN** the response is `200` and the report states the refusal and names the
  violated bound, as `report-generator` requires

#### Scenario: Invalid report request
- **WHEN** a client posts a report request that the report schema rejects (for example a
  missing developer surname while the signature block is enabled)
- **THEN** the response is `422` with the error body, and no document is returned

#### Scenario: Report of an unknown result
- **WHEN** a client posts a report request for a `result_id` that names no stored result
- **THEN** the response is `404` with the error body

### Requirement: Error responses
The system SHALL answer every error of this capability with a JSON body that holds a
stable machine-readable `code` and a human-readable `message`, and, for a validation
error, the location of each invalid field. It SHALL map errors to status codes as
follows: a missing resource `404`; an invalid request `422`; a calculation type with no
configured parameter source `503`; any other error `500` with a generic message. No
error body SHALL contain a stack trace, an SQL statement, a file path, or a
configuration value.

#### Scenario: Validation error body
- **WHEN** a request is rejected with `422`
- **THEN** the body has a `code`, a `message`, and the location of each invalid field

#### Scenario: Unexpected error
- **WHEN** an unexpected error occurs while a request is handled
- **THEN** the response is `500` with a `code` and a generic `message`, and the body
  holds no stack trace, SQL, file path, or configuration value

#### Scenario: Error log without request data
- **WHEN** an error is logged while a request is handled
- **THEN** the log line names the error `code` and the endpoint, and holds no input
  value, database URL, or credential (`security` "No sensitive data in logs")

### Requirement: Calculation parameter source
The system SHALL resolve the parameters of a calculation from two sources only: the
engineer-set values (rounding rules, validated range) from the calculation type's
`.yaml` file (`backend-architecture` "Engineer-set parameters stored in YAML"), and the
norm-given values (formulas, table values, thresholds, the method's range) from the
normative catalog through a parameter source for that type. The system SHALL NOT take a
norm-given value from code, from a `.yaml` file, or from the client. A calculation type
with no configured catalog source SHALL be rejected with `503` and the error body, and
nothing SHALL be stored.

#### Scenario: Type without a catalog source
- **WHEN** a client posts a valid request for a registered type that has no configured
  catalog parameter source
- **THEN** the response is `503` with the error body naming the calculation type, the
  engine does not run, and nothing is stored

#### Scenario: Parameters from the configured source
- **WHEN** a client posts a valid request for a type whose parameter source is
  configured
- **THEN** the engine receives the engineer-set values from the type's `.yaml` file and
  the norm-given values from that source, and the request body supplies only the inputs

#### Scenario: Client cannot supply parameters
- **WHEN** a client adds formulas, coefficients, bounds or rounding rules to a
  calculation request
- **THEN** the request is rejected with `422` as an unknown field

### Requirement: API documentation
The system SHALL publish an OpenAPI description in which every endpoint of this
capability appears with its request schema, its success response schema or media type,
and its error responses with the error body schema (`web-platform` "Backend API").

#### Scenario: Inspect the calculation endpoints
- **WHEN** a developer reads the OpenAPI description
- **THEN** each endpoint of this capability is listed with its request schema, its
  success response, and its `404`, `422` or `503` responses where this capability defines
  them

### Requirement: Cross-origin requests
The system SHALL accept cross-origin browser requests only from the origins named in
configuration, and SHALL accept none when no origin is configured.

#### Scenario: Configured origin
- **WHEN** a browser request comes from an origin named in configuration
- **THEN** the response allows that origin

#### Scenario: Other origin
- **WHEN** a browser request comes from an origin not named in configuration, or no
  origin is configured
- **THEN** the response does not allow that origin

### Requirement: Non-functional — request size and latency
The system SHALL reject a request body larger than 1 MiB with `413` and the error body
before it is parsed. A `POST /calculations` for a registered type with an in-process
parameter source SHALL respond within 1 second on a developer machine, excluding the
first request after start-up; the report endpoint SHALL stay within `report-generator`
"Non-functional — generation time".

#### Scenario: Oversized request
- **WHEN** a client posts a body larger than 1 MiB to any endpoint of this capability
- **THEN** the response is `413` with the error body, and the body is not parsed

#### Scenario: Calculation latency
- **WHEN** the pilot calculation type runs through `POST /calculations` with a synthetic
  in-process parameter source and a reachable `dec_app`
- **THEN** the response arrives within 1 second
