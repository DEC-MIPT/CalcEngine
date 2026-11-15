# Tasks

Owner: Akim, repository instructions and documentation. No code and no branch.
Documentation creation, editing, commits and pushes occur only on `develop`.
Preserve user work through an authorized safe switch or a develop worktree before writing. No commit, merge or push is authorized by this task.
Local `docs/akim/README.md` remains ignored; shared instructions contain a fallback.

## 1. Capture and plan

- [x] 1.1 Inspect Git state, instruction scopes, OpenSpec integration and task-related
  decisions and analysis. Verify: sources and preservation boundaries listed in design.
- [x] 1.2 Create proposal, design, delta spec and task plan with no-code scope and
  explicit acceptance/closure criteria.
- [x] 1.3 Run strict OpenSpec validation and obtain a current `spec-reviewer` report
  with no blocker or major finding before declaring navigation ready.

## 2. Context navigation

- [x] 2.1 Add selective entry, actual repository map, sourced commands and missing quality
  guidance to `AGENTS.md`; preserve existing team gates and section references.
- [x] 2.2 Create one local `docs/akim/README.md` with task routes and current-work pointers
  to existing records; verify report claims only to the extent needed for navigation.
- [x] 2.3 Record the agreed operational-index lifecycle in AGENTS.md, this change's
  proposal/design/delta and a short local index reminder; verify compact unfinished
  routes, existing completion gates, evidence preservation and durable dependency links
  without restructuring existing index history or introducing a numeric size limit.
- [x] 2.4 Verify the lifecycle amendment's documents and preservation scope; run selected
  and all strict validation, link/whitespace checks and available document hooks, and
  confirm existing history, unrelated work, source code and generated instructions remain intact.
- [x] 2.5 Obtain a current spec-reviewer report for the amended artifacts and a tester
  no-code reassessment with tests/coverage/UI/UX N/A reasons; record actual results in
  verification.md without inventing the pending other-developer acknowledgement or GO.

Completed original tasks and their verification describe the initial navigation scope.
The lifecycle amendment requires the current checks and reviews in 2.4-2.5 before its
readiness is recorded. This amendment codifies the rule only; retrospective cleanup of
existing index history is separate work.

## 3. Verification and review

- [x] 3.1 Check relative links, paths, command provenance, whitespace, privacy, instruction
  block preservation, unchanged Claude files and pre-existing edits. Run available
  documentation hooks and `openspec validate --all --strict`; record actual results.
- [x] 3.2 Rehearse task routes and obtain a final `spec-reviewer` review; fix blockers
  and major findings. Verify the tracked fallback without `docs/akim/` too.
- [x] 3.3 Second-human acknowledgement: N/A under the recorded sole-developer policy,
  [decision](../../../docs/decisions/backend/2026-11-15-solo-developer-document-workflow.md).
  The original request in question 3 of
  [the file to Egor](../../../docs/decisions/backend/2026-10-28-shared-config-changes-to-egor.md)
  is preserved as history; no acknowledgement from Egor is claimed.
- [x] 3.4 `tester` records the no-code verdict with `tests: N/A`, `coverage: N/A` and
  `UI/UX: N/A`, each because there is no code. GO requires 3.1-3.3.
  Initial result in `verification.md`: NO-GO for closure, solely because 3.3 was pending.
  The lifecycle amendment's tester reassessment is tracked in 2.5.
- [x] 3.5 Reassess the current no-code verdict after the sole-developer policy update;
  verify clean current review and document checks with individual N/A records,
  without treating the waived human acknowledgement as an automatic GO or archive.

## 4. Close

- [ ] 4.1 After GO and authorized delivery, `spec-keeper` syncs the delta and archives;
  verify `openspec validate --all --strict`. Commit/push remain subject to user consent.

## DOR

- [x] Proposal, design, specs and plan exist; scope is documentation only, no branch.
- [x] Functional scenarios and non-functional limits are explicit in the delta/design.
- [x] Tasks fit one session and identify acceptance checks; no external code dependency.
- [x] Strict validation passes and current `spec-reviewer` has no blocker or major finding.

## Acceptance and DOD / Go-No-Go

- Navigation identifies relevant requirements, actual code/tests and checks for engine,
  API, frontend, reports and specs without requiring all local reports.
- Shared instructions work when ignored local context is unavailable.
- Checks distinguish sourced commands from successful execution and facts from plans.
- The index routes unfinished work through compact summaries, removes completed cards
  only under existing completion gates, and preserves unique history, durable contracts
  and unresolved obligations in discoverable owning records.
- The lifecycle amendment adds policy and a reminder only; no retrospective history
  cleanup, numeric size budget, application change or new closure gate is included.
- Only allowed documentation changes; no secrets, private preferences or machine paths.
- GO: strict validation, clean review, verification complete and tester N/A records.
  Human acknowledgement is required only when the recorded active-team policy says so;
  it is waived while Akim is the sole developer. NO-GO: any failed check, open blocker/major
  or missing applicable evidence. Archive only after the GO and spec sync gates.
