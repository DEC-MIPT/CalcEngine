# Spec Delta

## Purpose
Defines the rectangular shallow-footing pressure-from-loads contract, full-contact
applicability, source provenance, ordered resistance checks and preservation of the
existing R pilot. Settlement and partial-contact analysis remain outside this type.

## ADDED Requirements

### Requirement: Registered loads type and input meanings
The system SHALL register foundations_shallow_loads with fifteen inputs in this
order: b, d_1, d_b, gamma_II, gamma_II_prime, c_II, phi_II, l, h, d, N, Mx, My,
Qx, Qy. Supplied p is not an input. Base units are m for lengths, kN for forces,
kN*m for moments, kN/m3 for specific weights, kPa for cohesion and deg for phi_II.
The rectangular base has x dimension b and y dimension l. Cut load N excludes
foundation and overlying soil weight; their uniform contribution is added exactly
once as gamma_mt*d, with gamma_mt from the prepared source. d is foundation
thickness in that expression, h the cut-to-base transfer distance, and d_1 the
independently prepared input of R. None is inferred from another. Mx and Qx affect
pressure along x=b, My and Qy along y=l. A positive moment increases pressure at
the positive end of its named axis; shear sign is defined through M+Q*h.

Source: Akim's engineering contract in the user conversation, confirmed 2026-11-08
and recovered 2026-11-14. The normative weight contribution comes from prepared
SP 22.13330.2016, edition 2016 with amendments 1-5, clause 5.6.28, explanation
of formula (5.11). Runtime NormRefs retain their recorded unverified status.

#### Scenario: Weight counted once
- **WHEN** the engineer supplies N without foundation and overlying soil weight
- **THEN** pressure adds gamma_mt*d once and the form and report explain this convention

#### Scenario: Moment input conversion
- **WHEN** a loads request supplies a supported moment unit other than its kN*m base unit
- **THEN** the API validates the moment dimension and the module boundary converts once to kN*m

#### Scenario: Internal volume quantities
- **WHEN** the geometry computes Wx or Wy
- **THEN** its declared dimension is volume, its base unit is m3, and the closed unit vocabulary validates it without adding a volume input to the loads request

#### Scenario: Independent depths
- **WHEN** d, h and d_1 differ within their allowed domains
- **THEN** each is used only for its declared purpose without automatic substitution

### Requirement: Bounded input applicability
The system SHALL enforce the engineer-defined typed domains after base-unit
conversion: all inputs finite; b,l,d positive; h,d_1,d_b,N,c_II nonnegative;
gamma_II and gamma_II_prime positive; b<=l with squares allowed; phi_II whole
degrees from 0 through 45 inclusive; moments and shears of either sign or zero.
No extra upper bounds are imposed on lengths, loads, specific weights or cohesion.
The angle domain selects exact prepared table rows, not a universal soil-angle
limit. Invalid engineer-domain inputs SHALL be rejected as invalid_input 422 with
named fields before pure calculation; direct typed calls enforce the same contract.
No axis swap, interpolation, clamping or rounding is permitted.

The supplied d_b SHALL already incorporate the engineer's normative preparation.
Its inclusive upper method bound SHALL come from signed LOADS-DB-1/d_b_cap_2m,
committed at 1b0ea46, source SP 22.13330.2016, edition 2016 with amendments 1-5,
clause 5.6.7 explanation of d_b, PDF page 36. Values above that loaded bound are
refused without clamping. This does not prohibit a deeper physical basement.
Initial validated_range is empty and claims no empirical range; generated test
inputs SHALL NOT automatically define it. A later nonempty range requires explicit
reference/invariant evidence and separate engineer approval.

#### Scenario: Reversed dimensions rejected
- **WHEN** b exceeds l after unit conversion
- **THEN** the request is rejected with named fields and dimensions and loads are not silently exchanged

#### Scenario: Exact angle rows
- **WHEN** phi_II is fractional or outside the approved selection domain
- **THEN** it is rejected without rounding or selecting a neighbouring table row

#### Scenario: Normative prepared-depth refusal
- **WHEN** d_b exceeds its source-loaded upper bound
- **THEN** the historical input-bound refusal identifies that bound and no pressure calculation runs

### Requirement: Signed geometry and pressure sequence
The system SHALL run the unchanged shared R sequence, then compute A=b*l,
Wx=l*b^2/6, Wy=b*l^2/6, Mx_base=Mx+Qx*h and My_base=My+Qy*h without intermediate
rounding. Signs remain through transfer; extrema use absolute values only after
transfer. Mean pressure is p=N/A+gamma_mt*d. Axis extrema are
p_x_min/max=p-/+abs(Mx_base)/Wx and p_y_min/max=p-/+abs(My_base)/Wy.
The four signed corners are p_corner_pp=p+Mx_base/Wx+My_base/Wy,
p_corner_pm=p+Mx_base/Wx-My_base/Wy,
p_corner_mp=p-Mx_base/Wx+My_base/Wy and
p_corner_mm=p-Mx_base/Wx-My_base/Wy. Corner extrema SHALL be selected from these
four values. V=N+gamma_mt*d*A is the vertical resultant for relative-eccentricity
diagnostics; eccentricity uses abs(M_base)/V with b along x or l along y. No new
R>0 restriction or division by R is introduced.

