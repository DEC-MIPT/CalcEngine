# Spec Delta

## Purpose
Defines the automated ingestion of normative documents: registry discovery, download,
metadata, dedup, and versioned storage. The collector is domain-agnostic and feeds
`dec_normatives`.

## ADDED Requirements

### Requirement: Registry discovery
The system SHALL discover and list the editions and releases of a normative document
from at least one authoritative registry without manual lookup.

#### Scenario: List editions
- **WHEN** the collector is pointed at a document designation
- **THEN** it lists the available editions and their status from the registry

### Requirement: Download with integrity
The system SHALL download a document file and record its `sha256` and source URL.

#### Scenario: Download and hash
- **WHEN** a document is downloaded
- **THEN** the file is stored with its `sha256` and source URL, and a re-download of an
  unchanged file is skipped

### Requirement: Metadata and dedup
The system SHALL store metadata (designation, title, edition, amendment, status, validity
date, source) and SHALL NOT duplicate an already-stored `(document, edition, sha256)`.

#### Scenario: No duplicate
- **WHEN** the same edition with the same content is fetched twice
- **THEN** exactly one record is kept

### Requirement: Additive revisions
The system SHALL store revisions additively and never rewrite a stored revision in place.

#### Scenario: New revision
- **WHEN** a new revision appears
- **THEN** it is stored as a new version, and previously stored revisions keep their
  reference
