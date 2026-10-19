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
