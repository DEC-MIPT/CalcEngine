# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-09-28)

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
  backend-layered-architecture-lead-change.md`). WP5 was split on 2026-09-28 and Egor
  acknowledged the split the same day (`docs/decisions/
  backend-layered-architecture-split-egor{,-ack}.md`): it now holds only Akim's
  scaffold, config, `DECError`, `dec_app` session and migrations, parameters layer for
  engineer-set values, and `Calculator` registry (tasks 1.1-3.2, 5.1, 6.1). Moved out:
  the `normatives/` package and the parameters layer's reading of formulas (item 9.3) go
  to planned `normative-catalog-backend` (Akim and Egor); ML (`ml/`, item 9.7) to
  planned `ml-model-storage` (Egor); Docker/DevOps (item 9.6) to Egor's infra change.
  None of the three moved changes exists yet. WP5's task 3.x verify clauses run on a
  `dec_app` database created by hand on `dec-postgres`. Item 9.3 is still open: Egor
  wants the normative code to stay in `normatives_pipeline/`, not a second loader in
  `backend/normatives/`; it is the first decision of `normative-catalog-backend`.
  Led by Egor, with Akim's parts: `retarget-mvp-domain` (WP1; Akim's review tasks are
  done, Egor applies the follow-ups in WP1 tasks 3.3 and 5.6). Egor:
  `normatives-collector`, `normatives-parser`, `normatives-formula-contract`. Planned,
  not created: `norm-source-traceability` (WP3).
- `normatives-formula-contract`: Egor agreed to Akim's findings 11-15 on 2026-09-28
  (`docs/decisions/normatives-formula-contract-review-egor.md`). The five `NormRef`
  fields are fixed in code, `status` and `provenance` are stored per formula and per
  coefficient, and the consuming backend and frontend tasks (old 4.1-4.2) left that
  change: Akim adds them to his own change. The code is on `feature/normative-parser/ml`
  (which also moves `normatives_pipeline/` to a `src/` layout), not on `develop`. Open
  for Akim: the user-side verification action that sets `human-verified`
  (`formula-verification-akim.md`).
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
