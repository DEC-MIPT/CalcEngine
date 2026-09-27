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
   `human-verified`. The parameters layer rejects `machine-extracted` values, so they
   never reach the engine (WP3 requirement 4).
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
  the method's range carries a `NormRef` list.
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
    `norm_ref` was also brought in line with the agreed `NormRef` in that commit (see the
    review file for what still does not match: `NormRef` fields for coefficients,
    stored `status`/`provenance`, and config-driven `NormRef` keys, its questions
    11-13; also empty `document`, question 15).
    Since 2026-09-27 (his `research-journal.md`, entry 10) the direction changed: OCR
    (pix2text + DocLayout-YOLO) is now the main source of formulas at scale, each one
    entered as `provenance = machine-extracted`, `status = unverified`; the hand-entered
    registry becomes the checked subset. How a formula becomes `human-verified` is the
    open question in `docs/decisions/formula-verification-akim.md`, not yet
    answered.
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
  (see above), and the pipeline has no column yet that records a formula moving to
  `human-verified` (`docs/decisions/normatives-formula-contract-review-egor.md`,
  question 12), so the `provenance` gate below has nothing to key on until that is
  fixed. Mitigation, to be fixed when task 7.2 settles where formulas live: expressions
  are parsed against a whitelist of symbols and operations, never passed to
  `eval`-based parsing as is, and only values that pass the `provenance` gate of the
  parameters layer (resolution 2) reach the engine; that gate needs the pipeline to
  persist verification state (question 12), which is not yet in place.
- The pilot (task 7.1) may need coefficient tables. The candidate first type, R by
  formula 5.7 of СП 22.13330.2016 (`unverified`), takes coefficients from a table.
  Egor added table storage on 2026-09-27 (`b44d6f3`, starting with table 5.5 of
  СП 22.13330.2016), but the stored cells carry no `NormRef` and no verification state
  yet (`docs/decisions/normatives-formula-contract-review-egor.md`, question 11; the
  same gap as question 12 above); until then he takes `M_γ`, `M_q`, `M_c` for the pilot
  from a manually verified copy of table 5.5 in the registry (his answer to question 7).
  Mitigation: only task 7.1 depends on it, and it starts when the table data is
  available with its `NormRef`; the other tasks of this change do not use a real
  calculation type.
