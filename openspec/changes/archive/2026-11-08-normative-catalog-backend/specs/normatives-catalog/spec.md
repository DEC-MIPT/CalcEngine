## ADDED Requirements

### Requirement: Catalog read contract
The system SHALL expose the content of `dec_normatives` to the backend only through a
read contract owned by the normative pipeline: a database schema `catalog_read` holding
a fixed set of views and one search function, and a role `dec_normatives_reader` whose
only privileges are `USAGE` on that schema, `SELECT` on its views, and `EXECUTE` on its
search function. The pipeline SHALL create the schema, the views, the function and the
role idempotently, as part of ingestion, and SHALL version them with it. The backend
SHALL connect to `dec_normatives` with that role, SHALL read only objects of
`catalog_read`, and SHALL NOT import the pipeline's code. The pipeline SHALL NOT import
the backend's code. Until the pipeline's database is split, `dec_normatives` is the
pipeline's current database (`dec`), and the schema and the role live there under the
same names. The contract SHALL provide:

- the documents (designation, title, edition, year, source address) and their clauses
  (number, title, page) in document order;
- a ranked search over documents, clauses and formulas;
- per calculation type and per parameter of that type: its formulas, its table values,
  its thresholds, the norm references of its checks, and the bounds of its method's
  range of application, as defined by the requirements below;
- for every formula, table value, threshold, check and bound, a non-empty list of norm
  references, each with the five fields `document`, `edition`, `clause`, `status` and
  `provenance` of `normatives-formula-contract` "Traceability reference".

The exact columns of each view are fixed in this change's `design.md`, decision 2. A
change to a view's columns SHALL be made through an OpenSpec change that both owners
acknowledge.

#### Scenario: The reader role cannot write
- **WHEN** a session connected as `dec_normatives_reader` tries to insert, update or
  delete a row in any table or view of `dec_normatives`, or to create an object in any
  schema
- **THEN** the database refuses the statement with a privilege error

#### Scenario: The reader role sees only the contract
- **WHEN** a session connected as `dec_normatives_reader` selects from a pipeline table
  outside `catalog_read`
- **THEN** the database refuses the statement with a privilege error

#### Scenario: Ingestion run twice
- **WHEN** the ingestion runs a second time on a database where the contract already
  exists
- **THEN** it finishes without error, and the schema, views, function and role exist
  once each with the same columns

#### Scenario: No import across zones
- **WHEN** the backend's and the pipeline's source trees are scanned for imports
- **THEN** no backend module imports the pipeline's package, and no pipeline module
  imports the backend's package

### Requirement: Expression tree form in the catalog
The system SHALL store each formula a calculation type uses as an expression tree in one
JSON form shared by the catalog and the calculation engine, with the unit of every
symbol. A node SHALL be one of:

- `{"kind": "number", "value": <finite number>}`;
- `{"kind": "symbol", "name": <symbol id>}`, where the symbol id follows
  `normatives-formula-contract` "Symbol normalization";
- `{"kind": "add" | "sub" | "mul" | "div" | "pow", "left": <node>, "right": <node>}`;
- `{"kind": "neg", "operand": <node>}`;
- `{"kind": "call", "function": <name>, "args": [<node>, ...]}`, where the name is one of
  `sqrt`, `exp`, `ln`, `log10`, `sin`, `cos`, `tan`, `abs`, `min`, `max`, and `args` is
  not empty.

A tree SHALL have a depth of at most 64 and at most 4096 nodes. The function list and
these two limits are the engine's (`calculation-core-contract` design decision 11), not
norm values. Each formula SHALL name its result symbol, and SHALL give a unit for the
result symbol and for every symbol of its tree, taken from the backend's list of accepted
unit symbols. A symbol or result symbol that names an input or an output of the
calculation type SHALL carry that quantity's base unit, as the type's contract declares
it: the engine hands a formula its inputs in their base units and converts nothing inside
a formula. The pipeline builds the tree at ingestion; the backend SHALL NOT parse a
formula's text or LaTeX to obtain it.

#### Scenario: A formula in the shared form
- **WHEN** the backend reads a formula whose tree uses only the node kinds above, within
  the limits, with a unit for every symbol and for the result symbol
- **THEN** the engine evaluates that tree for the calculation without any change to it

#### Scenario: A formula outside the form
- **WHEN** a formula a calculation type needs has a node of another kind, a function
  outside the list, a tree over the limits, a symbol without a unit, a unit outside
  the accepted list, or a symbol or result symbol that names an input or an output of the
  type in a unit other than that quantity's base unit
- **THEN** the calculation type is treated as having no usable parameter source
  ("Catalog parameter source", scenario "Catalog data that breaks the contract"), and the
  engine does not run

