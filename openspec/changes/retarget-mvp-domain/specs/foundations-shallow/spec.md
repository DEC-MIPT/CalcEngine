# Spec Delta

## Purpose
Defines the scope of the first MVP domain, shallow foundations: which calculation types
are in scope, which cases are out of scope, and how the system refuses an out-of-scope
case. It holds scope only. It contains no engineering method, formula, coefficient, or
clause number.

## ADDED Requirements

### Requirement: In-scope calculation types
The system SHALL support the full shallow-foundation calculation by the second group
of limit states on a natural base as the required MVP outcome. The registered
`foundations_shallow_r` calculation provides the delivered design-resistance R pilot
stage. It SHALL NOT be treated as completion of the full MVP workflow.

Separate reviewed implementation changes SHALL define the engineering workflow and
its executable component contracts before further calculation code is implemented.
Those contracts SHALL identify applicability, inputs, outputs, normative sources and
independent verification cases. This product-scope requirement SHALL NOT supply
unapproved methods, soil cases, coefficients, tolerances or future calculator ids.

#### Scenario: In-scope type runs
- **WHEN** a user selects a calculation type from the in-scope list
- **THEN** the type is part of the required first-domain workflow and its completed
  implementation must meet its reviewed end-to-end contract before MVP release;
  its norm references are verified or marked `status: unverified`

#### Scenario: List is complete before apply
- **WHEN** the change is proposed for apply
- **THEN** the scope names the full second-limit-state MVP outcome and identifies
  `foundations_shallow_r` as the delivered pilot, without a placeholder scope or
  invented identifiers for the remaining implementation components

### Requirement: Out-of-scope cases
The system SHALL treat calculations outside the required second-limit-state
shallow-foundation workflow, and foundation types other than shallow foundations on
a natural base, as out of scope for this capability. The scope revision SHALL NOT
broaden the existing natural-base restriction. Unsupported applicability cases SHALL
remain refused until their reviewed engineering contracts and implementations exist.

#### Scenario: Out-of-scope case requested
- **WHEN** a user asks for a case on the out-of-scope list
- **THEN** the system refuses to calculate and names the limit that excludes the case

#### Scenario: Case on neither list
- **WHEN** a user asks for a case that is on neither the in-scope nor the out-of-scope
  list
- **THEN** the system treats it as out of scope and refuses with the same message

### Requirement: Scope changes go through the vision
The system SHALL change the in-scope or out-of-scope list only through an OpenSpec
change that also references the MVP scope in `product-vision`.

#### Scenario: Scope edit
- **WHEN** a change adds a calculation type to the in-scope list
- **THEN** the change is validated and reviewed against `product-vision` before it is
  accepted

### Requirement: Foundation MVP release gate
The system SHALL declare the foundation MVP complete only when reviewed engineering
contracts identify the full required second-limit-state workflow and all required
components pass their recorded end-to-end acceptance checks. Approval or archive of
this scope-only change SHALL NOT serve as evidence that those components are delivered.

#### Scenario: R-only implementation
- **WHEN** the registered R pilot is available but the remaining required workflow
  components have no completed acceptance records
- **THEN** the R stage can be identified as delivered, but the foundation MVP remains
  incomplete

#### Scenario: Full workflow evidenced
- **WHEN** an MVP release is proposed
- **THEN** its evidence identifies the reviewed full-workflow contracts and completed
  acceptance of every required component, beyond the R pilot alone

#### Scenario: Method contract before implementation
- **WHEN** further foundation calculation functionality is proposed for implementation
- **THEN** its separate change defines and reviews the engineering contract and
  independent verification cases before code is written
