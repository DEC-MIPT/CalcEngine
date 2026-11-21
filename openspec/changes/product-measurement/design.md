# Design

## Context

FastAPI persists results before sending HTTP 201 (`backend/app/api/dependencies.py`, `backend/app/api/calculations.py`); a stored result can be refused. The DOCX form separates receiving a blob from asking the browser to download it (`frontend/src/components/ReportForm.tsx`). The existing `/health` endpoint does not check result storage (`backend/app/api/health.py`).

## Goals and non-goals

Keep the existing backend layer order. The C/C++ replacement boundary remains the pure `Calculator.calculate` interface. Browser and server instrumentation observe behavior outside that boundary. Do not alter calculation inputs, immutable results or report contents.

## Decisions

### Intake and storage

Use a same-origin private ingress with no direct public backend route. The infra feature must verify ingress isolation before enabling collection. Configure the frontend and backend flags off by default. The endpoint `POST /telemetry/events` accepts JSON with `schema_version: 1` and 1 to 50 observations in at most 32 KiB. Reject unknown fields, unknown event types and invalid UUIDs, sequence numbers or integer millisecond offsets. Requests outside the pilot ingress are blocked there; the disabled endpoint responds 404. For valid intake return 204 after persistence, 503 if persistence is unavailable, 413 for the size limit and 422 for invalid schema. Invalid batches are atomic. Ignore identical duplicate deliveries; reject conflicting event IDs or sequence positions with 409. Export is a local command executed under the application process account; no HTTP read endpoint exists.

A scenario UUID spans eligible routes in a single active browser tab; reload starts a new scenario. Generate a new attempt UUID for every calculation or DOCX request and carry it in `X-DEC-Measurement-Attempt`. Use an attempt ID only to correlate observations; it confers no authority and never deduplicates a business operation. Use separate client and server tables in application PostgreSQL; server timestamps are UTC. Store normalized route templates, numeric timings and enumerated outcomes. Do not record raw paths, payloads, free-form field values, or headers other than a validated correlation UUID. Run the writer with a separate bounded connection pool and transaction.

Client events: `scenario_started`, `field_committed`, `step_entered`, `validation_failed`, `calculation_submitted`, `progress_shown`, `result_visible`, `report_requested`, `report_ready`, `visibility_changed`. Events carry UUID, 1-based sequence, elapsed milliseconds and typed attributes only as applicable: attempt UUID, step key from the workflow vocabulary, or visible/hidden state. Start includes the initial visibility state. The exact envelope is `{schema_version, batch_id, scenario_id, events}` and each event is `{event_id, sequence, event_type, elapsed_ms, attempt_id?, step_key?, state?}`. `event_id` is globally deduplicated; `sequence` is unique within a scenario; `batch_id` identifies a delivery attempt. An identical event ID with a different payload or a conflicting sequence is a 409. Store events in memory and send up to 50 at a time; retry once on transport error or 503, retaining IDs. Cap pending events at 200; drop newest nonterminal events at capacity, without reusing their sequence numbers. Do not store events in browser persistent storage. Result latency stops once output is rendered, not on response receipt. The report-ready event fires once ready UI is visible for the successful response.

Capture server terminal markers after the business result is committed, with request duration measured through the start of the final response. Separately time the report generation call. Put observations on a bounded, nonblocking queue of 1,000 per process. A lifespan-owned worker flushes at 100 records or after one second, with a write timeout and a bounded shutdown flush. Emit counts for local drops and write failures through the existing structured application logging channel, recording only event class, reason, count and UTC time. Queue data is best-effort, not an audit log. Use separate storage paths for observed process failures and business results; never mark an uncommitted result successful.

### Metric definitions

Select starts by server receipt time in the half-open UTC report period. Use an explicit observation cutoff no earlier than the period end. Freeze an export by retaining its observation snapshot plus monitor input and parameters. For each start, take the first observed `report_ready` within 24 hours of the start according to the browser offset, provided the event reached the server by the cutoff. Metrics that depend on the full sequence require contiguous events from start through that terminal marker. Report how many starts remain immature and how many completed sequences have gaps. Receipt time is a cohort anchor, not a duration clock.

