# Proposal

## Why

The process documents describe a two-developer team, and the process cannot close a
change that has no code. Four findings of the project audit drive this change. The audit
reports are not tracked by git, so each finding is restated here in full:

- **D8**: `AGENTS.md` section 5 and `openspec/config.yaml:31-33` model two developers
  with no PM role, while the team is three people: Akim, Egor, and a PM. The DOD also
  defines GO only through passing tests and coverage, so a documentation-only change
  has no verdict path.
- **E5**: `record-installed-skills-akim` is stuck on exactly that gap. Its `tasks.md`
  task 1.5 waits for a colleague's acknowledgement and task 1.7 expects a `tester`
  verdict "no code, no tests, coverage not applicable", which no spec defines.
- **A13**: `openspec validate --strict` is structural. It passed all items while
  per-artifact rules were violated, so a green validation can be read as readiness.
  The DOR must also require a `spec-reviewer` report.
- **D2**: rationale in `backend-layered-architecture` cites "the passport", an external
  document git does not track, so a reviewer cannot open it. The first half of D2, the
  untracked `docs/`, is already fixed: `.gitignore` tracks `docs/decisions/**` and
  `docs/reports/**` (commit `d62999d`). This change does not repeat that fix; it adds
  the rule that specs cite only tracked sources and lists the remaining citations.

## What Changes

- Modifies `development-process`: the PM is a team role that owns scope, pricing, and
  legal questions and has no code zone.
- Modifies `development-process`: a change with no code reaches GO through validation,
  a `spec-reviewer` report with no blocker and no major finding, and acknowledgement by the developer who
  is not its author. The `tester` records tests as not applicable, with a reason.
- Modifies `development-process`: the DOR requires a `spec-reviewer` report with no
  blocker and no major finding and states that `openspec validate` checks structure only. No spec or
  change defines the DOR today; only `AGENTS.md` section 3 does.
- Adds to `development-process`: specs and `design.md` cite only git-tracked sources.
- The rules apply equally to Akim and Egor and to their agent tools, Claude Code and
  Kilo Code.

## Non-goals

- Editing `AGENTS.md`, `openspec/config.yaml`, or `CLAUDE.md` (see "Follow-up changes
  to shared files").
- Creating a PM agent or skill. Whether the PM needs one is left open.
- Rewriting the "passport" citations in `backend-layered-architecture`; they belong to
  that change and are only listed in `tasks.md`.
- Reprioritising meta-changes (the other half of E5).
- Making the `.gitignore` change for `docs/` again.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `development-process`: modifies "Non-overlapping developer responsibility zones",
  "Planning before implementation", "Review before merge", and "Go/No-Go verdict and
  archive"; adds "Shared decisions are tracked".

## Impact

- Affects `openspec/specs/development-process/spec.md` after archive. No code.
- Unblocks part of `record-installed-skills-akim`; see `design.md` for what it does and
  does not close.
- After archive, `AGENTS.md` and `openspec/config.yaml` still describe the old process
  until the shared-file follow-up is applied; `design.md` (Risks) and `tasks.md` fix the
  order.
- `openspec/` and `AGENTS.md` are shared files, so Egor reviews this change as the
  second developer (Akim is the author).
- `retarget-mvp-domain` and `calculation-core-contract` already carry a DOR checklist
  and already use `spec-reviewer` and a `[PM]` task tag. They fit the new rules and
  need no edit, but may cite the new DOR requirement.

## Follow-up changes to shared files

These files are shared with Egor. They are NOT edited by this change and NOT applied by
`/opsx:apply`. Each edit is applied by hand, together, only after Egor agrees.

| File | Current text | Needed edit |
|---|---|---|
| `openspec/config.yaml:31-33` | "Team: two developers, Akim (...) and Egor (...). Ask who is working before development." | Three-person team: Akim, Egor, and a PM with no code zone; the PM owns scope, pricing, and legal decisions. Keep the "ask who is working" rule for Akim and Egor. |
| `openspec/config.yaml` (Conventions) | no note on validate | One line: `openspec validate` is structural; readiness also needs a `spec-reviewer` report with no blocker and no major finding. |
| `AGENTS.md` section 5 (intro, tables) | "Two developers work on this project" | Three-person team; add a PM row to the zone table (scope, pricing, legal; no code zone); say the PM has no agent unless a later change adds one. |
| `AGENTS.md` section 3 (DOR) | no `spec-reviewer` item | Add: a `spec-reviewer` report with no blocker and no major finding exists; add one sentence that `openspec validate` is structural. |
| `AGENTS.md` section 4 (DOD, Go/No-Go) | GO only by tests, coverage, UI/UX | Add the code-free GO path and the `tester` "tests: N/A" record. |
| `AGENTS.md` section 2 (lifecycle, step 7) | code review after GO | Note that for a code-free change the second developer's acknowledgement is the review. |
| `CLAUDE.md:69` | "`docs/` is untracked by design" | Now stale: `docs/decisions/` and `docs/reports/` are tracked. Reword (optional, Akim's file, no Egor agreement needed but shown as a diff). |
