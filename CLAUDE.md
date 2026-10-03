# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-10-03)

- Code on `develop`: Akim's `backend/` (WP5 backend core, merged `53a4892`; WP6 backend
  tooling) and `frontend/` (WP6 tooling skeleton), and Egor's `ml/` (normative pipeline
  and collector under `ml/src/normatives_pipeline/`, with `ml/pyproject.toml`,
  `ml/configs/`, `ml/research/`, `ml/tests/`; moved there 2026-10-03, `24797f7`) and
  `infra/docker-compose.yml` (PostgreSQL `dec-postgres`, port 5433, single database
  `dec`). The root has no `pyproject.toml`, `tests/` or `normatives_pipeline/` any more.
  Akim's unmerged feature branches: `feature/calculation-engine/backend` and
  `feature/report-generator/backend` (WP2), `feature/calculation-api/backend` (WP8, from
  the report branch). `params/` does not exist; the pilot parameter file is under
  `backend/` on the engine branch.
- Active changes (`openspec list` shows progress). Akim: `calculation-core-contract`
  (WP2; task 1.8 closed 2026-10-03, so the engine branch can merge once its tasks pass),
  `calculation-api` (WP8, sections 2-3 implemented on its branch),
  `calculation-verification` (WP4), `bootstrap-dev-environment` (WP6),
  `backend-layered-architecture` (WP5, all tasks done, not archived),
  `record-installed-skills-akim`. Planned by Akim: `normative-catalog-backend` (Akim and
  Egor; Egor answered its questions 2026-10-03, so the proposal can be written),
  `user-accounts-auth` (test accounts made by an admin command, login, JWT, Argon2id;
  tiers, trial and billing deferred). Led by Egor, with Akim's parts: `retarget-mvp-domain` (WP1;
  Akim's review tasks are done, Egor applies the follow-ups in WP1 tasks 3.3 and 5.6).
  Egor: `normatives-collector`, `normatives-parser`, `normatives-formula-contract`.
  Planned, not created: `norm-source-traceability` (WP3), `ml-model-storage` and an
  infra change (both Egor's).
- Normative catalog contract (Egor, 2026-10-03,
  `docs/decisions/normative-catalog-backend-questions-akim.md`, "Answers"): the
  contract between the zones is the database. Egor owns read-only views and the role
  `dec_normatives_reader` in `dec_normatives`, the binding of a calculation type to its
  norms, and table row/column headings with units; the backend reads only the views,
  through its own repository, with `DEC_NORMATIVES_DATABASE_URL`, and never imports
  `ml/`. Old WP5 item 9.3 is settled this way. The exact JSON of the expression tree is
  fixed together in `normative-catalog-backend`. Egor named the end of 2026-10-04 for
  `normatives-formula-contract` 1.4-1.7, the views and WP1 task 3.1.
- Formula status: the pipeline writes `status = unverified` and
  `provenance = machine-extracted` (stored per formula and coefficient,
  `normatives-formula-contract` task 1.6, not done yet); the backend builds
  `NormRef.status` from `provenance`. Pilot steps are shown as unverified
  (`docs/decisions/pipeline-open-items-questions-akim.md`, "Answers", 2b). There is no
  user-side verification action. Egor's `formulas.toml` is to be deleted (still at
  `ml/configs/formulas.toml`).
- Variables: Akim's `Settings` reads `DEC_APP_DATABASE_URL` (`dec_app`) and
  `DEC_NORMATIVES_DATABASE_URL`. Egor's code still reads `DEC_DATABASE_URL`; he agreed to
  rename it to `DEC_NORMATIVES_DATABASE_URL`. `dec_app` is not in the compose file:
  backend verify clauses run on a database created by hand on `dec-postgres`.
- Known issue: `.secrets.baseline` lists paths from before the move and misses newer
  backend files, so `pre-commit run --all-files` fails on `develop`; the fix is WP6 task
  4.5 on `feature/dev-environment/backend`.
