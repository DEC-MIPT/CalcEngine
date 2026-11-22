# Transparent Output

## Purpose
Component 4: a transparent ("white box") presentation of the calculation: every step,
formula in mathematical notation (MathJax), value substitution, intermediate result,
and a link to the specific normative clause.

## Requirements

### Requirement: Detailed calculation display
The system SHALL display the full calculation trace: formulas in mathematical notation,
substituted values, intermediate results, and references to normative clauses.

#### Scenario: Inspect a calculation step
- **WHEN** a user expands a calculation step
- **THEN** the formula (MathJax), substitution, and result are shown with each normative
  reference the step rests on, for example `<NORM-DOC-PLACEHOLDER>`, edition
  `unverified`, clause `<CLAUSE-PLACEHOLDER>`, `status: unverified`

#### Scenario: Unverified reference is visible
- **WHEN** any reference of a step is marked `status: unverified`
- **THEN** the display shows that mark next to that reference

### Requirement: Expandable steps
The system SHALL allow each calculation step to be expanded and collapsed on demand, by
pointer and by keyboard, and SHALL expose the state of each step to assistive technology,
with controls that expand or collapse every step at once. Every step SHALL initially
be expanded when a result opens, including recognized loads traces, unrecognized
traces and derived diagnostic refusals. Grouping SHALL NOT change initial disclosure
state. Existing playback SHALL still control when each step is revealed and hide
pending content from keyboard and assistive technology. A collapsed header SHALL
retain the step's identity or declared symbol,
kind, stored result with unit and, for a check, text pass/fail. Every step's expression,
substitutions, result, comparison and recorded normative or engineer source SHALL
remain available by expanding that step or choosing expand all. Grouping SHALL NOT
add another disclosure action before a step can be reached.

#### Scenario: Expand a step
- **WHEN** a user clicks a calculation step header
- **THEN** that step toggles between its compact header and full details, without changing another step's disclosure state

#### Scenario: Expand a step with the keyboard
- **WHEN** a user moves focus to a step header and presses Enter or Space
- **THEN** the step expands or collapses, and the header's aria-expanded is true while expanded and false while collapsed

#### Scenario: Expanded on open
- **WHEN** a user opens any completed calculation or derived-refused result
- **THEN** every supplied step is initially expanded when revealed, with its expression, substitutions, result, comparison where applicable and recorded source visible; collapsing a step retains its result with unit in the header

#### Scenario: Grouped loads on open
- **WHEN** a completed or derived-refused result whose trace matches the complete typed loads signature opens
- **THEN** each available step header shows its identity or symbol, kind and stored result with unit, check headers retain text pass/fail, and all details start expanded without omitting any stored step

#### Scenario: Expand or collapse all
- **WHEN** a user chooses expand all or collapse all
- **THEN** every step's details are expanded or collapsed accordingly, preserving original step order and header summaries

#### Scenario: Inspect retained source details
- **WHEN** a user expands a compact loads step or chooses expand all
- **THEN** its original expression, all substitutions with units, result, check comparison where applicable and recorded normative or engineer source are available under the existing source-status rules

### Requirement: Normative clause references
The system SHALL show, for every normative calculation step, each `NormRef` in the `norm_refs` the engine recorded
for that step, together with its status as defined by the `normatives-catalog`
requirement "Norm reference status". The display SHALL NOT present an unverified
reference as verified and SHALL NOT invent or complete a reference. In the pilot's first iteration
(while the pilot is shown only inside the team: the two developers and the PM; `frontend-app`
design.md, decision 12) the setting `SHOW_NORM_STATUS` is off, and the trace SHALL then show the
references of its steps without a status mark (neither verified nor unverified) and without the
summary of unverified steps; the document, edition and clause are still shown as recorded, and the
refusal and the warnings keep the status of their sources.

#### Scenario: Verify the reference
- **WHEN** a step displays a normative reference with `SHOW_NORM_STATUS` on
- **THEN** the displayed document, edition, clause, and status are exactly those of each
  `NormRef` in the step's `norm_refs`, and a reference that is not verified is shown as unverified

#### Scenario: Status not shown in the pilot's first iteration
- **WHEN** a step displays a normative reference with `SHOW_NORM_STATUS` off
- **THEN** the displayed document, edition and clause are exactly those of the `NormRef`, and no
  status mark is shown, so an unverified reference is never shown as verified

