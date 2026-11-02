# Design

Copy the source tree without modifying Claude files. Markdown and JSON copies
preserve provenance. Standalone `.codex/agents/*.toml` retain role bodies and adapt
Claude tool names to available Codex tools; omit Claude model names so Codex
inherits its selected model. Read-only reviewer instructions remain read-only.

Mirror skills in `.codex/skills/`, discovered through relative directory symlinks
in `.agents/skills/`. Preserve existing find-skills. Six `.codex/commands/opsx/`
Markdown commands remain references; six `opsx-*` skill adapters provide invocation
as `$opsx-apply` etc., forwarding to the corresponding mirrored command.

Keep shared `settings.json` and ignored `settings.local.json` as exact source
copies. Codex does not interpret these JSON files. Native `config.toml` selects
workspace-write and on-request approval. A developer instruction reads permission
intent from both JSON files; these instructions do not enforce filesystem denial.
Native rules prompt for mutation/install commands and forbid supported dangerous
command prefixes without claiming complete Claude wildcard equivalence.
No broad allow rules or automatic package installs are added. Local permissions
are advisory, inherit managed restrictions and cannot bypass an approval.

Ignore `.codex/settings.local.json` in Git. No native config.local.toml loader is
assumed. Local JSON content is not copied into shared prose or config.
The project must be trusted and a new Codex session started for native discovery.
Existing running-session permissions and agent catalogs are unchanged.

Validation covers source equality, TOML parsing and CLI strict startup acceptance,
skill frontmatter and discoverable links, JSON validity and ignore behavior,
source preservation and OpenSpec validation. Application performance, UI and
application branch coverage are N/A: this feature changes instructions and
configuration only, with no executable application code. No Python/C++ boundary
changes. Full application suites are not required.

Official references:
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/rules

## Review clarifications

This is a change with code under AGENTS.md because settings and `.gitignore`
are included. There are no executable helper scripts shipped and no executable
statements/branches to measure; coverage has an empty denominator, not a waiver
for configuration files. If executable helpers are added, >=95% branch coverage
is required. Tester uses the feature GO path, not the no-code acknowledgement path.

Replace the broad `.agents/` ignore with `.agents/*`, allow `.agents/skills/`,
ignore its children by default and explicitly allow each mirrored skill directory.
Track the relative discovery links; keep installed find-skills ignored and unchanged.
A normal checkout therefore retains discovery. Verify links with git check-ignore.
Verify both JSON copies for equality, and the local copy for Git exclusion.

Native prompt prefixes: git add/commit/merge/push, docker, npm install/i,
pip/pip3 install. Forbidden prefixes: sudo; rm -rf/-fr/-r -f/-f -r;
git reset --hard, clean -f, branch -D, push --force/-f; chmod -R 777.
Check representative safe, prompt and forbidden commands. Prefixes do not cover
flags placed elsewhere or Claude wildcard/pipeline/Read/Edit patterns; preserve
those as source JSON and advisory instructions without enforcement claims.
