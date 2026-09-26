## ADDED Requirements

### Requirement: Pure calculation function
The system SHALL implement each calculation type as a pure function that takes typed
inputs and resolved parameters and returns a result envelope. The function SHALL NOT
perform file, network, or database access, read the clock, use randomness, or read or
write global or mutable state. Parameters are resolved and passed in by the caller; the
function never loads them itself.

#### Scenario: No I/O during a calculation
- **WHEN** the calculation function runs with the filesystem and the network patched to
  raise on any access
- **THEN** the function completes and returns a result envelope

#### Scenario: Same inputs, same envelope
- **WHEN** the function runs twice with identical inputs and identical resolved
  parameters on the same platform
- **THEN** the two envelopes are identical bit for bit, excluding `result_id`, which the
  service layer assigns when it stores the result

### Requirement: Typed trace step
The system SHALL record every calculation step as a typed trace step with these fields:
`step_id`; `expression`, in a form the transparent output can render; `substitutions`,
each a value with its unit; `result`, a value with its unit; and `norm_refs`, a list of at
least one `NormRef`. A step that rests on several clauses, tables, or documents carries
one `NormRef` per locator. No field may be null. Whether a `NormRef` counts as verified is
defined by the `normatives-catalog` requirement "Norm reference status". A step counts as
verified only when every `NormRef` in its `norm_refs` is verified.

#### Scenario: Every step is complete
- **WHEN** a calculation completes
- **THEN** every step in the trace has `step_id`, `expression`, `substitutions` with
  units, `result` with a unit, and `norm_refs`

#### Scenario: Step without a verified reference
- **WHEN** any `NormRef` in a step's `norm_refs` is not verified
- **THEN** the step stays in the trace, is marked as unverified, and is counted in the
  envelope's `unverified_step_count`; it is never dropped silently

### Requirement: Explicit units at the boundary
The system SHALL attach a unit to every input, output, constant, substitution, and step
result. Each quantity of a calculation type SHALL declare its base unit in that type's
contract. Unit conversion SHALL happen only at the engine boundary, where inputs enter
and outputs leave the engine, and never inside a formula. Each output quantity SHALL
declare a `rounding_rule` and a `rounding_source`, where the source is either a
list of one or more `NormRef` or an `EngineerRule` naming the engineer and the rationale;
the engine never chooses a rule. An `EngineerRule` is allowed only for a rounding rule and
for the source of a validated range, never for a trace step or a bound of the method's
range. At run
time each output quantity is returned in the envelope's `outputs` with its value, its
unit, its `rounding_rule`, and its `rounding_source`. This requirement fixes the fields
only; base units and rounding rules are data filled by the
engineer, not values of this spec.

#### Scenario: Input in a non-base unit
- **WHEN** an input arrives in a unit other than its declared base unit
- **THEN** it is converted at the boundary, and the trace shows the value in the base unit

#### Scenario: Output without a rounding rule
- **WHEN** a calculation type declares an output quantity without a `rounding_rule` or a
  `rounding_source`
- **THEN** the type's contract is invalid and the type cannot be registered with the
  engine

#### Scenario: Rounding rule source is visible
- **WHEN** an output value is rounded
- **THEN** its entry in the envelope's `outputs` holds the value, the unit, the
  `rounding_rule`, and the `rounding_source`, which is a `NormRef` list or an `EngineerRule`

### Requirement: Applicability check with three outcomes
The system SHALL check the inputs of each calculation against the method's range and
against its validated range before computing. The method's range consists of bounds,
each carrying the `NormRef` list it comes from. The validated range is a narrower range in
which the implementation has been checked, and it carries its own source: a `NormRef`
list or an `EngineerRule`. Both are
parameter data, not values of this spec. This check is separate from the schema
validation of the `security` requirement "Input validation", which runs first at the API
boundary and does not know the method's bounds.

#### Scenario: Input inside the method's range
- **WHEN** every input is inside the method's range and inside the validated range
- **THEN** the calculation runs and the envelope carries no applicability warning

