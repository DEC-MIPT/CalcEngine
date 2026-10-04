# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-10-04)

- Code on `develop`: Akim's `backend/` — WP5 backend core (`53a4892`), WP6 backend
  tooling, the WP2 calculation engine (`8c001b9`) and report generator (`9642d8d`), and
  the WP8 calculation API (`23318c1`: `GET /calculation-types`, `POST /calculations`,
  `GET /calculations/{result_id}`, `POST /calculations/{result_id}/report`, table
  `calculation_result` in `dec_app`, Alembic head `ae350ead9bfd`), all with branch
  coverage 100%; the pilot type `foundations_shallow_r` with its engineer-set file
  `backend/params/foundations_shallow_r.yaml`; `frontend/` is still the WP6 tooling
  skeleton. Egor's `ml/` (normative pipeline and collector under
  `ml/src/normatives_pipeline/`, with `ml/pyproject.toml`, `ml/configs/`, `ml/research/`,
  `ml/tests/`; moved there 2026-10-03, `24797f7`) and `infra/docker-compose.yml`
  (PostgreSQL `dec-postgres`, port 5433, single database `dec`). The root has no
  `pyproject.toml`, `tests/` or `normatives_pipeline/` any more. `develop` has no
  catalog parameter source yet, so `POST /calculations` for the pilot answers
  `503 parameter_source_unavailable` there until `feature/normative-catalog/backend`
  (WP9) is merged. The review follow-ups are merged too (`1027627`). The three merged
  feature branches and `fix/calculation-engine/backend` still exist on `origin` (delete
  only on Akim's word).
- Active changes (`openspec list` shows progress). Akim: `calculation-core-contract`
  (WP2; engine and report merged; open: the frontend feature 3.4, 3.5, 5.4, task 7.2,
  archive after WP1), `calculation-api` (WP8; merged, only 6.5 sync and archive left,
  after WP2), `calculation-verification` (WP4), `bootstrap-dev-environment` (WP6;
  `feature/dev-environment/backend` merged into `develop` in `bec3d43` on 2026-10-04
  after the `tester` GO and the `orchestrator` review, only 7.3 sync and archive left),
  `backend-layered-architecture` (WP5, all tasks done, not archived),
  `record-installed-skills-akim`, `normative-catalog-backend` (WP9, Akim and Egor; on
  `develop` since 2026-10-03, DOR met 2026-10-04 when Egor confirmed its read contract,
  task 1.4; Akim's sections 3-6 are done on `feature/normative-catalog/backend`
  against the synthetic contract (2026-10-04, last code commit `226d44f`, ticked in
  `tasks.md`): the catalog parameter source wired into `create_app`,
  `GET /normatives/search` and `GET /normatives/documents/{document_id}`; section 7
  waits for Egor's section 2 on `feature/normative-catalog/data`). Planned by Akim:
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
  `normatives-formula-contract` 1.4-1.7, the views and WP1 task 3.1. On 2026-10-04
  (`docs/decisions/normative-catalog-backend-contract-akim.md`, "Answers") he confirmed
  WP9 decisions 1-3 without changes: schema `catalog_read`, the reader role's
  privileges and the `REVOKE` on `public`, the interim database `dec`, every column of
  the views, the expression tree built at ingestion with no extra nodes; and his
  section 2, due on `develop` by the end of 2026-10-04.
- Formula status: the pipeline writes `status = unverified` and
  `provenance = machine-extracted` (stored per formula and coefficient,
  `normatives-formula-contract` task 1.6, not done yet); the backend builds
  `NormRef.status` from `provenance`. Pilot steps are shown as unverified
  (`docs/decisions/pipeline-open-items-questions-akim.md`, "Answers", 2b). There is no
  user-side verification action. Egor's `formulas.toml` is to be deleted (still at
  `ml/configs/formulas.toml`).
- Variables: Akim's `Settings` reads `DEC_APP_DATABASE_URL` (`dec_app`) and
  `DEC_NORMATIVES_DATABASE_URL` (the reader role `dec_normatives_reader`). Egor's
  ingestion keeps `DEC_DATABASE_URL` as the database owner's URL (2026-10-04, replacing
  his 2026-09-29 plan to rename it) and sets the reader's password from
  `DEC_NORMATIVES_READER_PASSWORD`. `dec_app` is not in the compose file:
  backend verify clauses run on a database created by hand on `dec-postgres`.
