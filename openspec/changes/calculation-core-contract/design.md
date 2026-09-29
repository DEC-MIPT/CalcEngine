# Design

## Context

The engine, the transparent output, and the report generator need one contract that
does not depend on the engineering domain. This change fixes that contract at the level
of fields and behavior. It fixes no norm value: bounds, validated ranges, formulas,
coefficients, and rounding rules are parameter data from a primary source or set by the
engineer, and base units are declared in each calculation type's contract.

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
   function `(typed inputs, resolved parameters) -> calculation result` (the envelope
   without `result_id`, decision 12). A later C/C++
   implementation replaces the body behind that signature; callers do not change.
2. **Conversion and applicability sit inside the engine boundary, outside the formulas.**
   The boundary adapter converts inputs to base units and runs the applicability check,
   then calls the formulas. Both steps are deterministic, so the whole call stays pure.
3. **A refusal is an envelope, not an exception.** An input outside the method's range
   yields an envelope with verdict `refused` and the violated bound. The function stays
   total over valid inputs and valid parameters, and the refusal can be stored, shown,
   and printed like any other result. Invalid parameter data (a formula tree outside the
   allowed set, a symbol without a value, a value that is not finite) is not a refusal: it
   fails with a `DECError` (decision 11), because it is a defect of the data, not a
   property of the inputs.
4. **Verdict values:** `pass`, `fail`, `refused`, with `verdict_reason` naming the
   deciding check and its `step_id`, or the violated bound for a refusal. The domain
   wording of a conclusion (for example "condition satisfied") is a label per calculation
   type, mapped onto these. The existing requirement "Automatic correctness validation"
   is modified to point at `verdict` and `verdict_reason`, so the capability has one
   description of a conclusion. A refused calculation has an empty `trace`.
5. **`result_id` is assigned outside the function.** The service layer assigns it when it
   builds the envelope from the calculation result (decision 12). The determinism check
   compares calculation results, which have no `result_id`.
6. **`input_hash`:** the requirement fixes what goes into it (the calculation type
   identifier, the inputs in base units, and the identity of the resolved parameter set).
   The algorithm is a proposal, open for review: SHA-256 over a canonical serialization
   of those three parts. Refined 2026-09-29 (proposal, still waiting for Egor's
   acknowledgement): the canonical serialization is JSON with sorted keys, no
   insignificant whitespace, and every number written by Python's `repr` of the float
   (the shortest string that reads back to the same value); the identity of the resolved
   parameter set is the SHA-256 of the same canonical JSON of the resolved parameters,
   each value with its `NormRef` list or `EngineerRule`. Two parameter sets that differ in
   one value or in one reference therefore give different hashes. Every number is
   serialized as a float, so `1` and `1.0` hash the same; a number that is not finite
   never reaches the hash, since schema validation and decision 11 reject it. Because a
   `NormRef` is part of the identity, a change of its `status` changes `input_hash`: a
   result computed on an `unverified` reference and one computed after it was verified
   are different results. For the regression corpus of `calculation-verification`, which
   keys entries on `input_hash`, this means a corpus entry is re-recorded when a
   reference it rests on changes status.
7. **`engine_version`** is the released version of the engine package; each calculation
   type may add its own version later. It is a constant in the engine package
   (`ENGINE_VERSION`), equal to the version in `backend/pyproject.toml` and checked
   against it by a test. It is not read from package metadata at call time, since that
   is file access inside the pure function.
8. **"Validated range"** is the roadmap's "validated envelope", renamed so it does not
   clash with the result envelope. Its values come from verification (WP4).
9. **Rounding data at run time:** each output quantity is returned in the envelope's
   `outputs` with its value, unit, `rounding_rule`, and `rounding_source`, so the UI and
   the report read the rule and its source from the envelope, not from the type contract.
