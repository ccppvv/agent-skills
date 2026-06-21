---
name: ted
description: "Intelligent file reading assistant that analyzes file size and type before reading. For large code files (200+ lines), uses LSP tools for structural analysis then reads target sections precisely, avoiding unnecessary context waste. For large non-code files, asks for user confirmation. Use when: (1) Reading or analyzing code files, especially large ones (200+ lines), (2) Modifying specific functions/classes in large files, (3) Searching for specific code patterns or definitions, (4) Any file reading task where efficiency matters, (5) Working with TypeScript, JavaScript, HTML, CSS, Python, or other LSP-supported languages."
---

# Ted - 智能文件读取助手

## 概述

Ted 是一个智能文件读取助手，通过预分析文件大小和类型来优化读取策略。对于大文件（>200行），优先使用 LSP 工具进行结构化分析，然后精确读取目标区域，显著减少 token 消耗并提高效率。

**核心优势**：
- ⚡ **Token 效率**: 大文件场景可节省 80-95% 的 token
- 🎯 **精确定位**: LSP 工具快速定位目标代码，无需浏览整个文件
- 🤖 **自动决策**: 根据文件大小和类型自动选择最优读取策略
- 💬 **用户友好**: 大型非代码文件会征求用户意见

## 工作流程

### 决策树

```
读取文件请求
    ↓
检查文件类型
    ↓
    ├─ 代码文件 (.ts/.js/.py/.java/etc.)
    │   ↓
    │   检查文件大小 (wc -l)
    │   ↓
    │   ├─ ≤ 200 行 → 直接读取全文 (Read tool)
    │   │
    │   └─ > 200 行 → LSP 工作流
    │       ↓
    │       1. 使用 LSP documentSymbol 获取结构
    │       2. 识别目标区域（函数/类/变量）
    │       3. 使用 Read tool 精确读取 (offset + limit)
    │
    └─ 非代码文件 (.md/.txt/.json/.yaml/etc.)
        ↓
        检查文件大小 (wc -l)
        ↓
        ├─ ≤ 200 行 → 直接读取全文
        │
        └─ > 200 行 → 询问用户
            ↓
            使用 AskUserQuestion tool:
            - 选项 1: 读取全文
            - 选项 2: 部分读取（指定行范围）
            - 选项 3: 取消读取
```

## 使用步骤

### Step 1: 预检查文件

在任何读取操作前，先获取文件元信息：

```bash
# 1. 检查文件行数
wc -l <file_path>

# 2. 确认文件类型（通过扩展名）
# .ts/.tsx/.js/.jsx → TypeScript/JavaScript (使用 vtsls)
# .html/.css → HTML/CSS (使用 vscode-langservers)
# .py → Python (使用 pylsp/pyright)
# .md/.txt/.json → 非代码文件
```

### Step 2: 选择读取策略

**情况 A: 小文件（≤200行）**
```bash
# 直接读取全文
Read filePath=<path>
```

**情况 B: 大型代码文件（>200行）**
```bash
# 步骤 1: 使用 LSP 获取文件结构
LSP operation=documentSymbol filePath=<path> line=1 character=1

# 步骤 2: 基于 LSP 结果，精确读取目标区域
# 示例：目标函数在 line 150-200
Read filePath=<path> offset=150 limit=51
```

**情况 C: 大型非代码文件（>200行）**
```bash
# 先询问用户
AskUserQuestion questions=[{
  "question": "文件 <path> 有 <N> 行，是否需要读取？",
  "header": "文件读取",
  "options": [
    {"label": "读取全文", "description": "加载完整文件内容"},
    {"label": "部分读取", "description": "指定行范围读取"},
    {"label": "取消读取", "description": "跳过此文件"}
  ]
}]
```

### Step 3: LSP 辅助操作（可选）

当需要更深入的代码分析时：

```bash
# 查找符号定义
LSP operation=goToDefinition filePath=<path> line=<N> character=<M>

# 查找所有引用
LSP operation=findReferences filePath=<path> line=<N> character=<M>

# 获取类型信息
LSP operation=hover filePath=<path> line=<N> character=<M>

# 查找实现
LSP operation=goToImplementation filePath=<path> line=<N> character=<M>
```

## 实战示例

### 示例 1: 分析大型 React 组件

**场景**: 用户要求分析 `src/components/Dashboard.tsx` (800 行) 中的数据加载逻辑

**传统方法** (不推荐):
```bash
# ❌ 直接读取 800 行，消耗大量 token
Read filePath=src/components/Dashboard.tsx
```

**Ted 方法** (推荐):
```bash
# ✅ Step 1: 检查文件大小
wc -l src/components/Dashboard.tsx
# 输出: 800

# ✅ Step 2: 使用 LSP 获取结构
LSP operation=documentSymbol filePath=src/components/Dashboard.tsx line=1 character=1
# 输出显示:
# - fetchDashboardData (line 250-320)
# - loadUserData (line 322-380)

# ✅ Step 3: 精确读取目标函数
Read filePath=src/components/Dashboard.tsx offset=250 limit=71
# 只读取 71 行，节省 91% token
```

### 示例 2: 修改特定方法

**场景**: 修改 `services/AuthService.ts` (600 行) 中的 `validateToken` 方法

```bash
# Step 1: 检查文件大小
wc -l services/AuthService.ts
# 输出: 600

# Step 2: 使用 LSP 定位方法
LSP operation=documentSymbol filePath=services/AuthService.ts line=1 character=1
# 输出显示: validateToken (line 145-180)

# Step 3: 读取方法及上下文（±10行）
Read filePath=services/AuthService.ts offset=135 limit=56

# Step 4: 进行修改
Edit filePath=services/AuthService.ts old_string=<...> new_string=<...>

# Step 5 (可选): 检查引用，确保修改不影响其他代码
LSP operation=findReferences filePath=services/AuthService.ts line=145 character=10
```

