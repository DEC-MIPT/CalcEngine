# Proposal

Owner: Akim. Two features are defined below. Implementation depends on the
integrated calculation-module-contract and a current review of this revised plan.
The DOR recorded on 2026-11-14 covers the previous design only.

## Why

The delivered `foundations_shallow_r` pilot checks a supplied pressure against R.
Engineers need a bounded rectangular-footing calculation that derives pressures from
loads, explains loss of applicability, and preserves existing pilot results.

## What Changes

- Register `foundations_shallow_loads` with the seven R inputs without p, then l, h,
  d, N, Mx, My, Qx and Qy. Transfer signed loads from the foundation cut to the base;
  compute mean, axial and four corner pressures before four ordered bearing checks.
  Negative minimum corner pressure produces a diagnostic refusal, not a partial-contact
  calculation or a bearing conclusion.
- Reuse R while preserving the pilot's step identifiers/order, deciding check, source
  identity, saved-result behavior and golden fixture. Compare unrounded quantities;
  round only output presentation under Akim's recorded rule.
- Consume the typed module executor, engineer_formula variant and diagnostic-stop
  infrastructure owned by calculation-module-contract. Add loads-specific moment/volume
  units, input and diagnostic schemas, geometry/transfer rules, and the compatible
  foundation adapter across API, storage, DOCX and UI. Historical norm-sourced steps
  and input-bound refusal shapes remain compatible. The shared executor is unchanged
  when this module is connected.
- Resolve this type's prepared pressure records through the existing interim source
  in strict mode. A separate loads-only supplement supplies the signed prepared
  basement-depth bound; aggregate identity preserves the pilot document digest.
- Add the type, input explanations, direction/sign diagram, all outputs/checks and
  diagnostic refusal actions to the existing user journey and report routes.
- Require three admitted independent full-type references, invariants, regression
  comparison and runner/API/DOCX checks before backend feature GO. Signed P1b formula
  points remain supplementary evidence.

## Capabilities

### New Capabilities

- `foundations-pressure-from-loads`: the engineering contract, applicability,
  pressure/check ordering, provenance and compatibility of the new public type.

### Modified Capabilities

- `calculation-engine`: source-assembled normative limit bindings using the integrated
  calculation-module-contract protocol and trace primitives. The new contract owns
  common units/source permissions, trace variants, state and result assembly.
- `interim-normatives`: explicit public-type alias, executable loads-record selection,
  separate supplement and aggregate data identity.
- `calculation-api`: additive input/output metadata and trace/refusal schemas for
  existing endpoints and immutable stored results.
- `calculation-verification`: narrow reference-origin admission for the new type,
  preserving the pilot's policy and oracle independence. Common source-aware metrics
  are owned by calculation-module-contract.
- `transparent-output`: engineer sources, all pressure/check results and diagnostic
  refusal rendering without client recomputation.
- `report-generator`: directions, load inputs, pressure/check trace and derived
  refusal reporting while preserving historical pilot report meaning.
- `web-platform`: type selection, input guidance, direction diagram and refusal
  reveal/navigation with existing draft eligibility retained.

## Non-goals

Partial contact or uplift redistribution; floor surcharge q; settlement; automatic
sizing; deriving prepared d_1 or d_b; friction-angle interpolation; new catalog views
or writes in Egor's zone; per-type source selection; new endpoints; NormRef promotion;
deployment; declaring the full foundation MVP complete. Independent d, h and d_1
inputs are not inferred from one another.

## Impact

`feature/foundations-loads/backend` owns schemas, parameters, source resolution,
pure engine module, API, DOCX and backend verification. The dependent
`feature/foundations-loads/frontend` owns forms, diagrams, results/trace/refusal UI,
mocks, generated API types and browser tests. Frontend branches from backend when
its unmerged contract is needed. Documents stay on develop; Git actions require
separate explicit consent.

The additional calculation-module-contract dependency must have tester GO, review
and consented integration into develop before this backend feature starts. Its
feature is feature/calculation-module-contract/backend. This change does not implement
that feature or duplicate its common executor/schema tasks.

The six earlier prerequisite owner changes are synchronized, archived and committed:
retarget, core, API, interim source, verification and frontend. Full MODIFIED
requirements must reconcile the current canonical contracts rather than copy old
active-owner drafts. Pressure data are already committed. Signed LOADS-DB-1
source evidence is in `docs/verification/foundations-pressure-from-loads/` at
1b0ea46; restoring this proposal does not install or promote a runtime record.

## Reference-policy decision

On 2026-11-09 Akim explicitly allowed manual references for this new type only,
conditional on his check: "Да, разрешить после моей проверки". An admitted example
must therefore have an independently engineer-checked full derivation, cited source
and edition, approved per-output tolerance/provenance and an admission record.
Policy consent alone admits no candidate or numerical tolerance. Akim subsequently
approved C, X and XY and their absolute 0.005 kPa per-output tolerances on 2026-11-14;
the immutable derivation and approval record is reference-candidates.md. Those
references still require runner/API/DOCX execution before GO. The pilot retains
its textbook-origin policy.
