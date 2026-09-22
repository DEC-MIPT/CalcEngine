# DEC — Verified Findings and Roadmap (Audit Step 3)

- Date: 2026-09-23
- Branch: `Specs-onboarding` (HEAD `6e0f84b`), working tree clean
- Input: `docs/audit/02-findings.md`, read for the first time in this step and checked
  against the files. The reviewer did not take part in writing it.
- Method: each finding checked below was re-read in the cited file, and the evidence
  was looked for independently. A keyword sweep over `openspec/` (soil, groundwater,
  settlement, bearing capacity, diameter, velocity, head loss, disclaimer, unit,
  rounding, tolerance, monolith) returned 0 hits. `ls` confirms that `LICENSE`, `adr/`
  and `.env.example` do not exist.
- Scope: all 4 Critical, all 17 High, and 14 of 16 Medium findings (35 in total). Not
  checked: D1 and E4 (improvements; for D1, only the missing `LICENSE`/`adr/` was
  confirmed with `ls`).
- This file cites no clause of any SP or GOST. Every norm edition named in the
  repository stays `unverified` (`agent-docs/domain-constraints.md:27-28`).
- Where this file lives: `docs/` is gitignored (`.gitignore:2`), so this file is not
  tracked and colleagues cannot see it unless it is shared. See D2 and section 5.

---

## 1. Verification table

Verdicts: **confirmed** — the claim holds as written. **partially** — the core gap is
real, but part of the claim or its severity does not hold. **not confirmed** — the
claim is wrong. **needs data** — the files cannot settle it.

Result: 27 confirmed, 7 partially, 1 needs data, 0 not confirmed as whole findings.
Five sub-claims are rejected (1.2). Four findings duplicate others and are merged: D3
into A1, C7 and C8 into A2, C9 into A4.

### 1.1 Findings

