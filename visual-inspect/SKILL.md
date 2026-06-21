---
name: visual-inspect
description: 从设计稿到代码的智能视觉还原系统。支持图片转代码、UI对比检测、布局分析和完整还原流程；优先结合截图对比、Ardot/Figma MCP 节点数据、DOM 测量与像素 diff 进行闭环还原。自适应框架（React/Vue/原生），像素级精度，响应式适配，设计系统集成，WCAG可访问性标准。触发关键词：视觉还原、设计稿、UI还原、截图对比、像素级还原、Ardot、figma-to-code。
---

# Visual Inspection

智能视觉还原系统 - 将设计稿精确转换为生产级代码。

## 工作流程

### Step 0: Design Tokens 初始化

**技能启动时自动执行，在任何用户请求处理之前。**

1. **检查项目目录** 确定当前工作目录（通常是 `git rev-parse --show-toplevel` 或当前目录）

2. **检测 Design Tokens 文件**
   ```bash
   # 检查项目根目录
   ls DESIGN-TOKENS.md
   ```

3. **加载或创建 Tokens**
   - **存在**: 读取 `DESIGN-TOKENS.md` 到上下文
   - **不存在**: 使用 `assets/DESIGN-TOKENS-template.md` 创建新文件

4. **Token 加载命令**
   ```bash
   # 使用 Read 工具加载
   Read DESIGN-TOKENS.md
   ```

### Step 1: 识别模式

根据用户请求自动选择工作模式：

| 模式 | 触发词 | 处理流程 |
|-----|-------|---------|
| **图片转代码** | "转代码"、"实现这个"、"还原设计稿" | 分析→生成代码→记录新Token |
| **UI对比检测** | "对比"、"检测差异"、"检查实现" | 对比→生成差异报告 |
| **布局分析** | "分析布局"、"结构分析" | 提取结构→生成文档 |
| **完整还原** | "完整还原"、"end-to-end" | 全流程执行→记录新Token |

使用 `AskUserQuestion` 确认模式时需要明确意图。

### Step 2: 提取设计信息

从设计稿/图片中提取关键信息：

```
颜色 → 提取色值（HEX/RGB）并构建调色板
字体 → 识别字体族、字号、行高、字重
间距 → 测量padding、margin、gap
尺寸 → 提取width、height、border-radius
布局 → 识别flex/grid/absolute定位
组件 → 划分组件边界和层级
```

使用 `mcp__chrome-devtools__take_snapshot` 或 `mcp__plugin_superpowers-chrome_chrome__use_browser` 获取页面结构。

### Step 2.5: 设计源锚定（Ardot / Figma / MCP）

当用户给出 Ardot/Figma/设计稿链接或要求“像素级还原”时，先锁定设计源，避免只凭肉眼猜：

1. **优先向用户索取精确元素链接**：请用户提供目标页面、Frame、组件或节点链接（例如带 `node_id` 的 Ardot 链接）。若用户只给总文件链接，先请求“需要还原的具体页面/组件链接”；用户无法补充时，再用截图和可见标题推断，并标注不确定性。
2. **使用 MCP 读取节点数据**：可用 Ardot MCP 时，读取目标节点的 `x/y/width/height/fills/strokes/cornerRadius/fontSize/lineHeight/padding/gap/content`，并记录为尺寸/颜色/间距对照表。
3. **导出目标基准图**：用 MCP 截图/导出目标节点，保存到 `.cache/<task>/ardot-targets/` 或项目约定缓存目录；不要用浏览器错误页、空白页、低分辨率图作为目标。
4. **建立 crop 口径**：对大画布先确定目标区域 crop（例如右侧面板 `x,y,w,h`），后续所有 diff 必须使用同一 crop，避免无关区域污染指标。

### Step 6.5: 截图像素闭环

每轮实现必须形成“截图 → diff → 小改 → 复截图”的闭环：

