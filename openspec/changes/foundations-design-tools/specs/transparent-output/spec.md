## ADDED Requirements

### Requirement: Inspectable design-tool visual evidence
The system SHALL display the selected load mode, every added weight and moment contribution, total vertical force, stored pressure envelope and candidate-selection provenance without recomputing physical quantities in the client. Original expressions, substitutions, results and normative or engineer sources SHALL remain accessible in initially expanded steps. Schematic labels SHALL use the adopted pressure-variation axis convention rather than silently adopting a competitor's physical moment labels. All diagram values and pressure signs SHALL have equivalent readable text with units.

#### Scenario: Visual and numeric evidence agree
- **WHEN** a user inspects a load schematic or pressure diagram
- **THEN** each numeric label agrees with its stored input or trace quantity, including negative diagnostic values and the total's complete weight composition

#### Scenario: Search decision is inspectable
- **WHEN** a candidate is selected
- **THEN** the trace shows the policy, selected dimensions and deciding checks and provides the reasons that other retained candidates failed or were refused

#### Scenario: No source promotion through a diagram
- **WHEN** a diagram uses an engineer-defined assembly or interpolation for display
- **THEN** it is not labelled as a verified normative formula or as a newly verified source
