# Design

## Context

See `proposal.md` "Why". The state this design starts from:

- **Backend** (`develop`, after the WP2 and WP8 merges):
  - `services/parameter_source.py` defines `ParameterSource.resolve(calculation_type,
    inputs) -> ResolvedParameters(parameters, method_range)`.
  - `CalculationService.submit` answers `503 parameter_source_unavailable` for a type with
    no source. `create_app(sources=...)` takes the sources; production passes none, so
    every type answers `503` today.
  - The pilot's `Parameters` (`engine/foundations_shallow_r.py`) holds six `TableValue`,
    one `Threshold`, three `Formula` and `check_norm_refs`, all from
    `schemas/resolved.py`.
  - `TableValue` carries no selector values (engine review 2026-10-03, minor 6).
    `table_step` writes the input it was given as the step's substitution, not the
    heading the value was selected by.
  - `schemas/expression.py` `parse_expression` reads the node form of WP2 decision 11,
    and `engine/expression.py` holds the closed function list and the limits (depth 64,
    4096 nodes).
  - `Settings.dec_normatives_database_url` exists and is optional, but `Settings` also
    requires `DEC_APP_DATABASE_URL`. Nothing reads that field yet.
- **Egor's pipeline** (on `develop` under `ml/src/normatives_pipeline/` since 2026-10-03):
  - tables `document`, `clause`, `formula` (LaTeX and an `expression` string, no tree),
    `notation_entry` (symbol, unit), `coefficient` (`row_index`, `col_index`,
    `value TEXT`);
  - `SERIAL` ids, with `pg_trgm` GIN indexes for search;
  - `status` and `provenance` are constants in `build_formula_payload`.
  - Egor's answers of 2026-10-03 (`normative-catalog-backend-questions-akim.md`) agree
    to the read contract, the binding, and the exact-match lookup, and name the end of
    2026-10-04 for his parts.
  - Egor's answers of 2026-10-04 (`normative-catalog-backend-contract-akim.md`,
    "Answers") confirm decisions 1-3 without changes and agree to his section 2 of
    `tasks.md`; the gaps listed above are his tasks 2.1-2.6.
- **Rules that shape the design:**
  - the layer order of WP5 decision 2 (`api` must not import `repositories`);
  - no import between `backend/` and `ml/`;
  - `agent-docs/domain-constraints.md`: no norm value in code or tests, units converted
    at the boundary.

## Goals / Non-Goals

**Goals:**

- One read contract that both zones can test on their own: Egor against his ingestion,
  Akim against a synthetic copy of the views.
- The backend side can be built and reach the coverage gate before Egor's views land on
  `develop`. Only the pilot task (7.1) waits for them.
- No change to the engine's pure function other than carrying and confirming the table
  selectors.

**Non-Goals:**

- A cache of catalog data in the backend. Each calculation reads the catalog again.
  Caching waits until a measured need appears (see "Risks").
- An ORM model of `dec_normatives`. The backend reads views with SQLAlchemy Core and
  owns no migration for that database.

## Decisions

### 1. The contract is a database schema of views, owned by Egor

The contract between the zones is a schema `catalog_read` in `dec_normatives`. Egor's
ingestion creates its views, one SQL function `search`, and the role
`dec_normatives_reader`, idempotently:

- `CREATE SCHEMA IF NOT EXISTS`;
- `CREATE OR REPLACE VIEW`;
- the role is created only if it is missing.