| ID | Audit sev. | Verdict | Reviewed sev. | Reason | Evidence (re-checked) |
|---|---|---|---|---|---|
| A1 | Critical | confirmed | Critical | The placeholder domain goes further than the audit reports: it also appears in an engine scenario, a catalog scenario and the engine design. D3 is the same issue and is merged here. | `product-vision/spec.md:37-45`; `config.yaml:21-23`; `backend-layered-architecture/tasks.md:21,27,32`; also `calculation-engine/spec.md:15-18`, `normatives-catalog/spec.md:33`, `design.md:62-63` |
| A2 | Critical | confirmed | Critical | No requirement, scope or out-of-scope statement exists for either MVP domain. C7 and C8 are sub-lists of this gap and are merged here. | keyword sweep over `openspec/**`: 0 hits |
| C1 | Critical | partially | High | Real gaps: no document status model, no rule that pins a stored result to the edition it used, no policy for superseded editions. The audit misses that a `Revision` entity is already planned and that "current revision" is already specified. In the MVP each norm has one edition, so no wrong result can come from a superseded edition before the defense. The risk is a data-model retrofit, so the severity is High. | `normatives-catalog/spec.md:33-35,37-43`; `backend-architecture/spec.md:58-60`; `tasks.md:20`; `domain-constraints.md:14-15` |
| C2 | Critical | partially | Critical | No requirement makes the engine act on applicability rules or on a breach of them. The audit misses `security/spec.md:14-15`: the API already rejects out-of-range input, but only as schema validation. That check does not tie to the method, does not name the violated bound or clause, and has no warning band. The severity stays Critical because silent extrapolation gives a wrong engineering result, and the fix is cheap. | `normatives-catalog/spec.md:13`; `calculation-engine/spec.md:28-34`; `security/spec.md:13-15` |
| A3 | High | confirmed | High | "99.9% accuracy" names no quantity, reference, or population. Do **not** adopt the audit's "≤ 0.1%": the audit invented that number. Tolerances come from the engineer or the norm. | `calculation-engine/spec.md:54-60` |
| A4 | High | confirmed | High | Branch coverage is the only gate anywhere, and no agent or skill mentions reference examples, regression or property tests. The citation `tester.md:84-87` is wrong: the file has 29 lines, and the gate is at `:16-19`. C9 is merged here. | `development-process/spec.md:81-87`; `AGENTS.md:88,97,150`; `.claude/agents/tester.md:16-19`; grep over `.claude/skills`, `.kilo`, `.kilocode`: 0 hits |
| A5 | High | confirmed | High | The domain rules live in a file that calls itself interim. Agents read it through `CLAUDE.md:8`, but the DOR, the DOD and `openspec validate` never do. | `agent-docs/domain-constraints.md:5-6`; nothing equivalent in `openspec/specs/**` |
| A6 | High | confirmed | High | `proposal.md` has no Non-goals section (Non-goals appear in `design.md:19-22`). `tasks.md` has no zone sub-branches, no DOR and no DOD. The delta spec has no non-functional requirement. | `config.yaml:43,46,51,52`; `proposal.md:1-40`; `tasks.md:1-42`; `backend-architecture/spec.md` |
| B1 | High | partially | Medium | The layers are purely technical: fact. That the two domains "will interleave" is a forecast labelled as fact. `Calculator` plus `engine/registry.py` already give a per-calculation seam. The MVP builds one domain first, so the risk comes later. It is still cheap to add domain subpackages now. | `backend-architecture/spec.md:10-19`; `design.md:26-32,62-63`; `tasks.md:31` |
| B2 | High | confirmed | High | No requirement gives a YAML parameter its clause and edition, so nothing connects the value used to the reference that the report must print. | `design.md:39-43,72-74`; `backend-architecture/spec.md:48-55`; `report-generator/spec.md:43-49` |
| B3 | High | partially | Medium | True: a foreign key cannot cross two databases. But in the MVP calculations read `params/`, not `dec_normatives`, so a foreign key to `dec_normatives` would not help. The audit's proposal (one database, **one Alembic tree**) also conflicts with the non-overlapping zones rule: the two-database split maps to Akim's and Egor's zones. Minimal fix: store the edition pin as denormalized columns in `dec_app`, and record the rationale for the split. | `design.md:45-50,72-74`; `AGENTS.md:108-110` |
| C3 | High | confirmed | High | No spec mentions units, conversion, rounding or tolerance. Drop the BLAS hypothesis: the MVP formulas are scalar. | sweep: 0 hits; `domain-constraints.md:16-19` |
| C4 | High | confirmed | High | No disclaimer and no statement of engineer responsibility. New: the spec contradicts itself, because the requirement calls the signature fields optional while its scenario requires them. Whether signatures are mandatory has to be checked in the text of GOST R 21.101. | `report-generator/spec.md:18-27` (`:22` vs `:26-27`); sweep: 0 hits |
| C5 | High | confirmed | High | No file addresses the legal status of storing normative texts, and the project has no LICENSE. The legal answer itself needs data (from the PM). | `backend-architecture/spec.md:57-65`; `tasks.md:21`; `ls` |
| C6 | High | confirmed | Medium | The example clause violates the project's own citation rule. The fix is small and the damage is limited, so the severity is Medium. | `transparent-output/spec.md:15-17`; `domain-constraints.md:23-28`; `report-generator/spec.md:12` |
| C7 | High | confirmed (dup of A2) | — | merged into A2 | sweep: 0 hits |
| C8 | High | confirmed (dup of A2) | — | merged into A2. The hypothesis "water supply first" needs data: the engineer decides. | sweep: 0 hits |
| C9 | High | confirmed (dup of A4) | — | merged into A4 | — |
| E1 | High | confirmed | High | Every measurable target is a latency, apart from one unmeasurable accuracy claim and one coverage figure. | `calculation-engine/spec.md:54-60`; `normatives-catalog/spec.md:53-59`; `report-generator/spec.md:51-56`; `web-platform/spec.md:43-49` |
| E2 | High | partially | Medium | No `adr/` exists: fact. "Rationale disappears into the archive" is wrong: archived changes stay tracked in `openspec/changes/archive/`. The real gap is that cross-cutting decisions have no index. | `CLAUDE.md:47`; `openspec/changes/archive/.gitkeep` |
| E3 | High | needs data | — | The scope facts hold. Whether the scope fits 38 weeks depends on team capacity, which is not in the repository. | `01-recon.md:98-101` |
| A7 | Medium | confirmed | Medium | The requirement appears in a third place, `user-accounts:10-17`. `user-accounts:39` already defers to web-platform, the opposite of the owner the audit proposes. | `web-platform/spec.md:27-33`; `user-accounts/spec.md:10-17,37-43` |
| A8 | Medium | confirmed | Low | A main spec references a capability that exists only in an unarchived change. | `normatives-catalog/spec.md:6-7` |
| A9 | Medium | confirmed | Medium | The "100 calculations/month" limit is attributed to product-vision, which states no limits. | `user-accounts/spec.md:20-23`; `product-vision/spec.md:29-35`; `AGENTS.md:27` |
| A10 | Medium | confirmed | Medium | No authorization between users or organizations, no audit trail, no retention rule, no personal-data requirement. For the MVP, only the "a user cannot read another user's calculation" rule is needed; the rest can be recorded as non-goals. | `security/spec.md:1-47` |
| A11 | Medium | confirmed | High | The trace has no schema, and the engine, UI and report each describe it from their own side. It is the contract between all three of Akim's components and the only route a clause reference can travel. | `calculation-engine/spec.md:20-27,44-52`; `transparent-output/spec.md:10-17`; `report-generator/spec.md:43-49` |
| A12 | Medium | partially | Medium | `worker` has no requirement: confirmed. "30 s vs sub-second" is not a contradiction: `web-platform:43-49` is about handing data between components, not about calculation time. Whether the MVP calculation is synchronous is still undecided. | `proposal.md:21`; `design.md:29-30`; `tasks.md:5`; `backend-architecture/spec.md:10-13` |
| B4 | Medium | confirmed | Medium | A SHALL that code review enforces is untestable. Small inaccuracy: `engine`, `parameters` and `reporting` are ranked (below `services`); only `schemas`, `core`, `db` and `worker` are not. | `backend-architecture/spec.md:21-29`; `design.md:34-36` |
| B5 | Medium | confirmed | Medium | The wording of task 6.2 implies I/O inside the engine, which contradicts the design. | `tasks.md:32` vs `design.md:39-41`, `backend-architecture/spec.md:52-55` |
| B6 | Medium | partially | Low | The provenance gap is real, but the MVP already requires manual entry, so the risk starts after the MVP. It is cheap to close inside `norm-source-traceability`. | `.claude/agents/data-engineer.md:15-17`; `product-vision/spec.md:49-50`; `normatives-catalog/spec.md:45-51` |
| C10 | Medium | confirmed | Medium | The team intends one declarative input model (`01-recon.md:97`), and no spec contains it. | `security/spec.md:9-15`; `web-platform/spec.md:19-25` |
| D2 | Medium | confirmed | Medium | The "passport" is cited as rationale but is untracked. The same applies to all the audit reports, this one included. | `.gitignore:1-2`; `proposal.md:6`; `design.md:5,20,55,64` |
| D3 | Medium | confirmed (dup of A1) | — | merged into A1 | `config.yaml:21-23` |
| D8 | Medium | confirmed | Medium | The documents model two people, and the team has three. Changes without code have no GO path. `config.yaml:31` also says "two developers". | `AGENTS.md:97,104`; `config.yaml:31`; `record-installed-skills-akim/tasks.md:13-15` |
| E5 | Medium | confirmed | Medium | Both active changes are process changes, and the skills change is blocked on an acknowledgement and a GO rule. That the priority order is wrong is the auditor's opinion, and this reviewer shares it. | `openspec/changes/`; `record-installed-skills-akim/tasks.md:13-15` |

