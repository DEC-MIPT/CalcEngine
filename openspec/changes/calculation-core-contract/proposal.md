# Proposal

## Why

The calculation engine, the transparent output, and the report generator are Akim's
three components, and the specs describe the calculation from each side separately.
Nothing states the contract between them, so "white box" cannot be tested. The verified
roadmap (`docs/reports/verified-roadmap.md`, section 3.2, WP2) records:

- **A11 (High):** the trace has no schema. The engine, the UI, and the report each
  describe it from their own side (`calculation-engine/spec.md:20-27,44-52`,
  `transparent-output/spec.md:10-17`, `report-generator/spec.md:43-49`). It is the only
  route a clause reference can travel.
- **A5 (High, engine half):** the rules for calculation code (pure, deterministic,
  explicit units) live only in `agent-docs/domain-constraints.md`, which calls itself
  interim. The DOR, the DOD, and `openspec validate` never read it.
- **C3 (High):** no spec mentions units, conversion, rounding, or tolerance.
- **C2 (Critical):** no requirement makes the engine act on applicability rules. The
  API rejects out-of-range input (`security/spec.md:13-15`), but only as schema
  validation: the check does not tie to the method, does not name the violated bound or
  clause, and has no warning band. Silent extrapolation gives a wrong engineering result.
- **C4 (High):** the report has no statement of engineer responsibility, and the spec
  contradicts itself: the requirement calls the signature fields optional
  (`report-generator/spec.md:22`) while its scenario requires them (`:26-27`).
- **C10 (Medium):** the team intends one declarative input model (`01-recon.md:97`), and
  no spec contains it.
- **B5 (Medium):** task 6.2 of `backend-layered-architecture` ("reading parameters from
  the parameters layer") implies I/O inside the engine, which contradicts its own design.
  Resolved in WP5 on 2026-09-28: its task 6.2 moved to this change's task 7.1.

## What Changes

- `calculation-engine`: adds a pure calculation function, a typed trace step, explicit
  units with conversion at the boundary and declared rounding rules, an applicability
  check with three outcomes, a result envelope, and the evaluation of formulas from data
  as expression trees (added 2026-09-29, `design.md` decision 11). "Step-by-step logging" points to the
  typed trace step, and "Automatic correctness validation" points to the envelope's
  `verdict` and `verdict_reason`.
- `transparent-output`: the trace is rendered from typed steps; unverified references,
  applicability warnings, and refusals are shown; a reference is shown with its status
  instead of being assumed correct.
- `report-generator`: adds a result accountability block with the envelope fields and a
  statement that the design engineer is responsible for the result; resolves the
  signature-field contradiction with a signature block that holds the developer and
  normative control lines, enabled by default (GOST R 21.101-2026, edition unverified);
  references in the report come from the steps and carry their status.
- `security`: "Input validation" is kept and gains a statement that separates it from
  the engine's applicability check.

## Non-goals

- Fixing any norm value: no tolerance, bound, coefficient, rounding rule, or clause
  number in calculation data. The unit vocabulary of `design.md` decision 13 holds
  definitions of units (symbol, dimension, conversion factor), not norm values. These are data that the engineer fills from a
  primary source. The only clauses this change cites as sources are the GOST R 21.101-2026
  (edition unverified) sources of the report's signature block, which were read from the
  standard's text. `design.md` ("Risks") also names formula 5.7 and table 5.5 of
  СП 22.13330.2016 (`unverified`) as the candidate pilot, taken from Egor's records; that
  mention identifies the pilot and fixes no value.
- Finalizing `NormRef`: its shape is agreed with Egor (see `design.md`).
- Choosing how the declarative input model generates API and form validation (C10 stays
  a design note).
- Editing `backend-layered-architecture`; its sync is a task for WP5.
- Verification against reference examples (WP4) and norm provenance and pinning (WP3).
- PDF output.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `calculation-engine`, `transparent-output`, `report-generator`: as in roadmap
  section 3.2.
- `security`: one requirement, to separate schema validation from the applicability
  check (C2). This capability is outside the roadmap's list.

## Impact

- Affects four specs after archive. The code is written on the feature branches named in
  `tasks.md`. No migration: storing the result envelope in `dec_app` belongs to a later
  change (`design.md`, decision 12).
- Depends on `retarget-mvp-domain` (WP1) for the domain name only; the first domain is
  `foundations-shallow` there, and the contract itself is domain-neutral.
- `NormRef` is shared with WP3 (`norm-source-traceability`, Egor) and is agreed
  (design.md, section "NormRef").
- After apply, `backend-layered-architecture` needs a sync (WP5).
