---
name: codeagent
description: 执行 codeagent-wrapper 处理多后端/前端 AI 编码任务，支持 @file 引用与结构化输出，兼容前端与后端研发场景。
---

# Codeagent Wrapper 集成指南

## 概览

通过 codeagent-wrapper 调用多后端 AI（Codex、Claude、Gemini）。支持 `@` 文件引用、并行任务与可配置安全控制，覆盖前端（React/Vue/CSS/构建链）与后端（Node.js/Python/Go/服务端）的开发需求。

## 适用场景

**后端开发**
- 复杂代码分析与架构梳理
- 多文件重构与依赖调整
- API 设计与实现

**前端开发**
- 组件与页面开发（React/Vue/Svelte 等）
- 样式与主题系统（CSS/Tailwind/SCSS）
- 响应式布局与交互优化
- 前端状态管理与数据流整合

## 前端场景兼容要点

- **框架与路由**：识别 React/Next/Vue/Nuxt/SvelteKit 等框架的目录约定与路由规则。
- **构建与打包**：Vite/webpack/Next CLI 等构建链的命令、配置与输出目录差异。
- **样式体系**：CSS Modules/SCSS/Tailwind/Styled Components 的使用方式与约束。
- **静态资源**：图片、字体、SVG、public 目录与 assets 管理策略。
- **体验与可用性**：响应式、无障碍（ARIA）、键盘交互、性能与可访问性。
- **测试与回归**：Vitest/Jest/RTL、Playwright/Cypress、Storybook 的测试策略。

## 使用方式

**HEREDOC 语法（推荐）**：
```bash
codeagent-wrapper - [working_dir] <<'EOF'
<task content here>
EOF
```

**指定后端**：
```bash
codeagent-wrapper --backend claude - <<'EOF'
<task content here>
EOF
```

**简单任务**：
```bash
codeagent-wrapper "simple task" [working_dir]
codeagent-wrapper --backend gemini "simple task"
```

## 后端能力与推荐

| 后端 | 命令 | 描述 | 适用场景 |
|---|---|---|---|
| codex | `--backend codex` | OpenAI Codex（默认） | 深度代码分析与复杂开发 |
| claude | `--backend claude` | Anthropic Claude | 简单任务与文档生成 |
| gemini | `--backend gemini` | Google Gemini | UI/UX 原型与组件搭建 |

### 后端选择建议

**Codex（默认）**
- 深度代码理解与复杂逻辑实现
- 大规模重构与精确依赖追踪
- 算法优化与性能调优
- 示例："分析 @src/core 的调用关系并优化模块依赖结构"

**Claude**
- 快速功能实现与清晰需求拆解
- 技术文档、API 说明、README 生成
- 提示词工程与规范化产出
- 示例："为 @package.json 生成安装、使用与 API 文档"

**Gemini**
- UI 组件脚手架与布局原型
- 设计系统与视觉一致性落地
- 交互与无障碍支持
- 示例："为 @src/pages/Dashboard.tsx 生成响应式布局与卡片组件"

**后端切换策略**
- Codex 负责分析与方案、Claude 负责文档、Gemini 负责 UI 实现
- 并行模式可按任务细分后端以发挥特长

## 前端任务模板

- 组件改造："优化 @src/components/Button.tsx 的交互状态与无障碍属性"
- 样式系统："为 @src/styles/theme.ts 增加浅色/深色主题变量"
- 页面布局："在 @src/pages/Home.tsx 添加响应式 Hero 与特性卡片"
- 性能优化："检查 @src/pages/Report.tsx 的渲染瓶颈并给出优化方案"

## 参数说明

- `task`（必填）：任务描述，支持 `@file` 引用
- `working_dir`（可选）：工作目录（默认当前）
- `--backend`（可选）：选择 AI 后端（codex/claude/gemini，默认 codex）
  - **说明**：Claude 后端仅在显式启用时添加 `--dangerously-skip-permissions`

## 返回格式

```
Agent response text here...

---
SESSION_ID: 019a7247-ac9d-71f3-89e2-a823dbd8fd14
```

## 会话续用

```bash
# 使用默认后端续用
codeagent-wrapper resume <session_id> - <<'EOF'
<follow-up task>
EOF

# 使用指定后端续用
codeagent-wrapper --backend claude resume <session_id> - <<'EOF'
<follow-up task>
EOF
```

## 并行执行

**默认（摘要模式，节省上下文）**：
```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: task1
backend: codex
workdir: /path/to/dir
---CONTENT---
task content
---TASK---
id: task2
dependencies: task1
---CONTENT---
dependent task
EOF
```

**完整输出模式（仅调试）**：
```bash
codeagent-wrapper --parallel --full-output <<'EOF'
...
EOF
```

**按任务指定后端**：
```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: task1
backend: codex
workdir: /path/to/dir
---CONTENT---
analyze code structure
---TASK---
id: task2
backend: claude
dependencies: task1
---CONTENT---
design architecture based on analysis
---TASK---
id: task3
backend: gemini
dependencies: task2
---CONTENT---
generate implementation code
EOF
```

**并发控制**：
通过 `CODEAGENT_MAX_PARALLEL_WORKERS` 限制并发（默认无限制）。

## 环境变量

- `CODEX_TIMEOUT`：超时时间（毫秒，默认 7200000 = 2 小时）
- `CODEAGENT_SKIP_PERMISSIONS`：控制 Claude 权限检查
  - Claude：`true`/`1` 添加 `--dangerously-skip-permissions`（默认关闭）
  - Codex/Gemini：当前无影响
- `CODEAGENT_MAX_PARALLEL_WORKERS`：并行任务数上限（默认无限制，建议 8）

## 调用模板

**单任务**：
```
Bash tool parameters:
- command: codeagent-wrapper --backend <backend> - [working_dir] <<'EOF'
  <task content>
  EOF
- timeout: 7200000
- description: <brief description>
```

**并行任务**：
```
Bash tool parameters:
- command: codeagent-wrapper --parallel --backend <backend> <<'EOF'
  ---TASK---
  id: task_id
  backend: <backend>  # Optional, overrides global
  workdir: /path
  dependencies: dep1, dep2
  ---CONTENT---
  task content
  EOF
- timeout: 7200000
- description: <brief description>
```

## 安全最佳实践

- **Claude 后端**：默认开启权限检查
  - 跳过检查：设置 `CODEAGENT_SKIP_PERMISSIONS=true` 或传 `--skip-permissions`
- **并发控制**：生产环境建议设置 `CODEAGENT_MAX_PARALLEL_WORKERS` 防止资源耗尽
- **自动化场景**：用于 AI 自动化执行，避免权限弹窗阻塞

## 最近更新

- 所有模式支持多后端（workdir / resume / parallel）
- 权限检查与可配置安全控制
- worker 池并发限制与失败快速取消
- 新增前端场景兼容要点与任务模板
