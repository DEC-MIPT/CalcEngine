# Product measurement

## Purpose

Measure the DEC workflow and service availability in a closed pilot and provide reproducible aggregate evidence for evaluation of the product hypothesis.

## ADDED Requirements

### Requirement: Closed pilot collection

The system SHALL enable measurement only in an operator-configured closed pilot. It SHALL disable collection by default, reject invalid and over-limit event batches, and record no engineering input values, clipboard contents, report contents, personal identifiers or company identifiers. Measurements SHALL be exported only by the dedicated least-privilege `dec-measurement-operator` OS/database role through the local export command. The PostgreSQL operator login SHALL read measurements and insert export snapshots and audit records only. Ordinary runtime and writer identities SHALL NOT have raw measurement read privileges. No public measurement-read endpoint SHALL exist. A successful export SHALL append a payload-free audit record containing operator role, period, definition version and UTC time.

#### Scenario: Collection disabled

- **WHEN** DEC runs with default settings
- **THEN** no measurement is collected and the event endpoint does not accept submissions

#### Scenario: Pilot ingress and validation

- **WHEN** a request reaches the pilot event endpoint from outside the allowed ingress or includes fields outside the versioned event schema
- **THEN** no observation from that batch is stored

#### Scenario: Public read is unavailable

- **WHEN** a client requests measurement data through the application API
- **THEN** the application exposes no measurement-read route and raw observations are not returned

#### Scenario: Local export requires process access

- **WHEN** a caller invokes the export command using the runtime or telemetry writer database login
- **THEN** the command exits nonzero without emitting CSV, and those logins cannot query raw observations

#### Scenario: Export audit

- **WHEN** the dedicated measurement operator successfully exports a period
- **THEN** the export produces one audit record without raw observations or identifiers from the event payload

### Requirement: Workflow correlation and completion

The system SHALL correlate browser observations and server operations without treating client observations as authoritative server outcomes. It SHALL count duplicate event deliveries once and detect gaps within observed browser sequences. A workflow starts on first input and completes when the browser receives a DOCX and displays it as ready; neither delivery nor readiness establishes disk persistence or compliance with GOST.

#### Scenario: Duplicate and incomplete delivery

- **WHEN** the same event is accepted twice and the associated workflow sequence has a missing event before its terminal event
- **THEN** the event counts once, the sequence is flagged incomplete, and sequence-dependent metrics exclude it

#### Scenario: Report delivered without download

- **WHEN** a DOCX response reaches the browser and its ready state is displayed without a subsequent download action
- **THEN** completion is observable and neither a disk save nor GOST compliance is reported

### Requirement: Timing and workflow metrics

The system SHALL export 1.1 as a provisional active-time measurement, 1.2 and 1.4 through 1.8, 1.11, and 3.1 and 3.2 according to the design metric definitions. It SHALL exclude hidden-tab time and idle gaps longer than five minutes from active duration, and distinguish result display, API response and DOCX generation. The system SHALL count starts with a full 24-hour observation window in the completion denominator, including starts with no observed completion. The completion numerator SHALL count only observed completions from that same cohort.

#### Scenario: Hidden time and long idle gap

- **WHEN** a complete workflow contains both a hidden-tab interval and an idle interval longer than five minutes
- **THEN** overlapping excluded time counts once, neither interval contributes to active duration, and full duration is unchanged

#### Scenario: No documented completion

- **WHEN** a recorded start has no terminal observation within 24 hours and the observation cutoff is at least 24 hours after that start
- **THEN** it remains in the completion denominator and is not counted as complete

#### Scenario: Completed but immature start

- **WHEN** one mature start has no completion and one start less than 24 hours old already has an observed completion
- **THEN** the numerator is zero and the denominator is one

### Requirement: Server outcomes and external availability

The system SHALL export 2.1, 2.2, 2.9 and 2.10 separately. Server outcomes SHALL distinguish executed calculations, expected refusals, invalid input and technical failure. Availability SHALL use externally recorded checks of the frontend and synthetic result retrieval in configured working windows and SHALL report missed checks separately.

#### Scenario: Stored refusal versus executed calculation

- **WHEN** two create requests return HTTP 201, one with a refusal and one with a completed result whose engineering check fails
- **THEN** only the latter is counted as an executed calculation and neither is counted as a server error

