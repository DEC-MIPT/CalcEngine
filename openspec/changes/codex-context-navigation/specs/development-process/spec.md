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

### Requirement: Operational local context index lifecycle
The system SHALL keep a maintained local context index focused on durable navigation,
working agreements and compact summaries of unfinished features. Each feature summary
SHALL identify its feature and branch, or an explicit no-code/no-branch marker,
current stage, next action,
blockers or dependencies, and links to its OpenSpec tasks, code journal where required,
and readiness or acceptance record. The summary SHALL route to the records that own
these facts rather than duplicate their full task checklists, execution history or
approval evidence. Shared agreements SHALL retain a tracked owner in repository
instructions or `docs/decisions/`; a local index SHALL NOT become their only record.

The system SHALL retain an unfinished feature's route when work switches or pauses.
It SHALL remove a completed feature's operational card only after its assigned tasks,
required acceptance, tester GO and review are recorded, UI/UX confirmation exists where
applicable, and actual integration into develop with the required integrated checks is
confirmed. A code-free task SHALL use the existing code-free completion gates instead
of code integration or application tests. A commit, a checked task list or a feature GO
alone SHALL NOT establish the completion needed for card removal. Change-level sync,
archive and unresolved follow-up obligations SHALL remain routed while they are open,
including when another feature of the same change is already complete.

Before removing unique historical index text, the system SHALL confirm that its unique
history and evidence are preserved in existing code journals, readiness records,
decisions or OpenSpec archives, with a discoverable route to those sources. Removing an
operational card SHALL NOT delete the underlying source records or hide unresolved
obligations. Durable contracts, limitations and agreements still needed by other work
SHALL retain short links to their current owners in general navigation or the dependent
work's route. A separate index entry for every completed feature is not required.

#### Scenario: Compact unfinished feature route
- **WHEN** an agent adds or materially updates the working summary of an unfinished feature
- **THEN** the summary names the feature, branch or no-code/no-branch marker, stage, next action,
  blockers or dependencies, and applicable tasks/journal/acceptance links
- **AND** detailed checklists, execution history and approval evidence remain in their owning records

#### Scenario: Switching or pausing unfinished work
- **WHEN** the agent switches to another feature or the developer pauses unfinished work
- **THEN** the unfinished feature retains a compact route and its remaining action or blocker remains discoverable

#### Scenario: Commit or GO without integration
- **WHEN** a code feature has a commit, checked implementation tasks or tester GO but its
  actual integration into develop and required integrated checks are not confirmed
- **THEN** its operational card remains active and does not claim the feature is complete

#### Scenario: Completed code feature card removed
- **WHEN** the feature's assigned tasks, required acceptance and review, applicable UI/UX
  confirmation, actual develop integration and integrated checks are recorded
- **AND** its history and evidence are preserved in discoverable owning records
- **THEN** its completed operational card can be removed without deleting those records
- **AND** any open change-level or follow-up obligations retain a route until resolved

#### Scenario: Code-free completion follows existing gates
- **WHEN** a code-free task is considered for removal from the active index section
- **THEN** the existing no-code GO conditions, including a tracked second-developer
  acknowledgement only when the recorded active-team policy requires it, are checked
  instead of code integration, application tests or coverage
- **AND** any pending sync/archive obligation remains discoverable

#### Scenario: Another feature of the change remains unfinished
- **WHEN** one feature is complete but another feature or a closure obligation of its
  OpenSpec change remains open
- **THEN** only the completed feature's operational card is eligible for removal
- **AND** the unfinished work's route remains and the change is not described as closed

#### Scenario: Historical text or a durable dependency is still needed
- **WHEN** an agent prepares to remove index history or a completed feature card
- **THEN** unique history is first confirmed in or transferred to the existing
  owning records, and a route to preserved history remains discoverable
- **AND** contracts, limitations and agreements needed by dependent work retain short
  links to their current authoritative sources rather than the obsolete operational narrative
- **AND** unresolved obligations and underlying evidence files are preserved
