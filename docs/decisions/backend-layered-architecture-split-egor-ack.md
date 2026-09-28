# `backend-layered-architecture` (WP5): Egor confirms the split

- Date: 2026-09-28
- From: Egor. To: Akim.
- Answers: `docs/decisions/backend-layered-architecture-split-egor.md`.

Russian version: `backend-layered-architecture-split-egor-ack-rus.md`.

## Confirmation

I confirm the split of WP5 as described:

1. The sections in my zones and the open items it names now live outside WP5: the ML
   section (old tasks 7.1, 7.2, 9.7), the Docker/DevOps section (8.1, 8.2, 9.6), and open
   item 9.3.
2. The planned ML change (`ml-model-storage`) and the infra change (`docker-compose.yml`
   with `dec_app` + `dec_normatives`, a role per zone) are mine.
3. WP5's task 3.x verify clauses run on a `dec_app` database created by hand on the
   existing `dec-postgres` service; `docker-compose.yml` is not touched by WP5.

Nothing I confirmed on 2026-09-27 (WP5 `design.md`, decisions 4-6) is reopened.

## Notes

- **Item 9.3 (where the normative ingestion/catalog code lives).** My position: it stays in
  my existing `normatives_pipeline/` package (now under `src/`), which already ingests into
  `dec_normatives`, owns the formula registry `formulas.toml`, and does search.
  `backend/normatives/` with a second loader would duplicate it. This is the first decision
  of the planned `normative-catalog-backend` and can be settled there.
- **Item 9.7 (`ml/` layout).** There is no `normatives_pipeline/ocr/` package any more. The
  OCR enrichment now lives in `normatives_pipeline/formulas/formula_ocr.py` (CNN detection +
  pix2text recognition), with the models loaded lazily and cached (research journal, entries
  11-12). The planned `ml/` layout should be checked against that, not against an `ocr/`
  directory.
- The ML and infra changes are not created yet; I create them as I take their tasks.
