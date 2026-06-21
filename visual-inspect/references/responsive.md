# 响应式设计模式

## 断点系统

```css
/* Mobile First */
@media (min-width: 640px)   { /* tablet */ }
@media (min-width: 1024px)  { /* desktop */ }
@media (min-width: 1440px)  { /* wide */ }
```

## 布局策略

| 屏幕 | 列数 | 间距 | 容器宽度 |
|-----|------|------|---------|
| mobile | 4 | 8px | 100% |
| tablet | 8 | 16px | 640px |
| desktop | 12 | 24px | 1024px |

## 图片响应

```css
img {
  max-width: 100%;
  height: auto;
  object-fit: cover;
}
```

## 字体缩放

```css
html { font-size: 16px; }
@media (max-width: 640px) {
  html { font-size: 14px; }
}
```
