## ADDED Requirements

### Requirement: Codex project tooling mirror
The system SHALL preserve Claude agents, commands, skills and shared settings in
`.codex/`, with native Codex roles and discoverable skill adapters. Claude sources
SHALL remain canonical and unchanged by mirroring.

#### Scenario: Role or workflow selected in Codex
- **WHEN** a trusted project is opened in a new Codex session
- **THEN** every Claude role has a TOML counterpart with its responsibilities preserved
- **AND** every mirrored skill and all six opsx command adapters have discoverable links
- **AND** Claude model and tool identifiers are not treated as Codex configuration

#### Scenario: Exact source copies inspected
- **WHEN** the mirror is checked against `.claude/`
- **THEN** source agents, commands, skills and shared settings have matching copies
- **AND** local settings match the source and remain Git-ignored
- **AND** existing local files and prior task edits are preserved

### Requirement: Codex mirror permission boundaries
The system SHALL keep local settings untracked and distinguish source JSON
permission intent from native Codex enforcement. Shared artifacts SHALL contain
no credentials, personal settings values or machine-specific paths.

#### Scenario: Permissions adapted
- **WHEN** native configuration is loaded
- **THEN** workspace-write and on-request are selected without broad outside-sandbox allows
- **AND** supported command rules prompt for mutations and forbid dangerous prefixes
- **AND** documentation identifies unsupported file-read and edit glob enforcement
- **AND** local JSON settings do not override managed restrictions

#### Scenario: Mirror validated
- **WHEN** the feature is assessed for GO
- **THEN** source equality, TOML/JSON parsing, strict CLI config loading, skill/link
  validity, local ignore behavior and strict OpenSpec validation pass
- **AND** tester records application tests, coverage and UI/UX as N/A because
  no application/UI changes or executable statements/branches are introduced
- **AND** settings/ignore changes use feature GO, with >=95% branch coverage if
  executable helper code is introduced
- **AND** discovery links are tracked through explicit Git ignore exceptions
