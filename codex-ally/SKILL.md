---
name: codex-ally
description: Delegates coding tasks to Codex CLI for prototyping, debugging, and code review. Use when needing algorithm implementation, bug analysis, or code quality feedback. Supports multi-turn sessions via SESSION_ID.
---

## ⚠️ MANDATORY USAGE RULE

**When user invokes `/codex-ally` command:**
- ✅ ALWAYS use `codex_bridge.py` to delegate the task to Codex
- ❌ NEVER execute the task directly with other tools (Bash, Read, Edit, etc.)
- The user's explicit choice to use this skill means they want Codex involvement

**Exception:** Only skip Codex if the task is literally "show help" or "explain this skill"

## When to Use Codex-Ally

Delegate to Codex when:
- ✅ User explicitly invokes `/codex-ally` (MANDATORY)
- Multi-step debugging or analysis
- Need code review from Codex perspective
- Want to leverage Codex's reasoning for prototyping
- Continue existing Codex session (SESSION_ID provided)

Do NOT delegate when:
- User uses other commands/skills without explicit `/codex-ally` call
- Simple queries about Codex itself (help/docs)

## Quick Start

```bash
python3 scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "Your task"
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

## Parameters

```
usage: codex_bridge.py [-h] --PROMPT PROMPT --cd CD [--sandbox {read-only,workspace-write,danger-full-access}] [--SESSION_ID SESSION_ID] [--skip-git-repo-check]
                       [--return-all-messages] [--image IMAGE] [--model MODEL] [--yolo] [--profile PROFILE]

Codex Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to codex.
  --cd CD               Set the workspace root for codex before executing the task.
  --sandbox {read-only,workspace-write,danger-full-access}
                        Sandbox policy for model-generated commands. Defaults to `read-only`.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the codex. Defaults to `None`, start a new session.
  --skip-git-repo-check
                        Allow codex running outside a Git repository (useful for one-off directories).
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the codex session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --image IMAGE         Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.
  --model MODEL         The model to use for the codex session. This parameter is strictly prohibited unless explicitly specified by the user.
  --yolo                Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.
  --profile PROFILE     Configuration profile name to load from `~/.codex/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python3 scripts/codex_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python3 scripts/codex_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

## Common Patterns

**Prototyping (read-only, request diffs):**
```bash
python3 scripts/codex_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging"
```

**Debug with full trace:**
```bash
python3 scripts/codex_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```

**Write mode (let codex edit files):**
```bash
python3 scripts/codex_bridge.py --cd "/project" --sandbox workspace-write --PROMPT "Fix the null pointer bug in auth.ts"
```

## 🚀 Parallel Execution

### Why Use Parallel Execution

When implementing multiple independent modules simultaneously, parallel execution can dramatically speed up development:
- 4 modules in parallel = 4x faster than sequential
- Each task runs in isolated Codex session
- Ideal for scaffolding new projects or large refactors

### Direct Bash Invocation (Recommended for Parallel Tasks)

The Skill tool cannot properly handle parallel codex-ally invocations. For parallel execution, use direct Bash calls:

```bash
cd /Users/v/.agents/skills/codex-ally

# Launch multiple tasks in background
python3 scripts/codex_bridge.py \
  --cd "/path/to/project" \
  --PROMPT "根据 docs/config.md 实现配置模块" \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 scripts/codex_bridge.py \
  --cd "/path/to/project" \
  --PROMPT "根据 docs/cli.md 实现 CLI 模块" \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 scripts/codex_bridge.py \
  --cd "/path/to/project" \
  --PROMPT "根据 docs/session.md 实现会话模块" \
  --sandbox workspace-write \
  --skip-git-repo-check &

# Wait for all tasks to complete
wait

echo "All modules implemented, running verification..."
cargo check  # or npm test, pytest, etc.
```

### Using Claude Code's Bash Tool for Parallel Tasks

When orchestrating from Claude Code, use the `run_in_background` parameter:

```xml
<!-- Task 1 -->
<invoke name="Bash">
<parameter name="command">cd /Users/v/.agents/skills/codex-ally && python3 scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "实现配置模块" --sandbox workspace-write --skip-git-repo-check</parameter>
<parameter name="description">实现配置模块 (background)</parameter>
<parameter name="run_in_background">true</parameter>
<parameter name="timeout">120000</parameter>
</invoke>

<!-- Task 2 -->
<invoke name="Bash">
<parameter name="command">cd /Users/v/.agents/skills/codex-ally && python3 scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "实现 CLI 模块" --sandbox workspace-write --skip-git-repo-check</parameter>
<parameter name="description">实现 CLI 模块 (background)</parameter>
<parameter name="run_in_background">true</parameter>
<parameter name="timeout">120000</parameter>
</invoke>

