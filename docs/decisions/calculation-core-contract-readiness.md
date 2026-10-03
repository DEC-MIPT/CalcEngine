# Readiness review: `calculation-core-contract` (WP2)

- Date: 2026-09-26; updated 2026-09-27 (tasks 6.5 and 7.3, reviewer passes 5-8, checker pass 3; Egor's written `NormRef` agreement; formula path and pipeline risks; tester GO for the spec phase)
- Change: `openspec/changes/calculation-core-contract/`
- Owner: Akim. Egor (data engineer) confirms `NormRef` only.
- Criteria: `docs/reports/verified-roadmap.md`, section 3.2, "Ready when".

## Final status

**GO (spec phase, task 1.6) — 2026-09-27**

All roadmap criteria are met: `NormRef` is agreed with Egor in writing, validation passes, `spec-reviewer` reports no blockers, and `norm-traceability-checker` confirms that no requirement fixes a norm value. The `tester` declared GO for the spec phase; see section 7. Implementation sections 2-6 remain open and are not covered by this verdict.

| Roadmap criterion (3.2) | State | Evidence |
|---|---|---|
| `NormRef` is agreed with DE | Met | Egor agreed to all eight resolutions in his own words in `docs/decisions/normref-questions-egor.md` (commit `a1a896c`, 2026-09-27); task 1.3; `design.md`, section "NormRef" |
| Validate passes | Met | `openspec validate --all --strict`: 17/17 on 2026-09-27, see section 1 |
| `spec-reviewer` reports no blockers | Met | 8 passes, 0 blockers in every pass; pass 8 (after commit `ab3adac`): 0 major, 1 minor (fixed) |
| `norm-traceability-checker` confirms no norm value is fixed | Met | 3 passes plus a re-check after `ab3adac`, "No requirement fixes a norm value"; pass 3 confirms the new signature-block rule names document, edition, and clause |

## 1. `openspec validate --all --strict`

Before the review:

```
✓ change/backend-layered-architecture
✓ change/calculation-core-contract
✓ spec/calculation-engine
✓ spec/development-process
✓ spec/normatives-catalog
✓ spec/product-vision
✓ change/record-installed-skills-akim
✓ spec/report-generator
✓ change/retarget-mvp-domain
✓ spec/security
✓ spec/transparent-output
✓ spec/user-accounts
✓ spec/web-platform
Totals: 13 passed, 0 failed (13 items)
```

After every round of fixes, and after the final edits, the result was identical: 13 passed, 0 failed (13 items). Re-run on 2026-09-27 after tasks 6.5 and 7.3 and after the pass 5 fixes: 13 passed, 0 failed (13 items). Re-run on 2026-09-27 after merging `develop` (new changes from Egor and WP4, WP7) and after recording Egor's written `NormRef` agreement: 17 passed, 0 failed (17 items).

## 2. `spec-reviewer` report

The reviewer ran seven times. Each pass checked the fixes of the previous one and looked for new issues. No finding was downgraded or dropped.

### Pass 1: 0 blockers, 3 major, 5 minor

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Major | Existing "Automatic correctness validation" (conclusion "with the reason") is not reconciled with the new envelope `verdict` | Fixed: MODIFIED requirement points at `verdict` and a new field `verdict_reason` |
| 2 | Major | `status`/`provenance` in `NormRef` clash with the `source: unverified` wording in `agent-docs/domain-constraints.md` and the WP1 deltas | Fixed in the design: clash recorded in the NormRef section; question 1 extended. The substance is **deferred to Egor** (task 1.3) |
| 3 | Major | "`rounding_source`: a `NormRef` or the engineer" is untyped and not reconciled with `domain-constraints.md:18-19` ("rounding rules come from the norm, not from the implementer") | Partly fixed: `design.md` records Akim's reading (implementer = software developer; the design engineer may set a rule where the norm gives none, and the rule is shown as engineer-set). Whether this is allowed, and how it is encoded, is **deferred to Egor** (question 3); tasks 4.3 and 5.1 stay blocked |
| 4 | Minor | The unverified-step count has no field name | Fixed: `unverified_step_count` in all three specs |
| 5 | Minor | `trace` of a refused calculation is unspecified | Fixed: scenario "Refused calculation envelope" |
| 6 | Minor | The inherited "99.9% accuracy" NFR is not measurable | Fixed in `design.md`: measurability deferred to WP4 (base spec untouched) |
| 7 | Minor | Tasks 6.5 and 7.1 have no zone tag | Fixed (see pass 2, m1) |
| 8 | Minor | WP1 task 2.1 (confirm the WP1 deltas match this contract) is open | Recorded: `design.md` and task 8.2 gate archive on it |

### Pass 2: 0 blockers, 1 major, 3 minor

All pass 1 fixes were confirmed; #7 was only partly resolved.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| M1 | Major | `rounding_rule`/`rounding_source` must appear "in the envelope", but no field carries them, so the scenario is untestable | Fixed: envelope field `outputs` (value, unit, `rounding_rule`, `rounding_source`); design decision 9; tasks 4.3 and 6.1 |
| m1 | Minor | Tag "report zone" on task 6.5 is not a defined zone | Fixed: "(backend, no code)" |
| m2 | Minor | Refused envelope leaves `unverified_step_count` and `warnings` open | Fixed in the scenario |
| m3 | Minor | The parameter set as an `input_hash` component is in the design only, untested | Fixed: requirement text plus scenario "Different parameters, different hash"; task 6.2 |

### Pass 3: 0 blockers, 1 major, 2 minor

M1 was only partly resolved; m1–m3 were resolved.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| — | Major | `outputs` is printed in the report but not rendered in the UI (`transparent-output`) | Fixed: scenario "Outputs with rounding rule shown"; frontend task 3.5; DOD updated |
| — | Minor | `input_hash` scenarios test only one of three components | Fixed: scenarios for different inputs and for a different calculation type |
| — | Minor | `norm_refs` on refusal is ambiguous when a warning also fires | Fixed: `norm_refs` defined exhaustively; refused scenario updated |

### Pass 4 (confirmation): 0 blockers, 0 major, 2 minor

All three pass 3 findings were resolved. The verdict was "READY for DOR on spec content — only the already-known open items block full DOR".

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| — | Minor | Task 6.1 does not test `norm_refs` of a refused envelope | Fixed after the pass |
| — | Minor | The SHALL text of "Trace display consumes typed steps and warnings" does not name `outputs` | Fixed after the pass |

Both pass 4 minors were text-only edits made after the reviewer run. Validation was re-run and passed.

### Pass 5 (2026-09-27, after tasks 6.5 and 7.3): 0 blockers, 0 major, 3 minor

Scope: the task 7.3 handoff in `design.md` and the task 6.5 signature-block rule in
`report-generator`, `design.md` decision 10, `proposal.md`, and `tasks.md`. The reviewer
confirmed that the three scenarios of "GOST report structure" are testable and agree with
its SHALL text, and that no text still calls the default undecided. It listed the
tracked base-spec edition conflict again for visibility (see section 3, pass 1), not as
a new finding.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Minor | The optional checker line has no defined content | Fixed: when present, it has the same three fields (surname, signature, date) |
| 2 | Minor | The opening list names the signature block as required, two sentences before it becomes conditional | Fixed: "and, when enabled, a signature block" |
| 3 | Minor | Task 6.5 says "the requirement stays `unverified`", which reads as the requirement being unready | Fixed: "the edition stays `unverified` until the normative pipeline confirms it" |

All three were text-only edits made after the pass. Validation was re-run and passed.
Verdict: ready for the reviewed edits; full DOR still blocked by tasks 1.3 and 1.6.

### Pass 6 (2026-09-27, Egor's written `NormRef` agreement): 0 blockers, 0 major, 1 minor

Scope: the edit that replaced "agreed on Akim's word" with Egor's written answers (commit `a1a896c`) in `tasks.md` 1.3, 1.4, the DOR and DOD, and `design.md` "NormRef" (intro, resolutions 3, 5, 8). The reviewer checked every claim against Egor's answers: no overstatement, no norm value or real edition introduced.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Minor | Resolution 8 did not name `amendment_no`, which Egor's answer 8 names | Fixed before commit `9eb75ae` |

### Pass 7 (2026-09-27, formula path and pipeline risks): 0 blockers, 0 major, 0 minor

Scope: after reading Egor's branches (`docs/reports/egor-branches-analysis.md`): `design.md` "Consistency with other specs" (the pipeline's formula registry and `normatives-formula-contract`; WP1 task 2.1 closed), resolution 5 (open item on the locator of a formula printed without a number), two new risks (executing an `expression` from data; coefficient tables for the pilot), and task 7.2 (its inputs). The reviewer verified the facts against Egor's branch and the decision files, found no decision taken for Egor's zone or WP5, and confirmed that formula 5.7 of СП 22.13330.2016 is marked `unverified`. Its one minor finding was about `backend-layered-architecture` section 9 (owners and closing criterion) and was fixed there.

