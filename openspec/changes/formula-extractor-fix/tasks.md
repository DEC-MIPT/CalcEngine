# Tasks

Branch: `fix/formula-extractor/data` (Egor, data zone). Code cherry-picked into
`fix/normative-catalog/data` (commit `5b06d9b`, 2026-10-13).

No separate branch merge required: the fix reaches `develop` with `fix/normative-catalog/data`.

## 1. Fix and test

- [x] 1.1 [Egor] Change the bare-integer pattern in `ml/configs/parser.toml` from
  `\((\d+)\)\s*$` to `(?<!\S)\((\d+)\)\s*$`; verify: `extract_formulas` no longer returns
  `d0(1)` as a formula number; on СП 22.13330.2016 the count drops from 130 to 127
  (confirmed: 120 stored after deduplication)
- [x] 1.2 [Egor] Add `test_extract_formulas_rejects_figure_label` and
  `test_extract_formulas_accepts_standalone_integer_number` in
  `ml/tests/test_extractors_unit.py`; verify: both tests pass
- [x] 1.3 [Egor] Audit results recorded in `ml/research/VERIFY.md` section 9

## 2. Tester and close

- [x] 2.1 [Agent: tester] GO/NO-GO — covered by `normative-catalog-backend` task 2.7
  tester run (the fix is part of that branch's test sweep); GO declared 2026-10-13,
  221 tests passed, `test_extract_formulas_rejects_figure_label` and
  `test_extract_formulas_accepts_standalone_integer_number` passed

## DOD

GO: tasks 1.1-1.3 checked off; `test_extract_formulas_rejects_figure_label` and
`test_extract_formulas_accepts_standalone_integer_number` pass in the full test suite;
`openspec validate formula-extractor-fix --strict` passes.
