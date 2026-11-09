# Spec Delta

## MODIFIED Requirements

### Requirement: Catalog parameter source
The system SHALL resolve the norm-given parameters of every registered calculation type
from the catalog contract when the catalog source is selected, as required by
`calculation-api` "Calculation parameter source". Explicit global selection of the
interim source follows `interim-normatives` "Scoped exception to the normative-database
rule" instead of this catalog read path. For one catalog-backed request it SHALL read,
for the requested type,
every parameter the type's calculator declares and the bounds of the method's range, and
SHALL give them to the engine without changing any value, apart from the selection of
table rows and the unit conversion of the range bounds. The engineer-set values SHALL
still come from the type's `.yaml` file. If the catalog gives a parameter the calculator
does not declare, lacks one it declares, or gives data that breaks this capability's
contract, the type SHALL be answered as having no usable parameter source.

#### Scenario: Parameters from the catalog
- **WHEN** the catalog source is selected and a client posts a valid calculation request
  for a bound type whose catalog
  data meet the contract, with every selecting input on a row heading
- **THEN** the response is `201`, the engine received every formula, table value,
  threshold, check reference and method bound from the catalog, and each step of the
  stored result carries the references the catalog gave for it

#### Scenario: Catalog data that breaks the contract
- **WHEN** the catalog source is selected and its data for the requested type miss a
  declared parameter, add an
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
- **WHEN** the catalog source is selected and `dec_normatives` holds the pipeline's
  ingested data for the pilot type
  `foundations_shallow_r`, and a client posts a valid request for it whose `phi_II` equals
  a row heading of the bound table
- **THEN** the response is `201`, every formula, table and threshold step of the result
  carries a reference from the catalog, and the stored result records the documents and
  editions the catalog named
