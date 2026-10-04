# `.secrets.baseline`: who refreshes it after a line shift, questions for Egor (2026-10-04)

- Date: 2026-10-04
- From: Akim. To: Egor.
- Context: the `orchestrator` review of WP6 (`bootstrap-dev-environment` task 7.2,
  `docs/decisions/bootstrap-dev-environment-readiness.md`, section 7, finding 1). The
  baseline and the files of your zone it lists are in `secrets-baseline-egor-files.md`.
  Please answer in this file under `## Answers`.

Russian version: `secrets-baseline-refresh-questions-akim-rus.md`.

## 1. The problem

`detect-secrets` 1.5 remembers each allowed finding by file and line number. When a
commit adds or removes a line above a flagged line in one of the 22 listed files, the
pre-commit hook rewrites the line numbers in `.secrets.baseline` itself and exits with
code 3, so the commit fails until the rewritten baseline is staged too. The
`orchestrator` reproduced it by adding one line above `README.md` line 46.

The files where this can happen include `README.md`, `ml/tests/conftest.py`,
`infra/docker-compose.yml`, `ml/research/research.ipynb`, six files in
`docs/decisions/`, `.env.example` and several backend tests.

Under `AGENTS.md` section 2, `.secrets.baseline` is code (it is not on the "no code"
list), so it changes only on a feature or fix branch. A document commit on `develop`,
or a commit on your branch, cannot carry the refreshed baseline without breaking that
rule. The hook runs only after `pre-commit install`, which neither of us has done yet;
it will start to bite once we do.

## 2. Proposal

Three parts; the first two cut how often it happens, the third settles who acts:

1. **Placeholders in code are marked inline.** A placeholder password in a test or a
   config file gets `# pragma: allowlist secret` on its line, so it leaves the baseline
   and no longer depends on line numbers. Each of us does it in our own files (for you:
   `ml/tests/conftest.py`, `infra/docker-compose.yml`; for me: the backend tests and
   `.env.example`).
2. **Documents hold no URL with credentials.** In `README.md` and `docs/decisions/` a
   connection string is written without the `user:password@` form (for example "user
   `dec`, password `dec`, `localhost:5433`, database `dec`"), as I did in
   `bootstrap-dev-environment` tasks 4.3 and 4.6. Notebook outputs: either clear the
   image outputs of `ml/research/research.ipynb` before commit, or exclude that file
   from the scan in `.pre-commit-config.yaml`.
3. **A line-only refresh travels with the commit that caused it.** When the hook only
   moved line numbers (no new finding), the rewritten `.secrets.baseline` is committed
   together with the change that shifted them, on whatever branch that change is,
   `develop` included. This needs one sentence in `AGENTS.md` section 2 (a baseline
   refresh that changes only line numbers counts as part of the document or code change
   that caused it). A new finding still needs a hand review and a scan on a feature or
   fix branch, as in task 4.5.

- **Your side:** agree with parts 1-3, or say which you would change. For part 2, say
  whether you prefer clearing the notebook outputs or excluding the file.

## 3. The import direction `ml/` -> `app`

WP5 decision 2 says `ml/` and `backend/app` have no import relationship in either
direction. WP6 task 5.1 now checks the backend side with `import-linter` (the backend
does not import `normatives_pipeline`). The reverse side (no module of `ml/` imports
`app`) cannot be checked from the backend's tooling, because `import-linter` would need
your package installed in the backend's environment.

- **Your side:** do you add that check on your side (for example an `import-linter`
  forbidden contract in `ml/pyproject.toml`, or a test like the backend's
  `test_zone_imports.py` on the WP9 branch), or should we leave it to review?

## Answers
