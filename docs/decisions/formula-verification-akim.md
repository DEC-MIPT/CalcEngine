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

**Answer.**

### 2. On the pilots there were no errors, right?

- **Observation.** On the two pilot formulas (5.5, 5.7) the OCR read them with no errors (semantic
  equality via `latex2sympy2`). If this generalizes at DPI 400 across the corpus, the "косяк" rate
  will be low, and user-side verification becomes mostly a confirmation.
- **Your side.** Confirm the UX assumption (the UI shows excerpt + LaTeX + notation, and the
  engineer confirms/fixes), or say what should be shown instead.

**Answer.**
