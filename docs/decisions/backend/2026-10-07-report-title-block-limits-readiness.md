# `report-title-block-limits`: readiness record, 2026-10-07

- Owner: Akim (backend zone, report generator). No part of the change is in Egor's zones.
- Russian version: `2026-10-07-report-title-block-limits-readiness-rus.md`.
- The change settles the follow-up "length limits per title-block column" of
  `calculation-core-contract` (`design.md` decision 18, "Risk"; review item 9 in
  `calculation-core-contract-readiness.md`).

## Verdict

**DOR met for the spec phase (2026-10-07).** `openspec validate --all --strict` passes
(21/21); the second `spec-reviewer` pass lists no blocker and no major finding;
`norm-traceability-checker` finds no norm value in the change. Code starts on
`feature/report-title-limits/backend` (`tasks.md`, section 2).

## Akim's decisions (2026-10-07)

- A fixed maximum length per field of the report request, computed once from the cell and
  its font size, published as `maxLength`; no fit check of each request.
- The surname in column 11 prints at 6 pt, as the date in column 13.
- The limits guarantee ordinary text (the reference text of `design.md` decision 3: words of
  5 to 14 letters with a capital first letter), not text entirely in capitals. Guaranteeing
  capitals would cut the limits to 78/96/4/85/7. Resulting limits: designation 123, document
  name 150, documentation kind 7, organization 130, surname 11.

## `spec-reviewer`

| Pass | Blocker | Major | Minor | Result |
|---|---|---|---|---|
| 1 | 0 | 2 | 11 | NOT READY |
| 2 | 0 | 0 | 5 | READY (spec-reviewer criterion) |

- Pass 1, major 1: "printed whole in its cell" was not testable and contradicted the stated
  risk of wide letters. Fixed: the requirement says a text within its limit is written to
  its cell in full and not shortened; the fit is defined for a reference text and checked by
  an automated layout test with the font's advance widths (scenario "Reference text fits",
  task 2.2a).
- Pass 1, major 2: the check by eye had no strings and no pass criterion, and its NO-GO clause
  would be hit by the worst case it described. Fixed: task 2.6 uses the reference text with
  9- and 14-letter words and a stated criterion; it only confirms that the simulation agrees
  with LibreOffice; overflow of text in capitals is a stated risk, not a NO-GO.
- While fixing major 1, a word-wrap simulation showed that the first limits (from the mean
  width of the Cyrillic capitals, 0.726 em: 126/156/7/135/12) let ordinary text overflow
  columns 5 and 9. `REFERENCE_WIDTH_EM` was calibrated to 0.753 em, the smallest width in
  0.001 em steps for which the reference text fits every cell.
- Pass 1, minors 3-13: all closed (scenarios for all five fields and the log line, cell sizes
  within 0.01 mm, the font's version and SHA-256, a test of the minimal width, the known long
  test text `"<NORM-CONTROL>"`, task 1.4 ticked, the folder rule of AGENTS.md section 7, the
  C/C++ boundary not touched, the performance requirement, no test of the surname size).
- Pass 2, minors 1-4 fixed: stale decision numbers in tasks 2.3 and 2.4; the exact rule and
  examples of the reference text in `design.md` decision 3; "Arial-compatible advance widths
  (Liberation Sans 2.1.5)" in the requirement and the scenario; the `fontTools` snippet goes
  into the code journal (task 2.2a). Minor 5 (performance target) needs no action.

## `norm-traceability-checker`

No requirement fixes a norm value: the five limits, the two font constants and the 6 pt
surname are layout choices; the only norm-derived inputs are the cell sizes, cited as
GOST R 21.101-2026 (edition unverified), Annex E. Its recommendations 1 and 2 are applied in
`design.md` decision 4: the cell sizes cite the figures of forms 5 and 6, and the font sizes
of columns 1, 5, 6 and 9 are stated as layout choices. Recommendation 3, the edition conflict
(GOST R 21.101-2020 in the base spec `report-generator`, 2026 in the changes and the code), is
not caused here; it stays with WP3 as `calculation-core-contract` records.