### Pass 8 (2026-09-27, after commit `ab3adac`): 0 blockers, 0 major, 1 minor

Scope: commit `ab3adac` edited `design.md` after pass 7 (the "Consistency with other specs" backend-architecture bullet, resolution 5, and the two Risks entries added in pass 7's scope) without a fresh pass; this pass supplies it. The reviewer re-verified every claim against `docs/decisions/normatives-formula-contract-review-egor.md` (questions 2, 10-13, 15), `docs/decisions/research-journal.md` entry 10, and confirmed `docs/decisions/formula-verification-akim.md` is still unanswered. No overstatement found; formula 5.7 stays `unverified`; nothing else in the change was invalidated.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Minor | Table 5.5 of СП 22.13330.2016 was named in the Risks section without an explicit `unverified` tag, unlike formula 5.7 three lines above | Fixed: tagged `unverified`; also reworded "manually verified copy" to "manually transcribed copy... a stopgap for the pilot, not a primary-source check" after `norm-traceability-checker`'s point of attention (below) flagged the same passage |

`norm-traceability-checker` re-checked the same edited passages in parallel: PASS, with one point of attention on the same "manually verified copy" wording (below), addressed by the same fix.

## 3. `norm-traceability-checker` report

### Pass 1

- No requirement, scenario, or design text fixes a norm value.
- **Minor:** GOST R 21.101 was written with its edition in some places and without it in others.
  - Fixed: the change now writes "GOST R 21.101 (edition unverified)" in every place where it states something itself.
  - The quotes of the base spec's "GOST R 21.101-2020" stay, but only as an unchecked citation handed to WP3 (task 7.3).
- **Major, tracked, not a defect of this change:** after archive, `report-generator` will name GOST R 21.101-2020 as settled in the untouched requirement "GOST-compliant report assembly", while this change marks the same document unverified. Recorded for WP3 (task 7.3); `openspec/specs/` is not edited here.
- **Informational:** "Norm reference status" (the definition of verified/unverified) sits in the unarchived WP1 draft. This is a listed dependency.

### Pass 2

- **PASS** on all three checks:
  - every calculation-bearing requirement defers its source to a `NormRef` field or marks it `unverified`;
  - no norm value is fixed;
  - GOST R 21.101 is marked consistently.
- Answer to "Does any requirement fix a norm value?": **No.**

### After pass 2

The fixes from reviewer passes 2–4 (`outputs`, hash scenarios, `norm_refs`) came after the checker's last run. A pattern grep over the change for numbers with units, clause numbers, `SP`/`СП` designations, and comparison bounds returned only process numbers:
- the inherited "99.9% accuracy", quoted as not measurable;
- the ">= 95% branch coverage" DOD target.

No norm value.

### Pass 3 (2026-09-27, after tasks 6.5 and 7.3)

- **PASS** on norm values: no coefficient, limit, tolerance, rounding value, or other
  numeric norm value is fixed. The new signature-block rule is a document-formatting
  rule, not a calculation value.
- The new rule in `report-generator` "GOST report structure" states document, edition,
  and clause (GOST R 21.101-2026, clause 4.1.7, Annex E instructions for columns 10-13)
  and marks the edition `unverified`. `design.md` decision 10 keeps it `unverified` until
  the normative pipeline confirms it.
- **Major, tracked, not a defect of this change:** the base `report-generator` still
  names GOST R 21.101-2020 without a marker, so after archive the capability cites the
  same document with two editions. Handed to WP3 (task 7.3).
- **Minor:** `proposal.md` Non-goals cited GOST R 21.101-2026 without "(edition
  unverified)". Fixed after the pass.

