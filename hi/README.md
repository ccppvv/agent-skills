# Ally Orchestrator - 任务编排中心

## 🎯 核心价值

作为**总控**，你只需：
1. 定义任务（30秒）
2. 分发任务（1秒）
3. 继续其他工作
4. 随时查看进度（5秒）
5. 获取最终结果（10秒）

**总计时间投入：< 1分钟**，实际工作时间：2-10分钟（并行执行）

## 🚀 快速开始

### 1. 创建任务批次

```bash
cat > /tmp/my-tasks.json << 'EOF'
{
  "batch_name": "quick-test",
  "project_root": "/Users/v/Minds",
  "tasks": [
    {
      "id": "task-1",
      "ally": "codex",
      "prompt": "列出当前目录的文件",
      "sandbox": "read-only"
    },
    {
      "id": "task-2",
      "ally": "claude",
      "prompt": "显示 git status",
      "sandbox": "read-only"
    }
  ]
}
EOF
```

### 2. 分发任务（立即返回）

```bash
python3 ~/.agents/skills/hi/scripts/orchestrator.py dispatch /tmp/my-tasks.json
```

### 3. 查看状态

```bash
python3 ~/.agents/skills/hi/scripts/orchestrator.py status quick-test
```

### 4. 实时监控（可选）

```bash
python3 ~/.agents/skills/hi/scripts/orchestrator.py watch quick-test
```

### 5. 获取结果

```bash
python3 ~/.agents/skills/hi/scripts/orchestrator.py results quick-test
```

## 📋 任务批次格式

```json
{
  "batch_name": "unique-batch-id",
  "project_root": "/path/to/project",
  "tasks": [
    {
      "id": "task-id",
      "ally": "codex|claude|tcodex|gemini|codebuddy",
      "prompt": "任务描述",
      "sandbox": "read-only|workspace-write|danger-full-access",
      "skip_git_repo_check": true,
      "priority": "high|medium|low",
      "timeout": 180
    }
  ],
  "on_error": "continue|stop",
  "retry_failed": true,
  "max_retries": 2
}
```

## 🎮 命令参考

| 命令 | 用途 | 示例 |
|------|------|------|
| `dispatch` | 分发任务批次 | `orchestrator.py dispatch tasks.json` |
| `status` | 查看批次状态 | `orchestrator.py status batch-id` |
| `watch` | 实时监控批次 | `orchestrator.py watch batch-id` |
| `results` | 生成结果报告 | `orchestrator.py results batch-id report.md` |
| `kill` | 终止批次/任务 | `orchestrator.py kill batch-id [task-id]` |

## 📁 示例文件

两个示例文件位于 `~/.claude/orchestrator/examples/`：

1. **simple-check.json** - 简单的状态检查任务
2. **feature-implementation.json** - 完整功能实现流程

## 🔧 可用的 Ally

| Ally | 用途 | 特点 |
|------|------|------|
| **codex** | 通用代码生成 | OpenAI/Anthropic，功能全面 |
| **claude** | Claude Code CLI | 最适合代码审查和分析 |
| **tcodex** | 腾讯内部 Codex | 腾讯环境，IOA 认证 |
| **gemini** | Google Gemini | 多模态能力 |
| **codebuddy** | Codebuddy CLI | 另一种代码助手选择 |

## 💡 最佳实践

### 1. 任务拆分原则

- **独立性**：每个任务应该独立执行，不依赖其他任务的结果
- **聚焦性**：一个任务专注一个模块/功能
- **明确性**：prompt 清晰具体，包含所有必要的上下文

### 2. Ally 选择建议

- **代码生成**：codex, tcodex
- **代码审查**：claude, gemini
- **测试编写**：claude, codex
- **文档生成**：claude, gemini
- **调试分析**：claude, codex

### 3. 异常处理策略

```json
{
  "on_error": "continue",      // 某个任务失败不影响其他任务
  "retry_failed": true,         // 自动重试失败任务
  "max_retries": 2              // 最多重试2次
}
```

### 4. 超时设置

- 简单查询/分析：60-90秒
- 代码生成（单模块）：120-180秒
- 复杂实现：180-300秒

## 🚨 故障排查

