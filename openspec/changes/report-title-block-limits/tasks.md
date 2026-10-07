# Tasks

Owner: Akim (backend zone, report generator). No task of this change is in Egor's zones.

Branch: one feature, `feature/report-title-limits/backend` (Akim, from `develop`), sections 2
and 3.1-3.3. It is merged into `develop` only when every task with code is checked off, the
`tester` has declared GO for the feature and the review has passed (`AGENTS.md`, Branching
rules). Spec work (section 1 and tasks 3.4-3.5) is committed directly to `develop`.
Checkboxes are ticked in `develop` as each subtask is done on the feature branch.

Code journal: `docs/akim/reports/report-title-block-limits-code-journal.md` (untracked,
Akim's zone), created before task 2.1.

## 1. Spec readiness

- [x] 1.1 (spec) Run `openspec validate report-title-block-limits --strict` and
  `openspec validate --all --strict`; verify: both pass (2026-10-07, 21/21)
- [x] 1.2 (spec) Run `spec-reviewer` on this change until a report on the current version
  lists no blocker and no major finding; verify: the passes are recorded in
  `docs/decisions/backend/2026-10-07-report-title-block-limits-readiness.md` and its `-rus`
  version (2026-10-07: pass 2, 0 blockers, 0 major)
- [x] 1.3 (spec) Run `norm-traceability-checker`; verify: it confirms that the limits are
  layout choices, not norm values, and that the cell sizes cite GOST R 21.101-2026 with its
  edition marked unverified; recorded in the readiness file (2026-10-07: confirmed)
- [x] 1.4 (spec) Point the follow-up of `calculation-core-contract` (`tasks.md`,
  "Dependencies", the length-limits item, and `design.md` decision 18, "Risk") at this
  change; verify: both places name `report-title-block-limits`, and
  `openspec validate --all --strict` passes (done 2026-10-07)

## 2. Backend (feature `report-title-limits/backend`)

- [ ] 2.1 Print the surname of column 11 at 6 pt (`SURNAME_SIZE_PT`), and keep the font sizes
  of columns 1, 5, 6, 9 and 11 in one mapping of `backend/app/reporting/title_block.py` that
  `add_title_blocks` and `_sign` use (`design.md` decision 6) (backend); verify: a test reads
  every surname run of form 5 at 6 pt, and the existing title-block and signature tests pass
  unchanged (none of them asserts the size of a surname run; the one size assertion,
  `test_reporting_signatures.py`, checks the date run)
- [ ] 2.2 Add pure functions for the extent of a cell (`W`, `H` from the grid widths, the
  merges and `row_heights_mm`) and its capacity, and the constants `LINE_HEIGHT_EM` and
  `REFERENCE_WIDTH_EM` with their source (`design.md` decisions 2-5) (backend); verify: tests
  find the cell sizes of the table in decision 4 within 0.01 mm, the lines and characters
  per line of each column, the smaller of forms 5 and 6 for column 1, and one line for
  columns 6 and 11
- [ ] 2.2a Add the fixture `backend/tests/fixtures/liberation_sans_metrics.json` (font version
  and SHA-256, units per em, the three `hhea` values, the advance widths of the space and of
  а-я and А-Я without ё and Ё), copied once from the font file of `design.md` decision 3, and
  the fit tests of decision 7 with a greedy word wrap written in the test module, and record
  the `fontTools` snippet that produced the fixture in the code journal (backend);
  verify: the reference text of every field, for every word length from 5 to 14, fits its
  cell at its limit (form 5 and form 6 for the designation); with `REFERENCE_WIDTH_EM − 0.001`
  at least one reference text overflows; `LINE_HEIGHT_EM` equals the fixture's `hhea` sum over
  units per em
- [ ] 2.3 Add the five limits to `backend/app/schemas/report.py` as `max_length` of the
  fields, keeping the character check (`design.md` decisions 1, 7) (backend); verify: for
  each field and each signatory role, Cyrillic text at its limit is accepted and one
  character more fails with `string_too_long`; a test in the reporting tests asserts that
  each schema limit equals the capacity of task 2.2 (`design.md` decision 7)
- [ ] 2.4 Add `string_too_long` to `STATIC_MESSAGE_TYPES` in `backend/app/api/errors.py`
  (`design.md` decision 8) (backend); verify: `POST /calculations/{result_id}/report` with a
  designation one character over the limit answers `422 validation_error` with one field at
  `["body", "title", "designation"]`, a message naming the limit and no part of the sent text
  in the body or in the captured log; the same, parametrised, for the document name, the
  documentation kind, the organization and the surname of each of the three roles at
  `["body", <role>, "surname"]`; `/openapi.json` gives `maxLength` for the five fields; a
  report requested with every text at its limit returns `200`, and the text of each cell of
  the returned `.docx` equals the text sent
- [ ] 2.5 Shorten any existing test text or fixture that exceeds a new limit (known:
  `"<NORM-CONTROL>"`, 14 characters, in `backend/tests/test_services_report.py`), and run
  `backend/check.sh`, the `postgres` module and the `pre-commit` hooks (backend); verify:
  `ruff`, `mypy`, `lint-imports` pass, branch coverage of `app` stays 100%, the `postgres`
  module passes against `dec_app_wp8_test`, the hooks pass
- [ ] 2.6 Check by eye that the simulation agrees with a renderer: build two reports with
  every field at its limit, one with the reference text of 9-letter words and one with
  14-letter words (`design.md` decision 3), convert them to PDF with
  `soffice --headless --convert-to pdf`, and look at form 5 of the first sheet and form 6 of
  the second (backend); verify: in each cell every line is visible, no line is cut by the
  cell's lower border and no letter crosses a side border; recorded in the code journal with
  the LibreOffice version and the two PDFs' names. If a text overflows, the simulation does
  not match the renderer: raise `REFERENCE_WIDTH_EM`, recompute the limits and repeat tasks
  2.2-2.6

## 3. Verify and close

- [ ] 3.1 `tester` GO for `feature/report-title-limits/backend`; verify: the verdict with the
  test count and the coverage is recorded in the readiness file
- [ ] 3.2 Review by the orchestrator or Egor; verify: the review is recorded in the readiness
  file, with no open blocker or major finding
- [ ] 3.3 Merge the feature into `develop` (backend, with Akim's word); verify: `develop`
  passes `backend/check.sh`
- [ ] 3.4 (spec) Tell the frontend: if `npm run gen:api` on `feature/frontend-app/frontend`
  shows a difference after the merge, regenerate `frontend/src/api/schema.d.ts` there;
  verify: the note is in `frontend-app` `tasks.md`, "Dependencies"
- [ ] 3.5 (spec) `spec-keeper` syncs the `report-generator` delta into `openspec/specs/` and
  archives this change; verify: `openspec validate --all --strict` passes after the archive

## Requirement coverage

| Requirement | Verified by |
|---|---|
| `report-generator` Title-block text length | tasks 2.1-2.6 (scenario "Reference text fits": task 2.2a) |

## Dependencies

- `calculation-core-contract` (not archived) owns "GOST report structure" and decision 18;
  this change only adds a requirement next to it and does not wait for its archive.
- `frontend-app`: no task waits for this change; task 3.4 tells it about the schema.
- No dependency on Egor's zones or on `normative-catalog-backend`.

## DOR checklist

- [x] `proposal.md` (with "Non-goals"), `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes and a `spec-reviewer` report on the current version
  lists no blocker and no major finding (tasks 1.1, 1.2)
- [x] Functional requirement and scenarios recorded; the requirement is mapped to tasks
- [x] Non-functional requirements recorded (`design.md`: security, performance, coverage;
  accessibility not applicable)
- [x] Each task fits one session and names how it is verified; every task with code is on
  the one feature branch
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branch defined (above)
- [x] Dependencies listed and satisfied

## DOD and Go / No-Go

- **GO for `feature/report-title-limits/backend`:** every task of section 2 is checked off;
  `backend/check.sh` passes with branch coverage of at least 95% (100% today); the `postgres`
  module and the hooks pass; the check by eye of task 2.6 is recorded; `openspec validate
  --all --strict` passes; no UI changes, so `UI/UX: N/A`.
- **NO-GO:** a failing test, coverage under 95%, a schema limit that differs from the
  capacity computed from the forms, a reference text that does not fit its cell in the fit
  test, a response or log line that repeats a client text, a reference text at its limit
  that overflows its cell in the check by eye of task 2.6, or an open blocker or major review
  finding. A text of wider letters (for example entirely in capitals) overflowing at its limit
  is a known risk (`design.md`, "Risks"), not a NO-GO.
