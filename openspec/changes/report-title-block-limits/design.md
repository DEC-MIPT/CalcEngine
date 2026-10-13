# Design

## Context

The report renderer (`backend/app/reporting/title_block.py`) draws the form-5 title block in
the first-page footer and form 6 in the footer of the following sheets, as tables whose rows
have the exact heights of the forms (`WD_ROW_HEIGHT_RULE.EXACTLY`) and whose columns have the
forms' widths (GOST R 21.101-2026, edition unverified, Annex E; `calculation-core-contract`
`design.md` decision 18). A text longer than its cell does not grow the row: Word and
LibreOffice cut it. The report request (`backend/app/schemas/report.py`, `ReportRequest`)
carries five client texts that land in such cells: the designation (column 1, both forms),
the document name (column 5), the documentation kind (column 6), the organization (column 9)
and the surname of each signatory (column 11). The schema type `Text` rejects characters
that cannot be written to XML and sets no length.

Akim's decisions (2026-10-07): a fixed maximum length per field, computed once from the cell
and its font size; the surname printed at 6 pt, as the date in column 13 already is; the
limits guarantee ordinary text (words with a capital first letter), not text entirely in
capitals.

## Decisions

1. **A fixed limit per field, in characters, in the request schema.** Each of the five fields
   gets `max_length` in `schemas/report.py`, so pydantic rejects a longer text with the error
   type `string_too_long`, and FastAPI publishes the limit as `maxLength` in the OpenAPI
   schema. Length is counted in Unicode code points, as `str` length in Python. The check of
   characters (`_writable_text`) stays; the alias `Text` goes, and each field is annotated
   `Annotated[str, Field(max_length=...), AfterValidator(_writable_text)]`, the length before
   the characters, since a limit placed after the validator is reported as `too_long`, not
   `string_too_long`. With the length checked first, pydantic itself rejects a lone surrogate
   (`string_unicode`) before `_writable_text` sees it; the request is still rejected with
   `422 validation_error` and the message "Invalid value." (changed 2026-10-07, task 2.3).
   A fit check of each request that simulates word wrap with the font's glyph widths was
   considered and not taken (proposal, "Non-goals"): it gives no number a client can show,
   and it moves validation out of the schema.

2. **The capacity rule.** For a cell of width `W` mm and height `H` mm printed at `S` pt:

   - `lines = floor(H / (S × 25.4 / 72 × LINE_HEIGHT_EM))`, taken as 1 for a single-line
     column (decision 5);
   - `per_line = floor((W − 2 × CELL_MARGIN_MM) / (S × 25.4 / 72 × REFERENCE_WIDTH_EM))`;
   - `limit = lines × per_line`.

   `W` is the sum of the widths of the grid columns the cell spans, and `H` the sum of
   `row_heights_mm(form)` over the rows it spans (the heights already corrected for the line
   thicknesses). `CELL_MARGIN_MM` (0.5 mm left and right) is the table's cell margin; top and
   bottom margins are zero. The C/C++ swap boundary of the engine is not touched: this is
   report layout, outside the calculation path.

3. **The font constants and the reference text.** The constants come from Liberation Sans
   Regular 2.1.5 (`fonts-liberation` 2.1.5,
   `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf`, SHA-256
   `4659bc0c58c5028dd488ec928d41d9265db43d9b669fc14ca8b0832daca7b144`), which is
   metric-compatible with Arial, the font of the title block (`layout.BODY_FONT`) and the font
   LibreOffice substitutes for it; 2048 units per em:

   - `LINE_HEIGHT_EM = 2355 / 2048` (about 1.150): ascender 1854 + descender 434 + line gap 67
     of the `hhea` table, the height of a single-spaced line. The title-block style therefore
     sets single spacing (`line_spacing = 1.0`): the document defaults (`w:docDefaults`,
     `w:line="276"`) give 1.15, a line step of about 1.32 em on the render, which cut the last
     line of column 9 in the first check by eye of task 2.6 (2026-10-07);
   - `REFERENCE_WIDTH_EM = 0.753`: calibrated, not measured. The mean advance of the 32
     Cyrillic capitals А-Я without Ё is 0.726 em (lowercase 0.578 em), but limits from 0.726
     let ordinary text overflow columns 5 and 9, because word wrap leaves the end of a line
     empty. 0.753 is the smallest width, in steps of 0.001 em, for which the reference text
     of every field fits its cell at the limit the rule gives, for every word length from 5
     to 14 letters.

   The reference text (`report-generator` "Title-block text length") for a limit `n` and a
   word length `L` (5 to 14) is built so:

   - the letters run through the 32 lowercase letters `а`-`я` without `ё` in order, continuing
     from word to word and starting again at `а` after `я`;
   - every word of one text has the same length `L`, and its first letter is a capital;
   - the words are joined by single spaces, the text is cut to its first `n` characters, and a
     space left at the end of the cut is dropped (the text is then `n − 1` characters long);
   - for the single-line columns 6 and 11 the text is one word of length `n`.

   Examples: `L = 5` gives `Абвгд Ежзий Клмно Прсту Фхцчш Щъыьэ Юяабв ...`; column 6 (`n = 7`)
   gives `Абвгдеж`, column 11 (`n = 11`) gives `Абвгдежзийк`. The fit is checked by greedy word wrap at spaces, as
   Word and LibreOffice wrap a left- or centre-aligned paragraph without hyphenation: a word
   that does not fit the rest of a line goes to the next line, and a word longer than a line
   is broken inside.

   The advance widths of the space and of the letters а-я and А-Я (without ё, Ё) and the three
   `hhea` values are copied once from the font file with `fontTools` outside the project into
   a test fixture, `backend/tests/fixtures/liberation_sans_metrics.json`, with the font's name
   and version. The SHA-256 above is kept only here: `detect-secrets` reports it in the JSON
   as a high-entropy string, JSON takes no allowlist pragma, and no test could check it,
   since the font file is not in the repository (changed 2026-10-07, task 2.2a). The project
   gets no new dependency; the fixture lets a test lay out the reference text, check
   `LINE_HEIGHT_EM` against the `hhea` values, and check that
   `REFERENCE_WIDTH_EM` is the smallest width that fits (decision 7).