### Requirement: Calculation type binding by name
The system SHALL keep the binding of each calculation type to its norms in
`dec_normatives`, keyed by the calculation type's registered name (for the pilot,
`foundations_shallow_r`), and the pipeline SHALL fill it from a registry it owns. For
each parameter of the type, the binding SHALL name where the value comes from: a formula
number, a table cell or a table with its heading, a threshold, a check's references, or a
bound of the method's range, each in a named document. The binding SHALL NOT hold a
value, and the backend SHALL NOT hold a binding of its own. This requirement narrows
"Binding a normative to a calculation type" for the backend read path.

#### Scenario: A bound calculation type
- **WHEN** the backend asks the contract for the parameters of a calculation type that
  the binding names
- **THEN** it receives one entry for each parameter the binding names for that type,
  and nothing for any other type

#### Scenario: A calculation type with no binding
- **WHEN** a client posts a valid calculation request for a registered type that the
  binding does not name
- **THEN** the response is `503` with the error body, code
  `parameter_source_unavailable`, naming the type; the engine does not run, and nothing is
  stored

### Requirement: Table value selection by heading
The system SHALL select a table value that depends on an input by the row heading of its
table, with exactly one heading per parameter. The contract SHALL give, for each row of
such a table, the heading's symbol (an input of the calculation type), the heading's
value, and the heading's unit; every row of one parameter SHALL have a heading, or none
SHALL. The backend SHALL know, for each calculation type, which table parameters its
method selects by which input; this is the method's structure, not a norm value. A
parameter that the method selects by an input SHALL come with headings of that input,
and a parameter that the method selects by no input SHALL come as exactly one row with
no heading symbol, heading value or heading unit. The backend SHALL convert the heading values and the input to the input's base
unit at the boundary and SHALL select the row whose converted heading value equals the
converted input exactly. Exact
matching is an API rule of the backend, not a norm rule. The backend SHALL NOT
interpolate, round, or take the nearest row; a rule for a value between rows
SHALL come only from the norm's own text, recorded with its document, edition and clause
by a later change. Each resolved table value SHALL carry the heading value that selected
it ("Table value selectors" in `calculation-engine`). A table value that depends on no
input SHALL carry no heading value.

An input that matches no row SHALL be rejected only if it lies inside the method's range
of application; this extends the meaning of `invalid_input` in `calculation-api` "Error
responses" to an input that the catalog's table does not cover. An input outside that
range SHALL be refused by the range, as `calculation-api` "Calculation request
validation over HTTP", scenario "Input outside the method's range is not a validation
error", requires, whether or not it matches a row.

#### Scenario: An input equal to a row heading
- **WHEN** a client posts a calculation whose selecting input, converted to its base
  unit, equals the heading of one row converted to the same unit (in particular, an
  input given in the heading's unit with the heading's value)
- **THEN** the table step uses that row's value, and the step lists the heading symbol
  with the selecting value as its substitution

#### Scenario: An input between two rows
- **WHEN** a client posts a calculation whose selecting input is inside the method's
  range and matches no row heading
- **THEN** the response is `422` with the error body, code `invalid_input`, one field
  error located at `["body", "inputs", <input name>]` with a fixed message that does not
  repeat the value; the engine does not run, and nothing is stored

#### Scenario: An input outside the range and off every row
- **WHEN** a client posts a calculation whose selecting input matches no row heading and
  violates a bound of the method's range
- **THEN** the response is `201` with a stored result whose verdict is `refused` and
  which names the violated bound, as for any input outside the method's range

#### Scenario: Rows that break the table rules
- **WHEN** the contract gives, for one parameter, two rows with equal heading values,
  rows with a heading mixed with rows without one, rows with different heading symbols,
  a heading symbol that names no input of the type, a heading unit outside the
  accepted list or of another dimension than that input, a parameter that the method
  selects by an input without a heading or with the heading of another input, a
  parameter that the method selects by no input with a heading, or a row with a heading
  value or heading unit but no heading symbol
- **THEN** the calculation type is treated as having no usable parameter source
  ("Catalog parameter source", scenario "Catalog data that breaks the contract")

### Requirement: Method range from the catalog
The system SHALL take the bounds of a calculation type's method range from the catalog
contract. Each bound SHALL name an input of the type as its quantity, and its unit SHALL
have that input's dimension. The backend SHALL convert each bound's value to the base
unit of that input at the boundary, before the engine compares it with the inputs.

#### Scenario: A bound in another unit of the same dimension
- **WHEN** the catalog gives a bound in a unit other than the input's base unit, of the
  same dimension
