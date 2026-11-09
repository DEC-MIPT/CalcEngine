## ADDED Requirements

### Requirement: Input and output metadata in the types listing
`GET /calculation-types` SHALL give each declared input and each declared output of a type, in
addition to the fields of "Calculation types listing", a `label` (an object with a required `ru`
text and an optional `en` text), a `symbol` (a LaTeX string), and, for an input, an optional
`hint` (the same shape as `label`) and a `whole_values_only` flag (`true` for an input that takes
whole values only, `false` otherwise). Every declared input and output of a registered type SHALL
have a non-empty `label.ru` and a non-empty `symbol`. This metadata describes a quantity to a
person. It SHALL NOT change a calculation's result, its trace, the `NormRef` of any step, a
resolved parameter, the result envelope, or `input_hash`, and it SHALL NOT be read from the
normative catalog.

#### Scenario: Metadata listed
- **WHEN** a client sends `GET /calculation-types`
- **THEN** each input and each output of each type carries `label.ru` and `symbol`, and each input
  carries `whole_values_only`, in the order of "Calculation types listing"

#### Scenario: Whole values marked
- **WHEN** a client reads the input `phi_II` of `foundations_shallow_r`
- **THEN** its `whole_values_only` is `true`, and the same flag is `false` for `b`

#### Scenario: Type without metadata not registered
- **WHEN** a calculation type declares an input or an output with no `label.ru` or no `symbol`
- **THEN** the type is not registered, and the failure names the quantity

#### Scenario: Calculation unchanged
- **WHEN** the metadata is added to a type
- **THEN** a calculation request for it gives the same result envelope, trace, `NormRef` list and
  `input_hash` as before