Engineer_formula steps SHALL instead identify the source engineer and rationale,
without a normative status badge or invented NormRef. This engineer-source display
SHALL NOT be hidden by SHOW_NORM_STATUS, which controls only normative status.

#### Scenario: Engineer source remains visible
- **WHEN** SHOW_NORM_STATUS is off and an engineer_formula step is shown
- **THEN** its EngineerRule attribution remains visible and is not presented as verified normative data

### Requirement: Non-functional — completeness
The system SHALL render 100% of calculation steps with correct mathematical notation
in a cross-browser compatible way.

#### Scenario: Full transparency
- **WHEN** a calculation completes
- **THEN** every step is displayed with MathJax-rendered formulas across supported browsers

### Requirement: Trace display consumes typed steps and warnings
The system SHALL render the trace from the typed trace steps and the result envelope of
the `calculation-engine` capability, without recomputing any value, and SHALL show the
envelope's `outputs`, applicability warnings, and refusals. In the pilot's first iteration the
setting `SHOW_ROUNDING_SOURCE` is off, and the outputs are then shown without their
`rounding_source` (it stays in the envelope and in the report).

#### Scenario: Every step field rendered
- **WHEN** a user opens a completed calculation
- **THEN** each step makes its expression, substitutions with units, result with unit and norm_refs or explicit engineer source available in its expandable details, and each check step also exposes its comparison, right-hand value with unit and text pass/fail; compact loads headers retain the stored result and check status without relying on colour

#### Scenario: Outputs with rounding rule shown
- **WHEN** a user opens a completed calculation with `SHOW_ROUNDING_SOURCE` on
- **THEN** each entry of the envelope's `outputs` is shown with its value, its unit, its
  `rounding_rule`, and its `rounding_source`; a rule set by the engineer is shown as
  engineer-set with the engineer and the rationale

#### Scenario: Outputs in the pilot's first iteration
- **WHEN** a user opens a completed calculation with `SHOW_ROUNDING_SOURCE` off
- **THEN** each entry of the envelope's `outputs` is shown with its value, its unit and its
  `rounding_rule`, and with no `rounding_source`

#### Scenario: Unverified steps counted
- **WHEN** the envelope's `unverified_step_count` is greater than zero and `SHOW_NORM_STATUS` is
  on
- **THEN** a summary above the trace shows `unverified_step_count`

#### Scenario: Validated-range warning shown
- **WHEN** the envelope carries an applicability warning
- **THEN** the warning is shown next to the result and names the input, the violated
  bound of the validated range, and that bound's source; a source set by the engineer is
  shown as engineer-set
  with the engineer and the rationale

#### Scenario: Refusal shown
- **WHEN** the envelope reports a refused calculation
- **THEN** the UI shows the historical bound reason or typed derived quantity, value,
  limit, source and limiting_corner, without final output values

#### Scenario: Warning readable without colour
- **WHEN** a warning or a refusal is shown
- **THEN** its meaning is conveyed by text that assistive technology can read, not by
  colour alone

A derived refusal SHALL show its completed diagnostic prefix as incomplete
calculation evidence, never as final outputs or passed bearing checks. No value,
corner choice or reason SHALL be recomputed by the client.

#### Scenario: Computed corner diagnostic
- **WHEN** the loads result is refused on p_corner_min
- **THEN** the stored limiting_corner and diagnostic prefix are shown immediately, with no final output table or bearing verdict

### Requirement: Parameter source label on the result screen
The result screen SHALL show, for every result whose envelope carries `parameter_source`,
which source supplied the norm-given parameters: for kind `catalog` the words for the
normative catalog; for kind `interim` the words for the interim normative data, the profile
and the data digest (its first 12 hex characters shown, the full digest available as
screen-reader text). A
`draft` profile SHALL be marked in words, not by colour alone. The label SHALL appear with
the verdict stamp of a checked result and in the refusal view. A result without
`parameter_source` (stored before this field existed) SHALL show no label and no error.

#### Scenario: Interim result labelled
- **WHEN** a result with `parameter_source` of kind `interim`, profile `strict` and a digest
  is opened
