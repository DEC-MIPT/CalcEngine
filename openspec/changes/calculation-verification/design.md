# Design

## Context

Correctness of a calculation is checked against three things: named references, a frozen
corpus of earlier results, and invariants that hold whatever the norm says. This change
fixes the structure of those checks. It fixes no norm value, tolerance, edition, or
clause; those are data that the engineer fills from a primary source.

The roadmap numbers the requirements 1 to 5. Requirements 1, 3, 4, and 5 are in
`calculation-verification`. Roadmap requirement 2 (accuracy replaced, latency separated)
is in `calculation-engine`.

## Goals

- Accuracy is measurable: a deviation of a named quantity from a named reference.
- A result cannot change silently between runs of the code.
- Every GO carries the metrics that show how far the result is from its references.
- The parts that wait for `calculation-core-contract` are visible and separate.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **N = 3** reference examples per calculation type. The audit suggests 3; the team
   agreed. Fewer than 3 makes the reference suite invalid, not merely weak.
2. **First-domain source:** a methodical guide for students on the design of shallow
   foundations, with worked calculation examples. Its `origin` category is `textbook`
   (of `manual calculation`, `textbook`, `norm application`). The engineer fills the
   bibliographic record of the guide, and the numeric references, after this change is
   applied. This design names no title, year, or page. The engineer is Akim (decided
   2026-09-27); what he fills is listed in `docs/decisions/reference-examples-foundations.md`.
3. **Tolerance is data.** Each expected output carries its own `tolerance` and
   `tolerance_source`. The spec fixes no number. The audit's "<= 0.1%" is not used.
4. **Latency split by replacement.** The existing requirement "Non-functional —
   performance and accuracy" is REMOVED, with reason and migration. It is replaced by
   "Calculation accuracy", which points at the references, and by "Calculation latency",
   which carries the 30-second target unchanged. A MODIFIED or RENAMED block would have
   to keep the old scenario "Fast and accurate", which joins both targets; the validator
   requires it. Replacement avoids a title and a scenario that name two things. This
   separation is what E1 lacks today. "Typical calculation" stays undefined; that is an
   open point, not decided here.
5. **`source_norm_edition` per example.** A student guide may calculate with an older
   norm edition than the one the engine implements. An example computed with a different
   edition cannot gate the result. The field records the edition (or `unverified`), so a
   mismatch is visible before the example is used. No edition is named here.
6. **Regression corpus key.** An entry is `(calculation type, inputs, edition) ->
   outputs and verdict` and also stores the `input_hash` and `engine_version` it was
   produced with. `input_hash` covers the type, the inputs in base units, and the
   identity of the resolved parameter set, so it stands for "inputs plus edition" in the
   envelope. `result_id` is never compared (it is assigned by the service layer).
7. **Declaring an intended difference.** Confirmed by Akim on 2026-09-27 (task 1.4):
   the change lists the corpus entry identifier, the old and new values, and the reason
   in a "Declared result differences" section of its `proposal.md`. The build fails for a
   difference that is not declared there.
8. **Invariants: structure only.** Each invariant has an identifier, a statement, and the
   quantities it involves. Determinism and unit-change consistency are shared by all
   types and are referenced, not restated. Invariants specific to foundations are for the
   engineer to confirm; none is invented here.
9. **Reproducibility over the reference examples.** The metric is computed on the
   reference suite, which exists without the regression corpus, so it is not blocked.
   A rate below 100% means the "Pure calculation function" contract is broken, so it is
   NO-GO. Confirmed by Akim on 2026-09-27 (task 1.4): the threshold follows from that
   contract and is not a tunable value.
10. **Deviation is reported per quantity.** No aggregate percentage is computed, because
    quantities have different units and tolerances.
11. **Property-test tool and runner** are decided in `bootstrap-dev-environment`. No
    command is invented here. (Superseded on 2026-10-05 by decision 16:
    `bootstrap-dev-environment` was archived on 2026-10-04 without deciding them.)
12. **Development-process delta** adds a requirement instead of rewriting "Test gate with
    >= 95% branch coverage", because the file is shared with Egor and another active
    change (`team-roles-update`) modifies a neighbouring requirement.

13. **Code location** (added 2026-10-05, Akim, before tasks 2.1-2.4). The reference
    suite runner and its models live in a new package `backend/app/verification/`, not
    in `backend/tests/`: the runner is a tool of the GO gate with its own logic, so it
    is covered by the 95% branch-coverage gate and tested itself. In the `import-linter`
    layers contract of `backend-layered-architecture` decision 2 it is a top layer beside
    `api | worker` (`"api | worker | verification"`), and a forbidden contract lets it
    import from the application only `engine`, `schemas` and `core`; nothing imports
    it.
    - Alternative: the runner in `backend/tests/`. Rejected: it would be outside the
      coverage gate, and untested code would decide GO.
