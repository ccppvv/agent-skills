# Design Tokens

> 本文件由 visual-reconstruction 技能自动维护
> 手动编辑请保持格式一致

## 更新记录

| 日期 | 新增 Tokens | 说明 |
|-----|-------------|------|
| {创建日期} | 初始文件 | 技能自动创建 |

---

## 颜色 (Colors)

### 品牌色 (Brand)
- `color.primary` = {值} - 主色
- `color.secondary` = {值} - 次要色

### 中性色 (Neutral)
- `color.text` = {值} - 正文文本
- `color.text-secondary` = {值} - 次要文本
- `color.border` = {值} - 边框色
- `color.background` = {值} - 背景色
- `color.surface` = {值} - 表面色

### 语义色 (Semantic)
- `color.success` = {值} - 成功
- `color.warning` = {值} - 警告
- `color.error` = {值} - 错误
- `color.info` = {值} - 信息

---

## 间距 (Spacing)

- `spacing.xs` = 4px - 极小间距
- `spacing.sm` = 8px - 小间距
- `spacing.md` = 16px - 中间距
- `spacing.lg` = 24px - 大间距
- `spacing.xl` = 32px - 超大间距

---

## 字体 (Typography)

### 字号 (Font Size)
- `font-size-xs` = 12px - 极小
- `font-size-sm` = 14px - 小
- `font-size-md` = 16px - 中（正文）
- `font-size-lg` = 18px - 大
- `font-size-xl` = 20px - 超大
- `font-size-2xl` = 24px - 特大

### 字体族 (Font Family)
- `font-body` = {值} - 正文字体
- `font-heading` = {值} - 标题字体
- `font-mono` = {值} - 等宽字体

### 行高 (Line Height)
- `line-height-tight` = 1.25 - 紧凑
- `line-height-normal` = 1.5 - 正常
- `line-height-relaxed` = 1.75 - 宽松

### 字重 (Font Weight)
- `font-weight-normal` = 400 - 常规
- `font-weight-medium` = 500 - 中等
- `font-weight-semibold` = 600 - 半粗
- `font-weight-bold` = 700 - 粗体

---

## 圆角 (Border Radius)

- `radius-none` = 0px - 无圆角
- `radius-sm` = 4px - 小圆角
- `radius-md` = 8px - 中圆角
- `radius-lg` = 12px - 大圆角
- `radius-xl` = 16px - 超大圆角
- `radius-full` = 9999px - 完全圆角

---

## 阴影 (Shadows)

- `shadow-sm` = {值} - 小阴影
- `shadow-md` = {值} - 中阴影
- `shadow-lg` = {值} - 大阴影
- `shadow-xl` = {值} - 超大阴影

---

## 过渡 (Transitions)

- `transition-fast` = 150ms - 快速
- `transition-normal` = 250ms - 正常
- `transition-slow` = 350ms - 慢速

---

## 断点 (Breakpoints)

- `breakpoint-mobile` = 640px - 手机
- `breakpoint-tablet` = 1024px - 平板
- `breakpoint-desktop` = 1440px - 桌面

---

## CSS Variables 输出

```css
:root {
  /* 颜色 */
  --color-primary: {值};
  --color-text: {值};

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;

  /* 字体 */
  --font-size-md: 16px;
  --font-body: {值};

  /* 圆角 */
  --radius-md: 8px;
}
```
