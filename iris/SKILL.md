---
name: iris
description: Use before reading code or project files. Prefer cx for structural navigation, fall back to LSP only when cx is unavailable, and read file content directly only after narrower options fail.
---

# Iris - 智能文件读取助手

像虹膜控制光线进入眼睛一样，Iris 用分层策略控制信息流入 context window。

## 核心原则

1. **先 `cx`，后 LSP，最后才是 Read** - 代码文件默认按 `cx > LSP > 精确读取 > 全文读取` 降级
2. **先侦察再下钻** - 先拿结构、符号、引用，再读取局部正文
3. **精确读取优于全文读取** - 只读必须读的片段
4. **非代码文件按体积分流** - 小文件可直读，大文件先询问用户或先搜索再读
5. **失败必须显式告知** - `cx` 或 LSP 失败时，说明原因、当前降级路径和下一步建议，禁止静默退化

## 优先级总览

### 代码文件

```
代码文件读取请求
    ↓
先判断是否可用 cx
    ↓
    ├─ cx 可用 → cx overview / symbols / definition / references
    │            ↓
    │         如仍需正文 → 精确 Read
    ↓
    └─ cx 不可用 → 明确说明原因
                 ↓
               尝试 LSP
                 ↓
                 ├─ LSP 可用 → symbol / definition / references
                 │            ↓
                 │         如仍需正文 → 精确 Read
                 ↓
                 └─ LSP 不可用 → 明确提示安装对应 LSP
                              ↓
                           必要时仅做保守的精确 Read / rg
```

### 非代码文件

```
非代码文件读取请求
    ↓
计算行数 / 大小
    ↓
    ├─ ≤200 行 → 可直接 Read
    ├─ >200 行 → 先问用户，或先搜索再按范围 Read
    └─ 特殊文件 → 使用专门策略
```

## `cx` 优先策略

`cx` 是代码理解的一等工具。只要 `cx` 可用，就不要先走 LSP，也不要先全文读取。

### 标准升级路径

1. **理解文件结构** → `cx overview <file>`
2. **跨项目找符号** → `cx symbols [--kind K] [--name GLOB] [--file PATH]`
3. **读取具体函数/类型** → `cx definition --name <name> [--from PATH]`
4. **追踪影响面** → `cx references --name <name> [--file PATH]`
5. **只在必要时读取正文** → 对目标片段做精确 `Read`

### 什么时候必须先用 `cx`

- 准备读任意代码文件前
- 准备修改函数、类、接口、类型前
- 准备重构、改签名、追引用前
- 在多个文件里找实现入口时
- 之前读过整文件但上下文被压缩掉时

### `cx` 快速参考

```bash
cx overview PATH                                    # 文件结构总览
cx symbols [--kind K] [--name GLOB] [--file PATH]  # 跨文件搜符号
cx definition --name NAME [--from PATH]            # 读取符号定义
cx references --name NAME [--file PATH]            # 查找引用
cx lang list                                        # 查看已安装 grammar
cx lang add LANG [LANG...]                          # 安装 grammar
```

短别名：`cx o`、`cx s`、`cx d`、`cx r`

### `cx` 不可用时的判定

以下任一情况都算 `cx` 当前不可用，必须显式说明后再降级到 LSP：

- 命令不存在，例如 `which cx` 失败
- grammar 缺失，例如 `cx: rust grammar not installed`
- 数据库或索引不可访问，例如权限、I/O、损坏
- 当前语言或文件类型不受支持

### `cx` 失败时的标准提示

```text
当前优先工具 `cx` 不可用：<具体原因>。
我将降级到 LSP 获取结构信息，而不是直接全文读取。
如果你希望恢复 `cx` 路径，可先处理：<安装 grammar / 修复索引 / 权限问题>。
```

### 缺 grammar 时的处理

如果报错类似 `cx: <lang> grammar not installed`：

```bash
cx lang list
cx lang add <lang>
```

常见示例：

- Rust → `cx lang add rust`
- Go → `cx lang add go`
- Python → `cx lang add python`
- TypeScript / JavaScript → `cx lang add typescript javascript`

## LSP 兜底策略

只有在 `cx` 当前不可用时，才使用 LSP 做结构化理解。

### LSP 的推荐用途

- `documentSymbol`：拿文件符号大纲
- `hover`：拿类型和说明
- `goToDefinition`：跳到定义
- `findReferences`：追引用
- `workspaceSymbol`：跨工作区搜符号

### LSP 工作流

#### 小代码文件（≤200 行）

```bash
# cx 不可用时，才使用 LSP
documentSymbol(file_path)

# 如果结构足够清楚，可直接精确 Read 目标片段
Read(file_path, offset=start, limit=count)
```

#### 大代码文件（>200 行）

```bash
# 1. 先用 LSP 拿结构
documentSymbol(file_path)

# 2. 必要时补类型和引用
hover(symbol)
goToDefinition(symbol)
findReferences(symbol)

# 3. 最后再精确读取正文
Read(file_path, offset=symbol.line, limit=30-80)
```

