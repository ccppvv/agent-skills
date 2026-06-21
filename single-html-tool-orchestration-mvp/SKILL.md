---
name: single-html-tool-orchestration-mvp
description: |
  用于“单 JS/单 HTML 工具仓”场景下的自动编排与页面生成。触发条件：
  (1) 用户以自然语言描述组合式工具需求；
  (2) 工具遵循 ToolSpec + process 接口；
  (3) 需要快速生成临时单 HTML 页面；
  (4) 出现“按 MIME 选路导致操作意图丢失”或“工具元信息直出带来 XSS 风险”问题。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Single HTML Tool Orchestration MVP

## Problem
在“web 武器库”模式中，用户希望一句自然语言就能得到一个可用的临时单 HTML 工具页。常见问题是：
1) 编排器只按 MIME 找路径，忽略用户明确动作（如“压缩后加水印”）；
2) 生成 HTML 时直接插入工具元信息，存在注入风险；
3) TypeScript Node 运行环境配置缺失导致 `node:fs` / `process` 等类型报错。

## Context / Trigger Conditions
- 工具契约统一为 `window.ToolSpec` + `window.process`
- 场景是“即用即走”的临时工具生成
- 出现以下症状之一：
  - 生成页面可运行，但步骤与用户描述动作不一致
  - 生成 HTML 中直接渲染未转义的工具 name/description/step
  - TypeScript 报错：`Cannot find module 'node:fs'` 或 `Cannot find name 'process'`

## Solution
1. **规划文件先行（planning-with-files）**
   - 在项目目录创建并维护：`task_plan.md`、`findings.md`、`progress.md`
   - 每个阶段推进后立即回写状态、错误与验证结果

2. **编排策略采用“操作序列优先 + MIME 回退”**
   - 先从自然语言提取操作序列（compress/watermark/clean/convert）
   - 按当前 MIME 逐步匹配每个操作对应工具
   - 若操作链产出 MIME 与目标不一致，再补“转换工具”
   - 无明确操作时再回退到 MIME 路径搜索

3. **生成层默认输出转义**
   - 对动态插入 HTML 的工具元信息与步骤 JSON 做统一 `escapeHtml`
   - 在 UI 回填中优先 `textContent` / 安全文本写入方式
   - 禁止将未清洗字符串直接拼入可执行 HTML/JS 上下文

4. **Node + TypeScript 运行环境修复**
   - 安装：`pnpm add -D @types/node`
   - `tsconfig.json` 设置：
     - `module` / `moduleResolution` = `NodeNext`
     - `types: ["node"]`

5. **临时页与评分治理基础闭环**
   - 生成入口确保输出目录存在（自动创建 `output/`）
   - 评分写入前做范围校验（如 1~5）
   - 评分策略可先阈值化：高分保留、低分销毁、其他 TTL 回收

## Verification
- 类型检查通过：`pnpm tsc --noEmit`
- 至少三类需求可生成页面：图片 / 文本 / JSON
- 编排步骤与用户动作一致（例如“压缩后加水印”应保持该顺序）
- HTML 中动态显示内容经过转义，避免注入
- 评分输入越界时被拒绝

## Example
用户输入：`把图片压缩后加水印`

预期：
1) Parser 提取 `operations = [compress, watermark]`
2) Planner 先按操作链选工具，再判断是否需 MIME 转换
3) Composer 输出单 HTML 页面，并展示对应步骤
4) 页面评分后触发保留/销毁策略判定

## Notes
- 这是 MVP 策略，后续可增加：
  - 语义检索召回（embedding）
  - 多候选路径打分（成功率/耗时/历史评分）
  - 工具沙箱执行隔离（iframe/Web Worker/权限策略）
- 若运行环境不支持子代理团队，需降级为主流程自审并在 `progress.md` 记录原因

## References
- https://www.typescriptlang.org/tsconfig#types
- https://www.typescriptlang.org/tsconfig#moduleResolution
- https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
