# Development Process

## Purpose
Defines the Spec-Driven Development (SDD) process enforced in this repository: every
task is captured as an OpenSpec change, planned with a DOR, implemented (documents directly
on develop, code on feature branches), tested with >= 95% branch coverage, and archived
only after a GO verdict.

## Requirements

### Requirement: Every task is an OpenSpec change
The system SHALL require that every task be recorded as an OpenSpec change proposal
with proposal, specs delta, design, and tasks artifacts, validated with
`openspec validate`.

#### Scenario: Task capture
- **WHEN** a new task is started
- **THEN** an OpenSpec change proposal exists and validates before implementation begins

### Requirement: Planning before implementation
The system SHALL require a plan produced by the business-analyst agent, including the
DOR, before implementation starts. The DOR SHALL require a `spec-reviewer` report
without blockers, because `openspec validate` checks structure only and does not check
content. "Without blockers" means the report lists no finding of severity blocker or
major.

#### Scenario: Plan gate
- **WHEN** a change is ready for implementation
- **THEN** the plan and DOR checklist are present in the artifacts

#### Scenario: Change declared ready
- **WHEN** a change is declared ready (DOR met)
- **THEN** a `spec-reviewer` report with no blocker and no major finding exists for the
  current version of the change, in addition to a passing `openspec validate`

#### Scenario: Validation passes but review has blockers
- **WHEN** `openspec validate` passes and the `spec-reviewer` report lists a blocker or
  a major finding
- **THEN** the change is not ready

### Requirement: Functional and non-functional requirements recorded
The system SHALL record functional requirements as OpenSpec requirements/scenarios and
record non-functional requirements (performance, security, accessibility, coverage)
explicitly.

#### Scenario: Complete requirements
- **WHEN** a change is proposed
- **THEN** both functional and non-functional requirements are recorded

### Requirement: Branch-per-feature with zone sub-branches
The system SHALL implement each feature on its own branch from develop (or from the branch
of an unmerged feature it depends on), and one feature
has exactly one branch, `feature/<feature>/<zone>` (a fix uses `fix/<feature>/<zone>`).
The zones are `backend` and `frontend` (Akim), and `data`, `ml`, and `infra` (Egor); work
in two zones is two features with two names. A feature is a component or a stage of the
plan that the `tasks.md` of the one OpenSpec change it belongs to names, together with its
branch and the tasks assigned to it; every task with code SHALL belong to exactly one
feature, and one change may hold several features. A feature that needs code from a
feature not yet merged SHALL branch from that feature's branch and be merged into develop
only after it.

A feature branch SHALL be pushed to the remote with the commit that finishes a subtask of
it, and SHALL be merged into develop only when the whole feature is done, in this order:
every task assigned to the feature is checked off, the tester declares GO for the feature,
the review of "Review before merge" passes, and then the branch is merged. A fix branch
follows the same gates, and its fix is done when its tests pass.

#### Scenario: Isolated implementation
- **WHEN** a feature is implemented
- **THEN** the code is on its dedicated feature/fix branch from develop, never on develop
  or main directly

#### Scenario: Finished feature may be merged
- **WHEN** every task assigned to a feature is checked off, the tester has declared GO
  for it, and the review has passed
- **THEN** the developer who owns the feature branch may merge it into develop

#### Scenario: Unfinished feature is not merged
- **WHEN** a feature has a task that is not checked off, or has no GO verdict, or has not
  passed review
- **THEN** its branch is not merged into develop, not even per section or per subtask

#### Scenario: Branch visible while in progress
- **WHEN** a commit finishes a subtask of a feature
- **THEN** the branch is pushed with it, so that the head of the remote branch contains
  that commit

#### Scenario: Features named in tasks.md
- **WHEN** a change is proposed
- **THEN** its `tasks.md` names each feature, its branch, and the tasks assigned to it
  (every task with code assigned to exactly one feature), or states that the change has
  no code and no branch

#### Scenario: Dependent feature
- **WHEN** a feature needs code from a feature that is not merged yet
- **THEN** its branch is created from that feature's branch, and it is merged into develop
  only after that feature

