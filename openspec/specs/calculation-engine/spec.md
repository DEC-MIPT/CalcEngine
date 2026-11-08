# Calculation Engine

## Purpose
Component 2: a verified calculation engine implemented in Python (NumPy/SciPy) that
executes engineering calculations deterministically, logs every step, and validates
each intermediate result. The architecture must allow hot-swapping hot paths to C/C++
later.

## Requirements

### Requirement: Deterministic verified calculation
The system SHALL execute engineering calculations with verified algorithms in Python
(NumPy/SciPy) that strictly follow the bound normative method.

#### Scenario: Run a beam deflection check
- **WHEN** an engineer enters inputs for the beam deflection check per SP 16.13330
- **THEN** the engine computes the result using the verified algorithm with no arithmetic
  drift and no ML influence

### Requirement: Step-by-step logging
The system SHALL log every calculation step, including formulas, value substitution,
and intermediate results, for later transparent display.

#### Scenario: Trace the calculation
- **WHEN** a calculation completes
- **THEN** every step, substitution, and intermediate result is available in the trace

### Requirement: Automatic correctness validation
The system SHALL automatically validate each intermediate result and produce a final
conclusion (for example "strength condition satisfied / not satisfied").

#### Scenario: Conclusion verdict
- **WHEN** a calculation completes
- **THEN** the engine returns a deterministic conclusion with the reason

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

### Requirement: Non-functional — performance and accuracy
The system SHALL complete a typical calculation in under 30 seconds and SHALL achieve
99.9% accuracy for correct inputs.

#### Scenario: Fast and accurate
- **WHEN** a typical calculation runs with correct inputs
- **THEN** it completes in under 30 seconds with 99.9% accuracy

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
