# Design

## Context

The engine, the transparent output, and the report generator need one contract that
does not depend on the engineering domain. This change fixes that contract at the level
of fields and behavior. It fixes no norm value: bounds, validated ranges, base units,
and rounding rules are parameter data that the engineer fills from a primary source.

## Goals

- A calculation is a pure function whose output can be compared across runs.
- The trace has one typed shape that the UI and the report consume as is.
- Units and rounding are explicit and traceable to their source.
- Applicability has three testable outcomes.
- Every result carries what is needed to re-run it and names who is responsible for it.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **The pure function is the C/C++ swap boundary.** The engine boundary is a pure
   function `(typed inputs, resolved parameters) -> result envelope`. A later C/C++
   implementation replaces the body behind that signature; callers do not change.
2. **Conversion and applicability sit inside the engine boundary, outside the formulas.**
   The boundary adapter converts inputs to base units and runs the applicability check,
   then calls the formulas. Both steps are deterministic, so the whole call stays pure.
3. **A refusal is an envelope, not an exception.** An input outside the method's range
   yields an envelope with verdict `refused` and the violated bound. The function stays
   total, and the refusal can be stored, shown, and printed like any other result.
4. **Verdict values:** `pass`, `fail`, `refused`, with `verdict_reason` naming the
   deciding check and its `step_id`, or the violated bound for a refusal. The domain
   wording of a conclusion (for example "condition satisfied") is a label per calculation
   type, mapped onto these. The existing requirement "Automatic correctness validation"
   is modified to point at `verdict` and `verdict_reason`, so the capability has one
   description of a conclusion. A refused calculation has an empty `trace`.
5. **`result_id` is assigned outside the function.** The service layer assigns it when it
   stores the result. The determinism check compares envelopes without it.
6. **`input_hash`:** the requirement fixes what goes into it (the calculation type
   identifier, the inputs in base units, and the identity of the resolved parameter set).
   The algorithm is a proposal, open for review: SHA-256 over a canonical serialization
   of those three parts.
7. **`engine_version`** is the released version of the engine package; each calculation
   type may add its own version later.
8. **"Validated range"** is the roadmap's "validated envelope", renamed so it does not
   clash with the result envelope. Its values come from verification (WP4).
9. **Rounding data at run time:** each output quantity is returned in the envelope's
   `outputs` with its value, unit, `rounding_rule`, and `rounding_source`, so the UI and
   the report read the rule and its source from the envelope, not from the type contract.

## NormRef (to be confirmed with data engineer — needs Egor confirmation)

This section records the shared interface from roadmap section 3 as the starting point.
It is not final. Egor owns the catalog side (WP3, `norm-source-traceability`), and the
shape is agreed with him before any requirement that carries `NormRef` is implemented.

    NormRef {document, edition, clause, status, provenance}

- `edition` and `clause` may hold the literal `unverified`.
- No field may be null.
- The meaning of verified and unverified is owned by the `normatives-catalog`
  requirement "Norm reference status" (WP1). This change only carries the value.
- Where a rule comes from the engineer instead of a norm (a rounding rule, a validated
  range), this change writes "a `NormRef` or the engineer". How the engineer case is
  encoded is an open question for Egor (see below).
- Wording clash to reconcile: `agent-docs/domain-constraints.md` and the WP1 deltas
  (`retarget-mvp-domain`: `normatives-catalog` "Norm reference status",
  `transparent-output` "Detailed calculation display") use the literal marker
  `source: unverified`. This interface uses the fields `status` and `provenance`. The
  agreement must state how the two map (for example, `source: unverified` is how a
  `NormRef` with an unverified `status` is displayed), so that both changes use one
  vocabulary.

Engineer-set rules and `domain-constraints.md`: that file says "Rounding and tolerance
rules come from the norm, not from the implementer." This change reads "implementer" as
the software developer, who never chooses a rule; the engine never chooses one either.
The design engineer who fills the parameter data is a different actor and may set a rule
where the norm gives none, with the rule recorded as engineer-set and visible in the
envelope and the report. This reading is Akim's; Egor confirms it together with the
encoding (question 3), and until then tasks 4.3 and 5.1 stay blocked.

