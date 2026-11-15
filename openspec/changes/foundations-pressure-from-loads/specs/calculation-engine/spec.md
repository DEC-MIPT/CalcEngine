## MODIFIED Requirements

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
