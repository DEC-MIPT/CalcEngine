# Open points for Akim, and a proposal for `docs/decisions/` (Egor, 2026-10-05)

- From: Egor (data zone). To: Akim (backend zone) and the PM.
- Status: open for discussion.

Russian version: `egor-open-points-akim-rus.md`.

## 1. Gates that need you

### 1.1 WP9 `normative-catalog-backend` — your review (task 2.7)

The data feature is merged into `develop`, and the `tester` declared GO (recorded in
`docs/decisions/normative-catalog-backend-readiness.md`). The one remaining step of task
2.7 is your review. Note transparently: I merged the feature **before** your review, on
Egor's instruction, so the readiness doc marks the review as "pending". Please acknowledge
there when you are done.

### 1.2 Formulas with Σ / ∏ / equation systems

`latex2sympy2` cannot auto-parse these into the expression tree, and I do not see a way to
wire it in (details and fresh numbers are in
`docs/decisions/formula-autoparse-limits-egor.md`). Proposal: mark such formulas in
`dec_normatives` with a kind (`sum | product | system`) and hand them to the engine as
parameters, not as a parsed tree. The doc lists three concrete questions.

### 1.3 `retarget-mvp-domain` — PM gate (task 1.4)

Egor's tasks (1.3, 3.2, 3.3, 4.1, 4.2) are done and validated. The merge into `Specs` is
blocked on the PM approving: the non-goals list, the domain order, and the B2C limit.

## 2. Proposal: stop the file-per-question sprawl in `docs/decisions/`

The channel has already grown to one file per question/feature and it will only get worse.
Egor proposes to keep `docs/decisions/` as the channel but consolidate by work direction,
not by feature:

| File          | Owner                                         |
| ------------- | --------------------------------------------- |
| `data.md`     | Egor (normative pipeline, catalog, ingestion) |
| `ml.md`       | Egor (NLP/RAG/ML research)                    |
| `infra.md`    | Egor (Docker, dev environment)                |
| `backend.md`  | Akim (engine, backend, report generator)      |
| `frontend.md` | Akim (UI/UX)                                  |
| `product.md`  | PM (scope, pricing, legal)                    |

Each file holds dated sections (one section per decision/question), so a new point appends
a section instead of adding a file. Agree? If yes, Egor will consolidate his existing files
and Akim his.

## Answers (Akim, 2026-10-05)

### 1.1 WP9 review (task 2.7)

Done on 2026-10-05. Verdict: changes requested (blocker B1, majors M1-M3, minors m1-m7),
in `normative-catalog-backend-readiness.md`, section "Akim's review" (and its `-rus`
file). Task 2.7 is unticked again until `fix/normative-catalog/data` passes a second
review.

### 1.2 Formulas with Σ / ∏ / systems

Answered where the questions were asked: `formula-autoparse-limits-egor.md`, section
"Answers" (and its `-rus` file).

### 1.3 `retarget-mvp-domain`: PM gate (task 1.4)

- **No `Specs` branch any more.** Under the branching model of 2026-09-28 a change with no
  code has no branch: its documents are already on `develop`. I reworded task 5.6 of
  `retarget-mvp-domain/tasks.md` accordingly: the second developer's acknowledgement
  instead of a merge into `Specs`.
- **The PM is not the only gate.** Tasks 5.2 (`spec-reviewer`), 5.3
  (`norm-traceability-checker`) and 5.5 (`tester` verdict) are still open.
- **More questions for the PM than the three of task 1.4.** Besides the non-goals list,
  the domain order and the B2C limit, the pilot's scope now raises: the layered base of
  clause 5.6.10 (averaged inputs disclosed in the report, or layers as input), the choice
  of `γc1` by soil kind (without it two of the three WP4 reference examples do not run),
  and a non-integer `φII` with no interpolation rule in table 5.5. The in-scope list you
  filled in task 3.1 (`foundations_shallow_r` only) is confirmed by the PM in the same
  task 1.4. I suggest taking all of it to the PM at once.
- **Who takes it to the PM:** we agree on that separately.

### 2. Consolidating `docs/decisions/`

I agree the channel needs order, but I propose a **folder per direction holding separate
dated files** instead of one file per direction.

Why not one file per direction:

- **Size.** Agents read `docs/decisions/` at the start of every session (AGENTS.md
  section 2). A `backend.md` with every readiness record and question grows to thousands
  of lines that an agent reads whole. Today `ml-model-journal-rus.md` already has 589
  lines and the WP2 readiness record 444.
- **Conflicts.** We both commit to `develop` directly. Two appends at the end of the same
  large file are an almost certain conflict on `pull --ff-only`.
- **Owner and section 7.** An answer goes into the file where the question was asked, so
  Egor writes into "Akim's file" and the other way round, and the owner column loses its
  meaning.
- **Migration.** The point of the scheme is to gather the old files, which means moving
  79 files and fixing 129 references from `openspec/` (archived changes included, which
  are not edited), `CLAUDE.md`, and 16 entries of `.secrets.baseline`.

Proposal:

1. **Folders per direction**, from your table: `data/`, `ml/`, `infra/`, `backend/`,
   `frontend/`, `product/`.
2. **File name** `YYYY-MM-DD-<topic>.md` with its pair `YYYY-MM-DD-<topic>-rus.md`. The
   date is the day the file is created; the file is never renamed, and `git log` shows
   later changes.
3. **Cross-zone topics** (about two thirds of the files): the file goes into the folder
   of whoever writes first (asks the question or keeps the record), and the name ends
   with the addressee, for example `2026-10-05-formula-autoparse-limits-to-akim.md`. A
   change's readiness record goes into the folder of the zone that leads the change. PM
   decisions go into `product/`, recorded by a developer (AGENTS.md section 5).
4. **Answers in the same file**, under `## Answers` (section 7 unchanged). A new question
   on an old topic is a new file that links to the earlier one, which stays a snapshot.
5. **New files only.** The current 79 files stay where they are, at the root of
   `docs/decisions/`. Topics still open in them (for example the WP9 review) go on in the
   same files until they close. No reference and no baseline entry breaks.
6. **No separate change.** The spec `development-process` only requires "a tracked file
   under `docs/decisions/`", which subfolders meet (`.gitignore` already has
   `!docs/decisions/**`), so no spec is touched. Only the example names in AGENTS.md
   section 2 and the rule in section 7 on where a new file is created change. If you
   agree, I make these edits to AGENTS.md in one commit on `develop` and refer to this
   answer; the new layout applies from that commit.

**Separately, outside this decision: the EN/RU pairs drift.** Five files have no pair;
`normative-catalog-backend-readiness.md` had 294 lines against 99 in its `-rus` file, which
lacked both my review and your section 2 (I have translated them now). The new layout does
not solve this. I propose at least the rule "both versions change in the same commit".
