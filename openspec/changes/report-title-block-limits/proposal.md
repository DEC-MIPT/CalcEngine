# Proposal

Owner: Akim (backend zone, report generator). No task of this change is in Egor's zones. A
follow-up of `calculation-core-contract`, not one of WP1-WP8.

## Why

The rows of the form-5 and form-6 title blocks have the fixed heights of the forms
(GOST R 21.101-2026, edition unverified, Annex E), so a text longer than its cell is cut on
the sheet. The report request accepts title-block and signature texts of any length: it
checks only that every character can be written to the document. An engineer who types a
long document name or organization gets a report whose title block silently loses text.

`calculation-core-contract` `design.md` decision 18 records this as a risk, the review of the
report feature lists it as item 9 (`docs/decisions/calculation-core-contract-readiness.md`:
"no length limit on `Text` fields; add per-column `max_length`"), and the change keeps it as a
follow-up in its "Dependencies", because it needs a decision on how many characters each
column holds and adds new request rejections with their own scenario. This change makes that
decision.

## What Changes

- `report-generator`: one added requirement, "Title-block text length": each title-block and
  signatory text of the report request has a maximum length in characters, derived from the
  size of its cell and its font size so that ordinary text (words with a capital first
  letter) at the limit fits; a longer text is rejected before any report is built; the
  limits are published in the request schema.
- The surname in column 11 prints at 6 pt instead of 7 pt, as the date in column 13 already
  does, so the narrow column holds more characters. A layout choice, not a norm value.
- The API passes pydantic's message for a too-long string ("String should have at most N
  characters"), which holds the limit and not the client's text, instead of the fixed
  "Invalid value.".
- Code on one feature branch, `feature/report-title-limits/backend` (`tasks.md`).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `report-generator`: ADDED requirement "Title-block text length". It is ADDED, not a
  modification of "GOST report structure", because that requirement's current text is still
  in the active change `calculation-core-contract`, not in `openspec/specs/`; the new
  requirement adds a rejection next to it and does not contradict it.

## Non-goals

- **A fit check of each request by glyph widths** (a word-wrap simulation of the client's
  text). The limit is a fixed number of characters per field, chosen so that ordinary text
  fits; a text entirely in capitals may not fit at the limit (`design.md`, "Risks"). The
  word-wrap simulation exists only in the tests, to check the limits.
- **Shrinking the font to fit** a long text, or any other change of the forms' geometry,
  captions or the font sizes of columns 1, 5, 6 and 9.
- **The `.pdf` renderer** (`report-generator` "PDF export (future)").
- **A length check in the frontend.** The report request screen of `frontend-app` already
  shows a server `422` next to its field; a client-side limit is a later frontend task.
- Columns 14-19 (empty in the MVP), 7, 8 (Word fields) and 26 (fixed text): no client text.

## Impact

- `backend/app/schemas/report.py` (limits), `backend/app/reporting/title_block.py`
  (surname size, single-spaced title-block style), `backend/app/reporting/capacity.py` (the
  capacity of a cell), `backend/app/api/errors.py` (one error type).
- `backend/tests/` for the above.
- The OpenAPI schema of `POST /calculations/{result_id}/report` gains `maxLength` on five
  fields; `frontend/src/api/schema.d.ts` on `feature/frontend-app/frontend` is regenerated if
  `npm run gen:api` shows a difference after this change is merged.
- No change in `ml/`, `infra/` or `dec_normatives`, no calculation, `NormRef`, parameter or
  result envelope changes; no Egor acknowledgement is needed because no file of his zone or
  his contract is touched.
