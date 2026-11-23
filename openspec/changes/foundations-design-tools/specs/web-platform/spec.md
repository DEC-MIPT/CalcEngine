## ADDED Requirements

### Requirement: Accessible footing design controls and diagrams
The system SHALL provide distinct controls for checking dimensions and selecting from bounded candidates, clearly identify averaged versus explicit weights and the selected type's fixed load level, and preserve raw entered values and units under existing draft-eligibility rules. Changing mode SHALL require an explicit user action and SHALL NOT silently reuse an incompatible weight set. Load schematic, pressure envelope and candidate outcomes SHALL be operable by keyboard and understandable without colour, pointer hover, animation or a spatial diagram. The views SHALL work at 320 px without page overflow, respect reduced motion, and retain existing WCAG 2.2 AA, supported-browser and transition requirements.

#### Scenario: Mode change does not double count weights
- **WHEN** a user changes from averaged weights to explicit weights
- **THEN** the form identifies the newly required contributions and does not submit both them and the averaged allowance

#### Scenario: Diagram without vision or pointer
- **WHEN** a user navigates by keyboard or assistive technology
- **THEN** dimensions, axes, signed loads, pressure extrema and candidate decisions remain available as labelled text or tables with units

#### Scenario: Search cannot proceed on unspecified policy
- **WHEN** candidate bounds or an approved policy are missing
- **THEN** the selection action is unavailable with a readable explanation and no default policy is silently inferred from competitor behavior

#### Scenario: Read the demo form in any mode
- **WHEN** a user opens the demo form in explicit-weight, averaged-weight, or size-selection mode
- **THEN** the diagram is horizontally centered within the guidance section, below the section heading
- **AND** the diagram-specific explanatory text is visually hidden but remains available to assistive technology; field hints stay visible
- **AND** in all three modes, each scalar input row places the field symbol to the left of its quantity label without overlap at supported widths, including 320 px

#### Scenario: Review the explicit-weight demo result
- **WHEN** a user opens a stored explicit-weight demo result with calculation steps, including a diagnostic refusal
- **THEN** the R result ruler shows the stored steps in order and links its ticks to the corresponding trace entries, respecting reduced motion and not causing page overflow
- **AND** each normative reference list shows each SP 22 edition once with its distinct stored locators and retains the stored reference status where displayed
- **AND** engineering quantities without a stored output rounding rule are displayed with two fractional digits, with halfway values rounded away from zero; stored output rules take precedence and formulas, normative locators, stored values and verdicts do not change
- **AND** if rounding the operands under the applicable rules would make the stored operator read against an individual check’s stored `passed` flag, both operands are shown unrounded wherever that comparison appears, including the verdict stamp when applicable
- **AND** opening a valid step fragment directly, including after reloading the result, focuses the corresponding rendered step
- **AND** the demo shows the stored rationale of an engineer-defined step or contact refusal separately from result-wide normative references; the engineer's identity may be omitted from this presentation and is retained in the stored result
- **AND** the diagnostic pressure diagram’s table and extrema retain the exact negative value if display rounding would turn it into zero

#### Scenario: Open the synthetic example from the type registry
- **WHEN** the explicit-weight demo type is available and the user opens its separate example entry by keyboard or pointer
- **THEN** the form identifies the synthetic `weights-C` data and initially presents all 19 editable quantities and their units without issuing a calculation request
- **AND** the example draft stays separate from the ordinary form, including when the user returns from the result to edit the submitted inputs
- **AND** explicit submission uses the existing calculation type and validation with no mock result or new API type

### Requirement: Revision-scoped browser acceptance evidence
For the foundations-design-tools frontend candidate `bd9924478cf24f8e392f75efe7ee4a8289756c3b` only, the tester SHALL accept the eight inherited manual browser-version verdicts from the pressure-from-loads matrix in combination with the candidate's full Playwright run and independent UI/UX PASS, in place of fresh branded desktop browser runs for feature acceptance. The tester SHALL retain the source revision and distinguish the inherited verdicts from current-candidate checks. This is an evidence exception, not a change to the base browser support requirement or to the other GO criteria. It SHALL NOT apply to another candidate or be retained as a general exception in the canonical spec.

#### Scenario: Assess the approved candidate without new branded runs
- **WHEN** the tester evaluates `bd9924478cf24f8e392f75efe7ee4a8289756c3b` with the documented inherited matrix, passing full Playwright and independent UI/UX PASS for the candidate
- **THEN** the absence of fresh branded runs does not block the candidate's browser acceptance
- **AND** no inherited slot is identified as newly executed

#### Scenario: Assess another revision
- **WHEN** the tester evaluates a different frontend candidate
- **THEN** the browser acceptance evidence exception does not apply
