---
name: claude-code-task-team-fallback
description: |
  处理 Claude Code 调用 Task 子代理时报 “Team ... does not exist” 的降级流程。
  触发条件：
  (1) 使用 Task 调用 specialized subagent；
  (2) 工具返回 team 未初始化错误；
  (3) 当前任务需要继续推进并可由主流程完成最小审查/验证。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Claude Code Task Team Fallback

## Problem
在某些环境中，调用 Task 子代理会失败并返回：
`Team "..." does not exist. Call spawnTeam first to create the team.`
这会阻断原计划中的并行审查或专项分析流程。

## Context / Trigger Conditions
- 你正在调用 `Task` 运行 code-review/security-review 等 subagent
- 报错明确指出 team 未初始化
- 当前上下文没有可用的 team 初始化路径或不适合继续反复尝试

## Solution
1. **立即停止重复同类失败调用**
   - 避免在同一参数组合上无意义重试

2. **切换到主流程降级方案**
   - 用 Read/Grep/Glob/Bash（测试）完成最小必要审查：
     - 类型检查
     - 关键路径逻辑核查
     - 基础安全点（输入、输出、注入、文件写入）

3. **记录降级原因与影响**
   - 在 `progress.md` 的 Error Log 记录：
     - 原错误
     - 已采取的降级动作
     - 后续建议（如可用时补做子代理审查）

4. **保持交付连续性**
   - 优先修复阻断问题
   - 明确说明哪些审查是“已完成”，哪些是“建议后补”

## Verification
- 任务主目标已完成
- 有类型检查/基础回归结果
- Error Log 中有 team 未初始化错误与降级记录
- 用户可得到可执行成果与下一步建议

## Example
症状：
`Team "feature-dev" does not exist. Call spawnTeam first to create the team.`

处理：
- 停止继续调用该 subagent
- 主流程执行 `pnpm tsc --noEmit` + 关键文件 Read 自审
- 在 progress 文件写入“子代理调用失败，已降级主流程自审”

## Notes
- 如果后续环境支持 team 初始化，可补跑专项子代理审查并更新记录
- 降级不是放弃质量，而是保证在受限环境下持续推进

## References
- https://docs.anthropic.com/en/docs/claude-code
