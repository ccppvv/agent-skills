---
name: github-skill-forge
description: '制造技能的技能：将任意 GitHub 仓库一键转换为 Claude Code 可用的标准化技能包。通过 GitHub API 云端扫描（Zero-Clone）+ Smart RAG 上下文聚合，自动提取核心代码和文档，生成 context_bundle.md 供 Agent 快速理解项目。'
tags: ["github", "skill-forge", "meta-skill", "automation", "skill-management", "context-aggregation"]
---

# GitHub Skill Forge

将任意 GitHub 仓库转换为 Claude Code 可直接使用的技能包。

## 触发条件

当用户说以下任何一种时触发：
- "帮我把这个仓库装成技能"
- "安装这个 GitHub 项目"
- "把这个开源工具变成技能"
- 发送 GitHub URL 并表示想集成/使用

## 使用方法

### 基础锻造

```bash
python3 ~/.claude/skills/github-skill-forge/scripts/forge.py "https://github.com/用户名/仓库名" -o ~/.claude/skills
```

### 指定技能名

```bash
python3 ~/.claude/skills/github-skill-forge/scripts/forge.py "https://github.com/用户名/仓库名" "自定义技能名" -o ~/.claude/skills
```

### 强制锻造（低 Star 仓库）

```bash
python3 ~/.claude/skills/github-skill-forge/scripts/forge.py "https://github.com/用户名/仓库名" --force -o ~/.claude/skills
```

## 工作流程

### Step 1: 执行锻造脚本
```bash
python3 ~/.claude/skills/github-skill-forge/scripts/forge.py "<GitHub URL>" -o ~/.claude/skills
```

### Step 2: 读取生成的上下文包
脚本会在 `~/.claude/skills/<技能名>/` 下生成 `context_bundle.md`。读取它来理解项目。

### Step 3: 创建 Claude Code 技能定义
在 `~/.claude/skills/<技能名>/` 下创建符合 Claude Code 格式的技能 markdown 文件：

```markdown
---
name: <技能名>
description: <简短描述>
---

# <技能名称>

## 功能
...

## 使用方法
...
```

### Step 4: 验证
运行工具的 help 命令确认安装成功：
```bash
python3 ~/.claude/skills/<技能名>/src/<main_script>.py --help
```

## 关键参数

| 参数 | 说明 |
|------|------|
| `URL` | GitHub 仓库地址（必填） |
| `SKILL_NAME` | 自定义技能名（可选，默认取仓库名） |
| `-o, --output` | 输出目录（默认 `~/.claude/skills`） |
| `--force` | 强制锻造低 Star 仓库 |
| `--dry-run` | 试运行，不实际执行 |

## 提升 API 限速

创建 `~/.claude/skills/github-skill-forge/.env`：
```
GITHUB_TOKEN=ghp_your_token_here
```
申请 Token: https://github.com/settings/tokens → 勾选 `public_repo`

## 注意事项

- 输出目录固定为 `~/.claude/skills/`，与 Claude Code 技能体系对齐
- 生成的 `context_bundle.md` 包含文件树、README、依赖信息
- 大型仓库可能耗时较长，脚本支持多线程 + 镜像轮换
- 锻造完成后需要手动创建符合 Claude Code 格式的技能 markdown 文件
