# 订阅收费打通手册（iOS）

## 0. 合规前提

- 数字内容与功能解锁应使用 `In-App Purchase`。
- 需完成 App Store Connect 协议、税务、银行账户配置。

## 1. 商品模型设计

1. 定义订阅组（Subscription Group）与档位（月/年）。
2. 设计试用、促销、升级降级路径。
3. 定义权益矩阵（每个产品 ID 对应哪些能力）。

产出：`subscription-products.md`（产品 ID、价格档、权益、生命周期规则）。

## 2. 客户端接入（StoreKit 2）

1. 拉取产品：根据产品 ID 获取商品信息。
2. 发起购买：处理成功、取消、pending。
3. 恢复购买：支持跨设备恢复。
4. 权益读取：基于当前交易状态实时显示权益。

要求：
- 客户端只负责“展示与购买触发”，最终权益以服务端为准。
- 交易处理必须可重入，避免重复发放权益。

## 3. 服务端接入（必须）

1. 用 `App Store Server API` 查询交易与订阅状态。
2. 接收 `App Store Server Notifications` 更新状态。
3. 做事件幂等：按 `originalTransactionId + notificationId` 去重。
4. 维护订阅状态机：active / grace / billing retry / expired / revoked。

建议数据表：
- `subscription_event_log`：原始通知与验签结果。
- `subscription_state`：用户当前权益快照。
- `billing_reconciliation`：对账记录。

## 4. 测试与发布

1. 本地：StoreKit 配置文件做交易流程测试。
2. 联调：Sandbox 账号验证续费与退订路径。
3. 灰度：TestFlight 小流量验证通知、权益同步、漏斗数据。
4. 上线：生产通知地址开启监控告警。

## 5. 运营与对账

- 每日核对：购买成功数、通知到达率、权益发放成功率。
- 每周跟踪：试用转化率、续费率、退款率、到期流失率。
- 异常告警：通知堆积、验签失败率、状态回滚失败。

## 6. KISS / YAGNI / SOLID / DRY 落地点

- KISS：先打通单一订阅组再扩展套餐。
- YAGNI：先不上复杂权益组合，验证转化后再细分。
- SOLID：计费域与业务域隔离，避免耦合 UI 逻辑。
- DRY：统一计费 SDK 与状态机，所有 App 复用同一套服务端能力。
