## ADDED Requirements

### Requirement: Title-block text length
Each text of the report request that is printed in a title-block cell SHALL have a maximum
length in characters, counted as Unicode code points (a Cyrillic letter is one character).
The limits SHALL be: 123 for the designation (column 1, printed in form 5 and form 6), 150
for the document name (column 5), 7 for the documentation kind (column 6), 130 for the
organization (column 9), and 11 for the surname of each signatory (column 11: developer,
checker and normative control). A request with a longer text SHALL be rejected before any
report is built; the rejection SHALL name the field and the limit and SHALL NOT repeat the
client's text. A text within its limit SHALL be written to its cell in full: the generator
SHALL NOT shorten it. The limits SHALL be published in the request schema.

The limits SHALL be chosen so that the reference text at its limit fits its cell when laid
out with Arial-compatible advance widths (Liberation Sans 2.1.5) and word wrap at spaces.
The reference text is words of 5 to 14 letters, each a capital followed by lowercase letters
taken in turn from the Russian alphabet without Ё and continuing from word to word, all
words of one text of the same length, separated by single spaces and cut to the limit, a
trailing space dropped; for the single-line columns 6 and 11 it is one such word of the
limit's length (`design.md`, decision 3, gives the exact rule and examples). A text of wider
letters, such as a text entirely in capitals, is not guaranteed to fit at its limit. The
limits are layout choices derived from the size of each cell and its font size
(`design.md`, decisions 2-5), not norm values; the cell sizes come from GOST R 21.101-2026
(edition unverified), Annex E, the figures of forms 5 and 6. The surname in column 11 SHALL
be printed at 6 pt.

#### Scenario: Text at the limit accepted
- **WHEN** a report is requested with each of the five texts exactly at its limit
- **THEN** the report is built, and the text of each cell equals the text sent

#### Scenario: Text over the limit rejected
- **WHEN** a client sends `POST /calculations/{result_id}/report` with one of the designation,
  the document name, the documentation kind or the organization one character longer than its
  limit
- **THEN** the response is `422` with code `validation_error`, one field entry located at
  `["body", "title", <field>]` whose message names the limit, no part of the sent text in the
  body or in the log line, and no report built

#### Scenario: Surname over the limit rejected
- **WHEN** a report is requested with the developer's, the checker's or the normative
  control's surname one character longer than its limit
- **THEN** the response is `422` with code `validation_error`, one field entry located at
  `["body", <role>, "surname"]` whose message names the limit, no part of the sent text in the
  body or in the log line, and no report built

#### Scenario: Limit counted in characters
- **WHEN** a field holds Cyrillic text of exactly its limit in characters
- **THEN** the request is accepted, although the text is longer than the limit in bytes

#### Scenario: Reference text fits
- **WHEN** the reference text of each field, for every word length from 5 to 14 letters, is
  laid out at its limit with Arial-compatible advance widths (Liberation Sans 2.1.5) and word
  wrap at spaces, in the cell width less the cell margins
- **THEN** it needs no more lines than its cell holds at its font size, in form 5 and, for the
  designation, in form 6

#### Scenario: Limits published
- **WHEN** a client reads the OpenAPI schema of the report request
- **THEN** each of the five fields carries its limit as `maxLength`

#### Scenario: Surname size
- **WHEN** a report is built with the signature block enabled
- **THEN** each surname in column 11 is printed at 6 pt
