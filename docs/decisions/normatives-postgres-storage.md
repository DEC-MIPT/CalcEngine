# Notice for Akim: `dec-postgres` — storage for NLP-processed normatives

- Date: 2026-09-27
- From: Egor (data engineer)
- To: Akim (frontend/backend)

## What

There is now a Docker PostgreSQL container `dec-postgres` that acts as the storage for
NLP-processed normative documents: structured entities plus a lemmatized search index,
built at ingestion time (offline), not at query time.

## Connection (local dev)

| Field | Value |
|---|---|
| host | `localhost` |
| port | `5433` |
| database | `dec` |
| user | `dec` |
| password | `dec` |
| DSN | `postgresql://dec:dec@localhost:5433/dec` |

## Schema

All tables are keyed by `document_id` (FK to `document`):

- `document` — `designation` (UNIQUE), `title`, `edition`, `year`, `source_url`.
- `clause` — `number`, `title`, `page`, `search_text`.
- `formula` — `number`, `clause_number`, `latex`, `raw_text`, `page`, `search_text`.
- `notation_entry` — `formula_number`, `symbol`, `meaning`, `unit`.
- `cross_ref` — `clause_number`, `ref_type` (`gost`), `ref_value`, `url`.

Full-text search uses a GIN index on `to_tsvector('simple', search_text)` over `clause`
and `formula`. `search_text` is pre-lemmatized at ingestion (ё→е, lowercase, pymorphy3),
so the query side only lemmatizes the query string and does a tsvector lookup.

## Current state

`СП 22.13330.2016` is already ingested: 647 clauses, 124 formulas, 141 notation entries,
56 cross-refs (GOST mentions).

## How the backend consumes it

- Search: `WHERE to_tsvector('simple', search_text) @@ to_tsquery('simple', <lemmatized query>)`.
- A formula row + its `notation_entry` rows + `cross_ref` rows are the payload for the
  engine / report generator. A formula carries a `NormRef` (`clause_number` + `designation`).
- This is dev-local; shared/CI credentials later via `DEC_DATABASE_URL` env var.

## Notes

- The container was started manually; it is not yet in a compose file (the repo has none).
