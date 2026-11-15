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
- Define the local index's operational lifecycle: durable navigation and working
  agreements, compact summaries of unfinished features, and removal of completed
  operational cards only after existing completion gates and evidence preservation.
- Keep contracts, limitations and unresolved obligations discoverable after a feature's
  card is removed, with detailed history owned by journals and acceptance records.

## Non-goals

- Application code, tests, algorithms, dependencies, infrastructure or CI changes.
- Product requirements, engineering methodology, new review gates or a second backlog.
- Editing `CLAUDE.md`, `CLAUDE.local.md`, generated instructions or user-level settings.
- Installing skills, committing, merging, pushing, publishing or archiving this change
  without the existing closure conditions.
- Retrospective consolidation or deletion of the current index history, deletion of
  source records, a fixed index template or a numeric line/word/size budget. This
  amendment records the maintenance policy; applying it to existing history is separate work.

## Capabilities

### New capabilities

None.

### Modified capabilities

- `development-process`: documents selective repository context navigation within the
  existing SDD process, including lifecycle rules for local operational feature cards
  and preservation of their source evidence. It does not change product or calculation requirements.

## Impact

Documentation only, no code and no branch. Documentation creation, editing,
commits and pushes occur only in a checkout of `develop`. Preserve existing work
through an authorized safe switch or a develop worktree before document authoring.
The local index remains ignored under the existing policy; it is not a document
that a fresh clone is guaranteed to contain. The shared fallback must be sufficient.
