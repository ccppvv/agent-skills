---
name: fe-verify
description: |
  前端三层自动验证体系：需求→结构化规格→行为合约测试→视觉快照断言。
  解决 AI 生成页面与需求不一致的核心痛点——用机器可读的规格驱动测试，而非人眼抽查。
  触发词：「验证页面」「AI写的页面不对」「需求不一致」「自动验证」「规格驱动测试」「行为合约」「视觉回归」「spec as contract」。
  当用户提到前端页面需要验证、AI生成结果需要校验、需求对齐、测试自动化时均应激活，即使用户没有明确说"三层验证"。
---

# FE Verify · 前端三层自动验证

> 你痛的不是 AI 写错代码，而是没有一个"需求→实现"的自动校验漏斗。

## 核心理念

Kent C. Dodds 的 Testing Library 哲学：**测试用户看到和做的，而不是实现细节。**

AI 今天用 CSS Grid 明天换 Flexbox——无所谓。关键是"用户能不能登录"这个行为没有变。
规格合约测的是行为，不是代码——这才是对 AI 输出最鲁棒的校验。

## 三层架构

从便宜到贵，逐步加码。每层独立可用，组合后形成完整闭环。

| 层 | 名称 | 成本 | 覆盖 | 输出 |
|----|------|------|------|------|
| L1 | 规格即合约 | 极低 | 80% 需求偏差 | `.spec.yml` |
| L2 | 行为合约测试 | 中 | 功能正确性 | `.test.ts` |
| L3 | 视觉快照断言 | 高 | 视觉还原度 | screenshot + CSS 断言 |

---

## 执行协议

### Phase 1: 需求 → 结构化规格（L1）

收到需求文档（PRD、设计稿标注、口头描述均可），输出行为规格 + 视觉规则。

**规格文件格式：**

```yaml
# specs/<component>.spec.yml
component: ComponentName
source: "需求来源（PRD链接/设计稿/口头）"

behaviors:
  - id: B001
    given: "前置条件"
    when: "用户动作"
    then: "期望结果"
    priority: P0 | P1 | P2

  - id: B002
    given: "未登录状态"
    when: "点击登录按钮"
    then: "显示错误提示'请输入手机号'"
    priority: P0

visual_rules:
  - target: "元素选择器描述"
    property: CSS属性
    expected: 期望值
    tolerance: 容差范围（可选）

  - target: "登录按钮"
    property: width
    expected: 100%
  - target: "错误提示"
    property: color
    expected: "#ff4d4f"

states:
  - name: default
    description: "默认状态"
    screenshot: true
  - name: error
    trigger: "触发错误态的动作"
    screenshot: true
  - name: loading
    trigger: "触发加载态"
    screenshot: false  # 非关键状态可跳过快照
```

**规格编写原则：**
- 行为用"用户语言"描述，不涉及实现（不说"div显示class"，说"错误提示可见"）
- 每个 behavior 可独立验证，不依赖其他 behavior 的副作用
- priority 区分：P0 = 核心路径，P1 = 重要分支，P2 = 边缘场景
- visual_rules 只写"设计稿明确约定的"视觉规则，不写通用样式

### Phase 2: 规格 → 行为合约测试（L2）

从 `.spec.yml` 自动生成 Testing Library 测试骨架。

**测试文件格式：**

```typescript
// __tests__/<component>.spec.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
// 从规格文件导入行为定义（或人工维护同步）

describe('ComponentName — 需求合约验证', () => {
  // B001: given → when → then
  test('B001: 未登录 → 点击登录 → 显示错误提示', async () => {
    // given
    render(<ComponentName />)

    // when — 优先用 userEvent（模拟真实用户）
    await userEvent.click(screen.getByRole('button', { name: /登录/ }))

    // then — 测用户可见的结果，不测实现
    expect(screen.getByText(/请输入手机号/)).toBeVisible()
  })

  // ... 更多 behavior
})
```

