## REMOVED Requirements

### Requirement: Manual normative maintenance for MVP
**Reason**: Contradicts ML-in-MVP: normative data is parsed by the NLP/RAG pipeline
with a human-in-the-loop verification gate, not maintained manually as the only path.
**Migration**: Replaced by the pipeline (`normatives-collector`, `normatives-parser`)
and the provenance gate in `norm-source-traceability`.

## MODIFIED Requirements

### Requirement: Binding a normative to a calculation type
The system SHALL bind each calculation type to the relevant normative document and
automatically load the applicable formulas and coefficients.

#### Scenario: Select a calculation type
- **WHEN** a user selects an in-scope calculation type of the first domain
- **THEN** the system loads the bound normative document, its current revision, and the
  required formulas and coefficients

## ADDED Requirements

### Requirement: Norm reference status
The system SHALL mark every norm reference held in a spec, a catalog entry, or a
calculation step as either verified against the primary source text or
`status: unverified`. A specification example SHALL use a synthetic placeholder
(document `<NORM-DOC-PLACEHOLDER>`, edition `unverified`, clause `<CLAUSE-PLACEHOLDER>`)
and SHALL NOT use a real clause number that nobody has checked. The reference field
format is defined by the planned change `norm-source-traceability` (`NormRef
{document, edition, clause, status, provenance}`).

#### Scenario: Reference not checked
- **WHEN** a norm reference has not been checked against the primary source text
- **THEN** it carries `status: unverified` and no clause number is invented

#### Scenario: Example reference in a spec
- **WHEN** a spec gives an example norm reference
- **THEN** the example uses the synthetic placeholder, not a real document number or
  clause

#### Scenario: Reference checked
- **WHEN** Egor's normative pipeline confirms a reference against the source text
- **THEN** the reference records the checked edition and clause and is no longer marked
  `unverified`