The role gets `USAGE` on the schema, `SELECT` on its views, `EXECUTE` on the function,
and nothing else. `dec-postgres` runs PostgreSQL 14, where every role may create objects
in `public` by default, so the ingestion also runs `REVOKE CREATE ON SCHEMA public FROM
PUBLIC` (and revokes `ALL` on Egor's tables from `PUBLIC`). The views join Egor's tables
with his binding table; the binding table and his own tables stay outside the contract.

Database, owner and credentials, until Egor's infrastructure change splits the
databases:

- `dec_normatives` is Egor's current database `dec` on `dec-postgres`. The backend's
  `DEC_NORMATIVES_DATABASE_URL` points at it with the reader role.
- The ingestion runs as the database owner (the compose user), which may create the
  schema and the role. The backend never uses that user.
- The ingestion connects as the owner through `DEC_DATABASE_URL`, which Egor keeps, and
  has no second owner URL. The two variables stay distinct: `DEC_DATABASE_URL` is the
  owner's URL of the ingestion, `DEC_NORMATIVES_DATABASE_URL` the reader's URL of the
  backend. This replaces Egor's plan of 2026-09-29 to rename his variable to
  `DEC_NORMATIVES_DATABASE_URL` (WP5 task 2.1).
- The reader's password comes from an environment variable of the ingestion,
  `DEC_NORMATIVES_READER_PASSWORD` (confirmed by Egor on 2026-10-04). The
  ingestion sets it with `ALTER ROLE ... PASSWORD` and never prints or logs it. Akim puts
  the same password into his local `DEC_NORMATIVES_DATABASE_URL`; neither is committed.
- When the infrastructure change creates a separate `dec_normatives` database, only the
  URL changes; the schema, the role and the views keep their names.

- **Why:** Egor's answer 1 (2026-10-03), confirmed without changes on 2026-10-04. The
  backend cannot import his package (WP5), and he keeps the freedom to change his tables
  behind the views.
- **Alternatives:**
  - Read Egor's tables directly. Every change to his schema would break the backend.
  - A small HTTP service in his zone. This adds a process, a port, and a deployment for
    what one SQL query does.
  - A shared Python package. This breaks the import rule.

### 2. The columns of the contract

`norm_refs` is a `jsonb` array of at least one object with the keys `document`,
`edition`, `clause`, `status` (`verified` | `unverified`), and `provenance`
(`human-verified` | `machine-extracted`). A value is `numeric`. A unit is a unit symbol
from the backend's `schemas/units.py` list (for example `kPa`, `m`, `deg`, `1`).

| Object | Columns | Notes |
|---|---|---|
| `catalog_read.documents` | `document_id int`, `designation text`, `title text`, `edition text`, `year int null`, `source_url text null` | One row per document. |
| `catalog_read.clauses` | `document_id int`, `position int`, `number text`, `title text null`, `page int null` | `position` gives document order. |
| `catalog_read.search(query text, max_rows int)` | returns `kind text` (`document`, `clause`, `formula`), `document_id int`, `designation text`, `edition text`, `number text null`, `title text null`, `rank real` | Egor's ranking (`pg_trgm`); at most `max_rows` rows. |
| `catalog_read.type_formulas` | `calculation_type text`, `parameter text`, `result_symbol text`, `latex text`, `tree jsonb`, `units jsonb` (symbol id → unit, including the result symbol), `norm_refs jsonb` | One row per formula parameter. |
| `catalog_read.type_table_values` | `calculation_type text`, `parameter text`, `symbol text`, `latex text`, `value numeric`, `unit text`, `heading_symbol text null`, `heading_value numeric null`, `heading_unit text null`, `norm_refs jsonb` | One row per table row for a selected parameter, one row with null headings for a parameter that no input selects. |
| `catalog_read.type_thresholds` | `calculation_type text`, `parameter text`, `latex text`, `value numeric`, `unit text`, `norm_refs jsonb` | |
| `catalog_read.type_checks` | `calculation_type text`, `parameter text`, `norm_refs jsonb` | The references of a check (`check_norm_refs` for the pilot). |
| `catalog_read.type_method_bounds` | `calculation_type text`, `quantity text`, `kind text` (`min` \| `max`), `value numeric`, `unit text`, `inclusive bool`, `norm_refs jsonb` | The method's range of application (WP2 decision 15). `quantity` is an input name; `unit` has that input's dimension (decision 11). |

A synthetic example of one `norm_refs` element, in the placeholder form of WP1 "Norm
reference status":

```json
{"document": "<NORM-DOC-PLACEHOLDER>", "edition": "unverified",
 "clause": "<CLAUSE-PLACEHOLDER>", "status": "unverified",
 "provenance": "machine-extracted"}
```

- `parameter` is the field name of the calculator's parameters model (`gamma_c1`, `m_q`,
  `k_z_threshold`, `r`, `check_norm_refs` for the pilot). A heading's symbol is an input
  name of the type (`phi_II`).
