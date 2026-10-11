# `normatives-formula-contract` 1.4–1.7: implementation handoff for Akim (2026-10-04)

- Date: 2026-10-04
- From: Egor. To: Akim (and his agents).
- Branch: `feature/normative-formula-contract/data` (not merged yet).
- Scope: `openspec/changes/normatives-formula-contract/tasks.md`, tasks 1.4–1.7.
- Purpose: tell Akim's agents exactly what is stored, how it is built, and how to check
  it, so the WP9 backend (`normative-catalog-backend`) can consume it without guessing.

Russian version: `normatives-formula-contract-implementation-egor-rus.md` (added by Akim,
2026-10-05).

## 1. What changed (tasks 1.4–1.7)

1.4 `build_formula_payload` builds the five fixed `NormRef` fields (`document`, `edition`,
`clause`, `status`, `provenance`) unconditionally; `norm_ref_keys` in `[output]` now adds
only extra fields beyond those five, never filters them.

1.5 `coefficient` gained `edition`, `clause`, `status`, `provenance` (plus `document`
through the `document_id` join). `build_coefficient_norm_ref` and
`build_coefficient_payload` build a five-field `NormRef` per value.

1.6 `formula` gained `status`, `provenance` columns. `formulas.toml` entries are stored as
`status=verified`, `provenance=human-verified`; OCR output as `status=unverified`,
`provenance=machine-extracted`. The payload reads the stored columns, never constants.

1.7 A formula or coefficient with no `document` raises `RuntimeError` (payload is never
built from an empty string); an empty document designation aborts ingestion.

Additionally (not in 1.4–1.7, but required to satisfy the `NormRef` invariant
`status=verified ⇒ edition and clause concrete`): `designation` and `edition` are now
extracted from the title page text, not from the file name. `parser/text_layer.py`:
`extract_designation()` (regex `СП NN.NNNNN.YYYY` over the first three pages) and
`extract_edition_year()` (the `YYYY` of the designation). A missing designation or year
raises.

## 2. Database state (verified on `dec-postgres`, db `dec`)

`document` (unchanged) plus `edition`/`year` populated from the title page. For the pilot:

- `designation = 'СП 22.13330.2016'`, `edition = '2016'`, `year = 2016`.

`formula` columns now include `status`, `provenance` (defaults `unverified`,
`machine-extracted`). `coefficient` columns now include `edition`, `clause`, `status`,
`provenance` (defaults `unverified`, `''`, `unverified`, `machine-extracted`).

`NormRef` (five fields, no nulls, unknown edition/clause is the literal `unverified`):

```
{document, edition, clause, status, provenance}
```

- `clause` is one locator in the canonical grammar: `форм. (N)`, `п. X`, or `табл. N.N`.
- `status ∈ {verified, unverified}`, `provenance ∈ {human-verified, machine-extracted}`.

## 3. How the payloads are built (for reference, not an API Akim imports)

The backend does NOT import pipeline code (WP9 decision 1). These are the pipeline's own
builders; Akim's backend reads the `catalog_read` views that Egor creates in WP9 task 2.6.

- `db.build_formula_payload(conn, formula) -> dict` — keys from `[output] formula_keys`:
  `norm_ref`, `formula_id`, `latex`, `symbols`, `expression`, `cross_refs`.
- `db.build_coefficient_norm_ref(coefficient) -> dict` — five `NormRef` fields.
- `db.build_coefficient_payload(coefficient) -> dict` — `table_number`, `page`,
  `row_index`, `col_index`, `value`, `norm_ref`.
- `db.fetch_coefficients(conn, doc_id, table_number) -> list[dict]` — raw rows joined with
  `document.designation` (each row already carries every `NormRef` field).
- `db.search_formulas` returns `document_id`, `designation`, `edition`, `status`,
  `provenance`, `latex`, `expression`, etc. (the fields `build_formula_payload` needs).

## 4. How to check it

Tests (need the venv + Postgres on `5433`; `DEC_DATABASE_URL` is the owner's URL of the
database `dec`, kept out of the command; edited by Akim 2026-10-05, WP9 review m6):

```bash
cd ml
DEC_DATABASE_URL="$DEC_DATABASE_URL" ../.venv/bin/python -m pytest tests/ -q
```

Direct SQL (table 5.5 of СП 22.13330.2016):

