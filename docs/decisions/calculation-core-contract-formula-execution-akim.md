# Formula execution, honest `NormRef` status, and the pilot: questions for Egor (2026-09-29)

- Date: 2026-09-29
- From: Akim. To: Egor.
- Context: an audit of `calculation-core-contract` (WP2) for implementation, after the
  WP5 split, the deletion of `formulas.toml` (`pipeline-followup-answers-akim.md`, A3) and
  the automatic "verified" mark (same file, A1). The audit changed WP2's `design.md`
  (resolution 2 amended, decisions 6 and 7 refined, decisions 11-17 added), added the
  requirement "Formula evaluation from data" to its `calculation-engine` delta, and split
  task 7.1 into 7.1a-7.1b (parameter file and pilot on synthetic data) and 7.1c (pilot on
  catalog data). WP2 task
  1.8 waits for your acknowledgement of items 1, 3 and 4 below.

Russian version: `calculation-core-contract-formula-execution-akim-rus.md`.

## 1. Formulas as expression trees (WP2 decision 11)

`backend-layered-architecture` "No hardcoding" forbids a formula or a coefficient as a
literal in code or in `.yaml`, and `formulas.toml` is gone. So the engine cannot hold the
pilot formula as Python code, and it must not parse formula strings either (`sympify`,
`parse_expr` and `lambdify` execute code; WP2 "Risks").

- **Decision (mine, for the backend).** The code of a calculation type holds only the
  order of the method: which formula, which table value, which branch, which check. The
  arithmetic is an interpreter of an expression tree that arrives with the resolved
  parameters. Allowed nodes: `number` (a constant printed in the formula), `symbol`,
  `add`, `sub`, `mul`, `div`, `pow`, `neg`, and `call` of a function from a closed list
  (first list: `sqrt`, `exp`, `ln`, `log10`, `sin`, `cos`, `tan`, `abs`, `min`, `max`; a
  function is added only when an in-scope formula needs it), at most 64 levels deep and
  4096 nodes. The engine checks the whole tree before evaluating it; anything else fails,
  and nothing is executed. Thresholds that choose a branch of the method, where the norm
  gives them, come as data too, each with its `NormRef`.
- **What I need from you.** For each stored formula, next to its LaTeX and its
  `NormRef`: (a) the expression tree as JSON in the node set above, built at ingestion
  (you already have `latex2sympy2`, so the LaTeX-to-tree step stays in your zone); (b) the
  binding of each symbol of the formula to a quantity with its unit (your
  `NotationEntry` has `symbol`, `meaning`, `unit`).
- **Your side.** Agree, or propose another tree format. The exact JSON shape can be fixed
  together in `normative-catalog-backend` (item 5).

## 2. Coefficients of the pilot formula

The pilot is R, formula 5.7 of СП 22.13330.2016 (`unverified`). Your answer to
`first-calculation-type-egor-pm.md`, question 3, promises table 5.5 (`unverified`;
`M_γ`, `M_q`, `M_c`) with a `NormRef` per value. The formula seems to have other
coefficients too (`γc1`, `γc2`, `k`, `kz`), but this list of symbols is itself
`unverified`: I have not checked it or their source against the text of the СП, so I do
not name a table or a clause for them.

- **Your side.** Name, from the primary text, where each of them comes from, and whether
  the pipeline will store them the same way as table 5.5 (each value with its `NormRef`,
  `unverified` until checked).

## 3. Honest `NormRef.status` (WP2 resolution 2, amendment)

In `pipeline-followup-answers-akim.md`, A1, I asked you to mark every formula as verified
automatically. Reading that against the specs, I keep the automatic mark, but it does not
become `NormRef.status`:

- `status = verified` keeps the meaning of the WP1 requirement "Norm reference status": a
  person checked the reference against the primary text. A `NormRef` with
  `provenance = machine-extracted` always has `status = unverified`; the backend enforces
  this when it builds a `NormRef`, whatever flag your row carries.
- For the MVP the parameters layer does not reject `machine-extracted` values. They reach
  the engine, and every step resting on one is marked unverified and counted in
  `unverified_step_count` (WP1 scenario "Unverified norm source"). Without this no
  calculation could run.
- **Your side.** Acknowledge. For your schema it means: keep `provenance` honest
  (`machine-extracted` for OCR output) whatever your automatic mark is called; the backend
  reads `provenance`, not the mark.

## 4. `input_hash` algorithm (WP2 decision 6)

A stored result will be identified by its `input_hash`, so the algorithm touches WP3
pinning (`norm-source-traceability`, yours).

- **Proposal.** SHA-256 over canonical JSON (sorted keys, no insignificant whitespace,
  numbers as Python's `repr` of the float) of: the calculation type name, the inputs in
  base units, and the identity of the resolved parameter set. That identity is the
  SHA-256 of the same canonical JSON of the resolved parameters, each value with its
  `NormRef` list or `EngineerRule`.
- **Your side.** Agree, or say what WP3 needs in addition.

## 5. Read path and the pilot on catalog data

WP2 task 7.1c (the pilot on real data) waits for:

1. `normatives-formula-contract` tasks 1.4-1.7 merged into `develop` (yours; first in your
   order, A4);
2. items 1 and 2 above (yours);
3. `retarget-mvp-domain` task 3.1: R in the in-scope list of `foundations-shallow`
   (yours; second in your order);
4. the read path from `dec_normatives` to the resolved parameters, in the planned
   `normative-catalog-backend` (both of us). Its first decision is old WP5 item 9.3: where
   the code that reads the norms lives, given that you want it to stay in the pipeline
   and not as a second loader in `backend/normatives/`.

- **Proposal.** I create `normative-catalog-backend` as a proposal, with item 9.3 as its
  first open question for you, so item 4 stops being nobody's.
- **Your side.** Agree, and give an estimate for items 1-3.

WP2 tasks 7.1a-7.1b (the pilot on synthetic data) wait for none of this, so I go on with the
engine in the meantime.

## Answers

- Date: 2026-10-03
- From: Egor. To: Akim.

1. **Expression trees.** Agree. Expression tree as JSON in your node set, built at
   ingestion (`latex2sympy2` stays in my zone), with the binding of each symbol to its
   quantity and unit. I (Egor) put the necessary data into `normative-catalog-backend`; you
   (Akim + Claude) take from there what you need. The exact JSON shape we fix together
   there.

2. **Coefficients of the pilot formula.** Needs re-checking. We already obtain these
   values (`γc1`, `γc2`, `k`, `kz`) in the pipeline; I re-verify them against the primary
   text of СП 22.13330.2016 before naming their source, then store them like table 5.5
   (each value with its `NormRef`).

3. **Honest `NormRef.status`.** Accept the mechanism (backend reads `provenance`, not the
   auto-mark; `machine-extracted ⇒ unverified`; MVP lets `machine-extracted` values reach
   the engine, counted in `unverified_step_count`). For the pilot, we accept for now that
   all its formulas are treated as verified.

4. **`input_hash`.** Accept (SHA-256 over canonical JSON; WP3 needs nothing more).

5. **Read path.** Accept your proposal: you create `normative-catalog-backend` with old
   WP5 item 9.3 as its first open question; estimate per item 6 of
   `normative-catalog-backend-questions-akim.md`.
