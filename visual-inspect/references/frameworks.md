# 框架代码模式

## React

```jsx
// 组件结构
import styles from './Component.module.css';

export function Component({ title, children }) {
  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{title}</h2>
      {children}
    </div>
  );
}
```

## Vue

```vue
<template>
  <div class="container">
    <h2 class="title">{{ title }}</h2>
    <slot />
  </div>
</template>

<script setup>
defineProps(['title']);
</script>

<style scoped>
.container { /* ... */ }
</style>
```

## 原生

```html
<div class="container">
  <h2 class="title">...</h2>
</div>

<style>
.container { /* ... */ }
</style>
```

## 框架检测

```bash
# package.json 检查
grep -E "(react|vue|next|nuxt)" package.json

# 文件扩展名
ls src/**/*.{jsx,tsx,vue}
```
