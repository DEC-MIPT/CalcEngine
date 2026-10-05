## ADDED Requirements

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
SHALL be written in the frontend code. Before submission the form SHALL check that every field is
filled, that the value is a finite number, and, for an input with `whole_values_only`, that the
value is a whole number (a number equal to its integer part, so `30`, `30.0` and `30e0` are
accepted and `30.5` is not); the form SHALL NOT round, interpolate or otherwise change an entered
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
The screen SHALL download the `.docx` that `POST /calculations/{result_id}/report` returns.

#### Scenario: Download the report
- **WHEN** a user fills the required title-block fields and the required signatories and submits
- **THEN** the `.docx` of the stored result is downloaded under the file name the response gives,
  and the user stays on the report screen

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

### Requirement: Non-functional — language, accessibility, browsers
The interface SHALL be available in Russian and in English, with Russian complete and a missing
English text shown in Russian; numbers SHALL be shown with the decimal separator of the interface
language. The `.docx` report stays in Russian. The interface SHALL meet WCAG 2.2 level AA: every
control reachable and operable by keyboard, text contrast at least 4.5:1 (3:1 for large text and
for the boundaries of controls), no meaning carried by colour alone, and every field with a
programmatically associated label. The interface SHALL work in the last two versions of Chrome,
Firefox, Edge and Safari on desktop, and every calculation step SHALL render with its formula in
each of them (`transparent-output` "Non-functional — completeness"). The time from the arrival of
the backend's response to the first render of the target screen SHALL be under 1 second at the 95th
percentile, measured over 20 runs in Chromium against the mocked backend. This refines the base
requirement "Non-functional — integration and latency" for the frontend and does not replace it.

#### Scenario: Switch the language
- **WHEN** a user switches the interface language from Russian to English
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
