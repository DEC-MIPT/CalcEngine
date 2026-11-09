# Design

> Reviewed by Egor (2026-10-05); the data-zone parts below are his.

## Context

The specs describe a placeholder domain. This change retargets the text and fixes the
scope; it adds no behavior beyond scope statements and a norm-reference marking rule.
It is documentation only, so performance, accessibility, and coverage are not applicable.

## Goals

- Every spec and the AI context point at the confirmed MVP domains.
- The MVP scope, the first domain's out-of-scope list, and the non-goals are written.
- Every rule has exactly one owner spec; other specs reference it.
- No norm value, edition, or clause appears without a checked source.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **Domain order: shallow foundations first, internal water supply second.** Taken
   from Akim's confirmation and `CLAUDE.md`. The kickoff file with the Decision section
   named in the task is not in the repository (assumption A1 below).
2. **Only the first domain gets a capability now.** Roadmap section 3.1 allows one new
   capability. The second domain (internal water supply) is named in `product-vision`
   with the `water-supply-internal` milestone.
3. **Owner spec per rule.**

   | Rule | Owner | Others |
   |---|---|---|
   | MVP scope, domain order, non-goals | `product-vision` | reference it |
   | First-domain scope and out-of-scope | `foundations-shallow` | reference it |
   | B2B/B2C limits, trial, authorization | `user-accounts` | `product-vision`, `web-platform` reference it |
   | Norm-reference marking | `normatives-catalog` | `transparent-output` follows it |

4. **Synthetic norm references.** Examples in specs use `<NORM-DOC-PLACEHOLDER>`,
   edition `unverified`, clause `<CLAUSE-PLACEHOLDER>`, and `status: unverified`, never a
   real clause number. The exact reference fields are defined by the planned change
   `norm-source-traceability` (`NormRef`), so this change does not fix a field format.
5. **Placeholders in the scope capability.** The in-scope list is filled (the
   `foundations_shallow_r` type, confirmed by Egor and the PM in
   `docs/decisions/first-calculation-type-egor-pm.md`); the out-of-scope list is its
   complement, for the PM to confirm with the in-scope list (task 1.4).
6. **ML-in-MVP (PM-approved).** The normative pipeline (collector, regex baseline parser,
   embeddings retrieval on CPU) is part of the MVP; no ML runs in the calculation path;
   generative-LLM structured extraction is deferred. The fold touches `product-vision`,
   `normatives-catalog`, `openspec/config.yaml`, `AGENTS.md`, and both `data-engineer.md`
   mirrors.

## PM scope amendment (2026-11-08)

The [product decision record](../../../docs/decisions/product/2026-11-08-mvp-scope-and-b2c-consent.md) records Akim's account of PM
approval dated 2026-10-19 and the scope clarification made in the current conversation.
It supersedes the R-only release boundary of decision 5 and resolves the pending
PM approval described in assumptions A1-A3. The earlier decisions and review note
remain historical records; they do not acknowledge this amended scope.

The required MVP outcome is a full shallow-foundation calculation by the second
group of limit states. `foundations_shallow_r` identifies the delivered R pilot.
That stage alone is insufficient to declare the MVP complete. The existing
restriction to shallow foundations on a natural base remains in force.

Internal water supply follows the foundation MVP at `water-supply-internal`, a
post-MVP milestone. This clarifies the domain-order wording of decisions 1 and 2.
No water-supply capability or implementation is added here.

This change defines a product release gate. Separate implementation changes must
identify the complete engineering workflow, component contracts, applicability,
inputs and outputs, normative sources, and independently derived verification
cases before further calculation code is written. This revision supplies no new
method, coefficient, tolerance, calculator identifier or unsupported soil case.
A release candidate needs those reviewed contracts and their completed acceptance
records to demonstrate the full required workflow; the R pilot cannot substitute
for that evidence.

The non-goals and B2C limit are confirmed in the product record. `user-accounts`
remains the sole specification owner of tier limits. Current-version spec review,
traceability review and second-developer acknowledgement remain separate closure
gates. The old review is not reused as acknowledgement of this amendment.

## Assumptions

A1-A3 below describe the earlier draft and are resolved by the dated amendment.
A4 remains the structural rule for the delta merge.

- A1: the kickoff file with the Decision section does not exist in the repository; the
  domain order comes from Akim's answer in the session.
- A2: the PM's meeting list of non-goals is not in the repository; the list is the
  example list of roadmap section 3.1.
- A3: the B2C limit (100 calculations a month) is kept from the current
  `user-accounts` text in exactly one place and marked unverified until the PM approves.
- A4: MODIFIED requirements repeat the full requirement text, because OpenSpec replaces
  the whole requirement at archive. The validator also refuses a MODIFIED block that
  drops an existing scenario, so "MVP scope" (`product-vision`) and "Deterministic
  verified calculation" (`calculation-engine`) are REMOVED and re-ADDED under new names.

## Boundary

The C/C++ hot-swap boundary of the engine is not touched by this change.
