## ADDED Requirements

### Requirement: Design-tool report provenance
The system SHALL generate new design-tool DOCX reports from stored inputs and outcomes, including load level, weight mode, complete vertical-force sum, signed moments, dimensions, pressure-envelope values and candidate policy/selection where present. Figures SHALL have text alternatives and SHALL NOT introduce values absent from stored evidence. Existing report section order, title block, source-label and accountability requirements remain. Historical pilot and averaged loads reports SHALL retain their recorded meaning without a new calculation.

#### Scenario: Complete added-force accounting
- **WHEN** a report presents N_base or p
- **THEN** every included weight, surcharge or moment contribution is shown in the expression and numeric substitution, and omitted-mode contributions are absent

#### Scenario: Refusal and search exhaustion report
- **WHEN** the stored outcome is a contact refusal or no-acceptable-candidate search
- **THEN** the report retains diagnostic evidence and the explicit outcome without a bearing-success or global-optimum conclusion

#### Scenario: Matches the explicit-weight result
- **WHEN** an ordinary DOCX is generated from a stored explicit-weight demo result
- **THEN** the trace preserves the stored step order and includes the same outputs and individual check outcomes as the result screen, with no final outputs for a refusal
- **AND** each normative step retains its own recorded locators and applicable status, grouping the distinct locators of each SP 22 edition within that step; the result-wide list is printed separately from the stored rationale of an engineer-defined step
- **AND** the base report precision rules apply except that demo trace, conclusion and diagram-table quantities without a stored output rule round to two digits, with halfway values rounded away from zero (`2.675` displays as `2.68`); the original input table remains lossless. A stored failed `4.001 ≤ 4` comparison stays unrounded rather than displaying `4.00 ≤ 4.00`
- **AND** trace expressions, check expressions, substitutions, results and diagram-table quantities are editable Office Math equations, retaining plain-text fallback for any genuinely unconvertible stored expression, including engineer-defined expressions
- **AND** source status, title block, and the meaning of historical pilot and averaged reports are unchanged
- **AND** the demo may omit the engineer's identity while retaining the stored rationale and distinguishing it from the normative sources; the stored result is unchanged
- **AND** diagnostic pressure tables retain the exact negative value if display rounding would turn it into zero
