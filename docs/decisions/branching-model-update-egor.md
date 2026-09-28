# Branching model: documents straight to `develop`, code by feature branch (acknowledgement requested from Egor)

- Date: 2026-09-28
- From: Akim. To: Egor.

Russian version: `branching-model-update-egor-rus.md`.

## Decision

Two rules change, for both developers.

1. **Documents are committed directly to `develop`**, with no sub-branch and no merge
   commit. A document is a file on the existing "no code" list: `openspec/**`, `docs/**`,
   `agent-docs/**`, the agent and skill definitions under `.claude/`, `.kilo/`, and
   `.kilocode/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `.editorconfig`. Reason: you read
   `develop`, not my sub-branches, and each doc-only merge cost both of us a pull into our
   own branches.
2. **Code goes only through a feature branch**, `feature/<feature>/<zone>`, one branch per
   feature (a component or a stage of the plan). It is merged into `develop` only when the
   whole feature is done: every task that `tasks.md` assigns to it checked off, `tester` GO,
   review (GO is per feature; a change is archived when all its features are merged). A feature
   has exactly one branch, so work in two zones is two features. A feature belongs to one
   change; a change may hold several features. Never per
   section or per subtask. The branch is pushed to `origin` whenever a subtask is finished, and
   picks up new documents with `git merge develop`. Every file not on the document list
   (source code, tests, package manifests, `.gitignore`, agent settings, pre-commit,
   `docker-compose.yml`) is code for this rule.

Before every commit and push to `develop`, run `git fetch --all` and `git pull --ff-only`;
if `develop` has diverged, stop and resolve it first.

## What I changed on `develop`

`AGENTS.md` (Branching rules, lifecycle steps 4 and 7, DOR), the `development-process` spec
(requirement "Branch-per-feature with zone sub-branches", new requirement "Documents commit
directly to develop"), `openspec/config.yaml`, the skills `branching-convention` and
`sdd-workflow`, the agents `orchestrator`, `business-analyst`, `backend-developer`,
`frontend-developer`, `data-engineer`, `spec-reviewer` (both `.claude/` and `.kilo/`),
`CLAUDE.md`, and the `Branch:` lines in the `tasks.md` of my changes. I did not touch
`retarget-mvp-domain` (you lead it; its `tasks.md` still names `feature/<task>/<zone>` in
line 7) or your changes.

These shared files were edited before your acknowledgement, at my decision. If you object
to any part, answer in the file named below and I revert that part.

## What Akim asks of Egor

1. Acknowledge the two rules for your zones (data, ml, infra) too, in a tracked file or a
   commit that names this note.
2. Confirm that your two open branches, `feature/normative-collector/data` and
   `feature/normative-parser/ml`, follow rule 2 as they are: each merges into `develop`
   when its feature is whole. Your `normatives-formula-contract` code is on the parser
   branch; say whether it is a separate feature branch or part of the parser one.
3. Update `retarget-mvp-domain/tasks.md` line 7 (`feature/<task>/<zone>`), since you lead
   that change. In the same edit, this is the moment to drop its "short-lived sub-branch"
   wording (already on your list from the WP1 review).
4. Note the pull step: because documents now land on `develop` without a merge from a
   sub-branch, `git pull --ff-only` on `develop` before you commit a document.

Nothing else is asked of you now. Deleting the old `Specs` and `Specs-onboarding` branches
on `origin` is a separate question and is not settled by this note.
