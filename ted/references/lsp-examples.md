# LSP 工具使用示例和参考

## 文件类型与 LSP 服务器映射

| 文件类型 | LSP 服务器 | 主要功能 |
|---------|-----------|---------|
| `.ts`, `.tsx`, `.js`, `.jsx` | vtsls | TypeScript/JavaScript 符号分析 |
| `.html`, `.css` | vscode-langservers | HTML/CSS 结构分析 |
| `.py` | pylsp/pyright | Python 符号分析 |
| `.java` | jdtls | Java 符号分析 |
| `.go` | gopls | Go 符号分析 |
| `.rs` | rust-analyzer | Rust 符号分析 |

## LSP 操作示例

### 1. documentSymbol - 获取文档符号列表

**用途**: 快速了解文件结构（类、函数、变量等）

**示例 - TypeScript 文件**:
```bash
# 假设要分析 src/components/UserProfile.tsx (500 行)
# 步骤 1: 使用 LSP 获取符号列表
LSP operation=documentSymbol filePath=src/components/UserProfile.tsx line=1 character=1
```

**典型输出**:
```
Functions:
- UserProfile (line 15-120)
- fetchUserData (line 122-145)
- handleSubmit (line 147-180)

Classes:
- UserProfileState (line 10-13)

Interfaces:
- UserProfileProps (line 5-8)
```

**步骤 2**: 基于 LSP 结果，使用 Read 工具精确读取目标函数
```bash
# 只读取 fetchUserData 函数（122-145 行，共 24 行）
Read filePath=src/components/UserProfile.tsx offset=122 limit=24
```

### 2. goToDefinition - 查找符号定义

**用途**: 跟踪函数/类/变量的定义位置

**示例**:
```bash
# 在 line 50, character 10 位置有一个 getUserInfo 调用
# 查找它的定义位置
LSP operation=goToDefinition filePath=src/services/api.ts line=50 character=10
```

### 3. findReferences - 查找所有引用

**用途**: 了解某个符号在哪些地方被使用

**示例**:
```bash
# 查找 UserProfile 组件的所有引用位置
LSP operation=findReferences filePath=src/components/UserProfile.tsx line=15 character=10
```

### 4. hover - 获取类型和文档信息

**用途**: 快速查看类型定义、参数说明

**示例**:
```bash
# 获取 fetchUserData 函数的类型信息和文档
LSP operation=hover filePath=src/components/UserProfile.tsx line=122 character=10
```

## 智能读取策略示例

### 场景 1: 分析大型组件文件 (800 行)

**目标**: 理解 `PaymentForm.tsx` 中的表单验证逻辑

**步骤**:
1. 使用 `wc -l` 确认文件大小：800 行
2. 使用 LSP `documentSymbol` 获取结构
3. 识别目标函数：`validatePaymentData` (line 350-420)
4. 使用 Read 精确读取：`offset=350 limit=71`

**Token 节省**: 800 行 → 71 行，节省约 91% 的 token

### 场景 2: 查找方法调用关系 (1200 行)

**目标**: 了解 `DatabaseService.ts` 中 `executeQuery` 方法的调用链

**步骤**:
1. 使用 LSP `goToDefinition` 定位方法定义
2. 使用 LSP `findReferences` 查找所有调用位置
3. 对每个调用位置使用 Read 精确读取上下文（±20 行）

**优势**: 不需要读取整个 1200 行文件，只读取相关的代码片段

### 场景 3: 修改特定功能 (600 行)

**目标**: 在 `AuthService.ts` 中修改 `login` 方法

**步骤**:
1. 使用 LSP `documentSymbol` 定位 `login` 方法
2. 使用 LSP `findReferences` 查看依赖关系
3. 使用 Read 精确读取方法定义和相关依赖
4. 进行修改并使用 Edit 工具

**优势**: 只读取需要修改的部分，避免加载整个文件

## 特殊文件处理策略

### JSON/YAML 配置文件
- **< 500 行**: 直接读取全文
- **≥ 500 行**: 先询问用户，或使用 jq/yq 提取特定部分

### Markdown 文档
- **< 200 行**: 直接读取全文
- **≥ 200 行**: 先使用 grep 搜索关键词，确定目标区域后精确读取

### 日志文件
- **始终**: 使用 `tail -n 100` 或 `head -n 100` 查看部分内容
- **搜索**: 使用 `grep` 过滤关键日志行

### 锁文件 (package-lock.json, yarn.lock)
- **默认**: 不读取（除非用户明确要求）
- **原因**: 文件庞大且格式化程度低，token 效率极低
