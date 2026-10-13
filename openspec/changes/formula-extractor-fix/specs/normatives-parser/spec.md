# Spec Delta

## Purpose

Tightens the formula number detection in the normative parser to reject figure labels
that match the bare-integer pattern `\((\d+)\)`.

## MODIFIED Requirements

### Requirement: Formula extraction (updated precision)

The system SHALL NOT extract a formula number from a figure label. A token of the form
`(N)` is a formula number only when preceded by whitespace or the start of the line; a
token immediately preceded by a non-whitespace character (e.g. `d0(1)`) is a figure label
and MUST be rejected.

#### Scenario: Figure label not matched as formula number

- **GIVEN** a PDF page containing a figure caption line such as `d0(1)` at end of line
- **WHEN** formulas are extracted from the page
- **THEN** `d0(1)` is NOT returned as a formula number

#### Scenario: Standalone formula number matched

- **GIVEN** a PDF page containing a line ending with `(1)` preceded by a space (whitespace before the paren)
- **WHEN** formulas are extracted from the page
- **THEN** `1` IS returned as a formula number