14. **Reference example model and the parameter source** (added 2026-10-05, Akim). A
    reference example is a pydantic model with the fields of the requirement "Reference
    examples"; a missing or empty field makes the example invalid (task 2.2). The runner
    does not decide where the resolved parameters of an example come from: it receives a
    function `resolve(example) -> (parameters, method_range)`. The framework is tested
    with a synthetic calculation type and synthetic parameters. For the pilot
    `foundations_shallow_r` the choice between the catalog, the example's own values, or
    a mix (formulas from the catalog, coefficients from the example) stays open and is
    decided before the first real example runs, together with the file format and the
    place of the real examples.
    - Why: the choice depends on the fixes of the catalog data (WP9 review, B1 and M1)
      and on the pilot's scope (the soil row of `γc1`, `φII` in the cards), neither of
      which the framework needs.
15. **Comparison and the suite report** (added 2026-10-05, Akim). Each computed output
    is converted to the unit of its expected value with `engine.boundary.convert`
    before the tolerance applies, so an `absolute` tolerance stays in the unit the
    engineer wrote it in. The edge of the tolerance is compared with a slack of a few
    units in the last place of the values (`FLOAT_SLACK_ULPS` in the runner), so a
    decimal value exactly on the edge (245.2 against 245.3 with 0.1) stays within it; the
    slack is a floating-point allowance, not part of the tolerance (added 2026-10-21 after
    the `orchestrator` review, finding 1). A refused result, or an expected output the result does not
    hold, fails that example. The suite report holds the verdict (GO, NO-GO, or
    "invalid suite" with its reasons) and, for every example and quantity, the computed
    value, the expected value, the `tolerance` and its kind (scenario "A quantity
    outside its tolerance"). The rule of at least 3 examples (decision 1) is checked
    against the list of calculation types the suite is given (task 2.4).

16. **Property-test tool and number of cases** (added 2026-10-05, Akim, before tasks
    2.8-2.10; replaces decision 11). The tool is Hypothesis, a development dependency in
    `backend/requirements-dev.txt`, so the generating tests live in `backend/tests/` and
    `backend/app/verification/` never imports it. Each invariant runs on 100 generated
    cases per calculation type (`max_examples=100`, the tool's default), without the
    tool's per-case deadline, since the latency requirement is a separate test (former
    task 3.7, a follow-up in `tasks.md` section 5). The seed is recorded in the test
    report: Hypothesis itself prints only the falsifying input, not the seed (checked
    2026-10-05 with Hypothesis 6.168), so `backend/tests/conftest.py` picks a seed when
    `--hypothesis-seed` is not given, hands it to Hypothesis, and prints it in the pytest
    report header (`hypothesis seed: <n>`);
    a run started with `--hypothesis-seed=<n>` repeats it. The example database is off
    (`database=None`), so a run does not depend on earlier local runs.
    - Alternative: a generator of our own on `random.Random(seed)`. Rejected: it would
      add code of our own for generation and lose the shrinking of a failing input.
17. **The two shared invariants and the valid range** (added 2026-10-05, Akim). For a
    calculation type, `backend/app/verification/` holds the list of its invariants
    (identifier, statement, quantities), the valid range of each input the generator may
    use (a lower and an upper bound in a unit of the input, and whether only whole
    values may be drawn, as for an input that selects a table row by whole degrees;
    added 2026-10-06), and a check function per
    shared invariant; the generating test draws inputs inside that range.
    - Determinism (requirement "Pure calculation function"): two calls of the pure
      function with the same inputs and resolved parameters give equal calculation
      results.
    - Unit-change consistency (requirement "Explicit units at the boundary"): an input
      given in a unit other than its base unit gives the same calculation result, field
      for field and without a tolerance, as that input converted to the base unit with
      the engine's own `engine.boundary.convert` and given in the base unit. Both sides
      then reach the formulas with the same floating-point values, so the comparison is
      exact, and a difference can only mean that the unit acts somewhere other than the
      boundary.
    - The valid range is data of the type, like its reference examples: for a synthetic
      type the tests declare it; for the pilot it is filled by the engineer with the
      invariants specific to the type (task 2.11). It is not a norm value and not the
      method's range of application, though it should lie inside it.

18. **Regression corpus: comparison and declared differences** (added 2026-10-05,
    Akim, with tasks 3.2-3.3).
    - A corpus entry is frozen from the result of the pure function: entry identifier,
      calculation type, inputs with their units, the envelope's `outputs` (quantity,
      value, unit) and `verdict`, its `input_hash` and its `engine_version`.
    - Recomputing an entry compares only the `outputs` (quantity, value and unit,
      exactly) and the `verdict`. A changed `input_hash` with the same outputs and
      verdict is not a difference. An output that disappeared or appeared is a
      difference to or from nothing.
    - The section "Declared result differences" of a change's `proposal.md` (decision 7)
      is a table with the columns `Entry | Quantity | Old | New | Reason`, under a
      heading of level 2 or deeper, up to the next heading. A value is written as
      `<number> <unit>` (a unit of the vocabulary), as a verdict (`pass`, `fail`,
      `refused`) for the quantity `verdict`, or as `—` when there is no output. A
      declaration covers a difference only when the entry, the quantity, the old and the
      new value all match; an unreadable row is an error that names its line. A
      declaration that matches no difference is reported, and does not fail the check.
    - Open, decided together with the parameter source of the pilot (decision 14): where
      the real corpus is stored, how its entries get their parameters, and which
      `proposal.md` files a build reads the declarations from.