10. **Signature block (task 6.5).** The report is a calculation, and GOST R 21.101-2026
    (edition unverified), clause 4.1.7, formats calculations as text documents. Annex E,
    instructions for columns 10-13, makes the signatures of the developer and of the
    person responsible for normative control mandatory and allows a checker line. The
    signature block therefore holds the developer and normative control lines, the
    checker line is optional, and the setting is enabled by default. Disabling it stays
    possible, for example for a draft that does not go into project documentation.
    Source check: the text was read from a copy of the official edition, and the edition
    was matched to the Rosstandart register entry (in force from 2026-04-01, replaces
    GOST R 21.101-2020). The edition stays `unverified` under
    `agent-docs/domain-constraints.md` until the normative pipeline confirms it.

Decisions 11-17 were added on 2026-09-29 after an audit of this change for
implementation and revised after the `spec-reviewer` pass of the same day. The testable
rules among them are also stated in the requirements of the `calculation-engine` delta;
the decisions give the shapes and the rationale. None of them fixes a norm value.

11. **Formulas are data, the method structure is code (option D).** A formula, a
    coefficient, and a threshold that chooses between branches of a method, where a norm
    gives it, never appear as a literal in code or in a `.yaml` file
    (`backend-layered-architecture` "No hardcoding"). They reach the engine inside the
    resolved parameters: each formula as an expression tree (JSON), next to its LaTeX,
    its `NormRef` list, and the unit bound to each of its symbols; each coefficient and
    threshold as a value with its unit and its `NormRef` list. The code of a calculation
    type holds only the order of the method: which formula to evaluate, which table
    value to use, which threshold decides a branch, and which checks run. An interpreter
    in the engine evaluates the tree ("Formula evaluation from data").
    - Allowed nodes: `number` (a constant printed in the formula itself), `symbol` (a
      quantity bound to an input, a parameter, or the result of an earlier step), the
      binary operations `add`, `sub`, `mul`, `div`, `pow`, the unary `neg`, and `call`
      of a function from a closed list kept in the engine. The first list is `sqrt`,
      `exp`, `ln`, `log10`, `sin`, `cos`, `tan`, `abs`, `min`, `max`; a function is added
      only when a formula of an in-scope type needs it.
    - Limits: depth at most 64 and at most 4096 nodes per tree. These are guards against
      malformed machine-extracted data, not norm values.
    - The interpreter checks the whole tree (node kinds, functions, limits, symbol
      bindings) before it evaluates any node, and fails with a `DECError` on the first
      problem. A value that is not a finite number (for example a division by zero or
      `sqrt` of a negative number) fails the step with a `DECError` that names the step.
    - The tree types (`ExpressionNode` and its kinds) live in `schemas`, next to the
      other types that cross layers, so `engine` imports them from `schemas` only.
    - The engine never uses `eval`, `exec`, `sympify`, `parse_expr`, or `lambdify`. The
      LaTeX-to-tree conversion happens at ingestion, in the normative pipeline (Egor's
      zone), not in the backend.
    - A formula step's `expression` is the formula's LaTeX from the catalog, so the
      transparent output shows the formula as the norm prints it; `substitutions` are
      built from the tree's symbols and their bound values; the unit of `result` is the
      unit bound to the formula's result symbol.
    - Rationale: satisfies "No hardcoding" without editing it, keeps untrusted string
      parsing out of the calculation path (see "Risks"), and needs little code for one
      pilot type. A fully declarative method scheme stays possible later, when there
      are many types.
    - Open for Egor: the tree field on a stored formula and the binding of formula
      symbols to quantities with units
      (`docs/decisions/calculation-core-contract-formula-execution-akim.md`, task 1.8).
12. **The engine returns a calculation result; the service returns the envelope.** The
    pure function returns a `CalculationResult`: every field of the result envelope
    except `result_id` ("Pure calculation function"). The service layer assigns
    `result_id` (a UUID) and builds the `ResultEnvelope`, in which no field is null. The
    determinism check (task 2.3) compares `CalculationResult` values. Storing the
    envelope in `dec_app` and the calculation endpoint belong to a later change. In this
    change task 2.4 is the service that assigns `result_id`, and task 5.3 tests schema
    validation on the request schema `CalculationRequest` (calculation type name, and
    each input as a value with its unit) and on the service, without HTTP. The HTTP
    scenarios of `security` "Input validation" are tested by the change that adds the
    endpoint.
