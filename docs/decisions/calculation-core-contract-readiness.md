# Readiness review: `calculation-core-contract` (WP2)

- Date: 2026-09-26; updated 2026-09-27 (tasks 6.5 and 7.3, reviewer passes 5-7, checker pass 3; Egor's written `NormRef` agreement; formula path and pipeline risks)
- Change: `openspec/changes/calculation-core-contract/`
- Owner: Akim. Egor (data engineer) confirms `NormRef` only.
- Criteria: `docs/reports/verified-roadmap.md`, section 3.2, "Ready when".

## Final status

**READY FOR TESTER VERDICT**

All roadmap criteria are met: `NormRef` is agreed with Egor in writing, validation passes, `spec-reviewer` reports no blockers, and `norm-traceability-checker` confirms that no requirement fixes a norm value.

This is not GO. The `tester` verdict (task 1.6) is still open. No implementation task waits for `NormRef` any more; the `[blocked: NormRef]` markers were removed.

| Roadmap criterion (3.2) | State | Evidence |
|---|---|---|
| `NormRef` is agreed with DE | Met | Egor agreed to all eight resolutions in his own words in `docs/decisions/normref-questions-egor.md` (commit `a1a896c`, 2026-09-27); task 1.3; `design.md`, section "NormRef" |
| Validate passes | Met | `openspec validate --all --strict`: 17/17 on 2026-09-27, see section 1 |
| `spec-reviewer` reports no blockers | Met | 7 passes, 0 blockers in every pass; pass 7 (formula path and pipeline risks): 0 major, 0 minor in this change |
| `norm-traceability-checker` confirms no norm value is fixed | Met | 3 passes, "No requirement fixes a norm value"; pass 3 confirms the new signature-block rule names document, edition, and clause |

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
