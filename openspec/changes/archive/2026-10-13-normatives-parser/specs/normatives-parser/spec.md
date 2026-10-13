# Spec Delta

## Purpose
Defines the structured extraction of calculation-bearing entities from normative documents:
formulas, coefficient tables, clause references, notation, and applicability bounds.

## ADDED Requirements

### Requirement: Formula extraction
The system SHALL extract a formula as structured data — its LaTeX source, a parsed
expression, and the attached notation and units.

#### Scenario: Executable formula
- **GIVEN** a formula extracted from a pilot document and a set of documented-unit values
- **WHEN** the parsed expression is lambdified and evaluated on those values
- **THEN** the result matches the documented reference value without raising an exception
  (exec_rate = executions without exception / total extracted formulas from the pilot ≥ 90%;
  measured on pilot СП 22.13330.2016; pilot formula 5.7 executes to 143.75 kPa)

#### Scenario: Source selected by PDF type
- **WHEN** a document is ingested
- **THEN** the parser chooses the formula-LaTeX source by the PDF type (text layer vs scan),
  with one shared entry point and one output contract

### Requirement: Text-layer formula reconstruction
The system SHALL reconstruct formula LaTeX deterministically from the PDF text layer for
text-based documents, without OCR or neural models.

#### Scenario: Deterministic LaTeX
- **WHEN** a text-based PDF is parsed
- **THEN** each numbered formula gets LaTeX assembled from character geometry (size/baseline),
  NFKC and the Adobe Symbol table, with Cyrillic kept as-is

### Requirement: Coefficient table extraction
The system SHALL extract a coefficient table with its structure, values, units, and
applicability conditions.

#### Scenario: Table with units
- **WHEN** a coefficient table is parsed
- **THEN** its cells carry values and units, and its applicability condition is recorded

### Requirement: Clause reference extraction
The system SHALL extract numbered clauses into locatable references.

#### Scenario: Locatable clause
- **WHEN** a numbered clause is parsed
- **THEN** it is stored with a locator (e.g. `cl. 6.2`) usable as a `NormRef.clause`

### Requirement: Notation extraction
The system SHALL extract the notation of a document (symbol → meaning and unit).

#### Scenario: Symbol with unit
- **WHEN** a notation entry is parsed
- **THEN** the symbol is stored with its meaning and base unit

### Requirement: Applicability bounds
The system SHALL extract applicability bounds with their normative references.

#### Scenario: Validated range
- **WHEN** a method or validated range is parsed
- **THEN** it is stored with a `NormRef` and usable for an applicability check

#### Scenario: Condition phrase
- **WHEN** a line states a condition using a phrase enumerated in the `condition`
  extractor config (`extract_conditions` in `parser/extractors.py`,
  e.g. «при условии что», «при соблюдении», «соблюдены следующие условия»)
- **THEN** it is extracted as a condition linked to its preceding clause
