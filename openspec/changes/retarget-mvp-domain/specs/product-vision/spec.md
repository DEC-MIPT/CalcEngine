## REMOVED Requirements

### Requirement: MVP scope
**Reason**: It fixes a single placeholder-domain reference calculation as the MVP, and a
MODIFIED block cannot drop its scenario.
**Migration**: Replaced by "MVP domains and their order" below.

## ADDED Requirements

### Requirement: MVP domains and their order
The system SHALL target two MVP domains in a fixed order: shallow foundations first,
internal water supply second. The scope of the first domain is owned by the
`foundations-shallow` capability. The scope of the second domain is fixed by a later
change that names its milestone. Calculation types are swappable and must not hard-code
the selection of the normative method. DRAFT — needs Egor review (domain order and
milestone name).

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
payment integration, NLP/RAG parsing of norms inside the product, PDF report output,
and a multi-tenant audit trail. DRAFT — the PM approves this list; it is the example
list from the verified roadmap, not the PM's meeting list.

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
