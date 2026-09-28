# Proposal

## Why

The only quality gate in the project is branch coverage. Coverage shows that code ran,
not that the result is right:

- **A3 (High):** "99.9% accuracy" (`calculation-engine/spec.md:54-60`) names no quantity,
  no reference, and no population, so it cannot be measured. The audit's "<= 0.1%" was
  invented and is not adopted; tolerances come from the engineer or the norm.
- **A4 + C9 (High):** branch coverage is the only gate
  (`development-process/spec.md:81-87`, `.claude/agents/tester.md:16-19`). No spec,
  agent, or skill mentions reference examples, regression tests, or property tests.
- **E1 (High):** every measurable target in the specs is a latency, apart from one
  unmeasurable accuracy claim and one coverage figure. Accuracy, the only target that
  says whether an engineering result is right, is the one that cannot be measured.

## What Changes

- New capability `calculation-verification` with four requirements: reference examples,
  regression corpus, invariant tests, and metrics per run. They keep the roadmap numbers
  1, 3, 4, and 5; roadmap requirement 2 (accuracy and latency) lives in
  `calculation-engine`, see below.
- `calculation-engine`: the requirement "Non-functional — performance and accuracy" is
  replaced by "Calculation accuracy", which states accuracy as deviation from named reference
  examples. The 30-second latency target becomes its own requirement, "Calculation
  latency".
- `development-process`: one new requirement adds the correctness gate for calculation
  changes to the GO rule. Existing requirements are not rewritten. **Needs Egor review**
  (shared file).

## Dependencies

`calculation-core-contract` (WP2) is the source of the result envelope and of `NormRef`.
`NormRef` is agreed with Egor: first on Akim's word (2026-09-26), then in Egor's own
words in `docs/decisions/normref-questions-egor.md` (commit `a1a896c`, 2026-09-27). Two parts of this change use it: requirement 3 (regression corpus,
which compares result envelopes) and the metric "traceability completeness". The
meaning of "verified" is the field `status` of `NormRef`; the wider rule sits in the
requirement "Norm reference status" of `retarget-mvp-domain` (draft, unarchived).
Soft dependencies on `calculation-core-contract` are listed in `design.md`. The latency
requirement waits for a definition of "typical calculation". `tasks.md` marks it.

## Non-goals

- Fixing any numeric tolerance. The spec defines the field; the engineer sets the value
  per quantity when filling a concrete reference example.
- Filling the reference examples. Real numeric references from the methodical guide are
  prepared separately, after this change is applied.
- Inventing engineering invariants for shallow foundations. The spec defines the
  structure; the engineer confirms the list.
- Fixing any norm value, coefficient, limit, edition, or clause number.
- Reference examples, sources, or invariants for internal water supply (the second
  domain); it needs its own decision (see `design.md`).
- Finalizing `NormRef`, the result envelope, or `input_hash`; those belong to
  `calculation-core-contract`.
- Choosing the property-testing tool and the test runner setup (planned change
  `bootstrap-dev-environment`).
- Editing `tester.md` or `openspec/specs/` directly.

## Capabilities

### New Capabilities

- `calculation-verification`

### Modified Capabilities

- `calculation-engine`: accuracy requirement replaced; latency requirement
  added.
- `development-process`: correctness gate for calculation changes (new requirement;
  needs Egor review).

## Impact

- Affects three specs after archive. No code, no migrations.
- Depends on `retarget-mvp-domain` (WP1) for the first domain (`foundations-shallow`) and
  its list of calculation types.
- Depends on `calculation-core-contract` (WP2) for the
  result envelope; see `design.md` for the list to re-check after its DOR.
- Shared files: `.claude/agents/tester.md`, the `test-process` skill, and
  `development-process` are shared with Egor. None is edited here; see `tasks.md`.
- `team-roles-update` also modifies `development-process` (requirement "Go/No-Go verdict
  and archive"). This change adds a new requirement and does not touch that one.
