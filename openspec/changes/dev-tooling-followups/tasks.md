# Tasks

Owner: Akim. One feature with code, `dev-tooling` (backend zone and the root tooling
files Akim owns: `.pre-commit-config.yaml`, `.secrets.baseline`, `.env.example`), on
branch `feature/dev-tooling/backend` from `develop`; it is merged into `develop` when
sections 2-4 and 6.1-6.2 are done. Documents (section 1, section 5) are committed
directly to `develop` (`AGENTS.md`, Branching rules). No file of Egor's zone (`ml/`,
`infra/`) is changed. Checkboxes are ticked on `develop` as each subtask is done on the
branch, so `tasks.md` may run ahead of the code on `develop`.

## 1. Spec readiness (spec)

- [ ] 1.1 (spec) Run `openspec validate dev-tooling-followups --strict` and
  `openspec validate --all --strict`; verify both pass
- [ ] 1.2 (spec) Run `spec-reviewer` on this change and resolve its findings until a
  report on the current version lists no blocker and no major finding; verify the
  report is recorded in `docs/decisions/dev-tooling-followups-readiness.md`
- [ ] 1.3 (spec) Run `norm-traceability-checker`; verify its report finds no formula,
  coefficient, limit or tolerance in this change (the 95% coverage threshold and the
  Python version are process and tooling values, not norm values)

## 2. Secrets baseline (backend)

- [ ] 2.1 Exclude the research notebooks from the secret scan (`design.md` decision 2):
  `exclude: ^ml/research/.*\.ipynb$` on the `detect-secrets` hook in
  `.pre-commit-config.yaml`; verify `pre-commit run detect-secrets --files
  ml/research/research.ipynb` reports the file skipped and a staged copy of a fake key
  under `ml/research/probe.ipynb` does not block, while the same key in another path
  does (both probes removed afterwards)
- [ ] 2.2 Mark Akim's placeholders inline (decision 3): `# pragma: allowlist secret` on
  each flagged line of `backend/tests/` (`test_api_dependencies.py`,
  `test_api_error_boundary.py`, `test_api_errors.py`, `test_config.py`,
  `test_db_session.py`, `test_calculation_result_postgres.py`), on the template comment
  of `backend/alembic.ini` and on the `revision`/`down_revision` lines of the two
  migrations; `# pragma: allowlist nextline secret` on its own line before each URL of
  `.env.example`; verify `detect-secrets scan` of these files reports nothing, `ruff`
  and the settings hook still pass, and `alembic heads` still prints `ae350ead9bfd`
- [ ] 2.3 Regenerate `.secrets.baseline` with `detect-secrets scan --exclude-files
  'package-lock\.json' --exclude-files '^ml/research/.*\.ipynb$'` and review every
  finding by hand (file, line, why it is not a secret); verify no path of Akim's zone and
  no `ml/research/` notebook is listed, every listed path exists, `pre-commit run
  --all-files` exits 0, and a staged fake key elsewhere still fails the hook
- [ ] 2.4 Check the line-only refresh of decision 1 on the branch: add a line above a
  flagged line of a file that stays in the baseline (in a scratch copy of the repository,
  not in Egor's file), run the hook; verify it exits 3 with "The baseline file was
  updated" and no "Potential secrets" report, and that `git diff .secrets.baseline` shows
  only `line_number` changes; record the commands and output in the code journal

## 3. Settings check (backend)

- [ ] 3.1 Read variable names like pydantic (decision 4): `validation_alias` before
  `alias`, `Field` and `<module>.Field`, `BaseSettings` and `<module>.BaseSettings`;
  verify tests show the validation alias chosen when both are given, in either keyword
  order, and a `pydantic_settings.BaseSettings` base recognised
- [ ] 3.2 Refuse unreadable names (decision 4): a non-constant `validation_alias` or
  `alias`, `env_prefix` in `model_config`, a class derived from another settings class
  of the module; exit 2 with `config.py: cannot read the variable name of
  <Class>.<field>`; verify one test per case, the exit codes 0, 1 and 2, and that the
  repository's `config.py` still exits 0
- [ ] 3.3 Pin the hook interpreter: `language_version: python3.12` on
  `env-example-matches-settings`; verify `pre-commit run env-example-matches-settings
  --all-files` passes after `pre-commit clean`

## 4. Import contracts and coverage (backend)

- [ ] 4.1 Make the layers contract exhaustive (decision 5): `containers = ["app"]`,
  `exhaustive = true`, `exhaustive_ignores = ["main"]`, layer names relative to `app`;
  verify `lint-imports` keeps every contract on the repository and a new test case with
  a top-level package `app/newpkg/` placed in no layer fails, naming `app.newpkg`
- [ ] 4.2 Find `lint-imports` with `shutil.which` in `test_import_contracts.py` and fail
  with a clear message when it is missing (decision 6); verify the existing cases pass
  and a run with an empty `PATH` and no venv `bin/` reports the message, not
  `FileNotFoundError`
- [ ] 4.3 Put `backend/scripts/` under the coverage gate (decision 6): `--cov=app
  --cov=scripts` in `backend/check.sh`, `source = ["app", "scripts"]`, the `__main__`
  guard in `exclude_also`; verify `check.sh` reports both packages and the total branch
  coverage stays at least 95%

## 5. Documents (spec, directly on `develop`)

- [ ] 5.1 Add the line-only refresh sentence of decision 1 to `AGENTS.md` section 2,
  only after Akim's explicit agreement to that edit (`CLAUDE.md`, "Do not change without
  agreement"); verify the sentence matches decision 1 and the spec delta, and that Egor's
  agreement (`docs/decisions/secrets-baseline-refresh-questions-akim.md`, "Answers",
  part 3) is cited in the commit message
- [ ] 5.2 Fix `CLAUDE.md`: replace "Egor installs it after he answers the baseline
  question" with what Egor's answer says (he marks his two files and adds the `ml/` ->
  `app` check; installing the hook is his own step, not yet stated), and describe the
  line-only refresh rule once 5.1 is in; verify the lines read as stated
