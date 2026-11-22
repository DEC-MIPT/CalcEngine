## ADDED Requirements

### Requirement: Versioned foundation design requests and results
The system SHALL expose design-tool requests and immutable stored outcomes through an additive, versioned API contract: a proposed new registered explicit-weight type uses existing calculation routes, while a dedicated typed search resource stores candidate evaluation and links a selected ordinary calculation result. Existing requests, routes and result retrieval remain compatible. The new registered type and methodology SHALL identify its fixed explicit-weight and upper-cut load semantics using only declared quantity fields; an additional selectable load-level variant requires a separately approved typed request shape and SHALL NOT place string enums inside QuantityValue. The new contract SHALL distinguish checking one supplied rectangle from evaluating a bounded candidate set and identify its engineering policy; and carry complete typed diagram and candidate-result data. Historical results SHALL remain valid without new mandatory fields. A candidate selection SHALL store the selected calculation and its original inputs, and SHALL link its search provenance without silently recalculating it on retrieval or report request.

#### Scenario: Old request and result compatibility
- **WHEN** a client sends an existing averaged calculation request or retrieves an old pilot or loads result
- **THEN** the request/result retains its prior behavior and no historical record is rewritten

#### Scenario: Search outcome retrieved unchanged
- **WHEN** a stored candidate outcome is retrieved twice
- **THEN** the candidate identities, policy, selected result and diagnostic data are equal without a new search

#### Scenario: Invalid contribution rejected
- **WHEN** a request uses an unsupported contribution unit, omits a declared scalar component or supplies an undeclared load-level field
- **THEN** validation rejects named fields before engine execution and no partial calculation is stored as complete; source attribution is supplied by the registered methodology rather than an unbounded per-contribution request object


### Requirement: Bounded foundation selection resource
The system SHALL expose POST /foundation-selections with schema_version=foundation-selection-request-v1, calculation_type=foundations_shallow_loads, policy_version=foundation-min-area-v1, common_inputs containing all registered quantities except b/l, and an ordered non-empty list of at most 256 strict candidate objects with b/l QuantityValue fields. The policy SHALL select minimum area among passing candidates and resolve equal-area ties using the first original input index. The existing 1 MiB HTTP body limit SHALL remain. The entire request SHALL be validated before evaluating any candidate, with no axis swap, implicit deduplication or encoding search configuration as quantity values. The service SHALL resolve parameters separately for each geometry and retain the original candidate indices and complete evaluated evidence.

#### Scenario: Invalid list rejected before work
- **WHEN** the list is empty, exceeds 256 entries, has an invalid dimension/unit, supplies common b/l or names another calculation type
- **THEN** the API returns named-field 422 without evaluating a candidate; an oversized HTTP body returns the existing 413 payload_too_large

#### Scenario: Terminal selection response
- **WHEN** a valid search produces a stored terminal outcome
- **THEN** POST returns 201 and Location for /foundation-selections/{selection_id}, with schema_version=foundation-selection-result-v1, original request, candidate outcomes, policy/source identities and status selected, no_acceptable_candidate or incomplete

#### Scenario: An incomplete set cannot certify a winner
- **WHEN** candidate source resolution fails, a calculation raises an unexpected error or the cooperative evaluation budget is exceeded
- **THEN** the stored status is incomplete with a typed reason and evaluated/unattempted indices, selected_candidate_index and selected_result_id are null, and an earlier passing candidate is not reported as a certified selection

### Requirement: Atomic selection and result persistence
The system SHALL persist a selected ordinary calculation, its immutable foundation visualization sidecar and the immutable selection record in one application-database transaction using the already evaluated winning result. A selected record SHALL link exactly that ordinary result. No-solution or incomplete outcomes SHALL contain no selected result. GET /foundation-selections/{selection_id} SHALL return the stored outcome unchanged, and POST /foundation-selections/{selection_id}/report SHALL use the existing ReportRequest and DOCX response conventions without reevaluation. Database failure SHALL return structured 503 and leave no orphan selected calculation or partial complete record.

#### Scenario: Winner write fails atomically
- **WHEN** any winner, sidecar or selection insert fails before commit
- **THEN** all writes are rolled back and no selected result or selection link is exposed

#### Scenario: Retrieval and report do not search again
- **WHEN** a stored selected, no-acceptable-candidate or incomplete outcome is retrieved or reported
- **THEN** its recorded candidate evidence and conclusion are used without engine execution or current-source resolution, and no-solution/incomplete reports contain no success conclusion

### Requirement: Cooperative selection cancellation and budget
The system SHALL apply a 10-second cooperative evaluation budget outside the pure engine and SHALL check it and client cancellation before/after candidates and before final selection. A running single source/calculation operation SHALL NOT be claimed forcibly terminated by that budget. The service SHALL introduce no detached search job, queue or unbounded candidate concurrency. Client cancellation SHALL preserve the form draft and stop future evaluation at a safe boundary; it SHALL NOT promise to delete an immutable result committed before cancellation was observed. If a cancellation audit record is persisted, its status SHALL be incomplete with no winner. Its identifier delivery to a disconnected client is not guaranteed.

#### Scenario: Budget exceeded after an earlier pass
- **WHEN** an earlier candidate passed but the full evaluation exceeds its cooperative budget
- **THEN** no winner is certified, the record identifies the timeout and remaining indices, and the response does not claim a hard 10-second HTTP latency guarantee

#### Scenario: Cancel before and after commit
- **WHEN** cancellation is observed before the atomic winner commit
- **THEN** no winner is committed, whereas a result already committed before cancellation remains immutable and the UI does not claim that cancellation undid it

### Requirement: Immutable foundation visualization context
The system SHALL expose GET /foundation-calculations/{result_id}/context returning an immutable sidecar with schema_version=foundation-result-context-v1 for new domain-supported runs. It SHALL contain original quantity inputs/type/methodology, explicit load/weight semantics and typed stored diagram values with input/trace references. It SHALL be written atomically with its ordinary result and SHALL NOT change ResultEnvelope, original input_hash or historical result meaning. Old rows without a sidecar SHALL remain valid and return structured 404 foundation_context_unavailable for the context route; their existing result and report routes remain usable. A missing ordinary result SHALL retain structured 404 not_found. No context route SHALL infer missing original inputs or rerun a calculation.

#### Scenario: Historical result has no visualization sidecar
- **WHEN** an old result without a context row is opened
- **THEN** existing result/report retrieval works, the context route reports foundation_context_unavailable, and the frontend shows the stored trace/table without fabricating a diagram

#### Scenario: Diagram quantities retain stored provenance
- **WHEN** a new complete or diagnostic-refused foundation context is retrieved
- **THEN** every physical diagram value identifies its stored input or trace step and all signed corner values and applicability labels are preserved without client-side pressure calculation