### Requirement: Documents commit directly to develop
The system SHALL let a developer commit documents directly to develop, with no
sub-branch and no merge commit. A document is a file on the "no code" list of
"Go/No-Go verdict and archive". Any other file (source code, tests, a package manifest,
`.gitignore`, agent settings, pre-commit configuration, `docker-compose.yml`) SHALL reach
develop only through a feature branch of the change that needs it, with one exception:
when a commit shifts or removes lines whose findings the secrets baseline already allows,
and the pre-commit secret scan only rewrites their line numbers or drops their entries,
the rewritten baseline SHALL be committed together with that commit, on the branch where
that commit is made, develop included. Such a refresh adds no finding: its diff changes
only `line_number` values, removes entries, or updates the generation timestamp. A
baseline change that adds a finding or alters an entry's hash is not covered by this
exception.

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

#### Scenario: Allowed line removed by a document commit
- **WHEN** a document commit on develop removes a line that the secrets baseline allows,
  and the pre-commit secret scan drops that entry from the baseline and stops the commit
- **THEN** the developer stages the rewritten baseline and commits it together with the
  document on develop, with no feature branch

#### Scenario: New finding during a document commit
- **WHEN** the pre-commit secret scan reports a finding that the baseline does not
  allow, on any branch
- **THEN** the baseline is not changed in that commit: the finding is removed from the
  file or marked as a placeholder in it, or the baseline is regenerated and every finding
  reviewed by hand on a feature or fix branch

### Requirement: Non-overlapping developer responsibility zones
The system SHALL keep the developers' responsibility zones non-overlapping: Akim owns
frontend/backend, the calculation engine, and the report generator; Egor owns the
normative-document pipeline, NLP/RAG parsing, DevOps, and ML/DL/NLP. Specs are the only
shared artifact. The team also has a product manager (PM), a role that owns scope,
pricing, and legal questions and has no code zone. A PM decision is recorded by a
developer as a dated entry in a tracked file under `docs/decisions/`.

#### Scenario: No zone overlap
- **WHEN** a task is assigned for implementation
- **THEN** it falls into exactly one developer's zone, and the orchestrator asks which
  developer (Akim or Egor) is working before implementation starts

#### Scenario: Scope, pricing, or legal decision
- **WHEN** a decision on scope, pricing, or a legal question is needed
- **THEN** its owner is the PM, and no developer records it as settled without the PM's
  approval

#### Scenario: PM approval recorded
- **WHEN** a developer records a PM decision
- **THEN** the record is a dated entry in a tracked file under `docs/decisions/` that
  names the decision, restates the PM's words, and says where they were given (a meeting
  or a message); the PM does not need to commit

#### Scenario: PM has no code zone
- **WHEN** a task is assigned for implementation
- **THEN** it is not assigned to the PM, and no branch `feature/<feature>/<zone>` is
  created for the PM

### Requirement: Specs complement and code does not overlap
The system SHALL require that specs extended by developers complement each other rather
than contradict, and that code does not overlap across zones so git branches merge
without conflicts.

#### Scenario: Conflict-free merge
- **WHEN** branches from different zones are merged
- **THEN** their code does not overlap, and their spec changes do not contradict

### Requirement: Skill availability check
The system SHALL check at the start of every iteration that the required skills are
present; a warning SHALL be shown when a skill is missing, and any newly installed
skill SHALL be recorded in the specs with the installing developer.

#### Scenario: Missing skill
- **WHEN** a required skill is missing at the start of an iteration
- **THEN** a warning is shown with the exact install command

#### Scenario: New skill installed
- **WHEN** a developer installs a new skill
- **THEN** the installation is recorded in the specs (an OpenSpec change) naming the
  developer and the skill

### Requirement: Test gate with >= 95% branch coverage
The system SHALL require the tester agent to write and run automated tests reaching at
least 95% branch coverage before a GO verdict is declared.

#### Scenario: Coverage gate
- **WHEN** a feature is implemented
- **THEN** automated tests pass with >= 95% branch coverage measured on its feature branch,
  otherwise the verdict is NO-GO

### Requirement: UI/UX verification
The system SHALL require the ui-ux-tester agent to verify visuals and control/button
behavior when UI changes.

#### Scenario: UI check gate
- **WHEN** a change modifies the user interface
- **THEN** the ui-ux-tester confirms visuals and button behavior before GO

### Requirement: Review before merge
The system SHALL require that a feature branch is reviewed before it is merged to
develop, in addition to the tester GO verdict. A document committed directly to develop is
not merged, so it has no branch review. For a change with no code, the review is the
acknowledgement required by "Go/No-Go verdict and archive", given in a tracked commit or
comment after the document commit; until it is given, the change has no GO and is not
archived. The documents of a change with code are reviewed together with its feature
branches, and a document that belongs to no change (a decision record, `CLAUDE.md`, a
mirrored agent file) needs no acknowledgement.