## 4. `{{FIRST_DOMAIN}}` check

- The change contains no `{{FIRST_DOMAIN}}`.
- It uses `foundations-shallow`, taken from the `retarget-mvp-domain` (WP1) draft, in `proposal.md` (Impact) and task 7.1.
- WP1 is not applied: `openspec/changes/archive/` is empty. If WP1 renames the domain, these two places change.
- The spec deltas are domain-neutral.

## 5. Open items carried forward

| Item | Owner | Blocks |
|---|---|---|
| `tester` verdict for the spec change (task 1.6) | `tester` agent | GO; final version on `develop` (8.1) |
| WP1 archived first (WP1 task 2.1 closed on 2026-09-27, task 8.2 done; `retarget-mvp-domain-akim-review.md`) | Egor | Archive (8.3) |
| `backend-layered-architecture` sync: task 6.2 wording (B5), decision 7, "formulas in YAML vs code" (task 7.2) | Akim and Egor (WP5) | Nothing in this change; runs after apply |
| Base `report-generator` names GOST R 21.101-2020, which the Rosstandart register lists as replaced by GOST R 21.101-2026 from 2026-04-01; handed over in `design.md` "Handoff to WP3" (task 7.3 done) | Egor (WP3) | Nothing in this change |
| GOST R 21.101-2026 edition used for the signature block stays `unverified` (task 6.5 done, `design.md` decision 10) | Egor (normative pipeline) | Nothing in this change; a correction changes one setting or line |

