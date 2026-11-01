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

## Recheck protocol review (2026-11-01)

The spec-reviewer found 0 blockers, 0 major findings and 2 minor findings in the
A/C and B/C amendment to design decision 11 and tasks 7.2b/c. Verdict: READY for this
protocol amendment, not feature GO. The minors were the missing execution record for
task 7.1 and obsolete wording that the amendment-5 answer still awaited P1. The actual
checks are below, and decision 11 now points to the recorded answer.

- `openspec validate interim-normatives-source --strict`: passed.
- `openspec validate --all --strict`: 22 passed, 0 failed. The existing unrelated
  `formula-extractor-fix` archive-target notice remains.
- On `feature/interim-normatives/backend` at `f33df61`, using the existing backend
  environment: `python -m pytest tests/test_interim_manifest.py
  tests/test_interim_pilot_data.py tests/test_parameter_source_contract.py -q`:
  30 passed, one Starlette deprecation warning. This confirms the manifest, current
  P1 digests, draft resolution, strict refusal and both source contracts.
- `extractcmp.promote.check_sheet` and `check_committed` returned no errors for
  P1-1 with verifier Akim. Its signed commit remains `e9ad390`, its data promotion
  `f33df61`. Both existing P2-1 answers are preserved; no new verdict was supplied.
- Extraction A contains 19 records, all with a page. Extraction C was produced by
  a separate agent with no inherited conversation, from the PDF and page list only.
  It received no A/B, pilot files, expected results or verifier sheets. The PDF SHA-256
  is `289dc6844340d0177dd01761af4b2adef075d567a16a9685d360b29a79700ecf`, equal to A/B's
  source. Rendering and files-read evidence is retained with C. B's historical
  dependence on A is preserved. This supplies task 7.2b's independent reading.

The working-session artifacts are in
`docs/akim/digitization/recheck-2026-11-01/` (ignored local files, not shared Git evidence):
`extract-c.yaml`, its provenance report, `mapping.json`, `comparison.json`, `compare.py`,
`numeric-proposal.json` and `report.md`. All 159 coefficient cells and 46 selectors match
in A/C and B/C. Three B/C text differences remain: two silty-sand row headings disagree
on the placement of wet sand, and note 1 differs in grammatical number. Akim must resolve
them; matching numbers do not establish matching applicability. Empty `method_bounds`
remains for P3 review. Six numerical diagnostics of 1,000 samples each found no difference,
but their proposed input domain and comparison criterion have no verifier approval yet.
Task 7.2c stays open. No status was promoted and signed sheets were not regenerated.

Task 9.4 is recorded in [the PM record](../product/2026-11-01-interim-normatives-consent.md)
and the local action plan, attributed to Akim's account of oral consent. It describes
feature-branch use and does not claim release on `develop`.

Follow-up spec-reviewer pass on these edits: 0 blockers, 0 major, 0 minor; READY
for the protocol amendment. Task 7.2b is complete, 7.2c remains open. This is not feature GO.

## Backend acceptance attempt (2026-11-01)

Tester verdict: **NO-GO** for `feature/interim-normatives/backend`. The prepared
`backend/tests/test_interim_ex1_acceptance.py` uses real interim files in `strict`,
API creation and stored-result retrieval, the reference card's absolute R tolerance,
the current document digest and one DOCX source line. It fails at the first POST:
`503 parameter_source_unavailable`, because the remaining data is not human-verified.
No xfail, skip, fixture promotion or changed expected result masks this gate.

`backend/check.sh` on `f33df61` plus this uncommitted test: Ruff passed; mypy passed
for 170 files; five layer contracts kept; 1336 passed, 11 skipped, 1 failed; app/scripts
branch coverage 100.00% (3154 statements, 580 branches). The sole failure is the new
acceptance test. The PostgreSQL checks were skipped, not verified.
`pre-commit run --all-files`: both hooks passed. Independent test review found no
blocker/major code finding; UI/UX is N/A for this backend test.

A separate temporary diagnostic using `draft` passed API, persistence and DOCX checks
(1 passed); it did not change the real data and is not strict acceptance. Sandbox
TestClient attempts stalled; the completed full suite ran with approved escalation.
Task 8.1 remains open, and the existing real-data strict-refusal test is retained until
verified data is available. No feature is merged and no GO is granted.

## Numerical comparison protocol approved (2026-11-01)

Akim explicitly approved the proposed input ranges, seed, sample count and B/C
comparison criterion for task 7.2c in this conversation. This resolves the pending
protocol approval in the recheck record above. It is not approval of normative data,
P2/P3 verdicts, the three text differences, or Git operations.

