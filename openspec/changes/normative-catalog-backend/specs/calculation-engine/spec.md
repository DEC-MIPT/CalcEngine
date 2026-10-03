## ADDED Requirements

### Requirement: Table value selectors
The system SHALL give each table value that the engine receives the heading value that
selected it, with the heading's symbol and unit, or no heading value when the table
value depends on no input. Before it uses a table value with a heading value, the engine
SHALL convert the heading value to the base unit of the input named by the heading
symbol, with the same conversion the parameter source uses for the selection, and SHALL
confirm that it equals that input in its base unit. A heading symbol that names no input
of the type SHALL make the engine raise a calculation error. The table value's trace
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
- **WHEN** the engine receives a table value with no heading value
- **THEN** the engine uses the value without a comparison, and its step has no
  substitution
