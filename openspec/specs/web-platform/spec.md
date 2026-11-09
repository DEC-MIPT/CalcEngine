# Web Platform

## Purpose
Component 3: a single web platform combining the normative base, the calculation
engine, and the report generator. Frontend in React + TypeScript, backend in FastAPI,
with a single authorization and no manual data transfer between components.

## Requirements

### Requirement: Unified web interface
The system SHALL present the normative base, the calculation flow, and the report
generation in a single React + TypeScript interface served by a FastAPI backend.

#### Scenario: Single window flow
- **WHEN** a user moves from selecting a calculation to entering inputs and exporting
  a report
- **THEN** all steps happen in the same interface without switching applications

### Requirement: Calculation input form
The system SHALL provide a web form for entering the inputs of the selected calculation
type, with the fields defined by that type's typed input contract, and with validation
before submission. The form SHALL NOT hard-code the fields of one calculation type.

#### Scenario: Enter and validate inputs
- **WHEN** a user selects an in-scope calculation type, fills the form, and submits
- **THEN** inputs are validated against that type's contract and sent to the calculation
  engine via the backend

#### Scenario: Different calculation type
- **WHEN** a user selects another calculation type
- **THEN** the form shows that type's fields without a code change to the form component

### Requirement: Single authorization
The system SHALL apply the authorization model owned by the `user-accounts`
capability across the normative base, the calculation engine, and the report generator,
and SHALL NOT define authorization rules of its own.

#### Scenario: One login for the whole platform
- **WHEN** a user signs in once
- **THEN** the identity and plan rules from `user-accounts` apply to all platform
  components

### Requirement: Backend API
The system SHALL expose a FastAPI backend with OpenAPI documentation and Pydantic
validation for all calculation and normative requests.

#### Scenario: Inspect the API
- **WHEN** a developer opens the API documentation
- **THEN** all calculation and normative endpoints are documented with schemas

### Requirement: Non-functional — integration and latency
The system SHALL integrate all components with 100% data-passing between them and
sub-second transition between components.

#### Scenario: Seamless component transition
- **WHEN** data moves between the normative base, engine, and report generator
- **THEN** no manual transfer is required and the transition completes in under 1 second

### Requirement: User journey and screens
The system SHALL provide four screens in one interface, each with its own address: type
selection (`/`), input form (`/calculations/new?type=<name>`), result (`/calculations/<id>`),
and report request (`/calculations/<id>/report`). The journey runs type selection, input form,
result, report request, and every transition below SHALL happen without leaving the interface.
A result SHALL be openable by its address alone, also after a page reload.

#### Scenario: Select a type
- **WHEN** a user chooses a calculation type on the type selection screen
- **THEN** the input form of that type opens, with the type's name in the address

#### Scenario: Submit valid inputs
- **WHEN** a user submits a valid form
- **THEN** the calculation is requested from `POST /calculations` and the result screen opens at
  the address of the stored result

#### Scenario: Submit invalid inputs
- **WHEN** the backend answers `422` to a submitted form
- **THEN** the user stays on the input form with every entered value kept and each reported field
  marked (see "Input form built from the type's contract")

#### Scenario: Refused calculation
- **WHEN** the stored result has the verdict `refused`
- **THEN** the result screen opens and shows the refusal and no result value
  (`transparent-output` "Trace display consumes typed steps and warnings")

#### Scenario: Open a result by address
- **WHEN** a user opens `/calculations/<id>` of a stored result, or reloads that page
- **THEN** the result is read with `GET /calculations/{result_id}` and shown without a new
  calculation

#### Scenario: Unknown result
- **WHEN** a user opens the address of a result the backend does not know
- **THEN** the screen says that the result was not found and offers a link to type selection

#### Scenario: Go to the report
- **WHEN** a user chooses to request a report on the result screen
- **THEN** the report request screen of that result opens

#### Scenario: Backend not available
- **WHEN** the backend answers `503` (for example `parameter_source_unavailable`) or cannot be
  reached
- **THEN** the screen says in text that the calculation is not available now, shows the error's
  `code`, and offers a retry that repeats the same request

