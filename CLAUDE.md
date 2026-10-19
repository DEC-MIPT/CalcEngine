# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-10-19)

- Code on `develop`: Akim's `backend/` — WP5 backend core (`53a4892`), WP6 backend
  tooling, the WP2 calculation engine (`8c001b9`) and report generator (`9642d8d`), the
  WP8 calculation API (`23318c1`: `GET /calculation-types`, `POST /calculations`,
  `GET /calculations/{result_id}`, `POST /calculations/{result_id}/report`, table
  `calculation_result` in `dec_app`, Alembic head `ae350ead9bfd`), the review follow-ups
  (`1027627`), the WP9 catalog backend (`ee94296`: the catalog parameter source,
  `GET /normatives/search`, `GET /normatives/documents/{document_id}`) and the backend part
  of `frontend-app` (`57abe06`: quantity metadata, Word equations in the report), all with
  branch coverage 100%; the pilot type `foundations_shallow_r` with its engineer-set file
  `backend/params/foundations_shallow_r.yaml`; `frontend/` is the React app of
  `frontend-app` (`c252375`, 2026-10-19). Egor's `ml/` (normative pipeline, collector and
  parser under `ml/src/normatives_pipeline/`, with `ml/pyproject.toml`, `ml/configs/`,
  `ml/research/`, `ml/tests/`), his WP9 data feature (`a01b84a`: schema `catalog_read`, its
  views and `search`, the role `dec_normatives_reader`, the pilot's bindings, table 5.5
  headings and coefficients) and its fixes (`c8fc338`), and `infra/docker-compose.yml`
  (PostgreSQL `dec-postgres`, port 5433, single database `dec`). With
  `DEC_NORMATIVES_DATABASE_URL` set, `POST /calculations` for the pilot computes on the
  ingested catalog; without it the catalog paths answer `503`.
