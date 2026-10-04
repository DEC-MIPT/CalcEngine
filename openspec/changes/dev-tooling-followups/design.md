# Design

## Context

See `proposal.md`, "Why". The state this design starts from, on `develop` after the WP6
merge (`bec3d43`) and its archive (`6186bc2`):

- `.pre-commit-config.yaml` runs `detect-secrets` (`rev: v1.5.0`, `--baseline
  .secrets.baseline`) and the local hook `env-example-matches-settings`
  (`language: python`, no `language_version`).
- `.secrets.baseline` (scan with `--exclude-files 'package-lock\.json'`) lists 31
  findings in 21 files. Akim's: `.env.example` (one hash for both `changeme` URLs),
  `backend/alembic.ini` (template comment `user:pass`), `backend/tests/test_api_dependencies.py`,
  `test_api_error_boundary.py`, `test_api_errors.py` (two findings on one line),
  `test_config.py` (three lines), `test_db_session.py`, the Alembic revision ids in the
  two migrations and `test_calculation_result_postgres.py`. Egor's or shared: `README.md`,
  six files in `docs/decisions/`, `infra/docker-compose.yml`, `ml/tests/conftest.py`,
  seven lines of `ml/research/research.ipynb`, `skills-lock.json`.
- `detect-secrets` 1.5 matches by file, hash and line. A line shift makes the hook
  rewrite the line numbers and exit 3; a moved file is a new finding. It honours an
  inline `pragma: allowlist secret` comment and a `pragma: allowlist nextline secret`
  comment on the line before; for a file whose extension it does not know
  (`.env.example`) it tries every comment syntax, `#` included.
- `backend/scripts/check_env_example.py` takes the first of `validation_alias` /
  `alias` among the keyword arguments of `Field(...)`, and falls back to the upper-cased
  field name for anything else; it finds only classes whose base is the bare name
  `BaseSettings`.
- `backend/pyproject.toml`: a "layers" contract with full module names
  (`app.api | app.worker`, ...), two forbidden contracts and the `normatives_pipeline`
  contract; `import-linter` 2.15 supports `containers` and `exhaustive` (only together).
- `backend/check.sh` runs `pytest --cov=app --cov-branch --cov-fail-under=95`;
  `[tool.coverage.run] source = ["app"]`. The script was measured by hand at 97% (only
  the `__main__` guard, run in a subprocess).
- `AGENTS.md` section 2 and the `development-process` requirement "Documents commit
  directly to develop" allow only documents on `develop`; `.secrets.baseline` is code.

## Goals / Non-Goals

**Goals:**

- A document commit on `develop` that shifts a flagged line can be completed without a
  feature branch, while every new finding still gets a hand review.
- Fewer baseline entries that depend on line numbers: Akim's placeholders leave the
  baseline.
- The two backend checks fail loudly instead of passing silently when the code grows in
  a way they do not understand (an unreadable variable name, a package outside every
  layer).

**Non-Goals:**

- Changing how the hook behaves in Egor's files beyond the notebook exclusion; his
  inline markers are his.
- A general settings parser: the check stays a static read of one module.

## Decisions

### 1. The line-only refresh is an exception in the branching rule, not a new document

`AGENTS.md` section 2 ("Documents are committed directly to `develop`") gains one
sentence, and the `development-process` requirement "Documents commit directly to
develop" gains the same exception and two scenarios (see the delta):

> When the pre-commit secret scan only rewrites line numbers in `.secrets.baseline`
> (no new finding), the rewritten baseline is committed together with the change that
> shifted them, on that change's branch, `develop` included; a new finding is handled on
> a feature or fix branch with a hand review, as before.

How a developer knows it is line-only: the hook prints "The baseline file was updated"
with exit 3 and no "Potential secrets" report, and `git diff .secrets.baseline` shows
only `line_number` changes (and `generated_at`, if present).

- **Why:** Egor's answer, part 3 (2026-10-04). The baseline holds no secret, and a
  line-number change carries no review decision.
- **Alternatives:** put `.secrets.baseline` on the "no code" list (too wide: a new
  finding would then skip the branch and the review); refresh it only on a `fix/`
  branch (a branch and a merge for a line number).

### 2. Notebooks are excluded in the hook and in the scan

`.pre-commit-config.yaml` gives the `detect-secrets` hook
`exclude: ^ml/research/.*\.ipynb$`, and the scan command of WP6 task 4.5 gains
`--exclude-files '^ml/research/.*\.ipynb$'`, so the baseline both stops listing the
notebook lines and records the filter in its `filters_used`. Both places are set,
because the hook's `exclude` keeps it from opening the files, while the baseline's
filter keeps a manual `detect-secrets scan` consistent with the hook.

- **Why:** Egor's answer, part 2: the notebooks stay executed, with images in their
  outputs; eight more notebooks arrive from `feature/normative-formula-contract/data`.
  The pattern covers them without listing names.
- **Trade-off:** a literal secret typed into a notebook is not flagged. Covered by the
  rule that credentials go to the environment, never into a notebook (spec delta).
- **Alternative:** clear the outputs (Egor declined), or list each finding (eight more
  notebooks of images would flood the baseline).

### 3. Inline markers for Akim's placeholders; the scan keeps the rest