### Requirement: Input form built from the type's contract
The frontend SHALL build the input form of a calculation type only from the entry of that type in
`GET /calculation-types`: one field per declared input, in the declared order, with the input's
`label` and `symbol` (rendered as formula), its `hint` when it has one, and a unit choice limited
to the input's listed `units`, preset to its `base_unit`; for an input with `whole_values_only` the
unit choice is fixed to its `base_unit`, so the value is whole in the unit in which the type
selects its table row. No field, label, unit or limit of a type
SHALL be written in the frontend code (the display-only factors of "Unit echo in the base unit" and
the Russian designations of the units, with the unit code shown in English, are the unit
vocabulary shared by all types, not a unit of a type; they are spelled as the report's fixed table of
`report-generator` "Report values, formulas and dates"). Before submission the form SHALL check that every field is
filled, that the value is a finite number, and, for an input with `whole_values_only`, that the
value is a whole number (a number equal to its integer part, so `30`, `30.0` and `30e0` are
accepted and `30.5` is not); a decimal comma SHALL be accepted as well as a decimal point, so
`172,5` is read and sent as the number 172.5 while the text in the field stays as typed; the form
SHALL NOT round, interpolate or otherwise change an entered
value. The form SHALL NOT decide whether a value is inside the method's range: that is the
backend's warning or refusal. The labels, hints and units shown follow the interface language.

#### Scenario: Form follows the contract
- **WHEN** a user selects a calculation type
- **THEN** the form shows one field per declared input of that type with its label, symbol and
  units, and selecting another type shows that type's fields without a change in the form
  component

#### Scenario: Empty or non-numeric value
- **WHEN** a user submits with an empty field, or a field that is not a finite number
- **THEN** no request is sent, and the field is marked with a message in text

#### Scenario: Whole values only
- **WHEN** a user enters `30.5` in an input with `whole_values_only` and submits
- **THEN** no request is sent, the field is marked with a message that names the whole-value
  rule, and the value stays `30.5` in the field

#### Scenario: Decimal comma
- **WHEN** a user enters `172,5` in a field and submits
- **THEN** the request carries the number 172.5, and the field still shows `172,5`

#### Scenario: Unit of a whole-values input
- **WHEN** a user opens the form of a type that has an input with `whole_values_only` (for
  example `phi_II`, base unit `deg`, which also lists `rad`)
- **THEN** that input shows its base unit only and offers no other unit, while the inputs without
  the flag offer every listed unit

#### Scenario: Server validation error
- **WHEN** the backend answers `422` with `fields`, each with a `location` and a `message`
- **THEN** each entry whose `location` ends with a declared input name marks that field with the
  entry's `message`, and an entry that names no field is shown above the form with its `message`

#### Scenario: Value outside the method's range
- **WHEN** the backend returns a result with a warning or a refusal for an entered value
- **THEN** the form has accepted the value, and the result screen shows the warning or the
  refusal

### Requirement: Report request screen
The frontend SHALL provide a report request screen for a stored result that collects the data of
`ReportRequest`: the title block (`designation`, `document_name`, `organization`, and optional
`documentation_kind`), the switch `signature_block` (on by default), and, for each of the
developer, the normative control and the checker, a surname and a date. While the signature block
is on, the screen SHALL require the surname and the date of the developer and of the normative
control, and the surname and the date of the checker when either is given, as the backend does
(the norm source of these rules is in the `report-generator` delta of `calculation-core-contract`).
The screen SHALL request the `.docx` from `POST /calculations/{result_id}/report` and, once it is
issued, show a stamp shaped as a title block (columns 1, 5 and 9 and the word «ВЫПУЩЕН») with the
file name and a download control; the file SHALL be saved only from that control, under the file
name the response gives. While the request runs, the submit control SHALL show that the report is
being generated (`aria-busy`) for at least 600 ms unless the user's system asks for reduced motion.
An error shows no stamp.

#### Scenario: Report being generated
- **WHEN** a user submits a complete report form and the response arrives 100 ms later, and the
  system does not ask for reduced motion
- **THEN** the submit control is `aria-busy` and says that the report is being generated until
  600 ms after the submit, and then the stamp shows columns 1, 5 and 9 of the title block, the word
  «ВЫПУЩЕН», the file name and the download control

#### Scenario: Download the report
- **WHEN** a user fills the required title-block fields and the required signatories and submits
- **THEN** the report of the stored result is generated, the stamp appears with the file name, and
  choosing its download control saves the `.docx` under the file name the response gives, with the
  user still on the report screen

#### Scenario: Report request fails
- **WHEN** the report request ends with an error
- **THEN** no stamp appears and no file is saved

