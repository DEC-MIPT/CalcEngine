# Proposal

> DRAFT — needs Egor review. Egor leads this change; Akim drafted it and wrote the
> engine-facing scenarios. The PM approves scope and the non-goals list. Nothing here is
> final until Egor has reviewed and rewritten his parts.

## Why

The specs and the AI context (`openspec/config.yaml`) still target a placeholder domain,
while the confirmed MVP domains are shallow foundations and internal water supply.
The verified roadmap (`docs/audit/03-verified-roadmap.md`, section 3.1) records this as:

- **A1 (Critical, confirmed):** the placeholder domain appears in more places than the
  audit reported: the `product-vision` MVP scope, the `config.yaml` context, an engine
  scenario, a catalog scenario, the transparent-output example, and the pilot tasks and
  design of `backend-layered-architecture`.
- **A2 (Critical, confirmed; C7 and C8 merged into it):** no requirement, scope, or
  out-of-scope statement exists for either MVP domain. A keyword sweep over
  `openspec/**` for the real domains returns no hits.
- **E3 (High, needs data):** the scope facts hold, but whether the scope fits 38 weeks
  depends on team capacity, which is not in the repository. This change therefore fixes
  the scope and the non-goals in writing and leaves the capacity question to the PM.

Duplicated rules also block a single owner per requirement: the B2B/B2C limits are
stated in both `product-vision` and `user-accounts`, and single authorization is stated
in both `web-platform` and `user-accounts`.

## What Changes

- `product-vision`: the MVP scope names both domains and their order (shallow
  foundations first, internal water supply second); a new requirement lists the
  non-goals before the defense; the subscription requirement stops restating limits.
- `calculation-engine`: the deterministic-calculation scenario no longer names the
  placeholder domain and runs a first-domain calculation type instead.
- `normatives-catalog`: the binding scenario uses a first-domain calculation type; a new
  requirement fixes how a norm reference is marked as verified or `source: unverified`.
- `transparent-output`: the example reference becomes a synthetic placeholder.
- `web-platform`: the input form is domain-neutral; single authorization becomes a
  reference to `user-accounts`.
- `user-accounts`: becomes the only owner of the subscription limits and of
  authorization.
- New capability `foundations-shallow`: scope only (what is in, what is out).
- `openspec/config.yaml`: the domain sentence in the context is retargeted.

## Non-goals

DRAFT — PM approval pending. The PM meeting list is not in the repository, so this list
is the example list from roadmap section 3.1.

Before the defense the project does not deliver:

- Billing or payment integration.
- NLP/RAG parsing of norms inside the product.
- PDF report output.
- A multi-tenant audit trail.

This change also does not:

- Write an engineering method, a formula, a coefficient, a limit, or a clause number for
  any domain. Every norm reference stays `source: unverified` until checked against the
  primary source text.
- Specify internal water supply as a capability. It is named as the second domain only;
  its scope change follows at a named milestone.
- Edit anything under `openspec/changes/archive/`.
- Edit `openspec/specs/` directly; the deltas apply at archive.
- Edit `backend-layered-architecture`; its cleanup is a task (see `tasks.md`).
- Decide whether the scope fits 38 weeks (E3); that is the PM's decision.

## Capabilities

### New Capabilities

- `foundations-shallow`: scope of the first domain (in-scope calculation types,
  out-of-scope cases, refusal behavior).

### Modified Capabilities

- `product-vision`, `calculation-engine`, `normatives-catalog`, `transparent-output`,
  `web-platform`, `user-accounts`.

## Impact

- Affects the six modified specs and one new spec after archive, plus
  `openspec/config.yaml` (edited in this draft; domain-specific lines only).
- `openspec/` is a shared area; Egor's zones (catalog, data) are marked in the deltas.
- No code, no migrations.
