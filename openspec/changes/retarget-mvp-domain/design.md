# Design

> DRAFT — needs Egor review.

## Context

The specs describe a placeholder domain. This change retargets the text and fixes the
scope; it adds no behavior beyond scope statements and a norm-reference marking rule.
It is documentation only, so performance, accessibility, and coverage are not applicable.

## Goals

- Every spec and the AI context point at the confirmed MVP domains.
- The MVP scope, the first domain's out-of-scope list, and the non-goals are written.
- Every rule has exactly one owner spec; other specs reference it.
- No norm value, edition, or clause appears without a checked source.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **Domain order: shallow foundations first, internal water supply second.** Taken
   from Akim's confirmation and `CLAUDE.md`. The kickoff file with the Decision section
   named in the task is not in the repository (assumption A1 below).
2. **Only the first domain gets a capability now.** Roadmap section 3.1 allows one new
   capability. The second domain is named in `product-vision` with a milestone.
3. **Owner spec per rule.**

   | Rule | Owner | Others |
   |---|---|---|
   | MVP scope, domain order, non-goals | `product-vision` | reference it |
   | First-domain scope and out-of-scope | `foundations-shallow` | reference it |
   | B2B/B2C limits, trial, authorization | `user-accounts` | `product-vision`, `web-platform` reference it |
   | Norm-reference marking | `normatives-catalog` | `transparent-output` follows it |

4. **Synthetic norm references.** Examples in specs use `<NORM-DOC-PLACEHOLDER>`,
   edition `unverified`, clause `<CLAUSE-PLACEHOLDER>`, and `source: unverified`, never a
   real clause number. The exact reference fields are defined by the planned change
   `norm-source-traceability` (`NormRef`), so this change does not fix a field format.
5. **Placeholders in the scope capability.** The in-scope calculation type names and the
   out-of-scope list are marked for Egor and the PM to fill. The draft does not invent
   them.

## Assumptions

- A1: the kickoff file with the Decision section does not exist in the repository; the
  domain order comes from Akim's answer in the session.
- A2: the PM's meeting list of non-goals is not in the repository; the list is the
  example list of roadmap section 3.1.
- A3: the B2C limit (100 calculations a month) is kept from the current
  `user-accounts` text in exactly one place and marked unverified until the PM approves.
- A4: MODIFIED requirements repeat the full requirement text, because OpenSpec replaces
  the whole requirement at archive. The validator also refuses a MODIFIED block that
  drops an existing scenario, so "MVP scope" (`product-vision`) and "Deterministic
  verified calculation" (`calculation-engine`) are REMOVED and re-ADDED under new names.

## Boundary

The C/C++ hot-swap boundary of the engine is not touched by this change.