- One parameter appears in exactly one of the four `type_*` parameter views, the one
  that matches the kind its field has in the parameters model (`Formula`, `TableValue`,
  `Threshold`, `NormRefs`).
- A selected table has one heading per parameter: every row of a parameter carries the
  same `heading_symbol`, or no row does. A selection by two inputs needs new columns and
  a change to this decision.
- **Why:** the views map one to one onto `schemas/resolved.py` and `MethodBound`, so the
  backend only validates. Egor's answer 2 lists the same content; on 2026-10-04 he
  confirmed every column without changes and placed each pilot parameter in exactly one
  view.
- **Alternative:** one generic `type_parameters` view with a `kind` column and nullable
  columns per kind. It is harder to validate, and the per-kind views stay small.

### 3. The expression tree is the JSON form `parse_expression` reads

The `tree` column holds exactly the JSON that `schemas/expression.py` validates, as the
spec "Expression tree form in the catalog" lists it. Egor builds it at ingestion
(`latex2sympy2`, then a conversion into these nodes) and refuses to store a formula he
cannot convert.

- **Why:** the user's decision of 2026-10-03, and WP2 task 1.8, which Egor
  acknowledged. The engine already evaluates this form, so the backend parses no text.
  On 2026-10-04 Egor confirmed that `latex2sympy2` output converts into this node set
  at ingestion and that he needs no other node kinds or functions.
- **Alternatives:** SymPy `srepr`, or MathML. Both would need a parser in the backend,
  which WP2 decision 11 rules out.

### 4. A separate settings class and a lazy, read-only engine

`NormativesSettings` holds only the optional `DEC_NORMATIVES_DATABASE_URL`, so the
catalog works without `DEC_APP_DATABASE_URL`. It is the only reader of that variable:
task 3.1 removes the unused `dec_normatives_database_url` field from `Settings` (WP5,
Akim's zone). The catalog session factory is built on the first request that needs it,
under the same lock pattern as `dec_app` (`api/dependencies.py`), and is disposed at
shutdown when the application built it. The engine has these options:

- `hide_parameters=True`;
- `pool_pre_ping=True`;
- `connect_args={"options": "-c default_transaction_read_only=on"}`.

Every transaction is therefore read-only, even if the role were wrong.

Errors map like this:

- the variable is unset, or a connection error (`OperationalError`, `InterfaceError`)
  occurs: `CatalogUnavailableError` on the catalog endpoints;
- the same conditions inside a parameter source: `ParameterSourceUnavailableError`.

- **Why:** the spec "Catalog unavailability". This is the WP8 decision 7 pattern for
  `dec_app`.
- **Alternative:** a connection at start-up. That stops the application when the
  catalog is down, which the spec forbids.

### 5. Layers

- `repositories/normatives.py`: Core queries on `catalog_read`, returning plain row
  dataclasses defined in `schemas/normatives.py`. Every client value is a bound
  parameter.
- `services/catalog_source.py`: `CatalogParameterSource` implements `ParameterSource`. It
  reads a type's rows in one short session and builds `Formula`, `TableValue`,
  `Threshold`, `NormRefs` and `MethodBound`. It selects table rows (decision 6) and
  validates the result with the type's parameters model.
- `services/normatives.py`: search and document reads for the endpoints.
- `schemas/normatives.py` also holds `CatalogSnapshot` (decision 6).
- `api/normatives.py`: the two endpoints, using response models from
  `schemas/normatives.py`.
- Each registration in `services/catalog.py` also names the type's parameters model
  (`foundations_shallow_r.Parameters`). `create_app` then configures a
  `CatalogParameterSource` for every registered type, unless the caller passes `sources`
  (tests).

- **Why:** this keeps WP5's order: `api` > `services` > `repositories` > `db` >
  `schemas`. WP5's design (`backend-layered-architecture` design.md, the read path of
  item 9.3) allowed the `parameters` layer to read `repositories` for norm values. This
  change places the catalog source in `services` instead, because it also needs the
  engine's conversion and applicability check, which `parameters` may not import; task
  8.1 records the placement in WP5.
