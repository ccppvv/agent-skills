# manage 样式规则

## 技术事实

- React 17 + TypeScript
- 样式形态：`styled-components` + JSS

## 执行规则

1. 优先复用已有样式文件与封装组件。
2. 避免新增内联 `style`。
3. 视觉改动同步覆盖状态样式。
4. 非必要不改全局主题，防止外溢。
