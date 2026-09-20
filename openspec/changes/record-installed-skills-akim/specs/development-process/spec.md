## ADDED Requirements

### Requirement: Installed skills are recorded per developer
The system SHALL record, for each skill a developer installs on their machine, the
developer name, the skill name, the source repository, the install scope (project or
global), and the installation date. Each developer SHALL record their own installs in
their own OpenSpec change.

#### Scenario: Akim installs the required skills on 2026-09-20
- **WHEN** Akim installed the required skills with `npx skills add` on 2026-09-20
- **THEN** the record names Akim and lists seven skills, all dated 2026-09-20:
  `find-skills` (source `vercel-labs/skills`, project scope);
  `vercel-react-best-practices`, `vercel-composition-patterns`, and
  `web-design-guidelines` (source `vercel-labs/agent-skills`, global scope);
  `webapp-testing`, `doc-coauthoring`, and `frontend-design` (source
  `anthropics/skills`, global scope)

#### Scenario: Akim installs optional skills on 2026-09-20
- **WHEN** Akim installed optional skills with `npx skills add` on 2026-09-20
- **THEN** the record names Akim and lists eight skills, all dated 2026-09-20 and all
  in global scope: `pytest-skill` (source `lambdatest/agent-skills`);
  `python-code-quality` (source `laurigates/claude-plugins`);
  `postgresql-database-engineering` (source `manutej/luxor-claude-marketplace`);
  `owasp-security` (source `hoodini/ai-agents-skills`); `code-security` (source
  `semgrep/skills`); `accessibility` (source `addyosmani/web-quality-skills`);
  `software-architecture-design` (source `vasilyu1983/ai-agents-public`);
  `technical-writing` (source `riekelt/technical-writer`)

#### Scenario: Colleague installs a skill
- **WHEN** Egor installs a skill
- **THEN** it is recorded in a separate change naming Egor, and Akim's record is not
  edited

### Requirement: Non-functional — skill record content
The system SHALL keep skill records free of local absolute paths, access tokens, and
credentials, and SHALL limit each entry to developer, skill, source repository, scope,
and date.

#### Scenario: Review a skill record
- **WHEN** a reviewer reads a skill record
- **THEN** it contains no home-directory path, token, or credential, and no field
  other than developer, skill, source repository, scope, and date