### 1.2 Sub-claims rejected

1. **A3**, the tolerance "≤ 0.1%": the audit made it up. Do not copy it into a spec.
2. **B3**, "one database, one Alembic tree": this would create a migration tree shared
   between two zones, which `AGENTS.md:108-110` forbids. Keep the split, and pin the
   edition with denormalized columns.
3. **A12**, "30 s vs sub-second transitions": the two requirements measure different
   things.
4. **E2**, "rationale disappears into the archive": archived changes stay in the
   repository.
5. **C3**, the BLAS determinism hypothesis: it does not apply to scalar formulas.

---

## 2. Work packages

| WP | Name | Findings | Owner | Depends on |
|---|---|---|---|---|
| WP1 | Spec stabilization and domain retarget | A1 (+D3), A2 (scope and out-of-scope only; +C7, C8), A7, A8, A9, C6, E3 (non-goals), contradictions 2–3 recorded as non-goals | DE leads the specs; Akim co-writes the engine-facing scenarios; PM decides scope | Team decision on the first domain |
| WP2 | Calculation-core contract | A11, A5 (engine half), C3, C2, C4, C10, B5 | Akim | WP1 (domain name only); `NormRef` shape agreed with DE |
| WP3 | Normative-data model | C1, B2, B6, B3 (edition pin), C5 (legal gate), A5 (catalog half) | DE; Akim reviews the consumer side | `NormRef` shape; PM's legal answer for C5 |
| WP4 | Verification strategy | A3, A4 (+C9), E1 | Akim; reference examples from an engineer (source: needs data) | WP1 (first domain), WP2 (trace and envelope) |
| WP5 | Architecture baseline revision | A6, A12, B1, B4, B5 | Akim (backend layout); DE (`normatives/`, `ml/`, compose tasks) | WP1, WP3 |
| WP6 | Dev environment bootstrap | B4 (tooling), D4, D5, contradiction 12 (`mypy` vs `ty`) | Split: Akim owns backend and frontend tooling; Egor owns Docker and CI. The audit's "me" breaks the zone table (DevOps is Egor's zone). | WP5 (the import contract) |
| WP7 | Process and team | D8, A13, E5, D2 | Together (`AGENTS.md` and the agents are shared files) | none |