## 6. Closed since 2026-09-26

| Task | Outcome |
|---|---|
| 1.3 (written confirmation) | Egor answered all eight `NormRef` questions in his own words in `docs/decisions/normref-questions-egor.md` (commit `a1a896c`, 2026-09-27) and agreed to each resolution. His answers add the locator syntax (answer 5) and the `edition` syntax with a separate `amendment_no` in the catalog (answer 8); `design.md` resolutions 5 and 8 reference them. Resolution 3 records his confirmation of the "implementer" reading |
| 7.3 | `design.md`, section "NormRef", block "Handoff to WP3": the base `report-generator` names GOST R 21.101-2020 as settled; the Rosstandart register lists GOST R 21.101-2026 (order No. 129-ст of 2026-02-12, in force from 2026-04-01) as its replacement |
| 6.5 | Checked against GOST R 21.101-2026 (text from a copy of the official edition, kept untracked in `docs/NTD/`). Clause 4.1.7: calculations are formatted as text documents. Annex E, columns 10-13: the developer's and the normative controller's signatures are mandatory, a checker line is allowed. The signature block holds the developer and normative control lines, the checker line is optional, the setting is enabled by default. Recorded in `report-generator` "GOST report structure", `design.md` decision 10, and task 6.4 |
| 1.6 | `tester` GO for the spec phase; see "Tester verdict" below |

## 7. Tester verdict (task 1.6, spec phase only)

```
Verdict: GO (spec phase only, task 1.6)
Change: calculation-core-contract (WP2), develop @ cd91116 + a small design.md wording fix (table 5.5 unverified tag), 2026-09-27
Conditions:
- Validation: PASS. `openspec validate calculation-core-contract --strict` -> valid. `openspec validate --all --strict` -> 17/17.
- spec-reviewer no blockers (current text): PASS. Pass 8 (0 blockers, 0 major, 1 minor) plus the tester's own read of the minor's fix (adds the `unverified` tag to table 5.5 and removes the "manually verified" phrasing that could read as a primary-source check).
- norm-traceability-checker: PASS. Re-check after `ab3adac` found no invented or altered norm source; its one point of attention (same wording) was fixed by the same edit the tester read.
- Egor's written agreement: PASS. `docs/decisions/normref-questions-egor.md`, all eight questions answered in his own words; commit `a1a896c` authored by Egor.
```

This verdict covers the spec phase only. Implementation sections 2-6 remain open and are not covered; archive (task 8.3) still needs those, WP1 archived, and the `spec-keeper` sync.

## 8. Implementation audit (2026-09-29, task 1.7)

Before implementation went on past task 2.1, Akim audited the change against the WP5
split, the deletion of `formulas.toml` and the automatic "verified" mark of the pipeline
(`docs/decisions/pipeline-followup-answers-akim.md`, A1 and A3). Akim's decisions: honest
`NormRef.status` (resolution 2 amended); formulas as expression trees interpreted by the
engine, method order in code (decision 11); `result_id` and schema validation at the
service level, storage and endpoint in a later change (decision 12).

Changes: `design.md` decisions 1, 3, 5, 6, 7 refined and 11-17 added, resolution 2
amended, new `NormRef` invariant (pending task 1.8); `calculation-engine` delta: new
requirement "Formula evaluation from data", and "Pure calculation function", "Typed trace
step", "Explicit units at the boundary", "Applicability check with three outcomes",
"Result envelope", "Automatic correctness validation" extended; check steps added to the
`transparent-output` and `report-generator` scenarios; `tasks.md` reworked (new 1.7, 1.8,
2.5, 3.6, 4.4, 6.1a, 6.1b; 7.1 split into 7.1a-7.1c). Letter to Egor:
`calculation-core-contract-formula-execution-akim.md` (task 1.8).

