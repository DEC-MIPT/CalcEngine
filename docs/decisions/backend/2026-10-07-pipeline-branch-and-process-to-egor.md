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