Deferred and recorded as non-goals in WP1, with no change now: A10 beyond the rule
that a user cannot read another user's calculation; billing integration
(contradiction 2); cloud deployment specifics (contradiction 3); ADR backfill beyond
the decisions WP3 and WP5 need; glossary (D1); audit file renumbering (D7).

---

## 3. Proposed OpenSpec changes

One change per package. Nothing is created in this step. No requirement below fixes
a norm value: tolerances, bounds and rounding rules are data fields that the
engineer fills from a primary source.

**Shared interface** between WP2 and WP3, to be agreed before either change is
written:
`NormRef {document, edition, clause, status, provenance}`. `edition` and `clause` may
be `unverified`, and no field may be null.

### 3.1 `retarget-mvp-domain` (WP1)

- **Goal:** point every spec and the AI context at the confirmed MVP domain, and fix
  the scope in writing.
- **Capabilities:**
  - MODIFIED: `product-vision`, `calculation-engine` (scenario), `normatives-catalog`
    (purpose, scenario), `transparent-output` (example), `web-platform`,
    `user-accounts`.
  - ADDED: one capability for the first domain (`foundations-shallow` or
    `water-supply-internal`), holding the scope requirements only.
  - Outside capabilities: `openspec/config.yaml` context.
- **Key requirements:**
  1. MVP scope names both domains and their order. *WHEN the MVP is delivered THEN the
     first domain's calculation types run end-to-end; the second domain follows at a
     named milestone.*
  2. Explicit out-of-scope list for the first domain. *WHEN a user asks for a case on
     the list THEN the system refuses and names the limit.*
  3. Non-goals before the defense (billing integration, NLP in the product, PDF,
     multi-tenant audit trail, and others; the PM approves the list). *WHEN a proposal
     touches a non-goal THEN product-vision is amended first.*
  4. A norm reference in a spec is either verified against the source text or marked
     `source: unverified`. *WHEN a spec gives an example reference THEN it uses a
     synthetic placeholder.*
  5. One owner per requirement: authorization lives in `user-accounts`, and the B2C
     limit lives in exactly one spec. *WHEN two specs state the same rule THEN one of
     them only references it.*
