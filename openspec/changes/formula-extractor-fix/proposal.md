# Proposal

## Why

The formula number detection regex `\((\d+)\)\s*$` matches any line ending with `(N)`,
including figure labels like `d0(1)` from figure captions. On the pilot document
СП 22.13330.2016 this produced 3 false-positive formula numbers from figure 6.5 (page 86),
inflating the formula count from 127 to 130 and storing noise in the pipeline database.

## What Changes

- `ml/configs/parser.toml`: tighten the bare-integer formula-number pattern from
  `\((\d+)\)\s*$` to `(?<!\S)\((\d+)\)\s*$`. The negative lookbehind requires the `(`
  to be preceded by whitespace or the start of the line, rejecting `d0(1)` while keeping
  standalone `(1)`.
- Two new unit tests in `ml/tests/test_extractors_unit.py` covering the fix.

## Non-goals

- No change to LaTeX reconstruction, notation extraction, or any other parser component.
- No model changes or ML work.
- Does not affect the backend zone.

## Capabilities

No new capabilities. Improves precision of existing capability `normatives-parser`
(formula extraction, requirement FR-PARSE-002).

## Impact

- `ml/configs/parser.toml` (one line changed).
- `ml/tests/test_extractors_unit.py` (two tests added).
- No schema, API, or contract changes.
