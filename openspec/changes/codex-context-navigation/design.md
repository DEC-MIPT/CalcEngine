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

## Non-goals

See `proposal.md`. No application or product behavior changes.

## Decisions

1. Keep shared rules and a fallback map in `AGENTS.md`. Preserve section numbers used
   by Claude and other documents. Codex need not load Claude entry points each session.
2. Use one local index rather than a new status system. Its current-work route points
   to CH1 readiness, `design.md` answers, `tasks.md`, verifier sheets and branch evidence.
   It also explains known stale snapshots without modifying historical reports.
3. Record commands from scripts, manifests and existing setup documentation. State
   working directories and prerequisites, especially venv activation and skipped DB tests.
   A documented command is not a claimed successful run.
4. Preserve the existing no-code closure gate. Review agents may assess this work;
   they cannot supply the other developer's acknowledgement. Leave acknowledgement
   and archive tasks open until their evidence exists.
5. Use only public repository context in shared text. The local Claude file establishes
   the working developer for this session; none of its personal preferences are copied.

## Component boundary

No calculation hot path changes, so a new C/C++ boundary is not applicable. The index
points to the existing pure `Calculator.calculate` boundary in
`backend-layered-architecture/design.md`, decision 7.

## Non-functional requirements

- Security/privacy: no credentials, private local preferences or machine-specific paths.
- Maintainability: one local navigation index; existing sources retain ownership of facts.
- Performance: no application impact; task routes limit document loading.
- Accessibility, automated application tests and branch coverage: N/A, documentation only.
- Compatibility: Claude files and OpenSpec configuration/generated instructions unchanged.

## Verification

Validate the change and all specs strictly. Check local links, paths, command provenance,
whitespace, preservation of pre-existing edits and the allowed file scope. Run available
document hooks on the edited files. Rehearse engine, API, frontend, report and spec routes
with a reader who has not inherited this session's audit. Record failures and skipped
checks; do not claim an actual new Codex session was tested.

## Risks and open items

- The local index is not distributed by Git. The shared fallback covers missing files.
- Task checkboxes and older readiness prose can lag branch work; compare direct evidence.
- Existing base-spec/domain drift and shared-config questions are routed to their owners,
  not resolved by this documentation change.
- No second-developer acknowledgement exists for this change at creation.
