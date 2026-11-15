---
name: branching-convention
description: Branching convention for DEC. Documents are edited, committed and pushed only on develop; code goes through one feature branch per feature, merged into develop only when the whole feature is done; main stays frozen until the MVP. Use when creating branches or deciding where a change goes.
---

# Branching Convention

## Repository flow

- `develop` is the integration branch. It was created from `main` and contains the former
  `Specs` / `Specs-onboarding` work; the `Specs*` branches are historical and no longer
  used.
- **Documents are edited, committed and pushed only on `develop`**, with no
  sub-branch and no merge commit. Before each documentation edit, commit or push,
  verify `git branch --show-current` is `develop`. The document/no-code list is
  defined in `AGENTS.md`; it includes instruction-only agent and skill mirrors.
  If another branch is checked out, preserve all work and use an authorized safe
  switch or a `develop` checkout before editing. Do not edit documents on a feature
  branch with the intention of committing them to `develop` later. Stop if a switch
  cannot preserve existing changes; never stash, reset or force checkout to clean it.
- **Code goes only through a feature branch.** Every other file (source code, tests,
  package manifests, `.gitignore`, agent settings, pre-commit config,
  `docker-compose.yml`) is code for this rule.
- A feature branch is merged into `develop` only when the whole feature is done: every
  task that `tasks.md` assigns to the feature is checked off, the `tester` declared GO
  for the feature, and the review passed. Never per section or per subtask. A feature belongs to one
  OpenSpec change; a change may hold several features, and the change is archived when all
  of them are merged.
- Nothing is merged into `main` until a working prototype (the MVP) exists in `develop`.

## Session start

Before starting a development session, check the state of commits on `develop` and
its remote: run `git fetch --all`, inspect the commits that arrived on `origin/develop`
and `origin/main` since the last session, and warn the developer about anything
important before doing other work. Remind the developer to run `git pull` (and
`git fetch --all`) so the local `develop` is up to date, and check `git status` for
uncommitted or untracked work left by previous sessions.

Before every commit and every push to `develop`, run `git fetch --all` and
`git pull --ff-only`. If `develop` has diverged, stop and resolve it first.

## Feature branches

A feature is a component or a stage of the plan (calculation engine, report generator,
backend core, frontend, ...). Each feature gets one branch from `develop`, named
`feature/<feature>/<zone>`, with these technical zones:

- `feature/<feature>/backend`
- `feature/<feature>/frontend`
- `feature/<feature>/data` (normative pipeline)
- `feature/<feature>/ml` (NLP/RAG/ML)
- `feature/<feature>/infra` (DevOps)

Akim is the sole active developer. Human ownership follows the current roster in
`AGENTS.md`; Egor's former ownership is historical. Existing branch names and
technical boundaries stay unchanged. A replacement is recognized only after
Akim announces one and the roster is updated.

## Fix branches

- `fix/<feature>/<zone>` (same zone set as above)

## Rules

- Create the branch from `develop`, or from the branch of an unmerged feature it depends on.
- Push the branch to `origin` with the commit that finishes a subtask, so it stays visible.
- With explicit consent, bring committed documents into a code branch with
  `git merge develop`; do not edit them while on that branch. Journal updates and
  OpenSpec task changes require a `develop` checkout even during a code feature.
- Never implement code directly on `develop` or `main`.
- The change's `tasks.md` names each feature, its branch and its tasks (every task with
  code belongs to exactly one feature), or states that the change has no code and no branch.
  One feature has exactly one branch; work in two zones is two features. A feature that
  needs code from an unmerged feature branches from it and merges after it. Subtasks are checked off in `develop` as they are
  done, so `tasks.md` may run ahead of the code in `develop` until the feature is merged.
- Code MUST NOT overlap across zones so git branches merge without conflicts.
- Workflow requirements do not grant Git delivery permission: commits, merges and
  pushes require Akim's explicit consent.
- While Akim is the sole active developer, second-human-developer acknowledgement
  is not required; independent agent reviews and tester gates still apply.

## Examples

- `feature/calculation-engine/backend`
- `feature/frontend-app/frontend`
- `feature/normative-collector/data`
- `feature/normative-parser/ml`
- `fix/docker-compose/infra`