- **Ready when:**
  - `grep -ri "beam\|16\.13330" openspec/ --exclude-dir=archive` returns 0 hits.
  - `openspec validate --all --strict` passes.
  - `spec-reviewer` reports no blockers.
  - The PM has approved the non-goals list and the B2C limit.
- **Owner:** DE (lead), Akim (co-author), PM (approves scope).

### 3.2 `calculation-core-contract` (WP2)

- **Goal:** a contract for the engine that is independent of the domain, which the UI
  and the report consume. This is where "white box" becomes testable.
- **Capabilities:** MODIFIED `calculation-engine`, `transparent-output`,
  `report-generator`.
- **Key requirements:**
  1. **Pure calculation.** A calculation function takes typed inputs and resolved
     parameters and returns a result envelope, with no I/O. *WHEN the function runs
     with the filesystem and the network patched to fail THEN it completes, and the
     same inputs give the same envelope.*
  2. **Typed trace step.** Each step carries `{step_id, expression (renderable),
     substitutions with units, result with unit, norm_ref}`. *WHEN a calculation
     completes THEN every step has these fields; a step without a verified `norm_ref`
     is marked and counted.*
  3. **Explicit units.** Units are carried everywhere and converted only at the
     boundary. Each output quantity declares its rounding rule and that rule's source.
     *WHEN an input arrives in a non-base unit THEN it is converted at the boundary,
     and the trace shows the base unit.*
  4. **Applicability check with three outcomes.**
     - *WHEN an input is inside the method's range THEN the calculation runs.*
     - *WHEN an input is outside the method's range THEN the calculation is refused,
       naming the bound and its `norm_ref`.*
     - *WHEN an input is inside the method's range but outside the validated envelope
       THEN the calculation runs, and a warning is carried into the UI and the
       report.*
  5. **Result envelope and accountability.** The envelope carries `result_id`, engine
     version, input hash, the `norm_ref`s used, the verdict and the warnings. The
     report prints all of them, plus a statement that the engineer is responsible for
     the result. *WHEN a report is generated THEN these fields appear on it.* Whether
     signatures are mandatory is left to be checked against GOST R 21.101, which is
     `unverified`.
- **Design note (C10):** the input schema of each calculation type is the single
  source for API and form validation; the generation mechanism is decided in
  `design.md`.
- **Ready when:**
  - `NormRef` is agreed with DE.
  - Validate passes, and `spec-reviewer` reports no blockers.
  - `norm-traceability-checker` confirms that no requirement fixes a norm value.
- **Owner:** Akim; DE reviews `NormRef`.

### 3.3 `norm-source-traceability` (WP3)

- **Goal:** every normative value that a calculation uses carries its source and
  edition, and every stored result stays pinned to what it used.
- **Capabilities:**
  - MODIFIED: `normatives-catalog` (the actuality requirement becomes a status model).
  - ADDED: requirements for provenance and pinning.
  - Moves the catalog half of `agent-docs/domain-constraints.md` into the spec.