### LSP 失败时必须怎么说

如果 LSP 调用失败，不要只说“LSP 不可用”。必须明确告诉用户应该安装或启用哪个语言服务器。

标准提示模板：

```text
`cx` 当前不可用，我已尝试降级到 LSP，但 <语言> 的 LSP 也不可用：<具体错误>。
请先安装或启用对应语言服务器 `<server-name>`，然后我再继续按符号级方式读取。
如果你现在只想临时推进，我可以先用 `rg` / 精确 `Read` 做保守分析，但准确性和结构信息会差一些。
```

### 常见语言与 LSP 提示映射

| 语言 | 优先提示的 LSP |
|------|----------------|
| TypeScript / JavaScript | `vtsls` 或 `typescript-language-server` |
| Python | `pyright` 或 `pylsp` |
| Go | `gopls` |
| Rust | `rust-analyzer` |
| Java | `jdtls` |
| HTML / CSS / JSON | 对应 VS Code language server / 编辑器内置语言服务 |

### 推荐的用户提示示例

- TypeScript / JavaScript  
  ```text
  `cx` 不可用，且当前没有可用的 TS/JS LSP。请安装或启用 `vtsls`（或 `typescript-language-server`）后重试。
  ```
- Python  
  ```text
  `cx` 不可用，且当前没有可用的 Python LSP。请安装或启用 `pyright`（或 `pylsp`）后重试。
  ```
- Go  
  ```text
  `cx` 不可用，且当前没有可用的 Go LSP。请安装或启用 `gopls` 后重试。
  ```
- Rust  
  ```text
  `cx` 不可用，且当前没有可用的 Rust LSP。请安装或启用 `rust-analyzer` 后重试。
  ```

## 非代码文件策略

### 小文件（≤200 行）

```bash
Read(file_path)
```

### 大文件（>200 行）

```bash
# 先询问用户，或先搜索再读
AskUserQuestion(...)

# 或者
Grep(pattern, path=file_path) → Read(offset, limit)
```

## 特殊文件策略

| 文件类型 | 策略 |
|---------|------|
| 二进制文件 | 不读取，直接说明不支持 |
| 配置文件（`.json` / `.yaml` / `.toml`） | `<500` 行可直读，`≥500` 行先询问 |
| 日志文件（`.log`） | 先询问，优先 `tail -n 100` / `head -n 100` |
| 锁文件（`package-lock.json` / `yarn.lock`） | 默认不读，除非用户明确要求 |

## 正确示例

### 示例 1：修改大型 TypeScript 文件中的函数

```bash
# ✅ 首选：cx
cx overview src/feature.ts
cx definition --name handleSubmit --from src/feature.ts
cx references --name handleSubmit --file src/feature.ts

# 必要时再精确读取正文
Read(src/feature.ts, offset=145, limit=40)
```

如果 `cx` 不可用：

```bash
documentSymbol(src/feature.ts)
goToDefinition(handleSubmit)
Read(src/feature.ts, offset=145, limit=40)
```

### 示例 2：理解项目架构

```bash
# ✅ 首选：cx 跨文件搜符号
cx symbols --name '*Router*'
cx definition --name AppRouter
```

如果 `cx` 不可用：

```bash
workspaceSymbol("Router")
documentSymbol(src/router.ts)
```

### 示例 3：LSP 也失败时的处理

```text
当前 `cx` 因权限/索引问题不可用，我已降级到 LSP。
但这个 Python 文件的 LSP 也不可用：未检测到 `pyright` / `pylsp`。
请先安装或启用 Python LSP；如果你要我先继续，我可以用 `rg` 和精确 `Read` 做保守分析。
```

## 检查清单

在读取任何文件前，问自己：

- [ ] 这是代码文件还是非代码文件？
- [ ] 如果是代码文件，我是否先尝试了 `cx`？
- [ ] 如果 `cx` 失败，我是否明确说明了原因？
- [ ] 如果降级到 LSP，我是否只把它当兜底而不是默认路径？
- [ ] 如果 LSP 也失败，我是否明确告诉用户该安装哪个 LSP？
- [ ] 我真的需要正文吗，还是结构/符号信息已经够了？
- [ ] 如果必须读取，我能否用 `offset` / `limit` 精确读取？

## 反模式

- 看到代码文件就直接 `Read`
- 把 LSP 当默认首选，而不是 `cx` 兜底
- `cx` 或 LSP 失败后静默改用全文读取
- LSP 失败时不告诉用户该安装哪个语言服务器
- 大文档不询问用户就直接整文件读取

## 效果预期

| 场景 | 旧路径 | 新路径 |
|------|--------|--------|
| 修改大型代码文件 | LSP → Read | `cx` → 精确 Read |
| 跨文件追引用 | `workspaceSymbol` / grep | `cx symbols` / `cx references` |
| `cx` 不可用 | 容易直接退到 Read | 明确降级到 LSP |
| LSP 失败 | 信息不足 | 明确提示安装对应 LSP |

目标不是“永远不用 Read”，而是**永远不要在还有更强结构化工具可用时先读正文**。