#### Scenario: Reviewed merge
- **WHEN** a feature has a GO verdict from the tester
- **THEN** it is reviewed (by the other developer or the orchestrator) and only then its
  branch is merged to develop

#### Scenario: Review of a change with no code
- **WHEN** the documents of a change with no code are on develop
- **THEN** the acknowledgement by the developer who did not author it counts as the
  review, no code review is required, and the change is not archived before it

### Requirement: Go/No-Go verdict and archive
The system SHALL archive a change only after a GO verdict and after the spec-keeper
syncs specs. For a change with code, the tester declares GO per feature, and the change is
archived only when every one of its features is merged into develop with its GO and
review. GO for a feature requires that tests pass with >= 95% coverage,
UI/UX is confirmed where the interface changed, and validation passed. A change has no
code when it adds or edits no file outside `openspec/`, `docs/`, `agent-docs/`, the
agent and skill definitions under `.claude/`, `.kilo/`, and `.kilocode/`, and the
repository documents `AGENTS.md`, `CLAUDE.md`, `README.md`, and `.editorconfig`. Agent
settings (for example `.claude/settings.json`) are not on this list. A refresh of
`.secrets.baseline` that adds no finding, committed with a document under the exception
of "Documents commit directly to develop", does not make a change a change with code.
For a change with no code, GO SHALL require that `openspec validate --strict` passes, that the
`spec-reviewer` report has no blocker and no major finding, and that the developer who did not author the
change has acknowledged it in a tracked commit or comment that names the change; the
tester agent SHALL record tests, coverage, and UI/UX as not applicable, each with a
reason, in the fields `tests: N/A`, `coverage: N/A`, and `UI/UX: N/A`. This rule applies to both developers and to both agent tools (Claude Code and
Kilo Code).

#### Scenario: Archive gate
- **WHEN** a change is archived
- **THEN** a GO verdict was declared and the delta spec was synced to the main specs

#### Scenario: Archive of a change with several features
- **WHEN** a change with code holds several features and one of them is not merged
- **THEN** the change is not archived

#### Scenario: Change with no code
- **WHEN** a change has no code
- **THEN** the code-free GO path applies instead of the test-coverage and UI/UX gates,
  and GO is declared once validation, the `spec-reviewer` report, and the second
  developer's acknowledgement are all present

#### Scenario: Tester records not applicable
- **WHEN** the tester issues a verdict for a change with no code
- **THEN** the verdict states `tests: N/A`, `coverage: N/A`, and `UI/UX: N/A`, each with
  the reason that the change has no code, and a verdict without that record is NO-GO

#### Scenario: Missing acknowledgement
- **WHEN** a change with no code lacks the acknowledgement of the developer who did not
  author it, or a `spec-reviewer` blocker or major finding is open, or validation fails
- **THEN** the verdict is NO-GO

#### Scenario: Change touches code
- **WHEN** a change adds or edits any file outside the paths listed above
- **THEN** the code-free path does not apply and the tests and coverage gate is required

#### Scenario: Document change with a line-only baseline refresh
- **WHEN** a change with no other file outside the listed paths commits a refresh of
  `.secrets.baseline` that adds no finding, under the exception of "Documents commit
  directly to develop"
- **THEN** the change still has no code, and the code-free GO path applies

### Requirement: Shared decisions are tracked
The system SHALL require that the rationale for a decision, given in a spec, a
`proposal.md`, or a `design.md`, cites only sources tracked by git, so that every
reviewer can open it. An external document that git does not track, such as the project
passport or an untracked research file, SHALL NOT be cited as the source of a rationale.
This requirement does not apply to citations of norm documents (SP, GOST, SNiP), which
follow `agent-docs/domain-constraints.md`: a norm is cited from its primary source
text, which the repository does not track.

#### Scenario: Rationale in a design
- **WHEN** a `design.md` or a `proposal.md` gives a rationale for a decision
- **THEN** the rationale cites a tracked file (for example under `openspec/`,
  `agent-docs/`, or `docs/decisions/`) or restates the reasoning in the text, and does
  not cite an untracked external document

#### Scenario: Untracked citation found
- **WHEN** the `spec-reviewer` finds a citation of an untracked external document as the
  rationale of a decision
- **THEN** it reports a finding and the citation is replaced with a tracked source

#### Scenario: Norm citation
- **WHEN** a spec cites a norm document as the basis of a formula, coefficient, or limit
- **THEN** this requirement does not apply and the norm-source rules of
  `agent-docs/domain-constraints.md` do

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
on, and that every top-level package and module of the backend application belongs to
a layer of that order, except the application's entry module (`main`), which composes
the layers and sits above them. Before that change's layered directory structure exists,
this check has nothing to verify and does not run.

