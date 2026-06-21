---
name: inlined-window-process-runtime
description: |
  将单 HTML 工具页中的 mock runtime 平滑替换为真实 `window.process` 执行链。用于：
  (1) 工具遵循 ToolSpec/process 契约；
  (2) 需要在不依赖外部脚本加载的前提下让临时页真实执行；
  (3) 避免生成后的 HTML 中正则和换行被模板转义破坏。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Inlined window.process Runtime

## Problem
单 HTML 生成器早期常用 mock runtime 只展示执行步骤，无法真正调用工具逻辑。把工具逻辑切到真实执行时，最常见的问题是：
1) 外部加载工具脚本过重或不稳定；
2) 运行时代码中的正则、换行、反斜杠在模板字符串里被破坏；
3) 页面层需要分别处理文本、JSON、文件结果，接口分叉明显。

## Context / Trigger Conditions
- 工具契约是 `window.ToolSpec` + `window.process`
- 临时页是单文件 HTML，需要自包含
- 你希望从“假执行”升级为“真执行”
- 典型症状：
  - 页面有执行按钮，但只是返回占位结果
  - 生成后的 HTML 中内联脚本被转义破坏
  - 文本和 JSON 结果展示逻辑重复

## Solution
1. **将每个工具生成为独立 IIFE 脚本块**
   - 每个工具在页面中注册：
     - `window.ToolSpec = ...`
     - `window.process = async (...) => ...`
   - 注册到统一容器：`window.__webArmoryTools[toolId]`
   - 这样可在单 HTML 内保持与真实契约一致

2. **外层运行时模板使用 `String.raw`**
   - 用 `String.raw` 包裹整段运行时代码字符串
   - 避免正则、换行、`\n` 等在生成阶段被二次转义
   - 尤其适合包含正则替换和多行文本处理的工具逻辑

3. **结果统一走 Blob 优先策略**
   - 文本与 JSON 都返回 `Blob`
   - 页面层统一做：
     - summary（type/size）
     - preview（可读文本）
     - download（Blob URL）
   - 这样工具实现更统一，页面逻辑更简单

4. **无浏览器环境先用“生成后读 HTML”验脚本**
   - 重新生成页面后直接 `Read` 产物 HTML
   - 检查是否存在：
     - `window.process = async ...`
     - `window.__webArmoryTools[...] = ...`
     - `window.__webArmoryRunPipeline = ...`
   - 这是无浏览器时验证运行时生成质量的高性价比方法

## Verification
- `pnpm tsc --noEmit` 通过
- 新生成的 HTML 中包含真实 `window.process` 定义，而非 mock 占位逻辑
- 文本/JSON 页面均带结果预览和下载按钮逻辑
- 页面中存在统一的 `window.__webArmoryRunPipeline`

## Example
- 文本清洗工具：在生成后的 HTML 中看到
  - `window.ToolSpec = {...text-clean...}`
  - `window.process = async (input, params = {}) => { ... }`
- 页面点击执行后：
  - 返回 `Blob(text/plain)`
  - 页面显示 preview
  - 用户可下载结果

## Notes
- 这是从 mock runtime 向真实执行过渡的中间态，适合单文件交付
- 后续若切换回真正的 `.tool.html` 源文件加载，可保留这套注册协议不变
- 真正上线前仍建议补浏览器级交互验证（手动或 E2E）

## References
- https://developer.mozilla.org/en-US/docs/Web/API/Blob
- https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#raw_strings
