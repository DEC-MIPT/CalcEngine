# Spec Delta

## Purpose
Defines the scope of the first MVP domain, shallow foundations: which calculation types
are in scope, which cases are out of scope, and how the system refuses an out-of-scope
case. It holds scope only. It contains no engineering method, formula, coefficient, or
clause number.

## ADDED Requirements

### Requirement: In-scope calculation types
The system SHALL support only the calculation types listed as in scope for shallow
foundations. The list is: design soil resistance of the base (R) of a shallow foundation
on a natural base, registered as `foundations_shallow_r`. Egor and the PM confirmed this
type on 2026-09-27 (`docs/decisions/first-calculation-type-egor-pm.md`, questions 1-2).

#### Scenario: In-scope type runs
- **WHEN** a user selects a calculation type from the in-scope list
- **THEN** the type is available end-to-end in the MVP, and its norm references are
  either verified or marked `status: unverified`

#### Scenario: List is complete before apply
- **WHEN** the change is proposed for apply
- **THEN** the in-scope list names at least one calculation type, and the placeholder
  "TBD" is gone

### Requirement: Out-of-scope cases
The system SHALL treat the cases on the out-of-scope list as unsupported for shallow
foundations. The list is: every calculation of shallow foundations other than the
in-scope type, and every foundation type other than a shallow foundation on a natural
base. This is the complement of the in-scope list; the PM confirms it with that list.

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
