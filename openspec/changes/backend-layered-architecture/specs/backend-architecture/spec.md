# Spec Delta

## Purpose
Defines the layered backend architecture for DEC: the separation into ORM models,
schemas, repositories, services, API routes, parameters, calculation engine, reporting,
and core layers, plus the isolated normative document database and ML model storage.

## ADDED Requirements

### Requirement: Layered architecture
The system SHALL organize the backend into distinct layers — ORM models, schemas,
repositories, services, API routes, parameters, calculation engine, reporting, core,
and db — each with a single responsibility.

#### Scenario: Layer responsibilities
- **WHEN** a developer adds or changes backend code
- **THEN** the code is placed in exactly one layer according to its responsibility
  (ORM in models, validation DTOs in schemas, data access in repositories, business
  logic in services, HTTP in api routes, calculation logic in the engine)

### Requirement: Strict dependency direction
The system SHALL enforce a top-down dependency direction `api -> services ->
repositories -> models`, where `services` may also depend on `engine`, `parameters`,
and `reporting`, and no layer may import a layer above it.

#### Scenario: No upward dependency
- **WHEN** a backend module imports another module
- **THEN** the import target is in the same or a lower layer, never a higher one
  (for example the api layer never imports from models directly, only schemas)

### Requirement: No layer mixing
The system SHALL NOT let ORM objects cross the service boundary into the API layer,
and SHALL NOT place business logic in routes or repositories.

#### Scenario: ORM isolation
- **WHEN** an API endpoint returns data
- **THEN** it returns Pydantic schemas, never SQLAlchemy ORM objects

### Requirement: No hardcoding
The system SHALL keep configuration in the core config layer (environment variables)
and SHALL NOT hardcode values such as database URLs, coefficients, or formulas in code.

#### Scenario: Configurable values
- **WHEN** a value like a database URL, a normative coefficient, or a formula is needed
- **THEN** it is read from configuration or a parameter file, not written as a literal
  in the code

### Requirement: Parameters stored in YAML
The system SHALL store normative parameters (coefficients, formulas, limits) in
separate `.yaml` files loaded and validated by the parameters layer.

#### Scenario: Load calculation parameters
- **WHEN** the calculation engine needs coefficients or formulas for a calculation type
- **THEN** the parameters layer loads them from the corresponding `.yaml` file and
  passes them to the engine as typed arguments

### Requirement: Normative document database
The system SHALL store normative documents in a dedicated PostgreSQL database
(`dec_normatives`) separate from the transactional application database, holding
documents, revisions, clauses, formulas, and coefficients.

#### Scenario: Incrementally fill the normative base
- **WHEN** the team works with a normative document (SP/GOST/SNiP)
- **THEN** the document and its clauses, formulas, and coefficients are ingested into
  `dec_normatives` via the manual ingestion loader

### Requirement: Normative full-text search
The system SHALL provide full-text search over the normative base using PostgreSQL
full-text search with GIN and pg_trgm indexes and Russian-language support.

#### Scenario: Search a normative clause
- **WHEN** a user searches the normative base by keywords or clause number
- **THEN** matching documents and clauses are returned by relevance

### Requirement: Isolated ML model storage
The system SHALL store machine-learning model artifacts and their registry in an
isolated `ml/` zone with no import relationship to the application and no role in the
calculation path.

#### Scenario: ML has no calculation role
- **WHEN** a calculation runs
- **THEN** no ML model is consulted; calculations remain deterministic and ML-free

### Requirement: ML model registry
The system SHALL maintain a registry of ML models (name, version, task, framework,
status, artifact path, metrics) in a versioned file or table, separate from model
binaries.

#### Scenario: Track an experimental model
- **WHEN** a model is produced during R&D
- **THEN** its metadata is recorded in the registry with an `experimental` status and
  its artifact is stored in the models directory (gitignored)
