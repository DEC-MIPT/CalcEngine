# `normative-catalog-backend`: the read contract, for Egor to confirm (2026-10-03)

- Date: 2026-10-03
- From: Akim. To: Egor.
- Context: the change `openspec/changes/normative-catalog-backend/` (WP9) is on
  `develop`, built on your answers of 2026-10-03
  (`normative-catalog-backend-questions-akim.md`, "Answers"). `spec-reviewer` and
  `norm-traceability-checker` pass on it
  (`normative-catalog-backend-readiness.md`). Its task 1.4 waits for your confirmation
  of the items below; the backend side (tasks 3.1 onward) starts after it. Please answer
  in this file under `## Answers`.

Russian version: `normative-catalog-backend-contract-akim-rus.md`.

## 1. Schema, role, database (`design.md` decision 1)

- One schema `catalog_read` with the views and the function `catalog_read.search`, and
  a role `dec_normatives_reader` with `USAGE` on the schema, `SELECT` on its views,
  `EXECUTE` on the function, and nothing else.
- `dec-postgres` runs PostgreSQL 14, where every role may create objects in `public` by
  default, so the ingestion also runs `REVOKE CREATE ON SCHEMA public FROM PUBLIC` and
  revokes `ALL` on your tables from `PUBLIC`.
- Until your infrastructure change splits the databases, all of it lives in your
  current database `dec`; my `DEC_NORMATIVES_DATABASE_URL` points there with the reader
  role.
- The ingestion runs as the database owner (the compose user). The reader's password
  comes from an environment variable of the ingestion, proposed name
  `DEC_NORMATIVES_READER_PASSWORD`, set with `ALTER ROLE ... PASSWORD` and never logged.
- **Your side:** agree, or name another schema, variable or owner.

## 2. The columns (`design.md` decision 2)

The table of decision 2 lists every view, its columns and their types:
`documents`, `clauses`, `search(query, max_rows)`, `type_formulas`,
`type_table_values`, `type_thresholds`, `type_checks`, `type_method_bounds`. Points that
matter most:

- `parameter` is the field name of the pilot's parameters model (`gamma_c1`, `gamma_c2`,
  `k`, `m_gamma`, `m_q`, `m_c`, `k_z_threshold`, `k_z_below`, `k_z_from`, `r`,
  `check_norm_refs`). Each parameter is in exactly one view.
- `norm_refs` is a `jsonb` array of objects with `document`, `edition`, `clause`,
  `status`, `provenance`.
- A selected table has one heading per parameter: `heading_symbol` (an input name, for
  the pilot `phi_II`), `heading_value`, `heading_unit`. Please store the heading in the
  input's base unit where the table allows it (`deg` for `phi_II`): an input typed in
  another unit than the heading's may miss it by the last binary digit (decision 6).
- `type_method_bounds.quantity` is an input name; its `unit` has that input's dimension.
- A unit is a symbol from `backend/app/schemas/units.py` (`kPa`, `m`, `deg`, `1`, ...).
- **Your side:** agree, or list the columns you change. A change after confirmation goes
  through this change's `design.md` and both of us.

## 3. The expression tree (`design.md` decision 3, spec "Expression tree form in the catalog")

The `tree` column holds the JSON that `backend/app/schemas/expression.py` reads: node
kinds `number`, `symbol`, `add`/`sub`/`mul`/`div`/`pow` (`left`, `right`), `neg`
(`operand`), `call` (`function`, `args`) with the functions `sqrt`, `exp`, `ln`,
`log10`, `sin`, `cos`, `tan`, `abs`, `min`, `max`; depth at most 64, at most 4096
nodes. `units` maps every symbol of the tree and the result symbol to a unit. A formula
you cannot convert is not stored as bound.

- **Your side:** agree that `latex2sympy2` output converts into this node set, or name
  the nodes you need added.

## 4. Your tasks (section 2 of `tasks.md`)

- 2.1 the binding of `foundations_shallow_r`; 2.2 the trees; 2.3 `status` and
  `provenance` on every row; 2.4 the headings of table 5.5 (СП 22.13330.2016, edition
  and clause unverified) and the method's range bounds; 2.5 the check of `γc1`, `γc2`,
  `k`, `kz` against the primary text, recorded with a dated file in `docs/decisions/`
  (statuses stay `unverified`); 2.6 the schema, the views, the function and the role,
  idempotent, with an import scan of `ml/`; 2.7 GO, my review, merge.
- Branch: `feature/normative-catalog/data`.
- **Your side:** agree with the split and the verify clauses, or say what to change; and
  give a date for section 2 on `develop`.