Each line in Akim's files that holds a placeholder credential or an Alembic revision id
gets `# pragma: allowlist secret` at its end. `.env.example` gets
`# pragma: allowlist nextline secret` on a line of its own before each URL, so the value
line stays a plain `KEY=value` (a `.env` loader or `source` never sees a trailing
comment). `backend/alembic.ini` gets the inline marker on its template comment line.
The Alembic migration headers (`revision`, `down_revision`) get the inline marker too;
`alembic` reads only the values. After marking, the baseline is regenerated with the
command of decision 2 and reviewed: Akim's entries are gone, Egor's and the shared ones
stay.

- **Why:** a marked line no longer depends on line numbers, so most of Akim's churn
  disappears; the marker sits next to the value and says it was reviewed.
- **Alternative:** keep everything in the baseline and rely on decision 1 only (still
  correct, but every test edit rewrites the baseline).

### 4. The settings check resolves names like pydantic, and refuses otherwise

`check_env_example.py`:

- for each field of a settings class, reads `Field(...)` called as `Field` or as
  `<module>.Field`; takes `validation_alias` if it is a string constant, else `alias`
  if it is a string constant, else the upper-cased field name when neither keyword is
  given;
- treats as unreadable, and reports as `config.py: cannot read the variable name of
  <Class>.<field>`: a `validation_alias` or `alias` that is not a string constant
  (`AliasChoices`, `AliasPath`, a name), a `model_config` with `env_prefix` in a settings
  class, and a class that derives from another settings class of the module (its
  inherited fields and prefix would need the parent);
- recognises a settings class by a base named `BaseSettings` or
  `<module>.BaseSettings`;
- exits 2 when any name is unreadable (the commit is blocked, the message names class
  and field), 1 when a readable name is missing from `.env.example`, 0 otherwise.

- **Why:** review item 3 of WP6. A wrong name silently passes the check today.
- **Alternative:** import the module and read pydantic's own resolution. That needs the
  backend's dependencies in the hook's environment and runs application code at commit
  time, which WP6 decision 5 avoided on purpose.

### 5. The layers contract becomes exhaustive over `app`

```toml
[[tool.importlinter.contracts]]
name = "Layers follow backend-layered-architecture design.md decision 2"
type = "layers"
containers = ["app"]
exhaustive = true
exhaustive_ignores = ["main"]
layers = [
    "api | worker",
    "services",
    "engine | parameters | reporting",
    "repositories",
    "db",
    "models | schemas",
    "core",
]
```

`app.main` is the composition root above every layer and stays outside the order. The
engine deny-list contract stays as it is; with the exhaustive layers contract a new
package must first be placed in a layer, and the review that places it also decides
whether `engine` may import it.

- **Why:** review item 4 of WP6.
- **Alternative:** turn the engine contract into an allow-list ("engine imports only
  schemas and core"): `import-linter` has no allow-list contract type; the exhaustive
  layers contract closes the same gap.

### 6. Small fixes

- The local hook gets `language_version: python3.12`, the backend's version
  (`backend/pyproject.toml` `requires-python`).
- `test_import_contracts.py` finds `lint-imports` with `shutil.which` (the venv's `bin/`
  first, then `PATH`) and fails with "lint-imports not found; install
  backend/requirements-dev.txt" when it is missing.
- Coverage: `[tool.coverage.run] source = ["app", "scripts"]`, `check.sh` passes
  `--cov=app --cov=scripts`, and `[tool.coverage.report] exclude_also` drops the
  `if __name__ == "__main__":` guard, which the tests run in a subprocess.

### 7. The C/C++ boundary does not move

This change touches tooling only. The swap boundary stays the pure function
`engine.pipeline.calculate` (`backend-layered-architecture` decision 7); the exhaustive
layers contract keeps `engine` where that decision puts it.

## Non-functional requirements

- **Security:** no new secret, no new place that prints values; the notebook exclusion
  is the one weakening and is bounded by decision 2's rule. The settings check prints
  class and field names only.
- **Performance:** both hooks stay sub-second; no application code runs at commit time.
- **Coverage:** branch coverage of `app` and `backend/scripts/` together >= 95% in
  `check.sh`.
- **Accessibility:** not applicable; no user interface.

## Risks / Trade-offs

- [The exception of decision 1 is misused to slip a new finding into a document commit]
  → The exception is defined by the hook's own output (exit 3 without a report) and by a
  diff of `line_number` only; review on `develop` sees the diff.
- [A marker hides a real secret pasted on a marked line] → Markers sit only on lines
  that hold the reviewed placeholders; a changed value on such a line is still a change
  the reviewer sees in the diff.
- [The stricter settings check blocks a commit for a legitimate `env_prefix`] → The
  message names the field; the fix is to extend the check in the same change that adds
  the prefix, deliberately.
- [Egor's files keep their baseline entries until he marks them] → Decision 1 covers
  their line shifts meanwhile.

## Migration Plan

- Order on the branch: markers and the notebook exclusion, then the regenerated
  baseline, so one scan covers the final files.
- `AGENTS.md` and the base requirement change on `develop` only through this change's
  archive (the delta) and its documents task; until then the old rule applies.
- Rollback: revert the feature's merge commit; the old baseline comes back with it.