### 问题：任务未启动

**检查：**
```bash
# 查看批次目录
ls -la ~/.claude/orchestrator/<batch-id>/

# 查看任务状态文件
cat ~/.claude/orchestrator/<batch-id>/<task-id>.status

# 查看输出文件
cat ~/.claude/orchestrator/<batch-id>/<task-id>.output
```

### 问题：任务卡住不动

**解决：**
```bash
# 强制终止
python3 orchestrator.py kill <batch-id> <task-id>

# 或终止整个批次
python3 orchestrator.py kill <batch-id>
```

### 问题：输出文件为空

**原因：** 任务还在运行或刚启动

**解决：** 等待更长时间，使用 `watch` 实时监控

## 📊 工作流示例

### 场景：实现一个完整的新功能

```bash
# 1. 准备实现文档（总控工作）
mkdir -p docs/feature-xyz
# 编写详细的实现文档...

# 2. 定义任务批次（总控工作，30秒）
cat > tasks/feature-xyz.json << 'EOF'
{
  "batch_name": "feature-xyz",
  "project_root": "/Users/v/Work/project",
  "tasks": [
    {"id": "impl-1", "ally": "codex", "prompt": "根据 docs/feature-xyz/core.md 实现核心模块", "sandbox": "workspace-write"},
    {"id": "impl-2", "ally": "tcodex", "prompt": "根据 docs/feature-xyz/api.md 实现API接口", "sandbox": "workspace-write"},
    {"id": "test-1", "ally": "claude", "prompt": "编写完整的单元测试，覆盖率80%+", "sandbox": "workspace-write"},
    {"id": "review", "ally": "gemini", "prompt": "全面代码审查，输出审查报告", "sandbox": "read-only"}
  ]
}
EOF

# 3. 分发任务（1秒，立即返回）
python3 orchestrator.py dispatch tasks/feature-xyz.json

# 4. 你去做其他工作...（喝咖啡、开会、处理其他项目）

# 5. 随时检查进度（5秒）
python3 orchestrator.py status feature-xyz

# 6. 实时监控（可选）
python3 orchestrator.py watch feature-xyz

# 7. 所有任务完成后获取结果（10秒）
python3 orchestrator.py results feature-xyz reports/feature-xyz-results.md

# 8. 查看报告并进行必要的调整
cat reports/feature-xyz-results.md
```

**总控时间：** 30秒（定义）+ 1秒（分发）+ 5秒（检查）+ 10秒（结果）= **46秒**  
**实际工作时间：** 4个任务并行，约 3-5分钟  
**效率提升：** 串行需要 12-20分钟，并行节省 **60-75%** 时间

## 🎯 总控工作模式

### 传统模式（低效）
```
总控 → 任务1 → 等待 → 任务2 → 等待 → 任务3 → 等待 → 完成
       ↓       ↓       ↓       ↓       ↓       ↓
       深度参与每个任务细节，无法并行
```

### Orchestrator 模式（高效）
```
总控 → [分发] → 继续其他工作 → [查看结果]
         ↓
    ┌────┴────┬────┬────┐
    任务1  任务2  任务3  任务4  ← 并行执行
    └────┬────┴────┴────┘
         ↓
      [汇总报告]
```

## 📈 扩展功能（未来）

- [ ] Web Dashboard - 浏览器实时监控
- [ ] 任务依赖管理 - `depends_on: ["task-1"]`
- [ ] 自动重试策略 - 指数退避
- [ ] 结果通知 - 邮件/Slack/企业微信
- [ ] 任务模板 - 预定义常用任务批次
- [ ] 历史查询 - 查看过往批次执行记录
- [ ] 性能统计 - Ally响应时间分析

## 🔗 相关文档

- [SKILL.md](SKILL.md) - 完整的 Skill 文档
- [codex-ally](../codex-ally/SKILL.md) - Codex Ally 文档
- [claude-ally](../claude-ally/SKILL.md) - Claude Ally 文档
- [tcodex-ally](../tcodex-ally/SKILL.md) - TCodeX Ally 文档

## 📝 License

Part of the Claude Code ECC (Enhanced Claude Configuration) ecosystem.
