# Web platform delta

## ADDED Requirements

### Requirement: Pilot workflow correlation

With closed-pilot collection enabled, the frontend SHALL attach a fresh measurement attempt UUID to each calculation and DOCX POST, following `calculation-api` "Optional pilot correlation header". With collection disabled it SHALL send neither telemetry events nor correlation headers.

#### Scenario: Repeat with pilot collection enabled

- **WHEN** a user issues two calculation requests from the same pilot scenario
- **THEN** the requests use different measurement attempt UUIDs and still execute according to the existing business contract
