# Spec Delta

## Purpose
Defines the layered backend architecture for DEC: the separation into ORM models,
schemas, repositories, services, API routes, parameters, calculation engine, reporting,
core, db, and worker layers, the dependency direction between them, and the minimal
runnable backend (health endpoint, configuration, errors, calculator registry). The
normative document database and the ML model storage are specified by later changes.

## ADDED Requirements

### Requirement: Layered architecture
The system SHALL organize the backend into distinct layers — ORM models, schemas,
repositories, services, API routes, parameters, calculation engine, reporting, core,
db, and worker — each with a single responsibility: ORM in models, validation DTOs and
shared typed values in schemas, data access in repositories, business logic in
services, HTTP in api routes, background jobs in worker, calculation logic in the
engine.

#### Scenario: Layers exist
- **WHEN** the backend is scaffolded
- **THEN** each of the eleven layers exists as a package under `backend/app`

### Requirement: Strict dependency direction
The system SHALL enforce one total order of layers, top to bottom: `api` and `worker`;
`services`; `engine`, `parameters`, and `reporting`; `repositories`; `db`; `models` and
`schemas`; `core`. A module SHALL import only from a layer strictly below its own layer
or from its own package; layers named together on one line SHALL NOT import each other.
Standard-library and third-party imports are outside this rule. In addition, `api` and
`worker` SHALL NOT import `repositories` or `models`, `engine` SHALL import from the
application only `schemas` and `core`, no backend module SHALL import from `ml/`, and
`ml/` SHALL import nothing from `backend/`.

#### Scenario: No upward dependency
- **WHEN** a backend module imports another module of the application
- **THEN** the import target is in a strictly lower layer or in the module's own
  package, never in the same line of layers or a higher one (for example `services`
  never imports `api`, and `models` never imports `repositories`)

#### Scenario: API reaches data only through services
- **WHEN** an api or worker module needs data
- **THEN** it calls `services` and uses `schemas`, and does not import `repositories`
  or `models`, directly

#### Scenario: Engine stays free of I/O layers
- **WHEN** an `engine` module is checked for imports
- **THEN** it imports nothing from `repositories`, `db`, `models`, `parameters`, or
  `reporting`, and receives resolved parameters as typed arguments

#### Scenario: ML stays outside the backend
- **WHEN** `ml/` exists and any module is checked for imports
- **THEN** no backend module imports from `ml/`, and `ml/` imports nothing from
  `backend/`

### Requirement: No layer mixing
The system SHALL NOT let ORM objects cross the service boundary into the API layer,
and SHALL NOT place business logic in routes or repositories.

#### Scenario: ORM isolation
- **WHEN** an API endpoint returns data
- **THEN** it returns Pydantic schemas, never SQLAlchemy ORM objects

### Requirement: No hardcoding
The system SHALL keep configuration in the core config layer (environment variables)
and SHALL NOT hardcode a database URL, a normative coefficient, or a formula in code.

#### Scenario: Configurable values
- **WHEN** a database URL is needed
- **THEN** it is read from configuration, not written as a literal in the code
- **WHEN** a normative coefficient or formula is needed
- **THEN** it is neither written as a literal in the code nor stored in a `.yaml` file;
  its source is the normative database, read through a path a later change adds

### Requirement: Engineer-set parameters stored in YAML
The system SHALL store engineer-set values that the norm does not fix (rounding rules,
validated ranges) in separate `.yaml` files, one per calculation type, loaded and
validated by the parameters layer against typed schemas. Each such value SHALL carry the
engineer who set it and the rationale. Formulas and coefficients a norm gives SHALL NOT
be stored in `.yaml`.

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

### Requirement: Health endpoint
The system SHALL expose `GET /health` that returns HTTP 200 with the JSON body
`{"status": "ok"}` and touches no database.

#### Scenario: Health check
- **WHEN** a client sends `GET /health`
- **THEN** the response is `200` with body `{"status": "ok"}`

### Requirement: Fail-fast configuration
The system SHALL read the application database URL from `DEC_APP_DATABASE_URL`, and the
normative database URL from `DEC_NORMATIVES_DATABASE_URL`, from environment variables
only. Construction of the settings SHALL fail when `DEC_APP_DATABASE_URL` is unset, with
no silent default. `DEC_NORMATIVES_DATABASE_URL` is optional until a later change reads
the normative database, and is read when set.

#### Scenario: Settings read from the environment
- **WHEN** `DEC_APP_DATABASE_URL` is set, with or without
  `DEC_NORMATIVES_DATABASE_URL`, and `Settings` is instantiated
- **THEN** it exposes the values that are set as read

#### Scenario: Missing application URL
- **WHEN** `DEC_APP_DATABASE_URL` is unset and `Settings` is instantiated
- **THEN** instantiation raises a validation error that names the environment variable
  `DEC_APP_DATABASE_URL`

### Requirement: Secret values stay out of output
The system SHALL NOT write a database URL or its credential to logs or to the printed
form of the settings.

#### Scenario: Settings printed
- **WHEN** `repr` or `str` of a `Settings` instance is taken, or the settings are logged
- **THEN** the output does not contain the credential part of any database URL

### Requirement: Common error hierarchy
The system SHALL define a base exception `DECError` in the core layer, and every
backend-defined exception SHALL derive from it, so callers can catch backend errors by
one type. Exceptions raised by third-party libraries, such as the validation error
raised by pydantic-settings, are outside this rule.

#### Scenario: Backend error type
- **WHEN** backend code raises one of its own exceptions
- **THEN** the exception is an instance of `DECError`

### Requirement: Calculator registry
The system SHALL define, in the calculation engine, a `Calculator` interface and a
registry in which a calculator is registered and looked up by calculation-type name. A
calculator SHALL take typed inputs and resolved parameters and return a result, as a
pure function. The interface SHALL be generic over the input, parameter, and result
types, so the engine does not import them.

#### Scenario: Register and look up a calculator
- **WHEN** a calculator is registered under a calculation-type name
- **THEN** looking up that name returns it, and looking up an unregistered name fails
  with a `DECError`

### Requirement: Transactional application database
The system SHALL provide a SQLAlchemy engine and session factory for the transactional
application database `dec_app`, configured from `DEC_APP_DATABASE_URL`, and an Alembic
migration tree for it, separate from any normative database migrations.

#### Scenario: Session connects and migrations run
- **WHEN** a `dec_app` database is reachable at `DEC_APP_DATABASE_URL`
- **THEN** the session factory connects to it, and `alembic upgrade head` completes
  without error on a fresh database and records the initial revision in the database
  named by `DEC_APP_DATABASE_URL`

### Requirement: Backend coverage gate
The system SHALL fail the backend check when branch coverage of `backend/app` is below
95%.

#### Scenario: Coverage below the gate
- **WHEN** `backend/check.sh` runs on `backend/app` with branch coverage below 95%
- **THEN** it exits non-zero and reports the coverage
