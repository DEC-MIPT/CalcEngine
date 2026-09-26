## MODIFIED Requirements

### Requirement: Detailed calculation display
The system SHALL display the full calculation trace: formulas in mathematical notation,
substituted values, intermediate results, and references to normative clauses.

#### Scenario: Inspect a calculation step
- **WHEN** a user expands a calculation step
- **THEN** the formula (MathJax), substitution, and result are shown with the normative
  clause reference, for example `<NORM-DOC-PLACEHOLDER>`, edition `unverified`, clause
  `<CLAUSE-PLACEHOLDER>`, `source: unverified`

#### Scenario: Unverified reference is visible
- **WHEN** a step carries a reference marked `source: unverified`
- **THEN** the display shows that mark next to the reference
