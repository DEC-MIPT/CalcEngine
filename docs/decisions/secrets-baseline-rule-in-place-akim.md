# Secrets baseline: your answers are in place (2026-10-04)

- Date: 2026-10-04
- From: Akim. To: Egor. For information; one point invites your objection (section 3).
- Context: your answers of 2026-10-04 in `secrets-baseline-refresh-questions-akim.md`
  ("Answers"). They were implemented by the change `dev-tooling-followups` and merged
  into `develop` in `a505352` (feature `feature/dev-tooling/backend`, `tester` GO and
  `orchestrator` review in `dev-tooling-followups-readiness.md`).

Russian version: `secrets-baseline-rule-in-place-akim-rus.md`.

## 1. What is in place

- **Notebooks (your part 2).** `detect-secrets` skips `ml/research/` notebooks: the
  pattern is `^ml/research/.*\.ipynb$` in `.pre-commit-config.yaml` and in the
  baseline's filters. It also covers subfolders of `ml/research/`, slightly wider than
  `ml/research/*.ipynb`, so your eight notebooks are covered wherever they sit under
  `ml/research/`. Nothing in the notebooks changed; credentials stay out of them by your
  convention.
- **Line-only refresh (your part 3).** `AGENTS.md` section 2 now says: when the hook only
  rewrites line numbers in `.secrets.baseline` or drops the entries of removed lines
  (exit 3, "The baseline file was updated", no "Potential secrets" report, a diff of only
  `line_number` values, removed entries and `generated_at`), the rewritten baseline is
  committed with the change that caused it, on that change's branch, `develop` included.
  A new finding is never added to the baseline in such a commit: it is removed from the
  file or marked there as a placeholder, or the baseline is regenerated with a hand
  review on a feature or fix branch.
- **Markers (your part 1, my side).** My placeholders in the backend tests,
  `backend/alembic.ini`, the migrations and `.env.example` carry
  `pragma: allowlist secret` and are no longer in the baseline. The baseline now lists
  12 findings, all the local development password or a content hash; your
  `ml/tests/conftest.py` and `infra/docker-compose.yml` are still in it until you add
  your markers there, as you planned.

## 2. If you install the hook

`backend/.venv/bin/pre-commit install` at the repository root (or your own
`pre-commit`). The settings hook (`.env.example` against the backend settings) now loads
`backend/app/core/config.py` and asks `pydantic-settings` for the variable names, so its
environment is built with `python3.12` and two pinned packages (`pydantic`,
`pydantic-settings`); it needs a `python3.12` on `PATH`. It runs only when `config.py` or
`.env.example` is staged, so it does not touch your commits otherwise.

## 3. A sentence added without asking you separately

Your answer covered the section 2 sentence. A spec review showed that without a second
sentence a spec-only change whose commit carries such a refresh would count as a change
with code and lose its code-free GO path. So `AGENTS.md` section 4 ("No code" means ...)
now also says:

> A refresh of `.secrets.baseline` that adds no finding, committed with a document under
> the exception of section 2, does not make a change a change with code.

I made it without a separate question because it follows from your part 3 and only
narrows the rule for that case. If you object, write it under `## Answers` in this file
and I reopen it.

## 4. WP9

When `feature/normative-catalog/backend` merges, its new tests bring placeholder
passwords that the baseline does not list, and `backend/tests/test_config.py` conflicts
with the markers. The steps are in `normative-catalog-backend` `tasks.md`,
"Dependencies"; that is my branch, nothing for you to do.

## Answers
