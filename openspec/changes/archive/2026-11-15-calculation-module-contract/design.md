# Design

## Context

The current pipeline in `backend/app/engine/pipeline.py` binds execution to flat
quantity mappings and the external `CalculationResult`. `boundary.run` converts
inputs, hashes them with resolved parameters and both applicability ranges, checks
bounds and calls `Calculator.calculate`. `result.assemble_result` rounds outputs,
orders sources and maps checks to the external pass/fail verdict. See `proposal.md`
for the reason to introduce a module boundary before pressure implementation.

`FoundationsShallowR` already receives resolved Pydantic parameters and is pure.
Its method sequence and the existing helpers can remain intact. Services resolve
parameters before calling the pipeline and persist the returned envelope as JSON;
reports consume that saved envelope. These boundaries remain in place.

## Goals and non-goals

Use Python 3.12 typing and the installed Pydantic validation machinery inside the
existing modular monolith. No additional package, runtime, database migration or
worker process is needed. Akim owns the backend feature. Catalog ingestion and the
read-only database contract with Egor are unchanged.

The generic executor must accept structured models without understanding their
contents. The quantity-mapping contract remains an external compatibility adapter.
Foundation geometry, transferred moments, contact and corner selection belong to
the pressure module. No foundation quantity or `limiting_corner` appears in the
generic executor or its neutral diagnostic schema.

The present feature changes no public API schema. Its engineer-formula steps and
neutral diagnostics are internal types. The pressure feature owns their additive
public representation, report support, generated frontend types and presentation.
No hydraulic suitability claim, network solver or methodology language follows
from introducing this protocol.

## Decisions

### 1. Separate module execution from external adaptation

Introduce a `CalculationModule` protocol parameterized by input, resolved-data,
execution-options, output, diagnostic-details and external-result types. A module
exposes immutable metadata identifying its calculation, methodology version and
input/data/options/output/diagnostic-detail schema versions. It exposes schema validators for all
five typed payloads; Pydantic models or `TypeAdapter` are sufficient. The schema
versions are explicit strings rather than introspected class names.

The protocol has these operations:

| Operation | Responsibility |
|---|---|
| `normalize(inputs)` | Return a new normalized input model without modifying its argument |
| `validate(inputs, data, options)` | Reject invalid domain models and incompatible resolved data/options before computation |
| `calculate(inputs, data, options)` | Check methodology applicability and return a typed outcome, including an early or later stop |
| `validate_diagnostic(diagnostic, trace, inputs, data, options)` | Validate module-owned details, source/quantity relationships and correction references |
| `identity(inputs, data, options)` | Return the run hash using the declared identity policy |
| `adapt_result(execution)` | Convert a validated internal execution to the module's external representation |

`execute_module(module, inputs, data, options)` returns an internal execution record
containing module metadata, run identity and the outcome. Its sequence is schema
validation of inputs/data/options, normalization, schema revalidation of normalized
inputs, domain validation, identity calculation, module calculation, outcome/output
schema validation, generic invariants and module diagnostic validation. It does not
call an external adapter, round values or select a final engineering verdict.
The caller invokes `adapt_result` when an external representation is needed.

Revalidate serialized model contents rather than trusting an existing model
instance created with validation-bypassing construction. Validation rejects
unexpected fields, wrong shapes and nonfinite engineering quantities. Deep-copy
payloads before passing them to module callbacks, so callers retain their input,
resolved-data and option objects even if a defective callback tries to mutate one.
Modules remain responsible for purity and may not retain cross-run state. Tests
must exercise interleaved calls and verify mutation isolation and deterministic
serialization; copying alone cannot prove absence of hidden state.

Applicability is checked inside the module's `calculate`, because structured
methodology guards need not be bounds on a flat input map. An early refusal returns
without invoking the numerical calculator. Domain schema errors remain errors;
they are never converted into methodology refusal. Malformed module output raises
`CalculationError` and is never adapted or persisted. Infrastructure errors are
not converted into a successful or refused engineering result.

The alternative, adding module-name branches to the present pipeline, would couple
the executor to each domain. A universal expression-based methodology description
would add an unneeded language and execution engine. Both are rejected.

### 2. Validate execution, applicability and check results independently

Use an immutable generic `ModuleOutcome[OutputsT, DetailsT]` with execution state,
applicability, optional typed final outputs, ordered trace, ordered check results,
warnings, optional diagnostic and optional stop stage. The execution record itself
has no public foundation verdict.

