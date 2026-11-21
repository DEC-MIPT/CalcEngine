# Proposal

## Why

DEC needs repeatable evidence of calculation workflow duration, completion and reliability during its closed pilot. API logs alone cannot establish when an engineer started entering data or when the browser displayed the result or received a DOCX.

## What changes

- Collect a bounded set of browser workflow events and server-owned timing and outcome observations. Keep collection off by default and isolate its failures from calculation and reporting.
- Store pilot observations in the application PostgreSQL database and export versioned aggregate metrics through an operator CLI.
- Import minute-level availability observations from a monitor outside the DEC application.

## Capabilities

### New capabilities

- `product-measurement`: closed-pilot instrumentation, data quality, aggregation and export, and availability monitoring.

### Modified capabilities

- `calculation-api`: allow a validated measurement-attempt correlation header on existing calculation and report requests without changing business responses.
- `web-platform`: allow the same header for configured frontend origins.

## Non-goals

Public analytics, company or engineer breakdowns, billing, dashboards, autosave, business-operation idempotency, new calculation methods, automated GOST certification, external-tool inference, surveys, and replay across normative revisions. These require separate sources or changes; absence of these measurements is not a zero result. The export is a local operator command, not a public API.

## Impact

The backend feature owns telemetry schema, storage, intake and export. The frontend feature owns workflow instrumentation and generated API types. The infra feature owns pilot ingress and the external monitor. See the branch and acceptance order in `tasks.md`.
