---
name: large-scale-parallel-development
description: |
  Systematic workflow for developing large multi-stage projects using parallel AI agents (codex-ally, claude-code).
  Use when: (1) project has 10+ interdependent development phases, (2) need to maximize development velocity,
  (3) multiple modules can be built independently, (4) using AI coding assistants for implementation.
  Covers dependency analysis, batch parallelization, progress tracking with planning-with-files, and handling
  background task output issues. Applicable to full-stack applications, microservices, or any complex software project.
author: Claude Code
version: 1.0.0
date: 2026-02-08
---

# Large-Scale Parallel Development Workflow

## Problem
Developing large projects with many interdependent phases sequentially is slow. Manual coordination of parallel development is error-prone and difficult to track.

## Context / Trigger Conditions
Use this workflow when:
- Project has 10+ development phases/modules
- Phases have clear dependencies (e.g., API must exist before frontend can integrate)
- Using AI coding assistants (codex-ally, claude-code, etc.) for implementation
- Need to maximize development velocity
- Want systematic progress tracking

## Solution

### Step 1: Project Planning with planning-with-files

Create three core files in project root:

**task_plan.md** - Define all phases and dependencies
```markdown
## Phase 1: Project Setup [pending]
**依赖**: 无
**任务**: 初始化项目结构、配置工具链

## Phase 2: Database Layer [pending]
**依赖**: Phase 1
**任务**: Schema设计、DAO实现

## Phase 3: API Layer [pending]
**依赖**: Phase 2
**任务**: REST API实现

## 并行执行策略
### 第一批（无依赖）
- Phase 1

### 第二批（依赖 Phase 1）
- Phase 2, Phase 3, Phase 4

## 进度追踪
- [ ] Phase 1
- [ ] Phase 2
...
```

**findings.md** - 记录技术选型和研究
```markdown
## 技术选型
- 数据库: SQLite vs PostgreSQL
- 选择 SQLite: 无需额外服务，适合本地应用

## 待解决问题
1. 如何处理并发写入？
2. 如何优化查询性能？
```

**progress.md** - 跟踪实施进度
```markdown
## 2026-02-08
- ✅ Phase 1 完成
- 🔄 Phase 2 进行中
- SESSION_ID: xxx (用于继续会话)
```

### Step 2: 依赖分析和批次划分

**原则**:
- 同一批次的任务必须无依赖关系
- 后续批次只能依赖前面批次的已完成任务
- 尽量让每批次的任务数量均衡

**示例**:
```
19个阶段 → 7个批次
批次1: Phase 1 (1个任务)
批次2: Phase 2,3,4,11 (4个任务，都依赖Phase 1)
批次3: Phase 5,7,8,12,14 (5个任务，依赖批次2)
批次4: Phase 6,13 (2个任务，依赖批次3)
批次5: Phase 9,10,15 (3个任务，依赖批次4)
批次6: Phase 16,17 (2个任务，依赖批次5)
批次7: Phase 18,19 (2个任务，依赖批次6)
```

### Step 3: 并行执行任务

**使用 codex-ally 并行启动**:
```bash
# 批次2: 同时启动4个任务
python3 /path/to/codex_bridge.py \
  --cd "/project/path" \
  --PROMPT "Phase 2: 数据库层实现..." \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 /path/to/codex_bridge.py \
  --cd "/project/path" \
  --PROMPT "Phase 3: Git管理器..." \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 /path/to/codex_bridge.py \
  --cd "/project/path" \
  --PROMPT "Phase 4: 代理适配器..." \
  --sandbox workspace-write \
  --skip-git-repo-check &

python3 /path/to/codex_bridge.py \
  --cd "/project/path" \
  --PROMPT "Phase 11: 前端架构..." \
  --sandbox workspace-write \
  --skip-git-repo-check &
```

**关键参数**:
- `--sandbox workspace-write`: 允许写入文件
- `--skip-git-repo-check`: 允许在非Git仓库运行
- `&`: 后台运行（可选）

### Step 4: 监控任务进度

**方法1: 使用 TaskOutput 工具**
```bash
# 等待任务完成
TaskOutput(task_id="xxx", block=true, timeout=180000)
```

**方法2: 检查文件系统**
```bash
# 检查文件是否创建
ls -la /project/path/server/src/services/
ls -la /project/path/client/src/components/
```

**方法3: 检查输出文件**
```bash
# 查看任务输出
cat /tmp/tasks/task-id.output | python3 -c "import sys, json; print(json.loads(sys.stdin.read())['success'])"
```

### Step 5: 处理后台任务输出问题

**问题**: 后台任务的输出文件可能为空

**解决方案**:
1. **优先使用 TaskOutput 工具**
   ```python
   TaskOutput(task_id="xxx", block=true, timeout=180000)
   ```

2. **检查文件系统确认完成**
   ```bash
   # 即使输出文件为空，检查实际文件是否创建
   ls -la /project/path/target/files/
   ```

3. **必要时使用前台运行**
   ```bash
   # 移除 & 符号，直接等待完成
   python3 codex_bridge.py --cd "/path" --PROMPT "..." 2>&1
   ```

### Step 6: 更新进度并继续

每批次完成后:
1. 更新 task_plan.md 标记完成的阶段
2. 更新 progress.md 记录 SESSION_ID 和完成情况
3. 启动下一批次任务

## Verification

**检查点**:
- [ ] 所有阶段都有明确的依赖关系定义
- [ ] 同批次任务之间无依赖冲突
- [ ] 每个阶段完成后都更新了进度文件
- [ ] 所有任务的输出都已验证（文件创建或输出内容）

**成功指标**:
- 并行执行减少了总开发时间
- 没有因依赖问题导致的返工
- 进度文件准确反映实际状态

## Example

**实际案例**: 多代理任务看板系统

**项目规模**:
- 19 个开发阶段
- 后端: 10 个模块（数据库、API、WebSocket、进程管理等）
- 前端: 7 个模块（看板、配置、通知等）

**执行结果**:
- 7 个批次并行执行
- 17 个阶段完成（89%）
- 生成 67 个 TypeScript 文件
- 约 460KB 代码

**时间对比**:
- 串行执行估计: 每阶段 15 分钟 × 19 = 285 分钟（4.75 小时）
- 并行执行实际: 每批次 20 分钟 × 7 = 140 分钟（2.3 小时）
- **节省时间: 约 50%**

## Notes

**最佳实践**:
- 每批次任务数量控制在 2-5 个，避免过度并行导致资源竞争
- 使用 SESSION_ID 可以继续之前的会话，保持上下文
- 定期检查文件系统，不要完全依赖输出文件
- 遇到问题时快速调整策略，不要死等

**常见陷阱**:
- 依赖分析不准确导致任务失败
- 后台任务输出为空但实际已完成
- 忘记更新进度文件导致状态混乱
- 过度并行导致系统资源不足

**适用场景**:
- ✅ 全栈应用开发
- ✅ 微服务架构
- ✅ 多模块系统
- ✅ 大型重构项目
- ❌ 高度耦合的单体应用（难以并行）
- ❌ 探索性原型（依赖关系不明确）

## References

- [Claude Code Tasks System: Parallel Development Workflow Management](https://claudecode.jp/en/news/claude-code-tasks-system)
- [Claude Code Agent Teams: Setup Guide](https://serenitiesai.com/articles/claude-code-agent-teams-guide)
- [How We're 20xing Development Velocity with Agents](https://xalliance.substack.com/p/how-were-20xing-development-velocity)
- [Planning with Files Skill](https://github.com/anthropics/claude-code/tree/main/skills/planning-with-files)
