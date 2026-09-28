# Formula verification on the user side: question for Akim (and the PM)

- Date: 2026-09-27
- From: Egor. To: Akim (owns the frontend "white box" UI and the backend) and the PM (scope).
- Context: the agreed `NormRef` (`provenance`/`status`), `research-journal.md` entries 8–10, and
  the pilot result that OCR (pix2text + DocLayout-YOLO + DPI 400) reads formulas with no errors
  (5.5 and 5.7 match semantically). Nothing here is final until you answer.

## Why now

OCR now auto-extracts formulas at scale, marking them `provenance=machine-extracted`,
`status=unverified`. For these to reach the engine they must become `human-verified`. Filling a
hand registry for hundreds of formulas is infeasible, so verification must be a user-side action,
not a data-entry job.

## Questions

### 1. Is verification a user-side action in the UI?

- **Proposal.** On a formula, the engineer sees: (a) the normative excerpt (the clause/text the
  formula sits in), (b) the extracted LaTeX (rendered), (c) the symbols/notation. They mark
  "верно" (no error) or "косяк" (error), and on "косяк" they fix the LaTeX. This is how
  `machine-extracted` becomes `human-verified`.
- **Why.** It matches the "white box" USP (transparent output) and is the only scalable path: the
  engineer verifies only the formulas they actually use, not the whole corpus.
- **Your side.** Agree, or propose another verification flow (who verifies, where, when).

**Answer.** Not as a customer-facing gate, for the MVP. The screen you designed (excerpt +
rendered LaTeX + notation, mark correct/issue, fix the LaTeX on issue) is a good
verification tool, but the verifier should be the team (Akim/Egor), not the paying
customer, while the scope stays small.

- `status`/`provenance` verify that the extraction matches the primary source text; the
  document's currency (in force / superseded) is a separate concern, kept out of
  `NormRef` and owned by WP3 (`design.md` resolution 1). Your proposal is scoped
  correctly there; my objection is about who does the checking, not what is checked.
- The product's own problem statement (`AGENTS.md` §1) is that engineers lose time
  re-checking norms and calculations. Asking a paying customer to verify OCR extraction
  the first time they use a formula reproduces exactly that cost, for the first of the
  three USP pillars (a normative base the customer should not have to check themselves).
- The parameters layer already rejects `machine-extracted` values (resolution 2), so no
  calculation runs on an unchecked formula either way; the only open question is who
  plays the verifier role, not whether one is needed.
- Two pilot formulas show OCR is a good draft generator; they do not show the checking
  role can safely move to whoever happens to run a calculation first. A wrong
  `human-verified` mark from one user becomes ground truth for every later user of that
  formula, and there is no reviewer role and no dispute or re-review process defined
  anywhere yet.
- MVP scope is small (a handful of formulas for `foundations-shallow`'s first type),
  well within what the team can check by hand, the way `formulas.toml` already worked
  before the OCR pivot. The scale problem you're solving for (hundreds of formulas
  across the full catalog) is real, but it is a later problem, once volume actually
  requires it.

For MVP: keep the flow you designed, but as a tool the team uses internally
(OCR-assisted, on the closed set of in-scope formulas), before any formula reaches a
customer. Whether and how to open verification to paying users later is a scope and
trust decision, so I'm taking it to the PM separately rather than deciding it here as a
frontend detail.

### 2. On the pilots there were no errors, right?

- **Observation.** On the two pilot formulas (5.5, 5.7) the OCR read them with no errors (semantic
  equality via `latex2sympy2`). If this generalizes at DPI 400 across the corpus, the "косяк" rate
  will be low, and user-side verification becomes mostly a confirmation.
- **Your side.** Confirm the UX assumption (the UI shows excerpt + LaTeX + notation, and the
  engineer confirms/fixes), or say what should be shown instead.

**Answer.** The UX (excerpt + rendered LaTeX + notation, confirm/edit) works, and I will
design it first as the internal reviewer's tool, per question 1. But "no errors on two
pilots" is not enough evidence to skip a review step or let a `machine-extracted`
formula reach a customer unreviewed: two formulas from one document do not generalize
across SP/GOST layouts, and the gate rejects `machine-extracted` values regardless of
the error rate, so someone plays the reviewer role either way. For MVP that someone is
the team, not the customer who happens to run the calculation first.
