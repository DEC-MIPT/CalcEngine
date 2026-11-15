# Design

## Context

The six prerequisite changes are synchronized and archived. The registered
foundations_shallow_r pilot evaluates R and checks supplied p. This change adds
foundations_shallow_loads through the same registry, source protocol, API, result
storage and report flow. See proposal.md for the outcome and non-goals.

The calculation-module-contract dependency owns the generic typed executor, module
protocol, separate execution/applicability/check states, engineering trace variant
and pre/post-computation diagnostic stops. It first reconnects the existing R pilot
without changing its external result or identity. This change consumes that integrated
contract; it does not alter the shared executor. Foundation-specific unit additions,
input/diagnostic models and public adaptation remain here. Relevant boundaries are
backend/app/engine/, schemas/calculation.py, schemas/units.py and
services/interim_source.py. The 2026-11-14 DOR does not cover this revised design.

## Goals and non-goals

Retain the modular monolith and its existing components: PostgreSQL catalog,
pure Python engine, FastAPI/React platform, MathJax trace and python-docx reports.
Resolve sources before calculation. Keep the pure Calculator.calculate interface
as the future C/C++ replacement boundary: normalized typed inputs, resolved
parameters and explicit execution settings produce deterministic typed results without I/O, clock, randomness or
ML. No queue, worker launch, new endpoint, database migration or new calculation
service is needed. Existing engine/backend layers remain enforced.

The contract covers rectangular full contact only. There is no partial-contact
solution, surcharge on floors, settlement, sizing or automatic preparation of
independent engineering inputs. Stored partial-detachment diagrams do not become
an executable redistribution method.

## Decisions

### 1. Inputs and unit boundary

Public inputs, in order, are b, d_1, d_b, gamma_II, gamma_II_prime, c_II,
phi_II, l, h, d, N, Mx, My, Qx and Qy. The first seven are R inputs; supplied
p is absent. The new type has fifteen inputs.

Add volume m3 and moment N*m, kN*m and MN*m to the closed unit vocabulary;
force units already exist. Convert once at the boundary to the declared base
units: m, kN, kN*m, kN/m3, kPa and degrees, as appropriate. A uses m2 and Wx/Wy
use m3. Volume is an intermediate section-modulus unit, not a new public input.
API conversion tests therefore vary the actual moment inputs independently from
force inputs. Separate engine/schema tests validate volume intermediates and
reject dimension mismatches. No API test invents a volume input to this type.

All inputs are finite. Engineering scope after conversion is b>0, l>0 with
b<=l; h>=0; d>0; N>=0; d_1>=0; d_b>=0 with a separately loaded normative upper
bound; gamma_II>0; gamma_II_prime>0; c_II>=0; and phi_II a whole number of
degrees from prepared rows 0 through 45 inclusive. Mx, My, Qx and Qy allow either
sign and zero. No additional magnitude ceiling is inferred. Square bases are
allowed. Reversed sides are rejected without swapping geometry or loads.
Schema/type errors remain HTTP 422; method-bound refusals retain their existing
result path and JSON shape. The d_b bound comes from the signed supplement.

N excludes foundation and soil weight. d is the thickness entering the weight
term, h is the distance from the load plane at the foundation top to the base,
and d_1 is an independently prepared R input. The service does not infer one from
another. d_b is the prepared R-method value; rejecting a value above its bound
is not a prohibition of deeper physical basements and performs no silent clamp.

### 2. Reuse R and define signed pressure operations

Extract the existing R sequence into a pure helper shared by both types. The
pilot retains the order and identifiers gamma_c1, gamma_c2, k, m_gamma, m_q,
m_c, k_z and R, followed by its supplied-p check. Preserve table selectors,
branches, substitutions, output rounding, source order, result and deciding check.
Compare the existing frozen golden fixture without rewriting it.

For the new type, input/method applicability runs first. The diagnostic trace
starts with the shared R prefix, then geometry A, Wx and Wy, signed load-plane
transfer, mean pressure, axial extrema and four signed corners. The full-contact
guard follows the corners; only admissible contact proceeds to bearing checks.
Refusal may retain this diagnostic prefix, including R steps, but publishes no
final output values.

