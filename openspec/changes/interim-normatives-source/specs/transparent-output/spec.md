## ADDED Requirements

### Requirement: Parameter source label on the result screen
The result screen SHALL show, for every result whose envelope carries `parameter_source`,
which source supplied the norm-given parameters: for kind `catalog` the words for the
normative catalog; for kind `interim` the words for the interim normative data, the profile
and the data digest (its first 12 hex characters shown, the full digest available as
screen-reader text). A
`draft` profile SHALL be marked in words, not by colour alone. The label SHALL appear with
the verdict stamp of a checked result and in the refusal view. A result without
`parameter_source` (stored before this field existed) SHALL show no label and no error.

#### Scenario: Interim result labelled
- **WHEN** a result with `parameter_source` of kind `interim`, profile `strict` and a digest
  is opened
- **THEN** the stamp names the interim data, the profile `strict` and the start of the digest,
  and the full digest is readable by a screen reader

#### Scenario: Draft marked in words
- **WHEN** the profile is `draft`
- **THEN** the label says in words that the data are draft data, and the axe check of the
  screen passes

#### Scenario: Refusal labelled
- **WHEN** a refused result carries `parameter_source`
- **THEN** the refusal view shows the same label

#### Scenario: Older result without the field
- **WHEN** a stored result has no `parameter_source`
- **THEN** the screen shows no source label and renders as before
