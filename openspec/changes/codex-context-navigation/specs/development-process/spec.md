## ADDED Requirements

### Requirement: Selective repository context navigation
The system SHALL provide shared repository instructions that route agents to the selected
task's OpenSpec artifacts, relevant decisions, implementation and checks. A local working
index MAY provide further routes, while existing specifications and records retain
ownership of requirements, task status and approvals.

#### Scenario: Task context selected
- **WHEN** an agent starts an engine, API, frontend, report or specification task
- **THEN** `AGENTS.md` identifies the applicable areas, check commands and OpenSpec entry
  points, with further task-specific routes in `docs/akim/README.md` when present
- **AND** reading the full analysis/report archive is not required

#### Scenario: Local working documents absent
- **WHEN** `docs/akim/` is absent from a checkout
- **THEN** shared instructions still route to `openspec/changes/`, `openspec/specs/`,
  `docs/decisions/`, existing source/test directories and configured checks

#### Scenario: Report or checklist differs from the branch
- **WHEN** a report's implementation claim or completed task differs from the selected
  branch's files or merge state
- **THEN** the agent identifies the discrepancy and distinguishes implemented behavior,
  requirements and plans before relying on that claim
- **AND** the navigation index does not replace OpenSpec tasks or approval records

### Requirement: Context documentation scope and verification
The system SHALL preserve existing team gates, Claude entry points, generated instruction
blocks and user changes during context-navigation maintenance. Shared context SHALL
exclude secrets, private preferences and machine-specific paths. Documentation checks
SHALL cover links, command provenance, scope and preservation; application performance,
UI accessibility tests and branch coverage are N/A for this no-code change.

#### Scenario: Documentation checked without application edits
- **WHEN** repository context instructions are updated
- **THEN** relative links and named paths resolve, commands trace to existing scripts,
  configuration or setup docs, and actual checks are distinguished from documented commands
- **AND** changes stay within instructions and documentation, with no changes to Claude
  entry points, application files or generated instruction blocks

#### Scenario: Working state changes
- **WHEN** the status of the selected task materially changes
- **THEN** its existing working-state record or journal and affected navigation pointers
  are updated rather than creating a separate report for each action
- **AND** shared decisions remain in `docs/decisions/` and requirements/tasks in OpenSpec
