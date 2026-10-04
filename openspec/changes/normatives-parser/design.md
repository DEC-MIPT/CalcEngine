# Design

## Context

The parser turns downloaded СП (text PDF, later scan) into the structured entities the
engine consumes: formulas (executable), coefficient tables, clause refs, notation,
applicability bounds, cross-references. It is domain-agnostic (per-type adapters, H10).

## Goals

- Extract the maximal calculation-bearing surface from the pilot СП.
- Prove extracted formulas are executable on a control example (H6, `exec_rate ≥ 90%`).
- Run on CPU; deterministic baseline first, ML fallback only where baseline fails.

## Non-Goals

See `proposal.md`.

## Decisions

1. **Formula → code is validation, not the production engine (H6).** The parser extracts
   structured entities. A throwaway SymPy executor (`parse_latex` → `lambdify`) runs 1–2
   control examples to prove executability. Production binding/execution is Akim's engine;
   the parser never ships a calculation path. Zone boundary respected.
2. **Output format (reliable).** Each extracted formula is stored as structured JSON:
   (a) raw LaTeX from the model, (b) a parsed SymPy expression (serialized), (c) attached
   notation and units. Alternatives to evaluate in the journal: LaTeX-only; raw model
   string (no normalization); direct-to-Python codegen.
3. **Variable binding (reliable).** For validation, a manual manifest maps each symbol
   (γ_c, R₀, …) to its source (input value | table lookup | derived from another formula).
   Alternatives to evaluate in the journal: auto-bind by notation-name match; auto-bind by
   table-header match.
4. **Per-type adapters (H10).** text-PDF → `pdfplumber`/regex. Formula LaTeX for text-PDF →
   **deterministic reconstruction from the text layer** (`text_layer_latex`: pdfplumber
   geometry + NFKC + Adobe Symbol table; Cyrillic kept as-is, transliterated to Latin for
   SymPy only) — no OCR, no models. Scan → OCR (Surya); for formulas on scans only,
   DocLayout-YOLO (detection) + pix2text (recognition). Table → `pdfplumber` (text) /
   Table Transformer (scan). MinerU 4.0.10 was evaluated (research `nb09`) and **rejected as
   a pipeline**: OCR heads corrupt Cyrillic (`h_зар`→`h_3arrom`) and the CLI reloads models
   per call (≈31 s/formula page); only isolated ideas (formula number as `\tag{}`, unified
   block representation) are taken.
5. **Model strategy.** Deterministic baseline first; ML only where it fails; every ML
   output is `machine-extracted` and gated behind `human-verified`.
6. **Unified parser entry point.** `normatives-pipeline/formulas/source.py` is the single
   formula-LaTeX source: `text_layer.classify` (`text` vs `scan`) picks deterministic
   reconstruction (`parser/latex_reconstruct.py`) for text PDFs or the deferred OCR step
   (DocLayout-YOLO + pix2text) for scans. Both feed the same `Formula.latex`/`expression`
   and the same payload contract. Applicability conditions are extracted deterministically
   (`parser/extractors.extract_conditions`) by config-driven phrase cues and stored in the
   `condition` table.

## Non-functional requirements

- Performance: CPU-only (no GPU); extraction is batch/offline; no real-time constraint.
- Security: no secrets or credentials; no ML in the calculation path; machine-extracted
  values never bypass `human-verified`.
- Coverage: ≥ 95% branch coverage for the changed code (DOD).
- Accessibility: not applicable (batch/CLI, no public UI).

## Boundary

The C/C++ hot-swap boundary of the engine is not touched. The parser has no public API.
