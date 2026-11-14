## MODIFIED Requirements

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
- **THEN** the body keeps the same sections in the same order, an input-bound refusal keeps its historical empty trace and bound reason; a
  derived refusal prints only its completed diagnostic prefix and stored quantity,
  value, limit, source and limiting_corner, with no final outputs or conclusion
  that bearing checks passed or failed

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

#### Scenario: Loads report attribution
- **WHEN** a DOCX is generated for the loads type
- **THEN** it distinguishes d, h and d_1, explains x=b and y=l and load signs, labels engineer_formula steps, prints completed bearing checks in order and retains the existing source profile/digest line
