## MODIFIED Requirements

### Requirement: GOST report structure
The system SHALL structure the report as a text document: every sheet has the sheet
frame and a title block (основная надпись), of form 5 on the first (title) sheet and of
form 6 on each following sheet. The body SHALL hold, in this order: the input data as a
table; the calculation trace with, for each step, its formula, its normative references
(printed inside the trace, not as a separate section), and, for each check step, its
comparison and whether it passed; the conclusion; and the result accountability block.
The signature block SHALL be the rows of columns 10-13 of the form-5 title block: a line
for the developer (Разраб.) and a line for the person responsible for normative control
(Н. контр.), each with a surname (column 11), a signature (column 12), and a date
(column 13); a line for the checker (Пров.) is optional and, when present, has the same
three fields and takes the row under the developer line. The surnames and dates are
given with the report request; column 12 is always left empty for the signature. The
signature block SHALL be controlled by one report setting whose default is enabled. When
it is enabled, a request without the surname or the date of the developer or of the
normative control line, or with a checker without a surname or a date, SHALL be
rejected before any report is built. When it is disabled, the role captions of the form
stay, columns 11 and 13 are left empty, and surnames and dates given with the request
are not printed. The title-block and signature texts SHALL NOT contain a control
character (a character of the Unicode category Cc, which includes the tab and the line
feed); a request with one SHALL be rejected.

Source: GOST R 21.101-2026 (edition unverified). Clause 4.1.7: calculations are
formatted according to the requirements for text documents. Clause 5.2.2: the title
sheet of a text document has the title block of form 5, each following sheet the title
block of form 6. Annex E, form 5, form 6 and the instructions for columns 10-13: the
signatures of the developer and of the person responsible for normative control are
mandatory, and a checker line is allowed in place of a position. Annex Zh, figure Zh.1
a): the frame and the place of the title block on an A4 sheet. The column grid and the
frame sizes are taken from those figures; this requirement fixes none of them as a number.

#### Scenario: Default signature block
- **WHEN** a report is generated without changing the signature-block setting, with the
  surnames and dates of the developer and the normative control lines
- **THEN** the title block of the first sheet carries both lines, each with its surname
  and date

#### Scenario: Signature block enabled without a surname
- **WHEN** a report is requested with the signature block enabled and without the
  surname of the developer line
- **THEN** the request is rejected and no report is built

#### Scenario: Complete report sections
- **WHEN** a report is generated with the signature block enabled
- **THEN** the document's first-page footer holds the title block of form 5, its other
  footer holds the title block of form 6 (checked on the document structure, not on
  rendered sheets), and the body contains the input-data table,
  calculation trace, conclusion, and result accountability block, in that order

#### Scenario: Check steps in the report
- **WHEN** a report is generated for a calculation with check steps
- **THEN** the trace prints, for each check step, its comparison, both values with their
  units, and whether it passed

#### Scenario: Report of a refused calculation
- **WHEN** a report is generated for a refused calculation
- **THEN** the body keeps the same sections in the same order, the trace section states
  that the calculation was refused and holds no step, and the conclusion names the
  violated bound, the input value with its unit, and the bound's normative references

#### Scenario: Report without the signature block
- **WHEN** a report is generated with the signature block disabled, with surnames and
  dates given
- **THEN** it contains the same title blocks and body sections in the same order, the
  role captions of columns 10-13 stay, and columns 11 and 13 are empty

#### Scenario: Optional checker line
- **WHEN** a report is generated with the signature block enabled and a checker given
- **THEN** the row under the developer line carries the caption Пров. with the checker's
  surname and date, and without a checker given the caption, surname, and date cells of
  that row are empty

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

### Requirement: Report values, formulas and dates
The system SHALL print in the report each number as the shortest decimal that reads back
to the same value, in positional notation without an exponent, with a decimal comma, followed by the Russian designation of its unit
from a fixed table kept with the report (source: unverified); a dimensionless value has no
unit designation. A formula SHALL be printed as its LaTeX from the normative catalog, as
text. A date in the title block SHALL be printed as two-digit day, month and year
separated by dots, as note 2 of Annex E of GOST R 21.101-2026 (edition unverified) gives
for dates on paper.

#### Scenario: A value with its unit
- **WHEN** a report prints the value 172.5 in the unit `kPa`
- **THEN** it prints `172,5 кПа`

#### Scenario: A small value and a dimensionless value
- **WHEN** a report prints the value 1e-07 in the unit `m` and the value 2.0 in the unit `1`
- **THEN** it prints `0,0000001 м` and `2`

#### Scenario: A date in the title block
- **WHEN** the developer line carries the date 2026-09-30
- **THEN** column 13 of that line prints `30.09.26`

#### Scenario: A formula
- **WHEN** a trace step's `expression` is a LaTeX string
- **THEN** the report prints that string unchanged as the step's formula
