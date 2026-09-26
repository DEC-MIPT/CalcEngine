## REMOVED Requirements

### Requirement: Deterministic verified calculation
**Reason**: Its only scenario is bound to the placeholder domain, and a MODIFIED block
cannot drop that scenario.
**Migration**: Replaced by "Deterministic verified calculation of in-scope types" below,
which keeps the requirement text and uses first-domain scenarios.

## ADDED Requirements

### Requirement: Deterministic verified calculation of in-scope types
The system SHALL execute engineering calculations with verified algorithms in Python
(NumPy/SciPy) that strictly follow the bound normative method.

#### Scenario: Run a first-domain calculation
- **WHEN** an engineer enters inputs for an in-scope shallow-foundation calculation type
  listed in `foundations-shallow`
- **THEN** the engine computes the result using the verified algorithm bound to that
  type, with no arithmetic drift and no ML influence, and the same inputs and the same
  norm edition give the same result

#### Scenario: Unverified norm source
- **WHEN** the bound normative method has no source checked against the primary text
- **THEN** the result is marked `source: unverified` and the engine does not treat it as
  a verified result

#### Scenario: Out-of-scope type
- **WHEN** an engineer requests a calculation type not listed in `foundations-shallow`
- **THEN** the engine does not run it and reports that the type is out of scope
