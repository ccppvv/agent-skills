---
name: claude-ally
description: 将编码任务委托给 Claude Code CLI（支持原型开发、排障、代码审查）。通过 SESSION_ID 支持多轮连续会话。
---

## ⚠️ 强制使用规则

**当用户调用 `/claude-ally` 命令时：**
- ✅ 必须使用 `claude_bridge.py` 将任务委托给 Claude Code
- ❌ 永远不要直接使用其他工具（Bash、Read、Edit 等）执行任务
- 用户明确选择使用此 skill 意味着他们希望 Claude Code 参与

**例外：** 仅当任务字面上是"显示帮助"或"解释此 skill"时才跳过 Claude Code

## 何时使用 Claude-Ally

委托给 Claude Code 的情况：
- ✅ 用户明确调用 `/claude-ally`（强制）
- 多步骤调试或分析
- 需要 Claude Code 视角的代码审查
- 希望利用 Claude Code 的推理进行原型开发
- 继续现有 Claude Code 会话（提供了 SESSION_ID）

不委托的情况：
- 用户使用其他命令/skills 而未明确调用 `/claude-ally`
- 关于 Claude Code 本身的简单查询（帮助/文档）

## 快速开始

```bash
python3 scripts/claude_bridge.py --cd "/path/to/project" --PROMPT "你的任务描述"
```

**输出：** JSON，包含 `success`、`SESSION_ID`、`agent_messages`，失败时包含 `error`。

## 参数说明

```text
usage: claude_bridge.py [-h] --PROMPT PROMPT --cd CD [--SESSION_ID SESSION_ID]
                        [--permission-mode {default,acceptEdits,bypassPermissions,dontAsk,plan}]
                        [--allowed-tools ALLOWED_TOOLS] [--disallowed-tools DISALLOWED_TOOLS]
                        [--append-system-prompt APPEND_SYSTEM_PROMPT] [--return-all-messages]
                        [--model MODEL] [--dangerously-skip-permissions]

Claude Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       发给 Claude 的任务指令。
  --cd CD               运行目录（项目根目录）。
  --SESSION_ID SESSION_ID
                        续接已有会话的 session_id；为空则新建会话。
  --permission-mode {default,acceptEdits,bypassPermissions,dontAsk,plan}
                        Claude Code 权限模式，默认 default。
  --allowed-tools ALLOWED_TOOLS
                        允许的工具列表（逗号分隔），例如 "Bash,Edit,Read"。
  --disallowed-tools DISALLOWED_TOOLS
                        禁用的工具列表（逗号分隔）。
  --append-system-prompt APPEND_SYSTEM_PROMPT
                        追加 system prompt。
  --return-all-messages
                        返回 Claude 原始 JSON 响应（便于调试）。
  --model MODEL         指定模型。除非用户明确要求，否则禁止设置。
  --dangerously-skip-permissions
                        跳过权限检查，仅在可信沙箱中使用。
```

## 多轮会话

**首轮务必保存 `SESSION_ID`**，后续请求复用该值：

```bash
# 第一次
python3 scripts/claude_bridge.py --cd "/project" --PROMPT "分析 login.py 的认证流程"

# 继续同一会话
python3 scripts/claude_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "基于上一步写单测"
```

## 常见模式

**只读评审（推荐）**

```bash
python3 scripts/claude_bridge.py \
  --cd "/project" \
  --permission-mode default \
  --allowed-tools "Read,Grep,Glob" \
  --PROMPT "做一次代码审查，输出高风险问题和修复建议"
```

**深度排障（返回原始 JSON）**

```bash
python3 scripts/claude_bridge.py \
  --cd "/project" \
  --PROMPT "定位这个堆栈错误并给出最小修复" \
  --return-all-messages
```

**计划模式（先出方案再改）**

```bash
python3 scripts/claude_bridge.py \
  --cd "/project" \
  --permission-mode plan \
  --PROMPT "先给出分步实施计划，再等待确认"
```