x spans b and y spans l. Mx/Qx vary pressure along x, My/Qy along y; labels state
this pressure-variation convention rather than relying on a physical moment-vector
interpretation. Geometry is A=b*l, Wx=l*b*b/6 and Wy=b*l*l/6. Signed transferred
moments are Mx_base=Mx+Qx*h and My_base=My+Qy*h; M and Q*h may cancel. Only after
transfer are absolute values taken for extrema. Geometry, transfer, signed corner
extension and diagnostic derived guards use Akim's EngineerRule and recorded
rationale, not an invented norm citation.

Mean pressure is N/A+gamma_mt*d. The complete vertical force used to interpret
eccentricity is V=N+gamma_mt*d*A, so e_x=abs(Mx_base)/V and e_y=abs(My_base)/V.
The approved positive d and source gamma_mt make V positive even when N=0.
Weight is included once; the service must not pre-add it to N. V and eccentricities
are intermediate trace quantities, not additional public outputs.

The stored exact one-axis applicability fraction is evaluated with complete V,
L=b for x and L=l for y. Do not recode a rounded fraction or assume the figure's
printed dimensionless caption uses a different method. Both axial minima being
nonnegative is insufficient for biaxial contact: all four corners are required.
For s,t in {-1,+1}, corner pressure is mean pressure plus
s*Mx_base/Wx+t*My_base/Wy. Suffixes pp, pm, mp and mm represent those x/y signs,
not sorted magnitudes. The minimum over all four is decisive.

Prepared pressure expressions retain their stored NormRefs and explicit typed
substitutions. Signed-corner extension/selection are engineer_formula operations
with explicit normative-component dependencies. The trace shows the component
evaluations and the engineer rule; it must not label the extension as a newly
verified SP formula. Repeated component evaluations have distinct step identifiers.

Full contact admits minimum corner pressure equal to zero. Negative minimum
returns refused before any bearing check; no uplift area, shortened triangle or
bearing pass/fail conclusion is computed. No numerical contact tolerance is
invented. The trace remains unrounded through the guard.

### 3. Normative limits, output order and deciding reason

For admissible contact, checks run in order: mean pressure, greatest x edge,
greatest y edge and greatest corner. Stable identifiers are p_le_R,
p_x_max_le_limit, p_y_max_le_limit and p_corner_max_le_limit. Verdict fail names
the first failed check; otherwise pass names the last check. Values are compared
before output rounding.

Resolve edge/corner limits through a fixed source-assembly binding: an expression
tree multiplies symbol R by the loaded edge/corner multiplier. Its NormRefs are
inherited from that existing multiplier record. This reviewed binding introduces
no numerical coefficient literal, new persisted normative record, signature edit
or record digest. The resulting limit is norm-sourced, not an engineer-set limit.
Assembly-derived describes its construction, not a new public NormRef.provenance
enum or a claim of independent human verification. Normative limit and check steps
show the inherited references. Do not normalize checks by dividing pressure by R:
approved inputs can yield R=0, and no positive-R restriction was approved.

Public outputs, in order, are R, p, p_x_min, p_x_max, p_y_min, p_y_max,
p_corner_pp, p_corner_pm, p_corner_mp and p_corner_mm. p is mean pressure.
Akim's output display rule is 0.01 kPa, half_up, for R and all pressure outputs.
Only presentation rounds; intermediates, guards, comparisons and correctness
metrics consume unrounded values. Display precision is not a reference tolerance.

### 4. Foundation module and compatible diagnostic adapter

Implement the module protocol from calculation-module-contract with typed loads
inputs, resolved data, explicit settings, result and diagnostic details. The module
owns engineering-domain validation, normalization and calculation. The current
flat public quantity map is translated by its external adapter; it is not a generic
executor requirement. Register trusted Python modules at application startup and
resolve all external data before execution. No code/file/data loading occurs in the
pure calculation.

Use the integrated engineer_formula primitive for reviewed geometry, signed transfer,
corner combination and selection. Its EngineerRule source and common source accounting
are supplied by the dependency. Normative component formulas, coefficients and method
bounds retain their resolved NormRefs. This change must not redefine generic trace
or state invariants, source enumeration or the normative metric denominator.

