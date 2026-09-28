# `backend-layered-architecture` (WP5): spec-reviewer report, 2026-09-28

- Date: 2026-09-28
- Reviewer: `spec-reviewer` subagent, run by Akim as the first DOR step after moving
  WP5's lead to himself (see `backend-layered-architecture-lead-change.md`).
- Scope: the full change (`proposal.md`, `design.md`, `tasks.md`,
  `specs/backend-architecture/spec.md`), with findings split between sections 1-3/5-6
  (Akim's own zone, no outstanding Egor dependency claimed) and the already-known
  section 4/7/8/9 deferral (not re-flagged as new).

Russian version: `backend-layered-architecture-readiness-rus.md`.

## Verdict

**NOT READY** for DOR (as of this first pass). 5 blockers, 3 major, 3 minor findings.
Sections 1-3 are closest to ready (blocked only by change-level findings 4 and 6, plus
major 7 and minors 9-11); sections 5-6 have their own new blockers (1, 2, 3, 5), not
just the change-level ones. **Update, same day:** all 5 blockers and all 3 major
findings addressed — see "Next steps" below. A second `spec-reviewer` pass is still
needed to confirm READY.

## Blockers

1. **Spec delta contradicts `design.md`'s own settled decision 3 and tasks 5.1-5.2.**
   `specs/backend-architecture/spec.md:39-56` ("No hardcoding" scenario, "Parameters
   stored in YAML" requirement) still says normative coefficients/formulas are read
   "from configuration or a parameter file" / stored in `.yaml`. `design.md:47-56`
   (decision 3, settled 2026-09-27, closes task 9.5) and `tasks.md` 5.1-5.2 say the
   opposite: formulas/coefficients the norm gives come from `dec_normatives` through
   the parameters layer's `provenance` gate; `.yaml` holds only engineer-set values.
   The spec delta was never synced to the revised decision. Closes with an edit to
   `specs/backend-architecture/spec.md`'s two affected scenarios/requirements.

2. **Task 6.2 / `design.md` decision 7 contradict `calculation-core-contract`'s "Pure
   calculation function" requirement.** `tasks.md` 6.2 ("reference implementation
   reading parameters from the parameters layer") implies I/O inside the engine;
   `calculation-engine/spec.md` (in `calculation-core-contract`) requires each
   calculation type to be a pure function that does not read external state.
   `calculation-core-contract/design.md:209-215` already names this exact conflict and
   holds the (still open) sync task — its own `tasks.md` task 7.2 — to reword 6.2 and
   decision 7. That sync has not happened.

3. **Task 5.1 depends on an undisclosed cross-team/cross-change dependency.**
   `design.md:55-56` (end of decision 3): tasks 5.1-5.2 read from `dec_normatives`
   "once that reading path exists." That path depends on open task 9.3 (normative
   code location, pending Egor) and on `calculation-core-contract`'s own open task 7.2
   (provenance gate needs pipeline verification state that is not yet in place,
   `calculation-core-contract/design.md:271-276`). Task 5.1 sits in section 5 (claimed
   ready, no Egor dependency), but cannot be completed as scoped until 9.3 and
   `calculation-core-contract` 7.2 resolve. The `tasks.md` header (added 2026-09-28)
   did not disclose this.

4. **No DOR checklist and no DOD/Go-No-Go section in `tasks.md`.**
   `openspec/config.yaml` (`rules.tasks`) requires both; `AGENTS.md` sections 3-4
   require the same at the change level. **Closed by this session's edit to
   `tasks.md`, 2026-09-28** (the DOR checklist and DOD/Go-No-Go sections added there
   record this exact NOT READY status rather than asserting readiness).

5. **Tasks 5.2 and 6.2 name the placeholder domain, inside the non-deferred
   sections.** `tasks.md` 5.2 (`params/normatives/beam_deflection.yaml`) and 6.2
   (`engine/beam_deflection.py`), plus `design.md` decision 7. `retarget-mvp-domain`
   is active and already introduces `foundations-shallow`; `calculation-core-contract`
   already waits for it instead of using beam deflection. Sections 5-6 have not made
   the same switch, unlike task 4.2's identical issue, which is already covered by the
   section 4 deferral and not re-flagged here.

## Major

6. **`proposal.md` has no "Non-goals" section.** Required by `openspec/config.yaml`
   (`rules.proposal`). The content exists (`design.md`'s "Non-Goals" under
   Goals/Non-Goals) but not in the artifact the rule names.

7. **No per-task verification/acceptance clause on tasks 1.1, 1.2, 2.1, 2.2, 3.1, 3.2,
   5.1, 5.2, 6.1, 6.2.** None states what observable check marks it done, unlike
   `bootstrap-dev-environment`'s tasks (every one has a "verify: ..." clause). Real
   ambiguity in places: 2.1 doesn't name the env-var keys to test for; 3.2 doesn't say
   whether an actual Alembic migration is expected against the still-empty `models/`;
   6.1 doesn't say what methods the `Calculator` interface must expose.

8. **Task 2.1's env-var names are left open despite a sibling change already waiting
   on them.** `tasks.md` 2.1 only says "app DB URL, normative DB URL," no names fixed.
   `bootstrap-dev-environment` task 4.3 already picked interim names
   `DEC_APP_DATABASE_URL` / `DEC_NORMATIVES_DATABASE_URL`, explicitly "pending
   confirmation once task 2.1 lands." Not tracked anywhere in this change's own
   section 9.

## Minor

9. Task 1.2 doesn't specify the health endpoint's path or response shape.
10. Task 2.2 doesn't say what must exist in the `core/exceptions.py`/`core/logging.py`
    stubs.
11. No non-functional-requirements section in `design.md`/`spec.md` (coverage target,
    security, performance for full-text search), unlike `calculation-core-contract`'s
    explicit NFR section.

## Not re-flagged (already known, section 4/7/8/9 deferral)

- Task 4.2's beam-deflection/СП 16.13330 placeholder pilot file — same class of issue
  as blocker 5, but section 4 is already deferred pending task 9.3.
- Sections 4, 7, 8 and open items 9.3, 9.6, 9.7 staying unimplemented — by design, per
  `tasks.md`'s own section 9 rule.

## Next steps

**Update, 2026-09-28 (same day): all 5 blockers and all 3 major findings addressed.**

- Blocker 4: closed — `tasks.md` DOR checklist, DOD/Go-No-Go, and Dependencies
  sections added.
- Blocker 1: closed — `specs/backend-architecture/spec.md`'s "No hardcoding" and
  "Parameters stored in YAML" reworded to match `design.md` decision 3.
- Blocker 2: closed — `tasks.md` task 6.2 and `design.md` decision 7 reworded to
  describe the engine as a pure function receiving resolved parameters as typed
  arguments; this is the WP5 side of `calculation-core-contract` task 7.2's sync
  request.
- Blocker 3: disclosure closed, dependency itself still open — task 5.1 now carries
  `[blocked: 9.3, calculation-core-contract 7.2]` and the `tasks.md` "Dependencies"
  section names it explicitly. The underlying wait on task 9.3 (Egor) and
  `calculation-core-contract` 7.2 (which itself still has an open sub-item: safe
  parsing of `expression`, and pipeline verification state per question 12) is not
  resolved by this edit and does not need to be — same as WP6's own `[blocked: WP5]`
  tasks, an explicitly named and tracked dependency does not block this change's own
  GO.
- Blocker 5: closed — tasks 5.2 and 6.2 no longer name `beam_deflection`; both now say
  "once WP1 names one," matching `calculation-core-contract` task 7.1's own wait on
  `foundations-shallow`'s still-`TBD` in-scope list.
- Major 6: closed — `proposal.md` gained a "Non-goals" section.
- Major 7: closed — tasks 1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 5.1, 5.2, 6.1, 6.2 each now
  have a "verify" clause.
- Major 8: closed — task 2.1 now names `DEC_APP_DATABASE_URL` and
  `DEC_NORMATIVES_DATABASE_URL`, confirming `bootstrap-dev-environment` task 4.3's
  interim choice.
- Minor 9, 10: closed as part of major 7's verify clauses (task 1.2 now specifies
  `GET /health` → `{"status": "ok"}`; task 2.2 now specifies `DECError` and one stdlib
  logger).
- Minor 11: closed — `design.md` gained a "Non-functional requirements" section.
- **Not yet done:** a second `spec-reviewer` pass on the current text, to confirm
  these fixes actually resolve the findings rather than relying on self-assessment.
  Until that pass reports no blocker/major, the DOR checklist item and the DOD spec-
  phase item in `tasks.md` stay unchecked.

## Second pass, 2026-09-28

- Reviewer: `spec-reviewer` subagent, run by Akim on the text after the first-pass fixes.
  Read-only; `openspec validate` was run by the caller separately.
- Verdict: **NOT READY** for DOR. 0 blockers, 7 major (N1-N7), 7 minor (N8-N14).

### First-pass items, re-checked

| # | Finding | Status |
|---|---|---|
| 1 | Spec delta vs decision 3 (YAML vs `dec_normatives`) | Partially resolved: `spec.md`, `tasks.md` fixed; `proposal.md` still said "parameters in `.yaml`" (N1) |
| 2 | Task 6.2 / decision 7 vs pure-function requirement | Resolved |
| 3 | Task 5.1 undisclosed dependency | Partially resolved: disclosed, but the chain is incomplete (5.1 also waits on WP1 transitively; N4, N5) |
| 4 | No DOR/DOD in `tasks.md` | Resolved, with defects: no security item in DOD, DOR dependency item reworded (N4) |
| 5 | Placeholder domain in 5.2, 6.2, decision 7 | Resolved |
| 6 | No Non-goals in `proposal.md` | Resolved on form, content contradicts `AGENTS.md` (N2) |
| 7 | No verify clauses | Mostly resolved; 3.1/3.2 need a `dec_app` database (N3), 5.2 needs blocked 5.1 (N5) |
| 8 | Env-var names | Resolved (relation to `DEC_DATABASE_URL` still unstated, N8) |
| 9, 10 | Health endpoint, stubs | Resolved |
| 11 | NFRs | Resolved in `design.md` |

### New findings

**Major**

- **N1.** `proposal.md` (What Changes, Capabilities) still said normative parameters live
  in `.yaml`, contradicting decision 3. **Closed 2026-09-28** (reworded to engineer-set
  values only).
- **N2.** The Non-goals text ("no automated NLP/RAG parsing of norms yet, manual ingestion
  for the MVP") in `proposal.md` and `design.md` contradicts `AGENTS.md` section 1, where
  NLP/RAG auto-parsing is part of the MVP. Entangled with open item 9.3. **Open.**
  Options: reword to what this change does not build (the backend adds no parsing
  pipeline; `normatives_pipeline/` owns it), or record a PM decision that changes scope.
- **N3.** Tasks 3.1 and 3.2 verify against a running `dec_app` database. Today only `dec`
  on port 5433 exists in `docker-compose.yml`, which is Egor's zone (tasks 8.1, 9.6). The
  header says section 3 needs no Egor agreement. **Open.**
- **N4.** Go/No-Go of the whole change is unclear: `AGENTS.md` section 4 wants all tasks
  checked, while sections 4, 7, 8 and task 5.1 stay open. The DOR dependency item was
  reworded to "or explicitly named as not blocking", and the DOD lacks the security item.
  **Open.** Options: split sections 4, 7, 8 (and 5.1) into a follow-up change, as
  `bootstrap-dev-environment` does, or state how the change reaches GO and archive.
- **N5.** Tasks 5.2 and 6.2 are implicitly blocked by WP1 (the `foundations-shallow` list
  is `TBD`), and 5.2's verify needs `param_schemas.py` from blocked 5.1. Only 5.1 carries a
  marker. **Open.**
- **N6.** The spec delta had no requirements for `GET /health`, fail-fast configuration,
  the `DECError` hierarchy, or the calculator registry. **Closed 2026-09-28** (four
  requirements with scenarios added; tasks 1.2, 2.1, 2.2, 6.1 aligned).
- **N7.** The dependency direction had no total order (where `schemas`, `core`, `db`,
  `worker` sit; what stops `engine` importing `services`), so it could not become an
  `import-linter` contract (`bootstrap-dev-environment` task 5.1). **Closed 2026-09-28**
  (ordered layer list plus two forbidden-import rules in `design.md` decision 2 and the
  spec).

**Minor**

- **N8.** The relation between `DEC_DATABASE_URL` (Egor) and
  `DEC_NORMATIVES_DATABASE_URL` is unstated; requiring both at start-up forces the
  normatives URL on sections 1-3 tests. **Open.**
- **N9.** Wording and testability gaps: `Calculator` as class or callable; "no I/O-performing
  import" in task 6.2 needs a named check; task 5.1 bundles three deliverables. **Open.**
- **N10.** Stale text in `tasks.md` (duplicate second-pass bullet, an unsupported
  "confirmed, readiness doc" claim). **Closed 2026-09-28.**
- **N11.** The spec delta listed ten layers, the other artifacts eleven (`worker`).
  **Closed 2026-09-28.**
- **N12.** Overlap with `normatives-catalog` main spec (full-text search, document
  storage, manual maintenance); NFRs only in `design.md`. **Open.**
- **N13.** The spec delta does not mark deferred areas (9.3, 9.6, 9.7) as open. **Open.**
- **N14.** Sections 4, 7, 8, 9 carry no per-task zone sub-branch (deferral is disclosed).
  **Open.**

### Next steps

- Still open before READY: N2, N3, N4, N5 (major), N8, N9, N12-N14 (minor). N4 decides the
  shape of the rest (follow-up change or not).
- A third `spec-reviewer` pass is needed after those close. The DOR and DOD spec-phase
  items in `tasks.md` stay unchecked until it reports no blocker and no major finding.

### Update after the split, 2026-09-28

WP5 was split (`backend-layered-architecture-split-egor.md`): sections 4, 7, 8, task 5.1's
`dec_normatives` half, items 9.3, 9.6, 9.7 and the pilot tasks 5.2, 6.2 moved out.

- **N2:** closed by the split (the non-goal now says this change builds no normative
  database, ingestion or parsing; the pipeline owns parsing).
- **N4:** closed (all remaining tasks are executable; DOR dependency item restored to the
  `AGENTS.md` wording; security item added to the DOD). Egor's acknowledgement of the split
  is requested, not yet given.
- **N5:** closed (5.2 and 6.2 moved to `calculation-core-contract` task 7.1; 5.1 no longer
  depends on blocked work).
- **N3:** addressed (verify clauses of 3.x run on a hand-made `dec_app` on the existing
  `dec-postgres`; nothing in `docker-compose.yml` is touched).
- **N9:** partly closed (5.1 no longer bundles the `provenance` gate; the `Calculator`
  class-or-callable wording and the named I/O-import check remain; the check moved with 6.2
  to task 7.1 of `calculation-core-contract`).
- **N12, N13, N14:** mostly moot for this change: the overlapping and deferred
  requirements left with the moved sections. Not re-verified.
- **Still open:** N8 (`DEC_DATABASE_URL` vs `DEC_NORMATIVES_DATABASE_URL`).

A third `spec-reviewer` pass is needed on the split text before READY.

## Third pass, 2026-09-28

- Reviewer: `spec-reviewer` subagent, run by Akim on the split text. Read-only;
  `import-linter` was not run against the proposed contract.
- Verdict: **NOT READY** for DOR. 0 blockers, 3 major (M1-M3), 15 minor (m1-m15).
- Status of N1-N14: resolved N1, N2, N4, N6, N10, N11, N13; partly N3, N5, N7, N9, N12,
  N14; open N8.

**Major**

- **M1.** The spec's dependency-direction, layer-mixing and hardcoding requirements had
  no task or verify, so the DOR claim "the delta covers exactly tasks 1.1-6.1" was false;
  the `import-linter` task (`bootstrap-dev-environment` 5.1) had no forbidden contracts
  and the `ml/` rule. **Addressed:** `tasks.md` has a "Requirement coverage" table; the
  DOR line is corrected; WP6 task 5.1 and its spec gained the forbidden contracts,
  `allow_indirect_imports` for the `api` rule, and the `ml/` rule.
- **M2.** The order forbade `engine` from importing the typed parameter and envelope types
  the tasks said it receives. **Addressed:** shared typed values live in `schemas`;
  `Calculator` is generic over them; `param_schemas.py` holds only the YAML file schema.
- **M3.** Dependency direction and registry ownership between WP5 and
  `calculation-core-contract` were unstated; WP2 task 7.2 and text in its `design.md` and
  `proposal.md` were stale. **Addressed:** order stated in both Dependencies sections
  (WP5 applies first); WP5 6.1 owns the registry, WP2 2.1 and 4.3 extend it; 7.2, the
  design bullet and the B5 line refreshed.

**Minor, addressed in this pass:** m1 (same-package and third-party imports, `db` clause
moved to review), m2 (`Base` in `models`, Alembic tree at `backend/alembic/`), m3
(decision 4 marked), m6/N8 (`DEC_NORMATIVES_DATABASE_URL` optional until
`normative-catalog-backend`; relation to `DEC_DATABASE_URL` stated), m9 (requirement
phrasing, `DECError` scope, named variable), m10 (secrets and coverage requirements in the
spec, `repr` test, accessibility N/A), m11 (name-to-file mapping, params root argument,
`engineer` and `rationale` required), m12 (task 1.3 adds runtime dependencies), m13 (`ml/`
rule in both directions), m4 in part (URL, teardown, fresh database, initial revision
check).

**Minor, left open:** m5 (`reporting` and `worker` have no task), m14 (size judgement is
Akim's own), m15 (Egor's acknowledgement is now stated as needed before spec-phase GO).
m7 and m8 (stale text in files this change does not own) are listed in `tasks.md`,
"Follow-ups outside this change". The norm-method-bounds gap (m11) is recorded there too.

A fourth `spec-reviewer` pass is needed before READY.
