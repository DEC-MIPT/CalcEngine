## MODIFIED Requirements

### Requirement: Normative clause references
The system SHALL show, for every calculation step, each `NormRef` in the `norm_refs` the engine recorded
for that step, together with its status as defined by the `normatives-catalog`
requirement "Norm reference status". The display SHALL NOT present an unverified
reference as verified and SHALL NOT invent or complete a reference.

#### Scenario: Verify the reference
- **WHEN** a step displays a normative reference
- **THEN** the displayed document, edition, clause, and status are exactly those of each
  `NormRef` in the step's `norm_refs`, and a reference that is not verified is shown as unverified

## ADDED Requirements

### Requirement: Trace display consumes typed steps and warnings
The system SHALL render the trace from the typed trace steps and the result envelope of
the `calculation-engine` capability, without recomputing any value, and SHALL show the
envelope's `outputs`, applicability warnings, and refusals.

#### Scenario: Every step field rendered
- **WHEN** a user opens a completed calculation
- **THEN** each step shows its expression, its substitutions with units, its result with
  its unit, and its `norm_refs`

#### Scenario: Outputs with rounding rule shown
- **WHEN** a user opens a completed calculation
- **THEN** each entry of the envelope's `outputs` is shown with its value, its unit, its
  `rounding_rule`, and its `rounding_source`; a rule set by the engineer is shown as
  engineer-set with the engineer and the rationale

#### Scenario: Unverified steps counted
- **WHEN** the envelope's `unverified_step_count` is greater than zero
- **THEN** a summary above the trace shows `unverified_step_count`

#### Scenario: Validated-range warning shown
- **WHEN** the envelope carries an applicability warning
- **THEN** the warning is shown next to the result and names the input, the validated
  range, and the range's source; a source set by the engineer is shown as engineer-set
  with the engineer and the rationale

#### Scenario: Refusal shown
- **WHEN** the envelope reports a refused calculation
- **THEN** the UI shows the `verdict_reason` (the violated bound, the input value, and the
  bound's `NormRef` list) and shows no result value

#### Scenario: Warning readable without colour
- **WHEN** a warning or a refusal is shown
- **THEN** its meaning is conveyed by text that assistive technology can read, not by
  colour alone
