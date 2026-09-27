# `team-roles-update` (WP7): questions for Egor

- Date: 2026-09-27
- From: Akim. To: Egor (second developer; `openspec/`, `AGENTS.md`, and `openspec/config.yaml` are shared files).
- Source: `openspec/changes/team-roles-update/` (proposal, design, delta, tasks A1.4 and B1) and `docs/decisions/team-roles-update-readiness.md`.
- Purpose: get your acknowledgement of the change and your agreement, or your changes, on the edits to shared files. Nothing here is final until you answer.

Russian version: `team-roles-update-egor-rus.md`.

## Why now

`team-roles-update` defines the only path to GO for a change with no code: validation,
a `spec-reviewer` report with no blocker and no major finding, and acknowledgement by
the developer who did not author the change. Without it, no spec-only change can reach
GO or be archived. Waiting on it now: `calculation-core-contract` (task 1.6),
`calculation-verification` (task 1.5), `retarget-mvp-domain` (task 5.5), and
`record-installed-skills-akim` (tasks 1.5-1.7). The change itself is ready: three
`spec-reviewer` passes, the last with 0 blockers and 0 major, and `openspec validate
--all --strict` passes.

## How to answer

Write your answer under "Answer" for each question and commit this file on a sub-branch
of `develop`, then merge it into `develop`. A commit by you that names
`team-roles-update` is the tracked acknowledgement that task A1.4 and the code-free GO
path require; it covers the version of the change on `develop` at the time of your
commit.

## Questions

### 1. Do you acknowledge the change as the second developer? (task A1.4)

- **What it changes** (`development-process`): the PM is a team role with no code zone
  (scope, pricing, legal); the DOR requires a `spec-reviewer` report with no blocker and
  no major finding, because `openspec validate` checks structure only; a change with no
  code reaches GO through validation, the review, and acknowledgement by the non-author,
  and the `tester` records `tests: N/A`, `coverage: N/A`, `UI/UX: N/A` with a reason;
  specs and designs cite only git-tracked sources (norm documents excepted).
- **Your side.** Read the delta `openspec/changes/team-roles-update/specs/development-process/spec.md`.

**Answer.**

### 2. The "no code" path list

- **Proposal.** A change has no code when it touches only `openspec/`, `docs/`,
  `agent-docs/`, everything under `.claude/`, `.kilo/`, `.kilocode/` (agent and skill
  definitions and agent settings), and the repository documents `AGENTS.md`,
  `CLAUDE.md`, `README.md`, `.editorconfig`. `.gitignore` stays off the list, so a
  change to it takes the normal gate.
- **Why.** The first draft listed only the directories and only agent and skill
  definitions. `AGENTS.md` (Branching rules) names `AGENTS.md` a no-code document (since
  commit `e484a42`) and names `.editorconfig`, agent settings, and agent entry files
  (`CLAUDE.md`) as repo-meta. `README.md` is not named in `AGENTS.md`; I add it as a
  prose document with no behavior. Without these files, Part B of this change (edits to
  `AGENTS.md` and `CLAUDE.md`) would itself count as code. `.gitignore` decides what gets
  committed, secrets included, so it is kept under the normal gate.
- **Please check.** Agent settings (`.claude/settings.json`) can hold permissions and
  hooks, and a hook runs shell commands. On this list, a settings change reaches GO with
  review and acknowledgement but without tests. If you want settings under the normal
  gate, say so and the list goes back to agent and skill definitions only.
- **Your side.** Agree, or name files to add or remove.

**Answer.**

### 3. The form of a PM approval (review minor 6)

- **Proposal.** A PM decision on scope, pricing, or a legal question counts as recorded
  when a developer adds a dated entry to a tracked file under `docs/decisions/` that
  names the decision, restates the PM's words, and says where they were given (meeting
  or message). The PM does not need to commit. If you agree, one sentence goes into the
  scenario "Scope, pricing, or legal decision" of the delta.
- **Why.** The delta says no developer records a PM decision as settled without the
  PM's approval, but not how that approval is shown. `retarget-mvp-domain` task 1.4
  (non-goals, B2C limit) needs exactly this.
- **Your side.** Agree, or propose another form.

**Answer.**

### 4. Edits to shared files (task B1)

They are applied by hand, together, after you agree, and are not part of
`/opsx:apply`. Current and target text: `proposal.md`, section "Follow-up changes to
shared files". Answer per line: agree, change (how), or reject.

| Task | File | Edit |
|---|---|---|
| B2 | `openspec/config.yaml:36-38` | "two developers" becomes a three-person team: Akim, Egor, and a PM with no code zone who owns scope, pricing, and legal decisions |
| B3 | `openspec/config.yaml` (Conventions) | one line: `openspec validate` is structural; readiness also needs a `spec-reviewer` report with no blocker and no major finding |
| B4 | `AGENTS.md` section 5 | three-person team; a PM row in the zone table; the PM has no agent unless a later change adds one |
| B5 | `AGENTS.md` section 3 (DOR) | a `spec-reviewer` item and the sentence that `openspec validate` is structural |
| B6 | `AGENTS.md` sections 4 and 2 (step 7) | the code-free GO path and the `tester` N/A record; for a code-free change the second developer's acknowledgement is the review |
| B7 | `CLAUDE.md:69` | reword "`docs/` is untracked by design": `docs/decisions/` and `docs/reports/` are tracked (Akim's file, shown for information) |

**Answer.**

### 5. When is Part B applied? (task A2.3)

- **Proposal.** Right after your answers to questions 1-4, in one commit, before the
  change is archived. If you want to defer Part B, write until when; the change can then
  be archived and B2-B8 move to a follow-up change.
- **Why.** After archive, `openspec/specs/development-process` states the new rules
  while `AGENTS.md`, which calls itself the single source of truth, still states the old
  ones. Task A2.3 therefore gates the archive on Part B or on your recorded deferral.

**Answer.**