#### Scenario: Incomplete signatories
- **WHEN** the signature block is on and the developer's date is empty
- **THEN** no request is sent and the field is marked with a message in text

#### Scenario: Signature block off
- **WHEN** a user turns the signature block off
- **THEN** the signatory fields are hidden and are not sent

#### Scenario: Report of a refused result
- **WHEN** a user requests the report of a result whose verdict is `refused`
- **THEN** the report is downloaded as for any result, because the backend returns a report that
  states the refusal (`calculation-api` "Report download"), and the screen shows no error

#### Scenario: Report not available
- **WHEN** the backend answers the report request with `422`, with `404`, with `409` (for example
  `calculation_type_not_registered`), or with another error
- **THEN** the screen shows the error's `message` in text, marks the report field that the `location` of
  each entry in `fields` names, shows an entry that names no field above the form
  (`design.md` decision 7), and downloads no file

### Requirement: Form draft and the edit-inputs action
The frontend SHALL keep the values and unit choices of an input form, for each calculation type, in
the memory of the open page for as long as the page is open, and SHALL restore them when the form of
that type is opened again, also by the browser's back action. The draft (the values and units typed into a form, not the inputs that a stored result itself
shows in its steps) SHALL NOT be written to browser storage, to the address, to the console or to
any screen other than the form's own fields.
The result screen SHALL offer an "edit inputs" action that opens the form of the type just
calculated with that draft, only for the result that the draft was last sent for; any other result
(opened by its address alone, or reached again by the browser's history after another calculation)
offers no such action. The input named by a refusal's bound is always an input of the calculated
type (`bound.quantity`, as `calculation-core-contract` fixes it). For a refusal the action SHALL be the
screen's main action and the link to the report request its second action, and the form it opens SHALL move focus to the input that the violated bound
names and show the bound next to that input.

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

### Requirement: Unit echo in the base unit
When a user chooses, for an input, a unit other than its base unit and the field holds a number,
the form SHALL show next to that field the value in the base unit, with its unit and in text, in the
interface language's number format with at most six significant digits. "Holds a number" is the
form's own rule of "Input form built from the type's contract" (a finite number as that check
reads it). The echo is shown for information only: the value and the unit that
are sent are the ones the user entered, and the conversion in the calculation stays with the
backend. The factors of the echo come from one display-only table of the unit vocabulary
(`backend/app/schemas/units.py`, `UNITS`), not from any type: this is a deliberate exception to
"no unit of a type in the frontend code", because the vocabulary is shared by all types and the
backend's own test of its table is mirrored by a frontend test that reads that table and fails when
a factor differs or a unit of the vocabulary has none. A unit with no factor shows no echo. The unit's label in the echo is the one the interface
already uses for that unit in the interface language (`м` in Russian, `m` in English), not a second
table. On a unit change the field flashes once with the accent colour for 120 ms, and under
reduced motion it does not.

#### Scenario: Another unit chosen
- **WHEN** a user enters `2` in the width and chooses `cm`
- **THEN** the form shows `= 0,02 м` next to the field, and the request carries `2` with the unit `cm`

#### Scenario: Echo in English
- **WHEN** the interface language is English and a user enters `2` in the width and chooses `cm`
- **THEN** the form shows `= 0.02 m` next to the field

#### Scenario: Flash of the field
- **WHEN** a user changes the unit of a field
- **THEN** the field flashes once with the accent colour for 120 ms, and under reduced motion it
  does not flash

#### Scenario: Base unit or no number
- **WHEN** the chosen unit is the base unit, or the field is empty or not a number
- **THEN** no echo is shown

### Requirement: Verdict focus on arrival
When a stored result is shown after it was loaded or after the form was sent, the frontend SHALL
move keyboard focus once to the verdict region (the stamp for a `pass` or a `fail`, whether or not
the check step is found, and the refusal for a refusal), so that a screen reader announces it and a
keyboard user starts from it. A warning SHALL NOT take focus.

#### Scenario: Result arrives
- **WHEN** a result with the verdict `pass` or `fail`, or a refusal, is shown
- **THEN** focus is on the verdict region, and the focus indicator meets the contrast of
  "Non-functional — language, accessibility, browsers"

#### Scenario: Focus is taken once
- **WHEN** the verdict is shown, the user moves focus elsewhere, and the screen is drawn again (a
  step is expanded, or the language is changed)
- **THEN** focus stays where the user put it

