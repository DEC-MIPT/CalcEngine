# `interim-normatives-source`: readiness record, 2026-10-20

- Owner: Akim (backend and frontend zones). No part of the change is in Egor's zones.
- Russian version: `2026-10-20-interim-normatives-source-readiness-rus.md`.
- Phase 1 (CH1) of Akim's plan for the second-limit-state calculation of shallow foundations:
  a temporary source of norm-given parameters in Akim's zone, read through `ParameterSource`.

## Verdict

**DOR met (2026-10-21).** Spec review criterion met on 2026-10-20; Egor's acknowledgement
(task 1.5) closed the last DOR item, see "DOR met" below.
- `openspec validate interim-normatives-source --strict` passes, and so does
  `openspec validate --all --strict` (21/21).
- The second `spec-reviewer` pass lists no blocker and no major finding.
- `norm-traceability-checker` finds no norm value in the change.

DOR still needs Egor's acknowledgement (task 1.5), asked in
`2026-10-20-interim-normatives-source-ack-to-egor.md`. The verifier's name and the sunset date
(`design.md`, open questions 3 and 4) are needed only before task 7.1, not for DOR: sections
2-6 do not use them, and task 2.5 tests the sunset on a fixture manifest (Akim, 2026-10-20).

## Akim's decisions (2026-10-19)

1. **Verifier's mark.** The verifier's mark is a separate verification record, used as the
   gate of the `strict` profile. `NormRef` stays `unverified` / `machine-extracted` until
   WP3, so `calculation-core-contract` and `normative-catalog-backend` are not changed.
2. **Data format.** YAML records repeat the `catalog_read` rows. The assembly code is shared,
   so both sources yield the same parameter objects.
3. **Where the verification record lives.** It sits next to its value. An edited value falls
   back to `pending` through `value_digest`.
4. **What `strict` does.** It refuses on request: `503 parameter_source_unavailable`, with
   the parameter named in the log. A broken file stops startup.
5. **Sunset.** It is a date plus an event. After the date, startup logs a warning and a
   backend test fails on purpose.
6. **Data scope.** The pilot's R data gate the change (`ex1` in `strict`). The phase-1b data
   form a separate portion on a third feature.
7. **Exception to decision 3 of `backend-layered-architecture`.** It is decided after a trial
   validate. A trial MODIFIED delta of "No hardcoding" passes `openspec validate --strict`,
   but OpenSpec notes "Archive would refuse this delta: backend-architecture: target spec does
   not exist". So the exception is an ADDED requirement that names the four requirements it
   bounds:
   - "No hardcoding" and "Engineer-set parameters stored in YAML" (`backend-layered-architecture`);
   - "Calculation parameter source" (`calculation-api`);
   - "Catalog parameter source" (`normative-catalog-backend`).

   Task 1.4 adds the MODIFIED deltas once those changes are archived.
8. **Agreement.** Egor and the PM agreed orally to the interim base on 2026-10-18 (Akim's
   words). This is recorded as one line in `design.md`, with no question round.

## `spec-reviewer`

| Pass | Blocker | Major | Minor | Result |
|---|---|---|---|---|
| 1 | 0 | 4 | 8 | NOT READY |
| 2 | 0 | 0 | 8 | READY (spec-reviewer criterion) |

Pass 1 majors and their fixes:

- **Major 1: the catalog-only rule was bounded in only one change.** The exception bounded
  only the `backend-architecture` requirements. `calculation-api` "Calculation parameter
  source" and `normative-catalog-backend` "Catalog parameter source" state the same rule.
  - Fixed: all four requirements are named in the exception requirement, the proposal,
    design decision 9 and task 1.4.
  - Two scenarios were added: "Interim mode and a type without a catalog source" and
    "Catalog mode and a type with interim data only".
- **Major 2: task 7.5 sat on the backend branch without gating it.** The phase-1b data were
  on the backend branch but did not gate its merge.
  - Fixed: task 7.5 is a third feature, `feature/interim-normatives-phase1b-data/backend`,
    with its own GO (task 9.3a).
  - The change is archived after all three features are merged.
- **Major 3: "always carries the field" did not hold.** The envelope field was said to be
  always present, while the source description is optional.
  - Fixed: the field is present whenever the source describes itself, which both new sources
    do.
  - A scenario was added: "Source without a description".
- **Major 4: per-type promise versus a global switch.** The text promised that each type
  could move back separately, but the switch is global.
  - Fixed: the selection is stated as global.
  - A per-type choice is a Non-goal and open question 7.

Pass 1 minors, all fixed:
- the "References not raised" scenario is limited to the envelope (the first-iteration
  settings hide the status on the screen and in the report);
- label limits are given in numbers;
- every task's verify clause names its scenarios by title;
- the sunset logic is tested on a fixture manifest, with the real-manifest test in task 7.1;
- record kinds and fields are listed in the spec;
- the report line extends "Result accountability block" when that section is on;
- rules and a scenario were added for `rejected` records;
- citation ranges were unified;
- untracked analysis is no longer cited as rationale.

Pass 2 minors, all fixed:
- the heading of section 7 is reworded;
- tasks 7.2 and 7.3 are split per extraction and per portion (7.2a-c, 7.3a-c);
- portions and a verifier are named for task 7.5;
- the label limits are restated in the spec, and it is said what is measured inside a tree;
- the last untracked citation is removed;
- "a type needs no registration beyond its entries in `PARAMETER_MODELS` and
  `TABLE_SELECTORS`";
- the open questions are reordered;
- the sunset scenario is tied to the fixture test.

## `norm-traceability-checker`

- Blocker 0, major 0, minor 4. No requirement fixes a norm value, and nothing is cited from
  memory.