- **Key requirements:**
  1. Every normative parameter entry, in `params/` or in the database, carries a
     `NormRef`. *WHEN a parameter file entry has no source THEN schema validation
     fails.*
  2. Document status is one of in force, superseded or withdrawn, and only a
     maintainer changes it. *WHEN a bound edition becomes superseded THEN the
     calculation types that use it show a warning.*
  3. A stored result is pinned to `{document, edition, clause set}` for good, using
     denormalized columns in `dec_app` (B3). It is never recomputed silently. *WHEN an
     edition is superseded THEN old results keep their values and show a flag.*
  4. **Provenance.** A value is either `human-verified` or `machine-extracted`, and
     the engine accepts only `human-verified`. *WHEN the parameters layer loads a
     machine-extracted value THEN it rejects the value.*
  5. The system stores only the kinds of normative content that the recorded legal
     decision permits: a reference, a paraphrase, or the full text (C5). *WHEN a
     loader ingests a source THEN it stores only the permitted fields.* If the PM has
     no answer yet, this requirement is explicitly deferred.
- **Ready when:**
  - The C5 answer is recorded, or requirement 5 is deferred.
  - `NormRef` is agreed.
  - Validate passes, and `norm-traceability-checker` passes on this change.
- **Owner:** DE; Akim reviews requirements 1 and 3.

### 3.4 `calculation-verification` (WP4)

- **Goal:** a gate on correctness, not only on coverage.
- **Capabilities:**
  - ADDED: `calculation-verification`.
  - MODIFIED: `calculation-engine` (replaces the accuracy requirement) and
    `development-process` (the GO rule for calculation changes).
- **Key requirements:**
  1. Each calculation type ships at least N reference examples (N is agreed; the
     audit suggests 3). Each example names its origin (manual calculation, textbook,
     or norm annex) and a tolerance per quantity, which the engineer sets. *WHEN the
     reference suite runs THEN every quantity is within its tolerance, or the verdict
     is NO-GO.*
  2. "99.9% accuracy" is replaced by requirement 1, and the 30 s latency target
     becomes a separate requirement. *WHEN accuracy is claimed THEN it is stated as
     deviation from the named references.*
  3. **Regression corpus.** A frozen set of `(inputs, edition) → outputs` re-runs on
     every change. *WHEN an output differs THEN the build fails, unless the change
     declares the difference.*
  4. **Invariant tests.** Each calculation type lists invariants that hold whatever
     the norm says (determinism, consistency under unit scaling, and others the
     engineer confirms), and each has a property test. *WHEN inputs are generated at
     random within the valid range THEN every invariant holds.*
  5. **Metrics per run:** deviation from the references, traceability completeness
     (the share of steps with a verified `NormRef`), and reproducibility rate. *WHEN
     the tester reports GO THEN the three metrics are attached.*
- **Ready when:**
  - The first domain is chosen, and at least one source of reference examples is
    named.
  - The changes to `tester` and `test-process` are agreed with DE, because those are
    shared files.
- **Owner:** Akim. The reference examples need an engineer; who that is needs data.

### 3.5 `backend-layered-architecture` (WP5): update the existing change, do not create a new one

- **Goal:** make the active change consistent with WP1–WP3 and able to pass the DOR.
- **Capabilities:** `backend-architecture` (delta).
- **Key requirements:**
  1. Domain subpackages in `engine/` and `parameters/`, one per engineering domain,
     and a domain module may not import another domain module. *WHEN domain A imports
     domain B THEN the import contract check fails.*
  2. The dependency direction covers every layer (including `schemas`, `core` and
     `db`) and is checked by an automated import contract. *WHEN a module imports
     from a higher layer THEN the check fails.*
  3. The engine receives its parameters as typed arguments (task 6.2 reworded). *WHEN
     the engine runs THEN it makes no call into the parameters loader.*
  4. The MVP calculation is synchronous and `worker` is removed; alternatively, a job
     contract is specified. *WHEN a calculation is requested THEN the HTTP response
     carries the result within the stated latency.*
  5. Non-functional requirements are recorded, including separate database roles per
     zone. The rationale for the two-database split and for the edition pin goes into
     `design.md`.
