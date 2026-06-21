---
name: init-project-non-git-worktree-fallback
description: |
  处理 /init-project 或类似初始化技能在非 git 目录中因 worktree 子代理无法启动而失败的回退流程。
  触发条件：
  (1) 使用依赖 Agent/worktree 的初始化技能；
  (2) 当前目录不是 git 仓库，或缺少 WorktreeCreate/WorktreeRemove hooks；
  (3) 出现 “Cannot create agent worktree” / “not in a git repository” / 无法启动子代理；
  (4) 任务本质上仍可通过主流程完成，例如批量初始化一级目录、生成或更新 CLAUDE.md、补结构索引。
author: Claude Code
version: 1.0.0
date: 2026-03-08
---

# Init Project Non-Git Worktree Fallback

## Problem
某些初始化技能依赖子代理，而子代理默认要求 worktree 隔离。在**非 git 多工作空间目录**中，这会直接失败，导致 `/init-project` 之类的流程无法继续。

典型报错：
- `Cannot create agent worktree`
- `not in a git repository`
- `no WorktreeCreate hooks are configured`

如果此时机械地重复调用原技能，只会卡住任务，不会推进结果。

## Context / Trigger Conditions
在以下情境中应使用本技能：

- 你要执行 `/init-project`、批量生成 `CLAUDE.md`、仓库上下文初始化等工作
- 当前目录是**工作空间容器**而不是 git 仓库根，例如知识库、多项目聚合目录、神祇目录容器
- 初始化技能底层依赖 Agent + worktree，而环境不满足
- 用户真正想要的是“完成初始化结果”，而不是执着于必须走原始技能链路

## Solution

### 1. 先明确失败根因，而不是盲目重试
看到 worktree 相关报错后，立即判断：

- 当前目录是否是 git 仓库？
- 是否配置了 WorktreeCreate/WorktreeRemove hooks？
- 失败是技能链路问题，还是任务本身不可做？

如果只是**子代理启动失败**，通常任务本身仍然可做。

### 2. 切换到“等价初始化”主流程
用主流程工具完成与原技能目标尽量等价的结果：

1. **盘点一级目录**
   - 列出所有一级目录
   - 区分空目录、非空目录、已有 `CLAUDE.md` 的目录

2. **识别活跃目录**
   优先看这些信号：
   - `README.md`
   - `CLAUDE.md`
   - `package.json`
   - `Cargo.toml`
   - `requirements.txt`
   - `pyproject.toml`
   - `go.mod`
   - 关键脚本或文档入口

3. **只初始化真正需要的目录**
   - 对空目录/占位目录通常不生成本地说明
   - 对非空且有活跃信号的目录补本地 `CLAUDE.md`

4. **写本地 `CLAUDE.md` 时遵循最小充分原则**
   包含：
   - 工作空间定位
   - 导航面包屑
   - 关键入口
   - 常用命令（如果已知）
   - 推荐工作方式
   - 注意事项/安全边界

5. **更新根级 `CLAUDE.md`**
   补充：
   - 已初始化目录列表
   - 新增目录列表
   - Mermaid 结构图
   - 覆盖率说明
   - 推荐下一步深挖路径

### 3. 避免被噪音目录误导
在多工作空间仓中，主动忽略：

- `node_modules/`
- `target/`
- `venv/`
- `sd_env/`
- `.next/`
- `dist/`
- `build/`
- `coverage/`
- 其它生成物目录

否则会把依赖包误识别成真实项目入口。

### 4. 对高敏感目录只做文档级初始化
若目录包含：
- `.env`
- 账号 JSON
- 凭据同步脚本
- 会访问外部服务的运维脚本

初始化时应**只写边界说明**，不要展开敏感细节，也不要自动执行。

### 5. 向用户说明这是“等价回退”
结果汇报时要清楚说明：

- 原技能为何不能直接跑
- ���采用了什么等价回退流程
- 已覆盖多少活跃目录
- 哪些目录因为空/无信号而跳过
- 下一步若要更完整，可以继续深挖哪些子目录

## Verification
回退方案完成后，应满足：

- 原任务目标已被实质推进，而不是停在报错
- 非空且活跃的一级目录都有明确的初始化处理结果
- 新建/更新的 `CLAUDE.md` 已落盘
- 根级 `CLAUDE.md` 已补目录索引与 Mermaid 结构图
- 用户能看到“覆盖范围、主要缺口、下一步建议”

## Example

场景：
用户要求“对当前文件夹下的所有一级目录执行 /init”。

实际情况：
- 当前目录是多工作空间容器
- 不是 git 仓库
- `zcf:init-project` 依赖子代理 + worktree
- 工具报错：`Cannot create agent worktree: not in a git repository`

正确处理：
1. 停止重复调用原技能
2. 盘点一级目录
3. 找出非空但缺少 `CLAUDE.md` 的活跃目录
4. 逐个读取入口文件并生成本地 `CLAUDE.md`
5. 在根级 `CLAUDE.md` 加一级目录初始化索引与 Mermaid 图
6. 汇报哪些目录已初始化、哪些为空跳过、建议下一步深挖哪些子项目

## Notes
- 这个回退技能适用于“目标仍可由主流程完成”的情况，不适用于真正依赖隔离 worktree 才能安全实施的代码改写任务
- 若后续环境补齐 git/worktree hooks，可重新回到原初始化技能链路
- 在多工作空间容器里，“全目录全覆盖”通常没有价值，优先覆盖活跃目录更务实
