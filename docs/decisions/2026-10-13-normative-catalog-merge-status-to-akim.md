# Normative Catalog Data — Merge Status and Next Steps (to Akim)

Date: 2026-10-13
From: Egor
To: Akim

## What was merged today

`fix/normative-catalog/data` is now on `develop`.

Key changes in Egor's zone:
- `formulas.toml` deleted; pilot formulas now come from `pilot.toml` (stored as
  `unverified` / `machine-extracted`, not `verified` / `human-verified` — M1 full fix).
- `document.edition` now stores the full text with change numbers
  (e.g. "2016 с Изм. N 1, 2, 3, 4, 5") — m7 fix.
- Pilot catalog rebuilt in one transaction — M1.
- `word_similarity`, `formula_extractor`, and `catalog_binding` query fixes.
- `_table_caption` guard against negative bbox top.
- New OpenSpec change `formula-extractor-fix` added (task 2.1 tester GO).
- Tester GO for `fix/normative-catalog/data`: 221 passed, 0 failed
  (`normative-catalog-backend-readiness.md`, Section 2 tester verdict).

Also merged today (Egor's other work):
- `normatives-parser` — archived (100% coverage, tester GO).
- `normatives-collector` — archived (100% coverage, tester GO).

## What Akim needs to do next

### Task 2.7 — re-review `fix/normative-catalog/data` (the merge just above)

Akim's second review (`normative-catalog-backend-readiness.md`, Section 2 "Akim's
second review") raised R1–R4, M1, and several minor findings. Egor's fix status
(`normative-catalog-backend-readiness.md`, Section 2 "Egor's fix status") records
R1–R4, m1, m3–m7, and M1 as fixed. Please re-review and record the verdict in
`normative-catalog-backend-readiness.md`.

### Sections 7 (pilot end-to-end) and 7.2–7.3 (performance + tester GO for backend)

These are blocked on task 2.7 passing.

**Important: to populate the database you must run Egor's ingestion pipeline.**
The backend cannot serve normatives from `GET /normatives/search` and
`GET /normatives/documents/{document_id}` until the pilot data is ingested.

To ingest:

```bash
# from the repo root, with DEC_DATABASE_URL pointing at dec-postgres (port 5433)
pip install -e "./ml[ml]"
python -m normatives_pipeline.ingest
```

Detailed usage in `docs/decisions/normatives-pilot-usage-akim.md` and `README.md`.
The pilot document is СП 22.13330.2016 с Изм. N 1, 2, 3, 4, 5
(`docs/normative-base/sp22_2016.pdf`; Akim has a copy under `docs/NTD/`).

After ingestion, `POST /calculations` for `foundations_shallow_r` should return a
real result instead of `503 parameter_source_unavailable`.
