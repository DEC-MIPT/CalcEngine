# Proposal

## Why

The current `foundations_shallow_loads` calculation computes pressure for a supplied rectangular footing, but it does not explain the load assembly visually, expose an explicit-weight alternative, or help an engineer compare candidate footing sizes. Public methodical examples and a competitor audit show that the load cut, added weights, moments, surcharge, and pressure envelope must be visible and unambiguous before a result can be compared or reviewed.

## What Changes

- Preserve the existing averaged-weight pressure mode and its stored-result identity.
- Clarify the load contract: load level, excluded weights, `d`, `h`, `d_1`, units, sign convention, and whether supplied loads are already at the footing base.
- Add a mutually exclusive explicit-weight mode that accepts engineer-supplied additional vertical weights and their signed moments, without deriving volumes or silently reusing `20*d*A`.
- Add a stored load schematic and pressure-envelope data for the rectangle, axes, signs, transferred moments, extrema, and corner pressures; the client renders these values without recalculation.
- Add bounded footing-size candidate evaluation and a deterministic selection policy only after the engineer selects the candidate bounds, step/grid, objective, and tie policy. The proposed first search supports the averaged mode only and accepts an explicit candidate list; explicit fixed weights are not reused across changing geometry. Candidate calculations retain full traces.
- Preserve strict full-contact refusal, existing ordered checks, historical pilot behavior, stored-result immutability, source provenance, and report compatibility.
- Regenerate API types and provide accessible frontend controls, diagram alternatives, result tables, and trace sections for the new stored data.

## Non-goals

- No partial-contact redistribution, uplift-area solution, or automatic soil-pressure redistribution.
- No automatic volume or weight inference from an unapproved foundation geometry model.
- No copying of competitor coefficients, hidden load factors, resistance values, or undocumented normative rules.
- No settlement, seismic, sliding, or structural concrete design implementation in this change.
- No change to the shared module executor or the historical pilot identity.
- No declaration that methodical examples or competitor output are independent correctness oracles.

## Capabilities

### New Capabilities

- `foundation-design-tools`: explicit-weight input, stored load schematic and pressure envelope, and bounded candidate-size evaluation for the loads calculation.

### Modified Capabilities

- `calculation-engine`: clarify load assembly and add an explicit-weight variant while preserving the averaged variant and full-contact contract.
- `calculation-api`: expose a new explicit-weight type through existing calculation routes, additive stored visualization context and a dedicated typed candidate-search resource.
- `transparent-output`: render stored load diagrams, pressure envelopes, weight contributions, candidate comparisons, and their sources without client recalculation.
- `web-platform`: add accessible controls for load mode and candidate selection, plus responsive schematic and pressure-envelope views.
- `report-generator`: include the selected load mode, weight contributions, schematic data, pressure envelope, and candidate decision in new loads reports.
- `calculation-verification`: add independent reference and invariant gates for explicit-weight equivalence, load conservation, signed transfer, candidate determinism, and unchanged averaged-mode examples.

## Impact

Backend code belongs to `feature/foundations-design-tools/backend`, branched from the reviewed loads backend dependency. Frontend code belongs to `feature/foundations-design-tools/frontend`, created from develop only after the existing loads frontend feature has completed its own acceptance, review and authorized integration. Documents are authored on `develop`.

The existing loads API remains backward compatible for averaged-mode requests. A proposed new registered type `foundations_shallow_weights` separates explicit weights from the unchanged fifteen-input loads contract. A dedicated typed search resource is additive; selected candidates become ordinary stored calculation results linked to immutable search provenance. Old stored envelopes and the pilot remain readable without migration or rewriting.

The change requires an engineer decision before implementation for candidate search bounds, step or grid, objective, tie policy, and the explicit-weight moment contract. No coefficient or tolerance is invented by this proposal. Implementation requires updated specs, a current spec-reviewer report, tester GO, UI/UX confirmation, branch coverage of at least 95%, and independent reference provenance.