- **THEN** the engine receives the bound converted to the base unit, and an input on
  either side of it is accepted or refused as the converted bound says

#### Scenario: A bound that does not fit its input
- **WHEN** the catalog gives a bound whose quantity is not an input of the type, or
  whose unit has another dimension than that input
- **THEN** the calculation type is treated as having no usable parameter source
  ("Catalog parameter source", scenario "Catalog data that breaks the contract")

### Requirement: Status of catalog references
The system SHALL keep the `status` and `provenance` of each norm reference exactly as the
pipeline wrote them in the contract, and SHALL apply the rules of `NormRef` from
`calculation-core-contract`: a reference with provenance `machine-extracted` has status
`unverified`, and a reference with status `verified` names a concrete edition and clause.
The backend SHALL NOT raise a reference's status. A step whose references are unverified
SHALL appear unverified in the result and in the report.

#### Scenario: A machine-extracted reference
- **WHEN** the contract gives a formula whose reference has provenance
  `machine-extracted` and status `unverified`
- **THEN** the formula's step in the result carries that reference with status
  `unverified`, and the report prints it with the unverified status

#### Scenario: A reference that breaks the rules
- **WHEN** the contract gives a reference with provenance `machine-extracted` and status
  `verified`, or a `verified` reference without a concrete edition or clause
- **THEN** the calculation type is treated as having no usable parameter source
  ("Catalog parameter source", scenario "Catalog data that breaks the contract")

### Requirement: Catalog parameter source
The system SHALL resolve the norm-given parameters of every registered calculation type
from the catalog contract, as the parameter source required by `calculation-api`
"Calculation parameter source". For one request it SHALL read, for the requested type,
every parameter the type's calculator declares and the bounds of the method's range, and
SHALL give them to the engine without changing any value, apart from the selection of
table rows and the unit conversion of the range bounds. The engineer-set values SHALL
still come from the type's `.yaml` file. If the catalog gives a parameter the calculator
does not declare, lacks one it declares, or gives data that breaks this capability's
contract, the type SHALL be answered as having no usable parameter source.

#### Scenario: Parameters from the catalog
- **WHEN** a client posts a valid calculation request for a bound type whose catalog
  data meet the contract, with every selecting input on a row heading
- **THEN** the response is `201`, the engine received every formula, table value,
  threshold, check reference and method bound from the catalog, and each step of the
  stored result carries the references the catalog gave for it

#### Scenario: Catalog data that breaks the contract
- **WHEN** the catalog data of the requested type miss a declared parameter, add an
  undeclared one, give one parameter in two kinds of entry or in the kind of entry that
  does not match the calculator's declaration, give a value that is not a finite number,
  give an empty reference list, give a row without a parameter name, give a method range
  with two bounds of one kind on one quantity or with no value between its bounds, or
  break another rule of this capability
- **THEN** the response is `503` with the error body, code
  `parameter_source_unavailable`, naming the type; the engine does not run, nothing is
  stored, and one log line names the type, and the parameter when the breach has one,
  without any value

#### Scenario: Pilot on catalog data
- **WHEN** `dec_normatives` holds the pipeline's ingested data for the pilot type
  `foundations_shallow_r`, and a client posts a valid request for it whose `phi_II` equals
  a row heading of the bound table
- **THEN** the response is `201`, every formula, table and threshold step of the result
  carries a reference from the catalog, and the stored result records the documents and
  editions the catalog named

### Requirement: Normative search endpoint
The system SHALL provide `GET /normatives/search` with a required query parameter `q`
and an optional `limit`. `q` SHALL be from 2 to 200 characters after trimming
surrounding white space; `limit` SHALL be an integer from 1 to 50, 20 by default. These
are API limits, not norm values. The response SHALL be `200` with a JSON object
`{"hits": [...]}`: at most `limit` documents, clauses and formulas that match `q`, ranked
by the catalog's search function, each with its kind (`document`, `clause` or
`formula`), the document's id, designation and edition, the clause or formula number
(none for a document), and the title. Hits SHALL be ordered by rank, highest first, then
by designation and number. Russian text SHALL be searched as it is written, without
transliteration. The query SHALL reach the database only as a bound parameter, and no
response or log line SHALL repeat it. This requirement implements "Full-text search" for
the backend.

#### Scenario: Search with matches
- **WHEN** a client calls `GET /normatives/search?q=<text>` and the catalog holds entries
  that match
- **THEN** the response is `200` with the matching hits in rank order, at most 20

#### Scenario: Search in Russian
- **WHEN** a client searches for a Russian word that occurs in a clause title of the
  catalog
- **THEN** the response is `200` and that clause is among the hits