Geometry, signed transfer and corner combination are EngineerRules attributed to
Akim's recorded contract, not newly verified norm formulas. Their normative pressure
components come from prepared SP 22.13330.2016, edition 2016 with amendments 1-5,
clauses 5.6.28 formula (5.11) and 5.6.29 formula (5.15). The trace SHALL retain
component evaluations with unchanged NormRefs and EngineerRule-labelled extensions.
Shared R retains clause 5.6.7 formula (5.7) and prepared table sources unchanged.

After the shared R prefix, stable distinct diagnostic step ids SHALL include A,
Wx, Wy, Mx_base, My_base, p, p_x_min, p_x_max, p_y_min, p_y_max,
p_corner_pp, p_corner_pm, p_corner_mp, p_corner_mm, p_corner_min, p_corner_max.
Auxiliary normative component and limit evaluations SHALL have deterministic unique
ids. Minimum-corner selection stores limiting_corner as pp, pm, mp or mm; equal
minima select the first in that order, without client recomputation.

#### Scenario: Central loading
- **WHEN** both moments and both shears are zero
- **THEN** mean, axial and all four corner pressures are equal

#### Scenario: Transfer cancellation
- **WHEN** Mx and Qx*h have opposite signs and equal magnitudes
- **THEN** Mx_base and its pressure increment are zero without taking absolute values before transfer

#### Scenario: Pure-module axis interchange
- **WHEN** dimensions and corresponding moment/shear axes are interchanged in a pure-module test
- **THEN** the pressure components and corner names interchange consistently while the public input contract still requires b<=l

### Requirement: Full contact before bearing checks
The system SHALL require the unrounded minimum of all four corner pressures to be
at least zero, with equality allowed and no numerical contact slack. This derived
guard SHALL run after corner evaluation and before any bearing check. A negative
minimum returns refused, retains only the completed diagnostic prefix, and has no
final outputs or bearing pass/fail conclusion. Its reason has kind=derived,
check_id=full_contact, step_id=p_corner_min, quantity=p_corner_min, value and limit
as kPa quantities, operator=ge, source=EngineerRule attributed to Akim's adopted
full-contact rule, limiting_corner from the deterministic stored selection, and
related_inputs=[N,Mx,My,Qx,Qy,h,b,l,d] in that order. Partial detachment, shortened
triangular redistribution and uplift area are not calculated.

Source: Akim's full-contact and signed-corner engineering contract, with prepared
applicability/diagram evidence SP 22.13330.2016, edition 2016 with amendments 1-5,
clause 5.6.28 applicability of (5.11), and clause 5.6.27 figure 5.1. Exact stored
fractions and differing printed caption forms SHALL remain unchanged. Passing each
independent axial minimum alone cannot establish biaxial full contact.

#### Scenario: Zero corner allowed
- **WHEN** the minimum unrounded corner pressure equals zero
- **THEN** full contact is admissible and all four bearing checks run

#### Scenario: Axial minima do not establish contact
- **WHEN** both independent axis minima are nonnegative but a combined corner is negative
- **THEN** the result is refused with the stored limiting_corner and no bearing checks

#### Scenario: Equal minima choose deterministically
- **WHEN** more than one corner attains the same minimum
- **THEN** the stored limiting_corner is the first in pp, pm, mp, mm order

### Requirement: Ordered resistance checks and outputs
The system SHALL run these bearing checks in order after contact is accepted:
p_le_R (p<=R), p_x_max_le_limit, p_y_max_le_limit and p_corner_max_le_limit.
Both edge limits equal the prepared edge multiplier times R; the corner limit
uses the prepared corner multiplier times R. These multipliers and unchanged
NormRefs come from SP 22.13330.2016, edition 2016 with amendments 1-5, clause
5.6.26, through the prepared records. Limit expressions use the reviewed source
assembly symbol/multiply binding, not numeric code literals or engineer-set
normative limits. Every check uses unrounded quantities, including when R=0.
The deciding check is the first failure, otherwise the last check.

Completed outputs SHALL be ordered R, p, p_x_min, p_x_max, p_y_min, p_y_max,
p_corner_pp, p_corner_pm, p_corner_mp, p_corner_mm. Each uses kPa and Akim's
half_up two-decimal output rule. Trace and comparisons remain unrounded. This
rule is display precision, not a reference tolerance. Diagnostic R or pressure
values in a refused trace SHALL NOT become final outputs.

#### Scenario: Separate bearing failures
- **WHEN** separate cases first fail each of the four bearing checks
- **THEN** the matching stable check id decides fail and completed check results remain in declared order

