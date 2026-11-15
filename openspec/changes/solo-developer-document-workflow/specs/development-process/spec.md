## MODIFIED Requirements

### Requirement: Branch-per-feature with zone sub-branches
The system SHALL implement each feature on its own branch from develop (or from the branch
of an unmerged feature it depends on), and one feature
has exactly one branch, `feature/<feature>/<zone>` (a fix uses `fix/<feature>/<zone>`).
The technical zone suffixes remain `backend`, `frontend`, `data`, `ml` and `infra`;
ownership follows the current recorded roster and task assignment. Work in two zones
is two features with two names. A feature is a component or a stage of the
plan that the `tasks.md` of the one OpenSpec change it belongs to names, together with its
branch and the tasks assigned to it; every task with code SHALL belong to exactly one
feature, and one change may hold several features. A feature that needs code from a
feature not yet merged SHALL branch from that feature's branch and be merged into develop
only after it.

A feature branch SHALL be pushed to the remote, after explicit consent, with the commit
that finishes a subtask of it, and SHALL be merged into develop only when the whole feature is done, in this order:
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
The system SHALL require all document creation, editing, commits and pushes to take
place only on develop, with no documentation sub-branch or merge commit. Before any
document edit, the agent SHALL check the actual branch and working state. A linked
worktree qualifies only when it is checked out on develop. A different branch SHALL
stop document authoring until an authorized safe switch to develop succeeds. Existing
user work, including ignored files, SHALL be preserved; force checkout, reset or stash
SHALL NOT be used to obtain an editable state. A refused switch SHALL be reported
and resolved without overwriting content. Reading feature documents or importing
already committed develop documents through a separately authorized merge is not
new document authoring. Git consent remains separate from edit authorization. A document is a file on the "no code" list of
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
- **THEN** its files are created and edited only in a develop worktree, and any
  separately authorized commit or push occurs on develop after `git fetch --all` and
  `git pull --ff-only` have completed without error, with no documentation branch or
  merge commit

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
- **THEN** document authoring, including edits to its tasks.md, occurs only on develop,
  and separately authorized document commits go to develop as work is completed
- **AND** a checked box on develop is not evidence that code is on develop; code stays
  on its feature branch until accepted integration and imports committed documents
  only through a separately authorized git merge develop

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

#### Scenario: Document authoring requested on a feature branch
- **WHEN** an agent is about to edit a document while its worktree is on a feature branch
- **THEN** it checks branch and working state and performs no document edit there
- **AND** only an authorized safe switch to develop or an authorized develop worktree
  permits the edit, preserving all existing work

#### Scenario: Branch switch refused with local documents
- **WHEN** Git refuses a switch to develop because local tracked or untracked files collide
- **THEN** the agent preserves their contents and reports the refusal before choosing a
  reversible resolution supported by verified file contents and existing authorization
- **AND** it does not force checkout, reset, stash or silently discard work

#### Scenario: Import committed documents without authoring on the feature
- **WHEN** a feature branch needs documents already committed on develop
- **THEN** reading those documents or a separately authorized merge can supply them
- **AND** any further document edits still occur only on develop

### Requirement: Non-overlapping developer responsibility zones
The system SHALL preserve non-overlapping responsibility assignment according to
the current recorded developer roster. Akim is the sole active developer and working
contact for current task coordination across technical areas; Egor is a former
contributor and has no active assignment or required confirmation role. Existing
component boundaries and technical branch suffixes remain unchanged. New work SHALL
remain explicitly scoped rather than being approved merely by this roster change.
The team also has a product manager (PM), who retains scope, pricing and legal
authority and has no code zone. PM decisions SHALL still be recorded by a developer
as dated entries in tracked files under docs/decisions/.

#### Scenario: No zone overlap
- **WHEN** a task is assigned for implementation
- **THEN** its technical area and current owner are recorded without overlapping
  developer assignments
- **AND** in the current single-developer mode the working developer is Akim; the agent
  does not ask whether Egor is working or wait for his confirmation

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

### Requirement: Review before merge
The system SHALL require a feature-branch review before integration into develop,
in addition to tester GO. The orchestrator can provide that review while Akim is
the sole active developer. A directly committed document has no branch merge.
For a change with no code, current spec-reviewer findings and the tester's documented
checks and verdict remain required. A second-human-developer acknowledgement SHALL
NOT be required in the current single-developer mode. If a later recorded roster
and policy require such an acknowledgement, it must be an actual tracked response
from the applicable reviewer; no absent developer's signature may be invented.
Documents of a code change remain reviewed with their features. Independent agent
review, engineering-source checks and explicit Git consent are not waived.

#### Scenario: Reviewed merge
- **WHEN** a feature has a GO verdict from the tester
- **THEN** it receives the required independent review, by the orchestrator in the
  current single-developer mode, and only a separately authorized integration follows

#### Scenario: Review of a change with no code
- **WHEN** the documents of a change with no code are on develop
- **THEN** current spec-reviewer and tester document checks are required, and no
  second-human-developer acknowledgement is required in the current single-developer mode
- **AND** any human acknowledgement required by a later recorded roster/policy must
  actually exist before it is counted; the other closure gates remain applicable