#### Scenario: Result with a warning
- **WHEN** a result with a warning is shown
- **THEN** focus is on the verdict stamp of that result, not on the warning

### Requirement: Calculation in progress
While a calculation request is sent, the form SHALL show that it is in progress (a progress rule and
a text message announced to assistive technology as a status), SHALL leave the entered values
readable at the contrast of "Non-functional — language, accessibility, browsers" and unchanged
(text fields read-only, unit choices not changeable), and SHALL send no second request, however
the form is submitted. Counted from the submit, after 3 seconds the message SHALL say that the
server is calculating, and after 10 seconds that it takes longer than usual and that the entered
data is kept. When the request ends with an error, the fields SHALL be changeable again with their
values kept, and the error is shown as without this requirement. While the request runs, the form
SHALL also trace the computation across its rows (a scan line passes the input rows from top to
bottom and leaves each row marked); unless the user's system asks for reduced motion, the result
SHALL open no sooner than 700 ms after the submit, and with reduced motion it opens as soon as the
response arrives.

#### Scenario: Request in progress
- **WHEN** a user submits a valid form and the response has not arrived
- **THEN** the fields cannot be changed, a message in text says that the calculation is in
  progress, and the submit control cannot send again

#### Scenario: Submitted twice
- **WHEN** a user presses Enter in a field twice while the first request is in progress
- **THEN** exactly one request is sent

#### Scenario: Response after 3 seconds
- **WHEN** the response has not arrived 3 seconds after the submit
- **THEN** the message says that the server is calculating

#### Scenario: Request fails
- **WHEN** the request ends with a `503` while in progress
- **THEN** the fields are changeable again with the values kept, and the error is shown

#### Scenario: Slow response
- **WHEN** the response takes more than 10 seconds
- **THEN** the message says that it takes longer than usual and that the entered data is kept

#### Scenario: Minimum duration of the computation trace
- **WHEN** the response arrives 100 ms after the submit and the system does not ask for reduced
  motion
- **THEN** the result opens 700 ms after the submit, and with reduced motion it opens when the
  response arrives

#### Scenario: Response after the minimum duration
- **WHEN** the response arrives 900 ms after the submit
- **THEN** the result opens when the response arrives, with no further wait

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
1.9 s after the last step), and a `fail` or a `pass` with a warning at once; a refusal has no steps
and shows at once. A result shown again in the same page session, or shown while the system asks
for reduced motion, shows every step, the verdict and the outputs at once.

#### Scenario: First showing of a result
- **WHEN** a result with nine steps is shown for the first time in a page session
- **THEN** the steps appear one by one, the stamp and the output values are held with the status
  «ВЫПОЛНЕНИЕ РАСЧЁТА» until the last step, and then they are shown

#### Scenario: Long trace
- **WHEN** a result with 40 steps is shown for the first time in a page session
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

### Requirement: Responsive type
The page heading SHALL scale with the viewport between 1.875 rem and 2.25 rem, and the verdict line
(the verdict word and the reading of the check in the stamp) between 1.5 rem and 1.875 rem; both
bounds are in rem so that browser text zoom still scales them. All other text, the value fields
and the columns of figures SHALL stay on fixed whole-pixel sizes. At every viewport width from
320 px to 1440 px no screen SHALL scroll horizontally, and the figures of a column (the value
fields of the form, the output values of a result) SHALL stay aligned on their right edge.

#### Scenario: No horizontal scroll
- **WHEN** any of the four screens is shown at a width of 1440, 1280, 1024, 768, 390 or 320 px
- **THEN** the page does not scroll horizontally

#### Scenario: Figures stay aligned
- **WHEN** the form or a result is shown at those widths
- **THEN** the right edges of the value fields, and of the output values, are the same on every
  row, and the computed font size of a figure in a column is a whole number of pixels

#### Scenario: Bounded scaling
- **WHEN** the browser text size is the default of 16 px and the viewport is 320 px wide and when
  it is 1440 px wide
- **THEN** the page heading is 30 px at 320 px and 36 px at 1440 px, and the verdict line is 24 px
  at 320 px and 30 px at 1440 px

### Requirement: Motion follows the user's setting
Every animation or transition the interface adds (the frame of the verdict, the flash of a field
after a unit change, the progress rule, the computation trace across the form, the trace playback
and the verdict reveal, the drawn motif of the type selection, and the report stamp with its jolt of
the form) SHALL run only when the user's
system does not ask for reduced motion. With `prefers-reduced-motion: reduce`, each such change
SHALL happen at once, without movement, and no information SHALL depend on the movement.

