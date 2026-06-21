---
name: symphony-elixir-preview-startup-flag
description: |
  启动 openai/symphony 的官方 Elixir 参考实现时使用。触发条件：
  (1) 按 README 运行 `./bin/symphony ./WORKFLOW.md` 后直接退出；
  (2) 终端提示 `This Symphony implementation is a low key engineering preview`；
  (3) 要求追加 `--i-understand-that-this-will-be-running-without-the-usual-guardrails`。
  解决 README 示例缺少实际必需启动参数的问题，并补充对应运行时版本信息。
author: Claude Code
version: 1.0.0
date: 2026-03-09
---

# Symphony Elixir Preview Startup Flag

## Problem
按照 `openai/symphony` 仓库中 `elixir/README.md` 的 Run 示例直接启动官方 Elixir 参考实现时，进程会立即退出，而不是进入轮询服务。

## Context / Trigger Conditions
在以下场景使用：

- 仓库是 `openai/symphony`
- 目标是 `elixir/` 下的官方参考实现
- 已完成 `mise exec -- mix setup` 和 `mise exec -- mix build`
- 运行 `mise exec -- ./bin/symphony ./WORKFLOW.md` 时退出
- 终端出现如下提示：

```text
This Symphony implementation is a low key engineering preview.
Codex will run without any guardrails.
To proceed, start with `--i-understand-that-this-will-be-running-without-the-usual-guardrails` CLI argument
```

## Solution
1. 先按仓库里的 `elixir/mise.toml` 安装指定运行时：
   - `erlang = "28"`
   - `elixir = "1.19.5-otp-28"`
2. 在 `elixir/` 目录执行官方准备流程：
   - `mise trust`
   - `mise install`
   - `mise exec -- mix setup`
   - `mise exec -- mix build`
3. 启动时不要只用 README 里的命令，必须追加确认参数：

```bash
mise exec -- ./bin/symphony ./WORKFLOW.md --i-understand-that-this-will-be-running-without-the-usual-guardrails
```

4. 如果只是验证是否能启动，观察到状态面板出现并开始刷新即可；验证后可停止进程，避免持续轮询。

## Verification
满足以下任一项即可判定修复生效：

- 不再立即退出
- 进入 `SYMPHONY STATUS` 终端面板
- 显示 `Agents: 0/10`、`Project: https://linear.app/project/...`、`Next refresh: ...`
- 周期性刷新状态而不是报错退出

## Example
```bash
cd /path/to/symphony/elixir
mise trust
mise install
mise exec -- mix setup
mise exec -- mix build
mise exec -- ./bin/symphony ./WORKFLOW.md --i-understand-that-this-will-be-running-without-the-usual-guardrails
```

## Notes
- 这是官方 README 与当前实现行为不完全一致导致的启动坑。
- 该参数的含义是显式确认：这是一个低保护、仅供评估的 engineering preview。
- 即使本机没有配置 `LINEAR_API_KEY`，追加参数后进程仍可能先进入状态面板并开始轮询；是否真正接入 Linear 取决于后续环境变量与工作流配置。
- 如果后续 README 更新并补上该参数，这个技能应同步修订或归档。

## References
- https://github.com/openai/symphony/blob/main/elixir/README.md
- https://github.com/openai/symphony/blob/main/elixir/mise.toml
