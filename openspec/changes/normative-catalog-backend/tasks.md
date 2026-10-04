# Tasks

Owners: Akim (backend zone) and Egor (data zone). WP9.

Branches: two features, one per zone (`AGENTS.md`, Branching rules).

- `feature/normative-catalog/data` (Egor): section 2. It branches from `develop`, where
  Egor's pipeline is (his answer of 2026-10-04), and is merged into `develop` when
  section 2 is done, after its `tester` GO and Akim's review.
- `feature/normative-catalog/backend` (Akim): sections 3-7. It branches from `develop`.
  Sections 3-6 do not wait for Egor: they run against the synthetic contract of
  `design.md` decision 9. Section 7 waits for `feature/normative-catalog/data` to be on
  `develop`, and the branch is merged into `develop` only after that, when every task of
  sections 3-7 is done, after its `tester` GO and the review.

Spec work (sections 1 and 8) is committed directly to `develop`. Checkboxes are ticked in
`develop` as each subtask is done on its feature branch.

Code journal: `docs/akim/reports/WP9-code-journal.md`, created before task 3.1 (Akim's
tasks only).

## 1. Spec readiness

- [x] 1.1 (spec) Run `openspec validate normative-catalog-backend --strict` and
  `openspec validate --all --strict`; verify: both pass
- [x] 1.2 (spec) Run `spec-reviewer` on this change and resolve its findings until a
  report on the current version lists no blocker and no major finding; record the passes
  in `docs/decisions/normative-catalog-backend-readiness.md` (with a Russian copy)
- [x] 1.3 (spec) Run `norm-traceability-checker`; verify: its report finds no
  requirement that fixes a norm-derived formula, coefficient, limit, heading or rounding
  rule; the engine, API and performance limits are labelled as non-norm; the example
  reference in `design.md` decision 2 is the synthetic placeholder; and the only real
  designations are those of tasks 2.4 and 2.5 (СП 22.13330.2016, its table 5.5 and the
  coefficients of the pilot), marked unverified and taken from
  `docs/decisions/first-calculation-type-egor-pm.md` (table 5.5) and
  `docs/decisions/calculation-core-contract-formula-execution-akim.md` (the
  coefficients)
- [x] 1.4 (spec) Ask Egor to confirm `design.md` decisions 1-3 (schema `catalog_read`,
  the privileges and the `REVOKE` on `public`, the interim database `dec`, the owner that
  runs the ingestion, the reader's password variable, the columns of each view, the tree
  form) and his tasks in section 2, in
  `docs/decisions/normative-catalog-backend-contract-akim.md` (with a Russian copy;
  answers under `## Answers` in the same file); verify: his answer is committed on
  `develop`, and any column he changes is applied to decision 2 and to this list before
  task 3.1 starts (2026-10-04, `348955c`: Egor agrees to decisions 1-3 and section 2
  without changes, no column changed; section 2 on `develop` by the end of 2026-10-04)

## 2. Read contract in `dec_normatives` (data, Egor)

Egor may split these tasks further on his branch; each one stays in his zone.

- [ ] 2.1 [Egor] Store the binding of `foundations_shallow_r` from a registry in his
  zone: for each parameter of the pilot (`design.md` decision 2, column `parameter`), the
  formula number, table, table cell or heading, threshold, check, or method bound it
  comes from, never a value (data); verify: his test shows one binding row per parameter
  of the pilot and no value column in the binding table
- [ ] 2.2 [Egor] Store each bound formula's expression tree in the JSON form of the spec
  "Expression tree form in the catalog", with the unit of every symbol and of the
  result symbol, built at ingestion (data); verify: his test validates every stored tree
  of the pilot against the node set, the function list and the limits, and a formula he
  cannot convert is not stored as bound
- [ ] 2.3 [Egor] Store `status` and `provenance` per formula, table value, threshold,
  check and method bound, as the pipeline sets them (`machine-extracted`, `unverified`)
  (data); verify: his test shows both columns on every row the views give for the pilot,
  and no `machine-extracted` row with status `verified`
- [ ] 2.4 [Egor] Store the row headings of the pilot's selected table (table 5.5 of
  СП 22.13330.2016; edition and clause unverified until checked against the primary
  text) with their symbol and unit (the selecting input's base unit where the table
  allows it, `design.md` decision 6), and the method's range bounds of the pilot with
  their quantity and unit (data); verify: his test shows one heading symbol, value and
  unit on every row of each selected parameter, no duplicate heading value, and every
  bound naming an input of the pilot
