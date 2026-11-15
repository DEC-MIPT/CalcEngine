## Purpose

Define a pure typed extension boundary for calculation modules and a domain-neutral
executor, while preserving the R pilot's external result and historical identity.

## ADDED Requirements

### Requirement: Trusted typed modules
The system SHALL execute only trusted modules registered by application startup. Registration occurs outside pure execution.
A module SHALL declare its identifier, methodology version, input/resolved-data/
execution-options/output/diagnostic-detail schemas and schema versions, pure input
normalization and domain validation, applicability validation, computation, diagnostic
validation and external-result adaptation. The common executor SHALL be parameterized
by those model types and SHALL NOT require a flat quantity mapping. Loading code or
resolving data is outside the pure execution boundary. Duplicate module identifiers,
empty version metadata or missing schema declarations SHALL prevent registration.

#### Scenario: Structured input model
- **WHEN** a registered test module receives a nested typed input model
- **THEN** the common executor validates and executes it without flattening it into a quantity mapping

#### Scenario: Unregistered or invalid module
- **WHEN** a caller requests an unknown module or startup attempts duplicate registration or incomplete module metadata
- **THEN** the operation raises a typed application error and executes no calculation

#### Scenario: Strict boundary validation
- **WHEN** inputs, resolved data or execution options violate their declared schema, including unknown fields and non-finite quantities
- **THEN** execution fails validation before computation, with no result adaptation or persisted result

### Requirement: Pure isolated execution
The system SHALL validate and normalize typed inputs before module computation,
validate resolved data and explicit execution options, obtain the run identity,
invoke module computation, which checks applicability before and during its method,
validate its returned outcome and diagnostic details, and only then permit external
adaptation by the caller. The common executor returns the internal execution record;
it does not invoke the external adapter itself.
Normalization, validation, computation, identity and adaptation SHALL perform no I/O,
clock reads, randomness or mutation of caller-owned inputs, data or options. No run
SHALL depend on mutable state from another run. The executor SHALL contain no branch
on a calculation identifier, foundation geometry or domain diagnostic field.

#### Scenario: Repeated and interleaved calls
- **WHEN** identical calls are repeated with another module call between them
- **THEN** their typed outcomes and identities match bit for bit and all caller-owned models remain unchanged

#### Scenario: Domain module extension
- **WHEN** another trusted module supplies its models, computation, validation and adapter
- **THEN** it executes without modifying the common executor or adding a domain identifier branch there

#### Scenario: No I/O during execution
- **WHEN** execution runs with file, network and database access patched to fail
- **THEN** an otherwise valid module run completes using only its supplied data

### Requirement: Independent execution applicability and checks
The system SHALL distinguish execution status completed or stopped from applicability
applicable, outside_validated_range or not_applicable and from ordered engineering
check results. A completed outcome SHALL be applicable or outside_validated_range,
contain its schema-valid final output model, have no stop diagnostic and retain its
ordered trace/checks. A failed engineering check SHALL NOT imply a stopped execution
or inapplicability. The applicability applicable SHALL carry no applicability warnings;
outside_validated_range SHALL carry at least one. A stopped outcome MAY retain
warnings found before its stop. A stopped outcome SHALL be not_applicable, contain a stop diagnostic,
have no final output model and no final aggregate engineering-check conclusion. A preflight
stop SHALL retain an empty trace; a stop during computation SHALL retain only its
completed diagnostic prefix. The stop stage SHALL explicitly distinguish
before_calculation from after_start; completed outcomes have no stop stage.
Individual completed checks in a diagnostic prefix remain trace facts, not a final
conclusion. Ordered engineering-check results SHALL match check steps in the trace. Technical faults and malformed module returns SHALL
raise a calculation error rather than become method refusal. Modules may have no
engineering checks internally; existing foundation adapters retain their required
checks and pass/fail decision rules.

#### Scenario: Failed check on an applicable method
- **WHEN** a completed applicable run includes a failed engineering check
- **THEN** its execution remains completed and applicable and its check retains failed status

#### Scenario: Contradictory outcome
- **WHEN** a module returns completed with not_applicable or a diagnostic, or stopped with final outputs or a final aggregate check conclusion
- **THEN** the executor rejects the outcome before invoking its external adapter

#### Scenario: Technical failure
- **WHEN** module computation returns malformed data or produces a non-finite intermediate
- **THEN** a typed calculation error is raised rather than a valid stopped outcome

### Requirement: Module-owned stop diagnostics
The system SHALL retain a stop diagnostic with a nonempty stable reason code, an
explicit Source, associated typed module details and, after computation starts, a
reference to a completed diagnostic step. The module's diagnostic schema and validator
SHALL reject details of another module or unknown/invalid domain fields before result
adaptation. The common executor SHALL validate generic structure, unique trace step
identifiers and presence of any diagnostic step reference in the retained trace,
without inspecting the details' field names. Preflight diagnostics have no step
reference because no computation has run. Diagnostic values SHALL remain intermediate
values, never final output quantities or successful engineering conclusions.

