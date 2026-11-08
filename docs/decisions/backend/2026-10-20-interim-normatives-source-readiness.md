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

## Verified R data and strict acceptance (2026-11-02)

The backend working tree `feature/interim-normatives/backend` now loads all 146 R
records as `human-verified`. `extractcmp promote` accepted the clean signed sheets
P1-1 (`e9ad390`), P2-1 (`d7e0619`), P2-2 (`aed81c8`), P2-3 (`a1c6bf9`) and
P3-1 (`f53f83c`), each last committed by signer Akim. Signature, mapping and shown
digests passed; all 146 promotion report lines were successful, with no skipped or
incomplete checks. The existing mapping and signed sheets are preserved.

Semantic comparison before replacing the data confirmed exactly 142 changed
`verification` blocks and no other content changes. All four P1 records are identical.
Portion counts: P1-1 4, P2-1 2, P2-2 138, P3-1 2; no pending or rejected R record.
P2-3 control points and notes remain evidence in sheets; rejected CP-T55-4 is not a
mapped data dependency. P3-1 confirms empty `method_bounds` for this pilot.
P4 is not required: promotion changed no values. Sunset remains 2026-12-01.

Current document SHA-256:
`9a19c159848ce71414ba75cb3fceab8d4586e29afacc99e41dfeb71f94ead57a`.
`test_interim_pilot_data.py` checks current verification digests, P1 provenance and
resolution in draft and strict without unchecked/changed warnings. Synthetic pending,
rejected and stale-digest checks are retained. `test_interim_ex1_acceptance.py` passes
real strict data through POST (201), stored-result GET and DOCX: R is within
206.16 +/- 0.005 kPa, verdict pass, source kind interim/profile strict, current digest,
and exactly one report source line. No unchecked or changed warning was captured.

Focused manifest, real-data, source-contract, interim source/data and ex1 tests:
71 passed, one existing Starlette deprecation warning. Sandbox TestClient stalled;
completed runs used approved escalation. Full backend result: Ruff/mypy PASS, five architecture contracts PASS; 1338 passed, 11 skipped, 100.00% app/scripts branch coverage (3154 statements, 580 branches). PostgreSQL integration checks skipped: test database URLs were not configured.
Pre-commit all-files passed both hooks; an explicit check of the untracked ex1 test
passed secret scanning (settings hook N/A for that file). Strict CH1 validation and
whitespace checks passed. Dependencies were not installed; migrations were not run.

Task 9.1 and independent review are handed to tester. Final feature GO still requires
the R data to be committed under the change's gate. No commit, merge, push, archive,
frontend acceptance or phase-1b work is included in this result.

Tester independent review: technical checks PASS, no blocker or major finding; UI/UX N/A (backend data/tests only). Task 9.1 remains open solely for the committed-R-data gate.

## Tester GO for backend, task 9.1 (2026-11-02)

Tester verdict: **GO** for `feature/interim-normatives/backend` at
`82c092d459bcea2c45cf8f1bc30112af075534e6`. The committed-R-data gate from the
preceding entry is satisfied. Sections 2-5, R-data tasks 7.1-7.4 and task 8.1
are complete; task 9.1 is complete.

An independent tester reran `backend/check.sh` on an exact committed snapshot
using the existing environment: Ruff PASS, mypy PASS, five architecture contracts
KEPT; 1338 passed, 11 skipped, one existing Starlette deprecation warning.
App/scripts branch coverage: 100%, all 3154 statements and 580 branches covered.
Both hooks passed in `pre-commit run --all-files`. Real-data strict ex1 through
API, stored-result reading and DOCX passed, as did all 21 source-contract tests.

All five signed sheets passed signature and committed-author checks. Independent
promotion from the parent commit reproduced all 146 records exactly as committed:
only 142 verification blocks changed, values and four P1 records stayed unchanged.
P4 is not required. No blocker or major finding remains in this acceptance scope.
UI/UX: N/A for this backend-only gate.

PostgreSQL tests were skipped: `DEC_TEST_APP_DATABASE_URL`,
`DEC_TEST_NORMATIVES_DATABASE_URL` and `DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL`
were not configured. This GO does not verify live-catalog integration.
Sandbox TestClient stalled; the completed run used approved escalation.
Local logs: `/tmp/ch1-91-tester/backend-check.log`, `pre-commit.log` and
`promotion.log` in the same directory (temporary, not shared artifacts).
Strict CH1 and all-artifact validation passed (22/22); the unrelated
`formula-extractor-fix` archive-target notice remains.