| ID | Definition v1 |
|---|---|
| 1.1, 1.2 | Median active and total seconds for complete observed sequences. Sum inter-action intervals of at most five minutes after subtracting hidden intervals; visibility and progress markers are not actions. Always include the start and report-ready boundaries. Label 1.1 provisional. |
| 1.4 | Observed completions divided by starts that are at least 24 hours old at the cutoff; a completion with sequence gaps still counts if both boundaries are observed. |
| 1.5 | Nearest-rank p95 of client milliseconds from submission to result visible for matched attempts within complete sequences. Also export the count above 10 seconds without progress shown by 10 seconds. |
| 1.6, 1.7 | Nearest-rank p95 of API response durations for executed calculations and DOCX generation durations for successful generations in the selected period. |
| 1.8 | Median of per-workflow ratios: sum of executed calculation response durations and successful report generation durations, divided by active duration. Require all submitted calculation and report attempts to have paired terminal observations, complete browser intervals, no overlap of timed operations and a positive active duration. Use only cycles in which each contributing client operation window lies inside active time. Report eligible count against complete cycles. |
| 1.11 | Executed calculation count per pilot-local day plus mean and peak over all covered days, including zero-observation days when collection was enabled. |
| 2.1 | Executed divided by executed plus technical failures in working windows; report excluded refusals and invalid input. An engineering failure verdict on an executed result does not change the technical outcome. |
| 2.2 | Successful external minute checks divided by observed checks in working windows. Export expected, successful, failed and missing slots and mark incomplete windows as partial. |
| 2.9, 2.10 | 5xx and 4xx respectively divided by final HTTP responses in working windows, overall and per registered API route template. Exclude the measurement endpoint, health, unmatched routes and client disconnects from both ratios; report disconnect counts separately. |
| 3.1, 3.2 | Over complete observed sequences, fraction without a return to a previously visited step, repeated submission without a field commit or intervening step transition, or validation failure followed by field commit on that step. Median number of field commits, calculation submits and report requests. |

Use exact ordered samples for median and p95; for even medians average the two central values. Samples are unweighted. Export CSV to stdout via `python -m scripts.export_pilot_metrics`; require period start, end, cutoff and an operator-provided JSON manifest containing IANA time zone and dated working windows. Windows are half-open, nonoverlapping and minute-aligned. Import monitor CSV columns `slot_utc,frontend_ok,result_ok`; a slot succeeds only when both probes pass, and duplicate slots are rejected as ambiguous. Use one read-only database snapshot per export; order rows by metric ID and dimension; represent absent results as `N/A`.

### HTTP instrumentation and monitor boundary

Use application middleware for final HTTP status and duration observations on every registered route. Normalize only the route template, not the raw path. Exclude the telemetry endpoint, health endpoint, unmatched routes and client disconnects from 2.9 and 2.10, but count their exclusions in diagnostics. The calculation and DOCX services additionally emit typed business outcome observations. Add `X-DEC-Measurement-Attempt` to the configured CORS allow-list and validate it as a UUID; no unconfigured origin is allowed.

Run the monitor on a separate host or service outside DEC's deployment. Probe a configured frontend URL and retrieve a designated immutable synthetic result through the private ingress; require HTTP 200 and identify the expected frontend and result. Set a five-second timeout per probe and store only booleans with the scheduled UTC minute slot. A missing observation is not downtime or uptime. This check does not claim fresh calculation or DOCX generation is available.

## Risks and trade-offs

- Missing browser tails are not distinguishable from abandonment. Export observed completion and report delivery gaps; do not claim unobserved user intent.
- A bounded queue can drop observations during overload or process termination. Use diagnostics to qualify the pilot sample; do not retry business operations because measurement failed.
- The same database host is a shared failure domain despite separate sessions. Keep queue and writer resource limits low and compare enabled and disabled runs against existing API latency checks.

## Migration plan

Apply an additive migration before enabling the backend flag. Deploy disabled, configure private ingress and retention, run the probe and one synthetic walkthrough, then enable both collection flags. Disable both flags to roll back collection without deleting evidence. The operator deletes raw pilot observations at the agreed date after saving an authorized aggregate export. Do not point the monitor at the real pilot until the operator confirms setup.
