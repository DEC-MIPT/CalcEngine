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
The system SHALL structure the report with the sections required for project
documentation: a title block with the organization stamp (основная надпись), the input
data as a table, the calculation trace with formulas and normative references, the
conclusion, and optional developer/checker signature fields.

#### Scenario: Complete report sections
- **WHEN** a report is generated
- **THEN** it contains the title block, input-data table, calculation trace, conclusion,
  and signature fields, in that order

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
report without manual insertion.

#### Scenario: References present
- **WHEN** a report is generated
- **THEN** normative clause references appear automatically in the calculation trace

### Requirement: Non-functional — generation time
The system SHALL generate a report in under 1 minute.

#### Scenario: Fast report
- **WHEN** a report is generated for a typical calculation
- **THEN** generation completes in under 1 minute