#### Scenario: Search without matches
- **WHEN** a client searches for a text that matches nothing
- **THEN** the response is `200` with `{"hits": []}`

#### Scenario: Query outside its limits
- **WHEN** a client calls the endpoint without `q`, with `q` shorter than 2 or longer
  than 200 characters after trimming, or with `limit` outside 1 to 50
- **THEN** the response is `422` with the error body, code `validation_error`, and the
  field error names the parameter without repeating its value

#### Scenario: A query that looks like SQL
- **WHEN** a client searches for a text that contains SQL syntax or quote characters
- **THEN** the response is `200`, and the database receives exactly one statement for
  the search, with the text as a bound parameter and not inside the statement's text

### Requirement: Normative document endpoint
The system SHALL provide `GET /normatives/documents/{document_id}` that returns `200`
with the document's id, designation, title, edition, year, source address, and its
clauses (number, title, page) in document order. `document_id` SHALL be a positive
integer.

#### Scenario: An existing document
- **WHEN** a client requests a document that the catalog holds
- **THEN** the response is `200` with the document's fields and all its clauses in
  document order

#### Scenario: An unknown document
- **WHEN** a client requests a positive id that the catalog does not hold
- **THEN** the response is `404` with the error body, code `not_found`

#### Scenario: An invalid id
- **WHEN** a client requests a document with an id that is not a positive integer
- **THEN** the response is `422` with the error body, code `validation_error`, and the
  field error does not repeat the value

### Requirement: Catalog unavailability
The system SHALL start and serve its other endpoints when `DEC_NORMATIVES_DATABASE_URL`
is unset or `dec_normatives` cannot be reached. The search and document endpoints SHALL
then answer `503` with the error body and code `catalog_unavailable`, and a calculation
request for a type whose parameters come from the catalog SHALL answer `503` with code
`parameter_source_unavailable` naming the type, with nothing stored. The code
`catalog_unavailable` extends the error table of `calculation-api` "Error responses"
with one row and a fixed message, and changes none of its rows. A search or document row
of the contract that does not fit the response SHALL be answered the same way, with one
log line that names the endpoint and holds no value. No response and no log line SHALL
contain the database address or its credentials.

#### Scenario: Catalog not configured
- **WHEN** the application runs without `DEC_NORMATIVES_DATABASE_URL`
- **THEN** it starts, `GET /health` answers `200`, `GET /calculation-types` answers
  `200`, and `GET /normatives/search?q=<text>` answers `503` with code
  `catalog_unavailable`

#### Scenario: Catalog down during a calculation
- **WHEN** `dec_normatives` cannot be reached while a client posts a valid calculation
  request
- **THEN** the response is `503` with code `parameter_source_unavailable` naming the
  type, nothing is stored, and the response and log do not contain the database address

#### Scenario: A search or document row of the wrong shape
- **WHEN** the contract gives a search hit or a document or clause row that does not fit
  the response, such as a hit of an unknown kind or a document without an edition
- **THEN** the response is `503` with code `catalog_unavailable`, and one log line
  `code=catalog_data_invalid` names the endpoint without any value

#### Scenario: Catalog back
- **WHEN** `dec_normatives` becomes reachable again after a `503`
- **THEN** the next request is served without restarting the application

### Requirement: Non-functional — catalog read path
The system SHALL meet these limits on the catalog read path. A developer machine means
the backend and `dec-postgres` running locally on one computer with no other load,
holding the pipeline's ingested pilot document. The time limits come from
`normatives-catalog` "Non-functional — performance" and are not norm values.

- **Performance:** resolving the parameters of one calculation, one search, and one
  document request SHALL each take under 2 seconds on a developer machine.
- **Security:** the backend SHALL read `dec_normatives` only as `dec_normatives_reader`
  in read-only transactions, SHALL send every client value as a bound parameter, and
  SHALL keep statement parameters out of error messages and logs.
- **Coverage:** the backend code of this change SHALL have at least 95% branch coverage,
  with the read path tested against a PostgreSQL database that holds the contract's
  views.
- **Accessibility:** not applicable; this change adds no user interface.

#### Scenario: Parameter resolution time
- **WHEN** the pilot's parameters are resolved 20 times in a row on a developer machine
  against the ingested data
- **THEN** each resolution takes under 2 seconds

#### Scenario: Search and document time
- **WHEN** 20 searches and 20 document requests are made in a row on a developer machine
  against the ingested data
- **THEN** each one answers in under 2 seconds

#### Scenario: A write through the backend session
- **WHEN** a statement that writes is run through the backend's catalog session
- **THEN** the database refuses it, because the transaction is read-only and the role
  has no write privilege
