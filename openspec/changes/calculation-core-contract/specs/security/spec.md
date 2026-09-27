## MODIFIED Requirements

### Requirement: Input validation
The system SHALL validate all user input through typed schemas at the API boundary and
SHALL NOT trust client-provided data. This validation checks form, types, and the ranges
that belong to the data schema. It does not check the calculation method's range; that
is the `calculation-engine` requirement "Applicability check with three outcomes", which
runs after this validation and does not replace it.

#### Scenario: Invalid input rejected
- **WHEN** a request contains malformed or out-of-range input
- **THEN** it is rejected with a validation error before reaching business logic

#### Scenario: Method bound is not a schema bound
- **WHEN** a request passes schema validation but an input is outside the method's range
- **THEN** the request reaches the engine, and the engine refuses the calculation under
  "Applicability check with three outcomes", naming the bound and its `NormRef` list
