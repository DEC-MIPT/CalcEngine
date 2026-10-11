# Pipeline branch and process questions (Akim to Egor, 2026-10-07)

- From: Akim (backend zone). To: Egor (data zone).
- Status: open; answers go into this file under `## Answers` (AGENTS.md section 7).
- Russian version: `2026-10-07-pipeline-branch-and-process-to-egor-rus.md`.

These come from reading your commits of 2026-10-07 (`2a95a8b`, `42c7a6d`,
`feature/normative-pipeline/data` at `2f92bad`). The findings on the fix branch are in my
second WP9 review (`normative-catalog-backend-readiness.md`, "Section 2: Akim's second
review"), not repeated here. This is the first file in the new layout of
`docs/decisions/` (AGENTS.md section 7, "Decision files", as you asked on 2026-10-06).

## 1. One branch for three changes

`normatives-formula-contract/tasks.md` now says the three pipeline changes
(`normatives-formula-contract`, `normatives-parser`, `normatives-collector`) share one
branch. AGENTS.md section 2 says a feature is named in the `tasks.md` of the one change it
belongs to, and one feature has exactly one branch. Also, `tasks.md` names the branch
`feature/normatives-pipeline/data`, while the branch on `origin` (and the `tester` verdict)
is `feature/normative-pipeline/data`.

Which do you prefer?

- (a) One change owns the feature `normative-pipeline` and its branch; the other two list
  that feature in their "Dependencies" and are archived after it is merged. No rule
  changes.
- (b) A rule change in AGENTS.md section 2 and `development-process`: a feature may serve
  several changes, each of which names it. This is a process change and needs its own
  OpenSpec change.

I suggest (a). Either way, please fix the branch name in `tasks.md`.

## 2. Task 1.6 of `normatives-formula-contract`

Task 1.6 and the message of `2f92bad` still say "`formulas.toml` entries are
`human-verified`". This is the rule M1 of my first review removed, against your answer 2b
(`pipeline-open-items-questions-akim.md`). Please reword 1.6 to "every formula and
coefficient is stored `unverified` / `machine-extracted`; WP3 raises a status", and keep
M1 when `feature/normative-pipeline/data` is merged after `fix/normative-catalog/data`.

## 3. Coverage in the `tester` verdict

`openspec/changes/normatives-formula-contract/tester-verdict.md` gives 100% for
`symbols.py` and `search.py`, but ">=95%" without a number for the payload functions of
`db.py`, and leaves out the catalog functions of `db.py` as belonging to sibling changes.
Those changes are on the same branch, so the feature's coverage is the coverage of all its
changed code (AGENTS.md section 4). Please add the measured branch coverage of the whole
`normatives_pipeline` package on the branch, with the database tests run (the verdict also
holds the local URL with its password at line 36, one of the m6 findings).

## 4. Root files changed on the pipeline branch

- `.python-version` goes from `3.12.3` to `3.12.12`. It is a root file and applies to
  `backend/` too: my `backend/.venv` and `python3` are 3.12.3, and tools that read the file
  (pyenv, uv) would ask for 3.12.12. Please leave it out of the branch, or tell me why
  3.12.12 is needed, so we agree on one version.
- `skills-lock.json` adds the skill `python-design-patterns`. AGENTS.md section 9 asks that
  a new skill be recorded in an OpenSpec change naming the developer (as
  `record-installed-skills-akim` does for mine). Please record it on your side.

## 5. `.claude/settings.json` in AGENTS.md section 8

Your edit of section 8 says `.claude/settings.json` is "machine-specific, not committed to
the repository". It is committed (`5d9fe07`): it holds the shared project permissions.
Claude Code's own convention puts machine-specific settings in
`.claude/settings.local.json`, which `.gitignore` already ignores (line 39). I propose
section 8 says: "Shared project settings live in `.claude/settings.json` (committed);
machine-specific settings in `.claude/settings.local.json` (ignored)". Agree? Until then,
please do not remove the tracked file.

## 6. "Who is working" in `CLAUDE.md` and AGENTS.md section 5

Your new text says both "Always ask which developer is working at the start of each
session" and "Akim's session: ask only when a task touches Egor's zones". AGENTS.md
section 5 still says the question is skipped when the entry file names the developer
("`CLAUDE.md`: Akim"), which `CLAUDE.md` no longer does. I propose: each developer names
themselves in their untracked `CLAUDE.local.md` (mine does from 2026-10-07); a session
whose `CLAUDE.local.md` names no developer asks. The edits are in the same commit as this
file: AGENTS.md sections 5 and 9, and `CLAUDE.md` "Who is working". Please add a
`CLAUDE.local.md` with your name to your checkout, or say if you want it otherwise.

## 7. The consolidated text of СП 22.13330.2016

You found that the ingested PDF is the base 2016 text without amendments. My copy is the
text with amendments 1-5 (formula (5.7) is marked "Измененная редакция, Изм. № 5"). WP9
task 7.1 should run on it. I can send you the file; where do you want it (it is not
tracked: `docs/normative-base/` is ignored), and when can you re-ingest?

## 8. WP9 task 8.1: your agreement with my notes in WP2, WP5 and WP8

Task 8.1 of `normative-catalog-backend` asks both owners to agree to three notes I wrote
on 2026-10-05 (`5282daa`); the task stays open until you do:

- `backend-layered-architecture/design.md`, decision 2: WP9 settles old item 9.3, and the
  catalog parameter source sits in `services` (`services/catalog_source.py`), not in
  `parameters`, because it also needs the engine's unit conversion and applicability
  check, which `parameters` may not import (WP9 `design.md` decision 5).
- `calculation-api/design.md`, error table: the row `CatalogUnavailableError` | 503 |
  `catalog_unavailable` for the two catalog endpoints (WP9 decisions 4 and 8); and
  `invalid_input` also covers a selecting input inside the method's range that matches
  no row of the catalog's table, located at `["body", "inputs", "<heading symbol>"]`
  (WP9 decision 6). An input outside the range stays a stored refusal (`201`).
- `calculation-core-contract/tasks.md`: minor 6 of the engine review (table entries carry
  no selector values) is fixed by WP9 tasks 5.1a-5.1b, and WP2 task 7.1c is carried out
  as WP9 task 7.1.

None of them changes your zone or the read contract. A line "agree with the 8.1 notes"
under `## Answers` is enough; otherwise say which note to change.

## 9. WP4 task 4.1: the correctness gate in the shared test files

`calculation-verification` (WP4) adds the requirement "Correctness gate for calculation
changes" to `development-process` (its delta
`specs/development-process/spec.md`, marked "Needs Egor review"). For a change with code
that adds or modifies a calculation, the `tester` also checks: the reference suite passes
within tolerance, the invariant tests pass, the metrics "deviation from the references",
"reproducibility rate" and "traceability completeness" are attached to the GO verdict,
and the regression corpus shows no undeclared difference. The 95% branch coverage gate
stays as it is, and a change without calculation code is not affected (your pipeline
included: it computes nothing, as your `normatives-formula-contract` design says).