Frontend acceptance (9.2), feature review and merge (9.3), phase-1b data
(7.5/9.3a), specification work (1.4) and archive (9.5) remain separate gates.
No commit, merge or push was performed for task 9.1.

## Frontend acceptance, task 9.2 (2026-11-03)

Tester verdict: **GO** for `feature/interim-normatives/frontend` at
`a8fb64e5678420eceb084f5db325809854de4941`, after **UI/UX CONFIRMED** by
ui-ux-tester. Task 9.2 is complete; this is frontend acceptance only.

An exact committed snapshot passed `frontend/check.sh`: API schema drift check,
ESLint and TypeScript PASS; 496 Vitest tests in 46 files passed, branch coverage
100% (634/634). Relevant backend API/schema paths are identical between this
snapshot and the accepted backend commit `82c092d`.
The unchanged configured Playwright suite passed: 50 passed, 52 intentional skips.
Chromium: 34 passed; Firefox and WebKit: 8 passed and 26 skipped each. Skips are
existing Chromium-only recordings, keyboard/contrast and transition-time checks.

Independent browser UI verification passed 28/28 combinations: catalog, interim
strict/draft, strict/draft refusal, legacy absent/null source; RU/EN at 1280/375 px.
The visible digest has 12 characters; the full 64 characters are in the
accessibility tree. Draft is identified in words, labels are readable, and there
is no horizontal page overflow. Full axe WCAG A/AA checks, including contrast,
found zero violations. Final browser console, page and HTTP errors: zero.
Keyboard trace toggling, visible focus and report navigation passed in all four
language/viewport combinations. Final screenshots were visually inspected.

Browser responses used fixtures. English used the existing provider state because
the public language switch is intentionally hidden. This does not establish live
backend/PostgreSQL integration, normative correctness or physical screen-reader
verification. The backend correctness/strict gate remains the separate 9.1 record.

Initial sandbox runs hit Python spawn EPERM and web-server restrictions; completed
runs used approved escalation. Dependency symlinks in the temporary snapshot caused
font 403s and two initial trace-playback failures. A local copy of existing
dependencies resolved the snapshot issue; the entire unchanged suite and UI matrix
then passed with actual fonts and no HTTP errors. No source edits, dependency
installation or migrations were needed.

Local evidence: `/tmp/dec-ch1-92/frontend-check.log`, `playwright-local-deps.log`,
`ui-probe-final.log`, `ui-evidence/results.json` and screenshots in `ui-evidence/`
under the same directory. These temporary files are not shared artifacts.
Strict OpenSpec validation passed (23/23); the unrelated `formula-extractor-fix`
archive-target notice remains. Review and merge (9.3), phase-1b data (7.5/9.3a),
specification work (1.4) and archive (9.5) remain open. No commit, merge or push
was performed for this acceptance task.

## Review correction committed (2026-11-03)

Backend correction `479172e` makes source page mandatory and positive for all
interim records. Independent re-review APPROVE and tester GO: 1351 passed,
11 PostgreSQL skips (test URLs unset), 100% branch coverage; Ruff/mypy, five
architecture contracts and pre-commit passed. Signed data and public OpenAPI
are unchanged. Evidence and the initial finding are in
[the feature review](2026-11-03-interim-normatives-source-review.md).
Frontend review at `a8fb64e` is APPROVE. Task 9.3 remains open until authorized
integration and both check scripts on develop. No merge or push was performed.

## Feature integration, task 9.3 (2026-11-03)

Task 9.3 is **complete**. Akim explicitly requested push and merge in the
conversation. Reviewed backend `479172e` was published and merged into develop
as `2d0f7db`, followed by reviewed frontend `a8fb64e` as `cbfb634`, without
conflicts. Both feature tips are ancestors of develop; their application trees
match the reviewed versions. The P2 correction remains included.