- The minors were attributions, all fixed:
  - the document is named by the author, edition `unverified`;
  - the claim about which edition the `ex1` textbook follows is attributed to the author and
    marked `unverified`;
  - "identifier given by Akim, checked by the verifier" is repeated at every use of formula
    (5.7).
- The checker notes that editions of СП 22.13330.2016 differ across the repository: "2016" in
  most changes, and "2016 с Изм. N 1, 2, 3, 4, 5" in `frontend-app` `tasks.md`. This change
  takes the edition as printed on the source text, marked `unverified`, and the verifier
  records it in portion P1.

## Open before DOR

| Item | Who |
|---|---|
| ~~Acknowledgement of this change as the second developer, and a look at the record format against `catalog_read` (task 1.5)~~ Done 2026-10-20, `7f394e4` | Egor |
| The verifier's name and the sunset date (`design.md`, open questions 3, 4); needed for task 7.1, not for DOR | Akim |
| The PM's dated record that norm values may be kept in git for the pilot (open question 6, task 9.4) | PM, recorded by Akim |
| ~~Tolerances of `ex1` (open question 1)~~ Answered 2026-10-28, see "Verifier's answers" | verifier |
| ~~Whether amendment 5 changes formula (5.7) (identifier given by Akim) (open question 2)~~ Answered 2026-10-28, see "Verifier's answers" | verifier |

## DOR met (2026-10-21)

- Egor's answers of 2026-10-20 (`2026-10-20-interim-normatives-source-ack-to-egor.md`,
  `7f394e4`): the change, the scoped exception and the rule that `NormRef` status is not
  raised are acknowledged (items 1-3); the record lists mirror the `catalog_read` views one to
  one, with no view change planned before CH3 (4a); the expression tree is the WP9 format,
  unchanged (4b). Task 1.5 and the DOR item "Dependencies satisfied" are checked off.
- Akim's decision before the code (2026-10-21): the profile judges records by group (a
  formula, threshold or check by its parameter, a table value by its parameter and row
  heading, a method bound by its quantity and kind). `rejected` records leave the group; an
  empty group, or one that still holds a record its profile may not use, makes the parameter
  or bound unusable (`503`). Recorded in `design.md`, decision 5.
- Next: the feature branch `feature/interim-normatives/backend` from `develop`, sections 2-4.

## Verifier's answers (portion P1)

- **Open question 2, amendment 5 and formula (5.7)** (task 7.3a; Akim as the verifier,
  2026-10-28): amendment 5 did not change formula (5.7). The formula in the textbook of `ex1`
  (Linovskiy, Yakushkina, 2023) and formula (5.7) of СП 22.13330.2016 with amendments 1-5
  (Akim's copy in `docs/NTD/`, PDF page 36) are identical. So `ex1` is a gate of task 8.1, not
  only a control point. Akim's words: "Изм. № 5 СП формулу 5.7 не меняло. Формулы в методичке
  ex1 и в СП (с учетом изм. № 5) идентичные. Соответственно, ex1 - гейт."
- Context: amendment 5 was approved by order No. 884/пр of 7 December 2023 and is in force from
  2024-01-08 (the foreword, PDF page 2). The mark "(Измененная редакция, Изм. № 5)." after note 6
  of 5.6.7 (PDF page 37) has no binding to a paragraph in either extract
  (`docs/akim/digitization/amendment-marks.md`, untracked). The draft formula gives R =
  206.155708 kPa on the inputs of `ex1` against 206.16 kPa in the textbook; `d_b = 0` there, so
  the `d_b` term is checked by control point CP-R-3, not by `ex1`.
- Akim is both the author of the digitization and the verifier, so this check is not
  independent (`design.md`, Risks).
- **Open question 1, tolerances of `ex1`** (task 7.3a, control point CP-R-2; Akim as the
  verifier, 2026-10-28): `ex1` has one output, R = 206.16 kPa. Its tolerance is ±0.005 kPa,
  absolute; `tolerance_source`: the rounding of the result in the textbook to 0.01 kPa. The
  draft formula gives 206.155708 kPa, within it. Filled in the card
  `foundations-r-linovskiy2023-ex1` of `docs/decisions/reference-examples-foundations.md`.

## Deferred portion D-1 (Akim, 2026-10-27; recorded 2026-10-29)

- Portion D-1 (`docs/verification/interim-normatives-source/D-1.yaml`, 10 items, unsigned)
  holds the checks of six records that the pilot's type file does not hold: the cap
  d_b = 2 m, the h_n allowances, b = √A, note 5 on d_1 > d, formula (5.8) and k = 1.1 for
  characteristics taken from appendix A, with their control points CP-D1-1, CP-K-2, CP-RULE-1
  and CP-RULE-2. Akim took them out of P1 on 2026-10-27, so that P1 checks only the pilot's R
  data (`design.md`, decision 11).
- Why they stay out of tasks 7.3a-7.4: `extractcmp promote` writes verdicts only to records
  of the type file, and these six have no record there. The schema has no rule record, `k`
  has one value with no categorical selector, and the pilot takes `d_1` as an input
  (`docs/akim/digitization/draft-notes.md`, untracked). Bringing them in would need a new
  record kind, a categorical selector and a change of the calculation, which are outside this
  change. The signed P1-1 already notes on `k`: "ветка k = 1,1 вне объёма пилота, выбор —
  категориальный вход (C2)".
- D-1 gates no feature of this change. It moves to the change that adds structured inputs
  (C2); if phase 1b needs formula (5.8), it moves to task 7.5. Recorded in `tasks.md` after
  section 7.
- The check sheets are not rebuilt in `docs/verification/`: `extractcmp build` rewrites every
  sheet there without a signature, which would void the signed P1-1. A later rebuild goes to
  a temporary directory, and only the needed sheet is copied.
