# Design

## Context

The six prerequisite changes are synchronized and archived. The registered
foundations_shallow_r pilot evaluates R and checks supplied p. This change adds
foundations_shallow_loads through the same registry, source protocol, API, result
storage and report flow. See proposal.md for the outcome and non-goals.

The current engine pipeline requires empty-trace refusals; trace steps require
normative sources; the unit vocabulary lacks moment and volume. These contracts
must be extended before the new calculator consumes them. Relevant boundaries are
backend/app/engine/pipeline.py, schemas/calculation.py, schemas/units.py and
services/interim_source.py. Runtime files are implementation targets, not edits
performed by this planning change.

## Goals and non-goals

Retain the modular monolith and its existing components: PostgreSQL catalog,
pure Python engine, FastAPI/React platform, MathJax trace and python-docx reports.
Resolve sources before calculation. Keep the pure Calculator.calculate interface
as the future C/C++ replacement boundary: normalized typed inputs and resolved
parameters produce deterministic typed results without I/O, clock, randomness or
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

### 4. Additive trace and diagnostic refusal contracts

Keep formula, table and check variants unchanged. Add a disjoint engineer_formula
variant with step_id, expression, typed substitutions/result and an EngineerRule
source. It carries no fabricated norm_refs or normative verified flag. The same
Source union permits an EngineerRule for a derived applicability guard, as well as
for geometry, transfer and selection. Existing method bounds remain norm-sourced.

The new reason is an exact kind=derived variant with check_id, step_id, quantity,
value (QuantityValue), operator, limit (QuantityValue), source (Source),
related_inputs (a list of registered input names), and limiting_corner, an enum
pp/pm/mp/mm. The full-contact reason uses the declared guard identifier, the
computed diagnostic quantity and an actually violated minimum-pressure comparison.
related_inputs names original inputs needed to explain/correct it; quantity is
the derived quantity and need not itself be a registered input.

limiting_corner identifies a corner attaining the minimum. Resolve ties by the
fixed first occurrence in pp, pm, mp, mm order, using the unrounded values.
The reported value must equal that corner and the minimum. step_id references a
retained diagnostic step with matching quantity/value; operator and limit describe
the failed applicability comparison, not a completed bearing check. Source is the
approved guard rule; normative components remain separately visible in the prefix.
Test malformed reasons, nonexistent steps/inputs/corners, mismatched minima and
incorrect tie selection at schema and API persistence boundaries.

Only kind=derived refusal retains a diagnostic prefix. It requires outputs=[] and
verdict=refused, no bearing checks and no bearing deciding reason. Historical
kind=bound refusal retains empty trace/outputs and its existing JSON shape.
Pass/fail still requires a deciding check in the trace. Shared result assembly and
API validation reject inconsistent combinations instead of dropping diagnostics.

Source enumeration remains deduplicated and first-use ordered: trace, refusal,
output rounding sources, then warnings. Norm-sourced steps form the normative
traceability denominator; engineer_formula steps are separately counted, not
counted as verified or unverified normative steps. unverified_step_count excludes
engineer_formula and still counts every unverified normative step. EngineerRule
sources, including derived guards, remain listed in engineer_rules. Old norm-only
results keep their previous metric values and source order.

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

The recorded manual-reference approval is conditional: Akim allowed the new type's
manual references after his check. It does not admit current arithmetic candidates
or approve tolerances. Each admitted example needs independent engineer review of
the full derivation, cited source/edition and approved per-output tolerance with
its origin and admission record. The pilot keeps its textbook-origin policy.

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

Implement backend tasks after recorded DOR on feature/foundations-loads/backend.
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