- Secrets baseline: `pre-commit run --all-files` passes on `develop` since the WP6 merge
  (`bec3d43`; files of Egor's zone in `docs/decisions/secrets-baseline-egor-files.md`).
  `detect-secrets` matches findings by file and line, so moving a listed file or shifting
  a flagged line fails the hook (a line shift rewrites the baseline and exits 3). Who
  refreshes it after a line shift, and on which branch, is asked of Egor in
  `docs/decisions/secrets-baseline-refresh-questions-akim.md`; until he answers, the
  baseline changes only on a feature or fix branch. Merging WP9 adds test files with
  placeholder passwords that the baseline does not list, so the scan of WP6 task 4.5 is
  re-run on the WP9 branch after `git merge develop`. `pre-commit install` is not done on
  Akim's machine yet (decided 2026-10-04 to install it later).
- Review follow-ups (the 18 minor items of
  `docs/decisions/calculation-core-contract-readiness.md` sections 12-14): done on
  `fix/calculation-engine/backend` (WP2 tasks 9.1-9.10, WP8 tasks 7.1-7.2), `tester` GO,
  `orchestrator` review, merged into `develop` in `1027627` on 2026-10-03 (section 16;
  `check.sh` 672 passed, coverage 100%). Item 3 was fixed earlier (`cc70f7d`). Still
  open on `develop`: item 6 (table entries carry no selector values), fixed by
  `normative-catalog-backend` tasks 5.1a-5.1b on its feature branch, not merged yet;
  item 9 (per-column length limits of the title block), a follow-up in
  `calculation-core-contract` `tasks.md` "Dependencies".
- Input form: the `web-platform` "Calculation input form" requirement (WP1 delta: fields
  from the type's contract, nothing hard-coded) has no task in any change yet.
  `GET /calculation-types` already lists each input's allowed `units` for it (WP8 task
  5.2a); the form needs its own change in the `frontend-app` feature.
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
- One-time setup per machine, before the commands below: `python -m venv backend/.venv`,
  `backend/.venv/bin/pip install -r backend/requirements-dev.txt`, `npm ci` in
  `frontend/`, and `backend/.venv/bin/pre-commit install` at the repository root, so the
  pre-commit hooks run on every `git commit` (WP6 task 6.2).
- Backend: `backend/check.sh` (`ruff`, `mypy`, `pytest` with branch coverage >= 95% on
  `app`, and `lint-imports` with the layer contracts of `backend-layered-architecture`
  decision 2 in `backend/pyproject.toml`), using `backend/.venv`. Tests
  marked `postgres` (migrations, JSON round-trip, latency) run only with
  `DEC_TEST_APP_DATABASE_URL` set to a hand-made database on
  `dec-postgres` (`dec_app_wp8_test` exists), and are skipped otherwise:
  `docker start dec-postgres`, then from `backend/`
  `DEC_TEST_APP_DATABASE_URL=postgresql://dec:<password>@localhost:5433/dec_app_wp8_test pytest -m postgres`.
  The catalog module (`test_normatives_postgres.py`, WP9 branch) also needs
  `DEC_TEST_NORMATIVES_DATABASE_URL` pointing at `dec_normatives_test` (made by hand on
  `dec-postgres`; the fixture refuses a database whose name does not end in `_test`).
  Do not start `infra/docker-compose.yml` instead: its project name differs from the one
  that created `dec-postgres`, so the container name would clash.
- Backend server: `uvicorn app.main:app --host 127.0.0.1` from `backend/`, with
  `DEC_APP_DATABASE_URL` pointing at a migrated `dec_app` (`alembic upgrade head`);
  `DEC_CORS_ORIGINS` (comma-separated) and `DEC_PARAMS_ROOT` are optional. On the WP9
  branch `DEC_NORMATIVES_DATABASE_URL` (the reader role) serves the catalog; without it
  the app still starts, and the catalog paths answer `503`.
- Frontend: `frontend/check.sh` (`eslint`, `tsc -b`, `vitest run --coverage`).
- Pre-commit: `pre-commit run --all-files` (`detect-secrets`, and a hook that
  `.env.example` lists every backend settings variable; see "Secrets baseline" above).
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
