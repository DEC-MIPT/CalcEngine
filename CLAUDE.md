# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-09-27)

- No application code on `develop`: `backend/`, `frontend/`, `params/`, `ml/`,
  `docker-compose.yml` do not exist. Egor's pipeline code is on his branches
  (`feature/normative-collector/data`, `feature/normative-parser/ml`), not yet merged.
- Active changes (`openspec list` shows progress). Akim: `calculation-core-contract`
  (WP2), `calculation-verification` (WP4), `team-roles-update` (WP7),
  `record-installed-skills-akim`. Led by Egor, with Akim's parts:
  `retarget-mvp-domain` (WP1), `backend-layered-architecture` (WP5, not yet
  retargeted). Egor: `normatives-collector`, `normatives-parser`. Planned, not
  created: `norm-source-traceability` (WP3), `bootstrap-dev-environment` (WP6).
- The base specs in `openspec/specs/` still describe the placeholder domain (beam
  deflection, SP 16.13330) until `retarget-mvp-domain` is archived, and
  `backend-layered-architecture` still names it. The MVP domains are shallow
  foundations, then internal water supply. Build on the active changes, not on the
  placeholder.
- No spec-only change can reach GO until `team-roles-update` is acknowledged by Egor;
  his answers are awaited in `docs/decisions/team-roles-update-egor.md`.
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

## Subagents (also mirrored in `.kilo/agent/`)

- `spec-reviewer` — read-only review of a spec or change for completeness,
  testability, and OpenSpec format.
- `norm-traceability-checker` — read-only check that every calculation requirement
  names its norm source and edition. It does not verify clause correctness.

The Kilo mirrors carry no `model` or `tools`, so "read-only" is enforced by the
prompt there, and by `tools` only in `.claude/agents/`. Keep the bodies identical.

`docs/` is untracked by design (`.gitignore`); do not `@import` from it.