```bash
PGPASSWORD=dec psql -h localhost -p 5433 -U dec -d dec -c "
SELECT c.table_number, c.row_index, c.col_index, c.value, c.clause, c.status, c.provenance
FROM coefficient c JOIN document d ON d.id=c.document_id
WHERE d.designation='СП 22.13330.2016' AND c.table_number='5.5'
ORDER BY c.row_index, c.col_index;"
```

Human eyeball check (the maintained reviews live under `ml/research/review/`, not part of the
contract; regenerate with `python -m research.make_review_html`, see `ml/research/VERIFY.md`):

- `ml/research/review/sp22_13330_2016.html` — pilot СП 22.13330.2016: formula 5.7 and
  table 5.5, PDF screenshot next to the DB payload and the rendered form.
- `ml/research/review/sp31_13330_2021.html` — СП 31.13330.2021: formula 9 and table 30.

## 5. What is NOT here yet (WP9 section 2, Egor's next branch)

`normatives-formula-contract` 1.4–1.7 only prepares the raw tables. The following are
WP9 tasks (`feature/normative-catalog/data`) and are NOT part of this change:

- 2.1 the `foundations_shallow_r` binding table;
- 2.2 the expression `tree` JSON per bound formula;
- 2.4 the table 5.5 headings (`heading_symbol`/`heading_value`/`heading_unit`) and method
  bounds;
- 2.6 the `catalog_read` schema, views, `search` function and the `dec_normatives_reader`
  role.

Until 2.6 lands, Akim's backend has no `catalog_read` to read and must keep using its
synthetic contract (WP9 decision 9). This change does not alter that.

## 6a. WARNING to Akim: `symbols[].id` for Cyrillic symbols changed (honest heads-up)

`symbols[].id` is the ASCII SymPy name of a quantity — the join key between a formula and its
notation, and the identifier your backend uses inside `expression` and in SymPy. Before the
fix `cyr_map` transliterated Cyrillic homographs to the same Latin letters (`с→s`, `а→a`, `е→e`,
`р→r`, `у→u`, `к→k`), so a Cyrillic symbol and a Latin one produced the **same** `id`:
`notation_entry.symbol` was ambiguous (one `id` → several different `latex`). On the pilot that
was 8 collision groups in extraction (11 counting the manifest), all on indices/letters.

The fix (`5918c30`, `parser/symbols.py`) adds a `_cyr` suffix, case preserved, to any symbol
that contains Cyrillic; Latin is unchanged. `latex` still renders Cyrillic via `\text{…}`:

| symbol | old `id` | new `id` | `latex` |
|---|---|---|---|
| Latin `s` | `s` | `s` | `s` |
| Cyrillic `с` | `s` | `s_cyr` | `\text{с}` |
| Cyrillic `а` | `a` | `a_cyr` | `\text{а}` |
| Cyrillic `К` | `K` | `K_cyr` | `\text{К}` |
| Cyrillic `Н` | `H` (via map) | `N_cyr` | `\text{Н}` |

What this means for you, concretely:

1. **Ids of Cyrillic symbols are different from before.** Any mapping or expression you wrote
   against the old (colliding) ids must be updated to the `_cyr` id.
2. **Auto-extracted Cyrillic ids are a separate namespace** from the plain Latin ids in your
   hand-written `formulas.toml`. `s` (Latin) and `s_cyr` (Cyrillic `с`) are *different*
   quantities; do not merge them unless the norm really uses one symbol.
3. **The migration is manual and has NOT been run on the live `dec` DB.** New ingests get the
   suffix automatically; existing rows keep the old ids until
   `python -m normatives_pipeline.parser.cyrillic --apply` is run (dry-run by default).

## 6. Known baseline limits (not regressions of 1.4–1.7)

- `extract_tables` stores table captions it cannot parse with an empty `table_number`;
  those cells (2077 of 2959 for the pilot) group by page only. Table headings
  (`row_index` 0/1 of table 5.5) are stored as ordinary cells; separating them is WP9 2.4.
- `expression` is still empty for OCR-extracted formulas (design decision 4); only
  `formulas.toml` entries carry an `expression`.

## Answers (Akim, 2026-10-05)

### 6a. Cyrillic symbol ids

Acknowledged. The backend holds no mapping to symbol ids of its own: it reads ids only from
the catalog, and the pilot's ids are all Latin (`formulas.toml`), so nothing changes on my
side now. Until `parser.cyrillic --apply` runs on the live `dec`, old notation rows and new
expressions can disagree on ids; with M2 of the WP9 review fixed
(`normative-catalog-backend-readiness.md`), such a formula is refused instead of getting
unit `1`.
