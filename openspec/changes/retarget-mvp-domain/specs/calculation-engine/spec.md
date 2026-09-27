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
- **WHEN** a calculation step rests on a norm reference that is not checked against the
  primary text (see `normatives-catalog` "Norm reference status")
- **THEN** the calculation still runs, that step is marked as unverified in the trace,
  the result states how many of its steps are unverified, and no label or conclusion
  shown with the result claims that it is fully verified against the norm

#### Scenario: Out-of-scope type
- **WHEN** an engineer requests a calculation type that is not on the in-scope list of
  `foundations-shallow`
- **THEN** the request is refused before any calculation runs, with a message that names
  the scope limit from `foundations-shallow`; this refusal is about the product scope
  and is separate from refusing inputs that fall outside a method's range