The module emits a generic diagnostic stop for failed full contact. Its private typed
details and foundation adapter provide the existing public kind=derived reason with
check_id, step_id, quantity, value (QuantityValue), operator, limit (QuantityValue),
source (Source), related_inputs (a list of registered input names), and limiting_corner
(pp/pm/mp/mm). The public full-contact reason uses the declared guard identifier,
the computed diagnostic quantity and an actually violated minimum-pressure comparison.
related_inputs names original inputs needed to explain/correct it; quantity is
the derived quantity and need not itself be a registered input.

The module validates limiting_corner, equal-minimum tie selection in pp, pm, mp, mm
order, the matching unrounded minimum value and diagnostic step, the allowed related
inputs and the declared guard source. Foundation schema/adapter validation enforces
the same rules on stored/API representations. These are module-specific validations,
never fields or branches of the shared executor. Test nonexistent steps/inputs/corners,
mismatched minima, incorrect ties and invalid source/value combinations.

The external adapter maps the internal stopped/not-applicable state to verdict=refused
and retains exactly the diagnostic prefix, with outputs=[] and no bearing checks or
bearing deciding reason. Historical input-bound refusals keep empty trace/outputs and
their existing JSON shape. Completed applicable results map engineering checks to the
existing pass/fail verdict and first-failure/last-pass reason. Do not leak diagnostic
intermediate values into final outputs.

New loads runs use the dependency's versioned identity over normalized inputs,
resolved data, methodology/schema versions and significant settings. The R pilot keeps
its legacy hashing algorithm and source identity; historical results are never rewritten.
Before and after module registration compare the shared executor file hashes: they
must be identical. If connecting loads requires a shared-executor change, stop at the
identified contract gap and revise calculation-module-contract before integration.

### 5. Source adapter and a separate applicability supplement

Register foundations_shallow_loads in the existing service catalog. Source selection
stays global: interim strict may resolve the new type after this executable binding
is installed; catalog mode never falls back to files and reports unavailable when
the type has no usable catalog source. No new endpoint is introduced.

Bind the public id through an explicit fixed alias to the prepared
sp-22-13330-2016/foundations_pressure_from_loads.yaml file. Do not resolve arbitrary
user filenames. Reuse existing R/pressure records without rewriting signed values.
Only this new type executes the exact stored applicability/diagram conditions
under the reviewed full-contact contract. Other registered extended files without
an executable contract still fail closed. Partial-contact cases remain stored only.
Human-verified source records retain unverified/machine-extracted NormRefs.

Install the prepared d_b MethodBound in a separate allowlisted directory,
backend/interim_normatives/sp-22-13330-2016-loads-scope/, with a manifest and
foundations_shallow_loads.yaml. The bound is inclusive and source-derived. Signed
LOADS-DB-1 evidence committed at 1b0ea46 supplies the source locator and verification
record; installing it is not an agent-created approval of a new normative fact.
The service rejects above-bound input instead of silently applying the printed
preparation cap. The source supplement does not authorize unrelated D-1 items.

The existing document digest includes all files in the original norm directory.
Changing that directory would change pilot source identity, so keep it byte-identical
and retain existing record/document digest algorithms. New-type data_sha256 is
SHA-256 of canonical JSON with format foundations-shallow-loads-source-v1 and a
documents array of {name,data_sha256}. The constituents are exactly
sp-22-13330-2016 and sp-22-13330-2016-loads-scope, sorted by name. Use UTF-8,
sorted object keys and compact JSON separators with unchanged constituent digests.

All constituents must pass the selected verification profile. Missing/unusable
components fail before engine execution. There is no dynamic constituent list or
external path. Only the new type receives the aggregate in the existing optional
parameter_source object; kind/profile/schema remain unchanged. A change to either
constituent changes it. Pilot identity, signed record digests and historical stored
source labels remain unchanged. Existing strict/draft and sunset semantics remain.

### 6. UI and DOCX consume the stored contract

