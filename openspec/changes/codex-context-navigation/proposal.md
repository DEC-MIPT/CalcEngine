# Proposal

## Why

Codex sessions lack a selective route from shared instructions to the current foundation
work. Useful commands and context pointers live in the Claude entry point and local
analysis, whose snapshots can disagree with the selected branch. Reading all reports
adds context without establishing the applicable requirements or implementation status.

## What changes

- Extend `AGENTS.md` with a repository map, sourced commands, context selection and
  calculation-quality guidance while preserving the existing team gates.
- Add one local navigation index at `docs/akim/README.md`, linking to the existing
  readiness record, change artifacts, code, tests and analysis for each task family.
- Record verified discrepancies as navigation cautions; preserve historical documents.
- Keep a tracked fallback in `AGENTS.md` because `docs/akim/` is intentionally ignored.

## Non-goals

- Application code, tests, algorithms, dependencies, infrastructure or CI changes.
- Product requirements, engineering methodology, new review gates or a second backlog.
- Editing `CLAUDE.md`, `CLAUDE.local.md`, generated instructions or user-level settings.
- Installing skills, committing, merging, pushing, publishing or archiving this change
  without the existing closure conditions.

## Capabilities

### New capabilities

None.

### Modified capabilities

- `development-process`: documents selective repository context navigation within the
  existing SDD process. It does not change product or calculation requirements.

## Impact

Documentation only, no code and no branch. Shared edits stay in the `develop` working
tree. The local index remains ignored under the existing policy; it is not a document
that a fresh clone is guaranteed to contain. The shared fallback must be sufficient.
