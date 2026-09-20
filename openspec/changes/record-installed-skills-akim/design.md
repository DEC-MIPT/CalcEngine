# Design

## Context

`development-process` already says a new skill "SHALL be recorded in the specs with the
installing developer" but defines neither what the record contains nor where it lives.
This change defines the content and adds the first record. It is documentation only.

## Goals

- One clear, checkable record format: developer, skill, source, scope, date.
- A record that stays correct when the colleague adds their own.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **Add a new requirement, do not modify the existing one.** The existing requirement
   is correct; it lacks only the record content. Adding avoids rewriting shared text
   and keeps the delta small.
2. **Record lives in the scenario of the new requirement.** The spec format has no data
   tables for facts, and a scenario is testable by reading. The record is expected to
   be extended by later changes, each adding scenarios for one developer.
3. **One change per developer.** Each developer records their own installs in their own
   change (`record-installed-skills-<developer>`), so zones do not overlap and the two
   changes cannot contradict each other.
4. **Scope is recorded.** `find-skills` was installed at project scope (`.agents/`,
   gitignored); the other six globally in the user's home. Scope tells a reader whether
   a skill applies to every project on that machine or only to this one.
5. **Sources are recorded as repositories**, exactly as in the `npx skills add`
   commands of `AGENTS.md` section 9, so a record can be replayed.

## Component boundary

Not applicable. No code is written, so there is no calculation hot path and no C/C++
swap boundary.

## Non-functional requirements

- Security: the record holds only skill name, source repository, scope, and date.
- Accessibility, performance, coverage: not applicable (documentation only).

## Risks

- **Stale record.** A skill may later be removed or updated; nothing in this change
  detects that. Accepted for MVP; the record states the date it was made.
- **Recording is not endorsement.** The `npx skills` CLI reported Snyk "Med Risk" for
  `find-skills`, `webapp-testing`, and `doc-coauthoring` and one Socket alert for
  `webapp-testing`, and states that skills run with full agent permissions. The record
  does not assess them.
- **Duplicated requirement text.** The new requirement partly restates the existing
  one; it is kept to content of the record only.