#### Scenario: Upward import
- **WHEN** a layer imports a layer it must not depend on
- **THEN** the backend command fails and names the offending import

#### Scenario: Forbidden import
- **WHEN** an `api` or `worker` module imports `repositories` or `models`, or an
  `engine` module imports anything from the application other than `schemas` and `core`
- **THEN** the backend command fails and names the offending import

#### Scenario: Package outside every layer
- **WHEN** a new top-level package or module, other than the entry module, is added to
  the backend application and no layer of the dependency order names it
- **THEN** the backend command fails and names the package or module

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
the scan cannot tell from secrets. The configuration check SHALL read each variable name
the way the configuration library resolves it, SHALL refuse to guess a name it cannot
read, and SHALL treat class-level configuration (the settings model's own configuration
attribute, class variables and attributes whose name starts with an underscore) as not
being a variable.

#### Scenario: Secret staged
- **WHEN** a file staged for commit matches a known secret pattern
- **THEN** the commit is blocked and the match is named

#### Scenario: Research notebook staged
- **WHEN** a notebook under `ml/research/` is staged for commit
- **THEN** the secret scan does not scan it and does not block the commit because of it

#### Scenario: Placeholder marked in its file
- **WHEN** a staged line holds a placeholder credential and the scanner's allowlist
  marker sits either on that line itself or, as `pragma: allowlist nextline secret`, on
  the line just before it
- **THEN** the commit is not blocked by that line, and the baseline does not list it

#### Scenario: Config variable missing from the template
- **WHEN** a commit is staged and the backend's configuration model declares an
  environment variable that `.env.example` does not list
- **THEN** the commit is blocked and the missing variable is named; this check runs as
  a pre-commit hook, and the backend tooling command may also run it

#### Scenario: Name changed by the configuration
- **WHEN** a commit is staged and the backend's configuration model changes a variable
  name through its configuration (a prefix, an alias generator, a choice of aliases,
  case sensitivity, a parent settings class)
- **THEN** every name the configuration library reads for that field, each choice of a
  choice of aliases included, must be listed in `.env.example`: the commit is blocked
  and each missing name is named, and it passes when all are listed

#### Scenario: Variable name that cannot be read
- **WHEN** a commit is staged and a settings class sets its variable names in code the
  check does not evaluate (a custom choice of settings sources, a custom constructor),
  the configuration library cannot resolve the names of a field, or the settings module
  cannot be loaded
- **THEN** the commit is blocked with an exit status different from that of a missing
  variable, and the message names the class, the class and the field, or the module and
  the error type

#### Scenario: Settings configuration attribute
- **WHEN** a settings class declares its configuration attribute, a class variable with
  a type annotation, or an attribute whose name starts with an underscore
- **THEN** the check does not treat it as an environment variable

#### Scenario: Both aliases given
- **WHEN** a field of the configuration model gives both a validation alias and a plain
  alias
- **THEN** the check uses the name or names of the validation alias, as the
  configuration library does, whatever the plain alias is

#### Scenario: Configuration model not yet present
- **WHEN** the backend's configuration model does not exist yet
- **THEN** this check has nothing to compare against and does not block the commit

### Requirement: Correctness gate for calculation changes

The system SHALL require, for a change that contains code that adds or modifies a
calculation, that the
tester agent verifies correctness in addition to the coverage gate: the reference suite
of `calculation-verification` passes within tolerance, the invariant tests pass, and the
metrics "deviation from the references", "reproducibility rate", and "traceability
completeness" are attached to the GO verdict, and the regression corpus of
`calculation-verification` shows no undeclared difference. The traceability completeness
has no threshold. The requirement "Test gate with >= 95% branch coverage" is unchanged
and still applies.

#### Scenario: Calculation change passes the correctness gate
- **WHEN** a change modifies a calculation and the reference suite is within tolerance,
  the invariant tests pass, and the metrics are attached
- **THEN** the correctness gate is satisfied, and GO still needs the coverage gate

#### Scenario: Change without calculation code
- **WHEN** a change contains no code that adds or modifies a calculation
- **THEN** the correctness gate does not apply

#### Scenario: Reference suite fails
- **WHEN** a change modifies a calculation and any reference output is outside its
  tolerance
- **THEN** the verdict is NO-GO even if branch coverage is at least 95%