| Check | Result |
|---|---|
| `openspec validate --all --strict` | 18/18 |
| `spec-reviewer` pass 9 | 3 blockers, 7 major, 4 minor: decisions 12, 16, 17 were only in `design.md`; fixed by moving the testable rules into the requirements |
| `spec-reviewer` pass 10 | 0 blockers, 3 major, 6 minor: warning source per bound, pilot start, hidden branch dependencies; fixed with minors 4, 5, 6, 8 |
| `spec-reviewer` pass 11 | 0 blockers, 0 major, 1 minor (fixed). **READY for DOR**, apart from tasks 1.7 and 1.8 themselves. Minors 7 (tasks 2.5, 6.1, 7.1b borderline for one session) and 9 (DOR checklist dates) left as they are |
| `norm-traceability-checker`, two passes | 0 blockers; major 1 of the first pass (proposal Non-goals) fixed; no norm value fixed, no invented citation. Minors: rounding policy recorded as an engine design choice (decision 14); the new invariant marked pending Egor; the GOST R 21.101-2026 copy location and the formula 5.7 locator origin carried over from earlier passes |

Open: task 1.8 (Egor's acknowledgement of the resolution 2 amendment, decision 11 and
decision 6). Task 6.2 is checked off only after it; task 7.1c waits for the items in
`tasks.md` "Dependencies".

## 9. Report amendment (2026-09-30, task 1.9)

Before starting the report (tasks 6.3-6.4), Akim found that no task built the report
itself (title block, input table, trace, conclusion), although the scenarios of 6.4
check the order of all sections. Akim's decisions: the missing body and title block
become their own tasks; formulas print as LaTeX text; the title block is the full form of
GOST R 21.101-2026 (edition unverified), form 5 on the first sheet and form 6 on the
following sheets; the signature block is the rows of columns 10-13 of form 5, not a
separate section; columns 20-22 and the dashed optional columns are out of the MVP.

Changes: `design.md` decision 10 refined and decision 18 added; `report-generator` delta:
"GOST report structure" rewritten (frame and forms 5/6, signatories from the request,
rejection rules, refused-calculation and checker scenarios), new requirement "Report
values, formulas and dates"; `tasks.md`: new 1.9 and 6.2a-6.2f, 6.3 and 6.4 reworded with
tests, a follow-up for title-block length limits.

| Check | Result |
|---|---|
| `openspec validate --all --strict` | 18/18 |
| `spec-reviewer` pass 12 | 0 blockers, 6 major, 7 minor: signatory data source, refused-report scenario, references section, base 2020 edition, task size, 6.3 without tests; all fixed |
| `spec-reviewer` pass 13 | 0 blockers, 1 major (generation-time test waited for the pilot; now a synthetic envelope of 200 steps), 5 minor; all fixed |
| `spec-reviewer` pass 14 | 0 blockers, 0 major, 3 minor (fixed). **READY for DOR** |
| `norm-traceability-checker`, three passes | 0 blockers; the two majors of the first pass (the 185 mm width and the frame without Annex Zh) fixed; no norm number fixed. Minors left: the Russian unit designations are `source: unverified` (for WP3); the base spec still names GOST R 21.101-2020 (recorded WP3 handoff) |

Open: none for task 1.9. Task 6.2a may start on `feature/report-generator/backend`.

## 10. Egor's acknowledgement (2026-10-03, task 1.8)

Egor answered in the "Answers" section of
`calculation-core-contract-formula-execution-akim.md` (commit `a01af6f`):

- Item 1 (decision 11, the expression tree): agreed. The pipeline builds the tree as JSON
  in the engine's node set at ingestion and stores the binding of each symbol to its
  quantity and unit; the exact JSON shape is fixed together in `normative-catalog-backend`.
- Item 3 (resolution 2 amendment): accepted. For the pilot, the steps stay unverified
  (`pipeline-open-items-questions-akim.md`, "Answers", 2b).
- Item 4 (decision 6, `input_hash`): accepted with no change.
- Item 2 (the other coefficients of the pilot formula): Egor re-verifies them against the
  primary text before naming their source; this waits in `normative-catalog-backend`, not
  here.

