---
name: lifecycle-disable-and-requestid-logging
description: |
  为临时页面平台补齐最小生命周期执行与可观测性。用于：
  (1) retention 已能产生日志但 destroy 还未真正生效；
  (2) 本地 HTTP 服务缺少统一 requestId；
  (3) 需要低成本把 P0-03 与 P0-05 推进一步。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Lifecycle Disable and RequestId Logging

## Problem
很多 MVP 平台已经能“判定”保留/销毁动作，但并没有真正执行；同时日志虽然存在，却无法把一次请求从入口追到结果，导致生命周期和可观测性都停留在半成品状态。

## Context / Trigger Conditions
- 已有 retention 决策（keep / destroy / ttl_expire）
- `destroy` 只是记录在文件里，还没有影响访问行为
- 本地 HTTP 服务已有接口，但缺乏统一 requestId
- 需要快速逼近关闭 P0-03 / P0-05

## Solution
1. **先用 disabled-pages 清单执行 destroy**
   - 新增 `disabled-pages.json`
   - 当 retention 动作为 `destroy` 时，把 `pageId` 写入 disabled 清单
   - 页面访问前先检查该清单，命中则返回 `410 Gone`
   - 这是不引入调度器时最小、最稳妥的执行化方案

2. **为每个请求生成或继承 requestId**
   - 优先读取请求头 `X-Request-Id`
   - 没有时服务端自动生成一个 requestId
   - 把 requestId 带入：
     - 成功响应
     - 失败响应
     - 结构化日志

3. **统一结构化日志字段**
   - 推荐字段：
     - `event`
     - `requestId`
     - `pageId`
     - `userId`
     - `code`
     - `ts`
   - 用同一格式覆盖：
     - page served
     - page blocked
     - view rejected
     - rating saved
     - rating rejected
     - internal error

4. **先做轻量本地回归**
   - 步骤：
     1) 生成一个 `destroy` 页面
     2) 启动本地服务
     3) 访问该页面，验证返回 `410`
     4) 带显式 `X-Request-Id` 调用接口
     5) 验证响应与日志中都出现同一个 requestId

## Verification
- `destroy` 页面访问返回 `410`
- 服务端日志出现 `page_blocked`
- 带 `X-Request-Id` 的请求在响应体中可见同值
- 日志中 `requestId` 与响应中的 requestId 一致

## Example
- 评分为 2，retention 判定为 `destroy`
- `disabled-pages.json` 写入该页面
- 再访问 `/view/<pageId>` 返回 `410 Gone`
- 使用 `X-Request-Id: manual-req-001` 请求评分接口
- 返回：`{"action":"keep","requestId":"manual-req-001"}`

## Notes
- 这是最小执行化方案，不等同于完整生命周期调度系统
- 后续仍应补：
  - TTL 到期回收任务
  - keep 白名单 / 保留池
  - 前端执行链 requestId 贯穿

## References
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/410
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Request-ID
