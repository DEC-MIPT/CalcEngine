# Transparent Output

## Purpose
Component 4: a transparent ("white box") presentation of the calculation: every step,
formula in mathematical notation (MathJax), value substitution, intermediate result,
and a link to the specific normative clause.

## Requirements

### Requirement: Detailed calculation display
The system SHALL display the full calculation trace: formulas in mathematical notation,
substituted values, intermediate results, and references to normative clauses.

#### Scenario: Inspect a calculation step
- **WHEN** a user expands a calculation step
- **THEN** the formula (MathJax), substitution, and result are shown with the normative
  clause reference (for example SP 16.13330.2024, clause 8.2.2)

### Requirement: Expandable steps
The system SHALL allow each calculation step to be expanded and collapsed on demand.

#### Scenario: Expand a step
- **WHEN** a user clicks a calculation step
- **THEN** the step expands to show its details and collapses when clicked again

### Requirement: Normative clause references
The system SHALL attach a correct reference to the specific normative clause for every
calculation step.

#### Scenario: Verify the reference
- **WHEN** a step displays a normative reference
- **THEN** the reference points to an existing clause of the bound normative document

### Requirement: Non-functional — completeness
The system SHALL render 100% of calculation steps with correct mathematical notation
in a cross-browser compatible way.

#### Scenario: Full transparency
- **WHEN** a calculation completes
- **THEN** every step is displayed with MathJax-rendered formulas across supported browsers
