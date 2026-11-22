## MODIFIED Requirements

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
"Interim normative data files". A registered type without the reviewed loads binding containing such records
SHALL refuse parameter resolution with `ParameterSourceUnavailableError` in both `strict` and `draft`,
regardless of verification status; the API SHALL retain `503 parameter_source_unavailable`.
Logs SHALL name the type and parameter without data values. The system SHALL NOT silently
drop or execute these records through generic catalog assembly. Only the explicit
foundations_shallow_loads binding MAY consume the allowlisted prepared records,
under the same verification/profile gates and with exact printed forms retained.
It follows foundations-pressure-from-loads "Full contact before bearing checks":
Akim's adopted signed-corner rule and the cited SP 22.13330.2016 edition 2016
with amendments 1-5, clauses 5.6.27-5.6.28. Axial minima alone do not establish
biaxial contact.

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
- **WHEN** a registered type without the reviewed loads binding contains a new record
  and resolves parameters in either profile,
  including when all records are human-verified or rejected
- **THEN** resolution raises ParameterSourceUnavailableError, the API returns the existing
  503 error code, and no stored condition is dropped or executed

#### Scenario: Reviewed loads binding
- **WHEN** the allowlisted new type resolves its prepared extended records
- **THEN** strict verification and exact fraction/diagram controls remain mandatory, and missing or unsupported required records fail closed

### Requirement: Interim parameter source contract
`InterimParameterSource` SHALL implement `ParameterSource` and SHALL return the same parameter
objects (`Formula`, `TableValue`, `Threshold` and the reference lists of the checks), the same
method range and the same errors as `CatalogParameterSource` for the same data. One
parametrized contract test battery SHALL run against both sources, with the same data loaded
into each. This equivalence applies to the five executable lists; extended records without the reviewed loads binding use the refusal specified
by "Stored applicability and diagram conditions". The reviewed loads binding is
an explicit interim-only adapter; generic catalog assembly stays unchanged.

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

#### Scenario: No fallback in catalog mode
- **WHEN** catalog mode has no usable complete binding for the loads type
- **THEN** the existing parameter_source_unavailable error is returned rather than reading interim files

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

Only foundations_shallow_loads SHALL use the fixed alias to the prepared file
foundations_pressure_from_loads.yaml. This allowlist does not permit arbitrary
client paths, inference of aliases, or changes to the pilot mapping or signed data.

#### Scenario: Fixed loads alias
- **WHEN** the public loads type resolves pressure records
- **THEN** only the fixed reviewed file is used, without renaming or modifying signed records

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

The loads-only supplementary directory sp-22-13330-2016-loads-scope SHALL hold its
own manifest and prepared normative d_b bound from signed LOADS-DB-1 evidence. The
original sp-22-13330-2016 directory SHALL stay byte-identical. For this type only,
data_sha256 SHALL be SHA-256 of UTF-8 canonical JSON (sorted keys, compact separators,
ensure_ascii=False, no trailing newline) with this structure:
{"format":"foundations-shallow-loads-source-v1","documents":[
{"name":"sp-22-13330-2016","data_sha256":"<original-document-digest>"},
{"name":"sp-22-13330-2016-loads-scope","data_sha256":"<supplement-digest>"}]}.
Documents SHALL be sorted by name from this fixed allowlist. Existing per-document
and signed-record digest rules stay unchanged. Every constituent must be present
and usable under the same selected profile or resolution fails closed. The existing
parameter_source object carries this aggregate without new envelope fields.

#### Scenario: Pilot identity remains stable
- **WHEN** a loads scope supplement is installed
- **THEN** the loads aggregate includes both constituents while pilot data bytes and document digest remain unchanged
