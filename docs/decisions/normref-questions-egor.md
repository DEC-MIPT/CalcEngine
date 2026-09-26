# NormRef: questions for Egor

- Date: 2026-09-26
- From: Akim. To: Egor (data engineer, owner of the catalog side, WP3 `norm-source-traceability`).
- Source: `openspec/changes/calculation-core-contract/design.md`, section "NormRef", and task 1.3 of that change.
- Purpose: confirm or change the shape of `NormRef` and the answers to eight open questions. Nothing here is final until you answer.

Russian version: `normref-questions-egor-rus.md`.

## Why now

`NormRef` is the shared interface between the calculation core (WP2, Akim) and the normative-data model (WP3, you). Until you confirm it, every task marked `[blocked: NormRef]` in `calculation-core-contract` cannot start, and the metric "traceability completeness" in `calculation-verification` (WP4) stays a draft.

## Proposed shape

```
NormRef {
  document:   string                       # designation as printed in the document; always concrete
  edition:    string | unverified
  clause:     string | unverified          # one locator: a clause, a table, or a formula
  status:     verified | unverified
  provenance: human-verified | machine-extracted
}
Invariant: status = verified implies edition and clause are concrete.

EngineerRule {engineer, rationale}

Step.norm_refs: NormRef[]                  # at least one
Source = NormRef[] (at least one) | EngineerRule
```

- No field may be null.
- `EngineerRule` is allowed only for a rounding rule and for the source of a validated range. Bounds of the method's range and trace steps use `NormRef` lists only.
- Akim already agrees with items 3 and 5 (the list on a step, the separate `EngineerRule` type). The others are Akim's proposals.

## Questions

For each question: the proposal, why, what it means for your side, and a field for your answer. Please mark **Agree**, **Change**, or **Disagree**, and write the change if any.

### 1. What does `status` mean?

- **Proposal.** Verification status only: `verified` or `unverified`. The document status (in force, superseded, withdrawn; WP3 requirement 2) is not a field of `NormRef`. It is read from the catalog by `(document, edition)` when a reference is shown.
- **Why.** The document status changes over time; a reference pinned in a stored result must not. The marker `source: unverified` from `domain-constraints.md` and WP1 is then the display form of `status = unverified`, so the two vocabularies do not compete.
- **Your side.** The catalog owns the document status and exposes it by `(document, edition)`. A named edition that nobody has checked has `status = unverified` with a concrete `edition`.
- **Answer:** Agree. Document status (in force / superseded / withdrawn) is the catalog's model (`dec_normatives`, WP3 requirement 2); only the maintainer changes it. The catalog exposes it by `(document, edition)` when a reference is shown, and it is not a field of `NormRef`: a pinned reference must not change with the document status. I confirm the `source: unverified` marker from `domain-constraints.md` and WP1 as the display form of `status = unverified`.

### 2. Are the `provenance` values final?

- **Proposal.** Yes for the MVP: `human-verified` and `machine-extracted`. `provenance` says where the value came from; `status` says whether the reference was checked against the source text. A `machine-extracted` value is `unverified` until a person checks it, then becomes `human-verified`. The parameters layer rejects `machine-extracted` values, so the engine never sees them (WP3 requirement 4).
- **Why.** The engineer-set case is a separate type (question 3), so no third `provenance` value is needed.
- **Your side.** The pipeline sets `provenance` on load and changes it only through a person's check. Does the rejection in the parameters layer suit your loader, or do you prefer it in the pipeline?
- **Answer:** Agree. I fix `human-verified` / `machine-extracted` for the MVP. The pipeline sets `provenance` on load and changes `machine-extracted` to `human-verified` only through a person's check. The gate stays in the parameters layer (WP3 requirement 4): it is the single entry point of values into the engine, and duplicating it in the pipeline is not needed — the pipeline marks provenance, it does not decide what reaches the engine.

### 3. How is a rule set by the engineer encoded?

- **Proposal.** A separate source type `EngineerRule {engineer, rationale}`, not a `NormRef` with a reserved `document`. Allowed only for a rounding rule and for the source of a validated range.
- **Why.** A reserved `document` value would leak into every consumer of `NormRef` and into the traceability metric, and would blur the rule "no invented sources". Akim reads "implementer" in `domain-constraints.md` ("Rounding and tolerance rules come from the norm, not from the implementer") as the software developer, not the design engineer who fills the parameter data. Please confirm this reading.
- **Your side.** Parameter files carry either a `NormRef` list or an `EngineerRule` for these two fields. Schema validation accepts either, and only these two places accept `EngineerRule`.
- **Answer:** Agree. A separate `EngineerRule {engineer, rationale}` type is right: a reserved `document` would blur the traceability metric and the rule "no invented sources". I confirm the reading of `implementer` in `domain-constraints.md` as the software developer, not the design engineer who fills the parameter data. The design engineer may set a rule where the norm gives none, recorded as an `EngineerRule` and visible in the envelope and the report.

### 4. `unverified` and an unknown document

