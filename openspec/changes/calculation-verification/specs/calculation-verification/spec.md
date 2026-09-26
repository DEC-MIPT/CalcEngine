# Calculation Verification

## Purpose
A gate on the correctness of calculations, not only on code coverage. Results are
checked against named reference examples, a frozen regression corpus, and invariants,
and each run reports metrics.

## ADDED Requirements

### Requirement: Reference examples
The system SHALL ship every calculation type of the first domain (`foundations-shallow`)
with at least 3 reference examples. Each reference example SHALL record: `example_id`;
the calculation type; the inputs, each with its unit; the expected outputs, each with its
unit; for every expected output a `tolerance`, a `tolerance_kind` (`absolute` or
`relative`), and a `tolerance_source`; an `origin`, one
of `manual calculation`, `textbook`, or `norm application`; a source citation (the
document, its year, and the page or example number); and `source_norm_edition`, the norm
edition the example was calculated with, which may be the literal `unverified`. The
`tolerance` of each quantity is set by the engineer who fills the example; this
requirement fixes the fields, not a value. An output is within its tolerance when the
absolute difference between the computed and the expected value is not more than the
`tolerance` (`absolute`), or not more than the `tolerance` times the absolute expected
value (`relative`). The calculation types are those listed in the requirement "In-scope
calculation types" of the capability `foundations-shallow` (delta of
`retarget-mvp-domain`, not yet archived). For `foundations-shallow` the `origin` of every
example is `textbook`, and the source is a methodical guide for students on the design of
shallow foundations that contains worked calculation examples.

#### Scenario: Reference suite within tolerance
- **WHEN** the reference suite runs and every output of every example is within its
  `tolerance` of the expected value
- **THEN** the reference check passes

#### Scenario: A quantity outside its tolerance
- **WHEN** the reference suite runs and any output of any example is not within
  its `tolerance`
- **THEN** the verdict is NO-GO, and the report names the example, the quantity, the
  computed value, the expected value, and the `tolerance`

#### Scenario: Too few or incomplete examples
- **WHEN** a calculation type has fewer than 3 reference examples, or an example lacks
  a `tolerance` or `tolerance_kind` for any expected output, an `origin`, a source citation, or
  `source_norm_edition`
- **THEN** the reference suite is invalid and the verdict is NO-GO

### Requirement: Regression corpus
Depends on the result envelope of `calculation-core-contract` (`input_hash`,
`engine_version`, `outputs`, `verdict`). The envelope has no edition field; `input_hash`,
which covers the parameter-set identity, stands for the edition in the entry key.

The system SHALL keep a frozen corpus of entries `(calculation type, inputs, edition) ->
outputs and verdict`, and SHALL recompute every entry on every change. Each entry also
records the `input_hash` and the `engine_version` from the result envelope defined by
`calculation-core-contract`. The comparison covers the envelope's `outputs` and
`verdict` and does not use `result_id`, which the service layer assigns.

#### Scenario: Result unchanged
- **WHEN** every corpus entry is recomputed and its outputs and verdict equal the stored
  ones
- **THEN** the regression check passes

#### Scenario: Undeclared difference
- **WHEN** a recomputed entry differs from the stored one and the change does not declare
  that difference
- **THEN** the build fails and names the entry, the differing quantity, and the
  `engine_version` of both runs

#### Scenario: Declared difference
- **WHEN** a recomputed entry differs and the change declares the difference in a
  section "Declared result differences" of its `proposal.md`, naming the entry
  identifier, the old and the new value of each differing quantity, and the reason
- **THEN** the regression check passes for that entry, and the corpus is updated in the
  same change

### Requirement: Invariant tests
The system SHALL list, for each calculation type, the invariants that hold whatever the
norm says, and SHALL provide a property-based test for each. Two invariants apply to
every calculation type: determinism (the requirement "Pure calculation function" of
`calculation-core-contract`, not restated here) and consistency when an input is given in
a different unit (the requirement "Explicit units at the boundary" of
`calculation-core-contract`, not restated here). Further invariants per calculation type
are to be confirmed by the engineer; this requirement fixes the structure of the list
(identifier, statement, quantities involved), not its content. The number of generated
cases and the tooling are decided in the planned change `bootstrap-dev-environment`.

#### Scenario: Invariants hold on random inputs
- **WHEN** inputs are generated at random within the valid range declared for the
  calculation type, with the seed recorded in the test report so a failing run can be
  repeated
- **THEN** every listed invariant holds for every generated input

#### Scenario: Invariant without a property test
- **WHEN** a listed invariant has no property-based test
- **THEN** the verification is incomplete and the verdict is NO-GO

### Requirement: Metrics per run
The system SHALL compute, for every verification run, the metrics "deviation from the
references", "reproducibility rate", and "traceability completeness", and SHALL attach all
three to the GO verdict of the tester.

- **Deviation from the references:** for each expected output of each reference example,
  the computed value minus the expected value, in the unit of the quantity, reported next
  to that quantity's `tolerance`. No aggregate percentage is reported.
- **Reproducibility rate:** each reference example is run twice on the same platform
  with identical inputs and parameters; the rate is the number of examples whose two
  result envelopes are identical, excluding `result_id`, divided by the number of
  examples. A rate below 100% is a determinism failure and the verdict is NO-GO.
- **Traceability completeness:** the number of trace steps that count as verified (every
  `NormRef` in the step's `norm_refs` is verified), divided by the number of trace steps,
  over the envelopes of the run that are not refused. The number of steps that do not
  count as verified is the envelope's `unverified_step_count`. Sources set by an engineer
  (`engineer_rules`) are not in this ratio; they are reported as a separate count of the
  `engineer_rules` entries. The metric has no threshold and does not by itself decide the
  verdict; it is reported so a reader can see how much of a result rests on unverified
  references.

#### Scenario: Metrics attached to GO
- **WHEN** the tester issues a GO verdict
- **THEN** the deviation from the references, the reproducibility rate, and the
  traceability completeness are attached

#### Scenario: Metrics missing
- **WHEN** the tester issues a GO verdict without one of the three metrics
- **THEN** the verdict is invalid and is treated as NO-GO

#### Scenario: Non-reproducible result
- **WHEN** two runs of a reference example give envelopes that differ other than in
  `result_id`
- **THEN** the reproducibility rate is below 100% and the verdict is NO-GO
