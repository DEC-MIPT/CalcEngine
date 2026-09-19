# Normatives Catalog

## Purpose
Component 1: a normative base that stores SP/GOST/SNiP documents, formulas, and
coefficients, and serves them to the calculation flow with full-text search and
actuality tracking. Storage is implemented as a dedicated `dec_normatives` database
per the `backend-architecture` capability.

## Requirements

### Requirement: Normative document storage
The system SHALL store normative documents (SP/GOST/SNiP) and their metadata in
PostgreSQL, including formulas, coefficients, and applicability rules.

#### Scenario: Store a normative document
- **WHEN** a methodologist adds a normative document with its formulas and coefficients
- **THEN** the document, formulas, and coefficients are persisted and retrievable by
  calculation type

### Requirement: Full-text search
The system SHALL provide full-text search over the normative base using PostgreSQL
full-text search (pg_trgm, GIN indexes) with Russian-language support.

#### Scenario: Find a normative by keywords
- **WHEN** a user searches by keywords such as a document number or topic
- **THEN** matching normative documents are returned by relevance

### Requirement: Binding a normative to a calculation type
The system SHALL bind each calculation type to the relevant normative document and
automatically load the applicable formulas and coefficients.

#### Scenario: Select a calculation type
- **WHEN** a user selects a calculation type (for example a beam check)
- **THEN** the system loads the bound normative document, its current revision, and the
  required formulas and coefficients

### Requirement: Actuality tracking
The system SHALL display the validity date of each normative document and warn when a
document is outdated or will soon become outdated.

#### Scenario: Outdated normative
- **WHEN** a normative document bound to a calculation is not the current revision
- **THEN** the system warns the user that the document is outdated

### Requirement: Manual normative maintenance for MVP
The system SHALL allow normative data to be maintained manually for the MVP (one pilot
file), without requiring automated NLP/RAG parsing.

#### Scenario: Pilot normative file
- **WHEN** the MVP uses a single pilot normative file
- **THEN** calculations reference the manually maintained normative data

### Requirement: Non-functional — performance
The system SHALL load a normative document and its formulas in under 2 seconds, and
the service normative base SHALL be updatable at least once per day.

#### Scenario: Fast normative load
- **WHEN** a normative document is requested for a calculation
- **THEN** the document and formulas load in under 2 seconds