Both check scripts passed on the actual merged develop, not only a temporary
patch simulation. Backend: Ruff/mypy PASS, five architecture contracts KEPT,
1351 passed, 11 skipped, one existing warning, 100% branch coverage
(3149 statements, 578 branches). PostgreSQL checks skipped because test URLs
were not configured. Frontend: API drift/ESLint/TypeScript PASS, 496 tests in
46 files passed, 100% branch coverage (634/634). Both pre-commit hooks passed;
strict OpenSpec validation passed (23/23). The existing unrelated
formula-extractor-fix archive-target notice remains.

Post-merge logs: `/tmp/dec-ch1-postmerge-backend.log` and
`/tmp/dec-ch1-postmerge-frontend.log` (local temporary evidence).
Live application processes were not restarted. Phase-1b data (7.5/9.3a),
requirement synchronization (1.4) and final sync/archive (9.5) remain open.
This integration does not close the entire CH1 change.

## Phase-1b numerical settings approved and comparison completed (2026-11-03)

Akim approved the proposed software settings in this conversation with the words
“Подтверждаю предложенные настройки”, after being told that the criterion was
proposed by the assistant, not taken from SP22 or an engineering tolerance.
Approval covers the exact proposal (SHA-256 recorded in local numeric-approval.json),
including seed 20261103, 1000 samples for each of three formulas and the criterion
abs(a-b) <= 1e-9 kPa + 1e-12*max(abs(a),abs(b)), with finite results required.

Approved test ranges: N=[1,10000] kN, A=[0.25,100] m2, d=[0,5] m,
M/M_x/M_y=[-10000,10000] kN*m, W/W_x/W_y=[0.01,100] m3,
gamma_mt fixed at 20 kN/m3. These are comparison settings, not normative
applicability limits or adopted engineering tolerances.

Initial A has eight pending target records. Independent image-only B was obtained
from a fresh-context agent using only the same source PDF, pages 42-45 and output
format; it contains 45 pending records. All eight targets are mapped explicitly.
Structural comparison has 115 matches, nine unavailable unit fields and zero
differences; three exact arithmetic normal forms and 93/93 tokens of 5.6.26 agree.
Source-caption ambiguity and unit inferences are preserved. A/B hashes are pinned.

The approved numerical run passed all 3000 samples: 1000 each for (5.11) plus,
(5.11) minus and (5.15). Zero mismatches, maximum absolute difference 0.0 kPa
for every formula. Read-only provenance/result audit found no new gaps. All 53
extraction records remain pending; numerical agreement is not human verification
or a proof of normative correctness.

Local evidence is under docs/akim/digitization/phase1b-2026-11-03/: immutable A/B,
comparison/numeric-approval.json, numeric-results.json, comparison.json,
numeric-run-metadata.json and report.md. Pre-approval reports were preserved.
verification-preparation.md is a neutral human-review queue, not a signed sheet.
Task 7.5 remains open for human verification/P1b-P2b decisions, future-type data
packaging and feature acceptance. No runtime data, API, signed pilot records or
application processes changed. No commit, merge or push was performed.

## Phase-1b verification sheets prepared (2026-11-03)

The sheets in docs/verification/interim-normatives-source/ are ready for human review:
P1b-1 has eight source records; P1b-2 has nine control-point placeholders (two
per formula and three threshold cases). Control inputs, expected results and
engineering tolerances remain unselected. P2b-1 is an empty template to populate
only after actual corrections; it must not be signed while empty. All verdict,
correction, verifier and signature fields are blank. Existing pilot sheets are unchanged.

Local evidence and shown-payload hashes are preserved in the phase-1b working
folder under sheets/items.json. Control payloads and hashes must be updated before
signing once the verifier selects data. These sheets do not yet provide the mapping
to the future runtime YAML. Task 7.5 remains open; no verification status was promoted.


## Storage-format extension approved, planning revision (2026-11-06)

Akim approved extending the interim format in the conversation with the words
"Подтверждаю расширение формата". P1b-1 is signed and committed at `582ea84`;
P1b-2 is signed and committed at `1c580fd`. These signed sheets provide source
and control-point evidence, but do not themselves promote the newly shaped runtime records.

Decision 14 and requirement "Stored applicability and diagram conditions" specify
optional applicability and diagram lists. Exact fractional conditions and separate printed
caption forms are preserved. The original five executable lists stay unchanged. New
records use the existing verifier, digest and strict-warning controls. A registered type
containing any new record refuses parameter resolution in both profiles, including when
verified; an unregistered file is validated and skipped. No execution of these conditions,
new engine mechanism, catalog view or public API schema change is authorized by this plan.