- [ ] 2.5 [Egor] Check the coefficients `γc1`, `γc2`, `k`, `kz` of the pilot against the
  primary text of СП 22.13330.2016 (edition and clauses unverified until this check) and
  store them like the table of task 2.4, each with its `NormRef` (data); verify: a dated
  record in `docs/decisions/` names, for each coefficient, the document, the edition and
  the clause or table it was found in, and who checked it; the stored rows keep
  `provenance = machine-extracted` and `status = unverified`, because raising a status is
  the gate of `norm-source-traceability` (WP3), not of this change
- [ ] 2.6 [Egor] Create the schema `catalog_read` with the views and the `search`
  function of `design.md` decision 2, and the role `dec_normatives_reader` with the
  privileges, the `REVOKE` on `public` and the password variable of decision 1,
  idempotently, as part of ingestion (data); verify: running the ingestion twice
  succeeds, the columns match decision 2, as the role an `INSERT`, a `CREATE TABLE` in
  `public` and a `SELECT` on a table outside `catalog_read` are all refused, the password
  appears in no log, and an import scan of `ml/` finds no import of the backend's package
- [ ] 2.7 [Egor] `tester` GO for `feature/normative-catalog/data`, Akim's review, and
  the merge into `develop` (data); verify: the GO and the review are recorded in
  `docs/decisions/normative-catalog-backend-readiness.md`

## 3. Groundwork (backend, Akim)

- [x] 3.1 Create `feature/normative-catalog/backend` from `develop`. Add
  `NormativesSettings` (only the optional `DEC_NORMATIVES_DATABASE_URL`) and remove the
  unused field from `Settings`; add `CatalogUnavailableError` with its row in
  `DEC_ERRORS` and its fixed message (`design.md` decisions 4 and 8) (backend); verify:
  tests show the setting unset by default and read from the environment without
  `DEC_APP_DATABASE_URL`, a search of `backend/app` finds no other reader of the
  variable, and a raised `CatalogUnavailableError` answers `503 catalog_unavailable`
  with the fixed message
- [x] 3.2 Add the lazy catalog session factory: built on the first request that needs
  it under a lock, read-only connections, `hide_parameters`, `pool_pre_ping`, disposed at
  shutdown when the application built it (decision 4) (backend); verify: tests show one
  engine for two concurrent first requests, the engine options set, disposal at shutdown
  and no disposal of a given factory, and an unset variable raising
  `CatalogUnavailableError` without the URL in the message
- [x] 3.3 Add the synthetic contract for tests: a SQLite fixture with an attached
  `catalog_read` database holding tables with the columns of decision 2, and
  `backend/tests/sql/catalog_contract.sql` for the postgres module (schema, tables named
  like the views, a `search` function, the role with the privileges and the `REVOKE` of
  decision 1); every value a synthetic placeholder
  (decision 9) (backend); verify: both fixtures load in tests, and a scan of the fixture
  data finds only the placeholder documents and values listed in the fixture's module

## 4. Repository and schemas (backend, Akim)

- [x] 4.1 Add `schemas/normatives.py` (the row dataclasses of each view, the search hit,
  the document view with its clauses, the parsed `norm_refs` list) and
  `repositories/normatives.py` with one Core query per view, every client value bound
  (decision 5) (backend); verify: tests against the SQLite fixture read each view for a
  type, return only that type's rows, return clauses in `position` order, and an unknown
  document id returns none
- [x] 4.2 Add the `search` call to the repository and the postgres module
  `test_normatives_postgres.py` with `DEC_TEST_NORMATIVES_DATABASE_URL` (decision 9)
  (backend); verify: in the module the search returns the fixture's ranked rows capped
  at `max_rows`, a Russian query finds a clause with that word in its title, a query
  with quotes and SQL syntax is sent as one statement with the text as a bound parameter
  (statement capture through a SQLAlchemy event), a write through the catalog session
  is refused, the role can neither read outside `catalog_read` nor create a table in
  `public`, and the module is skipped without the variable
- [x] 4.3 Add the contract test: `information_schema.columns` of `catalog_read` equals
  the column list of decision 2 (backend); verify: it passes on the synthetic postgres
  database and fails when a column is renamed in the fixture
- [ ] 4.4 Order ties inside the synthetic `catalog_read.search` before its `LIMIT`, as
  decision 2 now says (added 2026-10-04 from Egor's answer in
  `docs/decisions/normative-catalog-search-order-questions-akim.md`) (backend); verify:
  in the postgres module, a search whose hits tie in rank at the `max_rows` cut keeps
  the first hits in the order `rank DESC`, `designation`, `number`, and the endpoint
  test with `limit` keeps the same hits

## 5. Catalog parameter source and the engine change (backend, Akim)

