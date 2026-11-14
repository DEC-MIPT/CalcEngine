# Proposal

Owner: Akim. Two features are defined below. Current work restores the planning
contract and obtains DOR review; it implements no calculation code.

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
- Extend typed units, engineer-sourced geometry/transfer steps and computed-value
  applicability refusals across schemas, engine, API, storage, DOCX and UI. Historical
  norm-sourced steps and input-bound refusal shapes remain compatible.
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

- `calculation-engine`: units, engineer formula steps, diagnostic derived refusals,
  envelope source accounting and pilot compatibility.
- `interim-normatives`: explicit public-type alias, executable loads-record selection,
  separate supplement and aggregate data identity.
- `calculation-api`: additive input/output metadata and trace/refusal schemas for
  existing endpoints and immutable stored results.
- `calculation-verification`: source-aware trace metrics and narrow reference-origin
  admission for the new type, preserving the pilot's policy and oracle independence.
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

The six prerequisite owner changes are synchronized, archived and committed:
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
That policy consent approves no current candidate or numerical tolerance. Agent
arithmetic is not an admitted oracle. The pilot retains its textbook-origin policy;
three admitted full examples remain mandatory for the new type's GO.
