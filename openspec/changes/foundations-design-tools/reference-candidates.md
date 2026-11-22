# Explicit-weight reference candidates

**ADMITTED on 2026-11-22** by Akim after the scoped reviews and final manual-origin/tolerance confirmation recorded below. Earlier proposed/unadmitted statements remain historical; the final admission record controls. These are independent manual derivations for the new
`foundations_shallow_weights` type. They are not approved references, passing
implementation tests, or evidence of DOR/GO. The candidate identifiers are
`weights-C`, `weights-X` and `weights-XY`; they are distinct from the already
admitted averaged-mode C/X/XY references.

## Admission and provenance

The derivation author is the backend-developer agent, dated 2026-11-22. No human
reviewer or approval date is recorded for these candidates. The arithmetic below
uses stated inputs and elementary decimal operations; it does not execute the DEC
engine or capture its outputs. The source for the new explicit vertical/moment
assembly is the engineering contract proposed in this change, pending Akim's final
sign/load-plane approval. The independent arithmetic check is retained temporarily
as `/tmp/dec-design-tools-reference-arithmetic.json`; this document owns the
reviewable inputs, derivation and expected values.

Akim confirmed the capability of named weights and additional moments for one fixed
geometry. That confirmation alone does not admit these examples, their expected
values, the proposed moment signs, a new manual-origin exception or numerical
tolerances. The existing manual-reference exception and approvals in
`../foundations-pressure-from-loads/reference-candidates.md` apply to the old
averaged type only; they do not automatically extend to this new registered type.
The applicable three-complete-reference gate remains in force.

Before admission, record an explicit decision allowing manual origins for this
new type after Akim's independent check, his approval of all three complete
examples, the approved tolerance and its provenance for every output, and an
immutable digest of the reviewed derivation. No candidate may count toward DOR or
GO until the applicable gates in `tasks.md` and the verification spec are met.
Do not mark task 1.4 complete from the existence of this file.

## Proposed input and sign contract

All values are supplied for one fixed rectangular footing geometry. `N` is the
second-limit-state structural vertical load at the upper cut, excluding all three
additional weights. The proposed `G_fund`, `G_soil` and `G_other` are downward
nonnegative weights in kN. `Mx`, `My` and `Qx`, `Qy` are signed cut loads. The
proposed `Mx_add_base` and `My_add_base` are signed additional resultant moments
already at the base, in kN*m; they are not transferred through `h` again.

The adopted pressure-variation convention is x along b and y along l. A positive
base moment raises pressure at the positive end of its named pressure axis. The
additional moments describe the independently supplied weight/resultant assembly;
this candidate does not derive eccentricities, volumes or material densities from
the named weights. It introduces no automatic load-factor conversion.

Proposed explicit assembly, requiring final engineering approval:

- N_base = N + G_fund + G_soil + G_other, in kN.
- Mx_base = Mx + Qx*h + Mx_add_base, in kN*m.
- My_base = My + Qy*h + My_add_base, in kN*m.
- p = N_base/A, in kPa; no gamma_mt*d*A term is added.

The proposed candidate input set contains 19 scalar quantities, listed completely
in the common and case-specific tables below. It does not need the averaged
weight thickness `d` for pressure arithmetic. If the finalized module retains a
separate geometry-only field, its declared meaning must be reconciled before
admission; such a field must not silently add an averaged weight to this mode.
The extra fields and their exact schema are still proposed, not an approved API.

## Common inputs and reused resistance data

| Input | Value | Unit | Meaning |
|---|---:|---|---|
| b | 2 | m | x dimension |
| l | 3 | m | y dimension |
| d_1 | 1 | m | independently prepared R input |
| d_b | 0 | m | prepared basement-depth R input |
| gamma_II | 20 | kN/m3 | R soil input below base |
| gamma_II_prime | 20 | kN/m3 | R soil input above base |
| c_II | 10 | kPa | R cohesion input |
| phi_II | 20 | deg | exact whole-degree row |
| h | 1 | m | cut-to-base transfer arm |
| N | 600 | kN | structural cut load, excluding added weights |

The common geometry and R inputs are the independently derived resistance part
of the old averaged-mode examples. Their earlier approval is evidence for that
component only, not approval of the new explicit-weight assembly. Prepared data
provide gamma_c1=1.1, gamma_c2=1, k=1, M_gamma=0.51, M_q=3.06, M_c=5.66
and k_z=1, plus the existing loaded edge/corner multipliers 1.2 and 1.5. These
are inputs to hand arithmetic, not proposed new hardcoded values.

