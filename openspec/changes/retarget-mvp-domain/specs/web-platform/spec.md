## MODIFIED Requirements

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