- Not merged: Akim's `feature/calculation-verification/backend` (WP4; 166 commits behind
  `develop`) and `feature/report-title-limits/backend` (`report-title-block-limits`,
  `tester` GO at `61fb8d4`; task 3.3, the merge, waits for Akim's word). Egor's
  `fix/formula-extractor/data` (`formula-extractor-fix`, all tasks done),
  `fix/normative-catalog-followup/data` (2026-10-19, follow-ups R5, r6-r10, p2-p5 of
  Akim's third WP9 review) and `feature/normative-collector/data`. Merged branches stay on
  `origin` (delete only on Akim's word).
- Active changes (`openspec list` shows progress). Akim: `calculation-core-contract`
  (WP2; open: task 7.1, archive after WP1), `calculation-api` (WP8; only 6.5 sync and
  archive left, after WP2), `frontend-app` (no WP number; open: task 8.11, archive after
  `calculation-api` and `calculation-core-contract`), `calculation-verification` (WP4;
  open: 2.11 for the engineer, 3.7 blocked on a typical calculation, 6.1-6.2; task 4.1 is
  agreed by Egor, the edits of `tester.md` and the `test-process` skill are not applied
  yet), `report-title-block-limits` (open: 3.3 merge, 3.5 sync),
  `normative-catalog-backend` (WP9, with Egor; open: 7.4, the deferred `orchestrator`
  findings m2 and m3 on `fix/normative-catalog/backend`, and 8.2 sync),
  `backend-layered-architecture` (WP5, all tasks done, not archived) and
  `record-installed-skills-akim`. Led by Egor: `retarget-mvp-domain` (WP1; Akim's review
  tasks are done; open: the PM gate 1.4, 4.3 and 5.2-5.7) and `formula-extractor-fix`
  (complete, not archived). Archived: `normatives-formula-contract` (2026-10-11),
  `normatives-collector` and `normatives-parser` (2026-10-13). Planned: Akim's
  `user-accounts-auth` (test accounts made by an admin command, login, JWT, Argon2id;
  tiers, trial and billing deferred); `norm-source-traceability` (WP3), and Egor's
  `ml-model-storage` and an infra change.
- Next work (Akim): the plan from the pilot's R to the full shallow-foundation calculation
  for the second limit state is in `docs/akim/analysis-sls/08-sls2-action-plan.md`
  (untracked; decisions of 2026-10-18 and 2026-10-19). Its order: CH1
  `interim-normatives-source` (norm data from Akim's interim base; Egor and the PM agreed
  orally on 2026-10-18), phase 1b `foundations-pressure-from-loads` (a new type next to the
  pilot that computes the base pressures from N, M and Q), the WP4 merge, then C2
  structured inputs and the settlement blocks.
- Pilot's first iteration (`frontend-app` design decision 12, while the pilot is shown
  only inside the team): `SHOW_LANGUAGE_SWITCH`, `SHOW_NORM_STATUS`,
  `SHOW_ROUNDING_SOURCE`, `TRACE_NORM_STATUS` and `ACCOUNTABILITY_SECTION` are off; they
  are turned on before the first outside showing.
- Normative catalog contract (Egor, 2026-10-03,
  `docs/decisions/normative-catalog-backend-questions-akim.md`, "Answers"): the
  contract between the zones is the database. Egor owns read-only views and the role
  `dec_normatives_reader` in `dec_normatives`, the binding of a calculation type to its
  norms, and table row/column headings with units; the backend reads only the views,
  through its own repository, with `DEC_NORMATIVES_DATABASE_URL`, and never imports
  `ml/`. On 2026-10-04 (`docs/decisions/normative-catalog-backend-contract-akim.md`,
  "Answers") Egor confirmed WP9 decisions 1-3: schema `catalog_read`, the reader role's
  privileges and the `REVOKE` on `public`, the interim database `dec`, every column of
  the views, the expression tree built at ingestion with no extra nodes. The catalog
  covers only the pilot's R: one numeric selector per table, no categorical selector, no
  interpolation, no sum nodes.
- Formula status: the pipeline writes `status = unverified` and
  `provenance = machine-extracted`, stored per formula and coefficient; the backend
  builds `NormRef.status` from `provenance` and never raises it. `ml/configs/formulas.toml`
  is deleted (`c8fc338`); the pilot's 5.7 comes from `pilot.toml`. There is no user-side
  verification action.
- Edition of the pilot's norm: ingestion stores `document.edition` as
  "2016 с Изм. N 1, 2, 3, 4, 5" (the consolidated text Akim sent Egor on 2026-10-11, the
  same as Akim's copy in `docs/NTD/`, untracked); the status stays `unverified` until WP3
  (`docs/decisions/backend/2026-10-07-pipeline-branch-and-process-to-egor.md`, answer 7).
- Variables: Akim's `Settings` reads `DEC_APP_DATABASE_URL` (`dec_app`) and
  `DEC_NORMATIVES_DATABASE_URL` (the reader role `dec_normatives_reader`). Egor's
  ingestion keeps `DEC_DATABASE_URL` as the database owner's URL and sets the reader's
  password from `DEC_NORMATIVES_READER_PASSWORD`. `dec_app` is not in the compose file:
  backend verify clauses run on a database created by hand on `dec-postgres`.
- Secrets baseline: `pre-commit run --all-files` passes on `develop`. `detect-secrets`
  matches findings by file and line: when the hook only rewrites line numbers or drops
  entries of removed lines (exit 3, "The baseline file was updated", no "Potential
  secrets"), stage the rewritten baseline and commit it with the change that caused it,
  on its branch, `develop` included (`AGENTS.md` section 2, agreed by Egor on
  2026-10-04); a new finding is removed from the file or marked there as a placeholder,
  or the baseline is regenerated with a hand review on a feature or fix branch with the
  two-step command of `dev-tooling-followups` design decision 2. Research notebooks
  `ml/research/**.ipynb` are not scanned; Akim's placeholders carry
  `# pragma: allowlist secret`; the MSW worker's integrity checksum in
  `frontend/public/mockServiceWorker.js` is a reviewed false positive (`69c7b8a`). Egor
  regenerated the baseline twice directly on `develop` (`ff91e03`, `7b267ec`), against
  `AGENTS.md` section 2; to be raised with Egor, together with his merge of
  `feature/normative-pipeline/data` without a review (2026-10-11). The settings hook
  needs `python3.12` and installs pinned `pydantic` and `pydantic-settings` in its own
  environment.
- Review follow-ups of `docs/decisions/calculation-core-contract-readiness.md`
  sections 12-14 are merged (`1027627`); item 6 (table entries carry selector values)
  came with WP9; item 9 (per-column length limits of the title block) is
  `report-title-block-limits`, not merged.
- Branching model (Akim, 2026-09-28; Egor confirmed both rules 2026-09-29,
  `docs/decisions/pipeline-followup-answers-egor-rus.md`): documents (the "no code" list in
  `AGENTS.md`, including this file, `docs/reports/` and the code journals) are committed
  directly to `develop`, after `git fetch --all` and `git pull --ff-only`. Code goes only
  on `feature/<feature>/<zone>` and is merged into `develop` when the whole feature is
  done.
- The base specs in `openspec/specs/` still describe the placeholder domain (beam
  deflection, SP 16.13330) until `retarget-mvp-domain` is archived, and
  `backend-layered-architecture` still names it. The MVP domains are shallow
  foundations, then internal water supply. Build on the active changes, not on the
  placeholder.
- `bootstrap-dev-environment` (WP6) is archived (2026-10-04); its deferred follow-ups
  (review items 3-6, coverage of `backend/scripts/`) are listed in
  `docs/decisions/bootstrap-dev-environment-readiness.md`, sections 7-8, for a later
  tooling change.
- Code journals: `docs/akim/reports/WP<N>-code-journal.md`, or
  `<change>-code-journal.md` for a change with no WP number (untracked).
- Norm editions for the MVP domain come from the team and are `unverified` until
  checked against source texts.

## Who is working

- Both Akim and Egor use Claude Code (Egor switched from Kilo Code in October 2026).
  Akim: frontend/backend, engine, report generator.
  Egor: normative pipeline, NLP/RAG, ML, DevOps (`ml/`, `infra/`).
- Each developer's untracked `CLAUDE.local.md` names the developer of that checkout. If
  it names none, ask which developer is working at the start of the session
  (`AGENTS.md` section 5).
- Akim's session: ask only when a task touches Egor's zones (data, ml, infra).
  Egor's session: stay strictly within `ml/` and `infra/`; ask when a task touches
  Akim's zones (backend, frontend, engine, report generator).

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
  pre-commit hooks run on every `git commit` (WP6 task 6.2). For the end-to-end tests also
  `npx playwright install chromium firefox webkit` in `frontend/` (on Linux, plus the system
  packages that `npx playwright install-deps` names).
- Backend: `backend/check.sh` (`ruff`, `mypy`, `pytest` with branch coverage >= 95% on
  `app`, and `lint-imports` with the layer contracts of `backend-layered-architecture`
  decision 2 in `backend/pyproject.toml`), using `backend/.venv`. Tests
  marked `postgres` (migrations, JSON round-trip, latency) run only with
  `DEC_TEST_APP_DATABASE_URL` set to a hand-made database on
  `dec-postgres` (`dec_app_wp8_test` exists), and are skipped otherwise:
  `docker start dec-postgres`, then from `backend/`
  `DEC_TEST_APP_DATABASE_URL=postgresql://dec:<password>@localhost:5433/dec_app_wp8_test pytest -m postgres`.
  The catalog module (`test_normatives_postgres.py`) also needs
  `DEC_TEST_NORMATIVES_DATABASE_URL` pointing at `dec_normatives_test` (made by hand on
  `dec-postgres`; the fixture refuses a database whose name does not end in `_test`).
  Do not start `infra/docker-compose.yml` instead: its project name differs from the one
  that created `dec-postgres`, so the container name would clash.
- Backend server: `uvicorn app.main:app --host 127.0.0.1` from `backend/`, with
  `DEC_APP_DATABASE_URL` pointing at a migrated `dec_app` (`alembic upgrade head`);
  `DEC_CORS_ORIGINS` (comma-separated) and `DEC_PARAMS_ROOT` are optional.
  `DEC_NORMATIVES_DATABASE_URL` (the reader role) serves the catalog; without it the app
  still starts, and the catalog paths answer `503`.
- Frontend: `frontend/check.sh` (`npm run gen:api:check`, `eslint`, `tsc -b`,
  `vitest run --coverage` with branch coverage >= 95%). From `frontend/`:
  - `npm run dev` — dev server against the real backend at `VITE_API_BASE_URL` (default
    `http://127.0.0.1:8000` in development only); the backend needs `DEC_CORS_ORIGINS` with
    the dev server's origin.
  - `npm run dev:mock` — dev server with MSW answering the API in the browser, no backend.
  - `npm run gen:api` — regenerates `src/api/schema.d.ts` from the backend's OpenAPI
    description (runs `backend/.venv/bin/python`, override with `DEC_PYTHON`); run it after
    any change of the backend's API schemas and commit the file.
  - `npm run test:e2e` — Playwright in Chromium, Firefox and WebKit against its own
    `dev:mock` server on port 5179 (no server reuse); not part of `check.sh`.
- Pre-commit: `pre-commit run --all-files` (`detect-secrets`, and a hook that
  `.env.example` lists every backend settings variable; see "Secrets baseline" above).
- Egor's pipeline (his zone): `python -m normatives_pipeline.search --json "<query>"`
  after `pip install -e "./ml[ml]"`, with `DEC_DATABASE_URL` set, as in `README.md`
  and `docs/decisions/normatives-pilot-usage-akim.md`. Its PostgreSQL is
  `infra/docker-compose.yml`. Ingestion and the pipeline's `pytest` are Egor's to run.

Not set up yet: the frontend build for shipping (`npm run build` exists, but nothing
deploys its output). Do not invent commands for it.

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
