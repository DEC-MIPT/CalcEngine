# Acknowledgement of `interim-normatives-source` (Akim to Egor, 2026-10-20)

- From: Akim (backend zone). To: Egor (data zone).
- Status: a request for your acknowledgement. It is the last open DOR item of the change
  (`tasks.md`, task 1.5). Answers go into this file under `## Answers` (AGENTS.md section 7).
- Russian version: `2026-10-20-interim-normatives-source-ack-to-egor-rus.md`.
- Background: you and the PM agreed orally on 2026-10-18 that I may keep an interim normative
  base in my zone while the catalog grows. This change is that base. Nothing here waits for
  data from you, and no file of your zone changes.

## What the change does

`openspec/changes/interim-normatives-source/` (commit `2b56550`, readiness record
`2026-10-20-interim-normatives-source-readiness.md`) adds:

- a second, temporary parameter source, `InterimParameterSource`, which reads YAML files in
  `backend/interim_normatives/<document>/`. That directory is in the backend zone, not in
  `params/`, `ml/` or `infra/`;
- a setting `DEC_PARAMETER_SOURCE=catalog|interim`. The default stays `catalog`, and the
  setting switches all calculation types at once. The normative search and document
  endpoints keep reading your catalog whatever the setting;
- a verification record next to each value. A profile `strict` uses only values a verifier
  checked; `draft` uses all of them and marks the result;
- an optional `parameter_source` object in the result envelope (kind, data SHA-256,
  profile), shown on the result screen and in the report;
- a sunset date and event in the data. The event is CH3: compare the interim data with the
  catalog, switch back, delete the data.

## What I ask you to acknowledge

1. **The change as a whole**, as the second developer: `openspec/` is shared, and the change
   adds one capability (`interim-normatives`) and three ADDED requirements, next to
   `calculation-api`, `report-generator` and `transparent-output`.
2. **The exception to the catalog-only rule** (`specs/interim-normatives/spec.md`,
   requirement "Scoped exception to the normative-database rule"; `design.md`, decision 9).
   It bounds four requirements, one of them in your WP9 contract:
   `normative-catalog-backend` "Catalog parameter source".
   - The exception holds only while `DEC_PARAMETER_SOURCE=interim`, only for files in the
     interim directory, and only until the sunset event.
   - With the default setting, nothing changes for the catalog.
   - The four MODIFIED deltas follow once those changes are archived (task 1.4).
3. **`NormRef` status is not raised.**
   - A value checked by the verifier still reaches the result as `unverified` /
     `machine-extracted`.
   - The verifier's mark gates only the `strict` profile (`design.md`, decision 4).
   - This keeps your rule that the backend never raises a status. What the mark means for a
     reference's status is left to WP3.

## What I ask you to look at

4. **The record format** (`design.md`, decision 2; the spec lists the fields). A type file
   has five lists, and each mirrors one view of `catalog_read`:

   | List | Fields | View |
   |---|---|---|
   | `formulas` | `parameter`, `result_symbol`, `latex`, `tree`, `units` | `type_formulas` |
   | `table_values` | `parameter`, `symbol`, `latex`, `value`, `unit`, optional `heading_*` | `type_table_values` |
   | `thresholds` | `parameter`, `latex`, `value`, `unit` | `type_thresholds` |
   | `checks` | `parameter` | `type_checks` |
   | `method_bounds` | `quantity`, `kind`, `value`, `unit`, `inclusive` | `type_method_bounds` |

   Every record also carries `norm_refs`, `page` and `verification`.

   **Question 4a.** Does this mirror your views closely enough that CH3 can compare the two
   sources record by record, with the same parameter names, symbols and units? If a column
   is missing, or you plan to change a view before CH3, please say which.

   **Question 4b.** The `tree` field uses the expression-tree JSON we fixed together in WP9
   (`number`, `symbol`, binary operators, `neg`, `call`). Is that still the format your
   ingestion writes?

## How to answer

Add `## Answers` below with one line per item: 1-3 "acknowledged" or your objection, and 4a
and 4b. An acknowledgement in a commit message that names `interim-normatives-source` also
counts (task 1.5).

## Answers

1. **Acknowledged.** The change as a whole.

2. **Acknowledged.** The scoped exception to the catalog-only rule, under the stated
   bounds (only while `DEC_PARAMETER_SOURCE=interim`, only for files in the interim
   directory, only until the sunset event).

3. **Acknowledged.** `NormRef.status` is not raised by the interim source. The backend's
   existing rule stands.

4a. **Yes.** The five view groups in `catalog_read` produce rows whose fields match the
    lists in the table above one-to-one. Parameter names, symbols and units are the same
    keys in both sources, so CH3 can compare record by record without renaming. No
    planned changes to the views for the pilot scope before CH3.

4b. **Yes.** The pipeline builds trees with exactly these node kinds:
    `number`, `symbol`, `add`, `sub`, `mul`, `div`, `pow`, `neg`, `call`.
    Function list: `sqrt`, `exp`, `ln`, `log10`, `sin`, `cos`, `tan`, `abs`, `min`,
    `max`. This is the format agreed in WP9 (`normative-catalog-backend`, decision 3).
    Format unchanged.

Egor, 2026-10-20.
