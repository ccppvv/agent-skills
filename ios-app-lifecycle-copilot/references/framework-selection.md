# 框架选型参考

## 一、推荐顺序（默认）

1. `SwiftUI 原生栈`：仅 iOS，最快达到稳定商用。
2. `React Native + Expo`：需要 iOS/Android 并行、团队以 TS/前端为主。
3. `Flutter`：强调统一渲染一致性，接受 Dart 学习与生态差异。

## 二、选型决策表

| 维度 | SwiftUI 原生 | React Native + Expo | Flutter |
|---|---|---|---|
| 上手成本（iOS） | 低 | 中 | 中 |
| 多端复用 | 低 | 高 | 高 |
| iOS 新特性跟进 | 最快 | 中 | 中 |
| 性能上限 | 高 | 中高 | 高 |
| 订阅接入复杂度 | 低（原生） | 中（桥接/插件） | 中（插件） |
| 多 App 模板化 | 中高 | 高 | 高 |

## 三、KISS / YAGNI / SOLID / DRY 检查

### SwiftUI 原生
- KISS：优势明显，Apple 一等公民能力最完整。
- YAGNI：若短期只做 iOS，不必引入跨端抽象。
- SOLID：用模块化（Feature、Domain、Data）保持职责单一。
- DRY：把通用登录、订阅、埋点抽到共享 Package。

### React Native + Expo
- KISS：中等，需管理 JS + 原生桥接双栈复杂度。
- YAGNI：若短期只发 iOS，跨端收益可能不足。
- SOLID：业务层与平台层隔离，原生能力走统一 Adapter。
- DRY：多端 UI 与业务逻辑复用率高。

### Flutter
- KISS：中等，框架统一但生态选择需要治理。
- YAGNI：若已有强 iOS 团队且无 Android 计划，可能过度设计。
- SOLID：按 feature package 切分，避免单体状态管理膨胀。
- DRY：跨端代码复用高，但需管控插件分叉风险。

## 四、常见误区

- 误区 1：把“多端复用率”当唯一指标，忽略审核与计费链路复杂度。
- 误区 2：先做复杂基建再做业务验证，违背 YAGNI。
- 误区 3：订阅状态只信客户端，不做服务端状态机与幂等。