- **THEN** the stamp names the interim data, the profile `strict` and the start of the digest,
  and the full digest is readable by a screen reader

#### Scenario: Draft marked in words
- **WHEN** the profile is `draft`
- **THEN** the label says in words that the data are draft data, and the axe check of the
  screen passes

#### Scenario: Refusal labelled
- **WHEN** a refused result carries `parameter_source`
- **THEN** the refusal view shows the same label

#### Scenario: Older result without the field
- **WHEN** a stored result has no `parameter_source`
- **THEN** the screen shows no source label and renders as before

### Requirement: Trace steps named by their symbols
The result screen SHALL name each trace step, in its header and on the trace ruler, by the LaTeX
symbol of the quantity it computes, typeset as a formula, and SHALL keep the step's `step_id` as
text that assistive technology reads. The symbol is taken from the step itself: for a check step
the whole `expression`; for another step the left side of `expression` before its first `=` that
is not inside braces; for a table step without such an `=` the whole `expression`. A step whose
symbol cannot be found this way is named by its `step_id`, shown as code. A substitution is
typeset by the symbol of the step that computed the substituted quantity, or by the `symbol` of an
input or output in `GET /calculation-types`; a name that two types declare with different symbols,
or that is not found, is shown as code. This reading of `expression` as "left side = right side" is
a display convention of the frontend, not part of the `calculation-engine` contract; the pilot's
engine writes its table steps in this form (task 10.7), and a step that does not follow it falls
back to its `step_id`.

#### Scenario: Check step named by its expression
- **WHEN** a check step with the `step_id` `p_le_R` and the expression `p \le R` is shown
- **THEN** its header shows the typeset `p \le R`

#### Scenario: Substitution typeset by its symbol
- **WHEN** a step substitutes `phi_II`, an input whose `symbol` in `GET /calculation-types` is
  `\varphi_{II}`
- **THEN** the substitution shows the typeset `\varphi_{II}`

#### Scenario: Name declared differently by two types
- **WHEN** two types of the listing declare the input `b` with different symbols, and no step
  computes `b`
- **THEN** a substitution of `b` shows `b` as code

#### Scenario: Step named by its symbol
- **WHEN** a formula step with the `step_id` `R` and the expression `R = \frac{...}{...}` is shown
- **THEN** its header shows the typeset symbol `R`, and assistive technology also reads `R` as the
  step's identifier

#### Scenario: Step without a symbol
- **WHEN** a step's expression has no `=` outside braces and the step is not a table or check step
- **THEN** the step is named by its `step_id`, shown as code

### Requirement: Values of an output shown by its rounding rule
On the result screen, every value of an output quantity (the result of the step whose `step_id`
is that output, a substitution of its symbol, a side of a check, and the comparison in the verdict
stamp) SHALL be shown rounded by that output's `rounding_rule` from the envelope, in its mode as
the backend applies it and with exactly the rule's number of decimals (trailing zeros kept), in the
number format of the interface language. A check whose rounded sides would read against its
`passed` (for example, two sides that round to the same value while a `≤` check failed or a `<`
check passed) SHALL be shown with unrounded values. This is formatting for display: the envelope and its trace
keep the unrounded values, and nothing is recomputed (`calculation-core-contract`
`transparent-output` "Trace display consumes typed steps and warnings").

#### Scenario: Output rounded in the trace
- **WHEN** the envelope's output `R` has the illustrative value 168.2857 and a rule of 2 decimals,
  half up
- **THEN** the result of the step `R`, the substitution of `R` in the check and the stamp all show
  `168,29`

#### Scenario: Trailing zeros of the rule
- **WHEN** the output `R` has the illustrative value 172.5 and a rule of 2 decimals
- **THEN** every value of `R` on the screen shows `172,50`

#### Scenario: Rounding that would contradict a failed check
- **WHEN** the check `p ≤ R` failed and both sides round to the same value
- **THEN** the check and the stamp show both sides unrounded

#### Scenario: Rounding that would contradict a passed check
- **WHEN** the check `p < R` passed and both sides round to the same value
- **THEN** the check and the stamp show both sides unrounded

