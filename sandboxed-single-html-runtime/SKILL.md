---
name: sandboxed-single-html-runtime
description: |
  为单 HTML 工具页增加受限执行容器。用于：
  (1) 已有真实 `window.process` 执行链，但需要降低主页面暴露面；
  (2) 希望在不拆分部署的前提下实现 P0-04；
  (3) 需要在单文件 HTML 中同时保留内联脚本与执行隔离。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Sandboxed Single HTML Runtime

## Problem
单 HTML 工具页即使已经具备真实执行能力，如果工具逻辑直接运行在主页面上下文中，仍会扩大 XSS/脚本执行面的影响范围。完全拆成多文件又会破坏“单文件分发”的目标。

## Context / Trigger Conditions
- 页面已经有真实 `window.process` 执行链
- 需要为 P0-04 增加执行隔离
- 工具仍需在单 HTML 内交付
- 典型症状：
  - 工具脚本直接嵌在主页面中执行
  - 已有 CSP，但执行逻辑仍与 UI 同上下文
  - 希望收紧权限但不想引入完整后端沙箱系统

## Solution
1. **把真实执行迁移到 `iframe sandbox="allow-scripts"`**
   - 主页面只保留输入、结果展示、下载、评分 UI
   - 工具运行时和 `window.process` 放入沙箱 iframe 内
   - 主页面与工具逻辑分离，减少主文档暴露面

2. **采用双层 CSP**
   - 主页面：保留必要的 `script-src 'unsafe-inline'` / `connect-src 'self'` 等以兼容现有内联逻辑
   - 沙箱页面：使用更严格的策略，如：
     - `default-src 'none'`
     - `script-src 'unsafe-inline'`
     - `connect-src 'none'`
     - `object-src 'none'`
     - `frame-ancestors 'none'`
   - 这样可以在不推翻当前实现的前提下先形成最小安全闭环

3. **通过 `postMessage` 做主页面与沙箱通信**
   - 主页面发送：步骤、输入、requestId
   - 沙箱返回：执行结果 / 错误、summary、Blob
   - 主页面负责渲染结果、创建下载 URL

4. **`srcdoc` 注入时使用双重转义**
   - 先对整个沙箱 HTML 做属性级转义（用于塞进 `iframe srcdoc="..."`）
   - 在沙箱内部对脚本内容继续做脚本级转义（如 `</script>`）
   - 否则很容易因为 HTML 属性上下文或脚本上下文而破坏产物

5. **无浏览器场景做结构性验收**
   - 生成后直接读产物 HTML
   - 检查是否存在：
     - `iframe sandbox="allow-scripts"`
     - 顶层 CSP
     - `srcdoc` 内的沙箱 CSP
     - `postMessage` handler
   - 这是无法启动浏览器时的有效验收手段

## Verification
- 生成后的 HTML 含 `iframe sandbox="allow-scripts"`
- 主页面存在顶层 CSP
- `srcdoc` 内存在 `default-src 'none'` 的沙箱 CSP
- 主页面中存在 `postMessage` 发送与接收逻辑
- 类型检查通过，页面可成功生成

## Example
- 主页面点击“执行工具链”
- 主页面将 `{ steps, input, requestId }` 发给沙箱
- 沙箱执行真实 `window.process`
- 沙箱通过 `postMessage` 返回 `{ summary, blob }`
- 主页面显示 preview 并提供下载

## Notes
- 这是“单文件 + 最小隔离”的折中方案，不等于完整浏览器级安全隔离
- 若后续上生产，仍建议继续补：
  - 更严格的 origin 校验
  - 浏览器内真实交互验证 / E2E
  - 进一步限制能力（如 Worker/权限策略）

## References
- https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox
- https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
- https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#attr-srcdoc
- https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
