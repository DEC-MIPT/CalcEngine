# `normative-catalog-backend`: the order inside `catalog_read.search`, a question for Egor (2026-10-04)

- Date: 2026-10-04
- From: Akim. To: Egor.
- Context: `GET /normatives/search` (WP9 task 6.2) is done on
  `feature/normative-catalog/backend`. The backend calls
  `catalog_read.search(:query, :max_rows)` and orders the rows it gets back by
  `rank DESC, designation COLLATE "C", number COLLATE "C" NULLS FIRST`, as the spec
  "Normative search endpoint" requires ("ordered by rank, highest first, then by
  designation and number"). The read contract you confirmed on 2026-10-04
  (`normative-catalog-backend-contract-akim.md`, "Answers") says only "Egor's ranking
  (`pg_trgm`); at most `max_rows` rows" for the function (`design.md` decision 2). Please
  answer in this file under `## Answers`.

Russian version: `normative-catalog-search-order-questions-akim-rus.md`.

## 1. The problem

The function picks which rows fit into `max_rows`, and the backend only sorts what comes
back. When several hits share the rank at the cut, the hit that the spec puts first may
be dropped while a later one is kept.

My synthetic function in `backend/tests/sql/catalog_contract.sql` shows it: it orders
ties by `document_id`, so `limit=3` keeps the clause of document 1 and drops the clause
of document 2, although document 2's designation comes first. `pg_trgm` ranks often tie
for short queries, so the real function will meet this too.

## 2. Proposal: an addition to `design.md` decision 2 (no column changes)

- `catalog_read.search` orders its rows by `rank DESC`, then `designation`, then
  `number` (`NULLS FIRST`), both compared byte-wise (`COLLATE "C"`), and applies
  `LIMIT max_rows` after that order.
- The backend keeps its own `ORDER BY` as it is, so the result is the same either way.
- After your answer I update decision 2 and my synthetic function, and add a postgres
  test that `limit` keeps the first hits in the spec's order.

- **Your side:** agree, or name another tie order; if you rank with another key that
  never ties, say which one, and I describe it in decision 2 instead.

## Answers
