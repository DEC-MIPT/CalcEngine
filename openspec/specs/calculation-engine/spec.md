# Calculation Engine

## Purpose
Component 2: a verified calculation engine implemented in Python (NumPy/SciPy) that
executes engineering calculations deterministically, logs every step, and validates
each intermediate result. The architecture must allow hot-swapping hot paths to C/C++
later.

## Requirements

### Requirement: Step-by-step logging
The system SHALL log every calculation step, including formulas, value substitution,
and intermediate results, for later transparent display. Each step is recorded as a
typed trace step as defined in "Typed trace step".

#### Scenario: Trace the calculation
- **WHEN** a calculation completes
- **THEN** every step, substitution, and intermediate result is available in the trace

### Requirement: Automatic correctness validation
The system SHALL automatically validate each intermediate result and produce a final
conclusion. For the existing foundation adapters the conclusion is the result envelope's `verdict` (`pass`, `fail`, or
`refused`) together with its `verdict_reason`, which names the check that decided the
verdict and the `step_id` of that check, or, for an input-bound refusal, the violated bound. Every existing foundation
calculation type SHALL declare at least one check in its contract, and a contract without
one SHALL NOT be registered. A foundation calculation that is not refused has the verdict `fail` when
any check step did not pass, and its deciding check is the first failed check step in the
order the steps ran; otherwise its verdict is `pass`, and its deciding check is the last
check step that ran. Domain wording of a conclusion (for example "condition satisfied /
not satisfied") is a label per calculation type, mapped onto `verdict`.

#### Scenario: Conclusion verdict
- **WHEN** a foundation calculation completes through its external adapter
- **THEN** the engine returns a deterministic `verdict` with a `verdict_reason` that
  names the deciding check and its `step_id`

#### Scenario: Two checks, one fails
- **WHEN** a foundation calculation runs two check steps and only the second does not pass
- **THEN** the verdict is `fail`, and `verdict_reason` names the second check step

#### Scenario: All checks pass
- **WHEN** a foundation calculation runs two check steps and both pass
- **THEN** the verdict is `pass`, and `verdict_reason` names the last check step

#### Scenario: Type without a check
- **WHEN** a foundation calculation type declares no check in its public contract
- **THEN** the contract is invalid and the type cannot be registered with the engine

The common module result SHALL separate execution status and applicability from
ordered check results as defined in calculation-module-contract. It SHALL NOT
require a foundation pass/fail conclusion for an arbitrary internal module. The
foundation adapter SHALL continue requiring its declared checks and deterministic
first-fail/last-pass selection. A stopped module has no final aggregate engineering
conclusion, even if completed diagnostic steps contain individual checks.

#### Scenario: Module check failure is not an execution failure
- **WHEN** an applicable module completes and one of its engineering checks fails
- **THEN** execution remains completed and the foundation adapter returns fail with the first failed check


### Requirement: Hot-swap boundary for C/C++
The system SHALL isolate computational hot paths behind a well-defined boundary so
they can be replaced with C/C++ implementations later without changing callers.

#### Scenario: Swap a hot path
- **WHEN** a hot path is later reimplemented in C/C++
- **THEN** callers remain unchanged because the swap happens behind the engine boundary

### Requirement: Typed input and output contract
The system SHALL define a typed input and output contract per calculation type
(inputs such as loads, geometry, and material grade; outputs such as the result,
trace, and conclusion), validated by schemas at the engine boundary.

#### Scenario: Typed calculation contract
- **WHEN** a calculation type is implemented
- **THEN** its inputs and outputs are defined as typed schemas so callers validate
  inputs before the engine runs and read outputs without reaching into engine internals

The common module boundary SHALL accept schema-defined structured input, resolved
data, execution options and output models. The existing flat quantity mapping SHALL
remain the current public API adapter's contract, not a requirement imposed on
all internal modules. Module diagnostic details SHALL be validated using the
selected module's schema before external adaptation.

#### Scenario: Internal structured contract
- **WHEN** an internal module declares a nested schema and receives valid nested inputs
- **THEN** it executes without changing the existing foundation API input mapping


### Requirement: Table value selectors
The system SHALL give each table value that the engine receives the heading value that
selected it, with the heading's symbol and unit, or no heading value when the table
value depends on no input. Before it uses a table value with a heading value, the engine
SHALL convert the heading value to the base unit of the input named by the heading
symbol, with the same conversion the parameter source uses for the selection, and SHALL
confirm that it equals that input in its base unit. A heading symbol that names no input
of the type SHALL make the engine raise a calculation error. The calculator SHALL name
the input by which its method selects each table value, or none; a table value whose
headings differ from that, such as a value the method selects by an input that comes
without its heading, SHALL make the engine raise a calculation error. The table value's trace
step SHALL list the heading symbol with the heading value as its substitution. This
keeps the engine pure: it looks nothing up and only confirms the selection that the
parameter source made (`normatives-catalog` "Table value selection by heading").

#### Scenario: A heading equal to the input
- **WHEN** the engine receives a table value whose heading value, converted to the
  input's base unit, equals the corresponding input
- **THEN** the engine uses the value, and its step lists the heading symbol and the
  heading value as the substitution

#### Scenario: A heading that does not match the input
- **WHEN** the engine receives a table value whose heading value differs from the
  corresponding input
- **THEN** the engine raises a calculation error before the step is written, the
  response to the calculation request is `500` with code `internal_error`, and nothing is
  stored

#### Scenario: A heading on a symbol that is not an input
- **WHEN** the engine receives a table value whose heading symbol names no input of the
  calculation type
- **THEN** the engine raises a calculation error, the response is `500` with code
  `internal_error`, and nothing is stored

#### Scenario: A heading in a unit other than the base unit
- **WHEN** the heading's unit is not the input's base unit, the client gave the input
  in the heading's unit with the heading's value, and the parameter source selected that
  row
- **THEN** the engine's confirmation passes for the same input

#### Scenario: A table value without a heading
- **WHEN** the engine receives a table value with no heading value, and the method
  selects that value by no input
- **THEN** the engine uses the value without a comparison, and its step has no
  substitution

#### Scenario: Headings other than the method's
- **WHEN** the engine receives a table value that the method selects by an input but
  that has no heading or the heading of another input, or a table value that the method
  selects by no input but that has a heading
- **THEN** the engine raises a calculation error before the step is written, the
  response is `500` with code `internal_error`, and nothing is stored

### Requirement: Deterministic verified calculation of in-scope types
The system SHALL execute engineering calculations with verified algorithms in Python
(NumPy/SciPy) that strictly follow the bound normative method.

#### Scenario: Run a first-domain calculation
- **WHEN** an engineer enters inputs for an in-scope shallow-foundation calculation type
  listed in `foundations-shallow`
- **THEN** the engine computes the result using the verified algorithm bound to that
  type, with no arithmetic drift and no ML influence, and the same inputs and the same
  norm edition give the same result

#### Scenario: Unverified norm source
- **WHEN** a calculation step rests on a norm reference that is not checked against the
  primary text (see `normatives-catalog` "Norm reference status")
- **THEN** the calculation still runs, that step is marked as unverified in the trace,
  the result states how many of its steps are unverified, and no label or conclusion
  shown with the result claims that it is fully verified against the norm

#### Scenario: Out-of-scope type
- **WHEN** an engineer requests a calculation type that is not on the in-scope list of
  `foundations-shallow`
- **THEN** the request is refused before any calculation runs, with a message that names
  the scope limit from `foundations-shallow`; this refusal is about the product scope
  and is separate from refusing inputs that fall outside a method's range

### Requirement: Pure calculation function
The system SHALL implement each calculation type as a pure function that takes typed
inputs, resolved parameters and explicit execution options and returns a typed module
outcome. The module adapter returns a calculation result for its external representation;
for the existing foundation API this has every envelope field except `result_id`. The function SHALL NOT perform file, network, or database
access, read the clock, use randomness, or read or write global or mutable state.
Parameters are resolved and passed in by the caller; the function never loads them itself.
The service layer SHALL build the result envelope from the calculation result by adding
`result_id`.

#### Scenario: No I/O during a calculation
- **WHEN** the calculation function runs with the filesystem and the network patched to
  raise on any access
- **THEN** the function completes and returns a calculation result

#### Scenario: Same inputs, same result
- **WHEN** the function runs twice with identical inputs and identical resolved
  parameters on the same platform
- **THEN** the two calculation results are identical bit for bit

#### Scenario: Envelope built by the service
- **WHEN** the service layer builds result envelopes from two identical calculation
  results
- **THEN** the envelopes have different `result_id` values and are otherwise identical to
  the calculation result

The module's normalization, validation, identity, calculation and adaptation SHALL
not mutate caller inputs, resolved data or options or depend on another call's
mutable state. The common executor SHALL validate module schemas and the neutral
outcome invariants before external adaptation; technical errors are exceptions,
not applicability stops. Existing callers may use a compatible wrapper supplying
the module's explicit default execution options.

#### Scenario: Independent calls preserve their inputs
- **WHEN** two module executions are interleaved with another execution
- **THEN** matching calls return identical results and all supplied objects are unchanged


### Requirement: Typed trace step
The system SHALL record every normative calculation step as a typed trace step with these fields:
`step_id`; `expression`, in a form the transparent output can render; `substitutions`,
each a symbol with its value and unit; `result`, a value with its unit; and `norm_refs`, a
list of at least one `NormRef`. A step that rests on several clauses, tables, or documents
carries one `NormRef` per locator. No field may be null. A normative step is a formula step, a table
step, or a check step:

- a formula step evaluates a formula; its `expression` is the formula's LaTeX, and the unit
  of its `result` is the unit bound to the formula's result symbol;
- a table step takes a value from a table of a norm; its `expression` is LaTeX that names
  the table value by its symbol, its `substitutions` are the values that select the entry,
  and its `result` is the entry with its unit;
- a check step compares two quantities; it also records the comparison operator (one of
  `le`, `lt`, `ge`, `gt`), the right-hand value with its unit, and `passed`; its `result`
  is the left-hand value.

A common internal module trace additionally supports a disjoint engineer_formula
step containing step_id, expression, substitutions and result with explicit units,
and source: EngineerRule. Its source names the engineer and rationale; norm_refs
is forbidden on this variant. Only explicitly reviewed engineering rules may use
this variant; normative formulas, coefficients and method bounds retain their
normative sources. The module declares which engineering rules it adopts.
The existing R public schema continues exposing only its original normative step
variants; a new public adapter requires its own additive contract and acceptance.

Whether a `NormRef` counts as verified is defined by the `normatives-catalog` requirement
"Norm reference status". A normative step counts as verified only when every `NormRef` in its
`norm_refs` is verified.

#### Scenario: Every step is complete
- **WHEN** a calculation completes
- **THEN** every normative step in the trace has `step_id`, `expression`, `substitutions` with
  symbols and units, `result` with a unit, and `norm_refs`, and every check step also has
  its operator, its right-hand value with its unit, and `passed`

#### Scenario: Step without a verified reference
- **WHEN** any `NormRef` in a step's `norm_refs` is not verified
- **THEN** the step stays in the trace, is marked as unverified, and is counted in the
  envelope's `unverified_step_count`; it is never dropped silently

Engineer_formula steps SHALL count as neither verified nor unverified normative
steps. Source summaries SHALL list their EngineerRule once in first-use order.
The shared trace validation SHALL reject duplicate step identifiers.

#### Scenario: Engineer formula retains a distinct source
- **WHEN** an internal module emits an engineer_formula step
- **THEN** its engineer source is required, normative references are forbidden and it is excluded from unverified_step_count

#### Scenario: Normative source cannot be replaced
- **WHEN** an engineering rule is offered as the source for a normative formula, coefficient or method bound
- **THEN** the module's source validation rejects it without promoting the rule to a normative reference


### Requirement: Explicit units at the boundary
The system SHALL attach a unit to every input, output, constant, substitution, and step
result. Each quantity of a calculation type SHALL declare its base unit in that type's
contract. A unit SHALL be a symbol from a closed vocabulary that gives its dimension and
its conversion factor to the base unit of that dimension; a dimensionless quantity has
the unit `1`. Unit conversion SHALL happen only at the engine boundary, where inputs enter
and outputs leave the engine, and never inside a formula. Outputs leave the engine in
their base units. An input whose unit is not in the vocabulary, or whose dimension
differs from that of its declared base unit, SHALL be rejected before any computation:
by schema validation at the API boundary, and by the engine boundary with a `DECError`
when the engine is called without that validation.

Each output quantity SHALL declare a `rounding_rule` and a `rounding_source`, where the
source is either a list of one or more `NormRef` or an `EngineerRule` naming the engineer
and the rationale; the engine never chooses a rule. A rounding rule is a number of
decimal places and a mode, `half_up` or `half_even`. Only the values in the envelope's
`outputs` SHALL be rounded; trace steps and checks SHALL use unrounded values. An
`EngineerRule` is allowed for a rounding rule, a validated-range source, an explicitly
reviewed internal engineer_formula step and an explicitly engineer-adopted derived
applicability guard. It SHALL NOT replace the normative source of a formula,
coefficient, limit or method-range bound. Public variants beyond the existing R
schema require a module adapter contract. At run time each output
quantity is returned in the envelope's `outputs` with its value, its unit, its
`rounding_rule`, and its `rounding_source`. This requirement fixes the fields only; base
units and rounding rules are data, not values of this spec.

#### Scenario: Input in a non-base unit
- **WHEN** an input arrives in a unit other than its declared base unit
- **THEN** it is converted at the boundary, and the trace shows the value in the base unit

#### Scenario: Unknown unit
- **WHEN** an input arrives with a unit that is not in the vocabulary
- **THEN** it is rejected before any computation, and no calculation result is produced

#### Scenario: Unit of another dimension
- **WHEN** an input arrives with a unit whose dimension differs from that of its declared
  base unit
- **THEN** it is rejected before any computation, and no calculation result is produced

#### Scenario: Output without a rounding rule
- **WHEN** a calculation type declares an output quantity without a `rounding_rule` or a
  `rounding_source`
- **THEN** the type's contract is invalid and the type cannot be registered with the
  engine

#### Scenario: Rounding rule source is visible
- **WHEN** an output value is rounded
- **THEN** its entry in the envelope's `outputs` holds the value, the unit, the
  `rounding_rule`, and the `rounding_source`, which is a `NormRef` list or an `EngineerRule`

#### Scenario: Checks use unrounded values
- **WHEN** a check compares a quantity whose rounded output value would change the
  outcome of the comparison
- **THEN** the check and the verdict use the unrounded value

### Requirement: Applicability check with three outcomes
The system SHALL check the inputs of each foundation calculation against the method's range and
against its validated range before computing. Both ranges consist of bounds. A bound
applies to one input quantity, is a lower or an upper bound, holds its value in the
quantity's base unit, and states whether its own value is inside the range. A bound of
the method's range carries the `NormRef` list it comes from. The validated range is a
narrower range in which the implementation has been checked, and each of its bounds
carries a source: a `NormRef` list or an `EngineerRule`. Both are parameter data, not
values of this spec. When several bounds of the method's range are violated, the refusal
names the first of them in the order the calculation type declares them. This check is
separate from the schema validation of the `security` requirement "Input validation",
which runs first at the API boundary and does not know the method's bounds.

#### Scenario: Input inside the method's range
- **WHEN** every input is inside the method's range and inside the validated range
- **THEN** the calculation runs and the envelope carries no applicability warning

#### Scenario: Input equal to a bound
- **WHEN** an input equals the value of a bound of the method's range or of the validated
  range
- **THEN** it is inside that range if the bound states that its value is inside, and
  outside that range otherwise

#### Scenario: Input outside the method's range
- **WHEN** an input is outside the method's range
- **THEN** the calculation is refused, and the envelope's `verdict_reason` names the
  violated bound, the input value, and the bound's `NormRef` list

#### Scenario: Several bounds violated
- **WHEN** inputs violate two bounds of the method's range
- **THEN** the calculation is refused, and `verdict_reason` names the bound that the
  calculation type declares first

#### Scenario: Input outside the validated range
- **WHEN** every input is inside the method's range, but an input is outside the
  validated range
- **THEN** the calculation runs, and the envelope carries a warning that names the input,
  the violated bound of the validated range, and that bound's `Source`; the warning is
  shown in the UI and printed in the report

#### Scenario: Schema validation and applicability check
- **WHEN** a request is malformed or fails its schema
- **THEN** it is rejected by the `security` input validation before the engine runs, and
  the applicability check never replaces that validation

In the common module protocol, applicability SHALL be distinct from execution and
check outcomes. A module MAY additionally stop after computation starts when its
reviewed derived applicability guard fails. Such a stop SHALL retain the completed
diagnostic trace prefix and a generic source-bearing diagnostic whose details
are validated by the module. It SHALL expose no final outputs or aggregate
engineering conclusion. The common executor SHALL know no guard formula or domain
detail field. Existing R input-bound refusal payloads and ordering stay unchanged;
a module's external diagnostic variant is owned by its public adapter contract.

#### Scenario: Internal derived stop
- **WHEN** a module stops after a reviewed applicability guard on intermediate values
- **THEN** the internal result is stopped/not_applicable with its completed diagnostic prefix and schema-valid details, not final outputs

#### Scenario: Incorrect module diagnostics
- **WHEN** a stopped module returns details outside its schema or references a missing retained step
- **THEN** execution raises a calculation error before external adaptation


### Requirement: Result envelope
The system SHALL return every calculation through its declared external adapter. The
existing R foundation adapter returns every calculation, including a refused one, as a result envelope
with these fields: `result_id`, `engine_version`, `input_hash`, `outputs` (each output
quantity with value, unit, `rounding_rule`, and `rounding_source`), `norm_refs` (every `NormRef`
the calculation used: those of the trace steps, of a bound that refused the calculation,
of rounding sources, and of warnings whose source is a `NormRef`), `engineer_rules`
(every `EngineerRule` used as a rounding source or as the source of a warning; a possibly
empty list), `verdict` (one of `pass`, `fail`, `refused`), `verdict_reason`,
`warnings` (each recording the input, the violated bound of the validated range, and that bound's `Source`), `trace`, and `unverified_step_count` (the number of trace steps that do not count as verified). `input_hash` SHALL be computed from the calculation type
identifier, the inputs after conversion to base units, and the identity of the resolved
parameter set, so identical inputs and parameters give identical hashes and a change in
either gives a different hash.

The lists of the envelope SHALL have a fixed order: `trace` in the order the steps ran;
`outputs` in the order the calculation type declares its output quantities; `warnings`
in the order the calculation type declares the bounds of its validated range; `norm_refs`
and `engineer_rules` each hold every item once, in the order of its first use (trace steps
in order, then the bound that refused the calculation, then rounding sources in the order
of `outputs`, then warnings). Two `NormRef` are the same item when all their fields are
equal; two `EngineerRule` are the same item when both their fields are equal.

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

#### Scenario: Reference used twice
- **WHEN** two trace steps carry the same `NormRef`
- **THEN** the envelope's `norm_refs` holds it once, at the position of its first use

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

The common internal outcome is separate from this public envelope and SHALL follow
calculation-module-contract. Other public module adapters SHALL declare and validate
any additive trace or refusal representation in their own capability; the common
executor SHALL NOT assemble domain fields. Internal source summaries include
engineer_formula and diagnostic sources, each once in first-use order: retained
trace, stop diagnostic, output rounding, then applicability warnings. Normative
unverified counts exclude engineer_formula steps. The R adapter SHALL preserve
its original hash algorithm, public payload and source ordering; new modules use
the versioned run identity from calculation-module-contract without rewriting
historical data.

#### Scenario: Pilot external contract is unchanged
- **WHEN** the R compatibility module runs through the common executor
- **THEN** its public envelope and input_hash equal the existing regression expectations

#### Scenario: Internal stop source accounting
- **WHEN** an internal module stops after engineer-sourced and normative trace steps
- **THEN** its summary includes retained steps and diagnostic sources once in first-use order and counts only unverified normative steps
### Requirement: Formula evaluation from data
The system SHALL receive every formula, every coefficient, and every threshold that
chooses between branches of a method, where a norm gives it, as part of the resolved
parameters, never as a literal in the code of a calculation type. Each formula SHALL
arrive as an expression tree together with its LaTeX, its `NormRef` list, and the unit
bound to each of its symbols. The engine SHALL evaluate the tree only through a closed set
of node kinds and functions, within a limit of 64 levels of depth and 4096 nodes per tree
(a guard against malformed data, not a norm value), and
SHALL NOT execute or parse any string of the formula as code. The engine SHALL check the
whole tree before evaluating any node of it. A node or a function outside the set, a tree
over the limit, a symbol with no bound value, or a value that is not a finite number
SHALL fail the evaluation with a `DECError`. The code of a calculation type holds only the
order of the method's steps.

#### Scenario: Formula evaluated from its tree
- **WHEN** a calculation type evaluates a formula whose tree uses only allowed nodes and
  every symbol of which has a bound value with its unit
- **THEN** the step's `result` is the value of the tree, and the step's `expression` is the
  formula's LaTeX from the resolved parameters

#### Scenario: Node outside the allowed set
- **WHEN** a formula's tree contains a node kind or a function outside the allowed set
- **THEN** the evaluation fails with a `DECError` before any node of the tree is evaluated

#### Scenario: Tree over the limit
- **WHEN** a formula's tree is deeper or has more nodes than the limit
- **THEN** the evaluation fails with a `DECError` before any node of the tree is evaluated

#### Scenario: Symbol without a value
- **WHEN** a formula's tree contains a symbol that has no bound value
- **THEN** the evaluation fails with a `DECError` that names the symbol

#### Scenario: Value that is not finite
- **WHEN** evaluating a formula gives a value that is not a finite number, such as a
  division by zero
- **THEN** the evaluation fails with a `DECError` that names the step

### Requirement: Calculation accuracy
The system SHALL express the accuracy of a calculation as its deviation from named
reference examples, as defined by the requirement "Reference examples" of
`calculation-verification`. An accuracy claim SHALL name the calculation type, the
quantity, and the reference examples it refers to. An abstract percentage without those
SHALL NOT be used as an accuracy claim.

#### Scenario: Accuracy is stated against references
- **WHEN** accuracy is claimed for a calculation type
- **THEN** the claim is stated as the deviation of named quantities from named reference
  examples, within the `tolerance` each example records

### Requirement: Calculation latency
The system SHALL complete a typical calculation in under 30 seconds. This target is
independent of accuracy. What counts as a typical calculation and where the time is
measured are not yet defined.

#### Scenario: Calculation completes in time
- **WHEN** a typical calculation runs
- **THEN** it completes in under 30 seconds
