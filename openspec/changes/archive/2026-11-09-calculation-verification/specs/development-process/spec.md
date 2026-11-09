## ADDED Requirements

### Requirement: Correctness gate for calculation changes

The system SHALL require, for a change that contains code that adds or modifies a
calculation, that the
tester agent verifies correctness in addition to the coverage gate: the reference suite
of `calculation-verification` passes within tolerance, the invariant tests pass, and the
metrics "deviation from the references", "reproducibility rate", and "traceability
completeness" are attached to the GO verdict, and the regression corpus of
`calculation-verification` shows no undeclared difference. The traceability completeness
has no threshold. The requirement "Test gate with >= 95% branch coverage" is unchanged
and still applies.

#### Scenario: Calculation change passes the correctness gate
- **WHEN** a change modifies a calculation and the reference suite is within tolerance,
  the invariant tests pass, and the metrics are attached
- **THEN** the correctness gate is satisfied, and GO still needs the coverage gate

#### Scenario: Change without calculation code
- **WHEN** a change contains no code that adds or modifies a calculation
- **THEN** the correctness gate does not apply

#### Scenario: Reference suite fails
- **WHEN** a change modifies a calculation and any reference output is outside its
  tolerance
- **THEN** the verdict is NO-GO even if branch coverage is at least 95%
