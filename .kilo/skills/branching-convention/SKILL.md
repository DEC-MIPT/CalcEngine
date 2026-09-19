---
name: branching-convention
description: Branching convention for DEC. Planning happens on Specs, development on develop with zone sub-branches, and main stays frozen until the MVP. Use when creating branches for any task.
---

# Branching Convention

## Repository flow

- Planning happens on the `Specs` branch.
- When planning is done: commit and push `Specs`, create `develop` from `main`, and
  merge `Specs` into `develop`.
- Nothing is merged into `main` until a working prototype (the MVP) exists in `develop`.

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
