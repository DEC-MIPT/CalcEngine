# Proposal

## Why

`bootstrap-dev-environment` (WP6) was archived on 2026-10-04 with follow-ups that no
active change tracks (`docs/decisions/bootstrap-dev-environment-readiness.md`, sections
6-8). The one that hurts is the secrets baseline: `detect-secrets` remembers each allowed
finding by file and line, so an edit that shifts a flagged line fails the pre-commit hook
(exit 3, the hook rewrites `.secrets.baseline`), and the rules allow the baseline to
change only on a feature branch, so a document commit on `develop` cannot carry the
refresh. The pre-commit hook has been installed on Akim's machine since 2026-10-04, and
Egor answered how to handle this on 2026-10-04
(`docs/decisions/secrets-baseline-refresh-questions-akim.md`, "Answers"). The remaining
items are small hardening fixes from the `tester` and `orchestrator` reviews of WP6 that
matter before `user-accounts-auth` adds secrets to the settings and, most likely, a new
backend package.

## What Changes

- **Baseline refresh rule.** A `.secrets.baseline` update that changes only line numbers
  (no new finding) is committed together with the change that shifted them, on whatever
  branch that change is, `develop` included, and it does not make a change a change
  with code. A new finding still needs a hand review and a scan on a feature or fix
  branch. Recorded in `AGENTS.md` sections 2 and 4 and in the `development-process`
  requirements "Documents commit directly to develop" and "Go/No-Go verdict and archive"
  (Egor's answer, part 3; the section 4 sentence follows from it and Egor is told of it
  in the note of task 5.3).
- **Research notebooks out of the scan.** `ml/research/*.ipynb` is excluded from
  `detect-secrets` in `.pre-commit-config.yaml`; the notebooks keep their executed
  outputs (Egor's answer, part 2). Credentials stay out of notebooks by convention.
- **Placeholders marked inline in Akim's files.** Placeholder passwords and Alembic
  revision ids in the backend tests, `backend/alembic.ini` and `.env.example` get
  `pragma: allowlist secret` markers, so they leave the baseline and no longer depend
  on line numbers (Egor's answer, part 1, Akim's side; Egor marks his own files).
- **Settings hook reads names from the library.** `backend/scripts/check_env_example.py`
  loads the settings module and takes each variable name from `pydantic-settings`
  itself, so aliases, prefixes and case sensitivity are read exactly, never guessed; a
  class that sets names in code it does not evaluate, or a module that does not load,
  fails with a message (review item 3; changed on 2026-10-04 from a static reading after
  four review rounds kept finding silent guesses).
- **Every backend package sits in a layer.** The `import-linter` layers contract becomes
  exhaustive over `app`, so a new top-level package fails the backend command until it
  is placed in a layer (review item 4).
- **Hook interpreter pinned.** The local hook declares `language_version: python3.12`
  (review item 5).
- **Clearer failure in the import-contract test.** `test_import_contracts.py` finds
  `lint-imports` on the path and fails with a clear message when it is missing (review
  item 6).
- **Scripts under the coverage gate.** `backend/check.sh` measures `backend/scripts/`
  together with `app` (`tester` finding 2 of WP6).
- **`CLAUDE.md` fixed.** Its line "Egor installs it after he answers the baseline
  question" is Akim's assumption, not Egor's words; it is replaced by what is known.

## Non-goals

- Editing any file of Egor's zone: he marks `ml/tests/conftest.py` and
  `infra/docker-compose.yml` himself and adds the `ml/` -> `app` import check on his
  side (`ml/tests/test_zone_imports.py`, his answer).
- Rewording connection strings in `README.md` or in Egor's files under `docs/decisions/`:
  his answer covers notebooks, not documents; with the refresh rule above a line shift
  in those files no longer blocks anyone.
- The test placeholders that `normative-catalog-backend` (WP9) adds: they are marked or
  scanned when that feature merges, whichever of the two features lands second
  (`tasks.md`, "Dependencies").
- New tooling (another scanner, CI): out of scope.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `development-process`:
  - "Documents commit directly to develop": a line-number-only refresh of
    `.secrets.baseline` travels with the commit that caused it, `develop` included.
  - "Go/No-Go verdict and archive": such a refresh does not make a change a change
    with code.
  - "Backend tooling command": the coverage gate also measures `backend/scripts/`.
  - "Import contract check": a backend package outside every layer fails the check.
  - "Pre-commit secret scan and documented configuration": research notebooks are not
    scanned; names are read from the configuration library; a settings class whose
    names cannot be read from it, or a settings module that does not load, blocks the
    commit and is named.

## Impact

- Code (feature branch `feature/dev-tooling/backend`): `.pre-commit-config.yaml`,
  `.secrets.baseline`, `.env.example`, `backend/check.sh`, `backend/pyproject.toml`,
  `backend/scripts/check_env_example.py`, `backend/alembic.ini`, backend tests with
  placeholders, `backend/tests/test_check_env_example.py`,
  `backend/tests/test_import_contracts.py`.
- Documents (directly on `develop`): `AGENTS.md` sections 2 and 4 (edited only with
  Akim's explicit agreement, `CLAUDE.md` "Do not change without agreement", after GO and
  together with the archive; Egor agreed to the section 2 sentence on 2026-10-04 and is
  told of the section 4 sentence in the note of task 5.3), `CLAUDE.md`, one note to Egor
  in `docs/decisions/`.
- Egor: no file of his zone changes. The notebook exclusion and the refresh rule apply
  to his commits once he installs the hook.
