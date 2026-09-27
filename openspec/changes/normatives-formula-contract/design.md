# Design

## Context

The parser stores formulas, notation, and cross-references in Postgres. The backend consumes
them to (1) compute (SymPy), (2) render (MathJax), and (3) trace to the norm. The contract
fixes the handoff so both sides implement the same shape.

## Goals

- A single, config-driven shape for the formula payload.
- Clean LaTeX symbols in the notation block.
- An inspectable return: a function that returns the object, not console text.

## Non-Goals

See `proposal.md`.

## Decisions

1. **LaTeX is the canonical representation; SymPy stays in the backend.** The wire/storage
   carries `latex` (MathJax) and `symbols[].id` (the ASCII SymPy name). The pipeline never
   parses LaTeX to build the expression — `parse_latex` silently corrupts Greek (journal
   Entry 13).
2. **The contract shape is config-driven.** `parser.toml` → `[output]` lists `formula_keys`,
   `norm_ref_keys`, `symbol_keys`, and `default_symbol_kind`; the payload builder iterates
   those keys, so Akim can read the exact shape from config.
3. **Symbol normalization is a config-driven map.** NFKC for Unicode math alphanumerics,
   `greek_map` for Greek, `pua_map` as a font-specific stopgap, `cyr_map` for id
   transliteration. PUA is a known heuristic — the real fix is the text layer (ToUnicode/OCR).
4. **`expression` is a placeholder until structured extraction.** It is carried in the
   contract but empty for now; populated by the parser's formula step (pix2tex + symbol
   correction), never derived from LaTeX.
5. **`kind` defaults to `input`.** Output-variable detection (the left-hand side of `=`) is
   a later step.

## Non-functional requirements

- Performance: query is a normalized-query lookup over a GIN-indexed tsvector; no PDF read.
- Security: no eval of the expression by the pipeline; identifiers sanitized to
  `[A-Za-z_][A-Za-z0-9_]*`.
- Coverage: ≥ 95% branch coverage for the changed code (DOD).
- Accessibility: not applicable (data contract, no public UI).

## Boundary

The C/C++ hot-swap boundary of the engine is untouched; the pipeline computes nothing.