### Requirement: Go/No-Go verdict and archive
The system SHALL archive a change only after a GO verdict and after the spec-keeper
syncs specs. For a change with code, the tester declares GO per feature, and the change is
archived only when every one of its features is merged into develop with its GO and
review. GO for a feature requires that tests pass with >= 95% coverage,
UI/UX is confirmed where the interface changed, and validation passed. A change has no
code when it adds or edits no file outside `openspec/`, `docs/`, `agent-docs/`, the
instruction-only agent and skill definitions under `.claude/`, `.codex/`, `.kilo/`,
and `.kilocode/`, and the
repository documents `AGENTS.md`, `CLAUDE.md`, `README.md`, and `.editorconfig`. Agent
settings (for example `.claude/settings.json`) are not on this list. A refresh of
`.secrets.baseline` that adds no finding, committed with a document under the exception
of "Documents commit directly to develop", does not make a change a change with code.
For a change with no code, GO SHALL require strict OpenSpec validation, a current
spec-reviewer report with no blocker or major finding, and completed document checks
recorded by the tester. In the current single-developer mode no second-human
acknowledgement is required. A human acknowledgement is required only where the
recorded active roster and applicable policy require it. The tester SHALL record
tests: N/A, coverage: N/A, and UI/UX: N/A, each with its no-code reason. This applies
across supported agent tools. The no-code classification includes the existing
OpenSpec instruction configuration under openspec/; runtime or permission settings
are not documents merely because of their extension. Application code still requires
passing tests and at least 95% branch coverage, applicable UI/UX and engineering
correctness evidence. Independent agent checks, security findings, spec synchronization
and explicit Git-consent gates remain intact.

#### Scenario: Archive gate
- **WHEN** a change is archived
- **THEN** a GO verdict was declared and the delta spec was synced to the main specs

#### Scenario: Archive of a change with several features
- **WHEN** a change with code holds several features and one of them is not merged
- **THEN** the change is not archived

#### Scenario: Change with no code
- **WHEN** a change has no code
- **THEN** the code-free path applies with strict validation, clean current spec
  review, completed document checks and tester N/A records
- **AND** no second-human-developer acknowledgement is required while the recorded
  single-developer mode applies

#### Scenario: Tester records not applicable
- **WHEN** the tester issues a verdict for a change with no code
- **THEN** the verdict states `tests: N/A`, `coverage: N/A`, and `UI/UX: N/A`, each with
  the reason that the change has no code, and a verdict without that record is NO-GO

#### Scenario: Missing acknowledgement
- **WHEN** a change with no code lacks a human acknowledgement that is actually
  required by the current recorded roster and policy, or a spec-reviewer blocker or
  major finding is open, or validation or required document checks fail
- **THEN** the verdict is NO-GO

#### Scenario: Change touches code
- **WHEN** a change adds or edits any file outside the paths listed above
- **THEN** the code-free path does not apply and the tests and coverage gate is required

#### Scenario: Document change with a line-only baseline refresh
- **WHEN** a change with no other file outside the listed paths commits a refresh of
  `.secrets.baseline` that adds no finding, under the exception of "Documents commit
  directly to develop"
- **THEN** the change still has no code, and the code-free GO path applies

#### Scenario: Permission settings are not instruction-only mirrors
- **WHEN** a change edits agent permission settings, runtime configuration or application files
- **THEN** those edits follow the code path even if nearby instruction-only agent
  definitions or skill files follow the document path

#### Scenario: Old human-confirmation task in single-developer mode
- **WHEN** an active task still requests Egor's or a second developer's acknowledgement
  solely as the old human-confirmation gate
- **THEN** its current applicability is recorded as not applicable under the single-developer policy
- **AND** no approval or signature is fabricated and all unrelated technical work,
  independent checks and archive obligations remain visible

## ADDED Requirements

### Requirement: Current developer roster and historical evidence
The system SHALL record Akim as the sole active developer, Egor as a former contributor
and the absence of a replacement second developer. The source is Akim's explicit
instruction recorded on 2026-11-15 in the dated workflow decision. This is the record
date, not an invented departure date. Until Akim announces a replacement, agents SHALL
use the single-developer rules without requesting or simulating second-developer
confirmations. On such an announcement the roster, assignments and applicable
confirmation policy SHALL be updated before the new reviewer is assumed available.
Historical decisions, archive contents, code authorship and normative verification
provenance SHALL remain unchanged. Roster changes SHALL NOT settle unresolved
methodology, source verification or product decisions.

#### Scenario: No second developer available
- **WHEN** an agent selects a working developer or evaluates a human-confirmation gate
- **THEN** it uses Akim as the current working contact and does not block solely on
  Egor's or an unspecified replacement's acknowledgement
- **AND** independent agents still provide the reviews and verdicts required by the task

#### Scenario: New second developer announced
- **WHEN** Akim explicitly announces a new second developer
- **THEN** the roster, technical assignments and applicable confirmation rules are recorded
  before the new developer is treated as an available reviewer
- **AND** no replacement is inferred from an old branch, author name or example

#### Scenario: Earlier approval remains historical
- **WHEN** current instructions or active task applicability are reconciled with the new roster
- **THEN** earlier decisions, signatures and authorship remain historical evidence
- **AND** an obsolete human-confirmation request is recorded as waived or not applicable,
  not as an approval that the former developer supplied

### Requirement: Documentation governance verification
The system SHALL verify this document-only governance maintenance with strict OpenSpec
validation, current independent spec review, branch/scope and preservation checks,
relative-link and whitespace checks, and available document hooks. It SHALL preserve
pre-existing work, keep shared text free of secrets and machine-specific private data,
and make no runtime permission or application change under this document scope.
Application performance, branch coverage and UI accessibility tests are not applicable
to a change with no application or interface code; the tester SHALL state each N/A
reason rather than claim an application test pass.

#### Scenario: Document-only policy accepted
- **WHEN** the tester assesses this document-only policy change
- **THEN** actual document checks, independent review and each tests/coverage/UI/UX
  N/A reason are recorded without an invented second-human confirmation
- **AND** any remaining validation, security, review or archive failure keeps its
  normal blocking effect

#### Scenario: Existing work preserved during governance updates
- **WHEN** instructions, active confirmation records or mirrors are updated on develop
- **THEN** unrelated user changes, historical evidence, generated blocks, permission
  settings and application behavior remain unchanged