- [x] 5.1a Add `Selector` and `TableValue.selectors` in `schemas/resolved.py`,
  `confirm_selectors` in the engine, and take `table_step` substitutions from the
  entry's selectors (spec `calculation-engine` "Table value selectors", decision 6)
  (backend); verify: tests show a step whose substitution is the carried heading, a
  `CalculationError` when a carried heading differs from the input and when its symbol
  names no input, and a heading in a synthetic unit other than the input's base unit
  confirmed for an input given in the heading's unit with the heading's value
- [x] 5.1b Update the pilot to call `confirm_selectors` before each selected table step,
  and the engine and report tests to the new `TableValue` (backend); verify: the
  syntax-tree scan of the pilot still finds no numeric literal other than `0` and `1`,
  and `check.sh` passes with the existing engine and report tests
- [x] 5.2 Add `CatalogParameterSource` building `Formula`, `TableValue`, `Threshold`,
  `NormRefs` and `MethodBound` from the repository's rows, validated by the type's
  parameters model, with each registration in `services/catalog.py` naming that model,
  and each method bound converted to its input's base unit (decisions 5 and 11)
  (backend); verify: on synthetic rows for the pilot, `resolve` returns parameters equal
  to the expected `Parameters` and method range, with every reference as the rows gave
  it, and a bound given in another unit of the same dimension arrives converted
- [x] 5.3 Add the table selection by exact heading, with the method range checked first
  when no row matches (decision 6) (backend); verify: tests show the matching row
  chosen, an input given in a heading unit other than the base unit with the heading's
  value matching that row, an input in the base unit against a heading stored in
  another unit that misses by one ulp answering `422` (decision 6, accepted limit), an
  input inside the range between rows raising `InputValidationError` located at
  `["body", "inputs", <heading symbol>]` with the fixed message, an input outside the
  range and off every row giving `POST /calculations` `201` with verdict `refused` and
  the violated bound, an `input_hash` of that refused result of 64 hex characters and
  equal on a second identical request, and an unselected entry carrying no selector
- [x] 5.4 Add the data checks of decision 7 (backend); verify: one test per breach
  (missing parameter, undeclared parameter, a parameter in two views or in the wrong
  view, unparsable tree, symbol without unit, unit outside the list, non-finite value,
  empty `norm_refs`, `machine-extracted` with `verified`, duplicate headings, mixed rows
  with and without a heading, two heading symbols in one parameter, a heading symbol
  that names no input, a heading unit of another dimension, a heading whose conversion
  overflows, a bound whose
  quantity is not an input, a bound of another dimension, two bounds of one kind on one
  quantity, an empty range, no binding for the type) raises
  `ParameterSourceUnavailableError` naming the type, and writes one
  `code=catalog_data_invalid` line naming the type, and the parameter when there is
  one, and no value
- [x] 5.5 Map an unreachable or unconfigured catalog inside the source to
  `ParameterSourceUnavailableError` (decision 4) (backend); verify: a test with a closed
  port and a test without the variable both give `503 parameter_source_unavailable` on
  `POST /calculations`, nothing is stored, and neither the response nor the log holds the
  URL or its password

## 6. Endpoints and wiring (backend, Akim)

- [x] 6.1 Configure a `CatalogParameterSource` for every registered type in
  `create_app` unless `sources` is given (decision 5) (backend); verify: an application
  built without `sources` answers `POST /calculations` for the pilot from the SQLite
  fixture with `201`, every step carrying the fixture's references, and the existing
  WP8 tests that pass `sources` still pass