- **Artifact fixes:**
  - Add Non-goals to `proposal.md`.
  - Give every task its zone sub-branch, and add the DOR and the DOD.
  - Replace the beam tasks 4.2, 5.2 and 6.2 with the first-domain pilot.
- **Ready when:** `spec-reviewer` reports no blockers (it found 5 last time), and
  validate passes.
- **Owner:** Akim and DE, with tasks split by zone sub-branch.

### 3.6 `bootstrap-dev-environment` (WP6)

- **Goal:** the smallest set of tools that lets the first code meet the DOD.
- **Capabilities:** MODIFIED `development-process` (names the tools).
- **Key requirements:**
  1. One backend command runs lint, type checks, and tests with branch coverage.
     *WHEN it runs on a clean checkout THEN it exits 0.* The type checker
     (`mypy` or `ty`) is decided here.
  2. Frontend: `eslint`, `tsc` and `vitest` run the same way.
  3. The import contract from WP5 runs as part of the check. *WHEN there is an
     upward import THEN the check fails.*
  4. A pre-commit hook scans for secrets, and `.env.example` lists every variable
     the config reads. *WHEN a secret is staged THEN the commit is blocked.*
  5. Docker compose starts PostgreSQL (both databases) and the backend. *WHEN
     `docker compose up` runs THEN the health endpoint responds.*
- **Ready when:** the type checker is chosen, the CI target is decided (or CI is
  local-only for now), and validate passes.
- **Owner:** Akim (requirements 1–4), Egor (requirement 5 and CI).

### 3.7 `team-roles-update` (WP7)

- **Goal:** the process fits the three-person team and can close changes that contain
  no code.
- **Capabilities:** MODIFIED `development-process`; `AGENTS.md` and `config.yaml`
  follow once the team agrees.
- **Key requirements:**
  1. **PM role.** The PM owns scope, pricing and legal questions and has no code
     zone. *WHEN a scope, pricing or legal decision is needed THEN the PM is its
     owner.*
  2. **GO for code-free changes.** GO requires that validate passes, that
     `spec-reviewer` reports no blockers, and that the other developer acknowledges
     the change. The tester records that tests are not applicable. *WHEN a change has
     no code THEN this path applies.* This unblocks `record-installed-skills-akim`.
  3. **The DOR includes `spec-reviewer`**, because validate checks structure only.
     *WHEN a change is declared ready THEN a `spec-reviewer` report with no blockers
     exists.*
  4. **Shared decisions are tracked.** Specs cite only tracked sources. *WHEN a
     design gives a rationale THEN it cites a tracked file, not the passport.*
- **Ready when:** Egor agrees (these are shared files), and validate passes.
- **Owner:** together.

---

## 4. Improvements (bonus, max 7)

| # | Idea | Product value | Thesis value | Cost | Backed by |
|---|---|---|---|---|---|
| 1 | Result envelope with `NormRef`s, input hash, engine version and `result_id`: any stored result can be re-run and compared later. | High | High (reproducibility demo) | Low (part of WP2) | C1, A11, C4 |
| 2 | Reference examples as data fixtures, used three ways: parametrized tests, a "verification" appendix in the report, and the results chapter. | High | High | Medium | A4, A3, E1 |
| 3 | Traceability completeness computed automatically from the trace (share of steps with a verified `NormRef`). | Medium | High (a new metric) | Low | E1, B2 |
| 4 | One declarative input model per calculation type that generates the validators for the API, the form and the engine. | High (no drift) | High (a clear contribution) | Medium | C10, C2 |
| 5 | Provenance gate: only `human-verified` values reach the engine; NLP becomes a drafting aid with a human in the loop. | Medium | High (positions the NLP chapter safely) | Low | B6 |
| 6 | Import contract (for example `import-linter`) for layers and domain modules: architecture rules become tests. | Medium | Medium | Low (about an hour) | B4, B1 |
| 7 | Traceability matrix generated from the data: requirement id → test → reference example. | Low | High | Low–Medium | E4, A4 |