Open questions for Egor:

1. Is `status` the verification status (verified or unverified), the document status
   (in force, superseded, withdrawn; WP3 requirement 2), or are these two fields? How
   does it map to the `source: unverified` marker used in `domain-constraints.md` and
   WP1?
2. Are the `provenance` values `human-verified` and `machine-extracted` (WP3 requirement
   4) final, and does the engine or the parameters layer reject `machine-extracted`?
3. Is an engineer-set source allowed for a rounding rule or a validated range (see the
   reading of `domain-constraints.md` above), and if so, how is it encoded: a `NormRef`
   with a reserved document value, or a separate source type?
4. Is `unverified` a string literal in `edition` and `clause`, or an enum value with the
   field typed as a union? What does `document` hold when the document itself is unknown?
5. What does `clause` hold: one clause, or a clause plus a table or formula number? Can
   one step cite several clauses?
6. Is `document` a designation string or a key into `dec_normatives`?
7. Is a `NormRef` stored in a result immutable once pinned (WP3 requirement 3)?
8. What format does `edition` use: a year, a full designation, or an amendment number?

## Design note: declarative input model (C10)

This is a note, not a requirement. The team intends one declarative input model per
calculation type (`docs/audit/01-recon.md:97`). That model is the single source for
API validation (`security` "Input validation"), form validation (`web-platform`
"Calculation input form"), and the engine's typed inputs, base units, and applicability
bounds. How the API schema and the form are generated from it (a shared JSON Schema,
Pydantic models exported to TypeScript, or another route) is an open question for a
later design and is not fixed here.

## Consistency with other specs

- **`security` "Input validation":** kept word for word. This change adds a statement
  and a scenario that split the roles: schema validation first, at the API; method
  applicability second, in the engine (C2).
- **`backend-architecture` (active change `backend-layered-architecture`):**
  - "Parameters stored in YAML" says the parameters layer passes parameters to the
    engine as typed arguments. This agrees with "Pure calculation function".
  - Task 6.2 ("reference implementation reading parameters from the parameters layer")
    implies I/O inside the engine and conflicts with "Pure calculation function" (B5).
    Decision 7 of its `design.md` names a placeholder-domain reference implementation.
    Neither file is edited here; `tasks.md` holds the sync task for WP5.
  - "No hardcoding" says formulas are not written in code but read from configuration or
    a parameter file. If formulas live in YAML, the engine becomes an expression
    evaluator, which changes where a step's `expression` comes from. This is an open
    question for WP5 and is not decided here.
- **`report-generator` "GOST-compliant report assembly"** names GOST R 21.101-2020; that
  edition is not checked against the source text. Recorded for WP3; not edited here.
- **`retarget-mvp-domain` (WP1)** removes "Deterministic verified calculation" and
  modifies "Detailed calculation display"; this change touches neither, and WP1 archives
  first. WP1 task 2.1 (Akim confirms the WP1 engine and output deltas match this
  contract) is still open and must close before this change archives.

## Non-functional requirements

- Performance: unchanged; the existing "Non-functional — performance and accuracy"
  requirement applies. Its "99.9% accuracy" figure has no measurable definition yet;
  making it measurable is deferred to WP4 (`calculation-verification`).
- Determinism: bit for bit on the same platform (see "Pure calculation function").
- Accessibility: warnings and refusals are readable without colour (see
  `transparent-output`).
- Coverage: >= 95% branch coverage for the contract code, per the DOD.
- Security: the envelope holds no credentials; `input_hash` holds no raw input.

## Risks

- `NormRef` changes after agreement ripple through three specs. Mitigation: all three
  refer to it by name and never restate its fields.
- The signature-block default stays open until GOST R 21.101 (edition unverified) is
  checked. Mitigation: it
  is one setting, so the decision changes a default, not the report structure.
