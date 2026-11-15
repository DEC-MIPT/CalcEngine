# Proposal

## Why

The document workflow must require edits on develop, not only direct document commits.
Akim has also confirmed that Egor has left and no replacement second developer exists,
so current work must not wait for an unavailable person's confirmation.

## What changes

- Require all document creation, editing, commits and pushes to occur on develop,
  with branch/status checks before editing and safe preservation when switching.
- Record Akim as the only active developer and Egor as a former contributor. A new
  second developer is recognized only after Akim explicitly announces the change.
- Waive second-human-developer confirmations in the current single-developer mode,
  while retaining independent agent review, tester verdicts and all applicable
  code-quality, engineering-correctness and Git-consent gates.
- Reconcile current instructions, role/skill mirrors, OpenSpec context and affected
  active confirmation tasks without rewriting historical approvals or signatures.
- Identify instruction-only Codex agent/skill mirrors as documents consistently
  with the existing Claude and Kilo mirrors. Permission settings remain code.

## Capabilities

### New capabilities

None.

### Modified capabilities

- `development-process`: documentation editing on develop, current developer roster,
  responsibility assignment, review and conditional human-confirmation gates.

## Impact

Documentation only, no code and no feature branch. Preparation and editing happen
on develop. Scope includes AGENTS.md, current project entry points, instruction-only
agent/skill mirrors, OpenSpec planning context, the dated team/workflow decision and
this change. Active records may mark a second-developer request as not applicable
under the current policy; they must not claim that Egor approved it.

The existing technical area names and feature-branch format remain in use. Akim
coordinates current development; the PM retains scope, pricing and legal authority.
This policy does not authorize a commit, merge, push, archive or new product work.

## Non-goals

- Application code, runtime settings, dependencies, database changes, infrastructure
  behavior, numerical methods or normative-source status changes.
- Removing independent review, test, coverage, UI/UX, security or engineering
  correctness gates, or substituting a human confirmation for an agent verdict.
- Inventing a replacement developer, departure date, human signature or approval.
- Rewriting archived changes, prior decisions or former contributors' provenance.
- Automatically closing active changes, approving unresolved technical decisions,
  integrating the module-contract code or restructuring the local context history.
