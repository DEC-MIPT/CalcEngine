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
