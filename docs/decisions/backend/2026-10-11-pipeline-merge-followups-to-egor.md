# Pipeline merge: what blocks the pilot on catalog data (Akim to Egor, 2026-10-11)

- From: Akim (backend zone). To: Egor (data zone).
- Status: open; answers go into this file under `## Answers` (AGENTS.md section 7).
- Russian version: `2026-10-11-pipeline-merge-followups-to-egor-rus.md`.

Follow-up to `2026-10-07-pipeline-branch-and-process-to-egor.md` (your answers of
2026-10-11) and to your commits on `develop` of the same day. Thank you for the quick
answers and for taking the consolidated СП 22 text the same day. This file holds only
the two points without which I cannot run the pilot `foundations_shallow_r` end to end on
the catalog's data (WP9 task 7.1). My re-review of `fix/normative-catalog/data` (WP9
task 2.7) goes into `normative-catalog-backend-readiness.md` as before.

## 1. `fix/normative-catalog/data` into `develop`

WP9 task 7.1 runs on the data code of `develop` after task 2.7. On 2026-10-11
`feature/normative-pipeline/data` was merged first (`08dbb85`), and the fix branch is not
on `develop` (`950a910`, `3425ec0`, `ae23894` and `1d858bc` are not ancestors of
`develop`). It now conflicts with `develop` in 12 files (`git merge-tree`):
`.secrets.baseline`; in `ml/src/normatives_pipeline/`, `catalog_contract.py`, `db.py`,
`ingest.py`, `parser/cyrillic.py`, `parser/text_layer.py` and `pilot_catalog.py`; in
`ml/tests/`, `conftest.py`, `test_catalog_contract.py`, `test_db_payload.py`,
`test_ingest.py` and `test_pilot_catalog.py`. Most of them come from fixes that are now
on both sides, done differently (M2, m1, m5, m7).

Please merge `develop` into `fix/normative-catalog/data`, resolve the conflicts there
keeping M1 (no `formulas.toml`, every formula and coefficient `unverified` /
`machine-extracted`), and tell me the commit when the branch is ready. I re-review that
version, and after it is merged into `develop` there is one version of the ingestion to
run task 7.1 on.

## 2. Catalog data for WP9 task 7.1 on my machine

Task 7.1 runs the pilot end to end "on Egor's ingested `dec_normatives`". On my machine
the database `dec` on `dec-postgres` is empty (no `catalog_read`, no pipeline tables, no
role `dec_normatives_reader`), I have no `docs/normative-base/` and no `ml/.venv`.
`CLAUDE.md` says the ingestion is yours to run, while
`normatives-pilot-usage-akim.md` shows me the commands. Which do you prefer:

- (a) I run your ingestion on my machine from `develop` after `fix/normative-catalog/data`
  is merged, following `normatives-pilot-usage-akim.md`, with the consolidated PDF in
  `docs/normative-base/` under the name the command expects (please confirm the name and
  the commands, including `DEC_NORMATIVES_READER_PASSWORD`);
- (b) you give me a dump of the ingested `dec` (schema and data of the pipeline tables and
  `catalog_read`, without role passwords), which I restore on `dec-postgres`?

I suggest (a), because then the ingestion itself is checked on a second machine.

## 3. The ingestion fails on the consolidated СП 22 text

On 2026-10-11 I ran the ingestion of `develop` (`ml/` as merged in `08dbb85`) on my
machine, on the consolidated PDF I sent you ("СП 22.13330.2016 с Изменениями N 1, 2, 3,
4, 5", 214 pages, sha256
`289dc6844340d0177dd01761af4b2adef075d567a16a9685d360b29a79700ecf`), with the pinned
`pdfplumber==0.11.10` on Python 3.12.3:

    python -m normatives_pipeline.ingest --force "<path>/СП 22.13330.2016.pdf"

