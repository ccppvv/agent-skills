---
name: Prometheus
description: 基于 vibe-coding-cn 项目模板创建新项目，集成 planning-with-files 作为需求开发入口。支持在线克隆和本地复制两种模式，自动初始化 memory-bank、CLAUDE.md、Git 仓库等核心配置。
version: 1.0.0
author: Affairs & Claude
---

# Prometheus SKILL - Vibe Coding 项目模板创建器

## 核心能力

Prometheus 是一个项目初始化 SKILL，它将：
1. 基于 [vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn) 创建标准化项目结构
2. 自动配置 memory-bank 机制（architecture.md, progress.md 等）
3. 生成项目专属的 CLAUDE.md 行为准则
4. 集成 planning-with-files SKILL 作为需求开发入口
5. 初始化 Git 仓库并创建首次提交

## 使用场景

- 启动新的 Vibe Coding 项目
- 需要规范化的项目结构和 AI 协作流程
- 希望使用 planning-with-files 进行需求驱动开发

## 执行流程

### 阶段 1: 项目创建模式选择

询问用户选择项目创建模式：

**选项 A: 在线克隆模式**
- 从 GitHub 克隆最新的 vibe-coding-cn 仓库
- 优点：获取最新版本和完整资产
- 缺点：需要网络连接

**选项 B: 本地复制模式**
- 从本地已有的 vibe-coding-cn 副本复制
- 优点：快速、无需网络
- 缺点：需要用户提供本地路径

### 阶段 2: 项目信息收集

询问用户以下信息：
1. **项目名称**（必填）：用于创建项目目录
2. **项目描述**（必填）：一句话描述项目目标
3. **技术栈**（可选）：预期使用的技术栈（如：React + Node.js + PostgreSQL）
4. **目标路径**（可选）：项目创建位置，默认为当前目录

如果选择本地复制模式，额外询问：
5. **vibe-coding-cn 本地路径**：本地模板仓库的路径

### 阶段 3: 项目结构创建

执行以下操作：

1. **创建项目目录**
   ```bash
   mkdir -p <target_path>/<project_name>
   cd <target_path>/<project_name>
   ```

2. **获取模板**
   - 在线模式：`git clone https://github.com/tukuaiai/vibe-coding-cn.git .`
   - 本地模式：`cp -r <local_vibe_coding_path>/* .`

3. **清理模板痕迹**
   ```bash
   rm -rf .git  # 移除原仓库的 Git 历史
   ```

4. **创建 memory-bank 目录**
   ```bash
   mkdir -p memory-bank
   ```

5. **生成核心文件**

   **memory-bank/architecture.md**:
   ```markdown
   # 项目架构文档

   ## 项目概述
   - **项目名称**: <project_name>
   - **项目描述**: <project_description>
   - **技术栈**: <tech_stack>
   - **创建时间**: <timestamp>

   ## 目录结构

   ```
   <project_name>/
   ├── memory-bank/           # 项目记忆库
   │   ├── architecture.md    # 架构文档（本文件）
   │   ├── progress.md        # 进度追踪
   │   ├── implementation-plan.md  # 实施计划（待生成）
   │   └── tech-stack.md      # 技术栈详情（待生成）
   ├── i18n/                  # 多语言资产
   │   └── zh/                # 中文主语料
   │       ├── documents/     # 文档库
   │       ├── prompts/       # 提示词库
   │       └── skills/        # 技能库
   ├── libs/                  # 核心库代码
   │   ├── common/            # 通用模块
   │   ├── database/          # 数据库模块
   │   └── external/          # 外部工具
   ├── backups/               # 备份脚本
   ├── AGENTS.md              # AI Agent 行为准则
   ├── CLAUDE.md              # Claude 模型上下文
   └── README.md              # 项目主文档
   ```

   ## 文件职责说明

   ### 核心配置文件
   - **AGENTS.md**: 定义 AI Agent 的操作边界和行为约束
   - **CLAUDE.md**: 提供 Claude 模型的项目上下文和开发规范
   - **Makefile**: 自动化脚本（lint、备份等）

   ### memory-bank/ 目录
   - **architecture.md**: 记录项目架构、文件职责、模块关系
   - **progress.md**: 追踪开发进度和已完成任务
   - **implementation-plan.md**: 详细的实施计划和分步指令
   - **tech-stack.md**: 技术栈选型理由和最佳实践

   ## 开发规范

   ### 文件修改约束
   - ✅ 允许修改：`i18n/`, `libs/`, `memory-bank/`
   - ⚠️ 谨慎修改：`AGENTS.md`, `CLAUDE.md`
   - 🚫 禁止修改：`.github/workflows/`, `backups/gz/`, `LICENSE`

   ### 提交规范
   遵循 Conventional Commits：
   ```
   feat|fix|docs|chore|refactor|test: scope - summary
   ```

   ## 架构演进记录

   ### [<timestamp>] 项目初始化
   - 使用 Prometheus SKILL 基于 vibe-coding-cn 模板创建项目
   - 初始化 memory-bank 目录结构
   - 配置 Git 仓库
   ```

   **memory-bank/progress.md**:
   ```markdown
   # 项目进度追踪

   ## 项目信息
   - **项目名称**: <project_name>
   - **创建时间**: <timestamp>
   - **当前阶段**: 项目初始化

   ## 进度记录

   ### [<timestamp>] 项目初始化完成
   - ✅ 使用 Prometheus SKILL 创建项目结构
   - ✅ 初始化 memory-bank 目录
   - ✅ 生成 CLAUDE.md 项目上下文
   - ✅ 配置 Git 仓库
   - ⏳ 待办：使用 planning-with-files 创建需求文档

   ## 下一步行动

   1. 运行 `/planning-with-files` 开始需求规划
   2. 完善 `memory-bank/tech-stack.md` 技术栈文档
   3. 根据需求生成 `memory-bank/implementation-plan.md`

   ## 开发日志

   <!-- 在此记录每次重大功能开发的详细信息 -->
   ```

