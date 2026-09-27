# First calculation type of `foundations-shallow`: questions for Egor and the PM

- Date: 2026-09-27
- From: Akim. To: Egor (fills the in-scope list of `foundations-shallow`, `retarget-mvp-domain` task 3.1; owns the normative pipeline) and the PM (owns scope decisions).
- Source: `openspec/changes/retarget-mvp-domain/specs/foundations-shallow/spec.md` ("In-scope calculation types: TBD"), `openspec/changes/calculation-verification/` (WP4, "Reference examples"), `docs/decisions/reference-examples-foundations.md` (worksheet).
- Purpose: agree on the first calculation type of the first MVP domain. Nothing here is final until you answer.

Russian version: `first-calculation-type-egor-pm-rus.md`.

## Why now

The in-scope list of `foundations-shallow` is still TBD. It blocks:

- `calculation-core-contract` task 7.1: the pilot type for the contract tests;
- `calculation-verification`: the reference examples, 3 per type, taken from the methodical guide on shallow foundations (WP4 decisions 1 and 2), and the invariants and "typical calculation" for that type;
- step 5 of the roadmap: the first end-to-end slice, which needs pilot normative data for the type and at least one reference example.

Akim fills the reference examples as the engineer (`reference-examples-foundations.md`).

## How to answer

Egor: write your answer under "Answer" and commit this file on a sub-branch of `develop`,
then merge it into `develop`. PM: give your answer to Akim or Egor; the developer who
records it writes it under "Answer" with the date, the PM's words, and where they were
given (meeting or message), as proposed in `team-roles-update-egor.md`, question 3.

## Questions

### 1. How is the first type chosen? (Egor and the PM)

- **Proposal.** The first type is one that (a) the methodical guide covers with at least
  3 worked examples, so WP4 can have its 3 reference examples; (b) rests on norm
  documents that Egor's pipeline can deliver as pilot data (question 3); (c) the PM
  accepts as part of the MVP scope.
- **Why.** Without (a) the reference suite is invalid (WP4 scenario "Too few or
  incomplete examples"); without (b) the first slice has no normative data; (c) is the
  PM's decision on scope.
- **Your side.** Agree, or change the rule.

**Answer (Egor).** Agree with the rule: the first type must be covered by at least 3 worked examples in the guide, rest on documents my pipeline can deliver as pilot data, and be accepted by the PM.

**Answer (PM).**

### 2. Which type? (Egor and the PM)

- **Proposal.** Akim reads the guide and proposes the type(s) in section 1 of
  `reference-examples-foundations.md`, with the number of worked examples and their
  pages. Proposed type: `<pending: Akim fills from the guide>`.
- **Preliminary candidate.** The design soil resistance of the base R, formula 5.7,
  clause 5.6.7 of СП 22.13330.2016 (numbers from Egor's `formulas.toml`, `unverified`).
  It is already in Egor's formula registry and the SP is ingested. It becomes the
  proposal only if the guide has at least 3 worked examples of it; it also needs
  question 3 (coefficient table).
- **Your side.** Confirm or reject the proposed type. After confirmation, Egor writes it
  into "In-scope calculation types" of `foundations-shallow` (task 3.1).

**Answer (Egor).** I confirm R (formula 5.7, clause 5.6.7, СП 22.13330.2016) as the candidate: it is already in the registry (`formulas.toml`) and the СП is ingested. Note the dependency on coefficient table 5.5 (see the formula-contract review, question 7).

**Answer (PM).**

### 3. Pilot normative data for that type (Egor)

- **What is there now** (your records; editions `unverified` until checked against the
  primary text):
  - Pilot SP of the parser: СП 22.13330.2016 "Основания зданий и сооружений", the
    shallow-foundation pilot; already ingested into Postgres (647 clauses, 124 formulas,
    141 notation entries; `docs/decisions/normatives-postgres-storage.md` on
    `feature/normative-parser/ml`).
  - Downloaded corpus (`ml-model-journal.md`, entry 4, current editions only):
    СП 22.13330.2016, СП 24.13330.2021, СП 45.13330.2017 (foundations), СП 30.13330.2020,
    СП 31.13330.2021 (water); СП 32.13330.2018 has no file in the registry. Your note for
    Akim also mentions a scanned СНиП, not named.
  - `normatives-collector` task 1.2 (the 5-document pilot list) is still open.
- **Question.** Does the chosen type rest on СП 22.13330.2016 only, or does it also need
  another document (for example СП 24 or СП 45)? If another one is needed, when will it be
  ingested? Is the 5-document pilot list of task 1.2 the five downloaded documents above?
  If the type is R: its coefficients `M_γ`, `M_q`, `M_c` come from table 5.5, and
  tables are not stored yet. When will that table be available, each value with its
  `NormRef` (see `normatives-formula-contract-review-egor.md`, question 7)?
- **Your side.** Name the documents and editions the pipeline will deliver for the type,
  marked `unverified` until checked against the primary text.

**Answer (Egor).** R rests on СП 22.13330.2016 only. The 5-document pilot list of task 1.2 is the five downloaded documents (СП 22.13330.2016, СП 24.13330.2021, СП 45.13330.2017, СП 30.13330.2020, СП 31.13330.2021; СП 32.13330.2018 has no registry file). Table 5.5 (M_γ, M_q, M_c) is stored starting this iteration, each value with its `NormRef`, `unverified` until checked.