Task 4.1 asks you to agree before anything is applied, because the files are shared:

- the delta above;
- `.claude/agents/tester.md`, lines 16-19 (the GO rule), and its mirror
  `.kilo/agent/tester.md`, kept identical. Proposed wording:
  - "GO: all tests pass with >= 95% branch coverage and, for a change that adds or
    modifies a calculation, the correctness gate of `development-process` holds."
  - "NO-GO: any test failure, coverage < 95%, or a failed correctness gate."
- the `test-process` skill (`.claude/skills/` and `.kilo/skills/`, lines 21-22): the same
  two lines, and a step "attach the correctness metrics" after "measure branch coverage".

Do you agree, or what would you change? The edits are applied by me in one commit on
`develop` after your answer, and the archive of WP4 syncs the delta.

## Answers (Egor, 2026-10-11)

### 1. One branch for three changes

Option (a). `normatives-formula-contract` owns the feature `normative-pipeline` and its
branch; `normatives-parser` and `normatives-collector` reference it in their Dependencies.
No rule change needed.

Branch name typo fixed in `tasks.md`: `feature/normatives-pipeline/data` →
`feature/normative-pipeline/data`.

### 2. Task 1.6 of `normatives-formula-contract`

Agree. Task 1.6 reworded in `tasks.md` (same commit as this answer): every formula and
coefficient is stored `unverified` / `machine-extracted`; WP3 raises a status. M1 is kept
when `feature/normative-pipeline/data` merges after `fix/normative-catalog/data`.

### 3. Coverage in the `tester` verdict

Agree on both points. Password replaced with a placeholder in `tester-verdict.md`
(same commit). Full branch coverage of the whole `normatives_pipeline` package (including
catalog functions and database tests) will be measured and added to the verdict after
`fix/normative-catalog/data` is merged and the DB tests run cleanly.

### 4. Root files on the pipeline branch

`.python-version` reverted to `3.12.3` on `feature/normative-pipeline/data` (my runtime
is pinned in the untracked `ml/.python-version`). `python-design-patterns` will be
recorded in a `record-installed-skills-egor` OpenSpec change.

### 5. `.claude/settings.json` in AGENTS.md section 8

Agree with your proposed wording.

### 6. `CLAUDE.local.md`

Created locally (untracked). Agree with the proposed session-start logic.

### 7. The consolidated text of СП 22.13330.2016

Send via Telegram. File goes to `docs/normative-base/` (untracked). Re-ingestion the
same day I receive it; `document.edition` updated to name the consolidated text with its
amendment list and date, stays `unverified` until WP3.

### 8. WP9 task 8.1

Agree with all three notes as written.

### 9. WP4 task 4.1: correctness gate

Agree. The pipeline stores normatives and computes nothing, so the correctness gate does
not apply to any change in my zone. The proposed wording for `tester.md`,
`test-process` skill, and `development-process` delta is accepted as written.
