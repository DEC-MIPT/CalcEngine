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

## Answers (Akim, 2026-10-05)

I agree not to push formulas with Σ/∏/systems through sympy now. Three refinements to the
diagnosis change the answer to question 2.

**The parser is not the main barrier.** I checked `latex2sympy2==1.9.1` and the `lark`
LaTeX parser built into sympy 1.14:

| Formula | `latex2sympy2` | sympy `lark` |
|---|---|---|
| `\sum_{i=1}^{n} h_{i}` | parses | parses |
| `\prod_{i=1}^{n} k_{i}`, nested Σ | parses | parses |
| `\beta\sum_{i=1}^{n}\frac{(a_{i}-b_{i})h_{i}}{E_{i}}` | error | parses |
| the same with `\sigma_{zp,i}` | error | error (on the compound subscript) |
| `cases` | error | error |

The syntax can be covered: the `lark` parser plus the normalization of compound
subscripts that you already do for Cyrillic.

**But parsing gives the wrong meaning.** Both parsers take `h_{i}` for a constant symbol,
not an element of a series: `Σ h_i` becomes `n·h_i`. "Parses in sympy" is therefore not
"correct". It is good that your `_to_node` refuses the `Sum` node: no such formula reached
the catalog.

**The real barrier is the input model.** Our type inputs are scalars, while Σ in the
foundation norms runs over soil layers, each with its own values, and `n` is often not
given but set by a condition, that is, an algorithm. This already concerns the pilot:
formula (5.7) has no sum, but under clause 5.6.10 `γII`, `γ'II` and `cII` are
weighted averages over the layers within a depth `z` that depends on `b`. Today the user
averages them outside the system.

**1. The `form`/`kind` mark.** Yes, but only in your tables: for search, display, and to
track what is not executable yet. Do not expose it in the `catalog_read` views: the
backend has no consumer for it, and the contract stays as it is. I suggest the values
`sum`, `product`, `piecewise`, `system`. Keep `piecewise` apart from `system`: piecewise
definitions are already handled by branches plus a threshold (as `k_z`), true systems of
equations are not.

**2. How the engine receives Σ/∏.** Neither a `Formula` with an empty tree nor a new
parameter type. I propose "aggregation in the calculator, the term in the catalog":

- The type's inputs gain a list, for example `layers: [{h: m, E: kPa, ...}]`, with a unit
  per field. This is my part.
- You bind the **term** as an ordinary formula tree with scalar symbols: the index
  dropped (`sigma_zp,i` -> `sigma_zp`), with units and the `NormRef` of the formula's
  clause, under a synthetic number like `5.6.7#k_z_below`, for example `5.16#term`.
- The type's calculator walks the layers in a fixed order, calls `formula_step` on each
  and adds the results. The report gets a step per layer and a final step. The order of
  summation is fixed, so the result is reproducible bit for bit.
- Why not "parameters: operator, limits, operand". The operand is an expression and
  needs a tree anyway; the limits `1..n` are the length of an input list, not a norm
  value; and an operand passed as text would break the spec rule "the backend SHALL NOT
  parse a formula's text or LaTeX".
- Piecewise definitions: branches plus a threshold, as `k_z`. True systems of equations:
  outside the MVP.

**3. Leaving them unparsed for now.** Yes. They are not bound, and a type that needs such
a formula answers `503` (scenario "A formula outside the form"), which is right. We pin
the representation in a separate change, the one that introduces list inputs. Akim leads
it (input contract, engine, form, report); your part is the binding of terms and the
`form` mark. The first candidate may be the pilot itself (the averaging of clause
5.6.10), then settlement by (5.16) and piles. The timing depends on the MVP scope, which
we decide with the PM.

**Table 5.5 and a non-integer `φII`.** I checked page 38 of СП 22.13330.2016 (table 5.5):
the table gives no interpolation rule. For comparison, table 5.4 has one (note 3, for
L/H). The backend therefore keeps selecting a row only by an exact heading match, and a
non-integer `φII` inside [0°, 45°] gets `422`, which is right: a rule for intermediate
values can come only from the norm's text (`agent-docs/domain-constraints.md`). For a
layered base, where a weighted `φII` is almost always non-integer, this is a limit of the
pilot and part of the MVP scope decision we take with the PM. Nothing is needed on the
data side: the rows per whole degree, as stored now, are enough.
