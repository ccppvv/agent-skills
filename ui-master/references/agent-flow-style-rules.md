# agent-flow 样式规则

## 技术事实

- Vue3 + Vite + Less
- 规范源：`DESIGN-TOKENS.md`
- 实现层：`src/design-tokens.less`

## 强制规则

1. 禁止硬编码颜色值，优先 token/less 变量。
2. 禁止引入未定义圆角和边框色。
3. token 变更必须同步更新 md 与 less。
4. 检查禁用态、输入态、错误态的一致性。
