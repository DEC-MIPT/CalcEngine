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
   contract but empty for now; populated by the parser's formula step (DocLayout-YOLO +
   pix2text + symbol correction), never derived from LaTeX.
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

## Deterministic extraction stack (rationale)

The pipeline is a deterministic, library-only path: `pdftotext` (text layer), `pdfplumber`
(tables), regex from `parser.toml` (clauses/formulas), `pymorphy3` + Postgres `pg_trgm`
(search), PostgreSQL (storage). No LLM or neural model runs in extraction, search, or the
handoff, so the contract is reproducible and inspectable. Layout/OCR models (DocLayout-YOLO +
pix2text) are a separate, deferred step that may only fill `latex` for machine-extracted
formulas; they never raise `status`. Rationale and rejected alternatives:
`ml/research/RECOMMENDATION.md`, `ml/research/PIPELINE.md`.

## Verified end-to-end (2026-10-04)

The full cycle PDF -> parse -> DB -> read was verified on all five text SPs in
`docs/normative-base/` with `ml/research/verify_end_to_end.py`: the extraction-to-DB roundtrip
is exact (2959 / 1869 / 2909 / 2176 / 945 cells), one numbered table per document was
re-extracted independently via `pdfplumber` and matched, and every formula/coefficient
`NormRef` held its invariants. The terminal procedure is `ml/research/VERIFY.md`; the record is
`docs/decisions/normatives-pipeline-end-to-end-verification-egor.md`.

## Open work

`ml/research/PIPELINE.md` section 4: `latex` for non-manifest formulas, table headings and row
selection (WP9 2.4), concrete `edition`/`clause` for coefficients (WP9 2.5), a per-table
identifier for pages with several same-numbered tables, and Cyrillic indices in OCR formulas.

Cyrillic identifiers are disambiguated: a symbol containing Cyrillic gets the `_cyr` suffix with
case preserved (`А`→`A_cyr`, `а`→`a_cyr`), so `symbols[].id` no longer collides with Latin
homographs (`s` vs `s_cyr`); `tests/test_symbols.py` and `tests/test_cyrillic.py` guard this, and
`python -m normatives_pipeline.parser.cyrillic [--apply]` audits/migrates existing rows.

For `latex` of non-manifest formulas the deterministic path is the PDF text layer, not OCR:
`research/text_layer_latex.py` reconstructs LaTeX from pdfplumber char geometry (font size and
baseline separate sub/superscripts), NFKC maps math letterforms, and a Symbol-font table maps PUA
operators (`∑`, `≥`, `⋅`); Cyrillic is transliterated only for SymPy. It reaches 9/13 parsed on
SP 31.13330.2021 (pix2text: 48%) and parses every formula with Cyrillic indices. Remaining:
horizontal-bar fractions, radicals in complex layouts, and multi-column formulas.