- Branching model (Akim, 2026-09-28; Egor confirmed both rules 2026-09-29,
  `docs/decisions/pipeline-followup-answers-egor-rus.md`): documents (the "no code" list in
  `AGENTS.md`, including this file, `docs/reports/` and the code journals) are committed
  directly to `develop`, after `git fetch --all` and `git pull --ff-only`. Code goes only
  on `feature/<feature>/<zone>` and is merged into `develop` when the whole feature is
  done. Planned Akim features: `backend-core` (WP5), `calculation-engine` (WP2),
  `calculation-verification` (WP4), `report-generator` (WP2 6.3-6.4), `frontend-app`
  (WP2 3.4, 3.5, 5.4), `dev-environment` (rest of WP6). The eight earlier per-change
  branches are merged history.
- The base specs in `openspec/specs/` still describe the placeholder domain (beam
  deflection, SP 16.13330) until `retarget-mvp-domain` is archived, and
  `backend-layered-architecture` still names it. The MVP domains are shallow
  foundations, then internal water supply. Build on the active changes, not on the
  placeholder.
- `team-roles-update` (WP7) is archived (2026-09-27,
  `openspec/changes/archive/2026-09-27-team-roles-update/`): the PM role and the
  code-free GO path are in `openspec/specs/development-process/spec.md` and `AGENTS.md`
  section 4, so spec-only changes can get their `tester` verdict.
- Session state for continuing the work: `docs/akim/reports/session-state-2026-09-27.md`
  (untracked); WP code journals in `docs/akim/reports/WP<N>-code-journal.md`.
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
  running journal at `docs/akim/reports/WP<N>-code-journal.md` (one file per WP; English
  filename, Russian content). This directory is untracked (2026-09-28, Akim's own zone,
  not pushed to `origin`) — the journal is a personal working record, not the team's
  written channel; that is `docs/decisions/`. It records execution, not planning: it
  does not replace `tasks.md`'s checklist, and does not gate anything by itself.
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
- Anything in Egor's zones: normative pipeline, NLP/RAG, ML, DevOps (`ml/`, `infra/`).

## Language

- Specs, ADRs, agents, skills, code, and commits: English.
- Conversation with the user: Russian.

## Commands that exist today

- `openspec validate --all --strict` — validate all specs and changes (read-only).
- `openspec list`, `openspec status --change <name>`, `openspec show <item>`.
- Backend: `backend/check.sh` (`ruff`, `mypy`, `pytest` with branch coverage >= 95% on
  `app`), using `backend/.venv`. On `feature/calculation-api/backend`, tests marked
  `postgres` run only with `DEC_TEST_APP_DATABASE_URL` set to a hand-made database on
  `dec-postgres`, and are skipped otherwise.
- Frontend: `frontend/check.sh` (`eslint`, `tsc -b`, `vitest run --coverage`).
- Pre-commit: `pre-commit run --all-files` (`detect-secrets`; see the known issue above).
- Egor's pipeline (his zone): `python -m normatives_pipeline.search --json "<query>"`
  after `pip install -e "./ml[ml]"`, with `DEC_DATABASE_URL` set, as in `README.md`
  and `docs/decisions/normatives-pilot-usage-akim.md`. Its PostgreSQL is
  `infra/docker-compose.yml`. Ingestion and the pipeline's `pytest` are Egor's to run.

Not set up yet: `playwright`, and the frontend build for shipping. Do not invent
commands for them.

## Subagents (also mirrored in `.kilo/agent/`)

- `spec-reviewer` — read-only review of a spec or change for completeness,
  testability, and OpenSpec format.
- `norm-traceability-checker` — read-only check that every calculation requirement
  names its norm source and edition. It does not verify clause correctness.

The Kilo mirrors carry no `model` or `tools`, so "read-only" is enforced by the
prompt there, and by `tools` only in `.claude/agents/`. Keep the bodies identical.

`docs/` is untracked by design (`.gitignore`), except `docs/decisions/`, which git
tracks and the team uses as its written channel; do not `@import` from `docs/`.
`docs/akim/` (plan, code journals, personal notes) is Akim's own zone and stays
untracked on purpose (2026-09-28), not pushed to `origin`.
