# Readiness review: `dev-tooling-followups`

- Date: 2026-10-04
- Change: `openspec/changes/dev-tooling-followups/`
- Owner: Akim. Feature branch `feature/dev-tooling/backend` (not created yet); documents
  on `develop`. No file of Egor's zone changes.
- Criteria: `AGENTS.md` section 3 (DOR); `openspec/specs/development-process/spec.md`,
  "Planning before implementation".

Russian version: `dev-tooling-followups-readiness-rus.md`.

## Status

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