1. **采集实现截图**：用真实浏览器或项目既有 harness 截图，固定 viewport、device scale、主题、路由参数和等待时间。
2. **验证截图有效性**：检查文件大小、图片方差、页面关键 DOM/文本；发现空白页/白屏、`ERR_CONNECTION_REFUSED`、Vite 错误页或全白图时整轮作废，不得计入进度。
3. **计算指标**：至少输出 `MAE`、`changed>8%`、`changed>24%`，并保存 diff 热区图；指标只在同一 crop/viewport 下横向比较。
4. **只保留有效小改**：单轮只改一类视觉变量（尺寸、间距、颜色、文案密度、状态样式等）。指标或肉眼截图变差时立即回退，避免叠加过拟合。
5. **不得过早宣称完成**：没有目标图、实现截图、有效 diff 指标和人工查看截图四项证据时，只能说“待视觉验证/待验收”，不能说“像素级完成”。

### Step 3: 检测并记录新 Design Tokens

**关键步骤 - 自动识别未记录的 Tokens**

1. **识别可记录的 Tokens**

| 类别 | 识别规则 | Token 命名 |
|-----|---------|-----------|
| 颜色 | 重复出现≥2次 | `color.{用途}-{序号}` |
| 间距 | 是4/8的倍数 | `spacing.{size}` |
| 字号 | 常用值(12/14/16/18/20/24) | `font-size.{name}` |
| 圆角 | 常用值(4/8/12/16) | `radius.{size}` |
| 阴影 | CSS box-shadow | `shadow.{name}` |

2. **对比现有 Tokens**
   ```python
   # 逻辑：提取值 → 查找 DESIGN-TOKENS.md → 不存在则追加
   new_tokens = extract_from_design(design_values)
   existing_tokens = parse_design_tokens_md()

   for token in new_tokens:
       if token not in existing_tokens:
           append_to_design_tokens(token)
   ```

3. **Token 格式规范**
   ```markdown
   ## 颜色 (Colors)
   - `color.primary` = #0066CC - 主按钮色
   - `color.text` = #1A1A1A - 正文文本

   ## 间距 (Spacing)
   - `spacing.sm` = 8px - 小间距
   - `spacing.md` = 16px - 中间距
   ```

4. **自动追加脚本**
   ```bash
   python3 scripts/update_tokens.py --extract --append DESIGN-TOKENS.md
   ```

### Step 4: 检测框架

自动识别项目框架：

```bash
# 检测命令（按优先级）
ls package.json && cat package.json | grep -E "(react|vue|next|nuxt)"
ls src/**/*.{jsx,tsx}  # React
ls src/**/*.{vue}      # Vue
ls *.html              # 原生
```

如无法自动检测，使用 `AskUserQuestion` 询问用户。

### Step 5: 生成代码

根据检测结果选择模板，**使用已记录的 Design Tokens**：

| 框架 | 模板位置 | 输出格式 |
|-----|---------|---------|
| React | `assets/templates/react/` | JSX/TSX + CSS Variables |
| Vue | `assets/templates/vue/` | SFC + CSS Variables |
| 原生 | `assets/templates/native/` | HTML + CSS Variables |

代码生成时优先引用 Tokens：
```css
/* ✅ 使用 Token */
color: var(--color-primary);
padding: var(--spacing-md);

/* ❌ 避免硬编码 */
color: #0066CC;
padding: 16px;
```

### Step 6: 质量验证

使用 TodoWrite 跟踪检查清单：

- [ ] 像素级精度（颜色、间距、字体）
- [ ] 响应式断点（mobile/tablet/desktop）
- [ ] Design Tokens应用（优先使用变量）
- [ ] 新 Tokens 已记录到 DESIGN-TOKENS.md
- [ ] WCAG 2.1 AA级可访问性
- [ ] 语义化HTML
- [ ] ARIA标签（如需要）

## 核心能力

### 1. 图片转代码

输入：设计稿截图/Figma导出
输出：框架适配的组件代码 + 更新的 Design Tokens

