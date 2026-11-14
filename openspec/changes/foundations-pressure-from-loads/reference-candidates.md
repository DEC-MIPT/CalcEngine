# Reference candidates

The recovered manual calculations C, X and XY were checked by Akim, who confirmed
all results in the user conversation on 2026-11-14. Expected values remain the
independent manual derivation below, not outputs of the implementation under test.
Signed P1b formula points are supplementary evidence. NormRef statuses are unchanged.

## Admission gate

Before a candidate is an oracle, record its author/reviewer and date, immutable
source/derivation revision, inputs and intermediate values with units, every expected
output/check, source norm edition, and each tolerance, tolerance kind and tolerance
source. The three admitted examples must exercise central, one-axis and two-axis
loading through the verification runner, API and DOCX. Their admission is a GO gate,
not an extra pre-code DOR condition. C, X and XY are engineer-approved manual references. For each of the ten
expected outputs (R and all pressures), tolerance=0.005 kPa,
tolerance_kind=absolute. The tolerance source is Akim's explicit engineering
decision in the user conversation on 2026-11-14; no additional numerical rationale
was supplied. This tolerance is separate from display rounding. NormRefs keep their recorded unverified status.

## Engineer approval record

- Derivation author: recovered agent arithmetic, independently checked by Akim.
- Reviewer: Akim (Аким); review date: 2026-11-14.
- Cases: C, X, XY; inputs and expected results below confirmed without corrections.
- Approval: “Примеры C, X, XY проверены, результаты подтверждаю.”
- Tolerance decision: “Допуски для R и давлений: 0,005, абсолютные”.
- SHA-256 of the reviewed derivation section (UTF-8, from after the Common inputs
  heading to before Guide discrepancies, including its original whitespace):
  `27258b6d18d3d928f26976e3c9876f78fa4640cba4ff26d83b04035d7dbc55ea`.
- Runner/API/DOCX execution and feature GO remain pending; approval alone does
  not establish successful implementation verification.

## Common inputs

| Input | Value | Unit |
|---|---:|---|
| b | 2 | m |
| d_1 | 1 | m |
| d_b | 0 | m |
| gamma_II | 20 | kN/m3 |
| gamma_II_prime | 20 | kN/m3 |
| c_II | 10 | kPa |
| phi_II | 20 | deg |
| l | 3 | m |
| h | 1 | m |
| d | 1 | m |
| N, excluding foundation/soil weight | 600 | kN |

Prepared source records give gamma_c1=1.1, gamma_c2=1, k=1, M_gamma=0.51,
M_q=3.06, M_c=5.66 and k_z=1 for this branch; pressure records give gamma_mt=20
kN/m3 and the comparison multipliers. These are source inputs to hand arithmetic,
not code constants or newly verified normative statements. Their records and
NormRefs are in `backend/interim_normatives/sp-22-13330-2016/`.

- A=b*l=6 m2; Wx=l*b*b/6=2 m3; Wy=b*l*l/6=3 m3.
- Added weight=gamma_mt*d*A=120 kN; V=N+added weight=720 kN.
- p=N/A+gamma_mt*d=120 kPa.
- R=1.1*(0.51*2*20+3.06*1*20+(3.06-1)*0*20+5.66*10)=152.02 kPa.
- Edge limit=1.2*R=182.424 kPa; corner limit=1.5*R=228.03 kPa.

Source locators, as recorded in those files: СП 22.13330.2016, edition 2016
(с Изменениями N 1, 2, 3, 4, 5), clause 5.6.7/formula (5.7) and table 5.5 for R;
clause 5.6.28/formula (5.11), clause 5.6.29/formula (5.15) and clause 5.6.26 for
pressure components and limits. They remain `unverified` / `machine-extracted`;
human-verified data records do not promote them. Geometry, transfer, signs and
selection are the engineer rules of this change, not new formulas attributed to SP.

## Three complete candidate cases

| Case | Mx, kN*m | My, kN*m | Qx, kN | Qy, kN | Mx_base, kN*m | My_base, kN*m |
|---|---:|---:|---:|---:|---:|---:|
| C: central | 0 | 0 | 0 | 0 | 0 | 0 |
| X: one-axis | 40 | 0 | 20 | 0 | 60 | 0 |
| XY: two-axis | 40 | -30 | 20 | -15 | 60 | -45 |

Base moments are signed M+Q*h. X has contribution 60/2=30 kPa,
e_x=60/720=1/12 m and e_x/b=1/24. XY additionally has contribution
-45/3=-15 kPa, e_y=45/720=1/16 m and e_y/l=1/48. Corner suffixes give
signs of x/y terms, not sorted pressures: p_corner_pp=p+Mx_base/Wx+My_base/Wy.

| Expected output, kPa | C | X | XY |
|---|---:|---:|---:|
| R | 152.02 | 152.02 | 152.02 |
| p | 120 | 120 | 120 |
| p_x_min | 120 | 90 | 90 |
| p_x_max | 120 | 150 | 150 |
| p_y_min | 120 | 120 | 105 |
| p_y_max | 120 | 120 | 135 |
| p_corner_pp | 120 | 150 | 135 |
| p_corner_pm | 120 | 150 | 165 |
| p_corner_mp | 120 | 90 | 75 |
| p_corner_mm | 120 | 90 | 105 |

Minimum corners are 120, 90 and 75 kPa, so every candidate remains in full contact.
The four ordered comparison left sides are respectively:

| Check | Right side, kPa | C | X | XY |
|---|---:|---:|---:|---:|
| p_le_R | 152.02 | 120 | 120 | 120 |
| p_x_max_le_limit | 182.424 | 120 | 150 | 150 |
| p_y_max_le_limit | 182.424 | 120 | 120 | 135 |
| p_corner_max_le_limit | 228.03 | 120 | 150 | 165 |

All hand comparisons pass; the last check decides each pass verdict. Public outputs
would display two decimal places using half_up. Checks and intermediate values do
not use those rounded strings. Display precision is not a reference tolerance.

## Guide discrepancies to preserve

The prior local review of `docs/NTD/methodical_guides/` did not find three directly
admissible full examples for this exact contract. These recovered review notes require
source rechecking before textbook admission; they are not new primary-source verification.

- Линовский/Якушкина example 1 uses explicit foundation/soil weight 212.6 kN,
  whereas the proposed convention gives 189 kN for that geometry, and its reported
  edge/corner check uses different ordinates. Its reported pass is not this type's oracle.
- The guide's central strip example uses a different fixed coefficient set and lacks
  the complete rectangular-footing load-transfer inputs.
- RGR/MPU examples contain wall/lateral-soil or floor contributions outside scope;
  printed R arithmetic requires reconciliation. Duplicate PDFs are not independent examples.
- The older OiF guide uses older norm editions and explicit weights, requiring separate
  source/contract reconciliation.

Never resolve a source conflict by changing expected values or enlarging a tolerance
until a test passes. Before admission, recheck the exact guide page/example, edition,
load plane, weight convention, R coefficients and comparison rule. Source PDFs are
local and may be absent in another checkout.

## Additional invariant and boundary controls

Separate controls must cover p_min=0; a negative corner while both axial minima are
nonnegative; M/Q*h cancellation; pure-module axis interchange; equivalent units;
determinism; each isolated bearing failure; unrounded comparisons; unchanged pilot
fixtures; and typed refusal through runner/API/DOCX/UI. Assertions need independent
arithmetic or an approved invariant, not captured output of the new calculator.
Initially `validated_range=[]`; neither these samples nor generator intervals define
a verified range. New bounds require an evidence-based engineer decision after runs.
