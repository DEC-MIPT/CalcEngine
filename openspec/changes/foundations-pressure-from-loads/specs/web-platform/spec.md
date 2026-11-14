## MODIFIED Requirements

### Requirement: Form draft and the edit-inputs action
The frontend SHALL keep the values and unit choices of an input form, for each calculation type, in
the memory of the open page for as long as the page is open, and SHALL restore them when the form of
that type is opened again, also by the browser's back action. The draft (the values and units typed into a form, not the inputs that a stored result itself
shows in its steps) SHALL NOT be written to browser storage, to the address, to the console or to
any screen other than the form's own fields.
The result screen SHALL offer an "edit inputs" action that opens the form of the type just
calculated with that draft, only for the result that the draft was last sent for; any other result
(opened by its address alone, or reached again by the browser's history after another calculation)
offers no such action. For historical input-bound refusals, bound.quantity is a registered input.
For a derived refusal, related_inputs names registered inputs and the diagnostic
quantity SHALL NOT be treated as an input. For a refusal the action SHALL be the
screen's main action and the link to the report request its second action, and the form it opens SHALL focus the bound input for a historical refusal, or the
first related_input for a derived refusal, and show the readable reason nearby.
Existing eligibility remains limited to the last submitted result of that draft.

#### Scenario: Back keeps the values
- **WHEN** a user fills the form, submits, and returns to the form with the browser's back action
- **THEN** every field shows the value and the unit that was entered

#### Scenario: Edit inputs after a result
- **WHEN** a user opens "edit inputs" on the result just calculated
- **THEN** the form of that type opens with the entered values and units, and they can be changed
  and sent again

#### Scenario: Edit inputs after a refusal
- **WHEN** a user opens "edit inputs" on a refusal whose bound is on the input `b`
- **THEN** the form opens with the entered values, focus is in the field of `b`, and the violated
  bound is shown next to that field in text

#### Scenario: Result opened by its address
- **WHEN** a user opens a result by its address in a new page, or after a reload
- **THEN** the screen shows the result and no "edit inputs" action, and no draft value of an
  earlier calculation is present on the page

#### Scenario: Earlier result after a newer calculation
- **WHEN** a user calculates twice in one page session and returns by the browser's history to the
  first result
- **THEN** the screen shows that result and no "edit inputs" action

#### Scenario: Edit a derived refusal
- **WHEN** the derived refusal belongs to the eligible in-memory draft and edit inputs is chosen
- **THEN** the existing draft is restored and its first related_input is focused, without inventing a p_corner_min input

### Requirement: Trace playback on first showing
The first time a stored result is shown in a page session, and unless the user's system asks for
reduced motion, the result screen SHALL show the trace steps one by one, at an interval of
600 ms or of 10 s divided by the number of steps, whichever is shorter, so the whole playback takes
at most 10 s. A pointer click, Space, Enter, Escape or Tab SHALL end the playback and show every
step at once. Steps not shown yet SHALL NOT be reachable by keyboard or read by assistive
technology. Until the last step is shown, the content of the verdict stamp SHALL be hidden from
sight, and the values of the outputs table hidden from sight, keyboard and assistive technology,
with the status «ВЫПОЛНЕНИЕ РАСЧЁТА» in their place and the heading and frame of the outputs table
kept, so the trace does not move when they appear. The stamp keeps its accessible name, so the
focus of "Verdict focus on arrival" announces the verdict at once and assistive technology does not
wait for the playback; the stamp region is a live region, polite for a `pass` and assertive for a
`fail`. After the last step a `pass` with no warning SHALL be revealed with an expressive stamp (a
scan line from 200 ms, the content and the output values at 520 ms, a drawn check mark complete by
1.9 s after the last step), and a `fail` or a `pass` with a warning at once; an input-bound refusal has no steps and shows at once; a derived refusal may
contain diagnostic steps, but its reason and complete prefix SHALL also show at
once, with no delayed reveal or success animation. A result shown again in the same page session, or shown while the system asks
for reduced motion, shows every step, the verdict and the outputs at once.

#### Scenario: First showing of a result
- **WHEN** a non-refused pass/fail result with nine steps is shown for the first time in a page session
- **THEN** the steps appear one by one, the stamp and the output values are held with the status
  «ВЫПОЛНЕНИЕ РАСЧЁТА» until the last step, and then they are shown

#### Scenario: Long trace
- **WHEN** a non-refused pass/fail result with 40 steps is shown for the first time in a page session
- **THEN** the steps appear 250 ms apart, and the last one appears 10 s after the first showing at
  the latest

#### Scenario: Playback skipped
- **WHEN** a user clicks, or presses Space, Enter, Escape or Tab, during the playback
- **THEN** every step, the verdict and the output values are shown at once

#### Scenario: Verdict announced on arrival
- **WHEN** a result is shown for the first time and the playback starts
- **THEN** focus is on the verdict stamp and its accessible name is the verdict, while the stamp's
  content is hidden from sight until the last step

#### Scenario: Result shown again
- **WHEN** the same result is shown again in the page session
- **THEN** every step, the verdict and the output values are shown at once, with no playback

#### Scenario: Diagnostic refusal is immediate
- **WHEN** a derived refusal with trace steps is opened for the first time
- **THEN** its complete diagnostic prefix and reason are immediately accessible, outputs remain absent and no success animation plays
