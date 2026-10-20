# Tasks

Owner: Akim. Zone tags: an implementation task belongs to the `backend` sub-branch unless it says (spec) or (engineer, no code). Egor reviews the shared files only (section 4).

Branch: spec work is committed directly to `develop` (`AGENTS.md`, Branching rules). Code is
done on `feature/calculation-verification/backend` (Akim's zone, from `develop`) and merged
only when the whole feature is done. Checkboxes in this file are ticked in `develop` as each subtask is done on the feature branch; the code reaches `develop` only when the whole feature is done (`AGENTS.md`, Branching rules).

Marker **[blocked: typical calculation]**: the task waits for the engineer's definition of a
"typical calculation". The only task with it, 3.7, moved to section 5 on 2026-10-20.
`calculation-core-contract` is re-checked and `NormRef` is agreed
in writing by Egor (`docs/decisions/normref-questions-egor.md`, commit `a1a896c`), so no
task waits for it.

## 1. Spec readiness

- [x] 1.1 (spec) Run `openspec validate calculation-verification --strict` and `openspec validate --all --strict`
- [x] 1.2 (spec) Run `spec-reviewer` on this change and resolve blockers
- [x] 1.3 (spec) Run `norm-traceability-checker` and confirm that no requirement fixes a norm value or tolerance
- [x] 1.4 (spec) Akim confirms the proposed points in `design.md`: decision 7 (how a difference is declared) and decision 9 (reproducibility below 100% is NO-GO) (2026-09-27, both confirmed as proposed)
- [x] 1.5 (spec) `tester` issues the verdict for the spec change (see DOD) (2026-09-27: **GO**, spec phase; three `spec-reviewer` rounds (fixed a stale DOD wording and an untracked-citation major), validation, and an independent norm-value spot-check all pass; implementation sections 2-3 remain open and are not covered; see `docs/decisions/calculation-verification-readiness.md`)

## 2. Ready to implement now

Depends on `retarget-mvp-domain` for the list of calculation types of `foundations-shallow`.

### Requirement 1: reference examples (backend)

- [x] 2.1 Define the reference example data model with the fields of the requirement (`tolerance`, `tolerance_source`, `origin`, source citation, `source_norm_edition`)
- [x] 2.2 Test: an example without a `tolerance`, `origin`, citation, or `source_norm_edition` is rejected
- [x] 2.3 Implement the reference suite runner with the tolerance rule of the requirement; test: an output outside its `tolerance` gives NO-GO naming the example and the quantity
- [x] 2.4 Test: a calculation type with fewer than 3 examples makes the suite invalid

### Requirement 2: `calculation-engine` accuracy and latency

- [x] 2.6 (spec) Confirm that the REMOVED "performance and accuracy" requirement and the ADDED accuracy and latency requirements pass `openspec validate --strict` (2026-09-27: the `calculation-engine` delta has REMOVED "Non-functional — performance and accuracy" and ADDED "Calculation accuracy" and "Calculation latency"; `openspec validate calculation-verification --strict` passes)

### Requirement 4: invariant tests (backend)

- [x] 2.8 Define the invariant list structure (identifier, statement, quantities), a way to declare the valid range per calculation type, and the seed record in the test report
- [x] 2.9 Property test for unit-change consistency, shared by all types (uses the units requirement of `calculation-core-contract` by name)
- [x] 2.10 Property test for determinism, shared by all types (uses "Pure calculation function" by name)
- [x] 2.11 (engineer, no code, no zone) Confirm the invariants specific to `foundations-shallow`; then add a property test for each (2026-10-06: 9 invariants and the valid input range confirmed by Akim, `docs/decisions/reference-examples-foundations.md`, section 4; property tests of the 3 formula-independent ones done on `feature/calculation-verification/backend`, `eefc660`; 2026-10-20: the 6 that depend on formula (5.7) run on the formula and coefficients of the ingested catalog, `543876c`, and pass there; they are skipped without `DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL`)
- [x] 2.12 Test: a listed invariant without a property test makes the verification incomplete

### Requirement 5: metrics, ready part (backend)

- [x] 2.13 Compute "deviation from the references" per quantity with its `tolerance`
- [x] 2.14 Compute "reproducibility rate" over the reference examples, envelopes compared excluding `result_id`; test that a rate below 100% gives NO-GO
- [x] 2.15 Attach both metrics to the tester's GO report; test that a GO without them is invalid

## 3. Depends on `calculation-core-contract`

- [x] 3.1 (spec) Re-check every item in the dependency table of `design.md`
- [x] 3.2 Requirement 3, regression corpus, entire: define the corpus entry (type, inputs, edition, outputs, verdict, `input_hash`, `engine_version`)
- [x] 3.3 Regression runner; tests: unchanged result passes, undeclared difference fails the build, declared difference passes
- [x] 3.4 (spec) Requirement 5, metric "traceability completeness": confirm the definition (NormRef is agreed): a step is verified when every `NormRef` in its `norm_refs` is verified, engineer-set sources are a separate count, and the count comes from the envelope's `unverified_step_count` (resolutions 3 and 5 in `calculation-core-contract` `design.md`)
- [x] 3.5 Implement the traceability metric and attach it to the GO report
- [x] 3.6 (spec) Remove the DRAFT markers from the requirement "Regression corpus", the metric, and the `development-process` delta; re-run `openspec validate --strict`

## 4. Shared files: agreed with Egor (applied 2026-10-20, `2863bc9`)

- [x] 4.1 (spec) Agree with Egor the changes to `.claude/agents/tester.md` (its GO rule, lines 16-19) and its Kilo mirror, the `test-process` skill, and the `development-process` delta in this change. Both agent files stay identical. Do not apply before Egor agrees (2026-10-11: Egor agreed to the delta and to the proposed GO and NO-GO lines and the step "attach the correctness metrics" as written; the pipeline computes nothing, so the gate does not apply to his zone; `docs/decisions/backend/2026-10-07-pipeline-branch-and-process-to-egor.md`, answer 9)
- [x] 4.2 (spec) Check that the `development-process` delta of this change and the `team-roles-update` delta do not contradict each other (2026-09-27: no contradiction. This change ADDS "Correctness gate for calculation changes"; `team-roles-update` MODIFIES "Non-overlapping developer responsibility zones", "Planning before implementation", "Review before merge", and "Go/No-Go verdict and archive" and ADDS "Shared decisions are tracked", so no requirement is touched by both. The correctness gate applies only to a change with calculation code, so it never meets the code-free GO path of `team-roles-update`; for a change with code it is an extra GO condition next to the coverage gate. The GO wording in `tester.md` must still list both gates when task 4.1 and `team-roles-update` Part B are applied)

## 5. Follow-up, not in this change

- Filling the reference examples (3 per calculation type, one task per type, with `tolerance` and `tolerance_kind`) from the methodical guide, by the engineer, after this change is applied.
- Former task 3.7 [blocked: typical calculation], moved here by Akim on 2026-10-20: test that a typical calculation completes in under 30 seconds (requirement "Calculation latency" of the `calculation-engine` delta), in the change that defines a typical calculation and where the time is measured. The requirement is archived with this change and has no test until then.
- The real regression corpus (added 2026-10-20 after the `tester` implementation verdict, finding 2): the stored frozen entries per calculation type, their parameter source, and the build step that recomputes them and reads the declared differences of `proposal.md` (design decision 18, open). Until then the requirement "Regression corpus" is held by the runner's tests on synthetic entries only.

## 6. Close

- [ ] 6.1 After 1.1-1.5 pass, confirm the final version of the change is on `develop`
- [ ] 6.2 `spec-keeper` syncs the deltas and archives the change after GO; the open items in section 3 must be done or moved to a follow-up change first

## Dependencies

- `retarget-mvp-domain` (WP1): the first domain and its calculation types.
- `calculation-core-contract` (WP2): section 3 and the dependency table in `design.md`.
- `bootstrap-dev-environment` (WP6, planned): test runner and property-test tool.
- Egor: section 4.

## DOR checklist

- [x] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes (task 1.1)
- [x] Functional requirements and scenarios recorded
- [x] Non-functional requirements recorded (`design.md`; accessibility marked not applicable)
- [x] Each task is small enough for one session
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Branches defined (above)
- [x] Dependencies satisfied: `calculation-core-contract` DOR (blocks section 3 only; met, section 3 done); Egor review (section 4, done 2026-10-11)

## DOD and Go / No-Go

- GO is declared only by the `tester` agent (`AGENTS.md` section 4).
- For the spec phase: `openspec validate --all --strict` passes; a `spec-reviewer`
  report on the current version of the change lists no blocker and no major finding
  (`openspec/specs/development-process/spec.md`, "Planning before implementation");
  `norm-traceability-checker` confirms no norm value or tolerance is fixed.
- For implementation: sections 2 and 3 pass with >= 95% branch
  coverage; the reference suite is within tolerance; metrics are attached; the delta specs
  match the implementation.
- NO-GO: validation fails; an unresolved blocker; a numeric tolerance, norm value, or
  clause number fixed in a spec; a reference output outside its tolerance; reproducibility
  below 100%; a test failure or coverage below 95%.
- Archive (6.2) happens only after GO.