Source locators retained from the prepared data: SP 22.13330.2016, edition 2016
with amendments 1-5, clause 5.6.7/formula (5.7) and table 5.5 for R; clause
5.6.26 for the existing check limits; clauses 5.6.28/formula (5.11) and
5.6.29/formula (5.15) for the normative pressure components. The data and their
source-status provenance remain those recorded in
`backend/interim_normatives/sp-22-13330-2016/`. NormRefs remain
`unverified`/`machine-extracted`; this candidate does not promote them or claim
that the new explicit assembly is a newly verified SP formula. Geometry, signed
transfer/corners and contact are engineer rules, with the new weight/base-moment
assembly proposed separately above.

Common hand calculation:

- A = b*l = 2*3 = 6 m2.
- Wx = l*b*b/6 = 3*2*2/6 = 2 m3.
- Wy = b*l*l/6 = 2*3*3/6 = 3 m3.
- R = 1.1*(0.51*2*20 + 3.06*1*20 + (3.06-1)*0*20 + 5.66*10).
- R = 1.1*(20.4 + 61.2 + 0 + 56.6) = 152.02 kPa.
- Edge limit = 1.2*R = 182.424 kPa.
- Corner limit = 1.5*R = 228.03 kPa.

## Complete case inputs

These nine case-dependent quantities complete the common ten-input table.

| Input and unit | weights-C | weights-X | weights-XY |
|---|---:|---:|---:|
| G_fund, kN | 60 | 60 | 60 |
| G_soil, kN | 40 | 40 | 40 |
| G_other, kN | 20 | 50 | 50 |
| Mx, kN*m | 0 | 40 | 40 |
| My, kN*m | 0 | 0 | -30 |
| Qx, kN | 0 | 20 | 20 |
| Qy, kN | 0 | 0 | -15 |
| Mx_add_base, kN*m | 0 | 10 | 10 |
| My_add_base, kN*m | 0 | 0 | -15 |

### Central case weights-C

Added weight = 60+40+20 = 120 kN; N_base = 600+120 = 720 kN.
Both base moments and pressure increments are zero. Therefore p = 720/6 =
120 kPa, both axial minima/maxima and all four signed corners equal 120 kPa.
The full-contact minimum is positive; all corners tie and the retained first-tie
order pp, pm, mp, mm chooses limiting_corner=pp. All four bearing checks run.

This is an equivalence control: the added weight also equals the old averaged
allowance 20*1*6 = 120 kN for that distinct old-mode input d=1 m. Equal
assembled resultants and geometry give equal pressures and check results; their
calculation-type/methodology identities must still differ. The old allowance is
not an additional force in the new mode.

### One-axis case weights-X

Added weight = 60+40+50 = 150 kN; N_base = 600+150 = 750 kN.
Mean p = 750/6 = 125 kPa. The x cut transfer is 40+20*1 = 60 kN*m;
adding the base contribution once gives Mx_base = 60+10 = 70 kN*m.
My_base = 0. The signed x pressure increment is 70/2 = 35 kPa, and the
y increment is zero.

Thus p_x_min/max = 125-/+35 = 90/160 kPa; p_y_min/max = 125/125 kPa.
The corner order pp, pm, mp, mm gives 160, 160, 90, 90 kPa. The positive
minimum is 90 kPa, tied at mp/mm; the first minimum is limiting_corner=mp.
The greatest corner pressure is 160 kPa; all four bearing checks run.

### Two-axis case weights-XY

The same added weight and structural force give N_base = 750 kN and p =
125 kPa. The x base moment remains 70 kN*m. The y cut transfer is
-30 + (-15)*1 = -45 kN*m; the already-base addition is -15 kN*m, so
My_base = -45-15 = -60 kN*m. Signed pressure increments are +35 kPa in x
and -60/3 = -20 kPa in y.

Axial p_x_min/max are 90/160 kPa and p_y_min/max are 105/145 kPa.
The signed corners are:

- pp: 125+35-20 = 140 kPa.
- pm: 125+35+20 = 180 kPa.
- mp: 125-35-20 = 70 kPa.
- mm: 125-35+20 = 110 kPa.

