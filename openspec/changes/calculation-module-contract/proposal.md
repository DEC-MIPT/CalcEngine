# Proposal

## Why

The pressure-from-loads expansion needs engineer-sourced trace steps and a diagnostic
stop after intermediate computations. Defining those mechanisms once before adding
pressure avoids embedding foundation rules in the common executor, while retaining
the existing R pilot's results and public contracts.

## What Changes

- Introduce a pure typed calculation-module protocol for normalized inputs, resolved
  data, explicit execution options, typed outputs and module-owned diagnostic details.
- Separate execution status, method applicability and engineering check results;
  reject inconsistent outcomes before external adaptation.
- Retain completed diagnostic trace prefixes on a method stop without exposing them
  as final outputs. Module schemas validate domain details.
- Support a disjoint engineer_formula trace variant and source-aware verification
  metrics without promoting a normative source's status.
- Execute the existing R pilot through a compatibility module, preserving its exact
  hash algorithm, trace, outputs, source identity, API payloads and stored-result DOCX.
- Supply versioned run identity for new modules. Keep the current flat public input
  mapping in external adapters rather than requiring it in the common executor.

## Capabilities

### New Capabilities

- `calculation-module-contract`: trusted module registration, typed execution,
  neutral outcomes/diagnostics, identity, compatibility and acceptance boundaries.

### Modified Capabilities

- `calculation-engine`: pure module execution, typed trace sources, applicability
  stops and compatibility adaptation to existing foundation result envelopes.
- `calculation-verification`: normative-only traceability denominator with
  engineer-sourced steps and zero-denominator reporting.

## Impact

The backend feature `feature/calculation-module-contract/backend` owns module/outcome
schemas, the common executor and registry, shared trace helpers, the R adapter,
compatibility wiring and backend tests. Existing expression, table and unit helpers
remain computational tools. External services resolve data and store results;
calculation modules perform no I/O. API routes, public flat input shape and frontend
behavior remain compatible. Additive shared schemas must pass API schema drift checks.

`foundations-pressure-from-loads` depends on accepted integration of this feature;
its backend/frontend branch names remain unchanged. That change owns foundation
geometry, loads, contact, corner details, pressure formulas and bearing checks.
Adding its module must not require an edit to the common executor.

## Non-goals

Pressure computation, settlement, a complete foundation MVP, water-supply validation,
network solvers, hierarchical solver traces, a universal methodology language,
dynamic code loading, new public structured-model endpoints, new numerical methods,
catalog changes, source-status promotion, rewritten historical results, regenerated
golden fixtures or Git integration without separate explicit consent.

## Declared result differences

None for the R pilot, its frozen regression corpus, saved-result readback or reports.
The new internal protocol and unused additive trace support do not authorize a change
to a historical result, an expected value or an engineering tolerance.