6. **生成项目专属 CLAUDE.md**

   基于 vibe-coding-cn 的 AGENTS.md，生成定制化的 CLAUDE.md：

   ```markdown
   # CLAUDE.md - <project_name> 项目上下文

   ## 项目概述

   **<project_name>** - <project_description>

   - **技术栈**: <tech_stack>
   - **创建时间**: <timestamp>
   - **模板来源**: [vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn)

   ## 核心理念

   本项目遵循 **Vibe Coding** 开发哲学：
   - **规划驱动**: 先规划后编码，避免代码失控
   - **上下文固定**: memory-bank 机制确保 AI 理解项目全貌
   - **模块化优先**: 多文件架构，拒绝单体巨文件
   - **测试先行**: 每个功能都有验证步骤

   ## 关键命令

   ```bash
   # 需求规划（使用 planning-with-files SKILL）
   /planning-with-files

   # Lint 检查
   make lint

   # 项目备份
   bash backups/一键备份.sh

   # 提示词转换（如需要）
   cd libs/external/prompts-library && python3 main.py
   ```

   ## 开发工���流

   ### 1. 需求阶段
   - 使用 `/planning-with-files` 创建需求文档
   - 生成 `memory-bank/implementation-plan.md`
   - 明确技术栈并更新 `memory-bank/tech-stack.md`

   ### 2. 实施阶段
   - **必读文件**: 开始编码前必须阅读 `memory-bank/` 下所有文档
   - **分步执行**: 按 `implementation-plan.md` 逐步实施
   - **进度记录**: 每完成一步更新 `progress.md`
   - **架构同步**: 重大变更同步更新 `architecture.md`

   ### 3. 验证阶段
   - 每步完成后运行测试验证
   - 通过后提交 Git：`git add . && git commit -m "feat: <description>"`
   - 新建会话继续下一步（避免上下文污染）

   ## 文件修改约束

   ### 允许的操作
   - ✅ 读取、修改 `i18n/`, `libs/`, `memory-bank/` 下的文档与代码
   - ✅ 执行 `make lint`、备份脚本、prompts-library 转换工具
   - ✅ 新增/修改提示词、技能、文档
   - ✅ 提交符合规范的 commit

   ### 禁止的操作
   - 🚫 修改 `.github/workflows/` 中的 CI 配置（除非任务明确要求）
   - 🚫 删除或覆盖 `backups/gz/` 中的存档文件
   - 🚫 修改 `LICENSE`, `CODE_OF_CONDUCT.md`
   - 🚫 在代码中硬编码密钥、Token 或敏感凭证
   - 🚫 未经确认的大范围重构

   ### 敏感区域（禁止自动修改）
   - `.github/workflows/*.yml` - CI/CD 配置
   - `backups/gz/` - 历史备份存档
   - `.env*` 文件（如存在）

   ## 代码规范

   ### 架构原则
   - 保持根目录扁平，避免巨石文件
   - 多语言资产统一放在 `i18n/<lang>/` 下
   - 遵循三层结构：documents / prompts / skills

   ### 命名约定
   - 文档、注释、日志使用中文
   - 代码符号统一英文且语义直白
   - 文件名小写加中划线或下划线

   ### 提交规范
   遵循简化 Conventional Commits：
   ```
   feat|fix|docs|chore|refactor|test: scope - summary
   ```

   示例：
   - `feat: auth - add JWT authentication`
   - `fix: api - resolve CORS issue`
   - `docs: readme - update installation guide`

   ## 项目特定配置

   <!-- 在此添加项目特定的配置、约束和最佳实践 -->

   ## 常见问题

   ### Q: 如何开始第一个需求？
   A: 运行 `/planning-with-files`，按提示完成需求文档创建。

   ### Q: 如何确保 AI 理解项目上下文？
   A: 每次新会话开始时，提示 AI："阅读 memory-bank/ 下所有文档，了解项目当前状态。"

   ### Q: 如何避免代码失控？
   A: 严格遵循 implementation-plan.md，一次只实施一步，验证通过后再继续。

   ---

   **最后更新**: <timestamp>
   **维护者**: <project_name> Team
   ```

### 阶段 4: Git 仓库初始化

执行以下 Git 操作：

```bash
# 初始化 Git 仓库
git init

# 创建 .gitignore（如果不存在）
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# 环境变量
.env
.env.local
.env.*.local

# 备份
backups/gz/

# 临时文件
*.tmp
*.bak
EOF

# 添加所有文件
git add .

# 创建首次提交
git commit -m "chore: initialize project from vibe-coding-cn template

- Created project structure based on vibe-coding-cn
- Initialized memory-bank with architecture.md and progress.md
- Generated project-specific CLAUDE.md
- Configured Git repository

Created by Prometheus SKILL"
```

### 阶段 5: 依赖检查

检查并提示安装必要的依赖：

1. **Node.js 依赖**
   ```bash
   # 检查 markdownlint-cli
   if ! command -v markdownlint &> /dev/null; then
       echo "⚠️  markdownlint-cli 未安装"
       echo "安装命令: npm install -g markdownlint-cli"
   fi
   ```

2. **Python 依赖**
   ```bash
   # 检查 Python 版本
   python3 --version

   # 检查必要的 Python 包
   pip3 list | grep -E "pandas|openpyxl|PyYAML|rich|InquirerPy"

   # 如果缺失，提示安装
   echo "安装 Python 依赖: pip3 install pandas openpyxl PyYAML rich InquirerPy"
   ```

3. **生成依赖安装脚本**

   创建 `setup-dependencies.sh`:
   ```bash
   #!/bin/bash

   echo "🔧 安装项目依赖..."

   # Node.js 依赖
   echo "📦 安装 markdownlint-cli..."
   npm install -g markdownlint-cli

   # Python 依赖
   echo "🐍 安装 Python 包..."
   pip3 install pandas openpyxl PyYAML rich InquirerPy

   echo "✅ 依赖安装完成！"
   echo ""
   echo "运行 'make lint' 验证 Markdown 格式"
   echo "运行 'cd libs/external/prompts-library && python3 main.py' 使用提示词转换工具"
   ```

   ```bash
   chmod +x setup-dependencies.sh
   ```

### 阶段 6: 需求开发入口

询问用户是否立即开始需求规划：

**提示信息**:
```
🎉 项目 <project_name> 创建成功！

📁 项目路径: <target_path>/<project_name>
📋 核心文件已生成:
   - memory-bank/architecture.md
   - memory-bank/progress.md
   - CLAUDE.md
   - .gitignore
   - setup-dependencies.sh

🔧 下一步操作:
   1. 安装依赖: ./setup-dependencies.sh
   2. 验证环境: make lint
   3. 开始需求规划: /planning-with-files

是否立即启动 planning-with-files 进行需求规划？
```

**选项**:
- **是，立即开始** → 自动调用 `/planning-with-files` SKILL
- **否，稍后手动启动** → 显示完成信息并退出

如果用户选择"是"，执行：
```
/planning-with-files
```

如果用户选择"否"，显示：
```
✅ 项目初始化完成！

📖 快速开始指南:
   1. cd <target_path>/<project_name>
   2. ./setup-dependencies.sh  # 安装依赖
   3. /planning-with-files     # 开始需求规划

📚 参考文档:
   - CLAUDE.md: 项目开发规范
   - memory-bank/architecture.md: 项目架构说明
   - AGENTS.md: AI 行为准则

💡 提示: 每次新会话开始时，提示 AI 阅读 memory-bank/ 下所有文档。
```

## 错误处理

### 常见错误及解决方案

1. **网络连接失败（在线模式）**
   - 错误: `fatal: unable to access 'https://github.com/tukuaiai/vibe-coding-cn.git/'`
   - 解决: 提示用户切换到本地复制模式，或检查网络连接

2. **本地路径不存在（本地模式）**
   - 错误: 用户提供的 vibe-coding-cn 路径无效
   - 解决: 提示用户提供正确路径，或切换到在线克隆模式

3. **目标目录已存在**
   - 错误: 项目目录已存在
   - 解决: 询问用户是否覆盖、重命名或取消操作

4. **Git 未安装**
   - 错误: `git: command not found`
   - 解决: 提示用户安装 Git，或跳过 Git 初始化步骤

5. **权限不足**
   - 错误: 无法在目标路径创建目录
   - 解决: 提示用户检查目录权限或更换目标路径

## 使用示例

### 示例 1: 在线克隆模式

```
用户: /Prometheus

Prometheus: 欢迎使用 Prometheus SKILL！请选择项目创建模式：
       A. 在线克隆模式（从 GitHub 获取最新版本）
       B. 本地复制模式（从本地副本快速创建）

用户: A

Prometheus: 请提供以下项目信息：
       1. 项目名称: my-awesome-app
       2. 项目描述: 一个基于 AI 的智能助手应用
       3. 技术栈（可选）: React + FastAPI + PostgreSQL
       4. 目标路径（可选，默认当前目录）: ~/projects

Prometheus: 正在创建项目...
       ✅ 克隆 vibe-coding-cn 模板
       ✅ 创建 memory-bank 目录
       ✅ 生成 architecture.md
       ✅ 生成 progress.md
       ✅ 生成 CLAUDE.md
       ✅ 初始化 Git 仓库
       ✅ 创建首次提交

       🎉 项目创建成功！

       是否立即启动 planning-with-files 进行需求规划？

用户: 是

Prometheus: [自动调用 /planning-with-files]
```

### 示例 2: 本地复制模式

```
用户: /Prometheus

Prometheus: 欢迎使用 Prometheus SKILL！请选择项目创建模式：
       A. 在线克隆模式（从 GitHub 获取最新版本）
       B. 本地复制模式（从本地副本快速创建）

用户: B

Prometheus: 请提供以下项目信息：
       1. 项目名称: quick-prototype
       2. 项目描述: 快速原型验证项目
       3. 技术栈（可选）: Vue + Express
       4. 目标路径（可选）:
       5. vibe-coding-cn 本地路径: /tmp/vibe-coding-cn

Prometheus: 正在创建项目...
       ✅ 从本地复制模板
       ✅ 创建 memory-bank 目录
       ✅ 生成核心文件
       ✅ 初始化 Git 仓库

       🎉 项目创建成功！

       是否立即启动 planning-with-files 进行需求规划？

用户: 否

Prometheus: ✅ 项目初始化完成！

       📖 快速开始指南:
          1. cd ./quick-prototype
          2. ./setup-dependencies.sh
          3. /planning-with-files
```

## 最佳实践

1. **首次使用建议使用在线克隆模式**，确保获取最新的模板和文档
2. **项目名称使用小写加连字符**，如 `my-project` 而非 `MyProject`
3. **项目描述要简洁明确**，���句话说清楚项目目标
4. **技术栈尽量具体**，便于后续生成精确的实施计划
5. **定期运行 `make lint`** 保持文档质量
6. **每次新会话开始时提醒 AI 阅读 memory-bank/**，确保上下文连续性

## 与其他 SKILL 的集成

- **planning-with-files**: 需求规划和实施计划生成
- **skill-creator**: 创建项目专属的自定义 SKILL
- **workflow-creator**: 定义项目特定的工作流程

## 版本历史

- **v1.0.0** (2026-01-10): 初始版本
  - 支持在线克隆和本地复制两种模式
  - 自动初始化 memory-bank 和 CLAUDE.md
  - 集成 planning-with-files 作为需求入口
  - Git 仓库自动配置
  - 依赖检查和安装脚本生成

## 许可证

本 SKILL 基于 MIT 许可证开源。

---

**作者**: Affairs & Claude
**最后更新**: 2026-01-10
**模板来源**: [vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn)