#### Scenario: Application unavailable

- **WHEN** the external monitor can run but neither application probe succeeds
- **THEN** that minute is recorded independently as a failed check rather than a missing check

#### Scenario: Handled errors and exclusions

- **WHEN** a registered operation returns 422 or the application error boundary sends a final 500, and health, telemetry, preflight and unmatched routes also respond
- **THEN** the exporter counts the registered 422 and 500 by route template and excludes health, telemetry, preflight and unmatched requests
- **AND** response bodies and permitted CORS headers remain unchanged

#### Scenario: Streaming and disconnect

- **WHEN** one streamed response completes and another disconnects after headers but before the final body
- **THEN** only the completed response contributes to HTTP status ratios, and the second observation is counted as a disconnect

#### Scenario: Exception without a response

- **WHEN** an exception escapes before a response status is sent
- **THEN** the observation has an error terminal kind and no sent status, is excluded from response status ratios, and does not suppress the exception


### Requirement: Reproducible operator export

The system SHALL export a CSV with metric ID, definition version, period, unit, value, sample count, applicable numerator and denominator, and data-quality counts. It SHALL distinguish an unavailable measurement from zero, and reproduce the same rows for the same input observation snapshot, external checks, settings and definition version.

#### Scenario: Empty denominator

- **WHEN** no eligible observations exist for a ratio in the requested period
- **THEN** the export reports N/A, not zero

### Requirement: Measurement failure isolation and accessibility

The system SHALL preserve existing calculation and report behavior when measurement is disabled, unavailable or overloaded. Business responses SHALL NOT wait for telemetry database writes. Instrumentation SHALL NOT introduce interactive controls, move focus, announce telemetry failures, or delay interface updates.

#### Scenario: Measurement storage unreachable

- **WHEN** only telemetry storage or its writer is unavailable
- **THEN** calculation and DOCX outcomes are unchanged and the failure or measurement drop is exposed through payload-free operator diagnostics

### Requirement: Measurement diagnostics

The system SHALL expose measurement writer failures, queue drops, rejected batches and incomplete export inputs through structured application diagnostics containing event type, reason, count and UTC time only. Diagnostics SHALL be written through the existing application logging channel and SHALL omit request bodies, field values, report contents, raw paths, correlation UUIDs and authentication material.

#### Scenario: Diagnostic excludes payload

- **WHEN** a telemetry batch is rejected or a writer drops observations
- **THEN** the structured diagnostic contains the rejection or drop reason and count but no event payload or correlation identifier

### Requirement: Trusted pilot ingress

The system SHALL accept telemetry only when collection is enabled, the request carries exactly one valid deployment-specific proxy secret, and its Origin exactly matches the configured HTTPS pilot origin. The private proxy SHALL replace any incoming trust header with its own value. The endpoint SHALL NOT use browser cookies as authority or expose the backend port to pilot clients.

#### Scenario: Caller without pilot access

- **WHEN** a caller with missing, invalid or revoked pilot credentials sends a request to the proxy with a matching Origin
- **THEN** the proxy returns 401 before injecting its trust secret or forwarding the request, and nothing is stored

#### Scenario: Missing or forged trust header

- **WHEN** an enabled backend receives a batch without the configured secret, or with an incorrect or duplicated trust header
- **THEN** it returns 403 before reading the payload and stores nothing

#### Scenario: Cross-site browser request

- **WHEN** a proxied request has an absent, null, duplicate or foreign Origin even though it has a valid proxy secret
- **THEN** it returns 403 and stores nothing

#### Scenario: Valid trusted request

- **WHEN** the configured proxy overwrites a client-supplied trust header and forwards a valid same-origin batch
- **THEN** the application accepts one trusted header and returns 204 after commit

### Requirement: Raw observation retention

The system SHALL restrict deletion of raw pilot observations and raw export inputs to the migration-owner database identity. The export operator, application runtime and telemetry writer SHALL NOT be able to delete them.

#### Scenario: Retention at the agreed cutoff

- **WHEN** the approved retention procedure runs under the migration owner after an aggregate export is saved
- **THEN** the selected raw data is removed and aggregate exports and payload-free audit records are retained
- **AND** the same raw deletion is denied under each restricted identity
