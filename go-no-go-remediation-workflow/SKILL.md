---
name: go-no-go-remediation-workflow
description: |
  将 Go/No-Go 打分表直接落地为 task_plan 下一阶段并驱动整改执行。用于：
  (1) 已有门禁项但缺少执行抓手；
  (2) 需要按 P0/P1 优先级并行推进；
  (3) 单 HTML 工具页场景下快速补齐执行闭环、评分治理闭环、工具容错与可观测性。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Go/No-Go Remediation Workflow

## Problem
很多团队能做出 Go/No-Go 评审表，但无法把“评审结论”快速转成可执行的开发阶段，导致门禁长期停留在文档层面，整改失速。

## Context / Trigger Conditions
- 已完成初版 MVP，并产出 P0/P1 打分表
- 需要进入“整改执行”而非继续讨论
- 典型症状：
  - 评审项存在，但 task_plan 没有对应阶段
  - P0 项知道要做，但开发顺序和并行分组不清楚
  - 验证后遗留服务进程未清理

## Solution
1. **把门禁表映射到 task_plan 下一阶段**
   - 新增如 `Phase 6: Go/No-Go 门禁整改（P0/P1）`
   - 将每个关键门禁项直接改写成可勾选任务（checkbox）
   - 阶段状态跟随真实进展：`in_progress -> complete`

2. **先并行 P0 最小闭环，再处理 P1 质量项**
   - P0 并行首批建议：
     - P0-01：执行闭环（页面按钮 -> pipeline 运行 -> 结果回显）
     - P0-03：评分治理闭环（`/api/ratings` + retention 落盘）
     - P0-05：基础可追溯（关键路径日志/错误输出）
   - P1 紧随：参数链路与工具加载容错

3. **在无完整后端时，先落地“本地 HTTP 最小闭环”**
   - 增加本地接口（如 `/api/ratings`）
   - 评分写入 `ratings.json` 并写 retention 决策到 `retention.json`
   - 前端保留离线 fallback，确保页面可用性

4. **工具加载采用“单文件容错 + 全空保护”**
   - 单个坏 JSON：`try/catch` 跳过并告警
   - 全部不可用：统一抛错并终止流程

5. **验证后清理后台进程**
   - 启动本地验证服务后，测试完成必须显式停止（避免残留进程）

## Verification
- `task_plan.md` 中存在门禁整改阶段和可勾选任务
- P0 首批项有对应代码落地与回归验证
- 评分数据与 retention 决策文件有新增记录
- 工具目录存在坏文件时不会拖垮全量加载
- 背景服务在验证完成后已停止

## Example
- 阶段落地：`Phase 6: Go/No-Go 门禁整改（P0/P1）`
- 执行闭环：页面新增执行按钮并显示最终输出类型
- 评分闭环：`POST /api/ratings` 返回 `{ action: keep|destroy|ttl_expire }`
- 数据证据：`data/ratings.json` 与 `data/retention.json` 持续增长

## Notes
- 本技能强调“把评审表变成执行计划”，不是替代架构设计
- 本地 HTTP 闭环是过渡方案，后续应迁移到正式后端与鉴权体系
- 对外上线前，仍需补齐单用户访问控制与沙箱隔离

## References
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- https://owasp.org/www-community/attacks/Path_Traversal
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