#### Scenario: Reduced motion requested
- **WHEN** the system asks for reduced motion and a user opens a result or sends the form
- **THEN** no animation runs on the verdict, the field, the progress rule, the form or the trace,
  and the state they show is the same as without reduced motion

### Requirement: Non-functional — language, accessibility, browsers
The interface SHALL be available in Russian and in English, with Russian complete and a missing
English text shown in Russian; numbers SHALL be shown with the decimal separator of the interface
language. In the pilot's first iteration (while the pilot is shown only inside the team: the two
developers and the PM; `design.md` decision 12) the language switch SHALL NOT be shown and the
interface is in Russian, because the calculations cover Russian norms; the English texts and the
switch stay in the code, and the setting `SHOW_LANGUAGE_SWITCH` shows the switch again. The `.docx`
report stays in Russian. The interface SHALL meet WCAG 2.2 level AA: every
control reachable and operable by keyboard, text contrast at least 4.5:1 (3:1 for large text and
for the boundaries of controls), no meaning carried by colour alone, and every field with a
programmatically associated label. The interface SHALL work in the last two versions of Chrome,
Firefox, Edge and Safari on desktop, and every calculation step SHALL render with its formula in
each of them (`transparent-output` "Non-functional — completeness"). The time from the arrival of
the backend's response to the first render of the target screen SHALL be under 1 second at the 95th
percentile, measured over 20 runs in Chromium against the mocked backend; the minimum duration of
the computation trace ("Calculation in progress") counts in this time. This refines the base
requirement "Non-functional — integration and latency" for the frontend and does not replace it.

#### Scenario: Language switch in the pilot's first iteration
- **WHEN** a user opens any screen with `SHOW_LANGUAGE_SWITCH` off
- **THEN** no language switch is shown and the texts are in Russian

#### Scenario: Switch the language
- **WHEN** `SHOW_LANGUAGE_SWITCH` is on and a user switches the interface language from Russian
  to English
- **THEN** the screen texts, labels and hints that have an English text are shown in English and
  any without one stay in Russian, and `172.5` is shown as `172.5` in English and `172,5` in Russian

#### Scenario: Keyboard only
- **WHEN** a user completes the journey from type selection to the downloaded report with the
  keyboard alone, in an automated browser test against the mocked backend
- **THEN** every step is possible, and at every point the focused control shows a focus indicator
  (WCAG 2.4.7) whose colour differs from its surroundings by at least 3:1

#### Scenario: Automated accessibility check
- **WHEN** the screens are rendered in the component tests
- **THEN** an accessibility check (axe) finds no violation of WCAG 2.2 level AA that it can detect
  in jsdom, which does not include colour contrast

#### Scenario: Contrast in a real browser
- **WHEN** the screens are opened in Chromium, in the light and in the dark state if the interface
  has both
- **THEN** an axe contrast check finds no text below 4.5:1 (3:1 for large text), including the
  amber and red states of a warning and a refusal

#### Scenario: Supported browsers
- **WHEN** a calculation with a trace is opened in each supported browser
- **THEN** every step shows its formula typeset, and no step falls back to raw text

#### Scenario: Transition time
- **WHEN** a mocked response arrives for a screen change
- **THEN** the target screen is first rendered within 1 second at the 95th percentile of 20 runs

### Requirement: Non-functional — safe handling and test coverage
The frontend SHALL NOT write an entered input value, a response body or a stack trace to the
browser console or show a stack trace on a screen, SHALL typeset a formula or symbol received from
the backend without executing code or following a link from it, and SHALL keep branch coverage of
`frontend/src` at or above 95%.

#### Scenario: Error without leaking
- **WHEN** a request fails with any error
- **THEN** the screen shows the error's `code` and `message`, and the console holds no entered
  value, no response body and no stack trace from this application

#### Scenario: Hostile symbol
- **WHEN** the listing's `symbol` or a trace step's `expression` holds an instruction that loads a
  script or a link (for example `\href{javascript:alert(1)}{x}`)
- **THEN** no script runs and no link is created, and the text is shown as inert text

#### Scenario: Coverage gate
- **WHEN** `frontend/check.sh` runs
- **THEN** it fails if the branch coverage of `frontend/src` is below 95%
