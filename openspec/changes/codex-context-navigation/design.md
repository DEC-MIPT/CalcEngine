# Design

## Context

`AGENTS.md` owns shared process rules and is imported by `CLAUDE.md`. The latter also
contains dated status and commands. `docs/akim/` holds ignored working material;
`docs/decisions/` and `docs/verification/` are tracked. OpenSpec owns requirements and
change tasks. This work keeps those ownership boundaries.

## Goals

- Let a reader find the selected task's requirements, code, tests and state without
  loading the full archive.
- Separate the MVP target from implemented capabilities and feature-branch work.
- Preserve Claude compatibility, existing user edits and all managed instruction blocks.
- Keep the local index operational: stable navigation and agreements, with concise
  pointers for work that still needs action.

## Non-goals

See `proposal.md`. No application or product behavior changes.
The lifecycle-policy amendment does not consolidate or delete the existing index's
historical entries. It introduces no numeric line, word or byte limit and no fixed
document template. Historical consolidation is a separate scoped action.

## Decisions

1. Keep shared rules and a fallback map in `AGENTS.md`. Preserve section numbers used
   by Claude and other documents. Codex need not load Claude entry points each session.
2. Use one local index rather than a new status system. Its current-work route points
   to the selected task's readiness, design answers, `tasks.md`, relevant journals,
   verifier sheets and branch evidence. Historical snapshots are labelled as such;
   their original reports remain unchanged.
3. Record commands from scripts, manifests and existing setup documentation. State
   working directories and prerequisites, especially venv activation and skipped DB tests.
   A documented command is not a claimed successful run.
4. Apply the recorded active-team no-code gate. Akim is the sole active developer;
   the second-human acknowledgement requirement is waived under the dated roster
   decision. Independent review, tester assessment and archive conditions remain;
   no human acknowledgement or unrelated task completion is invented.
5. Use only public repository context in shared text. The local Claude file establishes
   the working developer for this session; none of its personal preferences are copied.
6. Put the shared index lifecycle rule in `AGENTS.md`, record its observable behavior
   in the development-process delta, and keep a short linked reminder near the start
   of `docs/akim/README.md`. The local index cannot be the only home of the shared rule.

## Local index lifecycle

The index has three kinds of content: durable navigation, working agreements and
concise unfinished-work cards. Task checklists belong to OpenSpec; execution history,
test outputs and review details belong to existing journals and readiness records.
The index links to those owners rather than maintaining another backlog or action log.
Shared agreements keep their tracked decision or instruction source; closing one
feature does not remove an agreement that remains applicable elsewhere.

A work card identifies the feature or owning change, its branch (or explicit
no-code/no-branch status), current stage, next action, blockers and dependencies,
and links to its tasks, journal and readiness evidence where applicable. State is
an evidence-backed navigation snapshot, not an independent completion declaration.
Switching to another task or pausing work keeps the unfinished work discoverable
through a compact card or pointer; the active task can have the fuller card.

For a code feature, a commit, passing tests or feature GO alone is insufficient to
clear its operational card. Its assigned work and required acceptance/review must
be complete, including UI/UX confirmation where applicable, actual integration
into `develop` and the integrated checks required by its owning plan. For code-free
work, use validation, review and tester N/A gates, plus human acknowledgement only
when the recorded active-team policy requires it;
do not introduce a fictional code branch or merge requirement.

Feature completion and change closure are distinct. If a feature is complete while
its multi-feature change still has integration, dependency-confirmation, spec-sync
or archive obligations, those obligations retain a compact pointer to the owning
change. Open follow-ups retain their own task or change owner before a completed
feature's card is removed. This policy does not waive any existing DOD or closure gate.

Before removing unique historical text from the index, preserve it in the appropriate
existing journal, readiness record or historical material, keeping its provenance
and historical status. Removing an operational card never deletes underlying
journals, decisions, reports, verification evidence or archived specifications.
Keep short canonical links to contracts and limitations used by dependent work;
they belong to durable navigation or the dependent task, not a completed-feature log.
An individual link for every completed feature is unnecessary when the ordinary
journal and archive routes still make its evidence discoverable.

This amendment records the policy and its maintenance checks only. Existing dated
index entries remain preserved and do not count as a completed consolidation.
The alternatives of an append-only event log and deleting all material on feature
GO are rejected: the former duplicates evidence and retains conflicting snapshots,
while the latter loses pending integration work and dependency context.

## Component boundary

No calculation hot path changes, so a new C/C++ boundary is not applicable. The index
points to the existing pure `Calculator.calculate` boundary in
`backend-layered-architecture/design.md`, decision 7.

## Non-functional requirements

- Security/privacy: no credentials, private local preferences or machine-specific paths.
- Maintainability: one local navigation index, no duplicated task checklist or event
  log; existing sources retain ownership of facts. Compactness is content-based,
  without a new numeric size budget or mandatory layout.
- Performance: no application impact; task routes limit document loading.
- Accessibility, automated application tests and branch coverage: N/A, documentation only.
- Compatibility: Claude files and OpenSpec configuration/generated instructions unchanged.

## Verification

Validate the change and all specs strictly. Check local links, paths, command provenance,
whitespace, preservation of pre-existing edits and the allowed file scope. Run available
document hooks on the edited files. Rehearse engine, API, frontend, report and spec routes
with a reader who has not inherited this session's audit. Record failures and skipped
checks; do not claim an actual new Codex session was tested.

For the lifecycle amendment, compare the shared rule, delta scenarios and local
reminder for the same completion gates and evidence ownership. Exercise document
cases for an unfinished or paused feature, GO without integration, completed feature
with remaining change obligations, and a completed feature supplying a durable
contract to another task. Verify that unique-history preservation precedes removal
and that original historical index content is unchanged by this policy-only edit.
Record current strict validation, link/whitespace checks and independent review.
Application tests, coverage and UI/UX remain N/A for this documentation-only scope.

## Risks and open items

- The local index is not distributed by Git. The shared fallback covers missing files.
- Task checkboxes and older readiness prose can lag branch work; compare direct evidence.
- Existing base-spec/domain drift and shared-config questions are routed to their owners,
  not resolved by this documentation change.
- At creation, second-developer acknowledgement was pending. Under the current
  sole-developer decision it is no longer a blocker; other checks and archive
  obligations still need their own evidence.
- A completed feature may still support unfinished dependent work. Its durable
  contract links and the owning change's remaining obligations must stay discoverable.
- The existing index includes historical entries. Policy codification does not
  imply that those entries have already been consolidated or reviewed for removal.
