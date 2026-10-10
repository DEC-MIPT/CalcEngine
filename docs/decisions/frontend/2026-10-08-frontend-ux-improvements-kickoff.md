# Frontend UX improvements: kickoff questions

Date: 2026-10-08. Author: Akim's Claude Code session. Addressee: Akim.

## Context

The heuristic review of `feature/frontend-app/frontend` (HEAD `facb151`) is in
`docs/akim/frontend-heuristic-review-2026-10-08.md` (untracked, Akim's zone). It is an expert review,
not a usability test. Its findings that need no decision and are not asked here: the four P0 defects
(form lost on "Back", no "edit inputs" action on a result or a refusal, the false inequality in the
fail stamp, the server `422` that does not mark its field, and the unit switch that silently changes
the meaning of a number) and the P1/P2 lists are to be fixed; the layout has no horizontal scroll from
1440 down to 320 px and stays as it is.

This file asks only what the report leaves to Akim. Each answer goes into the `Decision` line of its
question. Anything that adds a number to the screen (question 2, item B) or a contract field needs an
OpenSpec change first (`AGENTS.md` section 2); this file does not replace one.

## Question 1. Direction: keep, adjust, or revisit "technical terminal"

### Options

- **A. Keep, adjust locally (the report's recommendation).** Keep `frontend-app` design decision 5. Take
  the missing half of its own brief into the screens: the instrument readout (value, unit and tolerance
  state in one line) and dimension-line ticks used as content, not as an underline.
  - For: the only memorable element today, the verdict stamp, is the most "terminal" part; no finding
    traces back to the style; the fix cost is in layout and content, not in tokens; no rework of the
    accessibility checks already done.
  - Against: the direction is applied to the surface only, so a reviewer may still read the other
    screens as a plain admin page; the benefit depends on question 2 being done, otherwise "adjust"
    means nothing visible.
- **B. Keep as is.** Fix P0-P2 defects only, no new visual device.
  - For: smallest scope, no new decision for OpenSpec.
  - Against: leaves the memorability finding open: one element per product is thin.
- **C. Revisit the direction.**
  - For: a calmer or warmer look could feel friendlier to some users.
  - Against: the review found no defect caused by the style; the previous brief (a minimal drafting
    sheet) was already judged too sparse on 2026-10-06; a third change of direction costs more than it
    returns before any test with engineers.

Recommendation: A.

### Decision

Option A (2026-10-08, Akim, in chat): keep "technical terminal" and adjust locally.

## Question 2. Which micro-interactions go into the first iteration

### Options

The report lists eight points (section 8). Proposed first iteration: **four**, chosen for effect on
memorability and responsiveness against risk. Pick, replace or shrink.

| # | Point | Effect | Risk | Needs OpenSpec |
|---|---|---|---|---|
| 5 | "Edit inputs" on the refusal and the result: back to the form with kept values, focus in `b`, the bound under the field | removes the heaviest finding; responsiveness of the whole path | low: state kept in memory above the routes, no storage | no (a form behaviour of `frontend-app`; check its wording) |
| 1 | Unit select: echo "= 0,02 m" under the field for ~2 s | prevents a 100x error; instant feedback on a control | low: display only, the engine gets what was typed | no |
| 3 | Stamp reveal: focus moves to the stamp, the frame draws in 120 ms, then the verdict word | the one moment people will remember; fixes focus after navigation | low if reduced-motion is honoured | no |
| 2 | Calculate button while sending: stepped 1 px bar, fields `readonly`, text after 3 s and 10 s | answers "what is happening" | low-medium: `readonly` fields change the form's behaviour while a request is open | no |

Left for later and why: **4** (utilisation scale: highest memorability, but it adds a derived number, so
it needs a calculation-contract decision first, see item B below); **6** (field-level `422` link: a defect
fix, goes with P0-3 regardless of this choice); **7** (stamp-to-step jump) and **8** (file name from the
document designation: backend-side `Content-Disposition`).

Item B, a related choice: whether to start the OpenSpec change for the utilisation scale (point 4) now,
in parallel, so that it is ready for iteration two, or to wait for the engineers' test.

- B1. Start the change now. For: the scale is the strongest answer to "how much margin", and the test
  can then check it. Against: spec work before evidence.
- B2. Wait for the test. For: no spec work on a guess. Against: iteration two starts later.

Recommendation: points 5, 1, 3, 2 as above; B1 only if the change stays small (one derived number, its
rounding rule from the norm or from the engineer's rule, in the engine, never in the UI).

### Decision

First iteration: points 5, 1, 3 and 2 (Akim, 2026-10-08, in chat). Item B: B1, start the OpenSpec change for the utilisation scale now, on the condition that it stays small (one derived number, its rounding rule from the norm or from the engineer, calculated in the engine, never in the UI).

## Question 3. Responsive typography: `clamp()` or breakpoints

### Options

- **A. Fluid with `clamp()`.** Sizes scale continuously between a minimum and a maximum.
  - For: no jumps, one rule per size.
  - Against here: the form and the tables use fixed rem columns (`w-36`, `15.5rem`, `w-24`); text that
    grows continuously while the columns do not will wrap or crowd the value cell at some widths. A
    fractional pixel size makes digit columns render with uneven sub-pixel widths. Note on the
    monospace worry: within one face (Geist Mono) digits keep equal advance at any size, so columns do not
    "drift between fonts"; the real risks are the fractional sizes and the fixed columns above.
- **B. Breakpoints with fixed steps.** A few sizes (for example at 640 and 1024 px), as the layout already
  does (`sm:` variants).
  - For: every size is a whole pixel, tested once in a screenshot; matches the current Tailwind use and
    the 95% coverage / Playwright checks.
  - Against: a visible step at each break; more rules to keep in step.
- **C. Hybrid (recommended).** Body, labels, inputs, table cells: fixed steps, whole pixels. `clamp()`
  only for display text that is not in a column: the page heading and the stamp's verdict line, bounded
  by a minimum and a maximum so that nothing falls below the WCAG 2.2 AA target size or the 200% zoom
  reflow already passing at 320 px.

### Decision

Option C, the hybrid (Akim, 2026-10-08, in chat): fixed whole-pixel steps for body text, labels, inputs and table cells; `clamp()` only for the page heading and the stamp verdict line, bounded by a minimum and a maximum.

## Question 4. How bold the micro-interactions are

### Options

- **A. Quiet, near the threshold of notice.** Colour or 1 px changes, 100 ms, no movement.
  - For: no conflict with the seriousness of an engineering tool.
  - Against: the risk is that nobody notices, and then point 3 does not do its memorability job.
- **B. Measured, one expressive moment (recommended).** Quiet everywhere except one: the stamp reveal
  (frame drawn in 120 ms, then the verdict). Controls (unit echo, button state) stay quiet.
  - For: one memorable moment, tied to the product's actual value, a result; fits "precise and
    mechanical" motion of `frontend-app` decision 5.
  - Against: if the stamp reveal is read as showy by the engineers, it is the first thing to cut.
- **C. Expressive throughout.** Every action animates visibly.
  - For: feels alive.
  - Against: conflicts with the brief (no springs, bounces or overshoot), slows a user who repeats the
    same calculation many times, and most of the motion carries no information.

All options keep `prefers-reduced-motion` (already honoured: spinner stops) and never carry meaning by
colour alone.

### Decision

Option B, measured with one expressive moment (Akim, 2026-10-08, in chat): quiet everywhere except the stamp reveal.

## Question 5. A usability test with engineers after this iteration

The report (section 9) proposes a moderated test: 5 design engineers, 30-40 minutes each, think-aloud,
five scenarios (a check with mixed units, "it failed, change it", a width outside the validated range, two
reports in a row, "where does 172.5 come from"), measuring task success, time to the verdict, re-entries,
unit errors, the answer to "by which norm did it count", a single-ease question after each task, and the
open question "how is this different from your Excel sheet".

### Options

- **A. Plan it explicitly as the step after this iteration, not instead of it (recommended).** The
  iteration ships first (P0 defects and the chosen micro-interactions); the test then judges the result.
  Record it as a named task, with a place to find five engineers (a PM question: Yesenia).
  - For: the heuristic review only prepares hypotheses; some of its findings (the false inequality, the
    memorability verdict) are expert guesses that only a test can confirm.
  - Against: costs engineers' time and a recruiting task for the PM.
- **B. Leave it unplanned for now.**
  - For: no commitment.
  - Against: the iteration's conclusions stay unverified; nothing in the repo says when they will be.

### Decision

Option A (Akim, 2026-10-08, in chat): plan the usability test with engineers as a separate task after this iteration, not instead of it. The question to the PM (Yesenia) about where to find five engineers is still to be asked.
