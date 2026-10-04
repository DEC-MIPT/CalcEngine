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

### 1. The line-only refresh is an exception in the branching rule and the "no code" list

Two places change together:

- `AGENTS.md` section 2 ("Documents are committed directly to `develop`") gains one
  sentence, and the requirement "Documents commit directly to develop" gains the same
  exception and three scenarios (see the delta):

  > When the pre-commit secret scan only rewrites line numbers in `.secrets.baseline`
  > or drops entries of removed lines (no new finding), the rewritten baseline is
  > committed together with the change that caused it, on that change's branch,
  > `develop` included; a new finding is handled on a feature or fix branch with a hand
  > review, as before.

- `AGENTS.md` section 4 ("No code" means ...) and the requirement "Go/No-Go verdict and
  archive" gain one sentence: such a refresh does not make a change a change with code,
  so a spec-only change keeps its code-free GO path.

How a developer knows the refresh qualifies: the hook prints "The baseline file was
updated" with exit 3 and no "Potential secrets" report (in detect-secrets 1.5,
`pre_commit_hook.should_update_baseline` trims the entries of the staged files against a
fresh scan and returns true whenever the collection changed, so a removed allowed line
gives the same exit as a shifted one; task 2.4 confirms it on this repository, and the
scenario "Allowed line removed by a document commit" is revised before the archive if
it does not), and `git diff .secrets.baseline`
shows only changed `line_number` values, removed entries, or a new `generated_at`.

Egor agreed to the section 2 sentence on 2026-10-04; the section 4 sentence follows
from it but is a second edit of a shared file, so task 5.1 asks for his acknowledgement
before it is made (a new file in `docs/decisions/`).

- **Why:** Egor's answer, part 3 (2026-10-04). The baseline holds no secret, and a
  line-number change carries no review decision. Without the section 4 sentence a
  spec-only change that hits the case would lose its code-free GO path (`spec-reviewer`
  finding 1).
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
  convention Egor stated in his answer: credentials go to the environment, never into a
  notebook. It is a convention of his zone, not a checked requirement.
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

- does not treat the class-level configuration as a variable: an annotated or plain
  `model_config`, and any attribute annotated `ClassVar[...]`; `model_config` is still
  inspected for `env_prefix` (below);
- for each other annotated attribute of a settings class, reads `Field(...)` called as
  `Field` or as `<module>.Field`. If `validation_alias` is given, it is the name when it
  is a string constant and the name is unreadable otherwise, whatever `alias` says. If
  only `alias` is given, the same rule applies to it. With neither, the name is the
  upper-cased field name;
- treats as unreadable, and reports as `config.py: cannot read the variable name of
  <Class>.<field>`: a non-constant alias as above (`AliasChoices`, `AliasPath`, a
  name), a `model_config` with `env_prefix` in a settings class (reported for each
  field of that class), and a class that derives from another settings class of the
  module (its inherited fields and prefix would need the parent);
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

`app.main` is the composition root above every layer and stays outside the order. A
top-level module other than `main` falls under the same check (`exhaustive_ignores`
names only `main`). The engine deny-list contract stays as it is. The exhaustive layers
contract does not close the engine gap by itself: a new package placed in a layer below
`engine` (for example next to `core`) is importable by `engine` until the deny-list
names it. So the task that adds a top-level package also reviews the engine contract,
and the test helper that probes contracts can create a package (`app/<name>/__init__.py`)
as well as a module.

- **Why:** review item 4 of WP6.
- **Alternative:** turn the engine contract into an allow-list ("engine imports only
  schemas and core"): `import-linter` 2.15 has no allow-list contract type, so the
  deny-list stays and is reviewed with each new package.

### 6. Small fixes

- The local hook gets `language_version: python3.12`, the backend's version
  (`backend/pyproject.toml` `requires-python`).
- `test_import_contracts.py` finds `lint-imports` through a helper that tries the
  directory of `sys.executable`, then `shutil.which` on `PATH`, and calls `pytest.fail`
  with "lint-imports not found; install backend/requirements-dev.txt" when neither has
  it. Its own test monkeypatches `sys.executable` to a temporary directory and `PATH` to
  an empty one.
- Coverage: `[tool.coverage.run] source = ["app", "scripts"]`, `check.sh` passes
  `--cov=app --cov=scripts`, and `[tool.coverage.report] exclude_also` drops the
  `if __name__ == "__main__":` guard, which the tests run in a subprocess. This
  supersedes the WP6 decision "Gate scope: `app` only"
  (`docs/decisions/bootstrap-dev-environment-readiness.md`, section 6).

### 7. The C/C++ boundary does not move

This change touches tooling only. The swap boundary stays the pure function
`engine.pipeline.calculate` (`backend-layered-architecture` decision 7); the exhaustive
layers contract keeps `engine` where that decision puts it.

## Non-functional requirements

- **Security:** no new secret, no new place that prints values; the notebook exclusion
  is the one weakening and is bounded by decision 2's rule. The settings check prints
  class and field names only.
- **Performance:** no application code runs at commit time; the hooks add no new tool
  run beyond the two that exist.
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
- [Pinning `python3.12` breaks the hook environment on a machine without a
  `python3.12` on `PATH`, Egor's included] → It is the backend's version and
  `backend/.venv` provides it where the setup line of `CLAUDE.md` was followed; an
  unpinned interpreter older than 3.10 would fail anyway on the script's annotations.
  The note to Egor (task 5.4) says it.
- [WP9 adds a top-level `app.*` module or package] → Checked when the second of the two
  features merges (`tasks.md`, "Dependencies"); the exhaustive contract then names it.

## Migration Plan

- Order on the branch: markers and the notebook exclusion, then the regenerated
  baseline, so one scan covers the final files.
- `AGENTS.md` (task 5.2) is edited only after GO and the review (task 6.2), in the same
  session as the archive (task 6.3), so `AGENTS.md` and the base spec change on
  `develop` together. Until then the old rule applies: a line shift in a listed document
  waits for this change or goes through a fix branch.
- Rollback: revert the feature's merge commit; the old baseline comes back with it.
