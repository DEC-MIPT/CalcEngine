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
    command is invented here.
12. **Development-process delta** adds a requirement instead of rewriting "Test gate with
    >= 95% branch coverage", because the file is shared with Egor and another active
    change (`team-roles-update`) modifies a neighbouring requirement.

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
`a1a896c`); his answers change none of the items below. Re-check again if that change
alters an item:

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
points: the `input_hash` algorithm is no longer open (accepted 2026-10-03, `calculation-core-contract`
task 1.8); the wider
definition of "verified" is in the draft `retarget-mvp-domain`; the latency test waits for
a definition of "typical calculation". Soft dependencies: reference comparison and
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

- Latency is not testable until "typical calculation" is defined; task 3.7 waits for it.
- `calculation-core-contract` changes after agreement. Mitigation: the items
  are listed above; only they are re-opened.
- A published worked example has an error or uses another norm edition. Mitigation:
  `source_norm_edition` and the engineer's per-quantity tolerance; an example the engineer
  does not trust is not admitted.
- Property tests generate inputs the engineer would not consider valid. Mitigation: the
  valid range is declared per calculation type by the engineer.