#### Scenario: Input outside the method's range
- **WHEN** an input is outside the method's range
- **THEN** the calculation is refused, and the envelope's `verdict_reason` names the
  violated bound, the input value, and the bound's `NormRef` list

#### Scenario: Input outside the validated range
- **WHEN** every input is inside the method's range, but an input is outside the
  validated range
- **THEN** the calculation runs, and the envelope carries a warning that names the input
  and the validated range; the warning is shown in the UI and printed in the report

#### Scenario: Schema validation and applicability check
- **WHEN** a request is malformed or fails its schema
- **THEN** it is rejected by the `security` input validation before the engine runs, and
  the applicability check never replaces that validation

### Requirement: Result envelope
The system SHALL return every calculation, including a refused one, as a result envelope
with these fields: `result_id`, `engine_version`, `input_hash`, `outputs` (each output
quantity with value, unit, `rounding_rule`, and `rounding_source`), `norm_refs` (every `NormRef`
the calculation used: those of the trace steps, of a bound that refused the calculation,
of rounding sources, and of warnings whose source is a `NormRef`), `engineer_rules`
(every `EngineerRule` used as a rounding source or as the source of a warning; a possibly
empty list), `verdict` (one of `pass`, `fail`, `refused`), `verdict_reason`,
`warnings` (each recording the input, the validated range, and that range's `Source`), `trace`, and `unverified_step_count` (the number of trace steps that do not count as verified). `input_hash` SHALL be computed from the calculation type
identifier, the inputs after conversion to base units, and the identity of the resolved
parameter set, so identical inputs and parameters give identical hashes and a change in
either gives a different hash.

#### Scenario: Envelope fields present
- **WHEN** a calculation completes or is refused
- **THEN** the envelope contains every field listed above, and no field is null

#### Scenario: Refused calculation envelope
- **WHEN** a calculation is refused by the applicability check
- **THEN** `verdict` is `refused`, `trace` and `outputs` are empty lists,
  `unverified_step_count` is 0, `verdict_reason` names the violated bound, the input
  value, and the bound's `NormRef` list, `norm_refs` contains that list and the `NormRef`
  of every warning it carries whose source is a `NormRef`, `engineer_rules` holds the
  `EngineerRule` of every warning it carries whose source is one, and `warnings` holds only the validated-range warnings found
  by the applicability check, possibly none

#### Scenario: Identical inputs, identical hash
- **WHEN** two calculations of the same type receive identical inputs and identical
  resolved parameters
- **THEN** their `input_hash` values are equal

#### Scenario: Different inputs, different hash
- **WHEN** two calculations of the same type receive identical resolved parameters but
  inputs that differ after conversion to base units
- **THEN** their `input_hash` values differ

#### Scenario: Different calculation type, different hash
- **WHEN** two calculations of different types receive identical inputs and identical
  resolved parameters
- **THEN** their `input_hash` values differ

#### Scenario: Different parameters, different hash
- **WHEN** two calculations of the same type receive identical inputs but different
  resolved parameter sets
- **THEN** their `input_hash` values differ

## MODIFIED Requirements

### Requirement: Automatic correctness validation
The system SHALL automatically validate each intermediate result and produce a final
conclusion. The conclusion is the result envelope's `verdict` (`pass`, `fail`, or
`refused`) together with its `verdict_reason`, which names the check that decided the
verdict and the `step_id` of that check, or, for a refusal, the violated bound. Domain
wording of a conclusion (for example "condition satisfied / not satisfied") is a label
per calculation type, mapped onto `verdict`.

#### Scenario: Conclusion verdict
- **WHEN** a calculation completes
- **THEN** the engine returns a deterministic `verdict` with a `verdict_reason` that
  names the deciding check and its `step_id`

### Requirement: Step-by-step logging
The system SHALL log every calculation step, including formulas, value substitution,
and intermediate results, for later transparent display. Each step is recorded as a
typed trace step as defined in "Typed trace step".

#### Scenario: Trace the calculation
- **WHEN** a calculation completes
- **THEN** every step, substitution, and intermediate result is available in the trace
