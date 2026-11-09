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
- **THEN** the formula (MathJax), substitution, and result are shown with each normative
  reference the step rests on, for example `<NORM-DOC-PLACEHOLDER>`, edition
  `unverified`, clause `<CLAUSE-PLACEHOLDER>`, `status: unverified`

#### Scenario: Unverified reference is visible
- **WHEN** any reference of a step is marked `status: unverified`
- **THEN** the display shows that mark next to that reference

### Requirement: Expandable steps
The system SHALL allow each calculation step to be expanded and collapsed on demand.

#### Scenario: Expand a step
- **WHEN** a user clicks a calculation step
- **THEN** the step expands to show its details and collapses when clicked again

### Requirement: Normative clause references
The system SHALL show, for every calculation step, each `NormRef` in the `norm_refs` the engine recorded
for that step, together with its status as defined by the `normatives-catalog`
requirement "Norm reference status". The display SHALL NOT present an unverified
reference as verified and SHALL NOT invent or complete a reference. In the pilot's first iteration
(while the pilot is shown only inside the team: the two developers and the PM; `frontend-app`
design.md, decision 12) the setting `SHOW_NORM_STATUS` is off, and the trace SHALL then show the
references of its steps without a status mark (neither verified nor unverified) and without the
summary of unverified steps; the document, edition and clause are still shown as recorded, and the
refusal and the warnings keep the status of their sources.

#### Scenario: Verify the reference
- **WHEN** a step displays a normative reference with `SHOW_NORM_STATUS` on
- **THEN** the displayed document, edition, clause, and status are exactly those of each
  `NormRef` in the step's `norm_refs`, and a reference that is not verified is shown as unverified

#### Scenario: Status not shown in the pilot's first iteration
- **WHEN** a step displays a normative reference with `SHOW_NORM_STATUS` off
- **THEN** the displayed document, edition and clause are exactly those of the `NormRef`, and no
  status mark is shown, so an unverified reference is never shown as verified

### Requirement: Non-functional — completeness
The system SHALL render 100% of calculation steps with correct mathematical notation
in a cross-browser compatible way.

#### Scenario: Full transparency
- **WHEN** a calculation completes
- **THEN** every step is displayed with MathJax-rendered formulas across supported browsers

### Requirement: Trace display consumes typed steps and warnings
The system SHALL render the trace from the typed trace steps and the result envelope of
the `calculation-engine` capability, without recomputing any value, and SHALL show the
envelope's `outputs`, applicability warnings, and refusals. In the pilot's first iteration the
setting `SHOW_ROUNDING_SOURCE` is off, and the outputs are then shown without their
`rounding_source` (it stays in the envelope and in the report).

#### Scenario: Every step field rendered
- **WHEN** a user opens a completed calculation
- **THEN** each step shows its expression, its substitutions with units, its result with
  its unit, and its `norm_refs`, and each check step also shows its comparison, its
  right-hand value with its unit, and whether it passed, in text and not by colour alone

#### Scenario: Outputs with rounding rule shown
- **WHEN** a user opens a completed calculation with `SHOW_ROUNDING_SOURCE` on
- **THEN** each entry of the envelope's `outputs` is shown with its value, its unit, its
  `rounding_rule`, and its `rounding_source`; a rule set by the engineer is shown as
  engineer-set with the engineer and the rationale

#### Scenario: Outputs in the pilot's first iteration
- **WHEN** a user opens a completed calculation with `SHOW_ROUNDING_SOURCE` off
- **THEN** each entry of the envelope's `outputs` is shown with its value, its unit and its
  `rounding_rule`, and with no `rounding_source`

#### Scenario: Unverified steps counted
- **WHEN** the envelope's `unverified_step_count` is greater than zero and `SHOW_NORM_STATUS` is
  on
- **THEN** a summary above the trace shows `unverified_step_count`

#### Scenario: Validated-range warning shown
- **WHEN** the envelope carries an applicability warning
- **THEN** the warning is shown next to the result and names the input, the violated
  bound of the validated range, and that bound's source; a source set by the engineer is
  shown as engineer-set
  with the engineer and the rationale

#### Scenario: Refusal shown
- **WHEN** the envelope reports a refused calculation
- **THEN** the UI shows the `verdict_reason` (the violated bound, the input value, and the
  bound's `NormRef` list) and shows no result value

#### Scenario: Warning readable without colour
- **WHEN** a warning or a refusal is shown
- **THEN** its meaning is conveyed by text that assistive technology can read, not by
  colour alone
