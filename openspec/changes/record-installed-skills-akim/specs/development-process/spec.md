## ADDED Requirements

### Requirement: Installed skills are recorded per developer
The system SHALL record, for each skill a developer installs on their machine, the
developer name, the skill name, the source repository, the install scope (project or
global), and the installation date. Each developer SHALL keep their own record in a
requirement of their own, named "Installed skills of <developer>", added by their own
OpenSpec change. This requirement defines the content of the record required by
"Skill availability check".

#### Scenario: Record fields
- **WHEN** a developer's record is read
- **THEN** each entry names the developer, the skill, the source repository, the scope,
  and the installation date

#### Scenario: Colleague installs a skill
- **WHEN** Egor installs a skill
- **THEN** it is recorded in a requirement "Installed skills of Egor" added by a
  separate change, and the requirement "Installed skills of Akim" is not edited

### Requirement: Installed skills of Akim
The system SHALL keep a record of the skills Akim installed with `npx skills add`,
each with its source repository, scope, and installation date, and SHALL keep the
record consistent with the lock file the skills CLI keeps on Akim's machine.

#### Scenario: Required skills installed on 2026-09-20
- **WHEN** a reviewer compares the record with the skills CLI lock file on Akim's machine
- **THEN** the record lists seven required skills, all dated 2026-09-20:
  `find-skills` (source `vercel-labs/skills`, project scope);
  `vercel-react-best-practices`, `vercel-composition-patterns`, and
  `web-design-guidelines` (source `vercel-labs/agent-skills`, global scope);
  `webapp-testing`, `doc-coauthoring`, and `frontend-design` (source
  `anthropics/skills`, global scope); for each global skill the lock file holds the
  same source and installation date, and for `find-skills` the directory
  `.agents/skills/find-skills` exists in the project

#### Scenario: Optional skills installed on 2026-09-20
- **WHEN** a reviewer compares the record with the skills CLI lock file on Akim's machine
- **THEN** the record lists eight optional skills, all dated 2026-09-20 and all in
  global scope: `pytest-skill` (source `lambdatest/agent-skills`);
  `python-code-quality` (source `laurigates/claude-plugins`);
  `postgresql-database-engineering` (source `manutej/luxor-claude-marketplace`);
  `owasp-security` (source `hoodini/ai-agents-skills`); `code-security` (source
  `semgrep/skills`); `accessibility` (source `addyosmani/web-quality-skills`);
  `software-architecture-design` (source `vasilyu1983/ai-agents-public`);
  `technical-writing` (source `riekelt/technical-writer`); the lock file holds the
  same source and installation date for each

#### Scenario: No omission
- **WHEN** a reviewer lists the skills in the global lock file on Akim's machine
- **THEN** every one of them appears in the record

### Requirement: Non-functional — skill record content
The system SHALL keep skill records free of local absolute paths, access tokens, and
credentials, and SHALL limit each entry to developer, skill, source repository, scope,
and date.

#### Scenario: Review a skill record
- **WHEN** a reviewer reads a skill record
- **THEN** it contains no home-directory path, token, or credential, and no field
  other than developer, skill, source repository, scope, and date