### Requirement: Result screen reading aids
The result screen SHALL show, under the result heading, a trace ruler with one tick per step that
links to that step (`#trace-step-<i>`) and ends with the verdict's mark, and SHALL offer in the
verdict stamp a link to the start of the trace that names the number of steps. A dimensionless
quantity SHALL be shown without a unit designation; in a table cell it shows «—», with text for
assistive technology that names the quantity as dimensionless.

#### Scenario: Ruler link
- **WHEN** a user chooses the third tick of the trace ruler
- **THEN** the page moves to the third step of the trace

#### Scenario: Ruler end and stamp link
- **WHEN** a result with nine steps and the verdict `pass` is shown
- **THEN** the ruler has nine ticks and ends with the mark of a passed check, and the stamp offers
  a link that names nine steps and moves to the start of the trace

#### Scenario: Dimensionless output
- **WHEN** an output has the unit `1`
- **THEN** its value is shown without a designation, and its unit cell shows «—» with text that
  says the quantity is dimensionless

### Requirement: Compact loads trace sections
The system SHALL recognize the compact loads view only when all of these stored
step identifiers occur exactly once with kind=engineer_formula: A, Wx, Wy, Mx_base,
My_base, p_corner_pp, p_corner_pm, p_corner_mp, p_corner_mm and p_corner_min.
Recognition SHALL inspect identifiers, kinds and occurrence counts only, without
values or expression-text heuristics or an added API field. If any signature member
is absent, duplicated or has another kind, the trace SHALL use the existing flat,
initially expanded view. Unknown supplemental steps SHALL NOT prevent recognition
of an otherwise complete signature.

For recognized traces the frontend SHALL place semantic headings inside the same
flat ordered list for resistance R, geometry and load transfer, mean pressure, pressure along X,
pressure along Y, corner pressures, contact envelope, and bearing limits/checks.
Headings SHALL label contiguous runs of recognized stored steps, preserving every
step's original order, zero-based index, anchor and ruler tick. Headings SHALL add
no list items or nested step lists. Empty sections SHALL be absent. Unrecognized steps SHALL remain at their original positions in a neutral
contiguous section. The frontend SHALL NOT merge component and engineer-rule steps,
recompute pressures, change a source attribution or infer a missing calculation step.

Headings SHALL NOT have independent collapse controls. Existing playback SHALL
continue to reveal original step headers in order and hide pending steps from
keyboard and assistive technology; each heading SHALL appear with its first revealed
step. Playback completion SHALL NOT reset the user's disclosure choices. Derived
refusals SHALL immediately expose their complete prefix headers, reason and correction
action, with all diagnostic details initially expanded and still controlled by
existing per-step/global disclosure, without a final output table or bearing verdict. Historical pilot traces
SHALL retain their current initial expansion and presentation.

#### Scenario: Completed loads trace grouped without loss
- **WHEN** a stored completed trace with the complete typed loads signature is presented compactly
- **THEN** every stored step has exactly one header under its contiguous semantic section, in original order with unchanged anchor indices, and its complete stored details are initially expanded and can be collapsed and reopened

#### Scenario: Unknown or missing non-signature steps
- **WHEN** a trace with the complete typed loads signature has an unrecognized supplemental step or lacks a recognized non-signature step
- **THEN** the supplemental step remains inspectable in a neutral run at its original position, no missing step is synthesized and no empty section is shown

#### Scenario: Incomplete or unrecognized trace
- **WHEN** any required loads-signature step is absent, duplicated or has a different kind, or no loads signature is present
- **THEN** every supplied step remains in original order in the existing flat, initially expanded view, with no loads-specific headings and no inferred replacement step

#### Scenario: Ruler and playback preserve original indices
- **WHEN** playback advances or a ruler tick is chosen in a compact loads trace
- **THEN** it addresses the same original step index and anchor as the stored trace, and pending step content remains inaccessible until revealed or playback is skipped

#### Scenario: Compact derived diagnostic prefix
- **WHEN** a derived-refused result with the complete typed loads signature opens
- **THEN** all stored diagnostic headers and their result summaries plus the refusal reason are immediately available without playback or group disclosure, all stored details are initially expanded and remain individually/globally collapsible and no final output or bearing verdict is introduced

#### Scenario: Historical pilot remains expanded
- **WHEN** a foundations_shallow_r result opens
- **THEN** its trace remains initially expanded with its existing order, reading aids and controls, without loads-specific section headings
