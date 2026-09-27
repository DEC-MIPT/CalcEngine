# Spec Delta

## Purpose
Defines the structured extraction of calculation-bearing entities from normative documents:
formulas, coefficient tables, clause references, notation, and applicability bounds.

## ADDED Requirements

### Requirement: Formula extraction
The system SHALL extract a formula as structured data — its LaTeX source, a parsed
expression, and the attached notation and units.

#### Scenario: Executable formula
- **WHEN** a formula is extracted from a pilot document
- **THEN** its parsed expression evaluates on a control example with the documented units

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
