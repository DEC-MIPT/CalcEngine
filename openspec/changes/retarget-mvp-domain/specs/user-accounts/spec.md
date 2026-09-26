## MODIFIED Requirements

### Requirement: Subscription tiers
The system SHALL support B2B and B2C subscription tiers and is the only spec that states
their limits: B2B (30 000 ₽/mo for 10 seats) and B2C (3 000 ₽/mo, up to 100 calculations
per month). The B2C calculation limit is unverified until the PM approves it. Other
specs SHALL reference this requirement instead of restating a limit.

#### Scenario: Tier limits enforced
- **WHEN** a user on a B2C plan reaches their monthly calculation limit
- **THEN** further calculations are blocked until the limit resets or the plan is
  upgraded

#### Scenario: Limit stated once
- **WHEN** another spec needs a tier limit
- **THEN** it references this requirement and states no number of its own

### Requirement: Single authorization
The system SHALL use one authorization model across all platform components and is the
owner of that rule; `web-platform` references it.

#### Scenario: One identity everywhere
- **WHEN** a user accesses the normative base, calculation flow, and report generator
- **THEN** the same identity and plan are applied to all components
