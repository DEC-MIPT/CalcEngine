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
- **GIVEN** a base designation string (e.g. `"22.13330"`) and a registry source name
  (`"faufcc"` or `"pravo"`)
- **WHEN** `repository.search(designation)` is called
- **THEN** it returns a non-empty list of `Document` objects whose `.designation` matches
  the input pattern, each with `.edition` (year string or `None`) and `.state`

### Requirement: Download with integrity
The system SHALL download a document file and record its `sha256` and source URL.

#### Scenario: Download and store
- **GIVEN** a `Document` with a valid `download_url`
- **WHEN** `repository.download(document)` is called
- **THEN** the raw bytes are returned and `FileStorage.save()` persists them, returning
  `(path, sha256_hex, is_new=True)`

#### Scenario: Skip re-download (dedup)
- **GIVEN** a file with sha256 `H` already stored in `FileStorage`
- **WHEN** `FileStorage.save()` is called again with content whose sha256 is also `H`
- **THEN** the existing file path is returned with `is_new=False` and no new file is
  written to disk

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
