# Tasks

Owner: Akim. Egor confirms `NormRef` only.

Branch: the spec work stays on the `Specs` line (`Specs-onboarding` now, merged into
`Specs` after review). Implementation after apply uses
`feature/calculation-core-contract/backend` (engine, report) and
`feature/calculation-core-contract/frontend` (transparent output), both Akim's zone.

Marker **[blocked: NormRef]**: the task needs the `NormRef` shape agreed with Egor
(task 1.3) before it starts.

## 1. Spec readiness

- [x] 1.1 Write proposal, design, and spec deltas for `calculation-engine`, `transparent-output`, `report-generator`, `security` (2026-09-26)
- [x] 1.1a Resolve the first review pass of `spec-reviewer` and `norm-traceability-checker` (2026-09-26; see `docs/decisions/calculation-core-contract-readiness.md`)
- [x] 1.2 Run `openspec validate calculation-core-contract --strict` and `openspec validate --all --strict` (passed 2026-09-26, 13/13)
- [ ] 1.3 Egor confirms the `NormRef` shape and answers the open questions in `design.md` (section "NormRef"); record the answer in `design.md`
- [x] 1.4 Run `spec-reviewer` on this change and resolve blockers (2026-09-26, four passes, 0 blockers; see `docs/decisions/calculation-core-contract-readiness.md`)
- [x] 1.5 Run `norm-traceability-checker` and confirm that no requirement fixes a norm value (2026-09-26, two passes, no norm value fixed)
- [ ] 1.6 `tester` issues the verdict for the spec change (see DOD)

## 2. Requirement 1: pure calculation function (backend)

- [ ] 2.1 Define the calculation function signature `(typed inputs, resolved parameters) -> result envelope` and the calculation type registry
- [ ] 2.2 Test: run a calculation with the filesystem and the network patched to raise; it completes
- [ ] 2.3 Test: two runs with identical inputs give envelopes equal except `result_id`
- [ ] 2.4 Assign `result_id` in the service layer when a result is stored

## 3. Requirement 2: typed trace step

- [ ] 3.1 [blocked: NormRef] Define the typed trace step model with `step_id`, `expression`, `substitutions`, `result`, `norm_ref` (backend)
- [ ] 3.2 [blocked: NormRef] Test: every step of a completed calculation has all fields, none null (backend)
- [ ] 3.3 [blocked: NormRef] Test: a step with an unverified `norm_ref` is marked and counted in the envelope (backend)
- [ ] 3.4 [blocked: NormRef] Render typed steps and the unverified-step summary; show each `norm_ref` with its status (frontend)
- [ ] 3.5 [blocked: NormRef] Render the envelope's `outputs` with value, unit, `rounding_rule`, and `rounding_source` (frontend)

## 4. Requirement 3: explicit units at the boundary (backend)

- [ ] 4.1 Add unit-carrying value types and the base-unit declaration per quantity in the calculation type contract
- [ ] 4.2 Add boundary conversion of inputs and outputs; test that a non-base input shows in the trace in its base unit
- [ ] 4.3 [blocked: NormRef] Add `rounding_rule` and `rounding_source` per output quantity and return them in the envelope's `outputs`; test that a type without them cannot be registered

## 5. Requirement 4: applicability check with three outcomes

- [ ] 5.1 [blocked: NormRef] Define method bounds (with `norm_ref`) and the validated range (with its source) as parameter data (backend)
- [ ] 5.2 [blocked: NormRef] Implement the check with three tests, one per outcome: run; refuse naming the bound and its `norm_ref`; run with a warning (backend)
- [ ] 5.3 Test: a request that fails schema validation never reaches the engine (backend)
- [ ] 5.4 [blocked: NormRef] Show the warning and the refusal in the UI, readable without colour (frontend)

## 6. Requirement 5: result envelope and accountability

- [ ] 6.1 [blocked: NormRef] Define the envelope with `result_id`, `engine_version`, `input_hash`, `norm_refs`, `verdict`, `verdict_reason`, `warnings`, `trace`, `unverified_step_count`; `outputs`; test the refused envelope (empty `trace` and `outputs`, `unverified_step_count` 0, `verdict_reason` names the bound, `norm_refs` contains the bound's `NormRef` and every warning's `NormRef`) (backend)
- [ ] 6.2 Implement `input_hash` per `design.md` decision 6; test that identical inputs and parameters give identical hashes, and that a different input, calculation type, or resolved parameter set each gives a different hash (backend)
- [ ] 6.3 [blocked: NormRef] Print the accountability block and the engineer responsibility statement in the report (backend)
- [ ] 6.4 Add the signature-block report setting; test the section order with the block enabled and disabled (backend)
- [ ] 6.5 (backend, no code) Check GOST R 21.101 (edition unverified) from its primary source text and decide the default of the signature-block setting; until then the requirement stays `unverified`

## 7. Pilot and sync

- [ ] 7.1 Use one in-scope calculation type of `foundations-shallow` (from WP1) as the pilot for the contract tests, once WP1 names it (backend)
- [ ] 7.2 After apply of this change, sync `backend-layered-architecture` (WP5): reword task 6.2 so the engine receives parameters as typed arguments (B5); update `design.md` decision 7 to name the pure function as the C/C++ boundary; settle the open question "formulas in YAML vs in code" from this change's `design.md`. The change owners (Akim and Egor) edit it; this change does not
- [ ] 7.3 Record for WP3 that `report-generator` names GOST R 21.101-2020 with an unchecked edition

## 8. Close

- [ ] 8.1 Merge to `Specs` after 1.2-1.6 pass
- [ ] 8.2 Confirm WP1 task 2.1 (`retarget-mvp-domain`) is closed: the WP1 engine and output deltas match this contract
- [ ] 8.3 `spec-keeper` syncs the deltas and archives the change, after `retarget-mvp-domain` is archived

## Dependencies

- `retarget-mvp-domain` (WP1) archives first; this change needs only its domain name.
- Task 1.3 (`NormRef` agreed with Egor) blocks every task marked [blocked: NormRef].
- Task 7.2 runs after this change is applied.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task 1.2)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements recorded (`design.md`, "Non-functional requirements")
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branches defined (above)
- [ ] Dependencies satisfied: `NormRef` agreed with Egor (task 1.3)

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4).
- For the spec phase: `openspec validate --all --strict` passes; `spec-reviewer` reports
  no blockers; `norm-traceability-checker` confirms no norm value is fixed; Egor has
  confirmed `NormRef`.
- For implementation: all tests of sections 2-6 pass with >= 95% branch coverage;
  `ui-ux-tester` confirms the frontend tasks 3.4, 3.5, and 5.4; the delta specs match the
  implementation.
- NO-GO: validation fails; an unresolved blocker; a norm value, tolerance, or clause
  number fixed in a spec; a `NormRef` field that can be null; a test failure or coverage
  below 95%.
- Archive (8.3) happens only after GO.