Changes: `design.md` decisions 6 and 11, the `NormRef` invariant and the resolution 2
amendment record the acknowledgement; the "Consistency with other specs" and "Risks"
sections record the merge of `feature/normative-parser/ml` into `develop` (`0184450`) and
the new path `ml/configs/formulas.toml`; the citation of the untracked recon notes in the
design note on the declarative input model is replaced by its content. `tasks.md`: 1.8 and
6.2 checked off (6.2 was implemented in `ae096cd` and waited only for 1.8), the DOR
dependency line closed. No requirement and no scenario changed.

Open: none for task 1.8. Task 7.1c and its waits are in the planned
`normative-catalog-backend`.

## 11. `spec-reviewer` after Egor's answers (2026-10-03, passes 15-16)

Run on the current text after section 10's edits, together with WP5 (the 9.3 settlement).

| Pass | Result |
|---|---|
| 15 | 0 blockers, 0 major, 7 minor: stale passages that still called the user-side verification action open, the old B5 and "formulas in YAML" bullets, a repeated status line for `normatives-formula-contract` 1.4-1.7, the opening of task 7.2, the untracked `01-recon.md:97` cited in `proposal.md`, a long DOR line. All fixed (struck through with a dated "Superseded"/"Closed" note, one status line kept). **READY for DOR** |
| 16 | 0 blockers, 0 major, 2 minor (wording of "No hardcoding" as former WP5 text; the antecedent in task 7.2). Both fixed. **READY for DOR** |

`openspec validate --all --strict`: 19/19. No requirement or scenario changed.

## 12. Engine feature: GO, review and merge (2026-10-03)

`feature/calculation-engine/backend` (backend tasks of sections 2-5, 6.1, 6.1a, 6.1b, 6.2,
7.1a, 7.1b), with `develop` merged into it at `ae9d486`.

| Step | Result |
|---|---|
| `tester` | **GO** at `ae9d486`: `backend/check.sh` 343 passed, 0 skipped; branch coverage 100%; ruff and mypy clean; every task and verify clause mapped to tests; all 31 `calculation-engine` scenarios and `security` "Invalid input rejected" covered; purity (file, socket, clock, random, uuid patched to raise), determinism (three `PYTHONHASHSEED` subprocess runs) and the pilot literal scan pass; only `backend/` changed; UI/UX N/A (no UI) |
| `orchestrator` review | **APPROVED**: no blocker, no major. Checked sound: interpreter safety (closed node and function sets, limits and bindings checked on the whole tree before evaluation, no `eval`/`exec`/`sympify`, non-finite values caught per node), applicability with three outcomes, rounding by `Decimal(repr(value))` on outputs only, `input_hash` per decision 6, envelope order and dedup per decision 17, verdict, layer order (`engine` imports only `schemas` and `core`), no norm literal in the pilot, units converted once at the boundary |
| Merge | `8c001b9` into `develop`; `check.sh` on `develop` after the merge: 343 passed, coverage 100% |

`tester` minor findings, accepted: `params/*.yaml` is checked by a key whitelist and
forbidden words, not a literal scan (task 7.1a asks for that); `submit` with an input
outside the method's range is covered end to end by the `calculation-api` tests; the
unknown-node-kind cases fail at parsing, before any evaluation.

Review minor findings, follow-ups after the three backend branches are merged (planned
`fix/calculation-engine/backend`, with tests):

1. `engine/rounding.py`: `RoundingRule.decimals` has no upper bound, so `quantize` can
   raise `decimal.InvalidOperation` (a `500`, not a `DECError`) for many decimals or a
   very large value. Bound `decimals` or quantize in a local context and raise
   `CalculationError`.
2. `engine/steps.py`: the units of a formula's symbols are checked after evaluation, so a
   unit mismatch can surface as a non-finite value. Check units first.
3. `engine/hashing.py`: stale docstring about task 1.8. Already fixed on
   `feature/calculation-api/backend` (`cc70f7d`).
4. `engine/pipeline.py`: a refusal is detected by `outcome.result is None`; test
   `outcome.refusal is not None`, as decision 3 names it.
5. The step union type is spelled out five times and `Operator` twice; keep one alias
   each in `schemas`.
6. `schemas/resolved.py`: `TableValue` does not carry the values that selected it, so the
   engine cannot confirm that a table entry belongs to the given input. Goes to
   `normative-catalog-backend` (task 7.1c), together with the exact-match row lookup.
