## MODIFIED Requirements

### Requirement: Expandable steps
The system SHALL allow each calculation step to be expanded and collapsed on demand, by
pointer and by keyboard, and SHALL expose the state of each step to assistive technology. Steps
are collapsed when a result opens.

#### Scenario: Expand a step
- **WHEN** a user clicks a calculation step
- **THEN** the step expands to show its details and collapses when clicked again

#### Scenario: Expand a step with the keyboard
- **WHEN** a user moves focus to a step header and presses Enter or Space
- **THEN** the step expands or collapses, and the header's `aria-expanded` is `true` while the
  step is expanded and `false` while it is collapsed

#### Scenario: Collapsed on open
- **WHEN** a user opens a completed calculation
- **THEN** every step is collapsed and its header shows the step's result with its unit

#### Scenario: Expand or collapse all
- **WHEN** a user chooses "expand all" or "collapse all"
- **THEN** every step of the trace is expanded or collapsed accordingly
