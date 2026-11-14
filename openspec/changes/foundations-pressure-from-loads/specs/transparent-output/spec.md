## MODIFIED Requirements

### Requirement: Normative clause references
The system SHALL show, for every normative calculation step, each `NormRef` in the `norm_refs` the engine recorded
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

Engineer_formula steps SHALL instead identify the source engineer and rationale,
without a normative status badge or invented NormRef. This engineer-source display
SHALL NOT be hidden by SHOW_NORM_STATUS, which controls only normative status.

#### Scenario: Engineer source remains visible
- **WHEN** SHOW_NORM_STATUS is off and an engineer_formula step is shown
- **THEN** its EngineerRule attribution remains visible and is not presented as verified normative data

### Requirement: Trace display consumes typed steps and warnings
The system SHALL render the trace from the typed trace steps and the result envelope of
the `calculation-engine` capability, without recomputing any value, and SHALL show the
envelope's `outputs`, applicability warnings, and refusals. In the pilot's first iteration the
setting `SHOW_ROUNDING_SOURCE` is off, and the outputs are then shown without their
`rounding_source` (it stays in the envelope and in the report).

#### Scenario: Every step field rendered
- **WHEN** a user opens a completed calculation
- **THEN** each step shows its expression, its substitutions with units, its result with
  its unit, and its norm_refs or explicit engineer source, and each check step also shows its comparison, its
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
- **THEN** the UI shows the historical bound reason or typed derived quantity, value,
  limit, source and limiting_corner, without final output values

#### Scenario: Warning readable without colour
- **WHEN** a warning or a refusal is shown
- **THEN** its meaning is conveyed by text that assistive technology can read, not by
  colour alone

A derived refusal SHALL show its completed diagnostic prefix as incomplete
calculation evidence, never as final outputs or passed bearing checks. No value,
corner choice or reason SHALL be recomputed by the client.

#### Scenario: Computed corner diagnostic
- **WHEN** the loads result is refused on p_corner_min
- **THEN** the stored limiting_corner and diagnostic prefix are shown immediately, with no final output table or bearing verdict
