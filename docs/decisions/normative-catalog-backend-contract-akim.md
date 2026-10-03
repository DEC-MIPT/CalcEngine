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

## Answers

- Date: 2026-10-04
- From: Egor. To: Akim.
- Note to Akim: each item states an explicit agree/disagree and, where relevant, the
  current state of the pipeline on `develop`, so the decision is unambiguous.

1. **Schema, role, database (decision 1) — Agree, no changes.** I accept every element
   as written: the single schema `catalog_read`, the role `dec_normatives_reader` with
   only `USAGE` on the schema, `SELECT` on its views and `EXECUTE` on the function, and
   the `REVOKE CREATE ON SCHEMA public FROM PUBLIC` plus `REVOKE ALL` on my tables from
   `PUBLIC` (PostgreSQL 14 default). I do not propose another schema name, variable name
   or owner. Concretely:
   - I create the schema, views, function and role idempotently in ingestion
     (`CREATE SCHEMA IF NOT EXISTS`, `CREATE OR REPLACE VIEW`, role created only if it
     does not exist).
   - Until my infrastructure change splits the databases, everything lives in my current
     database `dec`; your `DEC_NORMATIVES_DATABASE_URL` points there with the reader
     role, and only the URL changes at the split.
   - Ingestion runs as the database owner (the compose user). It already connects as
     that owner through `DEC_DATABASE_URL`; I keep that variable and add no second owner
     URL.
   - The reader's password comes from `DEC_NORMATIVES_READER_PASSWORD`, set with
     `ALTER ROLE ... PASSWORD`, and is never printed, logged or committed.

2. **The columns (decision 2) — Agree, no column changes.** I accept every view and
   every column exactly as listed in decision 2; nothing in that table needs to change
   before task 3.1. The pilot's parameters map onto the views as follows:
   - `type_table_values`: `gamma_c1`, `gamma_c2`, `k` (no heading) and `m_gamma`,
     `m_q`, `m_c` (heading `phi_II`, stored in `deg` — the input's base unit);
   - `type_thresholds`: `k_z_threshold`;
   - `type_formulas`: `k_z_below`, `k_z_from`, `r`;
   - `type_checks`: `check_norm_refs`;
   - `type_method_bounds`: the pilot's method range.
   Each parameter appears in exactly one view. Statement of current state (not a change
   request): the schema on `develop` does not yet have the `tree`, the stored
   `status`/`provenance`, the `coefficient` `NormRef`/heading/unit, the binding table or
   the method bounds. Those gaps are exactly my tasks 2.1–2.6, so you can start task 3.1
   against the synthetic contract without waiting for them.

3. **The expression tree (decision 3) — Agree, no additional nodes.** `latex2sympy2`
   output (a SymPy expression) converts into the node set your `parse_expression` reads,
   at ingestion and not in the backend. I need no extra node kinds and no extra
   functions. A formula I cannot convert — a function outside the closed list, an
   unrecognized LaTeX construct, or a tree over the depth (64) or node (4096) limits —
   is not stored as bound; the type is then answered as having no usable parameter
   source, per the spec.

4. **My tasks (section 2) — Agree with the split and the verify clauses.** One
   clarification about the branch point: `feature/normative-catalog/data` branches from
   `develop`, because my pipeline is already on `develop`
   (`ml/src/normatives_pipeline/`); there is no need to branch it from
   `feature/normative-parser/ml`. I deliver section 2 on `develop` by the end of Sunday
   2026-10-04.
