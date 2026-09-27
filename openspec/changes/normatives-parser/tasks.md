# Tasks

Branch: `feature/normative-parser/ml` (Egor, ml zone).

## 1. Baseline extraction (deterministic)

- [ ] 1.1 [Egor] Text-layer classifier (text-PDF vs scan)
- [ ] 1.2 [Egor] Clause/numbered-item extraction (regex) → locatable `cl. 6.2`
- [ ] 1.3 [Egor] Notation extraction (symbol → meaning + unit) from «Обозначения»
- [ ] 1.4 [Egor] Coefficient-table extraction (`pdfplumber`) with units + applicability

## 2. Formula path (reliable + alternatives)

- [ ] 2.1 [Egor] Formula extraction (regex on text layer; `pix2tex` for images)
- [ ] 2.2 [Egor] Output format: structured JSON (LaTeX + SymPy + notation) — reliable
- [ ] 2.3 [Egor] Alternatives eval: LaTeX-only, raw model string, direct codegen
- [ ] 2.4 [Egor] SymPy `parse_latex` → `lambdify` executor (validation, H6)
- [ ] 2.5 [Egor] Manual manifest binding on 1–2 control examples
- [ ] 2.6 [Egor] Alternatives eval for binding: notation-name match, table-header match

## 3. RAG retrieval (search a normative by formula)

- [ ] 3.1 [Egor] `rubert-tiny2` → ONNX embeddings of clauses/formulas
- [ ] 3.2 [Egor] Vector search vs `pg_trgm` baseline; recall@k

## 4. Tests and quality

- [ ] 4.1 [Agent: tester] pytest: clause/table/formula extraction, executor; fixtures =
  pilot СП pages + hand markup; branch coverage ≥ 95%
- [ ] 4.2 [Egor] `ruff` + `mypy` clean

## 5. Validate and close

- [ ] 5.1 [Egor] `openspec validate normatives-parser --strict`
- [ ] 5.2 [Agent: spec-reviewer] review; resolve blockers
- [ ] 5.3 [Agent: tester] GO/NO-GO
- [ ] 5.4 [Egor] merge to `develop`
- [ ] 5.5 [Agent: spec-keeper] sync and archive

## Dependencies

- `normatives-collector` (downloaded pilot СП in `norm-docs/`).
- `norm-source-traceability` (WP3) finalizes the entity schema; the parser uses a
  provisional schema.

## DOR checklist

- [ ] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [ ] `openspec validate --strict` passes
- [ ] functional + non-functional requirements recorded
- [ ] branch defined (above)
- [ ] acceptance + Go/No-Go criteria written (below)

## DOD and Go / No-Go

- GO: pilot clauses/tables/formulas extracted; extracted formula executes on the control
  example (exec_rate ≥ 90%); alternatives for #2/#3 evaluated and recorded in the journal;
  tests pass with ≥ 95% branch coverage.
- NO-GO: test failure, coverage < 95%, un-evaluated alternatives, or a machine-derived
  value that bypasses `human-verified`.
