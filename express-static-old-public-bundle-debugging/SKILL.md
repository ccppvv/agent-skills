---
name: express-static-old-public-bundle-debugging
description: |
  Debug mismatches where an Express-served web UI shows stale data or old behavior while API endpoints already reflect new code. Use when: (1) package scripts like `start:ts` only rebuild backend output, (2) Express serves frontend assets via `express.static(publicDir)`, (3) browser UI stays old but direct `/api/*` calls are correct, or (4) `public/index.html` still references old hashed bundles. Covers backend-dist + static-public split deployments.
author: Claude Code
version: 1.0.0
date: 2026-03-10
---

# Express Static Old Public Bundle Debugging

## Problem
在“后端编译产物”和“前端静态产物”分离的项目里，很容易出现一种错位现象：API 已经是新代码，但浏览器页面仍然加载旧的前端 bundle，导致 UI 展示与接口返回不一致。

## Context / Trigger Conditions
在以下场景使用：

- 直接请求 API（例如 `/api/symphony/state`）返回正确的新数据
- 浏览器页面仍显示旧状态、旧字段或旧文案
- 启动命令类似 `pnpm start:ts` / `node dist/server.js`，只编译后端
- Express 通过 `express.static(publicDir)` 提供页面
- 前端构建输出落在 `public/` 这类目录里
- `public/index.html` 仍引用旧 hash 的 JS/CSS 文件

典型症状：
- “API 对了，UI 还没变”
- “手动 curl 正常，但页面显示旧值”
- “SSR/服务端日志看起来没问题，浏览器仍不对”

## Solution
1. **确认 API 侧是否真的已正确**
   - 先用 `curl` 或等价方式验证目标接口返回是否符合预期。
   - 不要先改代码；先确定问题发生在 API 层还是静态前端层。

2. **检查启动脚本是否会重建前端**
   - 查看 `package.json` 的 scripts。
   - 重点看当前使用的启动命令是否只执行后端构建（例如只跑 `build:backend`）。
   - 如果 `start:ts` 不包含前端构建，那么页面很可能还是旧的 `public/` 产物。

3. **检查 Express 的静态资源提供方式**
   - 查看类似 `backend/server.ts`、`backend/server/app.js` 的入口。
   - 如果存在 `createApp({ publicDir: PUBLIC_DIR })` 和 `express.static(publicDir)`，说明浏览器拿到的是磁盘上的静态产物，而不是运行时即时构建的前端代码。

4. **检查 `public/index.html` 或等价入口是否陈旧**
   - 查看其中引用的 JS/CSS hash。
   - 如果这些 hash 对应的是旧 bundle，而你刚改了 `frontend/src/**` 代码但没重新 `build`，根因基本就成立了。

5. **只做最小修复：重建前端静态资源**
   - 运行前端构建命令（例如 `pnpm build`）。
   - 不要先改业务代码；先验证是否只是产物陈旧。

6. **重载页面并再次比对 UI 与 API**
   - reload 浏览器页面
   - 再次检查页面文本/截图
   - 确认 UI 是否已与 API 返回对齐

## Verification
满足以下条件即可确认问题已解决：

1. 目标 API 返回正确数据
2. 重建前端后，浏览器页面的显示值与 API 一致
3. `public/index.html` 已引用新生成的 bundle hash（如果构建工具使用 content hash）
4. 不需要额外修改业务代码即可恢复一致性

## Example
项目结构：
- `pnpm start:ts` → `pnpm build:backend && node dist/server.js`
- Express 从 `public/` 提供页面
- 前端代码刚改了 `frontend/src/App.tsx`

现象：
- `curl http://127.0.0.1:8890/api/symphony/state` 返回 `{"counts":{"running":1,"retrying":0}}`
- 浏览器里仍显示 `Running 0`

排查结果：
- `start:ts` 不会执行 `pnpm build`
- `public/index.html` 仍引用旧的 bundle

最小修复：
```bash
pnpm build
```
然后 reload 页面，UI 变成：
- `Running 1 Retrying 0`

说明根因不是业务逻辑错误，而是前端静态产物过期。

## Notes
- 这类问题特别容易在“前端构建输出到 `public/`，后端单独启动 `dist/server.js`”的项目里发生。
- 如果你已经验证 API 正确，就不要急着改 React state、`useEffect`、缓存逻辑；先排除静态产物陈旧。
- 对这类项目，手动验证前最好明确区分：
  - **backend rebuild**
  - **frontend rebuild**
  - **browser reload**
- 如果项目长期容易踩这个坑，可以后续再考虑改进脚本，但排障时先用最小修复验证根因。

## References
- https://expressjs.com/en/starter/static-files.html
