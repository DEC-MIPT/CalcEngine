# interim-normatives Specification

## Purpose

Defines the temporary normative parameter source, its verification and provenance
controls, source selection and sunset, and its scoped exception to the catalog-only rule.

## Requirements

### Requirement: Interim normative data files
The system SHALL read interim norm-given parameters only from YAML files under one data root
in the backend zone, outside `params/`: one directory per norm document holding a
`manifest.yaml` and one file per calculation type, named as the type in the registry. A type
file SHALL hold the five required lists below, whose records have these fields, as the rows of the normative
catalog contract do:
- `formulas`: `parameter`, `result_symbol`, `latex`, `tree` (the expression tree), `units`;
- `table_values`: `parameter`, `symbol`, `latex`, `value`, `unit`, and optionally
  `heading_symbol`, `heading_value`, `heading_unit` (the selecting input's heading);
- `thresholds`: `parameter`, `latex`, `value`, `unit`;
- `checks`: `parameter`;
- `method_bounds`: `quantity`, `kind`, `value`, `unit`, `inclusive`.

The optional lists specified by "Stored applicability and diagram conditions" extend this
format without changing the five required lists.

Every record SHALL also have `norm_refs` (one or more complete `NormRef` objects), `page` (the
page of the source text the value was read from) and `verification`. The manifest SHALL name
the document, its edition as printed on the source text, the sunset date and event, and the
verifiers. The files SHALL NOT hold norm text: `latex` SHALL be at most 500 Unicode code
points; identifiers (parameter, symbol and unit names, names inside a tree, `by`, `portion`)
at most 64; `comment` at most 300; the manifest's document, edition and sunset event at most
200; and no field SHALL be meant for a passage of the norm. No norm value
is fixed by this requirement; values are data set by the engineer and checked by the
verifier.

#### Scenario: Record without a reference rejected
- **WHEN** the interim source is selected and a type file holds a record with no `norm_refs`,
  or with an empty list
- **THEN** the application does not start, and the error names the file and the path of the
  record

#### Scenario: Unknown field rejected
- **WHEN** a record, the manifest or a type file has a field the schema does not define
- **THEN** the application does not start, and the error names the file and the path of the
  field

#### Scenario: Over-long label rejected
- **WHEN** a record's `latex` or another label is longer than its limit
- **THEN** the application does not start, and the error names the file and the field, and
  does not repeat the text

#### Scenario: File of an unregistered type
- **WHEN** a valid type file names a calculation type that is not registered
- **THEN** the file is validated, its type gets no source, and one log line names the file

### Requirement: Stored applicability and diagram conditions
The system SHALL accept optional `applicability_conditions` and `diagram_cases` lists in an
interim type file, defaulting each to empty. Every record SHALL have the same `norm_refs`,
positive `page` and `verification` contract as records in the five required lists. New
records and all nested objects SHALL reject unknown fields. The existing identifier and
LaTeX limits SHALL apply to their labels and expressions, including unit keys and values.

An applicability record SHALL have `parameter`, `quantity`, `applies_to`, `latex`, `unit`,
`relation` (`lt`, `le`, `eq`, `ge` or `gt`) and `value_fraction`. `value_fraction` SHALL hold
strict integer `numerator` and positive strict integer `denominator`; booleans and values
requiring numeric coercion SHALL be rejected. The stored fraction SHALL remain exact and
SHALL NOT be converted into a floating-point threshold or a global method bound.

A diagram record SHALL have `parameter`, `units`, a non-empty `cases` list and a non-empty
`caption_forms_as_printed` list. Every case SHALL have `figure_case`, `diagram`,
`condition_latex` and optionally `edge_ordinate_latex`. Identifiers SHALL represent labels;
LaTeX fields SHALL represent printed expressions. Caption forms SHALL remain separate from
case expressions, preserving their differences without normalization or correction.

These records SHALL participate in record iteration, verifier validation, effective status,
strict startup warnings and record/document digests. Iteration SHALL append applicability
records and then diagram records after the existing five lists, preserving each list's
order. An unregistered type file SHALL remain validated and skipped as specified by
"Interim normative data files". A registered type containing any such record SHALL refuse
parameter resolution with `ParameterSourceUnavailableError` in both `strict` and `draft`,
regardless of verification status; the API SHALL retain `503 parameter_source_unavailable`.
Logs SHALL name the type and parameter without data values. The system SHALL NOT silently
drop or execute these records through the catalog assembly.

#### Scenario: Legacy file without optional lists
- **WHEN** a valid type file contains only the five required lists
- **THEN** both optional lists are empty and the file retains its existing loading and
  parameter resolution behavior

#### Scenario: Exact fraction preserved
- **WHEN** an applicability record has valid integer numerator and positive integer denominator
- **THEN** loading and serialization retain those integers, relation and applies_to label
  without floating-point conversion

#### Scenario: Invalid fraction rejected
- **WHEN** a fraction has a non-positive denominator, boolean, non-integer or unknown field,
  or the applicability relation is not one of the supported labels
- **THEN** validation rejects the file and names the offending path without its data value

#### Scenario: Diagram expressions remain distinct
- **WHEN** a valid diagram record has different printed expressions in cases and caption forms
- **THEN** both forms and their order survive loading and serialization unchanged

#### Scenario: Invalid nested diagram rejected
- **WHEN** a diagram has an empty cases or caption list, a missing case field, an unknown
  nested field or a label or expression exceeding its applicable limit
- **THEN** validation rejects the file and names the offending path without its data value

#### Scenario: New records use the verification gate
- **WHEN** a new record lacks required verification fields, names an unlisted verifier, or
  has a human-verified digest that differs from its current content
- **THEN** the same rejection or effective-pending rules as "Verification record" apply
  and strict startup warnings include effective-pending records

#### Scenario: Unregistered extended file is stored without execution
- **WHEN** an extended type file is valid but its calculation type is not registered
- **THEN** the loader validates all records, logs the file as unregistered and exposes no source
  for that type

#### Scenario: Registered extended file cannot bypass stored conditions
- **WHEN** a registered type containing any new record resolves parameters in either profile,
  including when all records are human-verified or rejected
- **THEN** resolution raises ParameterSourceUnavailableError, the API returns the existing
  503 error code, and no stored condition is dropped or executed

### Requirement: Verification record
Every interim record SHALL carry a verification record with `status` (`pending`,
`human-verified` or `rejected`), `by`, `at`, `portion`, `comment` and `value_digest`. A
record SHALL be `human-verified` only when `by` names a person listed in the manifest's
`verifiers` and `at`, `portion`, `value_digest` and the record's `page` are present. A record
SHALL be `rejected` only when `by` names a listed verifier and `at` and a `comment` with the
reason are present. The
`value_digest` SHALL be the SHA-256 of the record's canonical serialization without its
`verification`; a `human-verified` record whose current digest differs from its
`value_digest` SHALL be treated as `pending`. The status SHALL be set only by a listed
verifier, in a commit that cites the portion; an agent SHALL write new or changed records only
as `pending` and SHALL NOT edit a verification record.

#### Scenario: Verified record without its fields rejected
- **WHEN** a record is `human-verified` and lacks `by`, `at`, `portion`, `value_digest` or
  `page`, or `by` is not in the manifest's `verifiers`
- **THEN** the application does not start, and the error names the file, the record and the
  missing or unknown field

#### Scenario: Rejected record without its reason rejected
- **WHEN** a record is `rejected` and lacks `by`, `at` or `comment`, or `by` is not in the
  manifest's `verifiers`
- **THEN** the application does not start, and the error names the file, the record and the
  missing or unknown field

#### Scenario: Changed value needs a new check
- **WHEN** the value, unit, tree, heading or references of a `human-verified` record change
  and its `value_digest` is not renewed
- **THEN** the record counts as `pending`, and a startup log line names the file and the
  record

#### Scenario: Pending record allowed without a verifier
- **WHEN** a record is `pending` and has no `by`, `at` or `portion`
- **THEN** it passes validation

### Requirement: Interim source profiles
The interim source SHALL run in one of two profiles, chosen by setting: `strict`, the
default, uses only `human-verified` records; `draft`, chosen only explicitly, also uses
`pending` records. A `rejected` record SHALL never be used. In both profiles every `NormRef`
SHALL reach the result unchanged; the source SHALL NOT raise a reference's status or
provenance. A result computed in the `draft` profile SHALL carry the profile in its source
label.

#### Scenario: Strict refuses an unchecked value on request
- **WHEN** the profile is `strict` and a parameter that a calculation type needs has only
  `pending` or `rejected` records
- **THEN** `POST /calculations` for that type answers `503 parameter_source_unavailable`, the
  engine does not run, nothing is stored, and one log line names the type and the parameter;
  other types with checked data still compute

#### Scenario: Strict lists unchecked values at startup
- **WHEN** the application starts with the interim source in the `strict` profile and some
  records are not `human-verified`
- **THEN** a warning names each such file and record, and the application starts

#### Scenario: Draft uses pending values and marks the result
- **WHEN** the profile is `draft` and a needed parameter has a `pending` record
- **THEN** the calculation runs, the result's source label has profile `draft`, and each step
  built from interim data keeps its `NormRef` status as stored

#### Scenario: References not raised
- **WHEN** a result is computed from `human-verified` interim records whose references are
  `unverified` and `machine-extracted`
- **THEN** every such reference in the result envelope (`norm_refs` and the references of each
  step) is still `unverified` and `machine-extracted`

### Requirement: Interim parameter source contract
`InterimParameterSource` SHALL implement `ParameterSource` and SHALL return the same parameter
objects (`Formula`, `TableValue`, `Threshold` and the reference lists of the checks), the same
method range and the same errors as `CatalogParameterSource` for the same data. One
parametrized contract test battery SHALL run against both sources, with the same data loaded
into each. This equivalence applies to the five executable lists; storage-only extended
records use the refusal specified by "Stored applicability and diagram conditions".

#### Scenario: Same data, same parameters
- **WHEN** the battery loads one data set into the catalog fixture and into interim files and
  resolves a type for the same inputs
- **THEN** both sources return equal `parameters` and equal `method_range`

#### Scenario: Table row chosen by an input
- **WHEN** a table parameter is selected by an input and the input matches one heading row
- **THEN** both sources return that row with its selector

#### Scenario: Input off every table row
- **WHEN** an input inside the method range matches no heading row
- **THEN** both sources raise the same input error, which does not repeat the input's value

#### Scenario: Input outside the method range
- **WHEN** an input lies outside a method bound
- **THEN** both sources return a result that leads the engine to refuse with that bound

#### Scenario: Broken binding
- **WHEN** a parameter of the type's model has no record, or two records
- **THEN** both sources raise `ParameterSourceUnavailableError`

### Requirement: Interim data digest
The system SHALL compute, at startup, one SHA-256 per document directory over the canonical
serialization of the validated manifest and type files, taken in the order of their paths
relative to the document directory, with sorted keys, fixed separators and UTF-8. The digest
SHALL cover every value, reference, page and verification record and SHALL NOT depend on YAML
comments, key order or whitespace. Every result computed from interim data SHALL carry this
digest in its source label. Empty optional applicability and diagram lists SHALL be omitted
from canonical type-file data; populated optional lists SHALL be included. Existing record
serialization SHALL remain unchanged.

#### Scenario: Legacy digest preserved
- **WHEN** a corpus has only the original five lists, with optional lists absent or explicitly empty
- **THEN** its document and existing record digests equal those from the original format

#### Scenario: Extended digest covers the stored content
- **WHEN** a new applicability or diagram record changes outside its verification object,
  including a nested expression, reference or page
- **THEN** the affected record digest and document digest change

#### Scenario: Verification-only change preserves the record digest
- **WHEN** only a verification field of a new applicability or diagram record changes
- **THEN** the document digest changes and the record digest remains unchanged because
  record digests exclude the verification object

#### Scenario: Digest is deterministic
- **WHEN** the same data are loaded twice, or after a change of comments, key order or
  indentation only
- **THEN** the digest is the same

#### Scenario: Digest follows the data
- **WHEN** any value, reference, page or verification field changes
- **THEN** the digest changes

#### Scenario: Digest in the result
- **WHEN** a calculation runs on interim data
- **THEN** the result envelope's source label holds kind `interim`, the digest and the
  profile

### Requirement: Parameter source selection
The system SHALL choose the source of norm-given parameters for all calculation types at
once by setting: `DEC_PARAMETER_SOURCE` is `catalog` (the default) or `interim`; `DEC_INTERIM_PROFILE` is
`strict` (the default) or `draft`; `DEC_INTERIM_ROOT` optionally moves the data root. Every
such setting SHALL be listed in `.env.example`. The normative search and document endpoints
SHALL keep reading the catalog whatever the setting.

#### Scenario: Default stays the catalog
- **WHEN** no source setting is given
- **THEN** every calculation type reads the catalog, and results carry kind `catalog`

#### Scenario: Interim chosen
- **WHEN** `DEC_PARAMETER_SOURCE=interim`
- **THEN** every registered type that has an interim data file reads it, and a type without a
  file answers `503 parameter_source_unavailable`

#### Scenario: Catalog mode and a type with interim data only
- **WHEN** `DEC_PARAMETER_SOURCE=catalog` and a registered type has an interim data file but
  no usable catalog data
- **THEN** `POST /calculations` for that type answers `503 parameter_source_unavailable`, and
  the interim file is not read

#### Scenario: Unknown setting value
- **WHEN** `DEC_PARAMETER_SOURCE` or `DEC_INTERIM_PROFILE` has another value
- **THEN** the application does not start, and the error names the variable

### Requirement: Interim source sunset
Each manifest SHALL record a sunset `date` and `event`, set by the author. When the interim
source is selected and the date has passed, the application SHALL start and log a warning
naming the document, the date and the event, and a backend test SHALL fail until the date is
extended by a commit or the data are removed. The event SHALL be closed by the change that
switches the service back to the catalog, which deletes the data directory.

#### Scenario: Date passed
- **WHEN** the interim source is selected and today is after the manifest's sunset date
- **THEN** startup logs a warning with the document, the date and the event, and the backend
  test of the sunset fails

#### Scenario: Date not passed
- **WHEN** today is on or before the sunset date
- **THEN** no warning is logged and the test passes

### Requirement: Scoped exception to the normative-database rule
The rule that norm-given values come only from the normative catalog — stated in
`backend-architecture` "No hardcoding" and "Engineer-set parameters stored in YAML",
`calculation-api` "Calculation parameter source" and `normatives-catalog` "Catalog
parameter source" — SHALL have one temporary exception: norm-given formulas, table values, thresholds,
checks and method bounds MAY be read from YAML only while `DEC_PARAMETER_SOURCE=interim`,
only from the interim data root, only from records that carry `norm_refs`, `page` and a
verification record, and only until the sunset event. Engineer-set files under `params/`
SHALL keep rejecting norm-given values, and no norm-given value SHALL be written as a literal
in code.

#### Scenario: Catalog setting ignores interim files
- **WHEN** `DEC_PARAMETER_SOURCE=catalog` and interim files exist
- **THEN** no calculation reads them

#### Scenario: Interim mode and a type without a catalog source
- **WHEN** `DEC_PARAMETER_SOURCE=interim` and a registered type has interim data but no
  catalog bindings
- **THEN** the type computes from its interim data, and its result carries kind `interim`

#### Scenario: Norm value in params still rejected
- **WHEN** a file under `params/` holds a formula or a coefficient
- **THEN** its validation fails as before, whatever the source setting

### Requirement: Non-functional — interim source
The interim source SHALL read YAML with a safe loader, SHALL read only files directly under a
document directory of the resolved data root and follow no link outside it, SHALL load and
validate all files once at startup and resolve parameters in memory, and SHALL NOT write a
data value to the log. Branch coverage of the changed backend and frontend code SHALL be at
least 95%.

#### Scenario: File outside the root ignored
- **WHEN** a document directory holds a link to a file outside the data root, or a file that
  is not a manifest or a type file
- **THEN** it is not read, and one log line names it

#### Scenario: No data value in the log
- **WHEN** any interim validation or refusal is logged
- **THEN** the log line names files, records, parameters and types, and no value