- [ ] 5.3 Tell Egor in `docs/decisions/` that the notebook exclusion and the refresh rule
  are in place (a new file, per the team's habit of one file per question round);
  verify the file names the merge commit and the two lines he marks himself

## 6. Close

- [ ] 6.1 Run `backend/check.sh`, `frontend/check.sh`, `pre-commit run --all-files` and
  `openspec validate --all --strict` on the branch after `git merge develop`; verify all
  pass and coverage of `app` and `scripts` is at least 95%
- [ ] 6.2 `tester` GO for `feature/dev-tooling/backend` (UI/UX: N/A, no user interface)
  and the review by Egor or the orchestrator, then the merge into `develop`; verify the
  GO and the review are recorded in `docs/decisions/dev-tooling-followups-readiness.md`
- [ ] 6.3 `spec-keeper` syncs the delta into `openspec/specs/development-process/spec.md`
  and archives the change; verify `openspec validate --all --strict` passes after the
  archive and `pre-commit run --all-files` passes on the moved files

## Dependencies

- None to start: WP6 is merged and archived; Egor's answer is on `develop` (`dc09e57`).
- Order: 2.1 and 2.2 before 2.3 (one scan covers the final files); 2.3 before 2.4;
  section 5.1 before 5.2; 6.1 needs sections 2-4; 6.2 needs 6.1; 6.3 needs 6.2 and 5.1.
- `normative-catalog-backend` (WP9) adds tests with placeholder passwords
  (`test_db_catalog.py`, `test_services_catalog_unavailable.py`, `test_api_normatives.py`)
  that this change's baseline does not list. Whichever of the two features merges
  second marks those lines with `# pragma: allowlist secret` and re-runs the scan of 2.3
  on its branch after `git merge develop`.
- Egor marks `ml/tests/conftest.py` and `infra/docker-compose.yml` on his own branch;
  this change neither waits for it nor edits those files. Until he does, their line
  shifts are covered by the rule of decision 1.

## DOR checklist

- [x] `proposal.md`, `specs/development-process/spec.md`, `design.md`, `tasks.md` exist
- [ ] `openspec validate --strict` passes (task 1.1)
- [ ] A `spec-reviewer` report on the current version lists no blocker and no major
  finding (task 1.2)
- [x] Functional requirements recorded as requirements and scenarios (the delta)
- [x] Non-functional requirements recorded (`design.md`, "Non-functional requirements";
  accessibility not applicable)
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Feature branch named: `feature/dev-tooling/backend`
- [x] Dependencies listed; none blocks the start

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4). The change has
  code, so it uses the normal test and coverage path.
- Spec phase: `openspec validate --all --strict` passes; a `spec-reviewer` report on the
  current version lists no blocker and no major finding.
- Implementation: `backend/check.sh` exits 0 with branch coverage of `app` and `scripts`
  >= 95% and every import contract kept; `frontend/check.sh` exits 0; `pre-commit run
  --all-files` exits 0; the probes of 2.1, 2.3 and 2.4 behave as stated; the delta spec
  matches the implementation; reviewed before merge (6.2).
- NO-GO: validation fails; an open blocker or major review finding; a check fails;
  coverage below 95%; a real secret in the baseline or in a marked line; a file in `ml/`
  or `infra/` changed; `AGENTS.md` edited without Akim's explicit agreement.
- Archive (6.3) happens only after GO.