Task 7.5 is decomposed into planning/review (7.5a), format implementation and tests (7.5b),
and a pending future-type file (7.5c). Akim explicitly directed reuse of the existing
`feature/interim-normatives/backend` branch on 2026-11-06; no separate phase-1b branch
is created. This supersedes the original third-branch allocation, as an authorized exception
to one branch per feature. Task 9.3 remains historical acceptance of the original reviewed
features; task 9.3a gates tester GO, review and integration of this continuation. Documents
stay on develop. The file
will preserve eight source records. Promotion requires a checked source-to-runtime mapping
and Git provenance; control points remain separate evidence. P2b-1 is still an empty
correction template and must not be signed while empty.

This entry records the approved scope and revised plan, not a new DOR or GO verdict.
The extension still requires a current spec-reviewer report without blocker or major
findings before implementation. Existing historical acceptance
records remain valid evidence for their original feature revisions. Tasks 7.5, 9.3a, 1.4
and 9.5 remain open. No commit, merge or push is performed by this planning revision.


## Storage-format extension spec review, task 7.5a (2026-11-06)

The spec-reviewer rechecked the current proposal, design, delta and tasks after the
branch-plan revision and digest correction. Verdict: **READY**, 0 blockers, 0 major,
0 minor findings. The resolved major finding concerned record-digest semantics:
content changes outside verification affect both record and document digests;
verification-only changes affect the document digest and leave the record digest unchanged.
The current scenarios and task 7.5b state both cases explicitly.

The review covers reuse of the existing `feature/interim-normatives/backend` branch,
optional storage-only lists, fail-closed resolution for registered extended types,
legacy digest compatibility and preservation of the original task 9.3 acceptance.
Strict validation of this change and all artifacts passed (23/23); the existing unrelated
formula-extractor-fix archive-target information remains. `git diff --check` passed.
Task 7.5a is complete. Task 7.5b requires implementation and tests; task 7.5c requires
the pending runtime file. No source-to-runtime status promotion, tester GO, integration,
commit, merge or push is declared by this review record.

Architect review (`phase1b_architecture`, read-only, 2026-11-06): suitable for
implementation, no architectural blocker. The refusal checks the presence of new records
before rejected-record filtering. Only empty new top-level lists are omitted from the
document digest; all populated new records participate in iteration, verifier checks,
effective status and digests. Existing pilot record digests remain unchanged. No engine,
catalog or public API boundary changes are introduced. The architect edited no files.


## Storage extension and pending data prepared (2026-11-06)

Tasks 7.5b and 7.5c are complete in the uncommitted working tree on the existing
feature/interim-normatives/backend branch, as Akim requested. The storage models
retain exact integer fractions and separate diagram/caption expressions. New records
participate in verification and digests; empty optional lists preserve legacy document
digests. Registered types with stored-only conditions refuse resolution in both profiles.

The future-type file foundations_pressure_from_loads.yaml holds eight pending records:
three formulas, three table values, one applicability condition and one diagram record.
It validates, logs its unregistered type and receives no parameter source. All selected
source fields were compared with the signed P1b-1 payloads. Read-only architect review
approved the implementation with 0 blocker, 0 major and 0 minor findings, and confirmed
all 146 pilot record digests unchanged. Existing pilot data and signed sheets were not edited.

The tester declared GO only for storage extension and pending data preparation. The clean
full backend/check.sh passed: Ruff, mypy (171 files), five import contracts, 1430 tests
passed, 11 skipped, and 100% statement and branch coverage of app/scripts (3178 statements,
584 branches, no missing or partial branches). All three changed application modules have
100% coverage. Seventy-nine new test cases cover the extension; pilot, manifest and ex1
regression tests select the named pilot alongside the unregistered file. UI/UX: N/A,
because there are no UI changes. PostgreSQL/catalog checks skipped for missing test URLs
(three collection modules, one catalog fixture and seven ingested properties); the real
catalog was not verified. One existing Starlette deprecation warning remains.

