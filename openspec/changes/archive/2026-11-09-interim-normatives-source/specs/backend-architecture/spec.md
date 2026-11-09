# Spec Delta

## MODIFIED Requirements

### Requirement: No hardcoding
The system SHALL keep configuration in the core config layer (environment variables)
and SHALL NOT hardcode a database URL, a normative coefficient, or a formula in code.

#### Scenario: Configurable values
- **WHEN** a database URL is needed
- **THEN** it is read from configuration, not written as a literal in the code
- **WHEN** a normative coefficient or formula is needed
- **THEN** it is not written as a literal in code; storage in `.yaml` is forbidden
  outside the temporary exception in `interim-normatives` "Scoped exception to the
  normative-database rule", and its source is otherwise the normative database

### Requirement: Engineer-set parameters stored in YAML
The system SHALL store engineer-set values that the norm does not fix (rounding rules,
validated ranges) in separate `.yaml` files, one per calculation type, loaded and
validated by the parameters layer against typed schemas. Each such value SHALL carry the
engineer who set it and the rationale. Formulas and coefficients a norm gives SHALL NOT
be stored in engineer-set parameter files. Separate interim normative data files are
allowed only by `interim-normatives` "Scoped exception to the normative-database rule";
they SHALL NOT enter the engineer-set parameter loader.

#### Scenario: Load engineer-set parameters
- **WHEN** the calculation engine needs engineer-set parameters for a calculation type
- **THEN** the parameters layer loads them from that type's `.yaml` file, validates
  them, and returns them as typed values defined in `schemas`

#### Scenario: Reject a formula or coefficient in YAML
- **WHEN** a parameter `.yaml` file contains a key that the engineer-set schema does not
  define, such as a formula or a coefficient
- **THEN** validation fails with a `DECError` subclass and no values are returned

#### Scenario: Reject a value without an engineer or rationale
- **WHEN** an engineer-set value lacks the engineer or the rationale
- **THEN** validation fails with a `DECError` subclass and no values are returned
