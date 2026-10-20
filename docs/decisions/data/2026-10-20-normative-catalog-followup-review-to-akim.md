# Review request: `fix/normative-catalog-followup/data` (Egor to Akim, 2026-10-20)

- From: Egor (data zone). To: Akim (backend zone).
- Status: `tester` GO recorded (readiness doc, Section 8, 2026-10-20). Awaiting your
  review as the second developer (AGENTS.md section 2, step 7).
- Russian version: `2026-10-20-normative-catalog-followup-review-to-akim-rus.md`.

## Branch

`fix/normative-catalog-followup/data`, HEAD `3f5264d` (merge with develop `7f394e4`).
Fix commits: `fddfde3` and `27949c3`. Review these two commits only.

## What changed

Two commits close the findings of your third review
(`normative-catalog-backend-readiness.md`, Section 6, 2026-10-13):

**`fddfde3` — R5, r6-r10, p2-p5**
- R5: clause and formula search replaced with PostgreSQL FTS (`to_tsvector('russian')`,
  `plainto_tsquery`) and GIN indexes. Document search stays trigram. The `word_similarity`
  threshold that returned noise is gone.
- r6: `REVOKE TEMPORARY ON DATABASE` now targets `PUBLIC`, not the reader role (the
  reader role never had that privilege; revoking from `PUBLIC` is the correct hardening).
- r7: `ensure_catalog_read` accepts an explicit `role_name` parameter; tests pass an
  isolated `dec_catalog_test_reader` role, so they do not touch the production role.
- r8: a duplicate test function was renamed; import order fixed (`ruff I001`).
- r9: rollback test added for the `sync_pilot_catalog` error path.
- r10: postgres-only coverage limitation noted in `pyproject.toml` and the commit
  message; no non-postgres branch is uncovered.
- p2-p5: process-record corrections in the readiness doc.

**`27949c3` — word_similarity alias and assertion**
- `RealDictCursor` does not support numeric indexing; `word_similarity(...)` result is
  now aliased `AS ws`.
- Removed the `ws < 0.5` assertion: Russian inflections share enough trigrams (~0.8)
  regardless of morphological distance, so the claim was always wrong. The test still
  proves FTS works via the clause-title hit, which is what the fix is about.

## Files changed

- `ml/src/normatives_pipeline/catalog_contract.py` (R5, r6, r7 SQL)
- `ml/tests/test_catalog_contract.py` (r7 role isolation, r8 rename, r9 rollback)
- `ml/tests/test_pilot_catalog.py` (r8 import order)
- `ml/tests/test_retrieval.py` (AS ws alias, drop ws assertion)
- `ml/pyproject.toml` (r10 coverage note)
- `docs/decisions/normative-catalog-backend-readiness*.md` (p2-p5 corrections)

## How to answer

Add `## Answers` below. A single "reviewed, approved" or your findings, with a
merge-consent line if you approve. The merge is Egor's to execute after your approval.
