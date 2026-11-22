## ADDED Requirements

### Requirement: Design-tool report provenance
The system SHALL generate new design-tool DOCX reports from stored inputs and outcomes, including load level, weight mode, complete vertical-force sum, signed moments, dimensions, pressure-envelope values and candidate policy/selection where present. Figures SHALL have text alternatives and SHALL NOT introduce values absent from stored evidence. Existing report section order, title block, source-label and accountability requirements remain. Historical pilot and averaged loads reports SHALL retain their recorded meaning without a new calculation.

#### Scenario: Complete added-force accounting
- **WHEN** a report presents N_base or p
- **THEN** every included weight, surcharge or moment contribution is shown in the expression and numeric substitution, and omitted-mode contributions are absent

#### Scenario: Refusal and search exhaustion report
- **WHEN** the stored outcome is a contact refusal or no-acceptable-candidate search
- **THEN** the report retains diagnostic evidence and the explicit outcome without a bearing-success or global-optimum conclusion
