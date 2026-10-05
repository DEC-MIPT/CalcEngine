## REMOVED Requirements

### Requirement: MVP scope
**Reason**: It fixes a single placeholder-domain reference calculation as the MVP, and a
MODIFIED block cannot drop its scenario.
**Migration**: Replaced by "MVP domains and their order" below.

## ADDED Requirements

### Requirement: MVP domains and their order
The system SHALL target two MVP domains in a fixed order: shallow foundations first,
internal water supply second. The scope of the first domain is owned by the
`foundations-shallow` capability. The scope of the second domain (internal water supply)
is fixed by a later change at the `water-supply-internal` milestone, not inside the MVP.
Calculation types are swappable and must not hard-code the selection of the normative
method.

#### Scenario: MVP delivered
- **WHEN** the MVP is delivered
- **THEN** every in-scope calculation type of the first domain runs end-to-end, and the
  second domain follows at a named milestone, not inside the MVP

#### Scenario: Both domains and their order are stated
- **WHEN** a reader looks for the MVP scope
- **THEN** it names both domains, states that shallow foundations come first and
  internal water supply second, and points to `foundations-shallow` for the first
  domain's scope

### Requirement: Non-goals before the defense
The system SHALL treat the following as non-goals before the defense: billing or
payment integration, generative-LLM structured extraction from norms, PDF report
output, and a multi-tenant audit trail. ML-in-MVP is in scope: the normative pipeline
(collector, regex baseline parser, embeddings retrieval on CPU) parses norms into the
database; no ML runs in the calculation path.

#### Scenario: Proposal touches a non-goal
- **WHEN** a change proposal adds behavior that falls under a non-goal
- **THEN** this requirement is amended first, with PM approval, before the proposal is
  accepted

#### Scenario: Request for a non-goal feature
- **WHEN** a feature request matches a listed non-goal
- **THEN** it is recorded as deferred and no requirement for it is added to another spec

## MODIFIED Requirements

### Requirement: Subscription monetization
The system SHALL support B2B and B2C subscription tiers and a 14-day free trial. The
tier limits, the trial rules, and the enforcement are owned by the `user-accounts`
capability and are not restated here.

#### Scenario: Tiered access
- **WHEN** a customer subscribes to a B2B or B2C plan
- **THEN** the plan limits and features are those defined in `user-accounts`, and this
  spec states no limit of its own

### Requirement: No machine learning in the calculation path
The system SHALL NOT use machine learning for calculations; calculation algorithms
must be deterministic and verified. NLP/RAG auto-parsing of norms (collector, regex
baseline parser, embeddings retrieval on CPU) is part of the MVP and runs outside the
calculation path.

#### Scenario: Deterministic calculation
- **WHEN** the same inputs are provided twice
- **THEN** the calculation produces identical results, and no ML model influences the
  arithmetic or the normative references
