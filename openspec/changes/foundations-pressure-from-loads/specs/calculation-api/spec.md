## MODIFIED Requirements

### Requirement: Run a calculation
The system SHALL expose `POST /calculations`, which takes a calculation request (a
calculation type name and each input as a value with its unit), runs the calculation,
stores its result envelope, and returns that envelope with status `201` and a `Location`
header naming the stored result. A calculation that the method's range refuses
(`calculation-engine` "Applicability check with three outcomes") SHALL be stored and
returned the same way, with the verdict `refused`; a refusal is a result, not an error.
That requirement is defined in the canonical `calculation-engine` capability.

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

The new registered loads type SHALL use these existing endpoints, not a dedicated
endpoint. After unit conversion its typed input guard SHALL reject invalid
engineer-defined input domains, including reversed b/l, with invalid_input 422 and
named input fields; it SHALL NOT swap or round them. Normative method-bound and
derived-contact refusals remain stored 201 results with Location, not validation
errors. Pure direct calls must enforce the same typed engineering input contract.

#### Scenario: Stored derived refusal
- **WHEN** a valid loads request computes negative minimum corner pressure
- **THEN** POST returns 201 with the typed reason, limiting_corner and diagnostic prefix, GET preserves it, final outputs are empty and DOCX remains available

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
  same `engine_version`, the same `.yaml` file of the type, and a parameter source that
  returns the same values (in tests, the same synthetic source)
- **THEN** the new envelope has the same `input_hash` and is equal to the stored one
  except for `result_id`

Persistence SHALL accept engineer_formula and derived-reason variants without
recalculating stored results. The loads source metadata retains its interim marker,
profile and aggregate digest. Old stored envelopes remain valid without mandatory
new fields or rewriting their trace/reason shapes.

#### Scenario: Old and new payloads coexist
- **WHEN** stored pilot results and loads-derived refusals are retrieved
- **THEN** each payload is preserved and report generation uses its stored inputs/envelope, not a new calculation
