---
name: throw
description: Create, list, and remove session aliases — short names that map to session IDs, so you can resume them by name with pick. Use whenever the user wants to name / label / bookmark the current session ("alias this session as auth", "name this session", "save this as auth", "给这个 session 起个名"), list aliases ("what aliases do I have", "list session aliases"), or remove / show one. Pairs with pick — once aliased, "resume <alias>" resolves to the session. Trigger on "alias ... as ...", "bookmark this session", "list aliases", "remove alias X", "show alias X".
---

# Session Alias

Give sessions short, memorable names so the user can resume them by name instead of pasting UUIDs. Aliases live in `~/.agents/skills/throw/aliases.json` (a name → session-id map) and are resolved automatically by the `pick` skill.

## The script

```bash
python3 ~/.agents/skills/throw/alias_session.py <command>
```

- `set <name> [<session-id>] [--note "..."]` — alias a session to `<name>`. With no session-id, it aliases the **current** session (detected via `CLAUDE_CODE_SESSION_ID`, falling back to the newest session file in the current project). With an explicit id, it aliases that session (any tool — tool/project resolved at resume time).
- `list` — show all aliases (name → id, tool/project if known, created, note).
- `rm <name>` — remove an alias.
- `show <name>` — show one alias's details.

Names match `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`. Setting an existing name overwrites it (the script prints `updated` vs `set`).

## How to use

**Name the current session:**
```
alias_session.py set auth --note "login refactor, WIP"
```

**Resume it later by name** — hand the alias to pick:
```
pick auth            # continues here (--continue-here default)
pick auth --copy     # copies the relaunch command
```
pick resolves `auth` → the stored id before searching, so aliases take precedence over UUID/prefix lookup. It prints `(via alias 'auth' -> <id>)` so the resolution is visible.

**From Codex, or aliasing a non-current session:** pass the id explicitly — `set <name> <id>`. Auto-detection of the *current* session relies on `CLAUDE_CODE_SESSION_ID` (Claude Code); for Codex or other tools, give the id.

## Examples

- "把这个 session 命名为 auth" → `set auth` (current session, auto-detected).
- "给 session 019ee890-… 起个名叫 codex-auth" → `set codex-auth 019ee890-...`.
- "我有哪些 session 别名" → `list`.
- "auth 是哪个 session" → `show auth`.
- "删掉 auth 这个别名" → `rm auth`.
