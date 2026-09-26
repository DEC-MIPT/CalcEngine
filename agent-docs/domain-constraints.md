# DEC — Domain Constraints for Agents

Agent-neutral rules for anything that touches calculation logic, normative data, or
requirements that describe them. Read by Claude Code (via `CLAUDE.md`) and by Kilo Code.
These are interim: the target home is the `calculation-engine` and `normatives-catalog`
specs, through a future OpenSpec change (see planned change `norm-source-traceability`).

## Calculation functions

- Calculation functions MUST be pure: no I/O, no clock, no randomness, no global or
  mutable state, no network or database access inside the function.
- Calculation functions MUST be deterministic: the same inputs and the same norm
  version always produce the same output, bit for bit on the same platform.
- Reproducibility: a result is identified by (inputs, norm document, norm edition).
  A stored result MUST record all three so it can be re-run and compared later.
- Units are explicit: every input, output, and constant carries its unit, and unit
  conversion happens at the boundary, never implicitly inside a formula.
- No ML in the calculation path. Rounding and tolerance rules come from the norm,
  not from the implementer.

## Norm references

- Cite a norm only from its primary source text (the official document), never from
  memory or from a model's recollection. This applies to agents too.
- A citation names the document, its edition or year, and the clause. If the source
  text is not available, write `source: unverified` and do not invent a clause number.
- Norm editions named in the repository or by the team but not yet checked against the
  source text are `unverified` until Egor's normative pipeline confirms them.
- Never change a norm value, coefficient, or limit without the source clause and the
  edition it comes from.

## Requirements that describe calculations

- A requirement that fixes a formula, coefficient, or limit SHALL state its norm
  source (document, edition, clause) next to it. The exact field format is not yet
  defined in the specs and is part of the planned change `norm-source-traceability`.
