## MODIFIED Requirements

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
  `NormRef` in the step's `norm_refs` is verified), divided by the number of normative trace steps,
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

Engineer_formula steps in the common internal trace and, when exposed by an
accepted public adapter, the external trace SHALL be excluded from numerator and
denominator. A zero normative-step denominator SHALL be reported as N/A with its
zero count, not as 100 percent. Engineer sources remain a separate count.

#### Scenario: Engineer steps do not inflate completeness
- **WHEN** a completed trace includes normative and engineer_formula steps
- **THEN** the ratio uses only normative steps and reports engineer sources separately without an added acceptance threshold

#### Scenario: Zero normative denominator
- **WHEN** a completed internal module trace has only engineer_formula steps
- **THEN** traceability completeness is N/A with zero normative steps and the engineer-source count is retained