<!-- Task 3 -->
<invoke name="Bash">
<parameter name="command">cd /Users/v/.agents/skills/codex-ally && python3 scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "实现会话模块" --sandbox workspace-write --skip-git-repo-check</parameter>
<parameter name="description">实现会话模块 (background)</parameter>
<parameter name="run_in_background">true</parameter>
<parameter name="timeout">120000</parameter>
</invoke>
```

### Monitoring Task Progress

Check background task outputs:

```bash
# List background tasks
ls /private/tmp/claude-*/tasks/*.output

# Monitor specific task
tail -f /private/tmp/claude-*/tasks/[task-id].output

# Check task completion and results
cat /private/tmp/claude-*/tasks/[task-id].output | jq -r '.agent_messages'
```

### Verifying Generated Files

```bash
# Check if files were created
ls -la /path/to/project/src/module/

# Wait and check again if tasks are still running
sleep 20 && ls -la /path/to/project/src/module/
```

### Example: Implementing 4 Modules in Parallel

```bash
# Step 1: Create detailed implementation documents
docs/
├── config-implementation.md    # Exact code requirements for config module
├── cli-implementation.md       # Exact code requirements for CLI module
├── session-implementation.md   # Exact code requirements for session module
└── tools-implementation.md     # Exact code requirements for tools module

# Step 2: Launch all tasks in parallel
cd /Users/v/.agents/skills/codex-ally

python3 scripts/codex_bridge.py \
  --cd "/Users/v/Gods/Iris" \
  --PROMPT "根据 /Users/v/Gods/Iris/docs/config-implementation.md 文档，实现配置模块。严格按照文档中的代码实现。" \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 scripts/codex_bridge.py \
  --cd "/Users/v/Gods/Iris" \
  --PROMPT "根据 /Users/v/Gods/Iris/docs/cli-implementation.md 文档，实现 CLI 模块。严格按照文档中的代码实现。" \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 scripts/codex_bridge.py \
  --cd "/Users/v/Gods/Iris" \
  --PROMPT "根据 /Users/v/Gods/Iris/docs/session-implementation.md 文档，实现会话模块。严格按照文档中的代码实现。" \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 scripts/codex_bridge.py \
  --cd "/Users/v/Gods/Iris" \
  --PROMPT "根据 /Users/v/Gods/Iris/docs/tools-implementation.md 文档，实现工具模块。严格按照文档中的代码实现。" \
  --sandbox workspace-write \
  --skip-git-repo-check &

# Step 3: Wait for all to complete
wait

# Step 4: Verify results
cargo check
```

## Best Practices for Parallel Execution

1. **Detailed Implementation Docs**: Create comprehensive implementation documents with exact code examples before launching parallel tasks
2. **One Module Per Task**: Keep tasks focused on single modules for better parallelization and easier debugging
3. **Explicit File Paths**: Use absolute paths in PROMPT to avoid ambiguity (e.g., `/full/path/to/docs/module.md`)
4. **Monitor Progress**: Check file creation timestamps to track progress while tasks are running
5. **Timeout Generously**: Set timeout to 120000ms (2 minutes) for complex modules
6. **Independent Modules**: Ensure modules don't have circular dependencies that would cause compilation errors

## Troubleshooting Parallel Execution

**Problem**: Task output file is empty
- **Solution**: Task is still running, wait longer (codex sessions can take 30-120 seconds)

**Problem**: Files not created
- **Solution**: Check output for error messages with `cat /private/tmp/claude-*/tasks/[id].output`, verify paths are correct

**Problem**: Compilation errors after generation
- **Solution**: Review generated code for cross-module dependencies, may need manual fixes

**Problem**: Skill tool invocation fails silently
- **Solution**: Use direct Bash invocation instead of `Skill(codex-ally)` for reliable execution

## Verification

Successful parallel execution should show:

1. **Tasks Started**: Background task IDs are returned for each invocation
2. **Output Files Created**: `/private/tmp/claude-*/tasks/[id].output` exists for each task
3. **Files Generated**: Target module files appear in project directory
4. **Success Messages**: Each output contains `"success": true` and agent messages

Example successful output:
```json
{
  "success": true,
  "SESSION_ID": "019c84ed-...",
  "agent_messages": "已按文档实现以下文件：\n- src/config/mod.rs\n- src/config/settings.rs\n..."
}
```
