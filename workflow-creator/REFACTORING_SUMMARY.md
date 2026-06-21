# Workflow Creator 改造总结

## 改造完成时间
2026-01-03

## 改造目标
将 workflow-creator SKILL 从**工作流导向**改造为**能力导向**，确保生成的 agent 是可复用的通用能力，而非一次性的工作流特定组件。

---

## 核心问题

### 旧设计的问题 ❌

```yaml
工作流: multi-region-deploy
  ↓
决策: 复杂度 >= complex → 创建 agent
  ↓
生成: multi-region-deploy-specialist.md
  ↓
问题: 只能用于这一个工作流，无法复用
```

**根本原因**:
1. **工作流导向思维** - 决策基于工作流复杂度，而非能力需求
2. **缺失能力库检查** - 每次都创建新 agent，不检查已有能力
3. **命名工作流特定** - 使用工作流名称命名 agent
4. **目录结构混乱** - 无法区分通用能力和工作流特定

---

## 改造方案

### 新设计的流程 ✅

```yaml
工作流: multi-region-deploy
  ↓
Step 1: 提取能力需求
  - deployment-orchestrator (部署编排)
  - parallel-coordinator (并行协调)
  - health-monitor (健康监控)
  ↓
Step 2: 检查能力库
  - deployment-orchestrator: 已存在 → 复用
  - parallel-coordinator: 已存在 → 复用
  - health-monitor: 不存在 → 评估可复用性
  ↓
Step 3: 创建决策
  - health-monitor: reusability 0.90 >= 0.7 → 创建通用能力
  ↓
结果: 这些能力可被其他工作流复用
```

---

## 完成的工作

### 1. 新增核心模块

#### `core/capability-extractor.md`
- **功能**: 从工作流描述中提取通用能力需求
- **能力分类**:
  - Orchestration (编排): parallel-coordinator, sequential-coordinator, conditional-router
  - Domain (领域): deployment-orchestrator, health-monitor, rollback-handler
  - Integration (集成): api-integrator, service-connector, event-dispatcher
- **算法**:
  - 模式→能力映射
  - 领域→能力映射
  - 集成能力识别
  - 可复用性评分

#### `core/capability-library.md`
- **功能**: 管理能力库，避免重复创建
- **算法**:
  - 能力库扫描和索引
  - 精确匹配和模糊匹配
  - 覆盖度计算
  - 创建决策 (复用/创建/内联)

### 2. 重构现有模块

#### `core/decision-engine.md`
- **新增 Step 5A**: 提取能力需求
- **新增 Step 5B**: 检查能力库
- **修改 Step 5C**: 从复杂度导向改为能力导向决策
- **输出格式**: 包含能力分析和创建决策

### 3. 更新文档

#### `docs/agent-template-reference.md`
- **创建标准**: 从复杂度导向→能力导向
- **新增元数据**: type, reusability, applicable_workflows
- **输出位置**: capabilities/{category}/ vs workflows/
- **命名规范**: 能力名称 vs 工作流名称

#### `/commands/v-create-workflow.md`
- **流程更新**: 添加能力提取和库检查步骤
- **输出内容**: 添加能力分析报告
- **边界说明**: 明确只创建通用能力
- **示例**: 添加能力导向输出示例

### 4. 目录结构

```bash
~/.claude/agents/
├── capabilities/              # 通用能力 (新增)
│   ├── orchestration/         # 编排能力
│   │   ├── parallel-coordinator.md
│   │   ├── sequential-coordinator.md
│   │   └── conditional-router.md
│   ├── domain/                # 领域能力
│   │   ├── deployment-orchestrator.md
│   │   ├── health-monitor.md
│   │   └── rollback-handler.md
│   └── integration/           # 集成能力
│       ├── api-integrator.md
│       └── service-connector.md
└── workflows/                 # 工作流特定 (极少使用)
    └── legacy-migration-specialist.md
```

---

## 核心变化对比

| 维度 | 旧设计 ❌ | 新设计 ✅ |
|------|----------|----------|
| **决策依据** | 工作流复杂度 | 能力需求+库检查 |
| **Agent命名** | multi-region-deploy-specialist | deployment-orchestrator |
| **可复用性** | 单一工作流 | 多个工作流复用 |
| **目录结构** | workflows/ | capabilities/{category}/ |
| **创建阈值** | complexity >= complex | reusability >= 0.7 |
| **库检查** | 无 | 精确+模糊匹配 |
| **覆盖度评估** | 无 | 0.0-1.0 评分 |