An initial sandbox TestClient run stalled. The first complete escalated run found an old
manifest-test assumption about a single file; after correcting the assertion for corpus
coexistence, the clean full escalated run passed. OpenSpec selected/all strict validation
and whitespace checks passed. No new calculation method is implemented or accepted.
Task 7.5 remains open for the checked source-to-runtime mapping and status promotion;
9.3a, 1.4 and 9.5 remain open. No commit, merge, push, migration or live-process restart
was performed for this implementation.


## Storage implementation committed (2026-11-06)

Commit 014467f on feature/interim-normatives/backend records the reviewed storage
extension, tests and eight pending records described above. Both commit hooks passed
or skipped with no applicable files. The backend tree is clean. This commit does not
promote data, merge the continuation or close task 7.5. No push was performed.

## Phase-1b promotion and acceptance, task 7.5 (2026-11-08)

Task 7.5 is complete in the backend continuation working tree based on `014467f`.
The existing promotion CLI transferred signed P1b-1 verdicts to all eight runtime
records after independent mapping review. P1b-2 remains separate control evidence.
The portable payloads, mapping, field projections and reproduction recipe are in
[the promotion record](../../verification/interim-normatives-source/P1b-promotion.md).

Independent mapping and final continuation review (`phase1b_review`): **APPROVE**,
0 blockers, 0 major and 0 minor findings. Both signed sheets retain valid signatures
and clean Git provenance. Reproduction yields the exact parsed runtime file;
only verification fields changed. All pilot bytes and 146 record digests are unchanged.
The future type remains unregistered, with no parameter source in either profile.
Its conditions are stored without execution, and reference statuses remain unchanged.

The `tester` declared **GO** for task 7.5 and the format/data continuation before
integration. Full `backend/check.sh` passed: Ruff, mypy (171 files), five import
contracts, 1430 tests passed, 11 skipped and one existing Starlette warning.
Statement and branch coverage of app/scripts is 100% (3178 statements, 584 branches,
no missing or partial branches). Strict ex1 API/DOCX and registered stored-condition
refusal in both profiles pass. The existing promotion suite passed all 12 tests.

The independent acceptance harness passed exact CLI reproduction, all effective
verification statuses, unchanged record digests and the changed document digest.
It also confirmed that modified signatures, changed runtime content, wrong shown
hashes and incomplete mapping fail acceptance. UI/UX: N/A, because no UI changes.

The PostgreSQL/catalog skips cover three collection modules, one PostgreSQL fixture
test and seven ingested-catalog property tests. Their test database URLs are absent;
these runs do not verify real databases or the real catalog.

On an exported integration preview of `develop` plus the final backend changes,
`frontend/check.sh` passed API drift, ESLint, TypeScript and 496 tests in 46 files.
Frontend branch coverage is 100% (634/634); statement coverage is 99.88%.
The preview is a compatibility check, not evidence of a merge or post-merge acceptance.

The initial sandbox backend run stalled in TestClient and was interrupted (exit 130).
The frontend preview initially failed with Python spawn `EPERM`. Clean escalated
runs of both checks passed. Temporary logs and the independent acceptance harness
are under `/tmp/dec-phase1b-evidence/`; the portable inputs and review are prepared
alongside this record. Backend pre-commit checks passed without changing the baseline.

The current artifact recheck (`phase1b_spec_review`) is **READY**, with 0 blockers,
0 major and 0 minor findings after clarifying the recorded tester GO. Requirements
and design are unchanged. Strict selected/all OpenSpec validation passed (23/23);
the existing unrelated formula-extractor-fix archive-target notice remains.
Document links, whitespace checks and pre-commit checks passed, including an explicit
check of the new evidence files. The secrets baseline is unchanged.

No commit, merge, push, migration or live-process restart was performed.
Task 9.3a awaits explicit Git consent and both checks on the actual integrated
`develop`. Task 1.4 still depends on the three named changes being archived;
final specification sync and archive (9.5) remain open.

## Verified runtime data committed (2026-11-08)

Akim explicitly requested the prepared commits. Backend commit `dd0fd15` contains
the reviewed promotion and acceptance-test update described above. The commit hook
passed its secret scan; the settings check had no applicable files. The secrets
baseline is unchanged. This documentation commit records the evidence and task status.
No merge or push is authorized by this request or performed. Task 9.3a still requires
approved integration and checks on the actual integrated `develop`; 1.4 and 9.5 remain open.