- [x] 6.2 Add `GET /normatives/search` with its `q` and `limit` limits (spec "Normative
  search endpoint", decision 8) (backend); verify: tests show the ranked hits capped by
  `limit`, a Russian query passed through unchanged, `{"hits": []}` for no match, `422
  validation_error` without the value for a missing, short, long or blank `q` and for
  `limit` outside 1-50, and `503 catalog_unavailable` without the variable
- [x] 6.3 Add `GET /normatives/documents/{document_id}` (spec "Normative document
  endpoint") (backend); verify: tests show `200` with clauses in order, `404 not_found`
  for an unknown id, `422 validation_error` without the value for `0`, a negative or a
  non-integer id, and `503 catalog_unavailable` without the variable
- [x] 6.4 Add the new endpoints' OpenAPI responses and a test that the application
  starts and serves `GET /health` and `GET /calculation-types` with the catalog
  unreachable, then serves a catalog request once it is back (spec "Catalog
  unavailability") (backend); verify: the OpenAPI document lists `200`, `422` and `503`
  for `GET /normatives/search` and `200`, `404`, `422` and `503` for
  `GET /normatives/documents/{document_id}`, each error with the error body, and the
  recovery test passes
- [x] 6.5 Run `backend/check.sh` and the two postgres modules (backend); verify: ruff,
  mypy and pytest pass, branch coverage is at least 95% (target 100%), and the import
  scan finds no backend import of the pipeline's package

## 7. Pilot on catalog data (backend, Akim; waits for section 2 on `develop`)

- [ ] 7.1 Run the pilot `foundations_shallow_r` end to end on Egor's ingested
  `dec_normatives`, the former WP2 task 7.1c (backend); verify: with
  `DEC_NORMATIVES_DATABASE_URL` as `dec_normatives_reader`, the contract test of task 4.3
  passes on his database, `POST /calculations` for a request whose `phi_II` is a heading
  of the bound table answers `201`, every formula, table and threshold step carries a
  catalog reference with the status the catalog gave, and the stored result names the
  catalog's documents and editions; a Russian search for a word of a clause title of
  the ingested pilot document has that clause among its hits; the tests assert
  structure and statuses, never a norm value
- [ ] 7.2 Measure the read path on the ingested data (spec "Non-functional — catalog
  read path") (backend); verify: 20 parameter resolutions, 20 searches and 20 document
  requests each take under 2 seconds on a developer machine as the spec defines it,
  recorded with the machine and the times in the code journal
- [ ] 7.3 `tester` GO for `feature/normative-catalog/backend`, the review by Egor or the
  orchestrator, and the merge into `develop` (backend); verify: the GO and the review are
  recorded in `docs/decisions/normative-catalog-backend-readiness.md`

## 8. Close

- [ ] 8.1 (spec) Record in `calculation-core-contract` that task 7.1c is done here and
  that minor 6 of the engine review is fixed by tasks 5.1a-5.1b under the new
  `calculation-engine` requirement "Table value selectors"; record in
  `backend-layered-architecture` that item 9.3 is settled by this change and that the
  catalog source sits in `services`, not in `parameters` (`design.md` decision 5);
  record in `calculation-api` that its error table gains the row `catalog_unavailable`
  from this change and that `invalid_input` also covers an input that the catalog's
  table does not cover (both owners agree to the edits); verify: the notes are on
  `develop`
- [ ] 8.2 (spec) After both features are merged, `spec-keeper` syncs `normatives-catalog`
  and archives this change; verify: `openspec validate --all --strict` passes after the
  archive

## DOR checklist

- [x] `proposal.md`, `specs/normatives-catalog/spec.md`,
  `specs/calculation-engine/spec.md`, `design.md` and `tasks.md` exist and pass
  `openspec validate --strict` (task 1.1)
- [x] A `spec-reviewer` report on the current version lists no blocker and no major
  finding (task 1.2), and `norm-traceability-checker` passes (task 1.3)
- [x] Egor has confirmed the read contract and his section 2 (task 1.4)
- [ ] Functional requirements are recorded as requirements with scenarios; the
  non-functional ones (performance, security, coverage) are in "Non-functional — catalog
  read path"
- [ ] Each task fits one session and names how it is verified; each task with code
  belongs to exactly one of the two features above
- [ ] Dependencies are listed: `normatives-formula-contract` tasks 1.4-1.7 and the move
  to `ml/` (Egor, for section 2; the move is done); `retarget-mvp-domain` task 3.1
  (Egor, for task 7.1); `calculation-api` merged on `develop` (done). Egor's planned
  infrastructure change (a separate `dec_normatives` database) is not a dependency: until
  it exists, the contract lives in `dec` (`design.md` decision 1)

## DOD and Go / No-Go

- **GO for `feature/normative-catalog/data`:** every task of section 2 is checked off;
  Egor's tests pass with at least 95% branch coverage of his changed code; the ingestion
  is idempotent, the role's refusals are tested, and the coefficient record of task 2.5
  is committed; Akim's review passes.
- **GO for `feature/normative-catalog/backend`:** every task of sections 3-7 is checked
  off; `check.sh` passes with at least 95% branch coverage; the two postgres modules
  pass; task 7.1 passes on Egor's ingested data; `openspec validate --all --strict`
  passes; no UI changes, so `UI/UX: N/A`.
- **NO-GO** for either feature: a failing test, coverage under 95%, a contract test that
  differs from `design.md` decision 2, a norm value in code or test data, a response or
  log line that holds a client query, the database URL or a password, or an open blocker
  or major review finding.
- The change is done when both features are merged, task 8.1 is recorded, and the
  change is archived (task 8.2).
