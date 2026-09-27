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

**Answer (Egor).**

**Answer (PM).**

### 2. Which type? (Egor and the PM)

- **Proposal.** Akim reads the guide and proposes the type(s) in section 1 of
  `reference-examples-foundations.md`, with the number of worked examples and their
  pages. Proposed type: `<pending: Akim fills from the guide>`.
- **Your side.** Confirm or reject the proposed type. After confirmation, Egor writes it
  into "In-scope calculation types" of `foundations-shallow` (task 3.1).

**Answer (Egor).**

**Answer (PM).**

### 3. Pilot normative data for that type (Egor)

- **Question.** The collector and parser work on a pilot corpus (`normatives-collector`
  design: a 5-document pilot; `normatives-parser` design: the pilot SP). Does it include
  the norm documents that the chosen type rests on? If not, can they be added, and
  when? Step 5 needs them for the chosen type.
- **Your side.** Name the documents and editions the pipeline will deliver for the type,
  marked `unverified` until checked against the primary text.

**Answer (Egor).**
