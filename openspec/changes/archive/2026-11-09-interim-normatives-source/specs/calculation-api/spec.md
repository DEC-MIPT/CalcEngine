## ADDED Requirements

### Requirement: Parameter source in the result envelope
The result envelope returned by `POST /calculations` and `GET /calculations/{result_id}` SHALL
carry an optional `parameter_source` object with `kind` (`catalog` or `interim`),
`data_sha256` (64 lowercase hex characters for `interim`, `null` for `catalog`) and `profile`
(`strict` or `draft` for `interim`, `null` for `catalog`). A new result SHALL carry it
whenever its parameter source describes itself, which the catalog and interim sources always
do; a source that gives no description, and a result stored before the field existed, SHALL
yield an envelope without it, and its validation SHALL NOT fail. The field SHALL NOT enter `input_hash`, and the engine SHALL NOT read it. The
field SHALL be published in the OpenAPI schema.

#### Scenario: New interim result
- **WHEN** a calculation runs with `DEC_PARAMETER_SOURCE=interim` in the `strict` profile
- **THEN** the `201` envelope has `parameter_source` with kind `interim`, the data digest and
  profile `strict`, and `GET /calculations/{result_id}` returns the same object

#### Scenario: New catalog result
- **WHEN** a calculation runs with the catalog source
- **THEN** the envelope has `parameter_source` with kind `catalog`, `data_sha256` `null` and
  `profile` `null`

#### Scenario: Same inputs, same hash across sources
- **WHEN** the same inputs are computed on the catalog and on interim data with equal values
  and references
- **THEN** both results have the same `input_hash`, and only `parameter_source` differs

#### Scenario: Source without a description
- **WHEN** a calculation runs with a parameter source that gives no description
- **THEN** the `201` envelope has no `parameter_source`, and the result is otherwise the same

#### Scenario: Stored result without the field
- **WHEN** `GET /calculations/{result_id}` reads a result stored before the field existed
- **THEN** the response is `200` without `parameter_source`

## MODIFIED Requirements

### Requirement: Calculation parameter source
The system SHALL resolve the parameters of a calculation from two sources only: the
engineer-set values (rounding rules, validated range) from the calculation type's
`.yaml` file (`backend-architecture` "Engineer-set parameters stored in YAML"), each
carrying its source (the engineer and the rationale), and the
norm-given values (formulas, table values, thresholds, the method's range) from the
normative catalog through a parameter source for that type, or from the explicitly
selected interim source under `interim-normatives` "Scoped exception to the
normative-database rule". The system SHALL NOT take a norm-given value from code or
from the client; `.yaml` norm data are allowed only under that scoped exception. A
calculation type with no configured usable parameter source SHALL be rejected with
`503` and the error body, and
nothing SHALL be stored.

#### Scenario: Type without a catalog source
- **WHEN** the catalog source is selected and a client posts a valid request for a
  registered type that has no configured catalog parameter source
- **THEN** the response is `503` with the error body naming the calculation type, the
  engine does not run, and nothing is stored

#### Scenario: Parameters from the configured source
- **WHEN** a client posts a valid request for a type whose parameter source is
  configured
- **THEN** the engine receives the engineer-set values from the type's `.yaml` file and
  the norm-given values from that source, and the request body supplies only the inputs

#### Scenario: Engineer-set value without its source
- **WHEN** a calculation type's `.yaml` file holds a rounding rule or a validated-range
  bound without the engineer or the rationale
- **THEN** the application does not start, and the error names the file and the value

#### Scenario: Client cannot supply parameters
- **WHEN** a client adds formulas, coefficients, bounds or rounding rules to a
  calculation request
- **THEN** the request is rejected with `422` as an unknown field