- **Proposal.** `unverified` is a union value in `edition` and `clause` (a string in serialization). `document` is never `unverified`: it is always a concrete designation. A parameter whose document is unknown has no source, and schema validation fails (WP3 requirement 1). The placeholder `<NORM-DOC-PLACEHOLDER>` is allowed only in spec examples and tests, as in WP1.
- **Why.** A reference without a document is not a reference; the team names the document even when the edition is unchecked.
- **Your side.** If the pipeline can meet a fact whose document really is unknown, tell me how you want to record it.
- **Answer:** Agree. `unverified` is a union value in `edition` and `clause`; `document` is always a concrete designation. The pipeline never meets a fact with an unknown document: every datum is bound to its source document already at collection (registry + downloaded file). If a document cannot be identified, the fact does not enter `dec_normatives` and stays a draft in the pipeline — no separate "unknown document" representation is needed, and schema validation rightly fails.

### 5. What does `clause` hold? Can one step cite several clauses?

- **Proposal.** `clause` is one locator (a clause, a table, or a formula), as an opaque string. A step that rests on several clauses, tables, or documents carries several `NormRef` in `norm_refs`; two references of one document repeat `document` and `edition`. A step is verified only when every one of its references is `verified`. The "clause set" of a pinned result (WP3 requirement 3) is the set of all locators of all steps.
- **Why.** Real steps rest on a clause and a table, sometimes on another document. Keeping `NormRef` atomic covers this and keeps the counting rule simple. (Akim's first idea, "one step, one clause", was dropped for this reason.)
- **Your side.** Does the catalog model (`Document`, `Revision`, `Clause`, `Formula`, `Coefficient`) let you address a table or a formula by a locator? Is one string per locator enough?
- **Answer:** Agree: one locator per `NormRef`; several clauses/tables/documents mean several `NormRef`. For my side: yes, the catalog model (`Document → Revision → Clause/Formula/Coefficient`) addresses a table or a formula by a locator, and one string per locator is enough, but I define the locator syntax: a canonical grammar like `cl. 6.2`, `tab. 8.2`, `form. (12)` (clause number / table number / formula number). The loader normalizes the locator and the catalog resolves the entity from it; the string stays opaque to the engine.

### 6. Is `document` a key or a string?

- **Proposal.** A designation string, as printed in the document, not a key into `dec_normatives`. The catalog resolves `(document, edition)` uniquely and normalizes spelling. For `status = verified` the pipeline checks that the pair exists in `dec_normatives`.
- **Why.** The string is readable in the parameter YAML, in the `dec_app` columns, and in the report, and needs no foreign key across the two databases (finding B3).
- **Your side.** You define the normal form of a designation and the uniqueness of the pair.
- **Answer:** Agree: `document` is a designation string, as printed, not a key. The catalog defines the normal form (for example `СП 16.13330.2017`) and the uniqueness of the `(document, edition)` pair by a constraint in `dec_normatives`; the loader normalizes spelling at intake. For `status = verified` the pipeline checks that the pair exists in `dec_normatives`.

### 7. Is a pinned `NormRef` immutable?

- **Proposal.** Yes in a stored result: the values are copied into the `dec_app` columns and never change. In the catalog and in `params/`, a change (for example `unverified` to `verified`) creates a new version: new runs take it, old results keep the old one. The `status` in a stored result is the status at the time of the calculation. The flag "edition superseded" is computed from the catalog when a result is shown and is not stored.
- **Why.** WP3 requirement 3: a stored result is never recomputed silently, and a result is identified by (inputs, norm document, norm edition).
- **Your side.** The catalog must keep old versions of a reference reachable, or at least never rewrite them in place.
- **Answer:** Agree. A pinned `NormRef` in a stored result is immutable; a change creates a new version of the reference. The catalog stores revisions additively (never rewrites in place): a `Revision` stays reachable after a new one appears, so old results keep their reference. The "edition superseded" flag is computed on display and is not stored.

### 8. What format does `edition` use?

- **Proposal.** An opaque string that identifies one exact text version: the year of the edition, plus a marker for the amendments applied, when there are any (in examples `<YYYY>` or `<YYYY>+<amendment>`). Compared for equality only.
- **Why.** Akim does not fix the syntax, because no edition is checked against a primary source.
- **Your side.** Please set the exact syntax from real documents, and say whether an amendment number belongs in `edition` or in a separate field.
- **Answer:** Agree, with an exact syntax. `edition` is an opaque key string: `<YYYY>` without amendments (for example `2017`) and `<YYYY>+<N>` with amendment No. N applied (for example `2017+1`). The amendment number also lives as a separate `amendment_no` field in the catalog's `Revision` (for the status model and the amendment's effective date), and is folded into the `edition` string as the `NormRef` key. Compared for equality only.

## What happens after your answer

- I record your answers in `design.md` of `calculation-core-contract` and close task 1.3.
- I sync the delta specs and tasks of that change: `norm_ref` becomes `norm_refs`, sources become `NormRef` lists or `EngineerRule`, and the `[blocked: NormRef]` markers are lifted where nothing else blocks the task.
- I define the metric "traceability completeness" in `calculation-verification` (the share of steps whose references are all `verified`, over steps of non-refused envelopes; engineer-set sources counted separately).
- Points that touch your specs (`normatives-catalog` "Norm reference status", WP3) stay yours; I do not edit them.

## Wording clash

`domain-constraints.md` and the WP1 deltas use the marker `source: unverified`; this interface uses `status` and `provenance`. Under question 1 the marker is the display form of `status = unverified`. If you prefer another mapping, say so in the answer to question 1.
