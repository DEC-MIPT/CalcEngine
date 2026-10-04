# Spec Delta

## ADDED Requirements

### Requirement: Backend tooling command
The system SHALL provide a single command for the backend zone that runs lint
(`ruff`), static type checking (`mypy`), and the test suite, configured in its own
`backend/pyproject.toml`, separate from the normative pipeline's tooling and coverage
number. The test suite run SHALL gate on branch coverage once the backend zone has an
`app/` package to measure; before that, the command runs the test suite without a
coverage gate.

#### Scenario: Clean checkout
- **WHEN** the backend command runs on a clean checkout
- **THEN** it exits 0

#### Scenario: Lint, type, or test failure
- **WHEN** a lint violation, a type error, or a failing test exists in the backend zone
- **THEN** the command exits non-zero and names the failing check

#### Scenario: Coverage below threshold
- **WHEN** `backend/app/` exists and branch coverage for the backend zone is below 95%
- **THEN** the command exits non-zero, per the "Test gate with >= 95% branch coverage"
  requirement

#### Scenario: Coverage gate not yet applicable
- **WHEN** `backend/app/` does not exist yet
- **THEN** the command runs the test suite without a coverage gate, and the absence of
  a coverage number does not fail the command

### Requirement: Frontend tooling command
The system SHALL provide a single command for the frontend zone that runs `eslint`,
`tsc`, and `vitest`.

#### Scenario: Clean checkout
- **WHEN** the frontend command runs on a clean checkout
- **THEN** it exits 0

#### Scenario: Lint, type, or test failure
- **WHEN** a lint violation, a type error, or a failing test exists in the frontend zone
- **THEN** the command exits non-zero and names the failing check

### Requirement: Import contract check
The system SHALL check, as part of the backend command, that no layer imports a layer
that `backend-layered-architecture`'s dependency direction forbids it from depending
on. Before that change's layered directory structure exists, this check has nothing to
verify and does not run.

#### Scenario: Upward import
- **WHEN** a layer imports a layer it must not depend on
- **THEN** the backend command fails and names the offending import

#### Scenario: Forbidden import
- **WHEN** an `api` or `worker` module imports `repositories` or `models`, or an
  `engine` module imports anything from the application other than `schemas` and `core`
- **THEN** the backend command fails and names the offending import

#### Scenario: Layered structure not yet present
- **WHEN** the layered directory structure from `backend-layered-architecture` does not
  exist yet
- **THEN** the backend command does not run this check, and its absence does not fail
  the command

### Requirement: Pre-commit secret scan and documented configuration
The system SHALL scan staged changes for secrets before a commit is created, and SHALL
require `.env.example` to list every environment variable the backend's configuration
reads, checked automatically rather than by manual review.

#### Scenario: Secret staged
- **WHEN** a file staged for commit matches a known secret pattern
- **THEN** the commit is blocked and the match is named

#### Scenario: Config variable missing from the template
- **WHEN** a commit is staged and the backend's configuration model declares an
  environment variable that `.env.example` does not list
- **THEN** the commit is blocked and the missing variable is named; this check runs as
  a pre-commit hook, and the backend tooling command may also run it

#### Scenario: Configuration model not yet present
- **WHEN** the backend's configuration model does not exist yet
- **THEN** this check has nothing to compare against and does not block the commit
