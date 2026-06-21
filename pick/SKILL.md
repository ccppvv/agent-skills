---
name: pick
description: Continue a past coding session's work in the current session, or reopen it — by session ID or alias name, across Codex and Claude Code, even from a different project directory. Use whenever the user gives a session ID (UUID, prefix, or name) and wants to resume / continue / return to / switch to that session, get back into prior work, or port a session's in-progress work into the current one (e.g. the original tool crashed, or they want to switch tools mid-task). Searches globally across Codex (~/.codex/sessions) and Claude Code (~/.claude/projects), auto-detects the type, locates the original project, and by default emits a handoff context for continuing the work here (with a relaunch command as fallback). Trigger on phrases like "resume <id>", "continue session <id>", "接着那个 session", "接着这个 session 干", "continue <id> here", "codex 挂了接着干", "switch to session", "go back to that session", or any time the user pastes a UUID wanting to resume — even without the word "resume".
---

# Pick

The user gives a session ID (full UUID, prefix, or name). You locate it globally across Codex and Claude Code, identify what it is, and then — because this skill always runs *inside* a session — the default is to **continue that session's work here**, not to hand them a command to paste elsewhere. If they wanted to leave and reopen, they'd just exit and `claude --resume` themselves; invoking the skill in-session signals they want the effect here.

Verified facts on this machine:
- **Codex** (`codex` CLI, codex-cli 0.141.0): sessions at `~/.codex/sessions/YYYY/MM/DD/rollout-*-<UUID>.jsonl`. Filename UUID = session ID (UUIDv7). Storage is global; `codex resume <UUID>` looks up globally. **No prefix matching** — full UUID or name only. `-C <dir>` sets the working dir; `--all` disables cwd filtering for the picker.
- **Claude Code**: sessions at `~/.claude/projects/<encoded-cwd>/<UUID>.jsonl`. `claude --resume <UUID>` **only searches the current project dir** — it can't find a session from another directory. You must `cd` into the session's original project first. The real cwd is read from inside the file (each line carries `cwd`), not decoded from the lossy `/`→`-` folder name.

## Default: continue the work HERE

```bash
python3 ~/.agents/skills/pick/scripts/locate_session.py <ID> --continue-here [--copy]
```

It locates the session (global search, auto-detects type), streams the full transcript, and emits a **HANDOFF CONTEXT**: original intent, latest todo snapshot (or tasks created, when the source used TaskCreate), files touched (most-recent first), the last ~12 turns, the last assistant state, and a **RELAUNCH** line — the exact command to reopen the session elsewhere, as a fallback.

The script only reads; synthesis is your job. Once you have the handoff:

1. Read it and produce a short brief: **Task / Done / In progress / Next / Files**. Surface the todo list prominently — it's the most reliable signal of where work stopped.
2. Note any project mismatch: if the handoff's `project` differs from the current cwd, say so and ask whether to work against the source project.
3. If the source tracked tasks via TaskCreate/TaskList (not TodoWrite), the snapshot only has subjects — run `TaskList` for live statuses before planning.
4. Confirm the plan, then continue the work in this session. Reconstruct state from the brief + files on disk; tool-specific internals may not transfer exactly, and that's fine — the work product lives in the files.

This works across tools (a Codex session's work continued in this Claude Code session, and vice versa) and same-tool (continue a different Claude Code session's work without leaving this one).

## When they actually want to reopen / switch

If the user signals they want to *leave and reopen* — "重开"/"switch to"/"open that session"/"go back into"/"我要进入那个 session" — hand them the **RELAUNCH** command from the handoff output. Be honest about the harness limit: you cannot switch the current session in-place. Resuming is a launch-time (`--resume`) decision owned by the harness, not by a skill. So:

- Tell them to exit the current session first (`/exit` or Ctrl+D) then run the command, or use a new terminal.
- Don't `exec` or spawn a nested `claude`/`codex` from Bash — interactive TUIs need a TTY the Bash tool doesn't provide, and a nested session isn't a switch anyway.
- Offer `--copy` to put the relaunch command on the clipboard.

The script's RELAUNCH line is already `shlex.quote`-d, so it's safe to paste directly.

## Orientation only (lighter)

If the user just wants to know what an ID is — no continuation, no relaunch — the handoff already shows project/type/intent/last-active at the top. For an even lighter one-liner (no transcript read), use plain locate mode:

```bash
python3 ~/.agents/skills/pick/scripts/locate_session.py <ID> [--type codex|claude] [--json] [--copy]
```

No match? List recent sessions from both tools so the user can pick:

```bash
python3 ~/.agents/skills/pick/scripts/locate_session.py --recent
```

Exit codes: `0` single match / ok, `1` no match, `2` multiple matches, `3` bad usage.

## Auto-detection (no --type given)

Both tools use UUIDs, so format alone can't tell them apart. The script decides by **which store contains the ID**: it searches `~/.claude/projects/**` and `~/.codex/sessions/**` and picks the tool that has a matching file. If both have it (rare), it reports both and you ask. Prefixes are expanded to full UUIDs by filename search — necessary because Codex rejects prefixes at resume time. `--type codex|claude` forces a tool when the user names it or the ID is ambiguous.

## Aliases — resume by name

Sessions can be given short names via the `throw` skill (stored in `~/.agents/skills/throw/aliases.json`). When the user gives an alias name instead of a UUID, the locator resolves it to the stored id before searching — **aliases take precedence over UUID/prefix lookup**. The stored tool (if any) is used as a `--type` hint. The output prints `(via alias '<name>' -> <id>)` so the resolution is visible.

Manage aliases with the sibling skill:

```bash
python3 ~/.agents/skills/throw/alias_session.py set <name> [<id>] [--note "..."]   # no id -> current session
python3 ~/.agents/skills/throw/alias_session.py list
python3 ~/.agents/skills/throw/alias_session.py rm <name>
```

So `resume <alias>` works directly — the user doesn't need to know the UUID.

## Examples

**"resume 0793405f-…"** (default, in-session) → run `--continue-here` → it's a Claude Code session in /Users/v/Apps/TypeLess about continuing a Codex session → present the brief (Task/Done/Next/Files) and continue the work here. The RELAUNCH line `cd /Users/v/Apps/TypeLess && claude --resume 0793405f-…` is there if they'd rather reopen it.

**"接着那个 session：a1b2c3d4-…"** → `--continue-here` → continue that session's work here; note the project if it differs from the current cwd.

**"重开 019ee890-… 那个 codex session"** (explicit reopen) → they want to switch, not continue here → hand them `codex resume 019ee890-… -C /Users/v/Apps/TypeLess`, tell them to exit first, offer `--copy`.

**"resume abc123"** (prefix, several matches) → script lists matches and exits 2 → ask which, then proceed by full UUID.

**"我之前那个 session 不知道是哪个项目的"** → `--recent`, show both tools' recent sessions, let them point at one.
