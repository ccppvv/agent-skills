# WCAG 2.1 AA 可访问性清单

## 颜色对比度

| 元素 | 最小对比度 | 工具 |
|-----|-----------|------|
| 正文文本 | 4.5:1 | Chrome DevTools |
| 大文本(18px+) | 3:1 | WebAIM Contrast |
| 图标/图形 | 3:1 | Contrast Checker |

## 语义化 HTML

```html
<!-- ✅ 正确 -->
<button>提交</button>
<nav>...</nav>
<main>...</main>

<!-- ❌ 错误 -->
<div onclick="...">提交</div>
<div class="nav">...</div>
```

## ARIA 标签

```html
<!-- 图标按钮 -->
<button aria-label="关闭">
  <icon-x />
</button>

<!-- 无障碍名称 -->
<img src="logo.png" alt="公司Logo">

<!-- 隐藏装饰元素 -->
aria-hidden="true"
```

## 键盘导航

```css
/* 焦点样式 */
:focus-visible {
  outline: 2px solid #0066CC;
  outline-offset: 2px;
}
```

## 检测工具

```bash
# Lighthouse
npx lighthouse https://example.com --view

# axe DevTools
# Chrome 扩展安装
```
