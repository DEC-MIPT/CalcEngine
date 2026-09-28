# Reference examples for `foundations-shallow`: worksheet

- Opened: 2026-09-27
- Engineer who fills it: Akim (decided 2026-09-27; the roadmap had "who this is — data needed").
- Change: `openspec/changes/calculation-verification/` (WP4), requirement "Reference examples"; `design.md` decisions 1, 2, 3, 5; tasks 2.1-2.4, 2.11, 3.7; section 5 "Follow-up".
- Purpose: collect the source, the worked examples, and the engineer's inputs that WP4 needs. Nothing in this file is a norm value; every number comes from the guide or from the engineer, with its source.

## Status

| Item | State | Blocks |
|---|---|---|
| First calculation type(s) of `foundations-shallow` | **Agreed** 2026-09-27 (Egor and the PM, `first-calculation-type-egor-pm.md`, questions 1-2): R, formula 5.7 of СП 22.13330.2016. Egor still has to write it into `foundations-shallow`'s in-scope list (`retarget-mvp-domain` task 3.1) | WP2 task 7.1 (pilot), until task 3.1 is done |
| Coefficient table 5.5 of СП 22.13330.2016 (if the type is R) | **Open**: tables are extracted but not stored in Egor's pipeline; `normatives-formula-contract-review-egor.md`, question 7 | The pilot run of R; WP2 task 7.1 |
| Bibliographic record of the guide | Filled (section 2) | Source citation of every example |
| 3 worked examples per calculation type | Filled (section 3), 3 of 5 found; `tolerance`/`tolerance_kind`/`tolerance_source` still open | WP4 tasks 2.1-2.4; step 5 (first slice) |
| Invariants specific to shallow foundations | Open | WP4 task 2.11 |
| Definition of "typical calculation" | Open | WP4 task 3.7 (30-second latency test) |

## 1. First calculation type

The guide must hold at least 3 worked examples of the type (WP4 decision 1: N = 3; fewer
makes the suite invalid). Propose the type(s) from what the guide actually covers; the
decision goes into `foundations-shallow` "In-scope calculation types" through Egor and the
PM.

