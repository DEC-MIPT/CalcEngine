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
The system SHALL provide a web form for entering calculation inputs (loads, geometry,
material grade) with validation before submission.

#### Scenario: Enter and validate inputs
- **WHEN** a user fills the calculation form and submits
- **THEN** inputs are validated and sent to the calculation engine via the backend

### Requirement: Single authorization
The system SHALL use a single authorization across the normative base, calculation
engine, and report generator components.

#### Scenario: One login for the whole platform
- **WHEN** a user signs in once
- **THEN** the same identity is used across all platform components

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
