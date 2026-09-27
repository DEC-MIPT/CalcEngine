## REMOVED Requirements

### Requirement: Non-functional — performance and accuracy
**Reason**: It joins two targets in one requirement. "99.9% accuracy" names no quantity,
reference, or population and cannot be measured (audit finding A3). The latency target
was not separate from it (audit finding E1).
**Migration**: The accuracy target is replaced by "Calculation accuracy", which states
accuracy as deviation from the named reference examples of `calculation-verification`.
The 30-second latency target moves unchanged to "Calculation latency".

## ADDED Requirements

### Requirement: Calculation accuracy
The system SHALL express the accuracy of a calculation as its deviation from named
reference examples, as defined by the requirement "Reference examples" of
`calculation-verification`. An accuracy claim SHALL name the calculation type, the
quantity, and the reference examples it refers to. An abstract percentage without those
SHALL NOT be used as an accuracy claim.

#### Scenario: Accuracy is stated against references
- **WHEN** accuracy is claimed for a calculation type
- **THEN** the claim is stated as the deviation of named quantities from named reference
  examples, within the `tolerance` each example records

### Requirement: Calculation latency
The system SHALL complete a typical calculation in under 30 seconds. This target is
independent of accuracy. What counts as a typical calculation and where the time is
measured are not yet defined.

#### Scenario: Calculation completes in time
- **WHEN** a typical calculation runs
- **THEN** it completes in under 30 seconds
