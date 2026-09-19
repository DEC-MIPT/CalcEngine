# Product Vision

## Purpose
Defines the product vision, unique value proposition, target users, and MVP scope for
DEC (Design Engineer's Calculator), a cloud web service that automates engineering
calculations backed by a verified normative base and GOST-compliant reports.

## Requirements

### Requirement: Single-window engineering calculation service
The system SHALL provide one integrated environment that combines a normative base
(SP/GOST/SNiP), a calculation engine, and a report generator, so an engineer does not
switch between separate tools.

#### Scenario: Engineer completes a full calculation cycle
- **WHEN** an engineer selects a calculation type, enters inputs, runs the calculation,
  and exports the result
- **THEN** the whole cycle happens inside one web interface without manual data transfer
  between tools

### Requirement: Cloud accessibility
The system SHALL be delivered as a cloud web service accessible from a browser on any
device, without a desktop install.

#### Scenario: Access from any device
- **WHEN** a user opens the service URL in a browser
- **THEN** the service is available without installing desktop software

### Requirement: Subscription monetization
The system SHALL support B2B and B2C subscription tiers and a 14-day free trial.

#### Scenario: Tiered access
- **WHEN** a customer subscribes to a B2B or B2C plan
- **THEN** the plan limits and features match the purchased tier, and a 14-day trial
  grants full functionality for a limited time

### Requirement: MVP scope
The system SHALL target a single verified calculation type as the MVP reference: the
beam deflection check per SP 16.13330 (steel structures). The reference type is
swappable and must not hard-code the selection of the normative method.

#### Scenario: MVP reference calculation
- **WHEN** the MVP is delivered
- **THEN** the beam deflection check per SP 16.13330 is fully implemented end-to-end
  as the reference capability

### Requirement: No machine learning in the calculation path
The system SHALL NOT use machine learning for calculations; calculation algorithms
must be deterministic and verified. Normative data is entered manually for MVP;
NLP/RAG auto-parsing is a future, non-MVP goal.

#### Scenario: Deterministic calculation
- **WHEN** the same inputs are provided twice
- **THEN** the calculation produces identical results, and no ML model influences the
  arithmetic or the normative references