The approved settings are Python `random.Random(20261101)`, restarted per expression,
1,000 uniform samples per expression, variables drawn in sorted-name order, and
`abs(B-C) <= max(1e-10, 1e-12 * max(abs(B), abs(C)))`.

| Inputs | Approved sampling range |
|---|---|
| gamma_c1, gamma_c2, k, k_z | 0.1-2, dimensionless |
| M_gamma, M_q, M_c | 0-20, dimensionless |
| b | 0.1-50 m |
| gamma_II, gamma_II_prime, gamma_cf | 0.1-30 kN/m³ |
| d_1, d_b, h_s, h_cf | 0-10 m |
| c_II | 0-100 kPa |
| z_0 | 0.1-20 m |

For the separate k_z branches, b ranges from 0.1 to the floating-point value immediately
below 10, and from 10 to 50, respectively. Symbols vary independently; these artificial
sampling domains are not normative bounds. The criterion does not change ex1's tolerance.

Reran `backend/.venv/bin/python docs/akim/digitization/recheck-2026-11-01/compare.py`:
all six expressions, 1,000 samples each, have zero differences (maximum absolute
difference 0). Four expression sets belong to R; formula (5.8) and the appendix-A
constant remain D-1 diagnostics, outside the R acceptance gate. A second run was
byte-identical. The approved numerical settings were checked against the preserved
proposal and are unchanged. Ruff passed. A/C and B/C field counts and the three
text differences are unchanged. Task 7.2c remains open for their disposition;
verification statuses and signed sheets are unchanged.

The local recheck directory holds the approved settings in `numeric-proposal.json`,
results in `comparison.json` and the report. Its `before-protocol-approval/` directory
preserves the earlier unapproved artifacts. Approved settings file SHA-256:
`f112f75d2b15cc230e49be11c2aabdfc91d922492750c30c4c41b0331b107a24`.

## Table 5.4 row grouping resolved (2026-11-01)

After viewing versions B/C and the rendered fragment of PDF page 37, Akim stated in
this conversation: «Подтверждаю соответствие версии B». This resolves the two row-heading
differences in task 7.2c in favour of B:

| Record | Accepted B wording | gamma_c1 / gamma_c2 (L/H >= 4) / gamma_c2 (L/H <= 1.5) |
|---|---|---|
| `t54_sands_silty_low_moisture` | Пески пылеватые: маловлажные | 1.25 / 1.0 / 1.2 |
| `t54_sands_silty_wet_saturated` | [Пески пылеватые:] и влажные, насыщенные водой | 1.1 / 1.0 / 1.2 |

Source: СП 22.13330.2016, supplied consolidated PDF with amendments 1-5, table 5.4,
PDF page 37; source identity is recorded in the recheck protocol above. Bracketed text
supplies the common heading, not extra wording from the PDF. The two extractions and
raw comparison results are preserved. The local report records this human disposition
separately from the automatic differences. No backend data or verification sheet was
changed: this decision resolves the row grouping, not every check in those P2 items.
One text difference remains open: note 1, «от деформации оснований» in B versus
«от деформаций оснований» in C. Task 7.2c remains open.

## Table 5.4 note 1 resolved and task 7.2c complete (2026-11-01)

After viewing B/C and the rendered note 1 on PDF page 37, Akim stated in this
conversation: «Подтверждаю версию B». Accepted wording: «от деформации оснований».
Source: СП 22.13330.2016, supplied consolidated PDF with amendments 1-5, table 5.4,
note 1, PDF page 37. This resolves the last of the three B/C text differences.
The decision concerns this phrase, not the whole P2 table-notes verification item.

Task 7.2c is complete: the mapping and automatic report retain matches, differences
and unavailable fields; the approved numerical comparison found no differences;
Akim resolved all three text differences in favour of B. Original A/B/C and raw
comparison results are preserved. No backend record needs a correction from these
dispositions, and no new record was created. P1 and all verification blocks are unchanged.

Repeated on the backend feature worktree: `python -m pytest
 tests/test_interim_manifest.py tests/test_interim_pilot_data.py
 tests/test_parameter_source_contract.py -q`: 30 passed, one existing Starlette warning.
This confirms draft loading, current P1 digests and both source contracts; strict still
refuses the pending records. Missing applicability content and empty `method_bounds`
remain explicitly assigned to human review in P3, not silently counted as matches.
P2/P3 verification, P4 if corrections arise, and strict ex1 acceptance remain open.
No feature GO, commit, merge or archive follows from completing task 7.2c.
