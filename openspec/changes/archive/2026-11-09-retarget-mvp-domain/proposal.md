# Proposal

The current scope revision is described below. The following dated review note
records the earlier R-only draft and does not acknowledge this revision.

> Reviewed by Egor (2026-10-05): the data-zone parts (`normatives-catalog` delta,
> `foundations-shallow` lists, the domain-order and milestone decision) are his. Akim
> drafted the change and wrote the engine-facing scenarios. The PM still approves the
> scope and the non-goals list (task 1.4).

## Why

The MVP must deliver a full shallow-foundation calculation by the second group of
limit states. The current registered R calculation is the delivered pilot stage;
R alone does not satisfy the approved MVP outcome. Internal water supply follows
at a separate post-MVP milestone.

Akim reported PM approval dated 2026-10-19 and clarified its scope in the
2026-11-08 conversation. The [product decision record](../../../docs/decisions/product/2026-11-08-mvp-scope-and-b2c-consent.md) owns
that attribution, the confirmed non-goals and the B2C calculation limit.

The main specs still contain placeholder-domain examples. This documentation change
replaces those examples, states the target scope and keeps one owner for each
subscription and authorization rule. It does not define or implement the remaining
engineering contracts needed to deliver the full foundation workflow.

## What Changes

- `product-vision`: the MVP requires the full second-limit-state shallow-foundation
  workflow; internal water supply remains at a separate post-MVP milestone. A new
  requirement lists the non-goals; the subscription requirement stops restating limits.
- `calculation-engine`: the deterministic-calculation scenario no longer names the
  placeholder domain and runs a first-domain calculation type instead.
- `normatives-catalog`: the binding scenario uses a first-domain calculation type; a new
  requirement fixes how a norm reference is marked as verified or `status: unverified`.
- `transparent-output`: the example reference becomes a synthetic placeholder.
- `web-platform`: the input form is domain-neutral; single authorization becomes a
  reference to `user-accounts`.
- `user-accounts`: becomes the only owner of subscription limits and authorization;
  the confirmed B2C limit is no longer marked as awaiting PM approval.
- New capability `foundations-shallow`: scope only. It distinguishes the delivered
  R pilot from the full required MVP workflow, preserves the natural-base boundary,
  and requires reviewed engineering contracts before further implementation.
- `openspec/config.yaml`: the domain sentence in the context is retargeted, and
  "NLP/RAG auto-parsing = future" is replaced with ML-in-MVP.
- `AGENTS.md` and both `data-engineer.md` mirrors (non-OpenSpec files): drop
  "NLP/RAG auto-parsing = future/non-MVP" in the same fold.

## Non-goals

ML-in-MVP (PM-approved): the normative pipeline — collector, regex baseline parser, and
embeddings retrieval on CPU — is part of the MVP; no ML runs in the calculation path.

Before the defense the project does not deliver:

- Billing or payment integration.
- Generative-LLM structured extraction from norms (deferred; needs GPU/budget).
- PDF report output.
- A multi-tenant audit trail.

This change also does not:

- Define the full foundation workflow's engineering methods, applicability cases,
  future calculator identifiers, formulas, coefficients, limits or source clauses.
  These belong to separately reviewed implementation changes before code is written.
  No engineering-method implementation is authorized by this scope revision. Every
  norm reference stays `status: unverified` until checked against the primary source text.
- Specify internal water supply as a capability. It is named as the second domain only;
  its scope change follows at the `water-supply-internal` milestone.
- Edit anything under `openspec/changes/archive/`.
- Edit `openspec/specs/` directly; the deltas apply at archive.
- Edit `backend-layered-architecture`; its cleanup is a task (see `tasks.md`).
- Decide the delivery schedule or team capacity for the expanded scope; these remain PM decisions.

## Capabilities

### New Capabilities

- `foundations-shallow`: first-domain product scope, the full-workflow MVP release
  gate, the delivered pilot, and out-of-scope refusal behavior.

### Modified Capabilities

- `product-vision`, `calculation-engine`, `normatives-catalog`, `transparent-output`,
  `web-platform`, `user-accounts`.

## Impact

- Affects the six modified specs and one new spec after archive, plus
  `openspec/config.yaml` (edited in this draft; domain-specific lines only).
- `openspec/` is a shared area; Egor's zones (catalog, data) are marked in the deltas.
- No code, no migrations.
