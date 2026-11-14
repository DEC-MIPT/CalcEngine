## MODIFIED Requirements

### Requirement: Typed trace step
The system SHALL record every calculation step as a typed trace step with these fields:
`step_id`; `expression`, in a form the transparent output can render; `substitutions`,
each a symbol with its value and unit; `result`, a value with its unit; and `norm_refs`, a
list of at least one `NormRef` for normative steps. A step that rests on several clauses, tables, or documents
carries one `NormRef` per locator. No required field may be null. A normative step is a formula step, a table
step, or a check step:

- a formula step evaluates a formula; its `expression` is the formula's LaTeX, and the unit
  of its `result` is the unit bound to the formula's result symbol;
- a table step takes a value from a table of a norm; its `expression` is LaTeX that names
  the table value by its symbol, its `substitutions` are the values that select the entry,
  and its `result` is the entry with its unit;
- a check step compares two quantities; it also records the comparison operator (one of
  `le`, `lt`, `ge`, `gt`), the right-hand value with its unit, and `passed`; its `result`
  is the left-hand value.

Whether a `NormRef` counts as verified is defined by the `normatives-catalog` requirement
"Norm reference status". A normative step counts as verified only when every `NormRef` in its
`norm_refs` is verified. Engineer-sourced steps are counted separately, not as
verified or unverified normative steps.

A disjoint engineer_formula variant SHALL contain step_id, expression, substitutions
and result with the same units contract, plus source: EngineerRule naming engineer
and rationale. It SHALL NOT contain norm_refs or impersonate a normative formula.
It is restricted to reviewed geometry, signed transfer and signed pressure-combination
rules in foundations-pressure-from-loads, not normative coefficients or limits.

#### Scenario: Every step is complete
- **WHEN** a calculation completes
- **THEN** every step in the trace has `step_id`, `expression`, `substitutions` with
  symbols and units, `result` with a unit, and its normative norm_refs or engineer
  source; every check step also has
  its operator, its right-hand value with its unit, and `passed`

#### Scenario: Step without a verified reference
- **WHEN** any `NormRef` in a step's `norm_refs` is not verified
- **THEN** the step stays in the trace, is marked as unverified, and is counted in the
  envelope's `unverified_step_count`; it is never dropped silently

#### Scenario: Engineer formula has its own source
- **WHEN** an engineer_formula geometry step is emitted
- **THEN** its source EngineerRule is required, norm_refs is forbidden, and no normative verification status is inferred

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
EngineerRule is allowed for rounding, validated ranges, reviewed engineer_formula
steps and reviewed derived applicability guards. It SHALL NOT source a normative
method bound. At run time each output
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

#### Scenario: Moment input conversion
- **WHEN** a loads request supplies a supported moment unit other than its kN*m base unit
- **THEN** the API validates the moment dimension and the boundary converts once to kN*m

#### Scenario: Internal volume quantities
- **WHEN** the geometry computes Wx or Wy
- **THEN** its declared dimension is volume, its base unit is m3, and the unit vocabulary validates it without adding a volume input to the loads request

### Requirement: Applicability check with three outcomes
The system SHALL check the inputs of each calculation against the method's range and
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

After input checks, a calculation MAY enforce a reviewed derived applicability
guard. On violation it SHALL stop immediately and return a kind=derived reason
with check_id, step_id, quantity, value: QuantityValue, operator, limit: QuantityValue,
source: Source, related_inputs: a nonempty ordered list of registered input names,
and limiting_corner: one of pp, pm, mp, mm for the loads contact guard. step_id
SHALL identify the retained diagnostic trace step. The source MAY be an EngineerRule
for an explicitly engineer-adopted applicability guard, never a replacement for a
normative method bound. The diagnostic prefix contains no bearing check or final
outputs. Existing input-bound reason shapes and their refusal ordering are unchanged.

#### Scenario: Computed contact refusal
- **WHEN** a derived guard observes negative minimum corner pressure
- **THEN** the type returns refused with its diagnostic prefix and typed limiting_corner, and runs no bearing check

### Requirement: Result envelope
The system SHALL return every calculation, including a refused one, as a result envelope
with these fields: `result_id`, `engine_version`, `input_hash`, `outputs` (each output
quantity with value, unit, `rounding_rule`, and `rounding_source`), `norm_refs` (every `NormRef`
the calculation used: those of the trace steps, of a bound that refused the calculation,
of rounding sources, of a derived guard source that is a NormRef list, and of
warnings whose source is a `NormRef`), `engineer_rules`
(every EngineerRule used as rounding, engineer_formula or derived-guard source,
or as the source of a warning; a possibly
empty list), `verdict` (one of `pass`, `fail`, `refused`), `verdict_reason`,
`warnings` (each recording the input, the violated bound of the validated range, and that bound's `Source`), `trace`, and `unverified_step_count` (the number of normative steps that do not
count as verified; engineer_formula steps are excluded). `input_hash` SHALL be computed from the calculation type
identifier, the inputs after conversion to base units, and the identity of the resolved
parameter set, so identical inputs and parameters give identical hashes and a change in
either gives a different hash.

The lists of the envelope SHALL have a fixed order: `trace` in the order the steps ran;
`outputs` in the order the calculation type declares its output quantities; `warnings`
in the order the calculation type declares the bounds of its validated range; `norm_refs`
and `engineer_rules` each hold every item once, in the order of its first use (trace steps
in order, then the input bound or derived guard that refused the calculation, then rounding sources in the order
of `outputs`, then warnings). Two `NormRef` are the same item when all their fields are
equal; two `EngineerRule` are the same item when both their fields are equal.

#### Scenario: Envelope fields present
- **WHEN** a calculation completes or is refused
- **THEN** the envelope contains every field listed above, and no field is null

#### Scenario: Refused calculation envelope
- **WHEN** a calculation is refused by the input-bound applicability check
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

#### Scenario: Derived refusal envelope
- **WHEN** a reviewed derived guard refuses a calculation
- **THEN** outputs is empty, trace contains exactly the completed diagnostic prefix, its step_id and limiting_corner are stored, no bearing checks run, and source summaries include the prefix and guard in first-use order

#### Scenario: Historical payloads remain valid
- **WHEN** a stored result uses only the old trace and input-bound refusal variants
- **THEN** it validates without new mandatory fields, rewriting, recomputation or changes to its historical payload

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

For foundations_shallow_loads only, the reviewed source assembler MAY instantiate
limit expressions with symbol/multiply nodes binding R to the loaded edge or
corner multiplier. Their numeric values and unchanged NormRefs come from prepared
SP 22.13330.2016, edition 2016 with amendments 1-5, clause 5.6.26, as specified
by foundations-pressure-from-loads "Ordered resistance checks and outputs". The
composite is an assembled binding, not a separately human-verified record. It SHALL
use the existing closed interpreter, with no hardcoded coefficient and no new
NormRef provenance enum or rewriting of signed record digests. Reviewed geometry,
transfer and corner combinations use engineer_formula with their EngineerRule.

#### Scenario: Assembled limit provenance
- **WHEN** the source assembler binds R and a prepared pressure multiplier
- **THEN** the expression inherits that record source unchanged, uses the validated interpreter and introduces no verified-record claim