- **Alternative:** put the parameters model on the `Calculator` class. That changes
  WP5's `Calculator` contract for a concern of the parameter source.

### 6. Table selection in the source, confirmation in the engine

The source runs inside `CalculationService.submit` after `request.check_against`, so
the inputs already fit the type's contract: every declared input is present, and every
unit is in the vocabulary and of the input's dimension. A conversion of a client value
below can therefore fail only by overflow, which raises `UnitError` and gives
`422 invalid_input`, as at the engine's boundary. A conversion of a heading value that
fails (`UnitError`, including overflow) is a catalog data breach (decision 7).

For a parameter with a heading, the source:

1. converts the inputs to their base units with `engine.boundary.inputs_to_base_units`
   and the type's contract from the registry, exactly as `engine/boundary.run` does
   (`services` may import `engine`);
2. converts each row's heading, `QuantityValue(float(Decimal(heading_value)),
   heading_unit)`, to the base unit of the input named by `heading_symbol` with
   `engine.boundary.convert`;
3. keeps the rows whose converted heading equals the base-unit input (float equality).

`confirm_selectors` in the engine repeats steps 2-3 with the same call on the same two
values (the carried selector and the base-unit input that `engine/boundary.run` hands
the calculator), so the source and the engine compare the same two floats and cannot
disagree. Comparing in the base unit also matches an input that the client typed in
the heading's own unit: the input and the heading then take the same conversion
`x · f_heading / f_base` and give the same float. An input in any unit other than the
heading's own takes a different rounding path and may miss by one ulp. This includes
the base unit itself when the heading is stored in another unit: the input then passes
unchanged while the heading is converted. Such an input matches no row (`422`) and is
never accepted by a near match. For a selecting input, Egor stores the heading in the
input's base unit where the norm's table allows it (task 2.4), so this case does not
arise for the pilot's data.

The outcome of that match:

- one row: that row's value, with its heading as the selector;
- two or more rows with the same heading value: a data error (decision 7);
- no row: the source first checks the method's range (below). Only an input inside the
  range is rejected with `InputValidationError` and one
  `FieldError(("body", "inputs", heading_symbol), "No table row matches this input.")`,
  which gives `422 invalid_input`.

The range takes precedence because `calculation-api` requires an input outside the
method's range to give a stored refusal (`201`), not `422`. When no row matches, the
source calls the engine's pure `check_applicability` with the base-unit inputs of step
1, the converted method bounds (decision 11), and an empty validated range: only the
refusal matters here, and its warnings are discarded. `CalculationService.run` checks
again with the engineer's validated range. If it refuses, the source returns
`ResolvedParameters(parameters=CatalogSnapshot(...), method_range=...)`.

`CatalogSnapshot` is a frozen pydantic model in `schemas/normatives.py`. It holds the
type's catalog rows with every table row unselected, as `float` and `str` fields built
from the rows (no `Decimal`, no bare dataclass), so `engine/hashing.input_hash` can
normalize it. The engine refuses before it calls the calculator (`engine/boundary.run`),
so the calculator never sees the snapshot. `input_hash` covers the snapshot, so a
refused result still identifies the catalog data it was refused with.

No interpolation, rounding or nearest-row rule is made here. A rule for a value between
rows comes only from the norm's own text, with its document, edition and clause, in a
later change.

`TableValue` gains `selectors: tuple[Selector, ...]` (spec `calculation-engine` "Table
value selectors"), where `Selector` is `(symbol, value: QuantityValue)` with the heading
unit. It holds at most one selector under decision 2, and is empty for an unselected
entry; the tuple keeps the engine side open for a later two-key table. A selector whose
symbol is not an input of the type makes `confirm_selectors` raise `CalculationError`.
`table_step` takes its substitutions from `entry.selectors`. A new engine helper,
`confirm_selectors(entry, inputs)`, converts each selector's value to the base unit of
the base-unit input named by the selector's symbol with `engine.boundary.convert`, and
raises `CalculationError` if the result differs from that input. The pilot calls it
before `table_step`.

- **Why:** Egor's answer 4 and minor 6 of the engine review. The engine stays pure and
  never looks anything up, but it can no longer silently use a value selected for
  another input.
- **Alternative:** pass the whole table to the engine and select there. This moves a
  lookup into the pure function and widens `Parameters` for every table.

### 7. Data errors are a missing source, not an internal error

Any breach of the contract in a type's rows makes `CatalogParameterSource` raise
`ParameterSourceUnavailableError(f"... {calculation_type!r} ...")`, which gives
`503 parameter_source_unavailable`, naming the type. A breach is:

- a missing or undeclared parameter;
- a parameter in two `type_*` views, or in a view whose kind does not match its field;
- a tree that `parse_expression` refuses;
- a unit outside the list;
- a value that is not a finite number;
- an empty or invalid `norm_refs`, or a `NormRef` invariant broken;
- duplicate headings (equal after conversion to the input's base unit), rows with and
  without a heading mixed in one parameter, or two heading symbols in one parameter;
- a `heading_symbol` that names no input of the type, a `heading_unit` outside the
  list or of another dimension than that input, or a heading value whose conversion to
  the input's base unit overflows;
- a method bound whose `quantity` is not an input of the type, or whose unit has another
  dimension than that input;
- a method range that `check_bounds` (`schemas/calculation.py`) refuses, such as two
  bounds of one kind on one quantity or an empty range. The source calls `check_bounds`
  on the converted bounds before any `check_applicability`, so this never reaches the
  engine as a `500`.

No limit on decimal places is applied to catalog values: `MAX_DECIMALS` belongs to the
rounding rules of `calculation-core-contract`, and a `numeric` value from the norm is
passed on as `float(Decimal(value))`, rounding nothing.

Before that, the source writes one warning line,
`code=catalog_data_invalid type=<type> parameter=<parameter>` (without `parameter=` when
the breach has no parameter, as for a missing binding), with no value and no pydantic
text.

- **Why:** the client can do nothing about bad catalog data, and the type is in effect
  unavailable until Egor fixes it. A `500` would hide which type is broken.
- **Alternative:** a `500 internal_error`. This was rejected for that reason.

### 8. Errors and messages added to the API layer

`api/errors.py` gains `(CatalogUnavailableError, 503, "catalog_unavailable")` in
`DEC_ERRORS`, with the fixed message "The normative catalog is not available.". The
search `q` is an `Annotated[str, StringConstraints(strip_whitespace=True, min_length=2,
max_length=200)]`, so its errors are of the static types (`string_too_short`,
`string_too_long`, `missing`) and never echo the value. `document_id` is a `Path(gt=0)`
integer.

### 9. Testing without Egor's database

The backend has two kinds of tests:

- **Fast tests:** SQLite attaches an in-memory database named `catalog_read` that holds
  tables with the views' columns, filled with synthetic placeholders. These tests cover
  the repository's view queries, the source, the selection, and the endpoints.
- **Postgres module:** with `DEC_TEST_NORMATIVES_DATABASE_URL` (database
  `dec_normatives_test` on `dec-postgres`, created by hand like `dec_app_wp8_test`), the
  module runs `backend/tests/sql/catalog_contract.sql`. It creates `catalog_read` with
  synthetic tables, a `search` function, and the role. It tests:
  - the `search` call;
  - the role's refusals;
  - the read-only transaction;
  - SQL-looking queries.

  Without the variable, the module is skipped.

A contract test reads `information_schema.columns` of `catalog_read` and compares it with
decision 2. It runs on the synthetic database, and on Egor's database when
`DEC_NORMATIVES_DATABASE_URL` points to one with the ingested data (task 7.1). Every
value in the test data is a synthetic placeholder (`domain-constraints.md`).

### 10. The C/C++ boundary does not move

The read path is I/O and is not a hot path. The swap boundary stays the pure function
`engine.pipeline.calculate` (WP2, WP5 decision 7). Selection lives in `services`, and the
only engine change is `confirm_selectors`, a pure comparison inside that boundary.

### 11. Method bounds are converted to the input's base unit

For each row of `type_method_bounds`, the source finds the input named by `quantity` in
the type's contract, converts `QuantityValue(value, unit)` to that input's base unit with
`engine.boundary.convert`, and builds `MethodBound(quantity, kind, value, inclusive,
source=norm_refs)` with the converted value. `MethodBound.value` is a bare float in the
input's base unit (`schemas/calculation.py`), which is what `check_applicability`
compares.

- **Why:** spec "Method range from the catalog"; units are converted at the boundary,
  never inside the engine (`domain-constraints.md`).
- **Alternative:** require Egor to store bounds in base units. That couples his data to
  the backend's choice of base units.

## Non-functional requirements

- **Performance** (spec "Non-functional — catalog read path"): one parameter resolution
  is at most five queries, one per `type_*` view (formulas, table values, thresholds,
  checks, method bounds), on indexed binding keys that Egor provides. Task 7.2 measures
  20 resolutions, 20 searches and 20 document requests on the ingested data.
- **Security:**
  - the read-only role and read-only transactions;
  - bound parameters only;
  - `hide_parameters`;
  - the database URL kept in a `SecretStr`, never formatted into a message;
  - the WP8 error boundary (`UnexpectedErrors`) unchanged.
- **Coverage:** at least 95% branch coverage of the changed backend code in `check.sh`.
  The `tester` also runs the postgres module.
- **Accessibility:** not applicable; no user interface changes.

## Risks / Trade-offs

- [Egor's views land late or with other columns] → The backend is built against
  decision 2 and the contract test fails loudly. Only task 7.1 waits. A column change
  goes through this change's `design.md`, acknowledged by both owners.
- [Float equality of headings after a unit conversion] → The source and the engine
  convert the same heading to the input's base unit with the same call (decision 6), so
  they compare the same floats; an input typed in the heading's own unit matches
  exactly. Tests use a synthetic heading unit other than the base unit, with the input
  in the heading's unit. An input in any other unit, the base unit included when the
  heading is stored in another unit, may miss by one ulp; it matches no row and is
  rejected with `422`, never accepted by a near match. This limit is accepted; storing
  headings in the input's base unit (task 2.4) avoids it, and task 5.3 asserts the
  `422` for it.
- [One catalog round trip per calculation] → Under 2 s is the limit, and the pilot reads
  only a few dozen rows. A cache is a later change if task 7.2 shows a need.
- [Machine-extracted data makes every pilot step unverified] → This is the intended
  behavior (Egor's answer, "Status"). The report shows it, and WP3 owns verification.
- [The synthetic `catalog_contract.sql` repeats the view definitions in the backend
  zone, so it can drift from Egor's real views] → The contract test of task 4.3 compares
  columns with decision 2 on both databases; real drift is caught at the latest by task
  7.1, before the backend feature merges.
- [SQLite does not run the search function] → The function's call and ranking are
  covered by the postgres module, which the `tester` runs before GO.

## Migration Plan

- `dec_app`: no migration.
- `dec_normatives`: Egor's ingestion creates `catalog_read` and the role. Rollback is
  `DROP SCHEMA catalog_read CASCADE` and dropping the role. The backend then answers `503`
  on the catalog paths and keeps serving the rest.
- Configuration: `DEC_NORMATIVES_DATABASE_URL` uses the `dec_normatives_reader`
  credentials. Until Egor's database split, it points at his current database (`dec`).
