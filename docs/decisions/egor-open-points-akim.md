# Open points for Akim, and a proposal for `docs/decisions/` (Egor, 2026-10-05)

- From: Egor (data zone). To: Akim (backend zone) and the PM.
- Status: open for discussion.

Russian version: `egor-open-points-akim-rus.md`.

## 1. Gates that need you

### 1.1 WP9 `normative-catalog-backend` — your review (task 2.7)
The data feature is merged into `develop`, and the `tester` declared GO (recorded in
`docs/decisions/normative-catalog-backend-readiness.md`). The one remaining step of task
2.7 is your review. Note transparently: I merged the feature **before** your review, on
Egor's instruction, so the readiness doc marks the review as "pending". Please acknowledge
there when you are done.

### 1.2 Formulas with Σ / ∏ / equation systems
`latex2sympy2` cannot auto-parse these into the expression tree, and I do not see a way to
wire it in (details and fresh numbers are in
`docs/decisions/formula-autoparse-limits-egor.md`). Proposal: mark such formulas in
`dec_normatives` with a kind (`sum | product | system`) and hand them to the engine as
parameters, not as a parsed tree. The doc lists three concrete questions.

### 1.3 `retarget-mvp-domain` — PM gate (task 1.4)
Egor's tasks (1.3, 3.2, 3.3, 4.1, 4.2) are done and validated. The merge into `Specs` is
blocked on the PM approving: the non-goals list, the domain order, and the B2C limit.

## 2. Proposal: stop the file-per-question sprawl in `docs/decisions/`

The channel has already grown to one file per question/feature and it will only get worse.
Egor proposes to keep `docs/decisions/` as the channel but consolidate by work direction,
not by feature:

| File | Owner |
|---|---|
| `data.md` | Egor (normative pipeline, catalog, ingestion) |
| `ml.md` | Egor (NLP/RAG/ML research) |
| `infra.md` | Egor (Docker, dev environment) |
| `backend.md` | Akim (engine, backend, report generator) |
| `frontend.md` | Akim (UI/UX) |
| `product.md` | PM (scope, pricing, legal) |

Each file holds dated sections (one section per decision/question), so a new point appends
a section instead of adding a file. Agree? If yes, Egor will consolidate his existing files
and Akim his.