The full-contact minimum is 70 kPa at limiting_corner=mp; the greatest
corner is 180 kPa at pm. All four bearing checks run. The nonzero added
base moments remain explicit inputs; the candidates do not infer their source
locations from the component weights.

## Complete expected outputs

All ten quantities below are in kPa, in the existing public pressure-output order.
These are proposed expected values, not outputs read from an implementation.

| Output | weights-C | weights-X | weights-XY |
|---|---:|---:|---:|
| R | 152.02 | 152.02 | 152.02 |
| p | 120 | 125 | 125 |
| p_x_min | 120 | 90 | 90 |
| p_x_max | 120 | 160 | 160 |
| p_y_min | 120 | 125 | 105 |
| p_y_max | 120 | 125 | 145 |
| p_corner_pp | 120 | 160 | 140 |
| p_corner_pm | 120 | 160 | 180 |
| p_corner_mp | 120 | 90 | 70 |
| p_corner_mm | 120 | 90 | 110 |

The existing two-decimal half_up display policy would show these quantities to
0.01 kPa. That output-format rule is distinct from the proposed reference
comparison tolerance below. Intermediates and check comparisons remain unrounded.

## Ordered checks and deciding reason

The contact guard precedes the bearing checks and uses the unrounded minimum,
with equality to zero admitted and no numerical slack. The guard passes in all
three candidates. No claim of a validated application range follows from them.

| Check ID | Left C | Left X | Left XY | Right, kPa | Proposed result |
|---|---:|---:|---:|---:|---|
| p_le_R | 120 | 125 | 125 | 152.02 | pass in each |
| p_x_max_le_limit | 120 | 160 | 160 | 182.424 | pass in each |
| p_y_max_le_limit | 120 | 125 | 145 | 182.424 | pass in each |
| p_corner_max_le_limit | 120 | 160 | 180 | 228.03 | pass in each |

All comparisons use <=. Each completed candidate has proposed verdict=pass,
with deciding reason step_id=p_corner_max_le_limit, the last check in the
existing ordered sequence. Full-contact limiting_corner is diagnostic/intermediate
provenance here; it is not an extra final pressure output.

## Proposed tolerances and admission record

For every R/pressure output in the ten-row table and in each case, the proposed
reference fields are tolerance=0.005 kPa, tolerance_kind=absolute. Proposed
`tolerance_source`: an engineering decision requested from Akim for this new
explicit-weight type on 2026-11-22. The value is a proposal matching the earlier
pressure reference policy, not an automatically inherited or approved tolerance.
Check IDs/order/status and limiting_corner are exact categorical expectations.
No proposed pressure tolerance changes applicability, comparisons or the full-contact
guard. No numerical reference tolerance is proposed for force or moment outputs;
these remain intermediate values with the exact derivations recorded above.

| Admission field | Current value |
|---|---|
| origin | manual calculation, proposed and not admitted |
| calculation type | foundations_shallow_weights, proposed new type |
| derivation author | backend-developer agent |
| derivation date | 2026-11-22 |
| human reviewer/date | absent |
| manual-origin exception for new type | not granted |
| complete-case engineering approval | absent |
| per-output tolerance approval | absent |
| source citation | this file, 2026, common derivation and named case section |
| source_norm_edition | SP 22.13330.2016 edition 2016 with amendments 1-5; runtime NormRefs remain unverified |
| runner/API/DOCX execution | not performed |

Before admission, freeze and record a digest over the exact reviewed derivation
and expectation sections, plus the recorded approval wording and reviewer/date.
A later formula/input correction must receive fresh review; do not alter an
accepted expected result merely to match code.

## Separate sizing and boundary controls

These three fixed-geometry cases do not validate automated size selection. The
averaged-mode search still requires independently derived small-list controls with
candidate-specific R resolution, minimum-area and tie decisions, no passing
candidate, source failure and incomplete-search outcomes under the approved policy.
No search candidate R may be copied from this fixed-b reference when b changes.
Explicit weights remain fixed-geometry only; do not reuse these component weights
across sizing candidates.

Additional explicit-weight controls must cover zero weights, invalid negative
weights under the finalized downward-only contract, independent sign cancellation,
equivalent force/moment units, zero minimum corner, loss of full contact despite
nonnegative axial minima, each isolated bearing failure, named input errors and
unchanged old-type identity. A future source/contract gap remains a blocker rather
than permission to change the shared executor or an existing norm coefficient.


