# Security

## Purpose
Defines security requirements for DEC so that no security issues are introduced during
development, per the DOD "no known security issues" gate.

## Requirements

### Requirement: Input validation
The system SHALL validate all user input through typed schemas at the API boundary and
SHALL NOT trust client-provided data.

#### Scenario: Invalid input rejected
- **WHEN** a request contains malformed or out-of-range input
- **THEN** it is rejected with a validation error before reaching business logic

### Requirement: Secrets management
The system SHALL NOT hardcode or commit secrets; credentials and API keys SHALL be read
from environment variables or a local `.env` file excluded from version control.

#### Scenario: No secret in the repository
- **WHEN** a secret (database URL, token, key) is required
- **THEN** it is provided via environment, never written into code or committed to git

### Requirement: Authentication security
The system SHALL store passwords using a strong hash and SHALL issue and validate
session tokens (JWT) with appropriate expiry.

#### Scenario: Password never stored in plaintext
- **WHEN** a user registers or changes a password
- **THEN** only a strong hash is persisted, never the plaintext

### Requirement: No sensitive data in logs
The system SHALL NOT log passwords, tokens, or full normative input data considered
sensitive.

#### Scenario: Sanitized logs
- **WHEN** the application logs a request or error
- **THEN** secrets and sensitive fields are redacted

### Requirement: OWASP Top 10 awareness
The system SHALL follow OWASP Top 10 guidance for the implemented surfaces (for example
SQL injection prevention via ORM parameterization, XSS prevention via output encoding).

#### Scenario: Injection-safe data access
- **WHEN** data is read from or written to the database
- **THEN** parameterized queries are used and no raw string concatenation of SQL occurs
