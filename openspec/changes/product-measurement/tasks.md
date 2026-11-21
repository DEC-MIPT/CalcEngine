# Tasks

## 1. Definition of ready

- [ ] 1.1 Run `openspec validate product-measurement --strict` and obtain a current `spec-reviewer` report with no blocker or major finding before code work.
- [ ] 1.2 Create the feature branch `feature/product-measurement/backend` from current `develop` and record its backend task ownership; verify the branch is not `develop` before code edits.
- [ ] 1.3 Create the feature branch `feature/product-measurement/frontend` from the backend feature branch after its contract is available; verify it owns only frontend files and generated API types.
- [ ] 1.4 Create the feature branch `feature/product-measurement/infra` from current `develop`; verify its changes are limited to monitor and pilot configuration.

## 2. Backend feature - `feature/product-measurement/backend`

- [ ] 2.1 Add typed measurement schemas, event vocabulary, and feature settings; verify unknown fields, disabled defaults, UUIDs, sequence numbers, attribute allowlists, batch size and request size are covered by pytest.
- [ ] 2.2 Add additive PostgreSQL models, repositories and migration for scenarios, client events, server observations, monitor slots, export snapshots and writer diagnostics; verify migration upgrade/downgrade and repository round trips with PostgreSQL tests or documented skips.
- [ ] 2.3 Implement private event intake at `POST /telemetry/events` with atomic batches, duplicate handling, conflict responses, size limits and disabled behavior; verify API status codes, no payload logging and no persistence for invalid batches.
- [ ] 2.4 Add nonblocking server measurement around calculation and DOCX routes without changing business outcomes; verify refusal, executed engineering failure, HTTP failure, report success and report failure are represented separately.
- [ ] 2.5 Add bounded measurement writer and graceful lifespan flush; verify queue overflow and storage failure never fail a calculation or report response and diagnostics contain no request payloads.
- [ ] 2.6 Implement UTC cohort selection, visibility and idle exclusion, 24-hour completion cutoff, sequence-gap detection, exact median and nearest-rank p95 aggregation for metrics 1.1, 1.2, 1.4-1.8, 1.11, 2.1, 2.9, 2.10, 3.1 and 3.2; verify boundary, empty-denominator, duplicate and incomplete-sequence cases.
- [ ] 2.7 Implement monitor CSV import, snapshot-based metric export and `python -m scripts.export_pilot_metrics`; verify schema validation, duplicate slots, deterministic ordering, `N/A` output and identical repeat exports.
- [ ] 2.8 Run backend ruff, mypy, import-lint and focused pytest with branch coverage at least 95% for changed measurement code; record skipped database checks explicitly.

## 3. Frontend feature - `feature/product-measurement/frontend`

- [ ] 3.1 Add the versioned telemetry client with bounded in-memory queue, one retry for transport or 503, terminal event protection and silent failure; verify no request blocks form interactions and queue drops are bounded.
- [ ] 3.2 Instrument the calculation and report journey with scenario, step, field, attempt, visibility, progress, result-visible and report-ready events; verify one event per semantic action and no raw input, clipboard, route or report content is sent.
- [ ] 3.3 Add validated correlation headers to calculation and DOCX requests and regenerate/check API types; verify UUID format, attempt separation and compatibility with existing API tests.
- [ ] 3.4 Add browser tests for hidden-tab intervals, five-minute idle boundary, reload/new scenario, result visibility, report readiness, retry and disabled collection; verify Playwright produces a complete event sequence for one synthetic walkthrough.
- [ ] 3.5 Run ESLint, TypeScript, Vitest and focused Playwright checks with branch coverage at least 95% for changed telemetry code; obtain ui-ux-tester confirmation that instrumentation does not alter focus, announcements, controls or visible timing.

## 4. Infrastructure feature - `feature/product-measurement/infra`

- [ ] 4.1 Add a separate monitor command or container configuration for minute-aligned frontend and synthetic-result probes with five-second timeouts; verify it stores only slot and boolean results and continues when DEC is unavailable.
- [ ] 4.2 Add pilot configuration and operational instructions for private ingress, feature flags, UTC retention, working windows, monitor CSV import and rollback; verify the default deployment has collection disabled and no secret or personal value is committed.
- [ ] 4.3 Run the monitor and configuration checks in the local environment without changing application behavior; record unavailable external-host checks as skipped rather than successful.

## 5. Integrated acceptance

- [ ] 5.1 Merge feature branches only after their tester GO and review; in a clean `develop` checkout run backend and frontend checks, migration checks and selected strict OpenSpec validation.
- [ ] 5.2 Execute one disabled-collection walkthrough and one enabled-collection walkthrough; verify the calculation result and DOCX are unchanged, telemetry failures do not block responses, and the exported CSV matches the expected fixture.
- [ ] 5.3 Obtain tester GO with tests passing and branch coverage at least 95%, plus ui-ux-tester confirmation for the frontend; record limitations for unmeasured metrics and external monitor evidence before archiving.

## Definition of ready

- [ ] DOR: proposal, spec delta, design and tasks exist; strict validation passes; spec-reviewer reports no blocker or major finding; requirements and non-functional constraints are testable; branches and dependencies are listed.

## Definition of done and Go/No-Go

- [ ] DOD/GO: all tasks are checked, relevant tests pass, changed code has at least 95% branch coverage, security review has no finding, frontend UI/UX check passes, integrated validation passes, tester declares GO, and the spec-keeper syncs and archives the change.
- [ ] NO-GO evidence is recorded for any test failure, coverage below 95%, security finding, missing UI/UX confirmation, invalid OpenSpec artifact or unverified integrated behavior; no archive occurs until resolved.
