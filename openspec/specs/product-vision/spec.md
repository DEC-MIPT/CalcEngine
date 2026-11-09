# Product Vision

## Purpose
Defines the product vision, unique value proposition, target users, and MVP scope for
DEC (Design Engineer's Calculator), a cloud web service that automates engineering
calculations backed by a verified normative base and GOST-compliant reports.

## Requirements

### Requirement: Single-window engineering calculation service
The system SHALL provide one integrated environment that combines a normative base
(SP/GOST/SNiP), a calculation engine, and a report generator, so an engineer does not
switch between separate tools.

#### Scenario: Engineer completes a full calculation cycle
- **WHEN** an engineer selects a calculation type, enters inputs, runs the calculation,
  and exports the result
- **THEN** the whole cycle happens inside one web interface without manual data transfer
  between tools

### Requirement: Cloud accessibility
The system SHALL be delivered as a cloud web service accessible from a browser on any
device, without a desktop install.

#### Scenario: Access from any device
- **WHEN** a user opens the service URL in a browser
- **THEN** the service is available without installing desktop software

### Requirement: Subscription monetization
The system SHALL support B2B and B2C subscription tiers and the free trial defined by
`user-accounts` "Free trial". The tier limits, trial rules and enforcement are owned
by `user-accounts` and are not restated here.

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

### Requirement: MVP domains and their order
The system SHALL deliver the full shallow-foundation calculation by the second group
of limit states as the MVP outcome. Its scope is owned by `foundations-shallow`.
The R calculation is the delivered pilot stage and SHALL NOT be sufficient to declare
that MVP outcome complete. Internal water supply SHALL follow at the separate
post-MVP `water-supply-internal` milestone, with its scope defined by a later change.
Calculation types are swappable and must not hard-code the selection of the normative
method.

#### Scenario: MVP delivered
- **WHEN** the MVP is delivered
- **THEN** the full first-domain workflow meets the release gate in
  `foundations-shallow`, with completed end-to-end acceptance against its reviewed
  engineering contracts; the second domain follows at its named post-MVP milestone

#### Scenario: Both domains and their order are stated
- **WHEN** a reader looks for the MVP scope
- **THEN** it states the full second-limit-state foundation workflow as the required
  MVP outcome, names R as the pilot stage, places internal water supply after MVP,
  and points to `foundations-shallow` for first-domain scope

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