4. **The cells and the limits.** From `FORM5_MERGES`, `FORM5_COLUMNS` and the form-6 grid:

   | Field | Column | Cell `W × H`, mm | Size, pt | Lines × per line | Limit |
   |---|---|---|---|---|---|
   | `title.designation` | 1, form 5 | 120 × 15.18 | 10 | 3 × 44 | 132 |
   | `title.designation` | 1, form 6 | 110 × 15.00 | 10 | 3 × 41 | **123** |
   | `title.document_name` | 5 | 70 × 24.82 | 10 | 6 × 25 | **150** |
   | `title.documentation_kind` | 6 | 15 × 5.00 | 7 | 1 × 7 | **7** |
   | `title.organization` | 9 | 50 × 14.82 | 7 | 5 × 26 | **130** |
   | `*.surname` | 11 | 20 × 5.00 | 6 | 1 × 11 | **11** |

   The grid widths and row heights come from the figures of form 5 and form 6 of
   GOST R 21.101-2026 (edition unverified), Annex E, as `title_block.py` cites them
   (`FORM5_WIDTHS_MM`, `ROW_HEIGHT_MM`, `FORM6_WIDTHS_MM`, `FORM6_ROW_HEIGHTS_MM`); the heights
   in the table are those of `row_heights_mm`, corrected for the line thicknesses. The font
   sizes are layout choices of the report, not values of the standard: 10 pt for columns 1
   and 5 (`LARGE_SIZE_PT`), 7 pt for the other texts (`TITLE_SIZE_PT`, the title-block style),
   6 pt for the surname (decision 6). The designation is printed in both forms, so its limit
   is the smaller of the two.

5. **Columns 6 and 11 are single-line.** A surname is one word, and Word breaks a word that
   does not fit its line inside the word; two lines of 6 pt fit the 5 mm row of column 11,
   but a surname split across them reads as two words. Column 6 holds one line at 7 pt
   anyway. Their limit is one line.

6. **The surname prints at 6 pt.** At 7 pt column 11 holds 10 characters, at 6 pt 11. The
   date in column 13 already prints at 6 pt (`DATE_SIZE_PT`); the surname gets
   `SURNAME_SIZE_PT = 6`, a layout choice like it. The font sizes of all filled columns move
   into one mapping in `title_block.py`, used by the renderer and by the capacity tests.

7. **Limits live in `schemas`, geometry in `reporting`, and tests tie them.** `reporting`
   imports `schemas`, not the other way round (`backend-layered-architecture` decision 2,
   the `lint-imports` contracts), so the five numbers are constants in `schemas/report.py`.
   A module of its own, `reporting/capacity.py`, gets pure functions for the extent of a cell
   and its capacity, and the constants `LINE_HEIGHT_EM` and `REFERENCE_WIDTH_EM`;
   `title_block.py` keeps the grids and the font-size mapping (decision 6) and stays the
   renderer (changed 2026-10-07, task 2.2, so that `title_block.py` does not grow). Three
   tests tie them:
   - the capacity of every column, computed from the forms, equals the schema's constant;
   - the reference text of every field and word length fits its cell at its limit, laid out
     with the fixture's widths;
   - with `REFERENCE_WIDTH_EM − 0.001` some reference text overflows (the width is the
     smallest that fits), and `LINE_HEIGHT_EM` equals the fixture's `hhea` sum.

   A change of the geometry, a font size or a font constant without the matching limit fails
   one of them.

8. **The API passes the limit in its message.** `api/errors.py` replaces the message of every
   pydantic error type outside `STATIC_MESSAGE_TYPES` with "Invalid value.", because such a
   message may hold the client's value. The message of `string_too_long` ("String should have
   at most 123 characters") holds only the limit, so the type joins `STATIC_MESSAGE_TYPES`,
   and the client learns the limit from the response. The status, the code
   `validation_error`, the field location and the log line are unchanged (`calculation-api`
   error format); the log line holds the code and the route, not the text.

## Non-functional requirements

- **Security:** the limits bound the size of the five texts; no message or log line repeats a
  client value (decision 8).
- **Performance:** one length check per field; no new target. The report time stays under
  `report-generator` "Non-functional — generation time", which its existing test measures.
- **Coverage:** branch coverage of `app` stays at 100% (`backend/check.sh`, gate 95%).
- **Accessibility:** no UI in this change.

## Risks

- **Text in capitals can overflow at its limit.** The guarantee covers the reference text of
  decision 3. A text entirely in capitals with words of 7 letters or more needs up to a third
  fewer characters (for example about 87 instead of 130 in column 9). Akim accepted this on
  2026-10-07: guaranteeing capitals would cut the limits to 78/96/4/85/7, too few for a
  documentation kind or a surname.
- **The layout is simulated, not rendered.** The fit test lays out text with the font's
  advance widths and greedy wrap. A check by eye of the reference text at the limits in a
  `.docx` converted to PDF by LibreOffice (`tasks.md`, task 2.6) confirms that the simulation
  agrees with a real renderer; Word is not available on the development machine.
- **The frontend learns the limit only from a `422`** until a frontend task reads `maxLength`
  (proposal, "Non-goals").