The existing type selector gains the second type. Forms use generated metadata,
explain excluded weights and independent d/h/d_1/prepared d_b, and include a small
x=b, y=l direction diagram with signed load transfer. The frontend does no pressure
arithmetic. Moment input conversions use declared units; no volume field appears.

Render all outputs/checks and the deciding reason. A derived refusal shows a clear
full-contact scope message and inspectable diagnostic trace, with no final outputs
or bearing conclusion. Existing edit-input draft eligibility stays: only the draft
corresponding to this result enables editing. Directly opening a historical result
does not create a draft. Navigation/playback/reveal must not hide diagnostics or
block access to the refusal explanation.

python-docx consumes stored inputs/envelope, not a new calculation. It includes
load definitions/directions, typed trace, checks and deciding reason; derived
refusal has diagnostic sections and the contact explanation. Historical bound
refusals retain their previous empty-trace presentation. Temporary source label,
digest and responsibility statement remain under the existing report rules.

### 7. Verification and performance boundaries

Akim approved the C, X and XY manual derivations and the absolute 0.005 kPa
per-output tolerance on 2026-11-14. Preserve their inputs, intermediate derivation,
expected outputs/checks and approval provenance in reference-candidates.md. Import
these independent references into the runner without recapturing implementation
outputs or requesting new tolerance decisions. The pilot keeps its textbook-origin
policy. Engineer approval is not successful runner/API/DOCX execution.

Three admitted complete examples, central, one-axis and biaxial, must pass the
verification runner, API and DOCX before new-type backend GO. Signed P1b points
are additional evidence. This is a GO gate, not an additional pre-code DOR gate.
Keep validated_range=[] initially; test generation ranges and individual examples
do not establish validated bounds. Later bounds require an evidence-based engineer
decision. No normative status is promoted by tests or by reference admission.

Test deterministic source/model serialization; signed cancellation and axis exchange;
actual force/moment input conversion through the API; internal volume units separately;
zero M/Q; zero minimum corner; negative corner despite admissible axial minima;
first-tie limiting_corner selection; each independent bearing failure; diagnostic
refusal throughout schemas/storage/API/UI/DOCX; aggregate source failure/change;
no intermediate rounding; and unchanged pilot goldens/reports. Run backend/frontend
checks, Playwright and strict OpenSpec validation with branch coverage >=95%.
Report real database/catalog skips separately. Coverage is not a correctness oracle.

Existing local API latency and report-generation targets remain applicable; this
design introduces no undefined typical-calculation benchmark or claimed measurement.
The pure engine boundary stays replaceable by C/C++ without changing source loading,
UUID allocation, storage, HTTP, UI or report callers. No ML enters calculation.

## Risks and trade-offs

- Shared R extraction may alter pilot identity. Compare existing golden trace/order,
  result, deciding check, source digests and output policy without regenerating goldens.
- Composite bindings may overstate verification. Retain original NormRefs and label
  construction explicitly without creating human-verified source records.
- Reference-policy consent may be confused with example admission. Keep each
  independent engineer acceptance and tolerance record as a separate GO condition.
- Floating point can affect a contact edge. Compare unrounded values without a new
  tolerance, and test exact-zero, negative and equal-minimum corner cases.
- New unions affect historical envelopes. Read old stored results/reports unchanged
  and reject malformed new variants before storing them.
- Large finite inputs can overflow an intermediate. Use finite-result validation and
  a typed calculation error, never infinity or an unapproved applicability ceiling.

## Migration plan

Implement backend tasks on feature/foundations-loads/backend only after consented
integration of calculation-module-contract and current DOR for this revised change.
The frontend feature uses feature/foundations-loads/frontend, branching from the
unmerged backend feature when its contract is needed, otherwise from develop after
backend integration. Regenerate API types and mocks from the agreed schema.
Each feature requires its own tester GO and review; frontend also needs UI/UX.
Commits, merges and pushes require separate explicit consent.

No database migration is expected because result envelopes are JSON; validate
historical rows and both union generations. Rollback disables the new registry/source
binding while retaining immutable stored results and original pilot source data.
Do not delete stored new-type envelopes. Sync/archive only after both features
meet their acceptance and integration gates.