---

## 使用流程

### 旧流程 ❌
```
用户描述 → 分析复杂度 → 复杂度高 → 创建工作流特定 agent
```

### 新流程 ✅
```
用户描述
  ↓
提取能力需求 (capability-extractor.md)
  ↓
检查能力库 (capability-library.md)
  ├─ 已存在且覆盖度 >= 0.85 → 复用
  ├─ 已存在但覆盖度 < 0.85 → 评估扩展
  └─ 不存在 → 评估可复用性
     ├─ >= 0.7 → 创建通用能力
     └─ < 0.7 → 内联到 command
  ↓
生成 command + 复用/创建 agent
```

---

## 实际效果示例

### 场景：创建多区域部署工作流

**旧方式 ❌**:
```yaml
输入: "并行部署到三个区域，验证健康，失败回滚"
  ↓
分析: 复杂度 high (0.88)
  ↓
决策: 创建 multi-region-deploy-specialist.md
  ↓
问题: 下次创建 blue-green-deploy 时，又创建 blue-green-deploy-specialist.md
      两个 agent 功能重叠，无法复用
```

**新方式 ✅**:
```yaml
输入: "并行部署到三个区域，验证健康，失败回滚"
  ↓
提取能力:
  - deployment-orchestrator (0.95)
  - parallel-coordinator (0.92)
  - health-monitor (0.88)
  - rollback-handler (0.82)
  ↓
检查库:
  - deployment-orchestrator: 已存在 → 复用
  - parallel-coordinator: 已存在 → 复用
  - health-monitor: 不存在 → 创建 (reusability 0.90)
  - rollback-handler: 不存在 → 创建 (reusability 0.88)
  ↓
结果:
  - 复用 2 个现有能力
  - 创建 2 个新通用能力
  - 下次创建 blue-green-deploy 时，可以复用这 4 个能力
```

---

## 能力分类体系

### Orchestration (编排能力)
协调和控制工作流执行的能力。

- `parallel-coordinator` - 协调并行执行多个独立任务
- `sequential-coordinator` - 协调顺序执行有依赖关系的任务
- `conditional-router` - 根据条件路由到不同执行路径
- `async-executor` - 异步执行不阻塞主流程的任务
- `retry-coordinator` - 协调重试和循环执行逻辑
- `state-manager` - 管理跨步骤的共享状态

### Domain (领域能力)
特定业务领域的专业能力。

- `deployment-orchestrator` - 编排部署流程，协调多环境发布
- `health-monitor` - 监控系统健康状态，执行验证检查
- `rollback-handler` - 处理回滚逻辑，恢复到之前状态
- `test-coordinator` - 协调测试执行，管理测试流程
- `batch-processor` - 批量处理多个项目或文件
- `config-validator` - 验证配置文件和设置的正确性
- `build-orchestrator` - 编排构建流程，协调编译和打包
- `migration-coordinator` - 协调迁移流程，管理升级过程

### Integration (集成能力)
系统间集成和通信的能力。

- `api-integrator` - 集成外部API，处理HTTP请求
- `service-connector` - 连接和协调多个服务
- `event-dispatcher` - 分发事件和消息到订阅者
- `data-transformer` - 转换数据格式和结构
- `notification-dispatcher` - 发送通知和告警消息

---

## 创建决策规则

### 何时创建新能力

**必须同时满足**:
1. ✅ 能力库中不存在此能力
2. ✅ 可复用性 >= 0.7
3. ✅ 可被 3+ 个工作流使用
4. ✅ 不依赖特定工作流上下文

### 何时不创建

- ❌ 能力已存在且覆盖度高 (复用现有)
- ❌ 可复用性低 < 0.7 (内联到 command)
- ❌ 工作流特定逻辑 (写入 command 的 behavioral flow)
- ❌ 一次性操作 (不值得抽象)

---

## 可复用性评分算法

```python
reusability_score = (
    type_score * 0.4 +           # 能力类型 (orchestration=1.0, domain=0.7)
    abstraction_score * 0.3 +    # 抽象程度 (越少工作流特定词汇越高)
    breadth_score * 0.2 +        # 适用场景广度
    confidence * 0.1             # 提取置信度
)

# 阈值
if reusability_score >= 0.7:
    create_capability_agent()
else:
    inline_to_command()
```

---

## 覆盖度评分算法

