# Reference examples for `foundations-shallow`: worksheet

- Opened: 2026-09-27
- Engineer who fills it: Akim (decided 2026-09-27; the roadmap had "who this is — data needed").
- Change: `openspec/changes/calculation-verification/` (WP4), requirement "Reference examples"; `design.md` decisions 1, 2, 3, 5; tasks 2.1-2.4, 2.11, 3.7; section 5 "Follow-up".
- Purpose: collect the source, the worked examples, and the engineer's inputs that WP4 needs. Nothing in this file is a norm value; every number comes from the guide or from the engineer, with its source.

## Status

| Item | State | Blocks |
|---|---|---|
| First calculation type(s) of `foundations-shallow` | **Open**: the in-scope list is TBD (`retarget-mvp-domain` task 3.1, Egor and the PM) | Everything below; WP2 task 7.1 (pilot) |
| Bibliographic record of the guide | Open | Source citation of every example |
| 3 worked examples per calculation type | Open | WP4 tasks 2.1-2.4; step 5 (first slice) |
| Invariants specific to shallow foundations | Open | WP4 task 2.11 |
| Definition of "typical calculation" | Open | WP4 task 3.7 (30-second latency test) |

## 1. First calculation type

The guide must hold at least 3 worked examples of the type (WP4 decision 1: N = 3; fewer
makes the suite invalid). Propose the type(s) from what the guide actually covers; the
decision goes into `foundations-shallow` "In-scope calculation types" through Egor and the
PM.

- Proposed type(s): `<name as in the guide>`
- Worked examples of it in the guide: `<count>`, pages `<pages>`
- Agreed by Egor and the PM on: `<date>`, recorded in: `<tracked file or commit>`

## 2. Source record

One record for the guide. WP4 decision 2: `origin` is `textbook` for every example of this
domain.

| Field | Value |
|---|---|
| Title | |
| Authors | |
| Publisher or university | |
| Year, edition | |
| Norm documents the guide calculates with, and their editions | (becomes `source_norm_edition` per example; write `unverified` unless the edition is checked against the norm's primary text) |

WP4 decision 5: a student guide may use an older norm edition than the engine. Record the
edition the guide uses, not the current one.

## 3. Examples

Copy this block once per example; at least 3 per calculation type.

### `<example_id>`

| Field | Value |
|---|---|
| `example_id` | |
| Calculation type | |
| `origin` | `textbook` |
| Source citation | guide (section 2), year, page `<p>`, example No. `<n>` |
| `source_norm_edition` | |

Inputs:

| Quantity | Symbol in the guide | Value | Unit |
|---|---|---|---|
| | | | |

Expected outputs:

| Quantity | Symbol in the guide | Value | Unit | `tolerance` | `tolerance_kind` | `tolerance_source` |
|---|---|---|---|---|---|---|
| | | | | | `absolute` or `relative` | |

`tolerance_source`: the norm clause that sets the precision (document, edition, clause),
or, where the norm sets none, your reason as the engineer (for example, how many digits
the guide prints). The tolerance is set per quantity; WP4 fixes no number, and the
audit's "<= 0.1%" is not used (decision 3).

## 4. Engineer inputs for the other WP4 tasks

- **Invariants** (task 2.11): statements that hold for every valid input of the type,
  beyond determinism and unit-change consistency, which are shared and already covered.
  For each: identifier, statement, quantities involved, and the valid input range the
  property test may use. None is invented in the specs.
- **Typical calculation** (task 3.7): which calculation, with which inputs, counts as
  typical, and where the 30 seconds are measured. The calculation is asynchronous, so
  say whether the clock covers the engine call only or the whole job from request to
  result.

## 5. Completeness check

An example is admitted only when all of these hold (WP4 scenario "Too few or incomplete
examples"):

- [ ] At least 3 examples per calculation type
- [ ] Every expected output has `tolerance`, `tolerance_kind`, and `tolerance_source`
- [ ] Every input and output has a unit
- [ ] `origin`, the source citation, and `source_norm_edition` are filled
- [ ] No example that you do not trust (an error in the guide, another edition) is admitted
