# User Accounts

## Purpose
Defines user accounts, authentication, and subscription handling for DEC: a single
sign-on across all platform components, B2B/B2C subscription tiers, and the 14-day
free trial.

## Requirements

### Requirement: User registration and authentication
The system SHALL support user registration and authentication with a single set of
credentials across the whole platform.

#### Scenario: Sign in once
- **WHEN** a user signs in with valid credentials
- **THEN** the same session identity is accepted across the normative base,
  calculation engine, and report generator components

### Requirement: Subscription tiers
The system SHALL support B2B and B2C subscription tiers with the limits defined by
the product vision: B2B (30 000 ₽/mo for 10 seats), B2C (3 000 ₽/mo, up to 100
calculations per month).

#### Scenario: Tier limits enforced
- **WHEN** a user on a B2C plan reaches their monthly calculation limit
- **THEN** further calculations are blocked until the limit resets or the plan is
  upgraded

### Requirement: Free trial
The system SHALL provide a 14-day free trial granting full functionality for a
limited time.

#### Scenario: Trial expiry
- **WHEN** a trial period of 14 days ends
- **THEN** full functionality is restricted until a subscription is purchased

### Requirement: Single authorization
The system SHALL use one authorization model across all platform components, as
required by the web platform, without separate logins per component.

#### Scenario: One identity everywhere
- **WHEN** a user accesses the normative base, calculation flow, and report generator
- **THEN** the same identity and plan are applied to all components

### Requirement: Billing deferred for MVP
The system SHALL NOT require a payment integration for the MVP; subscription state is
managed administratively, and payment/billing integration is a future goal.

#### Scenario: MVP without payments
- **WHEN** the MVP is delivered
- **THEN** subscription tiers and the trial are tracked as account state without a
  live payment provider
