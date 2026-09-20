# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status

- Spec-only, no code yet. The repository holds OpenSpec specs, one active change
  (`backend-layered-architecture`), and agent/skill definitions. `backend/`,
  `frontend/`, `params/`, `ml/`, `docker-compose.yml` do not exist.
- The specs still target a placeholder domain (beam deflection, SP 16.13330). The
  confirmed MVP domain is shallow foundations and internal water supply. Do not
  build on the placeholder; a change to retarget the domain is planned.
- Norm editions for the MVP domain come from the team and are `unverified` until
  checked against source texts.

## Who is working

- Claude Code sessions here are Akim's (frontend/backend, engine, report generator).
  Egor uses Kilo Code. Skip the "which developer" question; ask only when a task
  touches Egor's zones (data, ml, infra).

## SDD gate

- Create an OpenSpec change (`openspec new change <name>`, or `/opsx:propose`) for any
  new behavior, changed requirement or contract, architecture decision, or change to
  a responsibility zone.
- Do not write application code, tests for unspecified behavior, or migrations
  without a change that meets the DOR (`AGENTS.md` section 3) and passes
  `openspec validate --strict`.

## Do not change without agreement

Edit these only when the user explicitly says so; otherwise show a diff.

- `openspec/**` (specs and changes are shared with Egor; extend, never contradict).
- `AGENTS.md`, `.gitignore`, `README.md`, `.kilo/**`, `.kilocode/**`,
  `.claude/agents/*` other than the two subagents added for Claude Code.
- Anything in Egor's zones: normative pipeline, NLP/RAG, ML, DevOps.

## Language

- Specs, ADRs, agents, skills, code, and commits: English.
- Conversation with the user: Russian.

## Commands that exist today

- `openspec validate --all --strict` — validate all specs and changes (read-only).
- `openspec list`, `openspec status --change <name>`, `openspec show <item>`.

TBD, see planned change `bootstrap-dev-environment`: tests (`pytest`, `vitest`,
`playwright`), lint and types (`ruff`, `mypy`, `eslint`, `tsc`), build, `docker`.
Do not invent or run commands from this list; none of them is set up yet.

## Subagents (Claude Code only)

- `spec-reviewer` — read-only review of a spec or change for completeness,
  testability, and OpenSpec format.
- `norm-traceability-checker` — read-only check that every calculation requirement
  names its norm source and edition. It does not verify clause correctness.

`docs/` is untracked by design (`.gitignore`); do not `@import` from it.
