---
name: signed-temp-page-access-control
description: |
  为临时 HTML 页面快速补齐“单用户可用”最小鉴权闭环。用于：
  (1) 页面是静态产物但需要限制只给某个用户访问；
  (2) 希望用低成本方案先满足 P0-02；
  (3) 需要同时保护页面访问与评分提交接口，避免前后端鉴权漂移。
author: Claude Code
version: 1.0.0
date: 2026-03-01
---

# Signed Temp Page Access Control

## Problem
临时生成的 HTML 页面往往是静态文件，天然缺少用户隔离能力。如果直接暴露文件路径，任何拿到链接的人都可访问或提交评分，无法满足“仅当前用户可用”的最低要求。

## Context / Trigger Conditions
- 需要给单个用户分发临时 HTML 页面
- 暂时没有完整登录系统或会话体系
- 需要低成本补齐 P0-02（单用户访问控制）
- 同时存在页面访问与评分提交两个入口

## Solution
1. **采用 HMAC 签名链接作为最小闭环**
   - claims 至少包含：`pageId`、`userId`、`exp`
   - 使用共享 secret 计算 `sig`
   - 链接形态：`/view/<pageId>?uid=<user>&exp=<unix>&sig=<hmac>`

2. **访问与评分共用同一 claims 校验函数**
   - 页面访问（GET `/view/...`）和评分提交（POST `/api/ratings`）都走同一套：
     - 完整性检查
     - 过期检查
     - HMAC 校验
   - 避免前后端各写一套逻辑导致规则漂移

3. **对 pageId 做白名单校验**
   - 限制为：仅允许字母数字、`.`、`_`、`-`
   - 且必须以 `.html` 结尾
   - 校验通过后才能参与文件路径拼接

4. **本地验证覆盖四类场景**
   - 正确签名：应返回 `200`
   - 篡改 `uid`：应返回 `403`
   - 篡改 `sig`：应返回 `403`
   - 过期 `exp`：应返回 `403`

5. **验证结束必须停掉后台服务**
   - 如果用本地 HTTP 服务做验证，完成后显式停止
   - 避免残留进程影响后续测试与端口占用

## Verification
- 正确签名用户可访问页面并成功提交评分
- 非法用户 / 非法签名 / 过期链接均被拒绝
- 页面访问与评分接口表现一致
- 本地服务在验证后已停止

## Example
1. 生成签名链接：
   - `uid=alice`
   - `exp=未来1小时`
   - `sig=HMAC(pageId|uid|exp)`
2. `alice` 使用原链接访问：`200`
3. 把 `uid` 改成 `bob`：`403`
4. 用原签名提交 `uid=bob` 的评分：`403`

## Notes
- 这是“最小闭环”，适合先补 P0-02，不等于完整鉴权系统
- 上线后仍建议升级为真正的用户身份体系、服务端会话或一次性令牌
- 如果页面进一步支持真实工具执行，还需配合沙箱/CSP

## References
- https://owasp.org/www-community/attacks/Path_Traversal
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
