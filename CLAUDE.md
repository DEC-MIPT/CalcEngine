# DEC — Claude Code entry point

Claude Code does not read `AGENTS.md` on its own, so it is imported here. `AGENTS.md`
is the single source of truth for process, team, and conventions; this file adds only
what it does not say. Do not restate `AGENTS.md` here.

@AGENTS.md
@agent-docs/domain-constraints.md

## Status (2026-10-11)

- Code on `develop`: Akim's `backend/` — WP5 backend core (`53a4892`), WP6 backend
  tooling, the WP2 calculation engine (`8c001b9`) and report generator (`9642d8d`), and
  the WP8 calculation API (`23318c1`: `GET /calculation-types`, `POST /calculations`,
  `GET /calculations/{result_id}`, `POST /calculations/{result_id}/report`, table
  `calculation_result` in `dec_app`, Alembic head `ae350ead9bfd`), all with branch
  coverage 100%; the pilot type `foundations_shallow_r` with its engineer-set file
  `backend/params/foundations_shallow_r.yaml`; `frontend/` on `develop` is still the WP6
  tooling skeleton (the app is built on `feature/frontend-app/frontend`). Egor's `ml/`
  (normative pipeline and collector under `ml/src/normatives_pipeline/`, with
  `ml/pyproject.toml`, `ml/configs/`, `ml/research/`, `ml/tests/`; moved there
  2026-10-03, `24797f7`), with his WP9 data feature (merged 2026-10-05, `a01b84a`:
  schema `catalog_read`, its views and `search`, the role `dec_normatives_reader`, the
  pilot's bindings, table 5.5 headings and coefficients), and `infra/docker-compose.yml`
  (PostgreSQL `dec-postgres`, port 5433, single database `dec`). The root has no
  `pyproject.toml`, `tests/` or `normatives_pipeline/` any more. `develop` has no
  catalog parameter source yet, so `POST /calculations` for the pilot answers
  `503 parameter_source_unavailable` there until `feature/normative-catalog/backend`
  (WP9) is merged. The review follow-ups are merged too (`1027627`). The three merged
  feature branches and `fix/calculation-engine/backend` still exist on `origin` (delete
  only on Akim's word).
- Active changes (`openspec list` shows progress). Akim: `calculation-core-contract`
  (WP2; engine and report merged; open: the frontend tasks 3.4, 3.5, 5.4, done through
  `frontend-app` section 6 and ticked by its task 8.4, task 7.1, archive after WP1),
  `calculation-api` (WP8; merged, only 6.5 sync and archive left, after WP2),
  `calculation-verification` (WP4; code on `feature/calculation-verification/backend`,
  not merged; open: 2.11, 3.7 blocked on a typical calculation, 6.1-6.2; task 4.1 is
  agreed by Egor on 2026-10-11, the edits of `tester.md` and the `test-process` skill
  are not applied yet), `frontend-app` (created 2026-10-06, no WP number;
  section 2, the quantity metadata, done on `feature/frontend-app/backend`, not merged;
  sections 3-7 in progress on `feature/frontend-app/frontend`, which branches from it;
  ticks on `develop` lag the branch), `backend-layered-architecture` (WP5, all tasks
  done, not archived), `record-installed-skills-akim`, and `normative-catalog-backend`
  (WP9, with Egor; next item). Planned by Akim: `user-accounts-auth` (test accounts made
  by an admin command, login, JWT, Argon2id; tiers, trial and billing deferred). Led by
  Egor, with Akim's parts: `retarget-mvp-domain` (WP1; Akim's review tasks are done;
  open: the PM gate 1.4, 4.3 and 5.2-5.7). Egor: `normatives-collector` and
  `normatives-parser`. The code of both and of `normatives-formula-contract` was on one
  branch, `feature/normative-pipeline/data`; Egor chose on 2026-10-11 that
  `normatives-formula-contract` owns that feature and the other two list it in their
  "Dependencies" (not yet written in their `tasks.md`). On 2026-10-11 Egor merged the
  branch into `develop` (`08dbb85`) and archived `normatives-formula-contract`
  (`c8225fc`, `openspec/changes/archive/2026-10-11-normatives-formula-contract/`, its
  requirements synced into `openspec/specs/normatives-catalog/spec.md`), before
  `fix/normative-catalog/data`, without the package coverage he had promised for the
  verdict after that fix merges, and without a review by Akim or the `orchestrator`
  (`AGENTS.md` section 2, step 7); to be raised with Egor.
  Planned, not created: `norm-source-traceability` (WP3), `ml-model-storage` and an
  infra change (both Egor's).
- WP9 `normative-catalog-backend` (DOR met 2026-10-04): Akim's sections 3-6 are done on
  `feature/normative-catalog/backend` (last code commit `226d44f`: the catalog parameter
  source wired into `create_app`, `GET /normatives/search` and
  `GET /normatives/documents/{document_id}`). Egor's section 2 was merged into `develop`
  after the `tester` GO and before the review. Akim's review (2026-10-05) and his second
  review of `fix/normative-catalog/data` (`950a910`, 2026-10-07) both request changes
  (`docs/decisions/normative-catalog-backend-readiness.md`): the code fixes of B1, M1
  and M2 are right, their tests are not (R1-R4). On 2026-10-11 Egor pushed `3425ec0`,
  `ae23894` and `1d858bc` to `fix/normative-catalog/data` and recorded his fix status
  (readiness doc, "Section 2: Egor's fix status": R1-R4, m1, m3-m7 and M1 in full,
  `formulas.toml` deleted); Akim's re-review of it is next, and task 2.7 stays open
  until it passes. Section 7 (the pilot end to end on ingested data) waits for task 2.7.
  Task 8.1 is done (Egor agreed on 2026-10-11). Egor had agreed that the fix branch
  merges before `feature/normative-pipeline/data`, but merged the pipeline branch
  first; the fix branch is not on `develop` and now conflicts with it (among others in
  `.secrets.baseline` and `catalog_contract.py`), Egor's to resolve. Egor's
  `fix/formula-extractor/data` (2026-10-11) is built on top of `3425ec0`.
- Normative catalog contract (Egor, 2026-10-03,
  `docs/decisions/normative-catalog-backend-questions-akim.md`, "Answers"): the
  contract between the zones is the database. Egor owns read-only views and the role
  `dec_normatives_reader` in `dec_normatives`, the binding of a calculation type to its
  norms, and table row/column headings with units; the backend reads only the views,
  through its own repository, with `DEC_NORMATIVES_DATABASE_URL`, and never imports
  `ml/`. Old WP5 item 9.3 is settled this way. The exact JSON of the expression tree is
  fixed together in `normative-catalog-backend`. On 2026-10-04
  (`docs/decisions/normative-catalog-backend-contract-akim.md`, "Answers") Egor
  confirmed WP9 decisions 1-3 without changes: schema `catalog_read`, the reader role's
  privileges and the `REVOKE` on `public`, the interim database `dec`, every column of
  the views, the expression tree built at ingestion with no extra nodes.
- Formula status: the pipeline writes `status = unverified` and
  `provenance = machine-extracted`, stored per formula and coefficient; the backend
  builds `NormRef.status` from `provenance`. Pilot steps are shown as unverified
  (`docs/decisions/pipeline-open-items-questions-akim.md`, "Answers", 2b). There is no
  user-side verification action. On `develop` `ml/configs/formulas.toml` is still
  there, so its formulas (the pilot's 5.7 among them) are still stored `verified` /
  `human-verified`; the fix is on `fix/normative-catalog/data`, not merged (WP9 review
  M1, `3425ec0`: `formulas.toml` deleted, 5.7 written from `pilot.toml`). The archived
  `normatives-formula-contract` task 1.6 states the new rule (`2d66c3e`, 2026-10-11).
- Edition of the pilot's norm: the ingested СП 22.13330.2016 is the base 2016 text
  without amendments (`docs/decisions/normative-catalog-pilot-coefficients-egor.md`,
  2026-10-07). Akim's copy (`docs/NTD/`, untracked) has amendments 1-5, and formula
  (5.7) is changed by amendment 5 (WP9 review m7); WP9 task 7.1 needs the consolidated
  text. Akim sent it to Egor by Telegram on 2026-10-11, and Egor received it the same day
  ("СП 22.13330.2016 с Изменениями N 1, 2, 3, 4, 5", the same as Akim's copy). On
  `fix/normative-catalog/data` (`ae23894`, m7) ingestion stores `document.edition` as
  "2016 с Изм. N 1, 2, 3, 4, 5"; the status stays `unverified` until WP3
  (`docs/decisions/backend/2026-10-07-pipeline-branch-and-process-to-egor.md`, answer 7).
- Variables: Akim's `Settings` reads `DEC_APP_DATABASE_URL` (`dec_app`) and
  `DEC_NORMATIVES_DATABASE_URL` (the reader role `dec_normatives_reader`). Egor's
  ingestion keeps `DEC_DATABASE_URL` as the database owner's URL (2026-10-04, replacing
  his 2026-09-29 plan to rename it) and sets the reader's password from
  `DEC_NORMATIVES_READER_PASSWORD`. `dec_app` is not in the compose file:
  backend verify clauses run on a database created by hand on `dec-postgres`.
- Secrets baseline: `pre-commit run --all-files` passes on `develop` again (2026-10-11).
  Egor regenerated `.secrets.baseline` twice on `develop`: `ff91e03` added five `ml/`
  findings and changed the scanner's filters, and `7b267ec`, after the pipeline merge,
  dropped those `ml/` entries (now marked `# pragma: allowlist secret` in the files) and
  added a false positive in `skills-lock.json`, reviewed by hand. The baseline no longer
  excludes `package-lock.json` and its notebook pattern lost the `^` anchor. A new
  finding in a `develop` commit and a regeneration outside a feature or fix branch are
  against `AGENTS.md` section 2; to be raised with Egor. The password in
  `tester-verdict.md` was replaced by `<password>` in `2d66c3e`. Research notebooks
  `ml/research/**.ipynb` are not scanned; Akim's placeholders carry
  `# pragma: allowlist secret`. `detect-secrets` matches findings by file and line: when
  the hook only rewrites line numbers or drops entries of removed lines (exit 3, "The
  baseline file was updated", no "Potential secrets"), stage the rewritten baseline and
  commit it with the change that caused it, on its branch, `develop` included
  (`AGENTS.md` section 2, agreed by Egor on 2026-10-04); a new finding is removed from
  the file or marked there as a placeholder, or the baseline is regenerated with a hand
  review on a feature or fix branch with the two-step command of `dev-tooling-followups`
  design decision 2. Merging WP9 brings test placeholders the baseline does not list:
  see `normative-catalog-backend` `tasks.md`, "Dependencies". `pre-commit install` is
  done on Akim's machine (2026-10-04, hook from `backend/.venv`); on Egor's on
  2026-10-11 (his fix status, r4). The settings hook needs `python3.12` and installs
  pinned `pydantic` and `pydantic-settings` in its own environment.
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
  from the type's contract, nothing hard-coded) is implemented by `frontend-app`
  section 5, from `GET /calculation-types` with the quantity metadata of its section 2.
- Branching model (Akim, 2026-09-28; Egor confirmed both rules 2026-09-29,
  `docs/decisions/pipeline-followup-answers-egor-rus.md`): documents (the "no code" list in
  `AGENTS.md`, including this file, `docs/reports/` and the code journals) are committed
  directly to `develop`, after `git fetch --all` and `git pull --ff-only`. Code goes only
  on `feature/<feature>/<zone>` and is merged into `develop` when the whole feature is
  done. Planned Akim features: `backend-core` (WP5), `calculation-engine` (WP2),
  `calculation-verification` (WP4), `report-generator` (WP2 6.3-6.4), `frontend-app`
  (the `frontend-app` change, which also does WP2 3.4, 3.5, 5.4), `dev-environment`
  (rest of WP6). The eight earlier per-change
  branches are merged history.
- The base specs in `openspec/specs/` still describe the placeholder domain (beam
  deflection, SP 16.13330) until `retarget-mvp-domain` is archived, and
  `backend-layered-architecture` still names it. The MVP domains are shallow
  foundations, then internal water supply. Build on the active changes, not on the
  placeholder.
- `dev-tooling-followups` (WP6 follow-ups) is archived (2026-10-04,
  `openspec/changes/archive/2026-10-04-dev-tooling-followups/`): merged in `a505352`
  after the `tester` GO and the `orchestrator` review; the baseline-refresh rule, the
  notebook exclusion, the settings check that asks `pydantic-settings`, the exhaustive
  layers contract and the coverage of `backend/scripts/` are in
  `openspec/specs/development-process/spec.md` and `AGENTS.md` sections 2 and 4.
- `bootstrap-dev-environment` (WP6) is archived (2026-10-04,
  `openspec/changes/archive/2026-10-04-bootstrap-dev-environment/`): merged in `bec3d43`
  after the `tester` GO and the `orchestrator` review; its four tooling requirements are
  in `openspec/specs/development-process/spec.md`. Its deferred follow-ups (review items
  3-6, coverage of `backend/scripts/`, the baseline-refresh question to Egor) are listed
  in `docs/decisions/bootstrap-dev-environment-readiness.md`, sections 7-8, for a later
  tooling change.
- `team-roles-update` (WP7) is archived (2026-09-27,
  `openspec/changes/archive/2026-09-27-team-roles-update/`): the PM role and the
  code-free GO path are in `openspec/specs/development-process/spec.md` and `AGENTS.md`
  section 4, so spec-only changes can get their `tester` verdict.
- Session state for continuing the work: `docs/akim/reports/session-state-2026-09-27.md`
  (untracked); WP code journals in `docs/akim/reports/WP<N>-code-journal.md`.
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
