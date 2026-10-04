# Readiness review: `dev-tooling-followups`

- Date: 2026-10-04
- Change: `openspec/changes/archive/2026-10-04-dev-tooling-followups/` (archived 2026-10-04; was `openspec/changes/dev-tooling-followups/`)
- Owner: Akim. Feature branch `feature/dev-tooling/backend` (created 2026-10-04 from
  `8a5fd74`); documents on `develop`. No file of Egor's zone changes.
- Criteria: `AGENTS.md` section 3 (DOR); `openspec/specs/development-process/spec.md`,
  "Planning before implementation".

Russian version: `dev-tooling-followups-readiness-rus.md`.

## Status

**GO (implementation, `tester`) and review APPROVED WITH FOLLOW-UPS — 2026-10-04** for
`feature/dev-tooling/backend` at `6e08295`, see sections 6-8; the settings check was
reworked after the review and the DOR re-confirmed on the revised delta (section 8).

**READY for DOR — 2026-10-04.** `openspec validate --all --strict` passes (20/20); the
`spec-reviewer` report on the current version lists no blocker and no major finding;
`norm-traceability-checker` passes. Implementation (sections 2-6) has not started.

| DOR condition | State | Evidence |
|---|---|---|
| `proposal.md`, delta, `design.md`, `tasks.md` exist and validate | Met | task 1.1 |
| `spec-reviewer` on the current version: no blocker, no major | Met | pass 2, below |
| Functional and non-functional requirements recorded | Met | the delta; `design.md`, "Non-functional requirements" |
| Tasks one session each, acceptance and Go/No-Go written | Met | `tasks.md` |
| Feature branch named | Met | `feature/dev-tooling/backend` |
| Dependencies listed and satisfied for the start | Met | `tasks.md`, "Dependencies" |

## 1. `openspec validate` (task 1.1)

`openspec validate dev-tooling-followups --strict`: valid. `openspec validate --all
--strict`: 20 passed, 0 failed.

## 2. `spec-reviewer` (task 1.2)

| Pass | Version | Result |
|---|---|---|
| 1 | `aab363a` | NOT READY: 0 blockers, 2 major, 10 minor |
| 2 | working tree after the pass-1 fixes | READY for DOR: 0 blockers, 0 major, 4 minor (all fixed after the pass) |

Pass 1, the two major findings and how they were settled (Akim, 2026-10-04):

1. The baseline exception conflicted with the "no code" list (a document change whose
   commit carries a line-only refresh would lose the code-free GO path). Settled by
   extending the "no code" definition: a MODIFIED "Go/No-Go verdict and archive" and
   `AGENTS.md` section 4 say that such a refresh does not make a change a change with
   code. Egor's answer of 2026-10-04 covers only the section 2 sentence, so task 5.1 asks
   him to acknowledge the section 4 sentence.
2. The `AGENTS.md` edit could land long before the archive, so `AGENTS.md` and the base
   spec would disagree on `develop`. Settled by ordering: the edit (task 5.2) comes after
   GO and the review (6.2), in the same session as the archive (6.3).

Pass-1 minors fixed: exact remaining baseline paths (2.3); probes in a scratch clone and
evidence recorded here (2.1, 2.4); how the missing `lint-imports` case is forced (4.2);
the engine gap stated honestly, `main` exemption and top-level modules (decision 5, 4.1,
the requirement); `model_config`, `ClassVar` and alias precedence (decision 4, 3.1-3.2,
scenarios); removed allowed lines (requirement and scenario); an unmeasured
"sub-second" claim removed; the `python3.12` pin under Risks; the superseded WP6
decision "Gate scope: `app` only" cited (decision 6, 4.3); the notebook-credentials rule
moved from the spec to a convention in the design; the WP9 dependency also checks for a
new top-level `app.*` package or module.

Pass-2 minors fixed: task 5.4 comes after 5.2; the exit 3 on a trimmed entry is cited
from the installed `detect-secrets` 1.5 source and confirmed by task 2.4; `model_config`
is "not treated as a variable, but still inspected for `env_prefix`"; the condition on
Akim's agreement and Egor's acknowledgement moved from the `tester`'s NO-GO list to the
verify of 5.2 and the archive.

## 3. `norm-traceability-checker` (task 1.3)

PASS. No formula, coefficient, limit or tolerance; every number in the change is a
process or tooling value (the 95% coverage gate, Python 3.12, tool versions, exit codes,
an Alembic revision id). No norm document is mentioned.

## 4. Change after DOR (2026-10-04)