```python
coverage_score = (
    focus_areas_coverage * 0.4 +    # Focus Areas 重叠度
    key_actions_coverage * 0.4 +    # Key Actions 重叠度
    scenario_coverage * 0.2         # 适用场景重叠度
)

# 决策
if coverage_score >= 0.85:
    reuse_existing()
elif coverage_score >= 0.7:
    evaluate_extension()
else:
    create_new()
```

---

## 元数据规范

### 通用能力 Agent 元数据

```yaml
---
name: capability-name              # 能力名称，非工作流名称
type: capability                   # 标识为能力型
reusability: 0.XX                  # 可复用性评分
applicable_workflows:              # 适用的工作流类型
  - workflow-type-1
  - workflow-type-2
  - workflow-type-3
description: Brief description     # 通用能力描述
category: orchestration|domain|integration
created_from: original-workflow    # 首次创建来源(可选)
---
```

### 命名规范

**✅ 好的命名** (通用能力):
- `deployment-orchestrator` - 通用部署编排能力
- `health-monitor` - 通用健康监控能力
- `parallel-coordinator` - 通用并行协调能力

**❌ 不好的命名** (工作流特定):
- `multi-region-deploy-specialist` - 工作流特定
- `project-x-deployer` - 项目特定
- `one-time-migration-handler` - 一次性操作

---

## 验证改造效果

### 测试场景 1: 首次创建部署工作流

```bash
输入: /create-workflow 部署到 staging 并验证健康

预期:
  - 提取能力: deployment-orchestrator, health-monitor
  - 检查库: 两者都不存在
  - 创建: 两个通用能力 agent
  - 位置: capabilities/domain/
```

### 测试场景 2: 创建第二个部署工作流

```bash
输入: /create-workflow 蓝绿部署到生产环境

预期:
  - 提取能力: deployment-orchestrator, health-monitor
  - 检查库: 两者都已存在
  - 复用: 两个现有能力 agent
  - 创建: 0 个新 agent
```

### 测试场景 3: 低可复用性逻辑

```bash
输入: /create-workflow 为项目 X 执行特定的数据迁移

预期:
  - 提取能力: custom-migration-logic
  - 评估: reusability 0.45 < 0.7
  - 决策: 不创建 agent，内联到 command
```

---

## 后续优化建议

### 短期 (1-2周)

1. **创建初始能力库**
   - 手动创建 6 个核心编排能力
   - 手动创建 8 个核心领域能力
   - 手动创建 5 个核心集成能力

2. **完善匹配算法**
   - 优化模糊匹配的相似度计算
   - 改进覆盖度评分的权重
   - 添加语义相似度匹配

3. **增强验证**
   - 添加能力命名规范检查
   - 验证 applicable_workflows 的合理性
   - 检查 reusability 评分的准确性

### 中期 (1-2月)

1. **能力库维护**
   - 定期审查能力使用情况
   - 合并功能重叠的能力
   - 扩展覆盖度不足的能力
   - 删除长期未使用的能力

2. **智能推荐**
   - 基于历史数据推荐相似能力
   - 自动识别可合并的能力
   - 提示可扩展的能力

3. **可视化工具**
   - 能力依赖关系图
   - 能力使用热力图
   - 覆盖度分析报告

### 长期 (3-6月)

1. **机器学习优化**
   - 基于使用数据优化可复用性评分
   - 自动学习能力分类规则
   - 预测能力需求

2. **跨项目能力共享**
   - 建立公共能力库
   - 能力版本管理
   - 能力市场

---

## 总结

### 改造成果

✅ **核心问题解决**:
- 从工作流导向转变为能力导向
- 建立了能力提取和库检查机制
- 实现了智能复用和创建决策

✅ **可复用性提升**:
- Agent 可被多个工作流复用
- 减少重复创建
- 提高能力库质量

✅ **目录结构优化**:
- 清晰的能力分类
- 通用能力 vs 工作流特定
- 易于维护和扩展

### 关键指标

- **可复用性阈值**: >= 0.7
- **覆盖度阈值**: >= 0.85
- **能力分类**: 3 大类 (编排/领域/集成)
- **核心能力**: 19 个预定义能力

### 设计原则

1. **能力优先**: 先识别能力，再决定创建
2. **复用优先**: 优先复用现有能力
3. **通用优先**: 只创建通用能力，不创建工作流特定
4. **质量优先**: 高可复用性才创建，低可复用性内联

---

*改造完成日期: 2026-01-03*
*改造者: Claude Sonnet 4.5*
