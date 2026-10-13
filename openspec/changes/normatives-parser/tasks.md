# Tasks

Branch: `feature/normative-parser/ml` (Egor, ml zone).
Coverage fix: `fix/normative-parser/ml` (latest commit `da3278b`, pending merge into `develop`).

## 1. Baseline extraction (deterministic)

- [x] 1.1 [Egor] Text-layer classifier (text-PDF vs scan) — `parser/text_layer.classify`
- [x] 1.2 [Egor] Clause/numbered-item extraction (regex) → locatable `cl. 6.2`
- [x] 1.3 [Egor] Notation extraction (symbol → meaning + unit) from «Обозначения»
- [x] 1.4 [Egor] Coefficient-table extraction (`pdfplumber`) with units + applicability
- [x] 1.5 [Egor] Applicability-condition extraction (`extract_conditions`, config-driven
  phrase cues, `condition` table) — deterministic, no models

## 2. Formula path (reliable + alternatives)

- [x] 2.1 [Egor] Formula extraction. Text-PDF: regex number detection + deterministic LaTeX
  reconstruction from the text layer (`latex_reconstruct`, A2: pdfplumber geometry + NFKC +
  Adobe Symbol table; Cyrillic kept, transliterated for SymPy only). Scan: DocLayout-YOLO +
  pix2text (deferred). MinerU evaluated and rejected as a pipeline (research `nb09`; see
  design §4). Unified entry point: `formulas/source.py` (PDF-type-based selection).
- [x] 2.2 [Egor] Output format: structured JSON (LaTeX + SymPy + notation) — reliable
- [x] 2.3 [Egor] Alternatives eval: LaTeX-only, raw model string, direct codegen
  (LaTeX-only: naive `parse_latex` fails on domain shift; codegen via `lambdify` chosen;
  Nougat/pix2tex evaluated in journal entries 15-26, research `nb09`; MinerU rejected)
- [x] 2.4 [Egor] SymPy `parse_latex` → `lambdify` executor (validation, H6)
  (`BoundFormula` in `formulas/formula_code.py`; formula 5.7 executes to 143.75 kPa,
  journal entry 13)
- [x] 2.5 [Egor] Manual manifest binding on 1–2 control examples
  (formula 5.7 + k_z_below, k_z_from bound via `pilot.toml`; `_write_synthetic_formulas`
  in `db.py`; confirmed in journal entry 13)
- [x] 2.6 [Egor] Alternatives eval for binding: notation-name match, table-header match
  (notation-name matching in `formulas/notation_restore.py`; manual manifest chosen as
  reliable baseline; alternatives recorded in journal entry 13)

## 3. RAG retrieval (search a normative by formula)

- [x] 3.1 [Egor] `rubert-tiny2` → ONNX embeddings of clauses/formulas
  (evaluated in journal entry 14: 20% recall@1 vs TF-IDF 60%; ONNX not required for
  MVP; `EmbeddingIndex` in `retrieval.py` is a research artifact with optional dep)
- [x] 3.2 [Egor] Vector search vs `pg_trgm` baseline; recall@k
  (journal entry 14: multilingual-e5-small=60%, TF-IDF=60%, rubert-tiny2=20%;
  MVP decision: lexical search via `pg_trgm`; `TfidfIndex` is the production class)

## 4. Tests and quality

- [x] 4.1 [Agent: tester] pytest: clause/table/formula extraction, executor; fixtures =
  pilot СП pages + hand markup; branch coverage ≥ 95%
  (GO 2026-10-13: 200 passed, exit 0; all formulas/ 100%; retrieval.py 100%;
  latex_reconstruct.py ≥98% with corpus; fix branch fix/normative-parser/ml `da3278b`)
- [x] 4.2 [Egor] `ruff` + `mypy` clean

## 5. Validate and close

- [x] 5.1 [Egor] `openspec validate normatives-parser --strict`
  (passes: 2026-10-13)
- [ ] 5.2 [Agent: spec-reviewer] review; resolve blockers
- [x] 5.3 [Agent: tester] GO/NO-GO
  (GO 2026-10-13; see docs/decisions/normative-catalog-backend-readiness.md Section 3)
- [x] 5.4 [Egor] merge to `develop`
  (merged via `feature/normative-pipeline/data` → `develop` in `08dbb85` 2026-10-11)
- [ ] 5.5 [Agent: spec-keeper] sync and archive

## Dependencies

- `normatives-collector` (downloaded pilot СП in `docs/normative-base/`).
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
