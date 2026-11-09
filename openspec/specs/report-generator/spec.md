# Report Generator

## Purpose
Component 5: automatic generation of a GOST-compliant calculation report. For the MVP
the report is exported as `.docx`; `.pdf` is a later goal.

## Requirements

### Requirement: GOST-compliant report assembly
The system SHALL assemble a report that contains the input data, the detailed
calculation trace with formulas and references, and the final conclusion, formatted
per GOST R 21.101-2020.

#### Scenario: Generate a report
- **WHEN** a user requests a report after a calculation
- **THEN** the report includes input data, the full calculation trace, and the conclusion

### Requirement: GOST report structure
The system SHALL structure the report as a text document: every sheet has the sheet
frame and a title block (основная надпись), of form 5 on the first (title) sheet and of
form 6 on each following sheet. The body SHALL hold, in this order: the input data as a
table; the calculation trace with, for each step, its formula, its normative references
(printed inside the trace, not as a separate section), and, for each check step, its
comparison and whether it passed; the conclusion; and the result accountability block (not
printed while the setting `ACCOUNTABILITY_SECTION` is off in the pilot's first iteration, see
"Result accountability block"; the sections before it keep their numbers). The signature block SHALL be the rows of columns 10-13 of the form-5 title block: a line
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
feed) or any other character that XML 1.0 does not allow (such as U+FFFE and U+FFFF); a
request with one SHALL be rejected before any report is built.

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

#### Scenario: Text that cannot be written to the document
- **WHEN** a report request carries, in a title-block or signature text, a control
  character or a character that XML 1.0 does not allow (for example U+FFFF)
- **THEN** the request is rejected before any report is built, and no document is
  produced

#### Scenario: Complete report sections
- **WHEN** a report is generated with the signature block enabled
- **THEN** the document's first-page footer holds the title block of form 5, its other
  footer holds the title block of form 6 (checked on the document structure, not on
  rendered sheets), and the body contains the input-data table,
  calculation trace, conclusion, and, with `ACCOUNTABILITY_SECTION` on, the result accountability
  block, in that order

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

### Requirement: DOCX export for MVP
The system SHALL export the report as `.docx` for the MVP using python-docx.

#### Scenario: Export DOCX
- **WHEN** a user exports the report
- **THEN** a `.docx` file is generated and downloadable

### Requirement: PDF export (future)
The system SHALL support `.pdf` export using reportlab as a future (non-MVP) capability.

#### Scenario: Export PDF (future)
- **WHEN** the PDF feature is implemented
- **THEN** a `.pdf` report is generated and downloadable

### Requirement: Automatic normative references in report
The system SHALL automatically include normative clause references in the generated
report without manual insertion. Each reference is taken from the `norm_refs` of its
trace step and is printed with its status; a reference that is not verified is printed
as unverified. In the pilot's first iteration (while the pilot is shown only inside the team: the
two developers and the PM; `frontend-app` design.md, decision 12) the setting `TRACE_NORM_STATUS`
is off, and the references of the trace steps are then printed without their status; the
references of a violated bound in the conclusion keep it, and so do the references of the
accountability block when it is printed.

#### Scenario: References present
- **WHEN** a report is generated with `TRACE_NORM_STATUS` on
- **THEN** normative clause references appear automatically in the calculation trace,
  each with the status of the `norm_refs` of its step

#### Scenario: Step references in the pilot's first iteration
- **WHEN** a report is generated with `TRACE_NORM_STATUS` off
- **THEN** each step of the trace prints its references with document, edition and clause and
  without a status, and the bound of a refused calculation is printed with the status of its
  references

### Requirement: Non-functional — generation time
The system SHALL generate a report in under 1 minute.

#### Scenario: Fast report
- **WHEN** a report is generated for a typical calculation
- **THEN** generation completes in under 1 minute

### Requirement: Result accountability block
The system SHALL print, in every report, the fields of the result envelope defined by
the `calculation-engine` capability: `result_id`, `engine_version`, `input_hash`, the
`outputs` with their rounding rule and its source, the `norm_refs` with their status,
the `engineer_rules` with the engineer and the rationale, the `verdict` and its `verdict_reason`, every warning, and `unverified_step_count`. The block SHALL also state that the design engineer, not
the system, is responsible for the result and for its use in project documentation.
In the pilot's first iteration the setting `ACCOUNTABILITY_SECTION` is off, and the block is then
not printed: the report carries none of the fields above (warnings included; `result_id` stays in
the file name of `calculation-api` "Report download"), and the responsibility statement is printed
as the last paragraph of the conclusion instead, so that every report states it exactly once. The
report model still holds the block. Akim accepted this loss for reports read inside the team on
2026-10-18; the setting is turned back on before the pilot is shown outside the team
(`frontend-app` design.md, decision 12).