## Swap boundary

The reference suite, the regression corpus, and the invariant tests call the calculation
only through the pure function `(typed inputs, resolved parameters) -> result envelope`
of `calculation-core-contract` (its decision 1, the C/C++ swap boundary). They read the
envelope and never engine internals. A later C/C++ implementation of a hot path is
checked by the same suites without change. The boundary is defined in that change.

## Second domain (note, not a requirement of this change)

Internal water supply, the second MVP domain, needs its own 3 reference examples per
calculation type and its own decision on the source. Do not assume the source of the
first domain applies. This change does not name a source, an origin, or invariants for
that domain.

## Dependencies on `calculation-core-contract`

Re-checked on 2026-09-26 after `NormRef` was agreed on Akim's word, and on 2026-09-27
after Egor agreed in writing (`docs/decisions/normref-questions-egor.md`, commit
`a1a896c`); his answers change none of the items below. Re-checked on 2026-10-03 after
he accepted the `input_hash` algorithm (`calculation-core-contract` task 1.8): only its
row changes. Re-check again if that change alters an item:

| Item | Used by | Status |
|---|---|---|
| `NormRef` fields, the meaning of `status`, `EngineerRule`, `norm_refs` list on a step | metric "traceability completeness" | agreed with Egor in writing (`docs/decisions/normref-questions-egor.md`, commit `a1a896c`, 2026-09-27; core-contract task 1.3) |
| Definition of "verified" (`normatives-catalog` "Norm reference status") | metric "traceability completeness" | in the unarchived `retarget-mvp-domain`, draft; the field `status = verified` is now defined by `NormRef` |
| Trace step fields (`step_id`, `expression`, `substitutions`, `result`, `norm_refs`) | metric "traceability completeness" | defined in `calculation-core-contract` |
| Envelope fields `outputs`, `verdict`, `norm_refs`, `engineer_rules`, `unverified_step_count` | reference comparison, regression, traceability | defined in `calculation-core-contract` |
| `input_hash` algorithm (SHA-256 over canonical serialization) | regression corpus | accepted 2026-10-03 (Egor's acknowledgement, `calculation-core-contract` task 1.8; it was "a proposal, open for review") |
| `engine_version` meaning | regression corpus | released version of the engine package |
| `result_id` excluded from comparison | regression, reproducibility | stated in "Pure calculation function" |
| Requirement "Pure calculation function" | invariants, reproducibility | stable |
| Requirement "Explicit units at the boundary" | invariants (unit consistency) | defined in `calculation-core-contract` |

Nothing in this change waits for `NormRef` any more. Requirement 3 and the traceability
metric use the envelope and `NormRef` as defined in `calculation-core-contract`. Open
points: the wider definition of "verified" is in the draft `retarget-mvp-domain`, and the
latency test waits for a definition of "typical calculation". The `input_hash` algorithm
is no longer open (accepted 2026-10-03, `calculation-core-contract` task 1.8). Soft dependencies: reference comparison and
reproducibility use the envelope's `outputs` and the exclusion of `result_id`, and the
unit-change invariant uses "Explicit units at the boundary".

## Non-functional requirements

- Performance: the 30-second target is its own requirement; the reference suite and the
  property tests run in the tester's environment, and their duration is not constrained
  here.
- Determinism: bit for bit on the same platform (from `calculation-core-contract`).
- Security: reference examples and the corpus hold no credentials or personal data.
- Coverage: >= 95% branch coverage for the verification code, per the DOD.
- Accessibility: not applicable, no UI.
- Reproducibility across platforms: not required; determinism is bit for bit on the same
  platform. Runtime limits of the suites are not set.

## Risks

- Latency is not testable until "typical calculation" is defined; its test (former task
  3.7) is a follow-up in `tasks.md` section 5, and the requirement is archived without it.
- `calculation-core-contract` changes after agreement. Mitigation: the items
  are listed above; only they are re-opened.
- A published worked example has an error or uses another norm edition. Mitigation:
  `source_norm_edition` and the engineer's per-quantity tolerance; an example the engineer
  does not trust is not admitted.
- Property tests generate inputs the engineer would not consider valid. Mitigation: the
  valid range is declared per calculation type by the engineer.
