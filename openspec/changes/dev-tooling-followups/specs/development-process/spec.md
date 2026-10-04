## MODIFIED Requirements

### Requirement: Documents commit directly to develop
The system SHALL let a developer commit documents directly to develop, with no
sub-branch and no merge commit. A document is a file on the "no code" list of
"Go/No-Go verdict and archive". Any other file (source code, tests, a package manifest,
`.gitignore`, agent settings, pre-commit configuration, `docker-compose.yml`) SHALL reach
develop only through a feature branch of the change that needs it, with one exception:
when a commit shifts the lines of findings that the secrets baseline already allows, and
the pre-commit secret scan rewrites only their line numbers, the rewritten baseline SHALL
be committed together with that commit, on the branch where that commit is made,
develop included. A baseline change that adds, removes or alters a finding is not covered
by this exception.

#### Scenario: Document change
- **WHEN** a change adds or edits only files on the "no code" list
- **THEN** it is committed directly to develop after `git fetch --all` and
  `git pull --ff-only` have completed without error, no branch is created for it, and no
  merge commit is created for it

#### Scenario: Diverged develop
- **WHEN** `git pull --ff-only` refuses because local develop and origin/develop have
  diverged, before a commit or a push
- **THEN** the developer does not commit or push, and resolves the divergence first

#### Scenario: Non-document file
- **WHEN** a change adds or edits a file that is not on the "no code" list
- **THEN** the file is changed on a feature branch and reaches develop only when that
  feature is done

#### Scenario: Change with documents and code
- **WHEN** one change has both documents and code
- **THEN** the documents, including the checked-off boxes of its `tasks.md`, are committed
  to develop as each subtask is done, so a checked box on develop is not evidence that the
  code is on develop; the code stays on its feature branch until the feature is done, and
  the feature branch takes new documents with `git merge develop`

#### Scenario: Baseline line numbers shifted by a document commit
- **WHEN** a document commit on develop shifts a line that the secrets baseline allows,
  and the pre-commit secret scan rewrites only the line numbers in the baseline and
  stops the commit
- **THEN** the developer stages the rewritten baseline and commits it together with the
  document on develop, with no feature branch

#### Scenario: New finding during a document commit
- **WHEN** the pre-commit secret scan reports a finding that the baseline does not
  allow, on any branch
- **THEN** the baseline is not changed in that commit: the finding is removed from the
  file or marked as a placeholder in it, or the baseline is regenerated and every finding
  reviewed by hand on a feature or fix branch

### Requirement: Backend tooling command
The system SHALL provide a single command for the backend zone that runs lint
(`ruff`), static type checking (`mypy`), and the test suite, configured in its own
`backend/pyproject.toml`, separate from the normative pipeline's tooling and coverage
number. The test suite run SHALL gate on branch coverage once the backend zone has an
`app/` package to measure; before that, the command runs the test suite without a
coverage gate. The coverage gate SHALL measure the backend's own tooling scripts
together with `app/`.

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

#### Scenario: Tooling script below threshold
- **WHEN** `backend/app/` exists and branch coverage of `app/` and the backend's tooling
  scripts together is below 95%, while `app/` alone is above it
- **THEN** the command exits non-zero

#### Scenario: Coverage gate not yet applicable
- **WHEN** `backend/app/` does not exist yet
- **THEN** the command runs the test suite without a coverage gate, and the absence of
  a coverage number does not fail the command

### Requirement: Import contract check
The system SHALL check, as part of the backend command, that no layer imports a layer
that `backend-layered-architecture`'s dependency direction forbids it from depending
on, and that every top-level package of the backend application belongs to a layer of
that order. Before that change's layered directory structure exists, this check has
nothing to verify and does not run.

#### Scenario: Upward import
- **WHEN** a layer imports a layer it must not depend on
- **THEN** the backend command fails and names the offending import

#### Scenario: Forbidden import
- **WHEN** an `api` or `worker` module imports `repositories` or `models`, or an
  `engine` module imports anything from the application other than `schemas` and `core`
- **THEN** the backend command fails and names the offending import

#### Scenario: Package outside every layer
- **WHEN** a new top-level package is added to the backend application and no layer of
  the dependency order names it
- **THEN** the backend command fails and names the package

#### Scenario: Layered structure not yet present
- **WHEN** the layered directory structure from `backend-layered-architecture` does not
  exist yet
- **THEN** the backend command does not run this check, and its absence does not fail
  the command

### Requirement: Pre-commit secret scan and documented configuration
The system SHALL scan staged changes for secrets before a commit is created, and SHALL
require `.env.example` to list every environment variable the backend's configuration
reads, checked automatically rather than by manual review. The secret scan SHALL skip
the research notebooks under `ml/research/`, whose executed outputs (images, numbers)
the scan cannot tell from secrets; credentials SHALL NOT be written into those notebooks.
The configuration check SHALL read each variable name the way the configuration library
resolves it, and SHALL refuse to guess a name it cannot read.

#### Scenario: Secret staged
- **WHEN** a file staged for commit matches a known secret pattern
- **THEN** the commit is blocked and the match is named

#### Scenario: Research notebook staged
- **WHEN** a notebook under `ml/research/` is staged for commit
- **THEN** the secret scan does not scan it and does not block the commit because of it

#### Scenario: Placeholder marked in its file
- **WHEN** a staged line holds a placeholder credential and carries the scanner's inline
  allowlist marker
- **THEN** the commit is not blocked by that line, and the baseline does not list it

#### Scenario: Config variable missing from the template
- **WHEN** a commit is staged and the backend's configuration model declares an
  environment variable that `.env.example` does not list
- **THEN** the commit is blocked and the missing variable is named; this check runs as
  a pre-commit hook, and the backend tooling command may also run it

#### Scenario: Variable name that cannot be read
- **WHEN** a commit is staged and a field of the backend's configuration model takes its
  environment variable name from something the check cannot read without running the
  code (a computed alias, a choice of aliases, a prefix, an inherited settings class)
- **THEN** the commit is blocked, and the message names the class and the field

#### Scenario: Both aliases given
- **WHEN** a field of the configuration model gives both a validation alias and a plain
  alias
- **THEN** the check uses the validation alias as the variable name

#### Scenario: Configuration model not yet present
- **WHEN** the backend's configuration model does not exist yet
- **THEN** this check has nothing to compare against and does not block the commit