Akim decided not to ask Egor for a separate acknowledgement of the section 4 sentence
(former task 5.1): `CLAUDE.md` lets Akim edit `AGENTS.md` on his explicit word, a change
with code needs the `tester` GO and a review (Egor or the orchestrator), not the second
developer's acknowledgement, and the sentence follows from Egor's answer, part 3. Egor
is told in the note of task 5.3, which invites his objection. Section 5 is renumbered:
the `AGENTS.md` edit is now 5.1, the `CLAUDE.md` fix 5.2, the note to Egor 5.3; the
references in section 2 above keep the numbering of the passes. `design.md` decision 1,
`proposal.md`, "Dependencies" and "DOD and Go / No-Go" updated; no requirement or
scenario of the delta changed, so the DOR stands.

## 5. Implementation evidence

On `feature/dev-tooling/backend`, commit `3605eaa` (2026-10-04). Probes ran in a scratch
clone of `develop` with the branch's staged files copied over; the working tree and
Egor's zone were not touched.

Task 2.1 (notebook exclusion):

| Probe | Result |
|---|---|
| `pre-commit run detect-secrets --files ml/research/research.ipynb` | `(no files to check) Skipped` |
| fake AWS key staged in `ml/research/probe.ipynb` | `Skipped`, exit 0 |
| the same key staged in `probe/key.txt` | `Failed`, exit 1 |

Task 2.4 (line-only refresh), on `README.md` line 46 (`dec:dec`):

| Probe | Exit | Hook output | `git diff .secrets.baseline` |
|---|---|---|---|
| insert a line above 46 | 3 | "The baseline file was updated", no "Potential secrets" | `line_number` 46 -> 47, `generated_at` |
| delete line 46 | 3 | same | the `README.md` entry removed, `generated_at` |
| no change | 0 | `Passed` | none |

The first run of the shift probe also added the filter `is_baseline_file` to
`filters_used`, because a baseline made by `scan` alone does not record it. The baseline
is therefore generated in two steps (`scan`, then `scan --baseline`, `design.md`
decision 2, task 2.3); the table shows the runs after that fix.

Task 2.3: 12 files, 12 findings, all reviewed: the local `dec:dec` (`README.md`, eight
files in `docs/decisions/`, `ml/tests/conftest.py`), `POSTGRES_PASSWORD: dec`
(`infra/docker-compose.yml`) and a `computedHash` (`skills-lock.json`). Two of the
`docs/decisions/` files (`secrets-baseline-refresh-questions-akim.md` and `-rus.md`) came
with Egor's answer `dc09e57` after the WP6 baseline, so `pre-commit run --all-files`
fails on `develop` until this feature merges.

Checks on the branch: `backend/check.sh` exit 0 (4 contracts kept, 700 passed, 1 skipped,
branch coverage of `app` and `scripts` 100%); `frontend/check.sh` exit 0;
`pre-commit run --all-files` exit 0; `openspec validate --all --strict` 20/20.

## 6. `tester` verdict (task 6.2, 2026-10-04)

Pass 1 on `a73b107` (`3605eaa` with `develop` merged, task 6.1), in a temporary worktree;
pass 2 on `a73b107` plus the fix, later committed as `6ce32d7`. Both passes **GO**;
UI/UX: N/A (no user interface; `frontend/` identical to `develop`).

| Criterion | Evidence (pass 2 unless noted) | Result |
|---|---|---|
| `backend/check.sh` | exit 0; ruff, mypy clean; 4 contracts kept; 704 passed, 1 skipped; `app` + `scripts` 100% (`check_env_example.py` 107 statements, 48 branches) | pass |
| postgres module (pass 1, migrations touched) | 5 passed on `dec_app_wp8_test` | pass |
| `frontend/check.sh` | exit 0 | pass |
| `pre-commit run --all-files` | exit 0, both hooks | pass |
| 2.1 notebook exclusion (pass 1) | notebook in `ml/research/` skipped; the same fake key in another file, in a notebook outside `ml/research/`, or in a non-notebook inside it fails | pass |
| 2.2 markers (pass 1) | 19 markers; scan of all of `backend/` and `.env.example` empty; `alembic heads` `ae350ead9bfd`; `ml/`, `infra/` unchanged | pass |
| 2.3 baseline (pass 1) | 12 files, 12 findings; 11 hashes are the local `dec`, one a content hash; fresh two-step scan differs only in `generated_at` | pass |
| 2.4 refresh (pass 1) | shift and delete: exit 3, diff only `line_number` / removed entry + `generated_at` | pass |
| 3.1-3.3 settings check | 24 tests; probes of decision 4 incl. exit 0/1/2; repository `config.py` exit 0 under the venv and system Python; hook env `python3.12` | pass |
| 4.1-4.3 contracts and coverage | unplaced `app/newpkg/`, `app/loose.py` break the layers contract; missing-tool message; an uncovered script drops the total to 89.69% and fails the gate | pass |
| `openspec validate --all --strict` | 20/20 | pass |

Pass-1 findings, fixed in `6ce32d7` and confirmed by pass 2:

1. Minor: settings classes were found one level deep only. Now at any depth; every class
   reached through another settings class is unreadable.
2. Minor: `Annotated[str, Field(validation_alias=...)]` was read as the field name, and
   `Field(**...)` was not refused. Now `Field` is read from the value and from
   `Annotated` metadata; two `Field` calls or `Field(**...)` are unreadable.
3. Info: a field with a leading underscore was reported as a variable. Now skipped, as
   pydantic treats it as private.

Left as they are (info, outside decision 4): redundant markers on
`backend/tests/test_db_session.py:10,15`; a field inherited from a plain pydantic model
(`class S(M, BaseSettings)`) is not seen; renamed imports (`Field as F`,
`BaseSettings as BS`) are not recognised.

## 7. Review before merge (task 6.2, 2026-10-04)

Reviewer: the `orchestrator` agent, read-only, on `6ce32d7` merged with `develop`
(`97a2c20`) in a scratch clone. **Outcome: APPROVED WITH FOLLOW-UPS**, no blocker, no
major. The merge is conflict-free; on the merged tree `backend/check.sh`,
`frontend/check.sh`, `pre-commit run --all-files` and `openspec validate --all --strict`
pass, and `pre-commit run --all-files`, failing on `develop` (two lines of Egor's answer
`dc09e57`), passes after the merge. All 12 baseline findings and 19 markers were read on
their lines; none hides a real secret. No file in `ml/` or `infra/` changed.

| # | Severity | Finding | Action |
|---|---|---|---|
| 1 | Minor | The settings check still guessed silently in some cases (`alias_generator`, `case_sensitive`, nested `class Config`, plain-model bases, renamed imports) | Fixed before merge by Akim's decision; after two more rounds the check was reworked to ask `pydantic-settings` (section 8) |
| 2 | Minor | Task 6.1 not ticked before merge | Ticked; 6.2 ticked with the merge |
| 3 | Note | WP9 merge: conflict in `backend/tests/test_config.py`, six new placeholder findings | "Dependencies" of this change extended; reciprocal entry added to `normative-catalog-backend` `tasks.md` (Akim agreed) |
| 4 | Note | Repeated placeholders: every occurrence needs a marker | Kept the markers on `test_db_session.py:10,15`; written into both "Dependencies" |
| 5 | Note | `^ml/research/.*\.ipynb$` also covers subfolders | Accepted (Akim, 2026-10-04); still only notebooks under `ml/research/` |
| 6 | Note | Scenario "Placeholder marked in its file" vs the `nextline` form in `.env.example` | For `spec-keeper` at 6.3 |
| 7 | Note | Stale header line of this record | Fixed |
| 8 | Note | The hook reads only `backend/app/core/config.py` | Recorded among the known limits of decision 4 |

## 8. Settings check reworked after the review (2026-10-04)

The `tester` re-verified each fix of the settings check:

| Pass | Version | Verdict | Main findings |
|---|---|---|---|
| 3 | `6ce32d7` + deny-list fix of review finding 1 | NO-GO | `model_config` built by a call read silently (major); renamed field, nested and aliased `Annotated`, unknown keys, class-body changes (minor) |
| 4 | `6ce32d7` + allow-list rewrite | NO-GO | `Field` from a helper or constant, `settings_customise_sources` (major); decorators, imported aliases, string annotations, shadowed base (minor) |
| 5 | `6ce32d7` + check that asks `pydantic-settings` | **GO** | `sys.exit` in `config.py` and overridden private source methods (minor, fixed in `6e08295`); four accepted limits added to decision 4 |

Decision (Akim, 2026-10-04): a static reading cannot keep up with what Python allows, so
the check loads `config.py` and takes the names from
`EnvSettingsSource._extract_field_info`, with `pydantic` and `pydantic-settings` pinned
in the hook's `additional_dependencies` and a test that the pins equal the installed
versions. The delta's scenarios ("Name changed by the configuration", "Variable name that
cannot be read", "Both aliases given", "Settings configuration attribute"), design
decision 4 (approach, NFRs, risks, accepted limits), the proposal and tasks 3.1-3.2 were
revised accordingly.

`spec-reviewer` on the revised delta: pass 3 NOT READY (1 major: stale NFRs; 8 minor),
all fixed; pass 4 **READY for DOR** (2 minor on the timing figure, fixed: the hook timing
through pre-commit, 0.22 / 0.18 / 0.18 s, is recorded as informational).

Re-run on the committed branch head `6e08295`: `backend/check.sh` exit 0 (4 contracts
kept, 706 passed, 1 skipped, coverage of `app` and `scripts` 100%), `frontend/check.sh`
exit 0, `pre-commit run --all-files` exit 0 (both hooks), `openspec validate --all
--strict` 20/20.
