---
name: ui-master
description: 面向 workstation-ccc-mui 的视觉还原技能，覆盖 packages/apps/manage 与 packages/apps/agent-flow。用于“按设计稿还原UI”“截图视觉还原”“Ardot/Figma 节点对齐”“修复样式不一致”“统一颜色/字体/间距/边框/圆角/状态样式”“抽取与同步 design tokens”等场景。命中 manage 时优先 styled-components/JSS 的最小改动；命中 agent-flow 时优先 DESIGN-TOKENS.md 与 src/design-tokens.less 双向同步，结合截图 diff 与 Ardot MCP 数据闭环验证。
---

# UI Master

## 概览

在 `manage`（React）与 `agent-flow`（Vue3）中执行高一致性的视觉还原，强调最小改动、可验证、可回滚。

## 路由

1. 判断目标目录。
- `packages/apps/manage/**`：执行 manage 流程。
- `packages/apps/agent-flow/**`：执行 agent-flow 流程。
- 跨包任务：先对齐 token 源头，再处理消费侧。

2. 读取 `references/routing.md`。

## 强制门禁（截图任务必做）

当用户输入页面截图后，必须先执行“组件化布局拆解”，并在拆解前完成组件库存检索。

### 门禁 0：设计源与截图口径锚定

1. 若任务涉及 Ardot/Figma/设计稿，优先请用户提供**具体页面或元素链接**（最好带 `node_id`）。不要只依赖总文件链接猜页面；用户无法补充时，按可见标题/截图推断并标注不确定性。
2. 可用 Ardot MCP 时，先读取目标节点尺寸与样式：`x/y/width/height/fills/strokes/cornerRadius/fontSize/lineHeight/padding/gap/content`。
3. 导出或截图目标节点，固定保存路径；实现截图必须使用同一 viewport、device scale、路由参数与 crop。
4. 若截图是白屏、错误页、Vite overlay、`ERR_CONNECTION_REFUSED` 或字节/哈希异常一致，整轮验证作废。

### 门禁 A：组件库存检索（先于拆解）

1. 在目标应用源码下检查 `src/components/common-components/`：
- 先查是否有可直接复用组件。
- 若无可复用组件，评估是否应新增通用组件。

2. 对候选组件做决策（复用 / 扩展 / 新增）：
- **复用**：结构与交互高度一致，改动仅为 token 或少量 props。
- **扩展**：核心结构可复用，但需要新增可选能力（props/slot/variant）。
- **新增**：现有组件无法承载且预计可在 2+ 页面复用。

3. 禁止绕过该步骤：
- 未完成 common-components 检索与决策，不得进入截图拆解表。

### 门禁 B：组件化截图拆解与用户确认

1. 完成组件化拆解（禁止直接改代码）：
- 页面级容器
- 区块容器（卡片/面板/弹窗）
- 表单组件（输入框/下拉/单选/开关）
- 信息组件（标题/说明/标签/提示）
- 操作组件（按钮/链接/图标按钮）

2. 输出组件清单并回传用户确认：
- 使用 `references/screenshot-decomposition.md` 模板。
- 必须包含：组件名、层级、布局关系、候选复用组件、决策（复用/扩展/新增）、预期 token。

3. 等待用户明确确认后才能继续：
- 仅当用户确认“拆解正确”后，才可进入 DESIGN tokens 应用与视觉还原。
- 用户未确认前，不得进入样式修改。

## 标准流程

1. 锁定目标页面/节点与验收截图；有 Ardot/Figma MCP 时先读节点数值，无 MCP 时用目标截图量测。
2. 先检索 `src/components/common-components/` 并完成复用决策。
3. 用 `references/screenshot-decomposition.md` 完成组件化拆解并回传确认。
4. 用户确认拆解后，用 `references/visual-checklist.md` 拆视觉差异。
5. 按包读取规则文件并实施最小改动；单轮只改一类视觉变量，方便截图验证和回退。
6. 采集实现截图并计算同 crop diff：至少记录 `MAE`、`changed>8%`、`changed>24%` 和 diff 热区图。
7. 指标或截图变差时回退该轮；指标下降但肉眼结构更差时也回退，避免为数字过拟合。
8. 执行 `scripts/check-hardcoded-colors.sh` 清硬编码风险。
9. 执行 `references/command-recipes.md` 中最小必要验证。
10. 输出改动、截图目录、diff 指标、保留/回退决策、风险与回滚点。

## 截图像素闭环经验

- **同口径比较**：目标与实现必须统一 viewport、scale、crop、主题和等待时间；大画布优先比较目标组件区域，不用全图噪声判断局部还原。
- **Ardot 数值优先**：容器、头像、标题、按钮、tabs、卡片、输入区等先用 Ardot 节点尺寸/颜色/间距建立对照表，再写 CSS。
- **小步试验**：例如只调整 `composer` 高度、只调整 tooltip 坐标、只调整历史消息 spacer；每次截图后决定保留/回退。
- **无效截图排除**：白屏、错误页、服务未启动、截图字节异常相同、关键 DOM 缺失时，不得宣称视觉进步。
- **状态矩阵留痕**：多页面/多状态任务必须维护 markdown 矩阵，记录页面、状态、Ardot 节点、实现路径、截图路径、diff 指标、是否待验收。

## manage 约束

1. 优先复用已有 `*.style.ts/js` 与 `StyledComponents.tsx`。
2. 优先 `styled-components`，避免新增内联 `style`。
3. 覆盖 `hover/focus/disabled/error` 关键状态。

## agent-flow 约束

1. 设计规范以 `DESIGN-TOKENS.md` 为准。
2. token 变更必须同步 `src/design-tokens.less`。
3. 禁止新增硬编码颜色、边框色、圆角值；若为 Ardot 精确还原必须临时使用设计稿色值，应在报告中标注来源节点与后续 token 化建议。
4. 视觉 harness 可用于状态复现，但真实业务组件仍需最小回归；不要把 harness 截图等同于生产路径完成。

## 快速命令

- `bash scripts/check-hardcoded-colors.sh`
- `bash scripts/verify-visual-restore.sh manage`
- `bash scripts/verify-visual-restore.sh agent-flow`

## 失败处理

1. 设计稿不完整：先完成可见区域并显式标注未覆盖项。
2. token 冲突：优先复用现有 token，新增时说明必要性与影响面。
3. 验证耗时过长：先跑目标包最小验证，再补全完整验证。