#### Scenario: Stop before computation
- **WHEN** module preflight finds the method inapplicable
- **THEN** numerical computation is not called, status is stopped/not_applicable, trace is empty and the diagnostic has no computed-step reference

#### Scenario: Stop after intermediate computation
- **WHEN** a module adopts a derived applicability guard after completed trace steps
- **THEN** its stopped outcome preserves those steps, names a retained step and exposes no final outputs or final check conclusions

#### Scenario: Invalid diagnostic details or reference
- **WHEN** diagnostic details fail the module schema or validator, a trace identifier repeats, or a diagnostic references a missing step
- **THEN** the executor raises a calculation error before external adaptation

### Requirement: Versioned module run identity
The system SHALL provide a versioned identity for new modules from canonical JSON
and SHA-256, covering the module identifier, methodology and schema versions,
normalized inputs, resolved data including source references, and all computation-
or applicability-affecting execution options. The identity version SHALL be explicit
in the hashed preimage as format=calculation-module-run-v1. The input, resolved-data,
options, output and diagnostic-details schema versions SHALL all be included. Object key order SHALL NOT change identity; sequence order
SHALL be preserved. Integer values SHALL retain exact precision, including above
2**53. Finite floats SHALL use their shortest round-trippable representation;
integer 1 and float 1.0 remain distinct unless module normalization produces the
same typed value. JSON object keys SHALL be strings; unsupported values, non-string
keys and non-finite floats SHALL be rejected rather than coerced. The new serializer
SHALL NOT alter the legacy canonical serializer or its integer-to-float policy.
The R compatibility module SHALL retain its existing identity algorithm including
both method and validated ranges; it SHALL NOT adopt the new preimage or rewrite
stored identities. Presentation-only envelope metadata remains outside computation.

#### Scenario: Semantic identity changes
- **WHEN** normalized inputs, resolved source data, methodology/schema version or a significant execution option changes for a new module
- **THEN** its run identity changes

#### Scenario: Equivalent canonical inputs
- **WHEN** two calls differ only in object-key insertion order or unit representations normalized to identical typed inputs
- **THEN** their versioned run identities match

#### Scenario: Large integers and invalid keys
- **WHEN** a new-module identity receives adjacent integers above 2**53 or an object with a non-string key
- **THEN** the integers produce different identities and the invalid key raises a calculation error without coercion

#### Scenario: Typed numeric identity
- **WHEN** normalized models retain integer 1 in one call and float 1.0 in another
- **THEN** their versioned preimages differ, while calls normalized to the same typed value have the same identity

#### Scenario: Legacy identity remains exact
- **WHEN** the R pilot runs using its original parameters and applicability ranges
- **THEN** its input_hash equals the original algorithm's value without a new identity-version field in its public payload

### Requirement: R pilot compatibility adapter
The system SHALL route the existing R pilot through the common executor and a
compatibility module, retaining its accepted input/output contract, original numerical
values and rounding, step order and identifiers, deciding check, normative references,
parameter-source digest, bound refusal ordering and hash algorithm. Its public API
payload and schema, saved-result reading and DOCX meaning SHALL remain unchanged.
Historical results SHALL be read and reported without recomputation or rewriting.
Regression expected values and golden fixtures SHALL NOT be regenerated to accept a
migration difference. A compatibility mismatch SHALL block feature GO.

#### Scenario: Pilot regression
- **WHEN** the pilot's existing reference and frozen-corpus suites run through the module adapter
- **THEN** all original expectations pass with unchanged fixtures, trace identifiers, source identity and deciding check

#### Scenario: Historical readback and report
- **WHEN** a result saved before the module contract is retrieved and rendered to DOCX
- **THEN** its payload validates and its report is produced from the saved data without executing the engine

### Requirement: Bounded non-functional acceptance
The system SHALL preserve the existing applicable API/report performance contracts
and record their actual checks, without asserting an undefined typical-calculation
benchmark. The module boundary SHALL preserve strict schemas, safe expression-tree
execution, existing layer restrictions and lack of dynamic code loading or ML.
Backend acceptance SHALL include lint, types, import boundaries and tests with at
least 95 percent branch coverage under backend/check.sh. Real database/catalog tests
not executed SHALL be reported as skips. This feature changes no UI; accessibility
acceptance is preservation of the existing public schema and UI behavior. A public
schema drift or a required frontend change SHALL block this feature until its scope
is resolved. Tester GO and independent review SHALL precede integration and archive.

#### Scenario: Backend acceptance evidence
- **WHEN** tester assesses the completed backend feature
- **THEN** the record includes actual lint/type/import/test results, branch coverage, compatibility evidence and database/catalog checks or skips

#### Scenario: UI and public schema remain compatible
- **WHEN** the backend-only module feature is checked against the existing API schema and frontend contract
- **THEN** existing pilot payloads and public schema match and no frontend adaptation is required
