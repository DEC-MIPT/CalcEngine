## MODIFIED Requirements

### Requirement: Non-overlapping developer responsibility zones
The system SHALL keep the developers' responsibility zones non-overlapping: Akim owns
frontend/backend, the calculation engine, and the report generator; Egor owns the
normative-document pipeline, NLP/RAG parsing, DevOps, and ML/DL/NLP. Specs are the only
shared artifact. The team also has a product manager (PM), a role that owns scope,
pricing, and legal questions and has no code zone.

#### Scenario: No zone overlap
- **WHEN** a task is assigned for implementation
- **THEN** it falls into exactly one developer's zone, and the orchestrator asks which
  developer (Akim or Egor) is working before implementation starts

#### Scenario: Scope, pricing, or legal decision
- **WHEN** a decision on scope, pricing, or a legal question is needed
- **THEN** its owner is the PM, and no developer records it as settled without the PM's
  approval

#### Scenario: PM has no code zone
- **WHEN** a task is assigned for implementation
- **THEN** it is not assigned to the PM, and no branch `feature/<task>/<zone>` is
  created for the PM

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

### Requirement: Review before merge
The system SHALL require that a change is reviewed before its branches are merged to
develop, in addition to the tester GO verdict. For a change with no code, the
acknowledgement required by "Go/No-Go verdict and archive" is that review.

#### Scenario: Reviewed merge
- **WHEN** a change has a GO verdict
- **THEN** it is reviewed (by the other developer or the orchestrator) and only then
  merged to develop

#### Scenario: Reviewed merge of a change with no code
- **WHEN** a change with no code has a GO verdict
- **THEN** the acknowledgement by the developer who did not author it counts as the
  review, and no further code review is required

### Requirement: Go/No-Go verdict and archive
The system SHALL archive a change only after a GO verdict and after the spec-keeper
syncs specs. For a change with code, GO requires that tests pass with >= 95% coverage,
UI/UX is confirmed where the interface changed, and validation passed. A change has no
code when it adds or edits no file outside `openspec/`, `docs/`, `agent-docs/`, the
agent tool directories `.claude/`, `.kilo/`, and `.kilocode/` (agent and skill
definitions and agent settings), and the repository documents `AGENTS.md`, `CLAUDE.md`,
`README.md`, and `.editorconfig`. For a change
with no code, GO SHALL require that `openspec validate --strict` passes, that the
`spec-reviewer` report has no blocker and no major finding, and that the developer who did not author the
change has acknowledged it in a tracked commit or comment that names the change; the
tester agent SHALL record tests, coverage, and UI/UX as not applicable, each with a
reason, in the fields `tests: N/A`, `coverage: N/A`, and `UI/UX: N/A`. This rule applies to both developers and to both agent tools (Claude Code and
Kilo Code).

#### Scenario: Archive gate
- **WHEN** a change is archived
- **THEN** a GO verdict was declared and the delta spec was synced to the main specs

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

## ADDED Requirements

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
  `agent-docs/`, `docs/decisions/`, or `docs/reports/`) or restates the reasoning in
  the text, and does not cite an untracked external document

#### Scenario: Untracked citation found
- **WHEN** the `spec-reviewer` finds a citation of an untracked external document as the
  rationale of a decision
- **THEN** it reports a finding and the citation is replaced with a tracked source

#### Scenario: Norm citation
- **WHEN** a spec cites a norm document as the basis of a formula, coefficient, or limit
- **THEN** this requirement does not apply and the norm-source rules of
  `agent-docs/domain-constraints.md` do
