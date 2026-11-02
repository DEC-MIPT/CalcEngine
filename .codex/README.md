# DEC Codex project tooling

Claude remains canonical. `agents/*.md`, `commands/`, `skills/` and `settings.json`
are source copies. `settings.local.json` is a local, Git-ignored copy.
To refresh source copies, copy `.claude/` again and regenerate the native adapters;
check equality and review changed roles and permissions before using them.

## Use

Start a new Codex session in this trusted repository. Project `config.toml`, agent
TOML and rules load at startup; this does not change an existing session's tools.
Ask Codex to use a named role such as tester or frontend-developer.
Project skills are exposed through relative `.agents/skills/` directory symlinks.
Use `$opsx-apply <change>`, `$opsx-propose`, `$opsx-explore`, `$opsx-update`,
`$opsx-sync` or `$opsx-archive`. The original `/opsx:*` command files remain
references; copying them does not register Claude slash commands in Codex.

## Permissions and compatibility

Native config selects workspace-write and on-request. Rules prompt for selected
mutation/install commands and forbid explicit dangerous prefixes. No outside-sandbox
allow rules are generated. Host and managed restrictions retain precedence.
Claude tool lists and model names remain only in Markdown source copies;
TOML roles inherit the parent model and adapt tool references.

Codex does not natively load `settings.json` or `settings.local.json`.
The config instructs agents to read their permission intent. Claude Read/Edit glob
restrictions are behavioral instructions, not enforced Codex filesystem rules.
Command-prefix rules cannot reproduce arbitrary Claude globs (including force-push
flags after other arguments and shell pipelines). No claim of identical enforcement
is made. Local allow entries do not bypass the sandbox or grant escalation.
There is no assumed automatic `config.local.toml` loader. Personal JSON stays local;
no personal permissions, credentials or machine paths are embedded in shared config.

## Sources

- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Configuration reference](https://developers.openai.com/codex/config-reference)
- [Command rules](https://developers.openai.com/codex/rules)