| Execution | Applicability | Outputs | Diagnostic | Stop stage |
|---|---|---|---|---|
| `completed` | `applicable` | Required | Absent | Absent |
| `completed` | `outside_validated_range` | Required | Absent | Absent |
| `stopped` | `not_applicable` | Absent | Required | `before_calculation` or `after_start` |

Every other combination is invalid. `outside_validated_range` requires at least
one applicability warning; `applicable` carries none. A stopped outcome may retain
validated-range warnings found before its methodology stop. Its diagnostic values
remain in the trace/details, never in final outputs.

Check results are the ordered `CheckStep` records in the trace; the outcome's
ordered checks must equal those records without omission, duplication or reordering.
A completed generic module may have zero checks. The legacy foundation adapter
continues requiring its declared checks and deriving pass/fail from the first
failed or last passed check. Thus a failed engineering check is still a completed,
applicable execution. A stop does not claim an overall bearing pass/fail result.
Any module restrictions on which checks may precede a stop belong to that module.

Step identifiers are unique within the retained trace. Every check references its
retained step. The executor does not interpret a check's name or recompute its
engineering methodology.

### 3. Keep diagnostic details typed and owned by modules

A neutral `ModuleDiagnostic[DetailsT]` has a nonempty `code`, `source` using the
existing `Source` union, optional `step_id` and typed `details`. A pre-calculation
stop has an empty trace and no step reference. A stop after calculation starts has
a nonempty completed trace prefix and a diagnostic `step_id` naming one of its
retained steps. Unknown step references and missing later-stop references fail
generic validation. No unfinished step is appended and no result is fabricated.

A module validates details both against its declared schema and against the actual
trace/inputs/data/options. The generic executor calls that validation without
knowing the fields. For pressure, the future details model owns corner identity,
minimum value, tie ordering and related input names. Its external adapter will map
them to the already agreed flat `kind=derived` reason. The generic schema does not
adopt foundation fields to facilitate that mapping.

The legacy module represents an existing `BoundViolation` in its own typed details
and maps it back without changing the external JSON. Its stop stage is always
`before_calculation`. A generic stopped result is therefore expressible now without
loosening the existing public bound-refusal validator.

### 4. Add internal engineer-formula steps with honest source accounting

Keep existing normative `FormulaStep`, `TableStep` and `CheckStep` fields and
validation intact. Add an internal `EngineerFormulaStep` with disjoint
`kind=engineer_formula`, step identifier, expression, typed substitutions/result
and one `EngineerRule` source. It has no `norm_refs` field and no claim of normative
verification. `ModuleStep` combines the existing normative variants with this
internal variant. Existing expression/table/unit operations remain reusable tools.

Shared internal source enumeration visits trace sources, diagnostic source,
output-rounding sources and warnings in that order, deduplicating by full equality
and preserving first use. Module-specific output sources are supplied by its
adapter because generic structured output models need not be flat quantities.
Normative step counts and the normative traceability denominator include only
norm-sourced variants. Engineer steps are counted separately and are neither
verified nor unverified normative steps. A zero normative denominator is reported
as not applicable rather than as 100% verified. Existing norm-only pilot counts
and source order remain byte-for-byte unchanged.

No shared engineer-formula type carries a numerical engineering formula or source
citation. Pressure binds its actual geometry, transfer and selection operations to
approved rules in its own feature. This change introduces no normative coefficient,
limit, tolerance, new source record or source-status promotion.

### 5. Use explicit run-identity policies

The common new-module identity helper hashes UTF-8 canonical JSON using a separate
lossless v1 serializer and SHA-256. It preserves integer values exactly, including
adjacent integers above 2**53, and finite floats in their shortest round-trip
representation. Integer 1 and float 1.0 remain distinct unless input normalization
produces the same typed value. Only string object keys are accepted; unsupported
values and non-finite numbers raise a calculation error. The existing legacy
serializer is unchanged. The v1 envelope has a fixed
`format=calculation-module-run-v1` and includes module identifier, methodology
version, input/data/options/output/diagnostic-detail schema versions, normalized inputs, resolved
data and all semantically relevant execution options. The identity-policy marker is
part of the hash. Output values, clocks, UUIDs and display-only metadata are absent.
Modules declare their options schema and include its complete normalized contents;
they do not silently omit an execution-affecting option. Equivalent supported unit
representations normalize to the same identity; changing resolved sources,
methodology version, schema version or meaningful options changes the identity.

The R compatibility module explicitly selects the legacy identity policy and invokes
unchanged `input_hash` with the same calculation name, normalized flat inputs and
`{parameters, method_range, validated_range}` payload currently used by
`boundary.run`. It does not wrap that payload in the new versioned envelope. The
legacy rounding/labels/source-label policy remains unchanged. Historical hashes
and stored envelopes are never recomputed or rewritten.

