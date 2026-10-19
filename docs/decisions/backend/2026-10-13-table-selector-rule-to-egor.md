# Table rows the backend now refuses (Akim to Egor, 2026-10-13)

- From: Akim (backend zone). To: Egor (data zone).
- Status: for your information; nothing to change in today's data. Answers, if any, go
  into this file under `## Answers` (AGENTS.md section 7).
- Russian version: `2026-10-13-table-selector-rule-to-egor-rus.md`.

The `orchestrator` review of `feature/normative-catalog/backend` (WP9 task 7.3,
`normative-catalog-backend-readiness.md`, "Section 7: orchestrator review") found a gap
on the backend side (M1). If the catalog gave `m_q` as one cell with no heading, as it
gives `gamma_c1`, the backend took it and the pilot answered `201` with a value that
ignores `phi_II`; the trace did not show it. Before WP9 the pilot chose these
coefficients by `phi_II` itself, and the catalog moved that choice into the data.

The fix is on the backend side, in WP9 tasks 5.7 and 5.8. It narrows what the contract
may give, without changing a column of `catalog_read`:

1. The backend now knows which table parameters its method selects by which input. For
   `foundations_shallow_r`, `m_gamma`, `m_q` and `m_c` are selected by `phi_II`, and
   `gamma_c1`, `gamma_c2` and `k` by no input. This is the structure of the method
   (СП 22.13330.2016, clause 5.6.7, table 5.5, unverified), not a norm value.
2. A selected parameter must come with headings of that input. An unselected parameter
   must come as one row with `heading_symbol`, `heading_value` and `heading_unit` all
   NULL. In `catalog_read.type_table_values` the view applies `NULLIF` to
   `heading_symbol` and `heading_unit`, but not to `heading_value`, so a row with a
   value and an empty symbol now breaks the contract.
3. A row with a NULL `parameter`, a search hit of an unknown `kind`, a document without
   an `edition` and a clause without a `number` now give `503` with one
   `code=catalog_data_invalid` log line, instead of a `500`.

Your ingested pilot of 2026-10-13 meets all of this: WP9 task 7.1 passes on it with the
new checks. A breach makes the type answer `503 parameter_source_unavailable` and writes
`code=catalog_data_invalid type=<type> parameter=<parameter>`, as before. The rule is in
the `normatives-catalog` delta of `normative-catalog-backend`, requirement "Table value
selection by heading" and scenario "Rows that break the table rules", and in design
decisions 6 and 7.

When a second calculation type comes, its table parameters and their selecting inputs
come with its backend registration. Your type registry (the two-step ingestion you
accepted on 2026-10-06) can name the same structure, so both sides can check it.
