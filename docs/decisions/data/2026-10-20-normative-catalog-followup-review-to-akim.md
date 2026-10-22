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

## Answers

Akim, 2026-10-20. Reviewed `fddfde3` and `27949c3` against the findings of my third
review (`normative-catalog-backend-readiness.md`, "Section 2: Akim's third review").

Method: a scratch worktree at `27949c3` and a venv with `pip install -e ./ml`,
`latex2sympy2`, `pytest` and `pytest-cov`. `pytest ml/tests` without a database: 242
passed, 23 skipped; package total 73% branch. `ruff check` in `ml/`: clean. The r9 test
was checked by reverting its fix; the other new tests need a database. The search was checked
read only on my local `dec` (ingested 2026-10-13, so it still has the old function), as
`dec_normatives_reader`, with the new `WHERE` condition run over `catalog_read.clauses`.
I did not run the pipeline's database tests: I have no owner URL of a `_test` database
for them.

**Verdict: approved, with one follow-up before the merge (f1).** The code of R5 and of
r6-r9 is right. f1 is a one-test change; when it is on the branch, the merge has my
consent and needs no new review round. f2-f4 are records and notes, for no new branch.

### Closed

- **R5, code.** On my `dec`: `мерзлый` now matches no clause (the old function gives 21,
  all noise: "мероприятий" scores 0.5); `осадка` matches 17; `одного` now finds 6.10.9, the
  known miss of the backend's task 7.1 test. The GIN indexes are on the same expressions
  as the `WHERE` conditions, so they can be used. `rank` stays `real`.
- **r6.** `REVOKE TEMPORARY ... FROM PUBLIC`, and `test_reader_role_refusals` checks the
  `CREATE TEMP TABLE` refusal.
- **r7.** `ensure_catalog_read(..., role_name=...)`; the contract tests use
  `dec_catalog_test_reader` only, so they no longer touch `dec_normatives_reader`.
- **r8.** Both bind tests run under their own names; `ruff check` is clean.
- **r9.** `test_sync_pilot_catalog_rolls_back_on_error` fails when `conn.rollback()` is
  removed, and passes with it.
- **p2, p4, p5.** The `c6c17a5` references and "re-reviewed by Akim" are corrected, the
  Russian "Раздел 4" exists, and `requests==2.34.2` is listed.

### Findings

- **f1 (minor, before the merge). The R5 test still passes with the old SQL.**
  `оснований` against "грунтовое основание" has `word_similarity` about 0.8 (your own
  figure in `27949c3`), so the old condition (`> 0.3`) finds the clause too; and
  `электромагнетизм` shares almost no trigrams with "грунтовый основание", so the old
  condition most likely returns nothing as well (I could not measure it: the reader role
  has no access to `pg_trgm`). Neither assertion fails with the fix reverted,
  which was the point of R5 in my third review. Fix: make the "no match" case a pair that
  the old condition matches and full text search does not, and assert the first half in
  the test. A pair modeled on the ingested catalog, where the old function ranks clause
  5.8.10 ("... без дополнительных защитных мероприятий") at 0.5 for `мерзлый`: a clause
  titled "дополнительные защитные мероприятия" (search text "дополнительный защитный
  мероприятие") and the query `мерзлый`. Assert `word_similarity('мерзлый', <search text>) > 0.3`, then assert that
  `catalog_read.search('мерзлый', 50)` returns no clause. The positive case can stay as it
  is.
- **f2 (record).** The commit message of `27949c3`, the review request and the `tester`
  GO (readiness, Section 8) say the test uses an `AS ws` alias. `27949c3` removes the
  `word_similarity` query entirely, so there is no alias in the code. Please correct the
  GO record.
- **f3 (record, r10).** The request and the GO say the coverage limit is "noted in
  `pyproject.toml`"; `fddfde3` changes only the `requests` line there. My r10 question is
  also still open: when does the package total reach 95% (73% in my run without a
  database)? A date or "not planned" in your answer is enough.
- **f4 (note).** Clause and formula ranks are now `ts_rank` (0.0608 for a one-word hit in a
  short title), while document ranks stay trigram `similarity` (0..1). Sorting one list by
  both scales is allowed by the contract, but a weak document match now outranks every
  clause. No change asked; I will update the ranking row of `normative-catalog-backend`
  `design.md` (it still says "`pg_trgm` `similarity`, 0..1") when that change is synced.

### Process

- p2 and p4 are corrected on the fix branch, not on `develop`, so `develop` shows the old
  records until the merge. Documents go straight to `develop` (AGENTS.md section 2); no
  action now, the merge brings them.
- p3 is not addressed (`2026-10-13-normative-catalog-merge-status-to-akim.md` is still at
  the root, with the `503` statement and the other PDF path). The file stays where it is
  (decision files are never renamed); one dated correction line in it is enough, or leave
  it as a snapshot and say so.

### Backend side (no action for Egor)

- After the merge and a re-ingestion, `KNOWN_MISSES` in the backend's
  `tests/test_catalog_ingested.py` becomes empty (6.10.9 is found), and I update the
  backend's copy of the contract SQL to full text search.

Merge consent: given, once f1 is on the branch. The merge is yours to run.
