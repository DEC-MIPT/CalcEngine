## Purpose

Provide explicit load assembly, inspectable load and pressure diagrams, and bounded candidate-size comparison for full-contact rectangular shallow foundations without changing historical calculations.

## ADDED Requirements

### Requirement: Weight-mode selection without double counting
The system SHALL retain the existing averaged-weight calculation and provide an explicitly selected additional-weight alternative. The proposed alternative SHALL use a separately registered calculation type with named scalar engineer-supplied downward weights and explicit force units and the agreed signed moment contributions, exclude those weights from the structural load N, and omit the averaged weight addition. The proposed new registered type SHALL identify explicit weights and upper-cut structural loads; named scalar additional moments identify already-base contributions. Any additional base-level structural-load variant requires a separately typed public contract approved before DOR; strings or numeric enum surrogates SHALL NOT be inserted into the old quantity map. Requests SHALL have an unambiguous mode and load level; the two modes SHALL NOT be combined. A base-level load SHALL NOT receive a second shear-arm transfer. No automatic conversion from full load by an averaged load factor is introduced.

Source: Akim's confirmed engineering direction in the working conversation, 2026-11-22. For the existing averaged mode, prepared SP 22.13330.2016, edition 2016 with amendments 1-5, clause 5.6.28 formula (5.11), supplies the existing pressure expression and gamma_mt; statuses remain unchanged. The scalar contribution, upper-cut structural-load and signed already-base moment assembly follows the three engineer-checked references admitted on 2026-11-22; no new normative coefficient is introduced.

#### Scenario: Averaged request remains unchanged
- **WHEN** a historical averaged-weight request is replayed with its original version and data
- **THEN** its original pressure outputs, trace, source identity and input hash remain unchanged

#### Scenario: Explicit weights replace the allowance
- **WHEN** the explicit-weight mode is selected with admitted weights
- **THEN** the total vertical force contains each supplied weight once and contains no gamma_mt*d*A allowance

#### Scenario: Ambiguous load assembly rejected
- **WHEN** a request mixes both weight modes or gives an unsupported load-level and transfer combination
- **THEN** it is rejected with named fields before calculation and values are not silently converted

### Requirement: Stored load schematic and pressure envelope
The system SHALL supply typed stored presentation data for the footing rectangle, x=b and y=l axes, signed applied loads, transfer arm, load level, added weight contributions, signed corner pressures and extrema. Every diagram value SHALL identify its stored input or trace origin. Drawing coordinates and scaling SHALL NOT alter calculation values or create a new numerical check. A completed full-contact result SHALL include a pressure envelope; a refused result SHALL label any completed pressure evidence as diagnostic and SHALL NOT draw a redistributed contact area or imply bearing success.

Source: Akim's requested schematic and pressure diagram, 2026-11-22; existing pressure contract sources are SP 22.13330.2016 edition 2016 with amendments 1-5, clauses 5.6.28-5.6.29 and the approved engineer signed-corner convention in foundations-pressure-from-loads.

#### Scenario: Diagram matches the stored result
- **WHEN** a completed result is opened
- **THEN** the diagram labels, corner signs, dimensions and extrema match the stored inputs and typed trace exactly and have a readable table alternative

#### Scenario: Refusal cannot become redistributed contact
- **WHEN** the minimum corner is negative
- **THEN** any pressure diagram is labelled diagnostic, shows the stored signed values and does not fabricate an active area, final pressure outputs or bearing verdict

### Requirement: Bounded candidate search
The system SHALL evaluate only an engineer-confirmed finite explicit list of candidate rectangles under a recorded search policy. The proposed initial search supports averaged weights only; explicit-weight checking remains available for one fixed supplied geometry, and search rejects that mode until a separately approved size-dependent weight contract exists. Candidate inputs, parameter-source identity, methodology version, weight mode, check outcomes and refusal reasons SHALL be reproducible. Selection SHALL use the minimum passing area and first original input index for equal-area ties; a selected candidate SHALL be admissible under the complete existing ordered pressure checks and strict full-contact rule. Exhaustion SHALL return no acceptable candidate rather than an unqualified success or the last attempted size. The outcome SHALL describe selection within the submitted candidate set, never global optimality or suitability outside that set.

Source: Akim's size-selection request, 2026-11-22. Akim confirmed the explicit candidate list, averaged-mode scope, minimum-area objective, first-submitted equal-area tie policy and 256-candidate technical cap in the working conversation on 2026-11-22. These are engineering/algorithm and technical decisions, not normative constants. Bearing-check sources remain the existing SP 22.13330.2016 edition 2016 with amendments 1-5, clause 5.6.26, and full-contact engineering contract.

#### Scenario: Every admitted candidate is considered under one policy
- **WHEN** a bounded candidate request is evaluated
- **THEN** selection follows the recorded candidate-generation, objective and tie policy and each evaluated candidate has an inspectable outcome without changing its b/l orientation

#### Scenario: No passing candidate
- **WHEN** every candidate fails a check or is refused
- **THEN** no candidate is reported as acceptable and the stored outcome distinguishes failure, method refusal and search exhaustion

#### Scenario: Size-dependent weights cannot be reused silently
- **WHEN** explicit component weights are supplied for one geometry but not for other candidate geometries
- **THEN** sizing does not reuse those fixed weights for other geometries and is unavailable until an approved candidate-specific weight contract is supplied

### Requirement: Non-functional design-tool boundaries
The system SHALL keep calculation deterministic, unit-explicit and free of I/O, unsafe formula parsing and ML. Candidate count and payload size SHALL be bounded by a documented technical limit approved before implementation, with cancellation and timeout behavior specified before the API is enabled. Bounds SHALL NOT be presented as normative application limits. Runtime measurements SHALL report candidate count, measured boundary and hardware; no undefined typical-design benchmark is claimed. Changed code SHALL meet at least 95% branch coverage, relevant lint/type gates, independent correctness checks and UI/UX confirmation. Existing applicable accessibility, browser, API latency, result privacy and report requirements remain in force.

#### Scenario: Oversized search rejected before work
- **WHEN** a request exceeds its documented technical candidate or payload limit
- **THEN** it is rejected before evaluation with a structured error and no partial result is represented as a completed design

#### Scenario: Coverage cannot replace correctness
- **WHEN** tests meet coverage but independent reference admission or engineering search-policy approval is missing
- **THEN** feature GO is withheld
