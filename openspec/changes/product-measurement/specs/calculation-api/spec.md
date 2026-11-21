# Calculation API delta

## ADDED Requirements

### Requirement: Optional pilot correlation header

The system SHALL, when pilot measurement is enabled, accept an optional `X-DEC-Measurement-Attempt` on `POST /calculations` and `POST /calculations/{result_id}/report`. The header SHALL be documented in OpenAPI and SHALL be used only to correlate observations. Missing or invalid UUID values SHALL be ignored for measurement and SHALL NOT change business responses, authorization, or calculation identity.

#### Scenario: Invalid correlation identifier

- **WHEN** a valid calculation request carries a malformed correlation header
- **THEN** the business response is unchanged and no correlation value from that header is stored

#### Scenario: Configured origin preflight

- **WHEN** an origin configured for a measurement-enabled pilot requests preflight for the correlation header
- **THEN** CORS allows that header for the configured origin, without relaxing the existing denial for unconfigured origins
