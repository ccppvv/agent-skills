# Design Tokens 集成

## Token 格式

```json
{
  "color": {
    "primary": "#0066CC",
    "text": "#1A1A1A"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px"
  },
  "font": {
    "body": "Inter, sans-serif",
    "heading": "Inter, sans-serif"
  }
}
```

## 检测现有 Tokens

```bash
# CSS Variables
cat styles.css | grep --color=auto ':root'

# SCSS
cat styles.scss | grep '\$'

# Styled Components/Tailwind
cat tailwind.config.js
cat theme.js
```

## 映射策略

```
设计值 → Token 查找 → 使用/创建
#FFFFFF → color.white → ✅ 使用
#AB12CD → color.brand-new → ➕ 新建
```
