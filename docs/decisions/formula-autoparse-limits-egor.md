# Formula autoparse limits: Σ / ∏ and equation systems (message to Akim)

- Date: 2026-10-05
- From: Egor (data zone). To: Akim (backend zone).
- Context: `normatives-formula-contract` research (nb08 §11) and the expression-tree
  contract of `normative-catalog-backend` (design decision 3).
- Status: **open for discussion** — no decision made.

Russian version: `formula-autoparse-limits-egor-rus.md`.

## What I found

The deterministic text-layer reconstruction now returns formulas that contain a summation
(`\sum_{i=1}^{n}`), a product (`\prod`) or a system of equations (`\begin{aligned}`) as
correct LaTeX — for example СП 22.13330.2016 (5.16) reconstructs to

```
s = β Σ_{i=1..n} (σ_{zp,i} − σ_{zγ,i}) h_i / E_i + β Σ_{i=1..n} σ_{zγ,i} h_i / E_{e,i}
```

But these formulas **do not pass through sympy**: they cannot be auto-parsed into the
expression-tree JSON by `latex2sympy2`. A fresh corpus measurement (2026-10-05, bytecode
cleared, fresh process):

| Document | formulas with Σ | parse in sympy |
|---|---|---|
| СП 22.13330.2016 | 14 | 1 |
| СП 24.13330.2021 | 10 | 5 |
| СП 31.13330.2021 | 1 | 1 |

The few that pass are simple `\sum` without stacked limits (for example `\sum y_i^2`).
Everything with `\sum_{i=1}^{n}` limits over or under a fraction operand, nested sums, a
`\prod`, or an `aligned` system fails.

## Why sympy cannot be wired in here

1. `latex2sympy2` has no reliable grammar for `\sum_{lower}^{upper}` with a multi-line
   fraction operand, for nested `\sum`, or for `\prod`. Normalizing these into a parseable
   form is a per-construct patch that does not generalize, and it violates the
   no-hardcode / no-pilot-tuning rule. I tried; it does not hold.
2. Even a successful parse would produce a `Sum` / `Product` node, which is **not in the
   contract's expression-tree node set** (`number`/`symbol`/`add`/`sub`/`mul`/`div`/
   `pow`/`neg`/`call`). The engine's form has no summation/product/system construct, so an
   auto-parsed tree of these types would not fit the contract anyway.

## Proposal (for discussion)

Do not force these formulas through sympy. Instead:

- store such a formula in `dec_normatives` with a label/kind marking it as not an
  auto-parsed tree — for example `form = sum | product | system`;
- represent it to the engine as **parameters** (structured data: the operator, its bounds,
  its operand, and the units), not as an expression tree.

## Questions for Akim

1. Is a `form`/`kind` label on `formula` (and a corresponding column in the
   `type_formulas` view) the right shape, or do you want a separate parameter kind?
2. How should the engine receive a Σ/∏/system: as a `Formula` with an absent/empty tree
   plus a structured `sum`/`product`/`system` descriptor, or as a new parameter type?
3. Is it acceptable to leave these formula types unparsed for now — they are not on the
   pilot's executable path — and pin the representation in a later change?