13. **Units.** A unit is a symbol from a closed vocabulary kept in `schemas`, each with
    its dimension and its factor to the base unit of that dimension. Unit symbols and
    conversion factors are definitions of the units, not norm values. A dimensionless
    quantity has the unit `1`. The unit of an input is checked twice: by the request
    schema (`CalculationRequest`, `security` "Input validation"), which rejects a unit
    outside the vocabulary or of another dimension than the declared base unit; and by
    the engine boundary, which raises a `DECError` for the same cases when the engine is
    called directly. Neither case is an applicability refusal. Outputs leave the engine
    in their base units. `pint` is not used: its registry reads its definitions file,
    and the vocabulary needed by the pilot is small.
14. **Rounding.** A `rounding_rule` is a number of decimal places and a mode, `half_up`
    or `half_even`; both come from the rule's source, never from the implementer. The
    float value is turned into `decimal.Decimal(repr(value))`, the shortest decimal that
    reads back to the same float, and rounded with `Decimal.quantize` in the rule's mode;
    the float `round()` is not used. Only the values in the envelope's `outputs` are
    rounded. Trace steps and check steps use unrounded values, so the verdict does not
    depend on presentation. This is an engine design choice with no norm source: it
    treats `rounding_rule` as a rule for presenting an output, which is what the
    requirement fixes. If a norm of an in-scope type requires a check on a rounded value,
    that rounding is a step of the method, with its own `NormRef`, run before the check,
    not the `rounding_rule` of an output. A `rounding_source` is a `Source`. The engineer-set parameter
    file of `backend-layered-architecture` holds only rules whose source is an
    `EngineerRule`; a rule whose source is a `NormRef` list comes from the normative
    catalog, through the path `normative-catalog-backend` adds. The `RoundingRule`
    schema of `backend-layered-architecture` (task 5.1) is split into the rule and its
    source by task 4.3.