---

## 5. Сообщение коллегам (черновик)

> Егор, [PM], привет! Итог перепроверки аудита спецификаций: из 35 находок подтвердились 27,
> ещё 7 — частично; дорожную карту пришлю файлом (`docs/` не в git).
> Главное: спеки и `config.yaml` всё ещё описывают прогиб балки, про фундаменты и водоснабжение
> нет ни одного требования; нет проверки применимости метода и нет привязки результата к редакции норм.
> Предлагаю в спеках: (1) `retarget-mvp-domain` — домен, scope, out-of-scope, non-goals до защиты;
> (2) `norm-source-traceability` — статус редакции, NormRef у каждого параметра, фиксация редакции в результате;
> (3) обновить `backend-layered-architecture`: убрать beam и worker, добавить DOR/DOD и ветки.
> Беру на себя: `calculation-core-contract` (трасса, единицы, применимость, конверт результата),
> `calculation-verification` (эталонные примеры, регрессия, метрики) и backend/frontend-тулинг.
> Обсудить на одной встрече (~1 ч):
> — какой домен делаем первым end-to-end; кто даёт эталонные ручные расчёты;
> — формат NormRef {document, edition, clause, status, provenance} — общий для нас интерфейс;
> — [PM]: что значит «первые продажи», лимит B2C, список «не до защиты», можно ли хранить тексты СП/ГОСТ;
> — расчёт синхронный? Как закрывать change без кода (GO-правило), роль PM в AGENTS.md.
> Две БД оставляю как есть (они совпадают с нашими зонами), но фиксируем редакцию в dec_app.

---

## 6. Recommended order

Constraints: no code exists; Akim's time is limited; the SDD gate forbids code before
a change meets the DOR. The cheapest moment for WP1–WP3 is now.

| Step | What | Who | In parallel with | Blocked by |
|---|---|---|---|---|
| 0 | One meeting (about 1 h). Decide the first domain, the source of the reference examples, the `NormRef` shape, sync vs async, what "first sales" means, the legal status of norm texts, and how to share the audit files (D2). **Ask for the reference examples now**, because they take the longest to arrive. | All | — | — |
| 1 | `retarget-mvp-domain` (including `config.yaml`) | DE (lead), Akim | Akim drafts `calculation-core-contract`, which is mostly domain-neutral | Step 0 (domain choice) |
| 1′ | `team-roles-update` (small; unblocks the skills change) | Together | Step 1 | Egor's agreement |
| 2 | `norm-source-traceability` | DE | Akim finishes `calculation-core-contract`, then starts `calculation-verification` | `NormRef` (step 0); C5 answer or deferral |
| 3 | Update `backend-layered-architecture` | Akim and DE | — | Steps 1 and 2 |
| 4 | `bootstrap-dev-environment` | Akim (tooling), Egor (Docker and CI) | The two halves run in parallel | Step 3 (import contract), type-checker choice |
| 5 | First vertical slice: one calculation type of the first domain, from input model to engine, trace, UI and DOCX, with reference examples | Akim, with data from DE | DE: pilot normative data for that calculation type | Steps 2–4 plus at least one reference example |
| later | Second domain; accounts and tenant isolation (A10); deployment; NLP as a research chapter | — | — | Step 5 |

- **Critical path:** step 0 → `retarget-mvp-domain` → `calculation-core-contract`
  (with `norm-source-traceability`) → `calculation-verification` →
  `backend-layered-architecture` update → bootstrap → first slice.
- **Akim's queue:** core contract → verification → tooling → the backend half of the
  architecture update.
- **DE's queue:** retarget → norm-source-traceability → the data half of the
  architecture update → Docker.
- **Do not do now:** ADR backfill beyond what steps 2–3 need, the glossary, audit file
  renumbering, the second domain, accounts and billing.
