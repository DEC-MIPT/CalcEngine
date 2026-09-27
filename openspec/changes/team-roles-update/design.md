# Design

## Context

`AGENTS.md` sections 3-5 and `openspec/specs/development-process/spec.md` define the
process for a two-developer team and for changes with code. The team has three people,
and several changes are documentation only. This change fixes the specs; the shared
files follow separately (see `proposal.md`). The change is documentation only.

## Goals

- A PM role that is explicit and does not overlap with the code zones.
- A GO path for changes with no code that a second person can check without running
  tests.
- A DOR that does not treat a green `openspec validate` as readiness.
- Rationale in specs that a reviewer can open in git.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **The PM is a role, not a zone and not an agent.** The PM owns scope, pricing, and
   legal questions. The PM writes no code and owns no branch, so the zone rules and the
   `feature/<task>/<zone>` scheme are unchanged. The existing `[PM]` executor tag in
   `openspec/changes/retarget-mvp-domain/tasks.md` (task 1.4) already treats the PM
   this way. The specs name the role only.
2. **"No code" is defined by paths.** A change has no code when it adds or edits no
   file outside `openspec/`, `docs/`, `agent-docs/`, the agent tool directories
   `.claude/`, `.kilo/`, and `.kilocode/` (agent and skill definitions and agent
   settings), and the repository documents `AGENTS.md`, `CLAUDE.md`, `README.md`, and
   `.editorconfig`. Anything else, including migrations, config, and test files, is code
   and uses the normal gate. A path rule is checkable from the diff and does not depend
   on the author's opinion. Where the list comes from: `AGENTS.md` (Branching rules)
   lists `AGENTS.md` among no-code documents ("A change to `openspec/**` (specs and
   changes), `AGENTS.md`, or any other no-code document", `AGENTS.md:73-74`) and names
   `.editorconfig`, agent settings, and agent entry files (which covers `CLAUDE.md`) as
   repo-meta (`AGENTS.md:70`). `README.md` is not named there; this change adds it as a
   prose document with no behavior. Without these files, Part B of this change would
   itself count as code. `.gitignore` stays off the list: it decides what gets
   committed, secrets included, so a change to it takes the normal gate. The list was
   extended by Akim on 2026-09-27 (review minor 8) and is part of what Egor
   acknowledges.
3. **The second developer is whoever did not author the change.** If Akim authored it,
   Egor acknowledges it; if Egor authored it, Akim does. This holds for either agent
   tool. The acknowledgement is a tracked artifact (a commit or a review comment that
   names the change), not a chat message, so it can be checked later.
4. **The `tester` records N/A, it does not skip.** The verdict records `tests: N/A`,
   `coverage: N/A`, `UI/UX: N/A`, each with a reason ("change has no code"). A missing
   record is NO-GO. This keeps the `tester` as the only agent that declares GO
   (`AGENTS.md` section 4) and makes the exception visible.
5. **`spec-reviewer` is required in the DOR and in code-free GO.** `openspec validate`
   checks structure only; the review checks completeness and testability. "No blockers"
   means the report lists no finding at the blocker or major level; the requirement text
   in the spec says so, so the spec and this design agree. The DOR is defined in
   `AGENTS.md` section 3 only; this change gives it a requirement in the spec.
6. **Modified requirements repeat their full text.** OpenSpec MODIFIED replaces a
   requirement, so each MODIFIED block below carries the whole requirement with the
   new sentences added.
7. **Only tracked sources, for rationale.** The rationale of a decision in a spec,
   `proposal.md`, or `design.md` cites a file git tracks (`openspec/`, `agent-docs/`,
   `docs/decisions/`, `docs/reports/`) or restates the reasoning in the text. The
   "passport" and the untracked audit reports are not sources; this change restates the
   audit findings it rests on in `proposal.md`. Norm citations are outside the rule:
   `agent-docs/domain-constraints.md` requires them to come from the primary source
   text (SP, GOST), which the repository does not track. The existing passport
   citations are listed in `tasks.md` for the owner of `backend-layered-architecture`
   to replace.

## What this change does and does not close in `record-installed-skills-akim`

Its `tasks.md` records the block:

- Task 1.5: "Get Egor's acknowledgement, because `openspec/` is shared; recorded as a
  commit or comment by Egor that names this change".
- Task 1.7: "`tester` issues the verdict for this change (see DOD)". Its DOD says
  `tester` "issues an explicit verdict 'no code, no tests, coverage not applicable'",
  which no spec defines, while `development-process` defines GO only as tests with
  >= 95% coverage, UI/UX confirmation, and validation.

Closed: the missing path. After this change is archived, that change is a change with
no code (`openspec/` files only), and the new "Go/No-Go verdict and archive"
requirement gives it a GO path whose three conditions are also in its DOD: validation
passes (task 1.3), `spec-reviewer` reports no blocker and no major finding (task 1.6;
its DOD says only "no blockers", which is weaker), and Egor, who did not author it,
acknowledges it (task 1.5). Its DOD adds a fourth condition, the record check against
the skills CLI lock file. The new rule does not include it and does not remove it: it
stays as an extra condition of that change, and the new rule is the minimum.

Not closed:

- **Acknowledgement.** Task 1.5 stays. The rule defines it as a GO condition; it does
  not remove the wait for Egor.
- **Verdict wording.** The new rule requires the `tester` verdict to carry the fields
  `tests: N/A`, `coverage: N/A`, and `UI/UX: N/A`, each with the reason that the change
  has no code. The DOD of that change says "no code, no tests, coverage not
  applicable", which lacks the UI/UX field and the reason. A verdict that follows that
  DOD literally is NO-GO under the new rule. So the `tester` must use the exact fields
  when it runs task 1.7, and the DOD wording of that change should be aligned when its
  owner next edits it (section C in `tasks.md`). This change does not edit it.
- **"No blockers".** Its task 1.4 review was "NOT READY" with major findings and no
  blocker. Under the new definition, task 1.6 passes only when no blocker and no major
  finding remains.
- **Timing.** The rule takes effect when this change is archived. Until then, task 1.7
  has no defined path, and its "Dependencies: None" line is not accurate.

Order of events: (1) this change is acknowledged by Egor, merged, and archived;
(2) Egor acknowledges `record-installed-skills-akim` (task 1.5); (3) `spec-reviewer`
is re-run (task 1.6); (4) `tester` records the verdict with the N/A fields (task 1.7).

## Risks

- **`AGENTS.md` and `config.yaml` lag behind the specs.** `AGENTS.md` calls itself the
  single source of truth, and it defines GO only through tests and coverage, has no PM,
  and has no `spec-reviewer` item in the DOR. Until the shared-file follow-up (Part B of
  `tasks.md`) is applied, the specs and `AGENTS.md` contradict each other. Mitigation:
  `tasks.md` orders the work so that this change is archived only after Part B is
  applied, or after Egor records in a tracked commit or comment that Part B is deferred
  and until when.
- The path rule for "no code" excludes some low-risk config files by design; a file that
  is neither code nor in the listed paths goes through the normal gate.
- Acknowledgement is one person's check. That is deliberate: the team has two
  developers, and the PM is not a code reviewer.

## Migration

None. Archive syncs the delta into `openspec/specs/development-process/spec.md`.
