# Ally Orchestrator 改进计划

## 对比 ok skill 后的改进方向

### 1. 模块化架构（高优先级）

```
hi/
├── SKILL.md
├── README.md
├── modules/
│   ├── dispatch.md      # 任务派发策略
│   ├── priority.md      # 优先级排序
│   ├── lifecycle.md     # 生命周期管理
│   ├── complexity.md    # 复杂度评估
│   ├── dependencies.md  # 依赖管理
│   └── state-machine.md # 状态转换
├── lib/
│   ├── state.js         # 状态管理
│   ├── lock.js          # 文件锁
│   └── priority.js      # 优先级计算
├── scripts/
│   └── orchestrator.py  # 主控脚本
└── config/
    ├── config.json      # 配置
    └── hooks.json       # 钩子定义
```

### 2. 复杂度感知（高优先级）

```json
{
  "tasks": [
    {
      "id": "simple-task",
      "complexity": 0,        // 简单查询，单 agent
      "ally": "codex",
      "prompt": "查询状态"
    },
    {
      "id": "medium-task",
      "complexity": 1,        // 中等复杂，单 agent + 后处理
      "ally": "claude",
      "prompt": "实现功能"
    },
    {
      "id": "complex-task",
      "complexity": 2,        // 高复杂度，planner + 多 agent teams
      "ally": "codex",
      "prompt": "重构整个模块",
      "requires_planning": true
    }
  ]
}
```

### 3. 状态机（中优先级）

```
当前: PENDING → RUNNING → DONE/FAILED

改进: 
N (New) → I (Implementing) → P (Processing) → 
A (Analyzing) → C (Complete, 待验收) → D (Done) / W (Rejected) / T (Trouble)
```

### 4. 依赖管理（中优先级）

```json
{
  "tasks": [
    {
      "id": "task-1",
      "ally": "codex",
      "prompt": "实现基础模块"
    },
    {
      "id": "task-2",
      "ally": "claude",
      "prompt": "基于 task-1 实现扩展",
      "depends_on": ["task-1"],      // 等待 task-1 完成
      "blocks": ["task-3", "task-4"]  // 阻塞后续任务
    }
  ]
}
```

### 5. 并发控制（中优先级）

```json
{
  "batch_name": "large-project",
  "concurrency": {
    "max_per_project": 5,      // 同项目最多 5 个并发
    "max_per_ally": 2,         // 同 ally 最多 2 个并发
    "total_max": 10            // 全局最多 10 个并发
  }
}
```

### 6. 智能调度（低优先级）

```python
# 优先级计算公式（参考 ok）
priority = (importance * 3) + (urgency * 2) - (complexity * 1)

# 排序规则
1. 优先级高的先执行
2. 复杂度低的优先（快速完成）
3. 无依赖的优先（不阻塞他人）
4. 重试次数少的优先
```

### 7. 文件锁机制（低优先级）

```python
# 防止并发修改冲突
with FileLock(f"{batch_dir}/batch.lock"):
    # 安全修改 batch.json
    pass
```

### 8. 钩子系统（低优先级）

```json
{
  "hooks": {
    "on_task_start": "notify_slack",
    "on_task_complete": "run_tests",
    "on_task_failed": "create_issue",
    "on_batch_complete": "generate_report"
  }
}
```

## 实施建议

### 阶段 1：核心改进（1-2小时）
1. 添加复杂度字段和分层处理
2. 实现依赖管理（depends_on/blocks）
3. 添加并发限制

### 阶段 2：增强功能（2-3小时）
4. 模块化拆分
5. 改进状态机
6. 优先级调度算法

### 阶段 3：高级特性（按需）
7. 文件锁机制
8. 钩子系统
9. Web Dashboard

## 当前版本保持不变的优势

1. ✅ 简单易用 - 上手门槛低
2. ✅ 快速分发 - 立即返回总控
3. ✅ 集中监控 - 统一状态查看
4. ✅ 结果聚合 - Markdown 报告

## 建议

**方案 A：渐进改进**
- 保留当前 hi 作为"轻量版"
- 创建 hi-pro 作为"增强版"（参考 ok 架构）

**方案 B：原地升级**
- 基于当前版本逐步添加复杂度/依赖/并发控制
- 保持向后兼容（简单任务批次仍可用）

**方案 C：保持现状**
- hi 专注"快速分发+监控"
- 复杂编排场景继续使用 ok skill

你倾向哪个方案？
