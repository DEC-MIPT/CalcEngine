---
name: branching-convention
description: Branching convention for DEC. All work happens on develop; every task is a sub-branch of develop for the developer (Akim or Egor) working on it, and main stays frozen until the MVP. Use when creating branches for any task.
---

# Branching Convention

## Repository flow

- All work happens on the `develop` branch only. `develop` was created from `main`
  and contains the former `Specs` / `Specs-onboarding` work; the `Specs*` branches
  are historical and no longer used.
- A sub-branch of `develop` is a task branch — exactly the branch a developer
  (Akim or Egor) is currently working on. Create it from `develop` and merge it
  back into `develop` when the task is done.
- Nothing is merged into `main` until a working prototype (the MVP) exists in `develop`.

## Session start

Before starting a development session, check the state of commits on `develop` and
its remote: run `git fetch --all`, inspect the commits that arrived on `origin/develop`
and `origin/main` since the last session, and warn the developer about anything
important before doing other work. Remind the developer to run `git pull` (and
`git fetch --all`) so the local `develop` is up to date, and check `git status` for
uncommitted or untracked work left by previous sessions.

## Development branches

Development base is `develop`. Every task gets its own branch AND a zone sub-branch
mapped to the developer responsibility zone:

- Akim:
  - `feature/<task>/backend`
  - `feature/<task>/frontend`
- Egor:
  - `feature/<task>/data` (normative pipeline)
  - `feature/<task>/ml` (NLP/RAG/ML)
  - `feature/<task>/infra` (DevOps)

## Fix branches

- `fix/<task>/<zone>` (same zone set as above)

## Rules

- Create the branch from `develop`.
- Never implement directly on `develop` or `main`.
- The branch plan must be recorded in the OpenSpec change (`tasks.md`).
- Code MUST NOT overlap across zones so git branches merge without conflicts.

## Examples

- `feature/beam-deflection-check/backend` (Akim)
- `feature/beam-deflection-check/frontend` (Akim)
- `feature/normative-pipeline/data` (Egor)
- `feature/normative-parsing/ml` (Egor)
- `fix/docker-compose/infra` (Egor)
