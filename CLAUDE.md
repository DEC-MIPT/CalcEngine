# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-09-27)

- Application code on `develop`: only Egor's normative pipeline (`normatives_pipeline/`,
  merged 2026-09-27, `02a33de`), with the root `pyproject.toml` (ruff exclude, pytest,
  branch coverage), `tests/`, and `docker-compose.yml` (PostgreSQL `dec-postgres` on
  port 5433, database `dec`). His collector is still on
  `feature/normative-collector/data`. `backend/`, `frontend/`, `params/`, `ml/` do not
  exist. What the pipeline means for Akim's work: `docs/reports/egor-branches-analysis.md`.
- Active changes (`openspec list` shows progress). Akim: `calculation-core-contract`
  (WP2), `calculation-verification` (WP4), `bootstrap-dev-environment` (WP6, spec
  phase GO, implementation not started), `record-installed-skills-akim`,
  `backend-layered-architecture` (WP5, not yet retargeted; lead moved from Egor to
  Akim 2026-09-28, since `backend/` is his zone — `docs/decisions/
  backend-layered-architecture-lead-change.md`; sections 1-3, 5-6 are his to decide
  and implement, Egor's agreement or execution is still needed for section 4, section
  7 (his ML zone), section 8 (his DevOps zone), and section 9's open items 9.3/9.6/9.7).
  Led by Egor, with Akim's parts: `retarget-mvp-domain` (WP1). Egor:
  `normatives-collector`, `normatives-parser`, `normatives-formula-contract`. Planned,
  not created: `norm-source-traceability` (WP3).
- The base specs in `openspec/specs/` still describe the placeholder domain (beam
  deflection, SP 16.13330) until `retarget-mvp-domain` is archived, and
  `backend-layered-architecture` still names it. The MVP domains are shallow
  foundations, then internal water supply. Build on the active changes, not on the
  placeholder.
- `team-roles-update` (WP7) is archived (2026-09-27,
  `openspec/changes/archive/2026-09-27-team-roles-update/`): the PM role and the
  code-free GO path are in `openspec/specs/development-process/spec.md` and `AGENTS.md`
  section 4, so spec-only changes can get their `tester` verdict.
- Session state for continuing the work: `docs/reports/session-state-2026-09-27.md`.
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

## Code journal

- Once implementation starts on a WP (writing actual code, not spec artifacts), keep a
  running journal at `docs/reports/WP<N>-code-journal.md` (one file per WP; English
  filename, Russian content, matching the existing `docs/reports/` convention). It
  records execution, not planning: it does not replace `tasks.md`'s checklist, and
  does not gate anything by itself.
- Create the file at the first implementation task of the WP, before starting it.
- One row per `tasks.md` subtask (its own numbering, e.g. `2.1`), appended right after
  that subtask is finished, as a Markdown table with exactly these five columns, in
  Russian:

  | Задача | Подзадача | Описание | Критерий успешности | Результат выполнения |
  |---|---|---|---|---|

  - Задача: the `tasks.md` section number and name (e.g. "2. Backend tooling").
  - Подзадача: the subtask id (e.g. `2.1`).
  - Описание: what `tasks.md` asked for, in Akim's own words.
  - Критерий успешности: how done is verified, from that subtask's own text (a
    command, a test, an observable behavior).
  - Результат выполнения: what actually happened — command output, files created or
    changed, and any deviation from the plan.

## Do not change without agreement

Edit these only when the user explicitly says so; otherwise show a diff.

- `openspec/**` (specs and changes are shared with Egor; extend, never contradict).
- `AGENTS.md`, `.gitignore`, `README.md`, `.kilo/**`, `.kilocode/**`,
  `.claude/agents/*` other than the two subagents added for Claude Code.
- Anything in Egor's zones: normative pipeline, NLP/RAG, ML, DevOps.
- The root `pyproject.toml` (shared with Egor's pipeline).

## Language

- Specs, ADRs, agents, skills, code, and commits: English.
- Conversation with the user: Russian.

## Commands that exist today

- `openspec validate --all --strict` — validate all specs and changes (read-only).
- `openspec list`, `openspec status --change <name>`, `openspec show <item>`.
- Egor's pipeline (his zone): `.venv/bin/python -m normatives_pipeline.search --json
  "<query>"` with `DEC_DATABASE_URL` set, as in
  `docs/decisions/normatives-pilot-usage-akim.md`. Its PostgreSQL is defined in
  `docker-compose.yml`. Ingestion and the pipeline's `pytest` are Egor's to run.

TBD, see planned change `bootstrap-dev-environment`: Akim's backend and frontend tooling
(`pytest` for the backend, `vitest`, `playwright`, `ruff`, `mypy`, `eslint`, `tsc`,
build). Do not invent or run commands from this list; none of them is set up for Akim's
zone yet.

## Subagents (also mirrored in `.kilo/agent/`)

- `spec-reviewer` — read-only review of a spec or change for completeness,
  testability, and OpenSpec format.
- `norm-traceability-checker` — read-only check that every calculation requirement
  names its norm source and edition. It does not verify clause correctness.

The Kilo mirrors carry no `model` or `tools`, so "read-only" is enforced by the
prompt there, and by `tools` only in `.claude/agents/`. Keep the bodies identical.

`docs/` is untracked by design (`.gitignore`), except `docs/decisions/` and
`docs/reports/`, which git tracks and the team uses as its written channel; do not
`@import` from `docs/`.
