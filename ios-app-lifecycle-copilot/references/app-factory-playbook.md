# iOS 多 App 批量生产 Playbook（2026-02-20）

## 1. 结论（推荐顺序）

1. `原生工厂线`（SwiftUI + 模块化 + XcodeGen/Tuist + fastlane）
2. `跨端工厂线`（Expo/React Native + EAS Workflows + Monorepo）
3. `混合双轨线`（核心付费产品原生，增长型产品跨端）

默认推荐 1 -> 3：
- 原生线更稳、订阅链路更可控、审核风险更低。
- 当 Android 同步需求变强时，再切到混合双轨。

## 2. 三条路线对比

| 维度 | 原生工厂线 | 跨端工厂线 | 混合双轨线 |
|---|---|---|---|
| iOS 稳定性 | 高 | 中高 | 高 |
| 多端速度 | 中 | 高 | 高 |
| 订阅排障效率 | 高 | 中 | 高 |
| 团队门槛 | 中 | 中（JS+原生） | 中高 |
| 长期上限 | 高 | 中高 | 最高 |

## 3. 工厂化核心设计

### 3.1 模板层（生成速度）
- 用 `manifest` 驱动新 App 生成：`appName`、`bundleId`、`teamId`、`paywallSku`、`theme`、`apiEnv`。
- 工程生成器统一到一条命令：`scripts/new-app --manifest apps/<app>/manifest.yml`。
- 项目模板仅保留必要参数，避免早期复杂主题系统（YAGNI）。

### 3.2 复用层（维护效率）
- 抽 3 个稳定包：
  - `core`：配置、网络、存储、日志、鉴权
  - `billing`：StoreKit 2、交易同步、权益状态机
  - `analytics`：埋点协议、事件定义、漏斗上报
- 业务差异只放 `apps/<app>/`。

### 3.3 自动化层（发布吞吐）
- 统一发布模板：`dev -> beta(TestFlight) -> prod(App Store)`。
- fastlane 统一签名与上传，优先 `App Store Connect API Key` 鉴权。
- 把 App 级差异（bundle id、metadata、截图路径）参数化，避免每个 App 写一套 lane。

### 3.4 运营层（增长闭环）
- 统一远程配置（功能开关、Paywall 文案、价格实验入口）。
- 统一指标看板：安装 -> 激活 -> 试用 -> 首付 -> 续费 -> 退款。
- 所有实验必须可回滚（KISS + 风险控制）。

## 4. 2026 仍有效的关键实践（截至 2026-02-20）

- Xcode Cloud 仍可用，Apple Developer Program 包含每月 25 compute hours，超额可订阅更高档位。
- TestFlight 仍是主流灰度渠道，外部测试上限可到 10,000。
- App Store Connect API 可自动化订阅、IAP、元数据等流程。
- React Native 在 0.82 版本已进入 New Architecture Only；若走 RN 工厂线，需按新架构治理依赖。
- Expo EAS Workflows 支持把 iOS/Android 构建并行化，并可用 GitHub 事件触发。
- App Store Connect Webhooks 可订阅构建上传状态等事件，适合做事件驱动发布编排。

## 5. 30 天落地节奏

### 第 1 周
- 固化目录：`apps/ + packages/ + scripts/ + ci/`。
- 定义 manifest schema 和第一个生成命令。

### 第 2 周
- 抽离 `billing` 与 `analytics` 到共享包。
- 打通一条完整 CI（构建 + 测试 + TestFlight 上传）。

### 第 3 周
- 接远程配置与订阅漏斗看板。
- 完成一个“同代码不同品牌壳”的复制发布。

### 第 4 周
- 复盘耗时与故障点。
- 把剩余人工步骤脚本化，产出 v2 工厂模板。

## 6. KISS / YAGNI / SOLID / DRY 检查清单

- KISS：先做“一个模板 + 一条发布流水线 + 一个计费闭环”。
- YAGNI：没有真实多品牌需求前，不做复杂多主题运行时系统。
- SOLID：计费、埋点、业务分层，禁止 UI 直接依赖计费存储细节。
- DRY：签名、上传、测试、埋点协议都走共享脚本与包。

## 7. 参考链接

- Apple Xcode Cloud（Get Started）：https://developer.apple.com/xcode-cloud/get-started/
- App Store Connect API 概览：https://developer.apple.com/app-store-connect/api/
- App Store Connect API（Help）：https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-api/
- App Store Connect Manage Webhooks：https://developer.apple.com/help/app-store-connect/manage-your-team/manage-webhooks/
- TestFlight 概览：https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview
- StoreKit Sandbox 测试：https://developer.apple.com/documentation/StoreKit/testing-in-app-purchases-with-sandbox
- App Store Server Notifications URL 配置：https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/enter-server-urls-for-app-store-server-notifications/
- Tuist Selective Testing：https://docs.tuist.dev/en/guides/features/selective-testing
- Tuist Cache：https://docs.tuist.dev/en/guides/features/cache
- XcodeGen Project Spec：https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html
- fastlane App Store Connect API：https://docs.fastlane.tools/app-store-connect-api/
- fastlane match：https://docs.fastlane.tools/actions/match/
- fastlane pilot：https://docs.fastlane.tools/actions/pilot/
- Expo EAS Workflows：https://docs.expo.dev/eas-workflows/get-started/
- Expo Monorepo：https://docs.expo.dev/guides/monorepos/
- Expo EAS Monorepo Build：https://docs.expo.dev/build-reference/build-with-monorepos/
- React Native 0.82（New Architecture Only）：https://reactnative.dev/blog/2025/10/08/react-native-0.82
- Flutter iOS Flavors：https://docs.flutter.dev/deployment/flavors-ios
- Firebase Remote Config：https://firebase.google.com/docs/remote-config
