# Spec Delta

## Purpose
Defines the structured formula payload the normatives pipeline hands to the backend and
frontend: traceability, LaTeX, normalized symbols, and cross-references.

## ADDED Requirements

### Requirement: Formula payload
The system SHALL return a formula as a structured payload with a normative reference, LaTeX,
normalized symbols, an expression field, and cross-references, in a shape defined by config.

#### Scenario: Config-driven shape
- **WHEN** a formula payload is built
- **THEN** its fields match the `[output]` keys in `parser.toml`

### Requirement: Symbol normalization
The system SHALL normalize each notation symbol to an ASCII machine id and a canonical LaTeX
representation.

#### Scenario: Greek symbol
- **WHEN** a notation symbol is `γc1`
- **THEN** its id is `gamma_c1` and its latex is `\gamma_{c1}`

### Requirement: Traceability reference
The system SHALL attach a normative reference to each formula payload.

#### Scenario: NormRef
- **WHEN** a formula is returned
- **THEN** it carries `designation`, `clause`, and `formula` identifying its source

### Requirement: Inspectable return
The system SHALL expose the payload through a query function whose return value is the
serialized object, not console text.

#### Scenario: JSON return
- **WHEN** a query is executed in JSON mode
- **THEN** the output is the JSON serialization of the returned object
