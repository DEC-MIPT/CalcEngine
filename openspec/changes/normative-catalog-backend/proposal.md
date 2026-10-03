# Proposal

Owners: Akim (backend zone) and Egor (data zone). Each task in `tasks.md` names its
owner; no task is in both zones.

## Why

The calculation endpoint (`calculation-api`, WP8) runs a calculation only when a
parameter source gives it the norm-given values: formulas, table values, thresholds, and
the method's range. No such source exists, so `POST /calculations` answers `503` for the
pilot type `foundations_shallow_r`. The normative base that holds these values is
`dec_normatives`, filled by Egor's pipeline, and the backend has no way to read it:

- **WP5 item 9.3** left the read path open. On 2026-10-03 Egor agreed that the contract
  between our zones is the database, not Python code: he owns read-only views in
  `dec_normatives` and a read-only role, and the backend reads only those views through
  its own repository (`docs/decisions/normative-catalog-backend-questions-akim.md`,
  "Answers", items 1-4).
- **WP2 task 7.1c**, the pilot on catalog data, moved here on 2026-10-01. It waits for
  the read path, the stored expression tree, and the selector values of table entries
  (engine review 2026-10-03, minor 6).
- **`normatives-catalog` "Full-text search"** is a requirement with no endpoint: the
  search exists only as Egor's command-line tool.

Egor named the end of 2026-10-04 for his parts, so the backend side can be specified now
and implemented against synthetic views that follow the same contract.

## What Changes

- **A read contract for `dec_normatives`**, owned by Egor and read by the backend:
  - a schema `catalog_read` with a fixed set of views and one search function;
  - a role `dec_normatives_reader` that may only read that schema;
  - both created idempotently by the ingestion and versioned with it;
  - until Egor's infrastructure change splits the databases, all of it lives in his
    current database `dec`.
  The views give: documents and their clauses; for each calculation type, its formulas
  (expression tree and the unit of each symbol), its table values (with the headings that
  select them), its thresholds, the norm references of its checks, and the bounds of the
  method's range. Every entry carries its norm references with the five `NormRef` fields.
- **One JSON form of the expression tree** for the catalog and the engine. It is the form
  the backend's `parse_expression` already reads (WP2 decision 11). Egor's ingestion
  builds the tree and stores it in this form.
- **The binding of a calculation type to its norms** lives in `dec_normatives`. Egor's
  ingestion fills it from a registry he owns, keyed by the type's name. It names formula
  numbers, table cells, and bounds; it never holds a value.
- **Table lookup by exact heading.** The backend selects the table row whose heading
  equals the input, both converted to the input's base unit. An input inside
  the method's range that matches no row is rejected; an input outside the range is
  refused by the range, as `calculation-api` requires. Nothing is interpolated. Each
  resolved table value carries the heading value that selected it, and the engine
  confirms it equals the input.
- **The status of machine-extracted references.** A reference read from the catalog
  keeps the `status` and `provenance` Egor's pipeline wrote. A machine-extracted reference
  is always unverified, and the trace and the report show it that way.
- **Backend read path:**
  - a read-only repository for `DEC_NORMATIVES_DATABASE_URL`;
  - a catalog parameter source behind the `ParameterSource` interface of
    `calculation-api`, configured for every registered type; it converts the bounds of
    the method's range to the inputs' base units;
  - two endpoints, `GET /normatives/search` and `GET /normatives/documents/{document_id}`;
  - `503` when the catalog cannot be reached, without stopping the application.
- **The pilot on catalog data** (former WP2 task 7.1c): `POST /calculations` for
  `foundations_shallow_r` returns `201` with every step taken from `dec_normatives`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `normatives-catalog`: ADDED requirements only. They cover the read contract of
  `dec_normatives`, the expression-tree form, the type binding by name, the table lookup,
  the method range from the catalog, the status of catalog references, the catalog
  parameter source, the search and document endpoints, catalog unavailability, and the
  read-path non-functional limits. No
  requirement of the base spec or of `retarget-mvp-domain` (which modifies "Binding a
  normative to a calculation type" and adds "Norm reference status") is modified here.
  The new requirements narrow those for the backend read path and do not contradict them.
- `calculation-engine`: one ADDED requirement, "Table value selectors": a table value
  carries the heading value that selected it, and the engine confirms it against the
  input. No requirement of `calculation-core-contract`'s delta is modified.

## Non-goals

- Ingestion, parsing, the search ranking itself, and the content of the views: Egor's
  pipeline (`normatives-collector`, `normatives-parser`, `normatives-formula-contract`).
  This change fixes only what the views return.
- Any norm value. No formula, coefficient, threshold, bound, or heading value is written
  in code, configuration, specs, or test data, other than synthetic placeholders. The
  values of the pilot come from `dec_normatives` at run time.
- Verifying a reference against its source text, and the verification gate
  (`norm-source-traceability`, WP3). Catalog references stay as the pipeline wrote them.
- Writing to `dec_normatives` from the backend, and any admin or edit endpoint.
- Interpolation between table rows, until the norm's own rule for it is recorded with
  its clause.
- `normatives-catalog` "Actuality tracking" (the validity date and the outdated-edition
  warning). The views carry the edition only.
- Authentication: the endpoints are open, like those of `calculation-api`, until
  `user-accounts-auth`.
- The frontend catalog page (`frontend-app`).
- Docker and the database setup of `dec_normatives` (Egor's infrastructure).