#### Scenario: Display rounding cannot change a verdict
- **WHEN** rounded pressure would reverse a comparison
- **THEN** its check and verdict use the unrounded value and display formatting does not imply the opposite result

### Requirement: Source identity and pilot preservation
The system SHALL register the loads type in the existing registry and strict interim
source via its fixed alias and separate loads-scope supplement. Original R/pressure
files, signed digests, NormRef status and provenance, and pilot source identity
SHALL remain unchanged. A loads-only aggregate identifies the two fixed allowlisted
documents using the unchanged per-document digest algorithm. Missing, unusable or
effectively unchecked records fail closed under strict profile rules.
R helper extraction SHALL preserve the pilot's step order and ids, decisive check,
outputs, golden fixture and historical stored/report meanings without rewriting
expected values to accommodate the refactor.

#### Scenario: Supplement preserves pilot identity
- **WHEN** the separate loads scope supplement is installed
- **THEN** its aggregate includes both constituents and the pilot directory bytes and digest remain unchanged

#### Scenario: Frozen pilot remains valid
- **WHEN** R is extracted for reuse
- **THEN** the original golden fixture passes unchanged and old API results and reports retain their meaning

### Requirement: Foundation module and external diagnostic adaptation
The system SHALL execute foundations_shallow_loads through the integrated
calculation-module-contract protocol and shared executor without modifying that
executor or adding foundation names, including limiting_corner, to it. The module
SHALL expose typed input/resolved-data/result and diagnostic-detail schemas, pure
normalization/domain validation and explicit settings. The existing flat public
request is translated by the foundation adapter. Its new run identity SHALL use
the versioned normalized-input/resolved-data/methodology/schema/settings identity
from the common contract; the R pilot retains its exact legacy hash algorithm.

The public foundation adapter SHALL add the engineer_formula trace variant with
step_id, expression, typed substitutions/result and source: EngineerRule, with
norm_refs forbidden, using the shared internal variant. It SHALL translate the
module's diagnostic stop into the public kind=derived reason defined by "Full
contact before bearing checks", validating its module-specific details without
adding them to the executor. A generic stop is not automatically a foundation
contact refusal. Public input-bound refusal and historical result shapes remain
valid without new mandatory fields or rewriting. Source summaries use the common
first-use accounting and engineer_formula steps do not increase normative verified
or unverified counts. Completed applicable module check results map to public
pass/fail; pre-computation and diagnostic stops map to refused, with final outputs
absent in either refused form.

#### Scenario: Pressure connects without executor changes
- **WHEN** the loads module and foundation adapter are installed after calculation-module-contract integration
- **THEN** the shared executor files match their integrated hashes and all foundation-specific validation lives in the module/adapter

#### Scenario: Invalid module diagnostic details rejected
- **WHEN** a contact diagnostic names a nonexistent step/input/corner, a nonminimum value, a wrong first-tie corner, or an incorrect guard source
- **THEN** the module and foundation adapter reject it before storage without silently dropping diagnostics or returning a bearing verdict

#### Scenario: Public engineer trace sources
- **WHEN** a completed or diagnostically stopped loads result contains engineer_formula steps
- **THEN** those public steps retain their EngineerRule and have no norm_refs, source summaries remain deduplicated in first-use order and unverified_step_count counts only normative steps

### Requirement: Correctness and non-functional gates
The system SHALL require three admitted independent full examples (central,
one-axis, biaxial), approved per-output tolerances and correctness metrics through
the verification runner, API and DOCX before feature GO. P1b formula points and
unapproved agent arithmetic do not replace them. Manual origins are permitted
only for this new type after Akim's independent recorded check, under his conditional
approval of 2026-11-09; the pilot textbook policy remains unchanged. Coverage alone
cannot establish calculation correctness.

Backend/frontend lint, type and test checks SHALL pass with branch coverage at least
95%; UI changes additionally require Playwright and UI/UX confirmation. The pure
module performs no I/O, unsafe formula parsing or evaluation. File paths use fixed
allowlists, and logs contain no input or normative data values. Existing API size
and latency and DOCX-generation targets remain applicable; no typical-calculation
latency claim is introduced. The form and direction diagram SHALL explain x=b,
y=l, d/h/d_1 distinctions and excluded weights, be keyboard accessible and have text
alternatives. Status and refusal meaning SHALL NOT depend on colour. Database or
catalog checks skipped without test URLs SHALL be reported separately.

#### Scenario: Candidates cannot satisfy GO
- **WHEN** coverage passes but an admitted reference or approved tolerance is absent
- **THEN** feature GO is refused even if three arithmetic candidate documents exist

#### Scenario: Accessible diagnostic refusal
- **WHEN** the user opens a derived refusal by keyboard or assistive technology
- **THEN** its reason and diagnostic prefix are immediately available, outputs are absent and edit-input navigation retains existing draft eligibility