### 示例 3: 处理大型配置文件

**场景**: 查看 `docs/API.md` (500 行) 中关于认证的部分

```bash
# Step 1: 检查文件大小和类型
wc -l docs/API.md
# 输出: 500 (非代码文件)

# Step 2: 询问用户
AskUserQuestion questions=[{
  "question": "文件 docs/API.md 有 500 行，是否需要读取？",
  "header": "文件读取",
  "options": [
    {"label": "读取全文", "description": "加载完整文档"},
    {"label": "搜索关键词", "description": "先用 grep 搜索 'authentication'"},
    {"label": "取消", "description": "跳过"}
  ]
}]

# Step 3: 如果用户选择搜索
Grep pattern="authentication" path=docs/API.md output_mode=content -n
# 定位到 line 180-250

# Step 4: 精确读取相关部分
Read filePath=docs/API.md offset=180 limit=71
```

## 特殊文件处理规则

| 文件类型 | 大小阈值 | 处理策略 |
|---------|---------|---------|
| 代码文件 (.ts/.js/.py/etc.) | > 200 行 | 使用 LSP + 精确读取 |
| 配置文件 (.json/.yaml/.toml) | > 500 行 | 询问用户或使用 jq/yq |
| Markdown (.md) | > 200 行 | 询问用户或 grep 搜索 |
| 日志文件 (.log) | 任意大小 | 使用 `tail`/`head` |
| 锁文件 (package-lock.json) | 任意大小 | 默认不读取 |
| 二进制文件 | 任意大小 | 拒绝读取 |

## 高级技巧

### 1. 组合使用 LSP 操作

```bash
# 场景: 重构一个被广泛使用的函数

# Step 1: 定位函数定义
LSP operation=documentSymbol filePath=utils/helpers.ts line=1 character=1

# Step 2: 查找所有引用位置
LSP operation=findReferences filePath=utils/helpers.ts line=50 character=10

# Step 3: 逐个检查引用（只读取相关上下文）
# 假设引用在 file1.ts:120, file2.ts:80, file3.ts:200
Read filePath=file1.ts offset=110 limit=21  # 读取 line 110-130
Read filePath=file2.ts offset=70 limit=21   # 读取 line 70-90
Read filePath=file3.ts offset=190 limit=21  # 读取 line 190-210
```

### 2. 增量分析大型文件

```bash
# 场景: 逐步理解一个 1000 行的复杂文件

# Round 1: 获取整体结构
LSP operation=documentSymbol filePath=complex.ts line=1 character=1

# Round 2: 读取主要入口函数
Read filePath=complex.ts offset=<main_function_start> limit=<length>

# Round 3: 根据需要读取依赖函数
Read filePath=complex.ts offset=<dependency1_start> limit=<length>
Read filePath=complex.ts offset=<dependency2_start> limit=<length>

# 逐步建立理解，而不是一次性加载全部
```

### 3. 多文件协同分析

```bash
# 场景: 理解一个功能模块（涉及 3 个大文件）

# Step 1: 使用 LSP 快速定位每个文件的关键部分
LSP operation=documentSymbol filePath=controller.ts line=1 character=1
LSP operation=documentSymbol filePath=service.ts line=1 character=1
LSP operation=documentSymbol filePath=model.ts line=1 character=1

# Step 2: 只读取相关的函数/类
Read filePath=controller.ts offset=<target_start> limit=<length>
Read filePath=service.ts offset=<target_start> limit=<length>
Read filePath=model.ts offset=<target_start> limit=<length>

# Token 节省: 3 x 600 行 → 3 x 50 行 = 节省 92%
```

## 参考资源

### LSP 使用详情

查看 `references/lsp-examples.md` 获取：
- 完整的 LSP 操作示例
- 文件类型与 LSP 服务器映射表
- 更多实战场景和最佳实践

### 何时使用此 SKILL

✅ **应该使用**:
- 分析大型代码文件（>200 行）
- 修改特定函数/类而不需要看整个文件
- 查找函数定义、引用、调用关系
- 在多个大文件间追踪代码逻辑
- 任何涉及读取文件的操作（养成好习惯）

❌ **不需要使用**:
- 文件确定很小（<100 行）
- 已经清楚知道文件内容（最近刚读过）
- 需要浏览性地快速扫描文件（可先看结构再决定）

## 注意事项

1. **200 行是经验阈值**，可根据实际情况调整（例如：简单配置文件可以提高到 300 行）
2. **LSP 工具需要正确配置**，确保项目有对应的语言服务器
3. **精确读取时留足上下文**，建议目标代码前后各留 5-10 行
4. **非代码文件优先考虑搜索**，使用 grep 定位后再精确读取
5. **日志文件永远不要全量读取**，使用 tail/head 或 grep 过滤

## 效果对比

| 场景 | 传统方法 | Ted 方法 | Token 节省 |
|-----|---------|---------|-----------|
| 800 行组件分析 | 读取 800 行 | LSP + 读取 70 行 | 91% |
| 600 行服务修改 | 读取 600 行 | LSP + 读取 60 行 | 90% |
| 1000 行工具类查找 | 读取 1000 行 | LSP + 读取 40 行 | 96% |
| 3 个 500 行文件协同 | 读取 1500 行 | LSP + 读取 150 行 | 90% |

**平均 token 节省率**: 85-95%
