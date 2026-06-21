---
name: dist-runtime-stale-server-debugging
description: |
  Debug cases where TypeScript/source tests pass but the live local server still behaves like old code. Use when: (1) unit tests cover a new route or behavior and pass, (2) real requests to a running service still return old results like 404, (3) the project runs via compiled output such as `node dist/server.js` or `start:ts`, and (4) a long-running local process may still be serving stale dist artifacts. Covers stale dist output, missing rebuilds, and missing process restarts.
author: Claude Code
version: 1.0.0
date: 2026-03-10
---

# Dist Runtime Stale Server Debugging

## Problem
在 TypeScript 或源码层的测试已经通过后，真实运行中的本地服务仍然表现得像旧版本代码。这类问题通常不是“测试错了”，而是运行中的服务没有加载最新的 `dist` 编译产物。

## Context / Trigger Conditions
在以下场景使用：

- 单测已覆盖新路由/新行为，并且全部通过
- 实际请求运行中的服务时，仍然得到旧结果，例如 404、旧响应结构、旧逻辑
- 项目通过以下方式运行：
  - `start:ts`
  - `node dist/server.js`
  - 任何先编译再运行 `dist/**` 的模式
- 本地服务是长跑进程，可能在你改完源码后没有重启

典型症状：
- 测试里 `POST /api/foo` 通过，真实服务里还是 404
- 源码文件已改，但 `dist/**` 对应文件内容还是旧的
- `curl` 命中 live 服务时结果与测试完全不一致

## Solution
1. **先确认测试通过的是源码层而不是 live 进程**
   - 单测通过并不代表运行中的服务已经加载了新代码。
   - 明确区分：
     - 测试导入的源码/ts 文件
     - 真实运行进程加载的 `dist/**`

2. **直接对 live 服务做最小复现请求**
   - 用 `curl` 或等价方式请求正在运行的服务。
   - 同时验证一个旧路由和新路由，确认问题稳定复现。

3. **检查 `dist/**` 中对应编译产物是否包含新逻辑**
   - 定位运行中的入口文件实际会加载哪个 `dist` 文件。
   - 直接查看 `dist` 下对应模块内容，确认是否已经包含新路由/新行为。

4. **检查运行命令的真实加载路径**
   - 看 `package.json` scripts。
   - 看 `start:ts` / `server.js` / 包装脚本是否最终跑的是 `dist/server.js`。
   - 如果是，就必须验证 `dist` 已更新且进程已重启。

5. **如果 `dist` 是新的，但 live 服务还是旧行为，优先怀疑进程未重启**
   - 长跑进程通常不会自动热加载新的 `dist` 文件。
   - 这时不要继续改业务代码，先重启服务进程。

6. **最小修复顺序**
   - 先执行后端构建，例如：
     ```bash
     pnpm build:backend
     ```
   - 再停止旧进程
   - 再重新启动服务

## Verification
满足以下条件即可确认问题已解决：

1. 单测仍然通过
2. `dist/**` 对应文件包含新逻辑
3. 重启后的 live 服务对新接口返回正确状态码/响应
4. 旧的错误现象（例如 404）消失

## Example
项目运行方式：
```bash
PORT=8890 pnpm start:ts
```
该命令最终执行：
```bash
pnpm build:backend && node dist/server.js
```

现象：
- `test/unit/symphonyRoutes.test.ts` 已覆盖 `POST /api/symphony/refresh` 并通过
- 但：
  ```bash
  curl -X POST http://127.0.0.1:8890/api/symphony/refresh
  ```
  返回 `404`

排查：
- 查看 `dist/server/routes/symphony.js`，发现最初没有 `app.post('/api/symphony/refresh', ...)`
- 重新 `build:backend` 后，`dist/server/routes/symphony.js` 已包含新路由
- 但运行中的 8890 服务仍未重启，所以继续返回旧结果

修复：
```bash
pnpm build:backend
# stop old process
PORT=8890 pnpm start:ts
```

再次验证：
```bash
curl -X POST http://127.0.0.1:8890/api/symphony/refresh
```
返回 `202`

## Notes
- 这类问题和“源码错了”很像，但根因其实在**运行时产物与进程生命周期**。
- 如果项目还有前端 `public/` 静态产物，同样可能出现“源码新、运行态旧”的错位；但这里关注的是 **backend dist + long-running process**。
- 当 live 行为和单测冲突时，优先检查：
  1. 测试覆盖的是哪一层
  2. live 进程加载的是哪个文件
  3. `dist` 是否更新
  4. 进程是否已重启

## References
- https://www.typescriptlang.org/docs/handbook/compiler-options.html