15. **Applicability data.** The method's range and the validated range are both lists of
    bounds. A bound is `{quantity, kind, value, inclusive, source}`: `kind` is `min` or
    `max`, `value` is in the quantity's base unit, and `inclusive` says whether the value
    itself is inside the range (the norm's wording, such as "not more than" or "less
    than", decides it). For the method's range `source` is a `NormRef` list; for the
    validated range it is a `Source`. Bounds apply to one input each; a bound that ties
    several inputs together (a ratio, for example) is out of scope of this change and
    would need a new requirement. When several bounds of the method's range are
    violated, `verdict_reason` names the first in the order the type declares them;
    warnings follow the declared order of the validated range's bounds, and each warning
    records the input, the violated bound, and that bound's `Source`. The
    `ValidatedRange` schema of `backend-layered-architecture` (task 5.1: `min_value`,
    `max_value`, `EngineerRule` only) is replaced by this bound form in task 5.1 of this
    change; its parameter file keeps only bounds whose source is an `EngineerRule`.
    Bounds of the method's range come from the norm, so they are not in the engineer-set
    parameter file; until `normative-catalog-backend` adds the path from
    `dec_normatives`, task 5.1 defines the types only and the tests use synthetic bounds.
16. **Trace steps, checks, and `verdict_reason`.** A trace step is a formula step, a
    table step, or a check step ("Typed trace step"); all three carry the five fields.
    `substitutions` is a list of `{symbol, value, unit}`.
    - A table step's `expression` is LaTeX of the form `<symbol> = <table value>` built
      from the symbol of the value, never from a number; its `substitutions` are the
      values that select the table entry; its `result` is the entry with the unit stored
      for it; its `norm_refs` are those of the entry. A branch is not a step: it only
      decides which steps run, and its threshold is a parameter with its own `NormRef`.
    - A check step records `operator` (`le`, `lt`, `ge`, `gt`), its `result` (the left
      value with its unit), `right` (the right value with its unit), and `passed`. Its
      `expression` is the comparison in LaTeX built from the two symbols.
    - Whether a step counts as verified is computed from its `norm_refs`, not stored
      separately.
    - Every calculation type declares at least one check in its contract, and a contract
      without one cannot be registered, so a result that is not refused always has a
      deciding check. The verdict is `fail` when any check did not pass, decided by the
      first failed check in trace order; otherwise `pass`, decided by the last check in
      trace order ("Automatic correctness validation").
    - `verdict_reason` is typed: for `pass` and `fail` it holds the deciding check's
      `step_id`; for `refused` it holds the violated bound, the input value with its
      unit, and the bound's `NormRef` list.
17. **Order of the envelope's lists** ("Result envelope"). `trace` is in run order;
    `outputs` in the declared order of output quantities; `warnings` in the declared
    order of the validated range's bounds. `norm_refs` and `engineer_rules` each list
    every item once, in the order of first use: trace steps in order, then the bound that
    refused the calculation, then rounding sources in the order of `outputs`, then
    warnings. A refused envelope has no `outputs`, so it holds no rounding source. Two
    `NormRef` are the same item when all five fields are equal; two `EngineerRule` when
    `engineer` and `rationale` are equal. Equal lists in equal order are needed for the
    bit-for-bit comparison of "Pure calculation function".

## NormRef (agreed with Egor)

This section records the shared interface from roadmap section 3 and Akim's answers to
the eight open questions. Egor agreed to the shape and to all eight resolutions in
writing in `docs/decisions/normref-questions-egor.md` (commit `a1a896c`, 2026-09-27);
task 1.3 was first closed on 2026-09-26 on Akim's word. Egor owns the catalog side
(WP3, `norm-source-traceability`). The delta specs use this shape (`norm_refs`,
`Source`, `engineer_rules`).

    NormRef {
      document:   string                       # designation as printed in the document; always concrete
      edition:    string | unverified
      clause:     string | unverified          # one locator: a clause, a table, or a formula
      status:     verified | unverified
      provenance: human-verified | machine-extracted
    }
    Invariant: status = verified implies edition and clause are concrete.
    Invariant (2026-09-29, resolution 2 amendment; pending Egor's acknowledgement, task
    1.8): provenance = machine-extracted implies status = unverified.
    Both invariants follow from the meaning of verified that the `normatives-catalog`
    requirement "Norm reference status" (WP1) owns, and the field format is WP3's
    (`norm-source-traceability`). This change does not restate them as a requirement; it
    enforces them in the backend `NormRef` schema (task 3.1).

    EngineerRule {engineer, rationale}

    Step.norm_refs: NormRef[]                  # at least one
    Source = NormRef[] (at least one) | EngineerRule

- No field may be null.
- `unverified` is a reserved literal: a union in code, a string in serialization.
- The meaning of verified and unverified is owned by the `normatives-catalog`
  requirement "Norm reference status" (WP1). This change only carries the value.
- Wherever this change names a source, it means a `Source`: one or more `NormRef`, or an
  `EngineerRule`. An `EngineerRule` is allowed only for a `rounding_source` and for the
  source of a validated range. The bounds of the method's range and the sources of trace
  steps are `NormRef` lists only.

### Resolutions

1. **`status` is the verification status only** (`verified` or `unverified`). The
   document status (in force, superseded, withdrawn; WP3 requirement 2) is not a field of
   `NormRef`: it changes over time, and a pinned reference must not. It is read from the
   catalog by `(document, edition)` when it is shown. The marker `source: unverified`
   (`domain-constraints.md`, WP1) is how a `NormRef` with `status = unverified` is
   displayed; the data lives in the fields, the marker is a display form. A named edition
   that nobody has checked is `status = unverified` with a concrete `edition`.
2. **`provenance` values are final for the MVP:** `human-verified` and
   `machine-extracted`. `provenance` says where the value came from; `status` says
   whether the reference was checked against the source text. A `machine-extracted`
   value has `status = unverified` until a person checks it, and then becomes
   `human-verified`. ~~The parameters layer rejects `machine-extracted` values, so they
   never reach the engine (WP3 requirement 4).~~ Superseded for the MVP by the amendment
   below.
   Amended 2026-09-29 (Akim; needs Egor's acknowledgement). Egor's pipeline now marks
   every formula as verified automatically, with no person checking it
   (`docs/decisions/pipeline-followup-answers-egor-rus.md`, A1, accepted in
   `pipeline-followup-answers-akim.md`, A1). That flag is not `NormRef.status`:
   - `status = verified` still means that a person checked the reference against the
     primary source text, as the `normatives-catalog` requirement "Norm reference
     status" defines it. A `NormRef` with `provenance = machine-extracted` always has
     `status = unverified`; the backend enforces this when it builds the `NormRef`,
     whatever flag the catalog row carries. In this change the `NormRef` schema rejects
     the combination (task 3.1 tests it); building a `NormRef` from a catalog row is
     `normative-catalog-backend`'s, and it inherits the rule through that schema.
   - For the MVP the parameters layer does not reject `machine-extracted` values. They
     reach the engine, and every step that rests on one of them is marked unverified and
     counted in `unverified_step_count`, as in the WP1 scenario "Unverified norm
     source". Otherwise no calculation could run, since no value is `human-verified`
     yet. Whether to reject them again is a later decision of `normative-catalog-backend`.
3. **A rule set by the engineer is a separate source type**, `EngineerRule`, not a
   `NormRef` with a reserved `document`. A reserved document would leak into every
   consumer of `NormRef` and into the traceability metric. It is visible in the envelope
   and in the report as engineer-set. This is also Akim's reading of
   `agent-docs/domain-constraints.md` ("implementer" is the software developer, not the
   design engineer who fills the parameter data); Egor confirmed this reading in
   writing (answer 3).
4. **`unverified` is a union value in `edition` and `clause`. `document` is never
   `unverified`:** it is always a concrete designation. A parameter whose document is
   unknown has no source, and schema validation fails (WP3 requirement 1). The synthetic
   placeholder `<NORM-DOC-PLACEHOLDER>` is allowed only in spec examples and tests, as in
   WP1.
5. **`clause` holds one locator** (a clause, a table, or a formula), as an opaque
   string. A step that rests on several clauses, tables, or documents carries several
   `NormRef` in `norm_refs`; two references of one document repeat `document` and
   `edition`. A step is verified only when every one of its references is `verified`, and
   it counts as unverified in `unverified_step_count` when any of them is not. The "clause
   set" that a stored result is pinned to (WP3 requirement 3) is the set of all locators
   of all references of all steps. The locator syntax is Egor's (answer 5): the loader
   normalizes it and the catalog resolves it; the engine keeps it opaque. Settled with
   Egor on 2026-09-27 (`docs/decisions/normatives-formula-contract-review-egor.md`,
   question 10): a formula that the document prints without a number is located by its
   clause in his canonical grammar, never by an invented number
   (`agent-docs/domain-constraints.md`); a synthetic internal id, if the pipeline needs
   one, stays outside `NormRef` (his payload carries it as `formula_id`).
6. **`document` is a designation string,** as printed in the document, not a key into
   `dec_normatives`. It reads well in the parameter YAML, in the `dec_app` columns, and in
   the report, and needs no foreign key across the two databases (B3). The catalog
   resolves `(document, edition)` uniquely and normalizes spelling. For `status =
   verified` the pipeline checks that the pair exists in `dec_normatives`.
7. **A `NormRef` in a stored result is immutable.** Its values are copied into the
   `dec_app` columns and never change. In the catalog and in `params/`, a change (for
   example `unverified` to `verified`) creates a new version of the reference: new runs
   take the new one, old results keep the old one. The `status` in a stored result is the
   status at the time of the calculation. The flag "edition superseded" is computed from
   the catalog when the result is shown; it is not stored.
8. **`edition` is an opaque string** that identifies one exact text version: the year of
   the edition, plus a marker for the amendments applied, when there are any (written
   `<YYYY>` or `<YYYY>+<amendment>` in examples). It is compared for equality only. Egor
   set the syntax in answer 8: `<YYYY>` for an edition without amendments and
   `<YYYY>+<N>` with amendment No. N applied; the catalog also keeps the amendment number
   as a separate field `amendment_no` of `Revision`. The engine depends on the string only
   through equality, so this change carries the syntax by reference and names no real
   edition.

Effects on the other requirements of this change, applied to the deltas on 2026-09-26:

- The typed trace step field `norm_ref` becomes `norm_refs`, a list of at least one
  `NormRef`.
- `rounding_source` and the source of the validated range are a `Source`; each bound of
  the method's range carries a `NormRef` list. Since 2026-09-29 (decision 15) each bound
  of the validated range carries its own `Source`.
- The envelope's `norm_refs` is the set of all `NormRef` used; `EngineerRule` sources are
  listed in the envelope's `engineer_rules` and are not part of it.
- The traceability metric of `calculation-verification` counts the steps whose
  references are all `verified`, over the steps of non-refused envelopes, and counts
  engineer-set sources separately.

Engineer-set rules and `domain-constraints.md`: that file says "Rounding and tolerance
rules come from the norm, not from the implementer." This change reads "implementer" as
the software developer, who never chooses a rule; the engine never chooses one either.
The design engineer who fills the parameter data is a different actor and may set a rule
where the norm gives none, with the rule recorded as an `EngineerRule` and visible in the
envelope and the report.

Wording clash, settled by resolution 1: `agent-docs/domain-constraints.md` and the WP1
deltas (`retarget-mvp-domain`: `normatives-catalog` "Norm reference status",
`transparent-output` "Detailed calculation display") use the marker `source: unverified`.
That marker is the display form of a `NormRef` with `status = unverified`.

Handoff to WP3 (`norm-source-traceability`, Egor). This is a record for WP3, not a
question that task 1.3 must answer:

- The base spec `report-generator`, requirement "GOST-compliant report assembly", names
  GOST R 21.101-2020 as settled. That edition has not been checked against the source
  text, so under `agent-docs/domain-constraints.md` it is `unverified`.
- The Rosstandart register lists GOST R 21.101-2026 as in force from 2026-04-01,
  replacing GOST R 21.101-2020 (order No. 129-ст of 2026-02-12). The base requirement
  therefore names a replaced edition.
- This change writes "GOST R 21.101-2026 (edition unverified)" in its own text and does
  not edit the base requirement. After this change archives, the capability names the same
  document both ways until WP3 either confirms the edition from the source text or marks
  it `unverified` in that requirement.

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
  - **Update 2026-09-28:** WP5 was revised and split. Its task 6.2 and the placeholder
    pilot moved to this change's task 7.1; decision 7 now names the pure function as the
    C/C++ boundary; "No hardcoding" now says formulas and coefficients come from
    `dec_normatives`, not from a parameter file, and `params/**/*.yaml` holds only
    engineer-set values. Of the points below, only the safe parsing of `expression` and
    the pipeline verification state for the `provenance` gate stay open (task 7.2).
  - **Update 2026-09-29:** both points are settled here. Formulas are evaluated as
    expression trees, never parsed from strings in the engine (decision 11); the gate
    passes `machine-extracted` values with `status = unverified` for the MVP (resolution
    2, amendment). What remains for WP5 and `normative-catalog-backend` is the path from
    `dec_normatives` to the resolved parameters.
  - "Parameters stored in YAML" says the parameters layer passes parameters to the
    engine as typed arguments. This agrees with "Pure calculation function".
  - Task 6.2 ("reference implementation reading parameters from the parameters layer")
    implies I/O inside the engine and conflicts with "Pure calculation function" (B5).
    Decision 7 of its `design.md` names a placeholder-domain reference implementation.
    Neither file is edited here; `tasks.md` holds the sync task for WP5.
  - "No hardcoding" says formulas are not written in code but read from configuration or
    a parameter file. If formulas live in YAML, the engine becomes an expression
    evaluator, which changes where a step's `expression` comes from. This is an open
    question for WP5 and is not decided here; task 7.2 settles it. Egor agreed on
    2026-09-27 (`docs/decisions/normatives-formula-contract-review-egor.md`, question 2):
    the pipeline writes formulas into `dec_normatives`; the parameters layer reads them,
    applies the `provenance` gate (resolution 2), and passes resolved parameters to the
    engine; the backend does not import pipeline code, so the zones stay apart. He owns
    the hand-entered formula registry (`normatives_pipeline/formulas.toml`, merged to
    `develop` in `b44d6f3`), which stays the MVP path for executable expressions. Its
    `norm_ref` was also brought in line with the agreed `NormRef` in that commit. Egor
    agreed on 2026-09-28 to the remaining findings 11-15
    (`docs/decisions/normatives-formula-contract-review-egor.md`): a `NormRef` on every
    stored coefficient value, `status`/`provenance` stored per formula and per
    coefficient instead of constants, the five `NormRef` fields built unconditionally in
    code (config selects only extra fields), and no payload built from an empty
    `document`. Applied on `feature/normative-parser/ml` (commit `a28cf0a`), not merged
    into `develop` yet.
    Since 2026-09-27 (his `research-journal.md`, entry 10) the direction changed: OCR
    (pix2text + DocLayout-YOLO) is now the main source of formulas at scale, each one
    entered as `provenance = machine-extracted`, `status = unverified`; the hand-entered
    registry becomes the checked subset, stored as `human-verified` at ingestion (answer
    12). How a formula moves to `human-verified` by a user action, as opposed to the
    registry's own entries, is still the open question in
    `docs/decisions/formula-verification-akim.md`, not yet answered.
    Update 2026-09-29 (`docs/decisions/pipeline-followup-answers-akim.md`, A1 and A3):
    `formulas.toml` is deleted, so it is no longer the MVP path for executable
    expressions; that path is the expression tree of decision 11. The question of
    `formula-verification-akim.md` is closed: there is no user-side verification action,
    and the pipeline marks every formula as verified automatically, which this change
    does not carry into `NormRef.status` (resolution 2, amendment).
- **`report-generator` "GOST-compliant report assembly"** names GOST R 21.101-2020; that
  edition is not checked against the source text. Handed to WP3 in section "NormRef"
  (task 7.3); not edited here.
- **`retarget-mvp-domain` (WP1)** removes "Deterministic verified calculation" and
  modifies "Detailed calculation display"; this change touches neither, and WP1 archives
  first. WP1 task 2.1 (Akim confirms the WP1 engine and output deltas match this
  contract) closed on 2026-09-27 after three WP1 scenarios were aligned with this
  contract (`docs/decisions/retarget-mvp-domain-akim-review.md`; task 8.2).

## Non-functional requirements

- Performance: unchanged; the existing "Non-functional — performance and accuracy"
  requirement applies. Its "99.9% accuracy" figure has no measurable definition yet;
  making it measurable is deferred to WP4 (`calculation-verification`), which replaces
  that requirement; this line is stale once WP4 archives.
- Determinism: bit for bit on the same platform (see "Pure calculation function").
- Accessibility: warnings and refusals are readable without colour (see
  `transparent-output`).
- Coverage: >= 95% branch coverage for the contract code, per the DOD.
- Security: the envelope holds no credentials; `input_hash` holds no raw input.

## Risks

- `NormRef` changes after agreement ripple through three specs. Mitigation: all three
  refer to it by name and never restate its fields.
- The signature-block rule rests on an edition that is still `unverified` (decision 10).
  Mitigation: it is one setting, so a correction after the normative pipeline confirms
  the edition changes a default or a line, not the report structure.
- If formulas come from data (see "Consistency with other specs"), the engine turns an
  `expression` string into executable code. SymPy's `sympify` and `parse_expr` use
  `eval`, and `lambdify` generates code, so an unchecked string is code execution, and a
  `machine-extracted` formula could reach the calculation path. Sharper since
  2026-09-27: OCR now writes most formulas as `machine-extracted`/`unverified` at scale
  (see above). Egor agreed on 2026-09-28
  (`docs/decisions/normatives-formula-contract-review-egor.md`, answer 12) to store
  `status` and `provenance` as columns per formula and per coefficient instead of
  constants, so the `provenance` gate has something to key on once that code reaches
  `develop` (currently on `feature/normative-parser/ml`). Still open: the user action
  that moves a formula to `human-verified` (`docs/decisions/formula-verification-akim.md`)
  is not designed yet, so no value reaches `human-verified` except the hand-entered
  registry, which his answer marks `human-verified` at ingestion, not by that action.
  Mitigation as first written (superseded by the next paragraph and by the amendment of
  resolution 2), to be fixed when task 7.2 settles where formulas live: expressions are
  parsed against a whitelist of symbols and operations, never passed to `eval`-based
  parsing as is, and only values that pass the `provenance` gate of the parameters layer
  (resolution 2) reach the engine.
  Settled 2026-09-29 by decision 11: the engine parses no string. It interprets an
  expression tree built at ingestion, with a closed set of nodes and functions, and
  fails on anything else. A wrong `machine-extracted` formula can still reach the
  engine for the MVP (resolution 2, amendment); it is then computed correctly from a
  wrong tree and shown as unverified. The reference examples of
  `calculation-verification` are what catch a wrong formula.
- Unit conversion in floating point is not always exact (a value converted to its base
  unit and back may differ in the last bit), so the unit-consistency invariant of
  `calculation-verification` needs a tolerance, and two inputs that differ only in their
  unit may give different `input_hash` values. Mitigation: conversion happens once, at
  the boundary (decision 13); the tolerance of the invariant is set in
  `calculation-verification`, not here.
- The pilot (task 7.1) may need coefficient tables. The candidate first type, R by
  formula 5.7 of СП 22.13330.2016 (`unverified`), takes coefficients from a table.
  Egor added table storage on 2026-09-27 (`b44d6f3`, starting with table 5.5 of
  СП 22.13330.2016, `unverified`) and agreed on 2026-09-28
  (`docs/decisions/normatives-formula-contract-review-egor.md`, answer 11) to add a
  `NormRef` per stored coefficient value, starting with that same table
  (`normatives-formula-contract` tasks 1.4-1.7). Not merged into `develop` yet; until it
  is, he takes `M_γ`, `M_q`, `M_c` for the pilot from his own manually transcribed copy
  of that table in the registry (his answer to question 7), which is a stopgap for the
  pilot, not a primary-source check. Update 2026-09-29: the registry `formulas.toml` is
  deleted, so that stopgap is gone, and the other coefficients of the formula have no
  named source in the pipeline yet (question to Egor in
  `docs/decisions/calculation-core-contract-formula-execution-akim.md`). Task 7.1 is
  split: 7.1a and 7.1b build the pilot on synthetic data, 7.1c runs it on catalog data.
  Mitigation: only task 7.1c depends on it, and it starts when the table data is
  available with its `NormRef`; tasks 7.1a and 7.1b use the candidate type's working
  name with synthetic data, and the other tasks of this change do not use a real
  calculation type.
