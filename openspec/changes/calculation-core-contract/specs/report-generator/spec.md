## MODIFIED Requirements

### Requirement: GOST report structure
The system SHALL structure the report with the sections required for project
documentation: a title block with the organization stamp (основная надпись), the input
data as a table, the calculation trace with formulas, normative references, and, for each
check step, its comparison and whether it passed, the
conclusion, the result accountability block, and, when enabled, a signature block. The
signature block SHALL contain a line for the developer (Разраб.) and a line for the
person responsible for normative control (Н. контр.), each with a surname, a signature,
and a date; a line for the checker (Пров.) is optional and, when present, has the same
three fields. The signature block SHALL be controlled by one report setting whose
default is enabled.

Source: GOST R 21.101-2026 (edition unverified). Clause 4.1.7: calculations are
formatted according to the requirements for text documents. Annex E, instructions for
columns 10-13: the signatures of the developer and of the person responsible for
normative control are mandatory, and a checker line is allowed in place of a position.

#### Scenario: Default signature block
- **WHEN** a report is generated without changing the signature-block setting
- **THEN** it contains the signature block with the developer line and the normative
  control line

#### Scenario: Complete report sections
- **WHEN** a report is generated with the signature block enabled
- **THEN** it contains the title block, input-data table, calculation trace, conclusion,
  result accountability block, and signature block, in that order

#### Scenario: Check steps in the report
- **WHEN** a report is generated for a calculation with check steps
- **THEN** the trace prints, for each check step, its comparison, both values with their
  units, and whether it passed

#### Scenario: Report without the signature block
- **WHEN** a report is generated with the signature block disabled
- **THEN** it contains the same sections in the same order, without the signature block

### Requirement: Automatic normative references in report
The system SHALL automatically include normative clause references in the generated
report without manual insertion. Each reference is taken from the `norm_refs` of its
trace step and is printed with its status; a reference that is not verified is printed
as unverified.

#### Scenario: References present
- **WHEN** a report is generated
- **THEN** normative clause references appear automatically in the calculation trace,
  each with the status of the `norm_refs` of its step

## ADDED Requirements

### Requirement: Result accountability block
The system SHALL print, in every report, the fields of the result envelope defined by
the `calculation-engine` capability: `result_id`, `engine_version`, `input_hash`, the
`outputs` with their rounding rule and its source, the `norm_refs` with their status,
the `engineer_rules` with the engineer and the rationale, the `verdict` and its `verdict_reason`, every warning, and `unverified_step_count`. The block SHALL also state that the design engineer, not
the system, is responsible for the result and for its use in project documentation.

#### Scenario: Envelope fields on the report
- **WHEN** a report is generated
- **THEN** it shows `result_id`, `engine_version`, `input_hash`, the `outputs` with
  their rounding rule and its source, the `norm_refs` with their status, the `engineer_rules`, the `verdict` and
  `verdict_reason`, the warnings, and `unverified_step_count`

#### Scenario: Engineer responsibility statement
- **WHEN** a report is generated
- **THEN** it states that the design engineer is responsible for the result

#### Scenario: Warnings carried into the report
- **WHEN** the envelope carries an applicability warning
- **THEN** the report prints the warning with the input, the violated bound of the
  validated range, and that bound's source