Preliminary candidate: the design soil resistance of the base R, formula 5.7, clause
5.6.7 of СП 22.13330.2016 (numbers from Egor's `formulas.toml`, `unverified`). The
formula is in Egor's registry and the SP is ingested; check first that the guide has at
least 3 worked examples of R.

Egor's test `tests/test_formula_code.py` computes R = 143.75 kPa from arbitrary input
values. It checks the formula-to-code binding only; it has no source citation, so it is
not a reference example and must not be admitted to the suite.

- Proposed type(s): design soil resistance of the base, R (formula 5.7, clause 5.6.7,
  СП 22.13330.2016), guide wording "расчётное сопротивление грунта основания".
- Worked examples of it in the guide: checked against two of the three PDFs in
  `docs/NTD/methodical_guides/` (both cite СП 22.13330.2016 directly; the third,
  `OiF.pdf`, cites the older СНиП 2.02.01-83* and is not used for this type). In
  `Calc_OiF_Linkovskiy.pdf` (chosen as the source, section 2): 5 distinct numeric
  applications of formula 5.7, pages 7-8 (Пример 1, trial and refined width), page 16
  (Пример 1, `Rz` check of a weaker underlying layer), pages 21-23 (Пример 2, trial and
  refined width). `Metodrekomendacii_po_RGR_Osnovaniya_i_fundamenty.pdf` has 5 more
  (pages 11-12, 14, 19, 21) and can serve as a second source later if more than 3
  examples are wanted. Well above the required 3.
- Agreed by Egor and the PM on: 2026-09-27. Egor confirmed the candidate in
  `first-calculation-type-egor-pm.md`, question 2, before this count was checked; the
  PM approved verbally to Akim the same day (no repository access yet, recorded on her
  behalf; same file, question 2, "Answer (PM)"). Both questions 1 and 2 are now
  answered by both.

## 2. Source record

One record for the guide. WP4 decision 2: `origin` is `textbook` for every example of this
domain.

| Field | Value |
|---|---|
| Title | Проектирование и расчёт фундаментов мелкого заложения на естественном основании (примеры расчёта): методические указания |
| Authors | С. В. Линовский (канд. техн. наук, доцент), Т. А. Якушкина (ст. преподаватель) |
| Publisher or university | Новосибирский государственный архитектурно-строительный университет (Сибстрин), кафедра инженерной геологии, оснований и фундаментов |
| Year, edition | 2023 (approved by the institute's methodical commission on 2023-06-13) |
| Norm documents the guide calculates with, and their editions | СП 22.13330.2016 "Основания зданий и сооружений" (актуализированная редакция СНиП 2.02.01-83*, изменения 1-4, введена в действие 2017-07-01), per the guide's own bibliography item 2. Egor's pipeline also targets СП 22.13330.2016, so this matches the engine's edition; still `unverified` under `agent-docs/domain-constraints.md` until checked against the primary text (see `docs/decisions/calculation-core-contract-readiness.md`, decision 10 note on the same rule for the report generator). File: `docs/NTD/methodical_guides/Calc_OiF_Linkovskiy.pdf`. |

Note on the file name: the PDF file is named `Calc_OiF_Linkovskiy.pdf`, but the author's
name as printed in the guide is «Линовский» (Linovskiy), not «Линьковский»/«Linkovskiy».
Cite the author as Линовский in any text derived from this record.

WP4 decision 5: a student guide may use an older norm edition than the engine. Record the
edition the guide uses, not the current one.

## 3. Examples

Three examples filled below, all from the source in section 2 (Линовский/Якушкина,
2023). Symbol ids match Egor's registry entry for formula 5.7
(`normatives_pipeline/formulas.toml`, `unverified`). `tolerance`, `tolerance_kind`, and
`tolerance_source` are left for the engineer (Akim) to fill; nothing else here fixes a
norm value beyond what the guide and the registry already state.

Two more examples of the same type are available on pages 11-12, 14, 19, and 21 of
`Metodrekomendacii_po_RGR_Osnovaniya_i_fundamenty.pdf` if a larger suite is wanted later
(same norm document, same formula, not yet turned into cards).

Copy the block below once per additional example.

### foundations-r-linovskiy2023-ex1

| Field | Value |
|---|---|
| `example_id` | `foundations-r-linovskiy2023-ex1` |
| Calculation type | design soil resistance of the base, R (formula 5.7) |
| `origin` | `textbook` |
| Source citation | Линовский, Якушкина, 2023 (section 2), page 8, Пример 1 (refined width, step 4 "Уточним расчетное сопротивление грунта под подошвой") |
| `source_norm_edition` | СП 22.13330.2016, `unverified` |

Inputs:

| Quantity | Symbol in the guide | Symbol id | Value | Unit |
|---|---|---|---|---|
| Coefficient of working conditions (soil) | γc1 | `gamma_c1` | 1.1 | — |
| Coefficient of working conditions (structure) | γc2 | `gamma_c2` | 1.0 | — |
| Coefficient (strength properties from direct tests) | k | `k` | 1 | — |
| Table 5.5 coefficient | Mγ | `M_gamma` | 0.47 | — |
| Depth coefficient (b < 10 m) | kz | `k_z` | 1 | — |
| Footing width (refined) | b | `b` | 2.1 | m |
| Unit weight of soil below the base | γII | `gamma_II` | 18.74 | kN/m³ |
| Table 5.5 coefficient | Mq | `M_q` | 2.89 | — |
| Foundation depth | d1 | `d_1` | 1.5 | m |
| Unit weight of soil above the base | γ'II | `gamma_II_prime` | 18.74 | kN/m³ |
| Basement depth | db | `d_b` | 0 | m |
| Table 5.5 coefficient | Mc | `M_c` | 5.48 | — |
| Specific cohesion | cII | `c_II` | 16 | kPa |

Expected outputs:

| Quantity | Symbol in the guide | Value | Unit | `tolerance` | `tolerance_kind` | `tolerance_source` |
|---|---|---|---|---|---|---|
| Design soil resistance | R | 206.16 | kPa | | `absolute` or `relative` | |

### foundations-r-linovskiy2023-ex1-rz

| Field | Value |
|---|---|
| `example_id` | `foundations-r-linovskiy2023-ex1-rz` |
| Calculation type | design soil resistance of the base, R (formula 5.7), applied to a conditional foundation for the weak-layer check |
| `origin` | `textbook` |
| Source citation | Линовский, Якушкина, 2023 (section 2), page 16, Пример 1 (`Rz` for the weaker underlying layer, formula 5.7 per the guide's own note) |
| `source_norm_edition` | СП 22.13330.2016, `unverified` |

Inputs:

| Quantity | Symbol in the guide | Symbol id | Value | Unit |
|---|---|---|---|---|
| Coefficient of working conditions (soil) | γc1 | `gamma_c1` | 1.4 | — |
| Coefficient of working conditions (structure) | γc2 | `gamma_c2` | 1.0 | — |
| Coefficient (strength properties from direct tests) | k | `k` | 1 | — |
| Table 5.5 coefficient | Mγ | `M_gamma` | 2.28 | — |
| Depth coefficient (b < 10 m) | kz | `k_z` | 1 | — |
| Conditional footing width | b | `b` | 2.85 | m |
| Unit weight of soil below the base | γII | `gamma_II` | 10.6 | kN/m³ |
| Table 5.5 coefficient | Mq | `M_q` | 10.11 | — |
| Depth to the check point | d1 | `d_1` | 3.02 | m |
| Unit weight of soil above the base | γ'II | `gamma_II_prime` | 17.4 | kN/m³ |
| Basement depth | db | `d_b` | 0 | m |
| Table 5.5 coefficient | Mc | `M_c` | 11.25 | — |
| Specific cohesion | cII | `c_II` | 1 | kPa |

Expected outputs:

| Quantity | Symbol in the guide | Value | Unit | `tolerance` | `tolerance_kind` | `tolerance_source` |
|---|---|---|---|---|---|---|
| Design soil resistance at depth (weak-layer check) | Rz | 855.9 | kPa | | `absolute` or `relative` | |

### foundations-r-linovskiy2023-ex2

| Field | Value |
|---|---|
| `example_id` | `foundations-r-linovskiy2023-ex2` |
| Calculation type | design soil resistance of the base, R (formula 5.7) |
| `origin` | `textbook` |
| Source citation | Линовский, Якушкина, 2023 (section 2), page 23, Пример 2 (strip footing, refined width, step 4 "Уточним расчетное сопротивление грунта под подошвой") |
| `source_norm_edition` | СП 22.13330.2016, `unverified` |

Inputs:

| Quantity | Symbol in the guide | Symbol id | Value | Unit |
|---|---|---|---|---|
| Coefficient of working conditions (soil) | γc1 | `gamma_c1` | 1.25 | — |
| Coefficient of working conditions (structure) | γc2 | `gamma_c2` | 1.0 | — |
| Coefficient (strength properties from direct tests) | k | `k` | 1 | — |
| Table 5.5 coefficient | Mγ | `M_gamma` | 0.66 | — |
| Depth coefficient (b < 10 m) | kz | `k_z` | 1 | — |
| Footing width (refined) | b | `b` | 1.8 | m |
| Unit weight of soil below the base | γII | `gamma_II` | 19.33 | kN/m³ |
| Table 5.5 coefficient | Mq | `M_q` | 3.65 | — |
| Reduced foundation depth | d1 | `d_1` | 0.53 | m |
| Unit weight of soil above the base | γ'II | `gamma_II_prime` | 19.33 | kN/m³ |
| Basement depth | db | `d_b` | 2.0 | m |
| Table 5.5 coefficient | Mc | `M_c` | 6.24 | — |
| Specific cohesion | cII | `c_II` | 9 | kPa |

Expected outputs:

| Quantity | Symbol in the guide | Value | Unit | `tolerance` | `tolerance_kind` | `tolerance_source` |
|---|---|---|---|---|---|---|
| Design soil resistance | R | 273.71 | kPa | | `absolute` or `relative` | |

`tolerance_source`: the norm clause that sets the precision (document, edition, clause),
or, where the norm sets none, your reason as the engineer (for example, how many digits
the guide prints). The tolerance is set per quantity; WP4 fixes no number, and the
audit's "<= 0.1%" is not used (decision 3).

## 4. Engineer inputs for the other WP4 tasks

- **Invariants** (task 2.11): statements that hold for every valid input of the type,
  beyond determinism and unit-change consistency, which are shared and already covered.
  For each: identifier, statement, quantities involved, and the valid input range the
  property test may use. None is invented in the specs.
- **Typical calculation** (task 3.7): which calculation, with which inputs, counts as
  typical, and where the 30 seconds are measured. The calculation is asynchronous, so
  say whether the clock covers the engine call only or the whole job from request to
  result.

## 5. Completeness check

An example is admitted only when all of these hold (WP4 scenario "Too few or incomplete
examples"):

- [ ] At least 3 examples per calculation type
- [ ] Every expected output has `tolerance`, `tolerance_kind`, and `tolerance_source`
- [ ] Every input and output has a unit
- [ ] `origin`, the source citation, and `source_norm_edition` are filled
- [ ] No example that you do not trust (an error in the guide, another edition) is admitted