## Partial engineer review, 2026-11-22

Akim reviewed the presented common inputs and central weights-C derivation,
including all central pressures, R/check limits, contact and equivalence with
the old allowance, then explicitly answered: "weights-C подтверждаю".
Reviewer: Akim. This confirms weights-C only. The other cases, final manual-origin
exception and per-output tolerance decision remain pending; task 1.4 is not complete.

The reviewed arithmetic snapshot is SHA-256 over the UTF-8 concatenation of
the text after "## Common inputs and reused resistance data" and before
"## Complete case inputs", then the text after "### Central case weights-C"
and before "### One-axis case weights-X", excluding those heading lines:
`0198954fdd92be9d5e885135227c33fe7f010ad383cd5ba35821acda5c118b42`. No result was captured from the implementation.


## One-axis engineer review, 2026-11-22

Akim explicitly answered "weights-X подтверждаю" after reviewing the supplied
one-axis inputs and derivation, including G_other=50 kN, total added weight
150 kN, N_base=750 kN, the single base-moment addition, pressures, contact,
first-tie corner and all four checks. Reviewer: Akim. This confirms weights-X
in addition to the earlier scoped weights-C approval. weights-XY, the new-type
manual-origin exception and output tolerance decision remain pending.

SHA-256 over the UTF-8 common-input text defined above followed by the text
after "### One-axis case weights-X" and before "### Two-axis case weights-XY",
excluding the heading lines: `bd017d31ca9c12c8bc7bb5b38abacf8bb7be969ffede2ec6798aed8afee4fe14`. No engine output was used as an oracle.


## Two-axis engineer review, 2026-11-22

Akim explicitly answered "weights-XY подтверждаю" after reviewing the two-axis
inputs, signed cut-to-base transfer and single additional base moments, all four
corners, minimum contact pressure and all four checks. Reviewer: Akim. The
arithmetic of weights-C, weights-X and weights-XY is now engineer-reviewed.
The new-type manual-origin exception and per-output tolerance decision are still
pending; these reviews alone do not complete reference admission or task 1.4.

SHA-256 over the UTF-8 common-input text defined above followed by the text
after "### Two-axis case weights-XY" and before "## Complete expected outputs",
excluding those heading lines: `fda1816ec75abc5df29b136d54066a00a6ff89a40ad3d5942f2087e2e195a41f`. No engine output was used as an oracle.


## Final admission, 2026-11-22

Akim explicitly confirmed each presented derivation with "weights-C подтверждаю",
"weights-X подтверждаю" and "weights-XY подтверждаю", then stated:
"Ручные эталоны и допуск 0,005 кПа подтверждаю". This grants the narrow
manual-calculation origin exception for these three engineer-checked references
of foundations_shallow_weights and approves absolute tolerance 0.005 kPa for
each of the ten R/pressure outputs in every case. Reviewer: Akim; date: 2026-11-22.
Derivation author remains the backend-developer agent, not Akim. Source citation:
this document (2026), Common inputs, Complete case inputs, named case derivations,
Complete expected outputs and Ordered checks sections.

The arithmetic/expectation snapshot SHA-256 is `24044046751e1024b457deef3ca4f99fb9bc8cb261e741ce43cb2f928cbe5578`,
computed over the exact UTF-8 text from and including "## Common inputs and
reused resistance data" up to but excluding "## Proposed tolerances and
admission record". The scoped digests above remain historical evidence.
Source_norm_edition is SP 22.13330.2016, edition 2016 with amendments 1-5,
with unchanged unverified runtime NormRefs. The per-output tolerance_source
is Akim's explicit final approval quoted above, recorded in the working conversation
and paired design-tools readiness. Check identity/order, booleans and corner labels
remain exact; no tolerance alters method guards or normative comparisons.

The upper-cut structural-load and already-base added-moment assembly presented
and checked in the three cases is the implementation contract: downward weights
are nonnegative, cut moments/shears and added moments are signed under the existing
x=b/y=l pressure-variation convention, transfer is M+Q*h once, and additional
base moments are added once. No reverse load-factor conversion, volume inference
or averaged weight allowance is introduced. The reference admission establishes
expected results, not successful runner/API/DOCX execution, validated_range or GO.