7. `schemas/parameters.py` (WP5): `EngineerRule` accepts empty strings and is not frozen;
   add `min_length=1` and `frozen=True`.

Open in this change: the report feature (`feature/report-generator/backend`, tasks
6.2a-6.4), the frontend feature (3.4, 3.5, 5.4), task 7.2, and the archive (8.3) after
`retarget-mvp-domain`.

## 13. Report feature: GO, review and merge (2026-10-03)

`feature/report-generator/backend` (tasks 6.2a-6.2f, 6.3, 6.4), with `develop` (engine
included) merged into it at `035c640`.

| Step | Result |
|---|---|
| `tester` | **GO** at `035c640`: 447 passed (report tests 104 in 2.6 s); branch coverage 100%, all 7 report modules 100%; ruff and mypy clean; every verify clause of 6.2a-6.4 mapped to tests; all 15 `report-generator` scenarios covered; 200 trace steps rendered in 0.14 s; GOST R 21.101-2026 citations "edition unverified", unit designations "source: unverified"; only `backend/` changed; UI/UX N/A (`.docx` output, no UI) |
| `orchestrator` review | **APPROVED**: no blocker, no major. Checked sound: body order and the refused report, number, unit and date formats (no clock read), form-5 and form-6 geometry (185 mm widths, 40 mm and 15 mm heights, merges, columns 10-13), `PAGE`/`NUMPAGES` fields, the signature block enabled and disabled, the accountability block and statement, layer order (`reporting` does not import `engine`), untrusted text written only through python-docx runs (escaped), XML attributes built from constants only, no invented norm value |
| Merge | `9642d8d` into `develop`; `check.sh` on `develop` after the merge: 447 passed, coverage 100% |

Follow-ups added to the planned `fix/calculation-engine/backend` (after the three
backend branches are merged), numbered after section 12's seven:

8. **First of the fix branch.** `schemas/report.py`: the `Text` check rejects only
   category Cc; U+FFFE and U+FFFF pass the schema and python-docx then fails while
   rendering, so `POST /calculations/{result_id}/report` answers `500 internal_error`
   instead of `422`. Reject every character that is not valid XML 1.0 and refine the
   "GOST report structure" scenario of the `report-generator` delta. Safe to do after the
   `calculation-api` merge: the endpoints run on a developer machine only, with no client
   and no login yet.
9. `schemas/report.py`: no length limit on `Text` fields (decision 18, "Risk"); add
   per-column `max_length`.
10. `reporting/title_block.py`: `FORMAT_BOX_MM` has neither a source nor a "layout
    choice" label; label it.
11. `reporting/title_block.py` and `layout.py`: two `FRAME_SIDES` constants with opposite
    meanings; rename the title-block one (for example `FRAME_DRAWN_SIDES`).
12. `reporting/title_block.py`: `"Arial"` and one sheet setting repeat `layout`; use the
    `layout` constants.
13. `reporting/docx_writer.py` and `accountability.py`: the verdict words are defined
    twice; keep one table.
14. `backend/requirements.txt`: pin `python-docx>=1.2,<2`, since the code uses its
    private objects (`_tbl`, `_p`, `_sectPr`, `_Header`).
15. (`tester`) The timing and two-sheet tests build a `Report` without the accountability
    section; add it, so the timing covers the whole body.
16. (`tester`) Three geometry docstrings (`FRAME_MM`, `ROW_HEIGHT_MM`,
    `FORM6_ROW_HEIGHTS_MM`) name the GOST figure without "edition unverified"; add it.

Accepted as they are: the control-character test covers 3 of the `Text` fields (they share
one type); the two-sheet test checks structure, not real page breaks (the spec allows it).

Open in this change: the frontend feature (3.4, 3.5, 5.4), task 7.2, and the archive (8.3)
after `retarget-mvp-domain`.

## 14. Follow-ups from the `calculation-api` review (2026-10-03)

The three backend branches are merged (`8c001b9`, `9642d8d`, `23318c1`), so the planned
`fix/calculation-engine/backend` can start. Two more items from the second
`calculation-api` review:

17. `api/errors.py`: an unexpected error writes two log lines (`error=<Type>` and
    `code=internal_error route=…`), and only the type when the response had already
    started; design.md decision 5 asks for one line with code, route and type. Log once.
18. `main.py`: the engine the application built is not disposed if shutdown fails after
    `yield`; wrap the `yield` in `try`/`finally`.