**测试编写原则：**
- 选择器优先级：`getByRole` > `getByLabelText` > `getByText` > `getByTestId`
  - 为什么：Role 和 Label 在重构时最稳定，TestId 是最后手段
- 异步断言用 `waitFor`，不靠 `setTimeout`
- 每个测试对应一个 behavior ID，溯源到规格
- AI 生成测试后，人审的重点：选择器鲁棒性 + 异步顺序

### Phase 3: 关键状态 → 视觉快照断言（L3）

只对规格中 `screenshot: true` 的状态做快照，不是全页盲比。

**快照测试格式：**

```typescript
// __tests__/<component>.visual.test.ts
import { test, expect } from '@playwright/test'

test.describe('ComponentName — 视觉规格验证', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/path-to-component')
  })

  test('default 态 — 视觉规则 + 快照', async ({ page }) => {
    // CSS 属性断言（从 visual_rules 生成）
    await expect(page.locator('button[type=submit]'))
      .toHaveCSS('width', '100%')

    // 视觉快照
    await expect(page).toHaveScreenshot('component--default.png')
  })

  test('error 态 — 视觉规则 + 快照', async ({ page }) => {
    // 触发状态
    await page.click('button[type=submit]')

    // CSS 属性断言
    await expect(page.locator('.error-msg'))
      .toHaveCSS('color', 'rgb(255, 77, 79)')

    // 视觉快照
    await expect(page).toHaveScreenshot('component--error.png')
  })
})
```

**快照原则：**
- 首次运行生成基线 → 人肉眼确认一次 → 锁定
- 后续 AI 改动自动对比，偏差超阈值即报错
- 只截图关键状态，不截图所有状态

---

## 工程化闭环

```
需求文档 (PRD/设计稿/口头)
     ↓ [L1] AI 生成规格
结构化规格 (.spec.yml)
     ↓ [L2] AI 生成测试骨架
行为合约测试 (.test.ts)     ← 人工审选择器(20%工作量)
     ↓ CI 跑通
     ↓ [L3] 关键状态快照
视觉快照断言 (.visual.test.ts) ← 人工确认基线(一次性)
     ↓
AI 生成/修改代码 → CI 自动跑三层验证 →
  ✅ 通过 → 交付
  ❌ 不通过 → diff 报告 → 自动打回
```

---

## 快速启动

当用户没有现成需求文档时，用以下 prompt 模板引导：

```
请根据以下需求，生成 YAML 格式的行为规格和视觉规则：
- 组件名：{用户提供的组件名}
- 需求描述：{用户的需求描述}
- 输出格式：behaviors (given/when/then + priority) + visual_rules + states
```

生成规格后，立即追问：
1. "规格中的 behavior 是否覆盖了你的核心路径？" → 确认 P0
2. "visual_rules 是否遗漏了设计稿的关键约束？" → 补视觉规则
3. "states 中哪些需要截图？" → 确认 L3 范围

---

## 技术栈适配

| 框架 | L2 测试库 | L3 快照库 |
|------|----------|----------|
| React | @testing-library/react + vitest/jest | Playwright |
| Vue | @testing-library/vue + vitest | Playwright |
| Svelte | @testing-library/svelte + vitest | Playwright |
| Vanilla | Playwright (纯 DOM) | Playwright |

检测项目 `package.json` 中的依赖自动选择，不硬编码。

---

## 反模式

- 不测实现细节（不检查 class 名、组件 state、内部 DOM 结构）
- 不对非关键状态做快照（浪费 CI 资源且产生噪音）
- 不跳过 L1 直接写测试——没有规格的测试是"测了什么不知道"
- 不把 L3 当 L2 用——快照断言不能替代行为断言
- 不让人工审全部测试——只审选择器和异步，其余自动

## 诚实边界

- L1 规格只能捕获"已表达的"需求，隐含需求需人工补充
- L2 测试覆盖行为但不覆盖性能、可访问性（需额外工具）
- L3 基线图片必须人肉眼确认一次，这步无法自动化
- 三层体系不替代设计评审——它验证的是"实现是否匹配规格"，不是"规格是否正确"
