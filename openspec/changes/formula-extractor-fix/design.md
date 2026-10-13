# Design

## Context

Formula number detection in `parser/extractors.py` uses patterns from
`ml/configs/parser.toml` (`formula_num_res`). The bare-integer pattern
`\((\d+)\)\s*$` matches any line ending with `(N)`. Figure labels such as
`d0(1)` (subscript markers in figure 6.5 of СП 22.13330.2016) satisfy this
pattern, producing false-positive formula numbers.

## Decision

**Single regex tightening.** Add a negative lookbehind `(?<!\S)` to the
bare-integer pattern:

    Before: \((\d+)\)\s*$
    After:  (?<!\S)\((\d+)\)\s*$

`(?<!\S)` asserts the character immediately before `(` is not a non-whitespace
character, i.e. `(` is either at the start of the line or preceded by a space
or tab. This rejects `d0(1)` (preceded by `0`) while keeping ` (1)` (preceded
by a space).

The fix lives entirely in `ml/configs/parser.toml` — no Python code changes.
The pattern is read at runtime by `extract_formulas` via `parser_config()`.

## No-change zone

`latex_reconstruct`, notation extraction, table extraction, and all other
parser components are untouched.