流程：
1. 读取 DESIGN-TOKENS.md（自动）
2. 读取设计稿 `Read(path_to_image)`
3. 提取设计属性（颜色/字体/布局）
4. 识别新 Tokens → 追加到 DESIGN-TOKENS.md
5. 选择对应框架模板（使用 Tokens）
6. 生成组件代码

### 2. UI对比检测

输入：设计稿 + 实现截图
输出：差异报告 + 修复建议

流程：
1. 并排分析设计稿和实现
2. 对比关键属性
3. 生成差异清单
4. 提供修复代码

像素级对比补充规则：
- 先确认目标截图与实现截图来自同一尺寸、同一 crop、同一缩放倍率。
- 优先用设计源 MCP 的数值修正布局，再用截图 diff 验证结果。
- 记录每轮截图目录、指标、保留/回退决策，便于长任务跨会话续跑。

### 3. 布局分析

输入：设计稿/页面截图
输出：结构文档（层次树 + 属性表）

流程：
1. 识别组件边界
2. 构建DOM树映射
3. 提取样式属性
4. 输出分析文档

### 4. 完整还原流程

组合上述所有能力，执行：
1. Design Tokens 初始化（自动）
2. 设计稿分析
3. 新 Token 记录（自动）
4. 代码生成（使用 Tokens）
5. 对比验证
6. 迭代优化

## Design Tokens 管理

### Token 文件位置

```
项目根目录/
└── DESIGN-TOKENS.md          # 技能自动维护
```

### Token 更新时机

| 场景 | 动作 |
|-----|------|
| 技能启动 | 自动加载 DESIGN-TOKENS.md |
| 提取新设计 | 自动识别并追加新 Tokens |
| 代码生成 | 优先使用已记录 Tokens |
| 文件不存在 | 自动从模板创建 |

### Token 命名规范

```
{类别}.{用途}.{修饰?}

示例:
color.primary - 主色
color.text-secondary - 次要文本
spacing.md - 中间距
radius.lg - 大圆角
```

## 可访问性标准

遵循 WCAG 2.1 AA 级：

- **颜色对比度** ≥ 4.5:1 (正文) / 3:1 (大文本)
- **焦点指示器** 可见且清晰
- **语义化HTML** 正确使用 `<button>`, `<nav>`, `<main>`
- **ARIA标签** `aria-label`, `role`, `aria-hidden`
- **键盘导航** Tab顺序合理

详见 `references/accessibility.md`

## 响应式策略

标准断点系统：

| 断点 | 宽度 | 用途 |
|-----|------|-----|
| mobile | < 640px | 手机竖屏 |
| tablet | 640px - 1024px | 平板/小笔记本 |
| desktop | > 1024px | 桌面显示器 |

使用 `@media` 或框架响应式工具实现。

## 资源

### scripts/

- `extract_colors.py` - 从图片提取调色板
- `analyze_spacing.py` - 分析间距模式
- `update_tokens.py` - **更新并追加 Design Tokens**

### references/

- `pixel-perfect.md` - 像素级精度指南
- `responsive.md` - 响应式设计模式
- `design-systems.md` - Design Tokens 集成
- `accessibility.md` - WCAG 完整清单
- `frameworks.md` - 框架代码模式

### assets/

- `templates/react/` - React 组件模板
- `templates/vue/` - Vue SFC 模板
- `templates/native/` - 原生 HTML/CSS 模板
- `DESIGN-TOKENS-template.md` - **Design Tokens 模板文件**

## 输出格式

代码输出包含：

```
文件路径: src/components/ComponentName.jsx
├── 组件代码（使用 CSS Variables）
├── Props 接口定义
├── 可访问性属性
└── 使用示例
```

差异报告格式：

```markdown
# UI 对比报告

## 颜色差异
| 属性 | 设计稿 | 实现 | 状态 |
|-----|-------|------|-----|
| 主色 | #0066CC | #0055BB | ⚠️ |

## 新发现的 Design Tokens
- `color.accent` = #FF6B00 (已追加到 DESIGN-TOKENS.md)

## 修复建议
[代码块]
```
