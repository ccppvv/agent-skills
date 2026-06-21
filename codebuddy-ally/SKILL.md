---
name: codebuddy-ally
description: Delegates coding tasks to Codebuddy CLI for prototyping, debugging, and code review. Use when needing algorithm implementation, bug analysis, or code quality feedback. Supports multi-turn sessions via SESSION_ID.
---

## ⚠️ MANDATORY USAGE RULE

**When user invokes `/codebuddy-ally` command:**
- ✅ ALWAYS use `codebuddy_bridge.py` to delegate the task to Codebuddy
- ❌ NEVER execute the task directly with other tools (Bash, Read, Edit, etc.)
- The user's explicit choice to use this skill means they want Codebuddy involvement

**Exception:** Only skip Codebuddy if the task is literally "show help" or "explain this skill"

## When to Use Codebuddy-Ally

Delegate to Codebuddy when:
- ✅ User explicitly invokes `/codebuddy-ally` (MANDATORY)
- Multi-step debugging or analysis
- Need code review from Codebuddy perspective
- Want to leverage Codebuddy's reasoning for prototyping
- Continue existing Codebuddy session (SESSION_ID provided)

Do NOT delegate when:
- User uses other commands/skills without explicit `/codebuddy-ally` call
- Simple queries about Codebuddy itself (help/docs)

## Quick Start

```bash
python scripts/codebuddy_bridge.py --cd "/path/to/project" --PROMPT "Your task"
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

## Parameters

```
usage: codebuddy_bridge.py [-h] --PROMPT PROMPT --cd CD [--sandbox {read-only,workspace-write,danger-full-access}] [--SESSION_ID SESSION_ID] [--skip-git-repo-check]
                       [--return-all-messages] [--image IMAGE] [--model MODEL] [--yolo] [--profile PROFILE]

Codebuddy Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to codebuddy.
  --cd CD               Set the workspace root for codebuddy before executing the task.
  --sandbox {read-only,workspace-write,danger-full-access}
                        Sandbox policy for model-generated commands. Defaults to `read-only`.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the codebuddy. Defaults to `None`, start a new session.
  --skip-git-repo-check
                        Allow codebuddy running outside a Git repository (useful for one-off directories).
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the codebuddy session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --image IMAGE         Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.
  --model MODEL         The model to use for the codebuddy session. This parameter is strictly prohibited unless explicitly specified by the user.
  --yolo                Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.
  --profile PROFILE     Configuration profile name to load from `~/.codebuddy/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python scripts/codebuddy_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python scripts/codebuddy_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

## Common Patterns

**Prototyping (read-only, request diffs):**
```bash
python scripts/codebuddy_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging"
```

**Debug with full trace:**
```bash
python scripts/codebuddy_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```