#### Scenario: Envelope fields on the report
- **WHEN** a report is generated with `ACCOUNTABILITY_SECTION` on
- **THEN** it shows `result_id`, `engine_version`, `input_hash`, the `outputs` with
  their rounding rule and its source, the `norm_refs` with their status, the `engineer_rules`, the `verdict` and
  `verdict_reason`, the warnings, and `unverified_step_count`

#### Scenario: Engineer responsibility statement
- **WHEN** a report is generated
- **THEN** it states once that the design engineer is responsible for the result: at the end of
  the block when the block is printed, and as the last paragraph of the conclusion when it is not

#### Scenario: Block not printed in the pilot's first iteration
- **WHEN** a report is generated with `ACCOUNTABILITY_SECTION` off
- **THEN** the body has the input data, the trace and the conclusion only, and the conclusion ends
  with the responsibility statement

#### Scenario: Warnings carried into the report
- **WHEN** the envelope carries an applicability warning and `ACCOUNTABILITY_SECTION` is on
- **THEN** the report prints the warning with the input, the violated bound of the
  validated range, and that bound's source

### Requirement: Report values, formulas and dates
The system SHALL print in the report each number as the shortest decimal that reads back
to the same value, in positional notation without an exponent, with a decimal comma, followed by the Russian designation of its unit
from a fixed table kept with the report (source: unverified); a dimensionless value has no
unit designation. A value of an output quantity (the result of the step whose `step_id` is that
output, a substitution of its symbol, a side of a check, the output in the conclusion and in the
accountability block) SHALL be printed rounded by that output's `rounding_rule` and with exactly
the rule's number of decimals; a check whose rounded sides would read against its `passed` is
printed with unrounded values, and the envelope stays unrounded. A formula SHALL be printed from
its LaTeX in the normative catalog, unchanged. Every value and every formula of the body (the
symbols and values of the input table, the symbol that names each trace step, the step's
expression, substitutions, result and comparison, the conclusion, and the accountability block)
SHALL be printed as a Word equation (Office Math) built from LaTeX, left-aligned; only the
expression of a step may be broken across lines by Word. A formula whose LaTeX cannot be
converted SHALL be printed as its LaTeX in plain text, and the report SHALL still be produced. A date in the title block SHALL be printed as two-digit day, month and year
separated by dots, as note 2 of Annex E of GOST R 21.101-2026 (edition unverified) gives
for dates on paper.

#### Scenario: A value with its unit
- **WHEN** a report prints the value 172.5 in the unit `kPa`
- **THEN** it prints a Word equation that reads `172,5 кПа`

#### Scenario: An output by its rounding rule
- **WHEN** the output `R` has the illustrative value 172.5 and a rule of 2 decimals, and the
  illustrative value 168.2857 in another report with the same rule
- **THEN** the reports print `172,50 кПа` and `168,29 кПа` wherever `R` is printed

#### Scenario: A small value and a dimensionless value
- **WHEN** a report prints the value 1e-07 in the unit `m` and the value 2.0 in the unit `1`
- **THEN** it prints `0,0000001 м` and `2`

#### Scenario: A date in the title block
- **WHEN** the developer line carries the date 2026-09-30
- **THEN** column 13 of that line prints `30.09.26`

#### Scenario: A formula
- **WHEN** a trace step's `expression` is a LaTeX string
- **THEN** the report prints, as the step's formula, a Word equation converted from that string
  unchanged

#### Scenario: A formula that cannot be converted
- **WHEN** a trace step's `expression` is `R = \frac{a}{`, LaTeX that has no denominator
- **THEN** the report is produced, and the step's formula is printed as that string in plain text

### Requirement: Parameter source line in the report
The report of a result whose envelope carries `parameter_source` SHALL print one line naming
the source of the norm-given parameters: for kind `interim` the words for the interim
normative data, the profile and the full data digest; for kind `catalog` the words for the
normative catalog. While the result accountability section is not printed, the line SHALL be
printed in the conclusion, immediately before the engineer-responsibility sentence; when that
section is printed, the line SHALL be printed there instead, extending the content of the
"Result accountability block" of `calculation-core-contract`, so that it appears exactly
once.
A result without `parameter_source` SHALL produce a report without the line.

#### Scenario: Interim line in the conclusion
- **WHEN** a report is built for a result computed on interim data in the `strict` profile
  while the accountability section is off
- **THEN** the conclusion holds one line with the interim data, `strict` and the 64-character
  digest, directly before the responsibility sentence

#### Scenario: Line printed once
- **WHEN** the accountability section is on
- **THEN** the line appears in that section and not in the conclusion

#### Scenario: Older result
- **WHEN** a report is built for a stored result without `parameter_source`
- **THEN** the report has no source line and is otherwise unchanged
