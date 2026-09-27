## MODIFIED Requirements

### Requirement: Detailed calculation display
The system SHALL display the full calculation trace: formulas in mathematical notation,
substituted values, intermediate results, and references to normative clauses.

#### Scenario: Inspect a calculation step
- **WHEN** a user expands a calculation step
- **THEN** the formula (MathJax), substitution, and result are shown with each normative
  reference the step rests on, for example `<NORM-DOC-PLACEHOLDER>`, edition
  `unverified`, clause `<CLAUSE-PLACEHOLDER>`, `source: unverified`

#### Scenario: Unverified reference is visible
- **WHEN** any reference of a step is marked `source: unverified`
- **THEN** the display shows that mark next to that reference
