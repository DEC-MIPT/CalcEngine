# Development Process

## Purpose
Defines the Spec-Driven Development (SDD) process enforced in this repository: every
task is captured as an OpenSpec change, planned with a DOR, implemented on dedicated
branches, tested with >= 95% branch coverage, and archived only after a GO verdict.

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
DOR, before implementation starts.

#### Scenario: Plan gate
- **WHEN** a change is ready for implementation
- **THEN** the plan and DOR checklist are present in the artifacts

### Requirement: Functional and non-functional requirements recorded
The system SHALL record functional requirements as OpenSpec requirements/scenarios and
record non-functional requirements (performance, security, accessibility, coverage)
explicitly.

#### Scenario: Complete requirements
- **WHEN** a change is proposed
- **THEN** both functional and non-functional requirements are recorded

### Requirement: Branch-per-task with zone sub-branches
The system SHALL implement each task on its own branch and zone sub-branch from
develop, mapped to developer responsibility zones: `feature/<task>/backend` and
`feature/<task>/frontend` (Akim), `feature/<task>/data`, `feature/<task>/ml`, and
`feature/<task>/infra` (Egor), or `fix/<task>/<zone>`.

#### Scenario: Isolated implementation
- **WHEN** a task is implemented
- **THEN** the work is on its dedicated feature/fix branch and zone sub-branch from
  develop, never on develop or main directly

### Requirement: Non-overlapping developer responsibility zones
The system SHALL keep the two developers' responsibility zones non-overlapping: Akim
owns frontend/backend, the calculation engine, and the report generator; Egor owns the
normative-document pipeline, NLP/RAG parsing, DevOps, and ML/DL/NLP. Specs are the only
shared artifact.

#### Scenario: No zone overlap
- **WHEN** a task is assigned for implementation
- **THEN** it falls into exactly one developer's zone, and the orchestrator asks which
  developer (Akim or Egor) is working before implementation starts

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
- **WHEN** a change is implemented
- **THEN** automated tests pass with >= 95% branch coverage, otherwise the verdict is NO-GO

### Requirement: UI/UX verification
The system SHALL require the ui-ux-tester agent to verify visuals and control/button
behavior when UI changes.

#### Scenario: UI check gate
- **WHEN** a change modifies the user interface
- **THEN** the ui-ux-tester confirms visuals and button behavior before GO

### Requirement: Review before merge
The system SHALL require that a change is reviewed before its branches are merged to
develop, in addition to the tester GO verdict.

#### Scenario: Reviewed merge
- **WHEN** a change has a GO verdict
- **THEN** it is reviewed (by the other developer or the orchestrator) and only then
  merged to develop

### Requirement: Go/No-Go verdict and archive
The system SHALL archive a change only after a GO verdict (tests pass with >= 95%
coverage, UI/UX confirmed, validation passed) and after the spec-keeper syncs specs.

#### Scenario: Archive gate
- **WHEN** a change is archived
- **THEN** a GO verdict was declared and the delta spec was synced to the main specs