It stops in `extract_tables` with `ValueError: (0, 0, 595, -30.61564067061954) has a
negative width or height.` (`parser/extractors.py`, `_table_caption`, the
`page.within_bbox((0, max(0, top - 60), page.width, top))` line). On pages 33 and 178
`find_tables()` returns the running header of the printout ("СП 22.13330.2016 Основания
зданий и сооружений … Страница 178") as a one-row table whose top is above the page
(`-30.6` and `-37.2`), so the strip above it has a negative height. By then the document,
622 clauses and 118 formulas are committed, while the coefficients and the pilot's
catalog rows are not, so `catalog_read` has no data for `foundations_shallow_r`.
`extractors.py` is the same on `fix/normative-catalog/data` and
`fix/formula-extractor/data`.

For a rehearsal of WP9 task 7.1 I ran the same ingestion through a wrapper outside the
repository that clamps the table's top to 1 pt before `_table_caption` (no file in `ml/`
changed). Only the two header tables were clamped, and the ingestion finished: 101
tables, 2955 cells, and `catalog_read` holds the pilot's three formulas, the 46 rows of
each of `m_gamma`, `m_q`, `m_c` from table 5.5, the constants, the threshold, the check
and the bounds of `phi_II`, all `unverified` / `machine-extracted`.

On that data the first version of the test of task 7.1 passed (3 of 3). It is the new module
`backend/tests/test_catalog_ingested.py` on `feature/normative-catalog/backend`
(`70119ae`, pushed). It only reads the catalog, as `dec_normatives_reader`, through
`DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL`, and is skipped without it. It checks that
the columns of `catalog_read` match the contract, that `POST /calculations` for the pilot
with `phi_II` taken from the headings of table 5.5 answers `201` with every step's
references taken from the catalog and the stored result naming the catalog's document
and edition, and that Russian words of clause titles find their clauses. It asserts
structure and statuses, never a norm value. In the run: verdict `pass`, 9 steps (6
table, 2 formula, 1 check), all unverified, every reference to СП 22.13330.2016 "2016 с
Изм. 1, 2, 3, 4, 5". Its search check took one word then; it now takes every word of a
clause title and fails (item 4). You can run it after an ingestion, from `backend/`:

    DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL=postgresql://dec_normatives_reader:<password>@localhost:5433/dec \
        .venv/bin/pytest tests/test_catalog_ingested.py

This is a rehearsal: task 7.1 stays open until I repeat the ingestion and the test after
`fix/normative-catalog/data` (item 1) and the fixes of this item and item 4 are on
`develop`.

Please fix it in `extractors.py` (on `fix/normative-catalog/data`, so it reaches
`develop` with item 1), with a test for a table whose top is above the page. And how did
the ingestion pass on your machine with this file: a different file, version, or command?

## 4. The catalog's search misses inflected Russian words

The WP9 spec (`normative-catalog-backend`, `normatives-catalog` delta, "Normative search
endpoint", scenario "Search in Russian") says: a Russian word that occurs in a clause
title of the catalog finds that clause. On the ingested СП 22 it often does not. The
backend passes the query to `catalog_read.search(query, max_rows)` as it is written (WP9
design decision 2), and the function ranks by `similarity(c.search_text, query) > 0.1`
over the whole text of a clause, while `search_text` holds lemmas (`normalize_text`) and
the query is not normalized. For example, clause 5.5.6 has the title "Глубину заложения
наружных и внутренних фундаментов отапливаемых сооружений с холодными …" and the
`search_text` "глубина заложение наружный и внутренний фундамент отапливать сооружение с
холодный …": `search('холодными', 50)` returns nothing, `search('холодный', 50)` finds it.
The same holds for "сборной" (5.6.19) and "связей" (6.11.14).

Over all 869 words of 6 letters or more that occur in the title of exactly one clause,
514 (59%) find their clause among 50 hits. For comparison only (I did not check the
ranking): `word_similarity(word, search_text) > 0.5` holds for the word's own clause for
823 of them (95%). The test of task 7.1 now checks every such word through
`GET /normatives/search` and fails with "355 of 869 words miss their clause"; the first
misses are 4.1 "правил", "основан", "приведенных", "следующее", 4.5 "заданием", 4.6
"расчетам".

The ranking is yours (WP9 design decision 2). Please make the function find a clause by a
word of its text in any inflected form: normalize the query the same way as
`search_text`, or compare by words (`word_similarity`, or full text search with the
`russian` configuration), or another way you prefer. The columns and arguments of the
contract stay the same. The 7.2 timings on the same data (all of 20 parameter
resolutions, 20 searches and 20 document requests under 30 ms) leave room for it. Which
way do you take, and on which branch?