A universal hash change is rejected because it would break the accepted pilot
contract. A hash over public inputs alone is rejected because it omits resolved
data, method version and meaningful options for new modules.

### 6. Register trusted implementations and retain the legacy facade

Trusted modules are selected by fixed identifiers during application startup.
Registration checks nonempty metadata, schema availability and duplicate module
identifiers. It never imports a path provided by a request, evaluates text,
discovers arbitrary plugins or loads source data during calculation. The existing
calculator registry may retain its public contract/legacy calculator facade while
also exposing the corresponding registered module for execution. New module
registration does not require editing `execute_module`.

Keep `pipeline.calculate` as the compatibility entry point used by services and
verification. It invokes the R-compatible quantity module through `execute_module`,
then its adapter produces the same `CalculationResult`. Existing low-level
`boundary.run` may remain for its published callers and regression tests; no second
numerical implementation is introduced. Shared normalization/applicability/hash
helpers are reused rather than copied with differing logic. Keep `CalculatorOutput`
import compatibility if its definition moves to avoid import cycles.

The wrapper preserves existing selector confirmation, method ordering, parameter
schema, `Calculator.calculate` call and output assembly. Formula evaluation, R
arithmetic and threshold branch selection do not change. No shared R-prefix
extraction or pressure computation is performed in this feature. Module numerical
calculation remains the future Python-to-C/C++ boundary: normalized typed
inputs/data/options produce typed unrounded outputs and trace without HTTP, storage,
source-loading or reporting dependencies. The engine imports only permitted
schemas/core and its own modules under the existing import-linter contracts.

### 7. Verify compatibility before downstream pressure work

Backend acceptance includes generic structured-model test modules, early/later stops,
wrong states, output/details validation, invalid step references, source accounting,
identity sensitivity, deterministic interleaving, input mutation isolation and
no-I/O execution. The fixtures demonstrate extensibility without implementing an
unapproved second engineering methodology. A synthetic module must be registered
and executed without modifying the executor.

Run the unchanged pilot golden corpus and compare complete serialized outputs,
trace order/identifiers, deciding check, source metadata and hash. Do not regenerate
fixtures or adjust expected values. Historical saved envelopes must validate and
produce DOCX without invoking the calculator or consulting current source data.
Existing report/API tests cover their unchanged presentation.

`backend/check.sh` must pass Ruff, mypy, import boundaries and tests at >=95% branch
coverage. Run selected/all strict OpenSpec validation and API schema drift checks.
No frontend UI changes occur, so UI/UX acceptance is N/A for this feature. Record
real database/catalog tests or skips separately. Coverage is not independent
calculation correctness evidence.

Existing measured targets remain those in canonical specs: API median <=1 second
for twenty sequential requests after one warm-up against a local migrated dec_app
with an in-process source; report timing remains the report-generator target.
The undefined typical-calculation input for the broader thirty-second target is
not invented here. No new latency, accuracy or hydraulic performance claim is made.

## Risks and trade-offs

- A compatibility wrapper can accidentally change hash inputs or ordering. Compare
  existing complete fixtures, source identities and persisted reports unchanged.
- Generics can hide invalid payloads when existing models bypass revalidation.
  Validate serialized contents, forbidden fields, nested quantities and diagnostics.
- Copying callbacks' arguments adds allocation cost. Prefer this bounded cost to
  caller mutation; keep it measurable in existing API acceptance and avoid caches.
- A generic schema can accumulate foundation rules. Keep domain details behind the
  module validator and require pressure integration without executor edits.
- An internal trace extension can accidentally change public OpenAPI. Require schema
  drift checks to pass unchanged and expose new public variants only downstream.
- Refusal can be mistaken for failed engineering checks. Enforce the state table,
  preserve diagnostics separately and map external foundation verdicts in adapters.

## Migration plan

Prepare and independently review the new change and revised pressure change first.
Implement this feature on `feature/calculation-module-contract/backend`, obtain
separate tester GO and review, then integrate only with explicit Git consent.
Pressure implementation starts only after accepted integration of the contract.

The rollback point is the compatibility facade wiring: restore its old runner while
preserving saved results. No database migration or historical data rewrite is
required. Archive only after reviewed integration and the feature's actual checks.
Future settlement and water-supply methods require their own sources, references,
requirements and changes. A limitation discovered when adding pressure is a contract
review trigger before pressure integration, not permission for a domain branch in
the shared executor.
