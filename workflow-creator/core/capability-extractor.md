# Capability Extractor

## Purpose
从工作流描述中提取通用能力需求，而非创建工作流特定 agent。这是能力导向设计的核心模块。

## 设计原则

**能力导向 vs 工作流导向**:
```yaml
❌ 工作流导向:
  工作流: multi-region-deploy
  → 创建: multi-region-deploy-specialist
  → 问题: 只能用于这一个工作流

✅ 能力导向:
  工作流: multi-region-deploy
  → 分析需要的能力:
    - deployment-orchestrator (部署编排)
    - health-monitor (健康监控)
    - rollback-handler (回滚处理)
  → 检查能力库
  → 复用已有 / 创建缺失的通用能力
  → 结果: 这些能力可被其他部署工作流复用
```

---

## 能力分类体系

### 1. Orchestration Capabilities (编排能力)

协调和控制工作流执行的能力。

| 能力名称 | 触发模式 | 关键词 | 适用场景 |
|---------|---------|--------|---------|
| parallel-coordinator | Parallel | parallel, concurrent, simultaneously | 任何需要并行执行多个独立任务的工作流 |
| sequential-coordinator | Flow | then, next, after, pipeline | 任何需要顺序执行有依赖关系的工作流 |
| conditional-router | Branch | if, when, based on, condition | 任何需要根据条件选择执行路径的工作流 |
| async-executor | Async | background, async, non-blocking | 任何需要异步执行不阻塞主流程的工作流 |
| retry-coordinator | Looping | retry, repeat, until, while | 任何需要重试机制的工作流 |
| state-manager | Shared | shared, global, coordinated, state | 任何需要跨步骤共享状态的工作流 |

### 2. Domain Capabilities (领域能力)

特定业务领域的专业能力。

| 能力名称 | 领域 | 关键词 | 适用场景 |
|---------|------|--------|---------|
| deployment-orchestrator | Deployment | deploy, release, rollout, publish | 部署、发布、上线类工作流 |
| health-monitor | Monitoring | health, verify, check, status | 健康检查、状态验证类工作流 |
| rollback-handler | Recovery | rollback, revert, undo, restore | 回滚、恢复、撤销类工作流 |
| test-coordinator | Testing | test, validate, verify, qa | 测试、验证、质量保证类工作流 |
| batch-processor | Batch | batch, bulk, all files, each item | 批量处理、批处理类工作流 |
| config-validator | Configuration | config, settings, validate, check | 配置验证、设置检查类工作流 |
| build-orchestrator | Build | build, compile, package, bundle | 构建、编译、打包类工作流 |
| migration-coordinator | Migration | migrate, upgrade, convert, transform | 迁移、升级、转换类工作流 |

### 3. Integration Capabilities (集成能力)

系统间集成和通信的能力。

| 能力名称 | 集成类型 | 关键词 | 适用场景 |
|---------|---------|--------|---------|
| api-integrator | API | api, rest, graphql, endpoint | API集成、调用类工作流 |
| service-connector | Service | service, microservice, connect | 服务连接、微服务编排类工作流 |
| event-dispatcher | Event | event, message, queue, publish | 事件驱动、消息队列类工作流 |
| data-transformer | Data | transform, convert, map, etl | 数据转换、ETL类工作流 |
| notification-dispatcher | Notification | notify, alert, send, message | 通知、告警、消息发送类工作流 |

---

## 提取算法

### Step 1: 模式到能力映射

从检测到的图模式提取编排能力。

```python
def extract_pattern_capabilities(detected_patterns):
    """
    从图模式提取编排能力

    Args:
        detected_patterns: 来自 graph-detector.md 的模式列表

    Returns:
        编排能力列表
    """
    capabilities = []

    # 模式到能力的映射
    pattern_map = {
        'parallel': {
            'name': 'parallel-coordinator',
            'category': 'orchestration',
            'description': '协调并行执行多个独立任务'
        },
        'flow': {
            'name': 'sequential-coordinator',
            'category': 'orchestration',
            'description': '协调顺序执行有依赖关系的任务'
        },
        'branch': {
            'name': 'conditional-router',
            'category': 'orchestration',
            'description': '根据条件路由到不同执行路径'
        },
        'async': {
            'name': 'async-executor',
            'category': 'orchestration',
            'description': '异步执行不阻塞主流程的任务'
        },
        'looping': {
            'name': 'retry-coordinator',
            'category': 'orchestration',
            'description': '协调重试和循环执行逻辑'
        },
        'shared': {
            'name': 'state-manager',
            'category': 'orchestration',
            'description': '管理跨步骤的共享状态'
        }
    }

    for pattern in detected_patterns:
        # 只提取高置信度的模式
        if pattern['confidence'] >= 0.6:
            cap_info = pattern_map.get(pattern['name'])
            if cap_info:
                capabilities.append({
                    'name': cap_info['name'],
                    'category': cap_info['category'],
                    'description': cap_info['description'],
                    'source': 'pattern',
                    'confidence': pattern['confidence'],
                    'evidence': pattern.get('evidence', [])
                })

    return capabilities
```

### Step 2: 领域到能力映射

从工作流描述和分类提取领域能力。

```python
def extract_domain_capabilities(workflow_description, category, tasks):
    """
    从工作流描述提取领域能力

    Args:
        workflow_description: 用户的工作流描述
        category: 工作流分类 (deployment, testing, etc.)
        tasks: 结构化任务列表

    Returns:
        领域能力列表
    """
    capabilities = []
    description_lower = workflow_description.lower()

    # 领域能力的关键词映射
    domain_keywords = {
        'deployment-orchestrator': {
            'keywords': ['deploy', 'release', 'rollout', 'publish', 'launch'],
            'category': 'domain',
            'description': '编排部署流程，协调多环境发布'
        },
        'health-monitor': {
            'keywords': ['health', 'verify', 'check', 'status', 'validate', 'ensure'],
            'category': 'domain',
            'description': '监控系统健康状态，执行验证检查'
        },
        'rollback-handler': {
            'keywords': ['rollback', 'revert', 'undo', 'restore', 'recover'],
            'category': 'domain',
            'description': '处理回滚逻辑，恢复到之前状态'
        },
        'test-coordinator': {
            'keywords': ['test', 'validate', 'verify', 'qa', 'quality'],
            'category': 'domain',
            'description': '协调测试执行，管理测试流程'
        },
        'batch-processor': {
            'keywords': ['batch', 'bulk', 'all files', 'each item', 'for each'],
            'category': 'domain',
            'description': '批量处理多个项目或文件'
        },
        'config-validator': {
            'keywords': ['config', 'configuration', 'settings', 'validate', 'check'],
            'category': 'domain',
            'description': '验证配置文件和设置的正确性'
        },
        'build-orchestrator': {
            'keywords': ['build', 'compile', 'package', 'bundle', 'assemble'],
            'category': 'domain',
            'description': '编排构建流程，协调编译和打包'
        },
        'migration-coordinator': {
            'keywords': ['migrate', 'migration', 'upgrade', 'convert', 'transform'],
            'category': 'domain',
            'description': '协调迁移流程，管理升级过程'
        }
    }

    for capability_name, info in domain_keywords.items():
        # 计算关键词匹配度
        matched_keywords = [kw for kw in info['keywords'] if kw in description_lower]
        match_count = len(matched_keywords)

        # 至少匹配2个关键词才认为需要此能力
        if match_count >= 2:
            confidence = min(match_count / len(info['keywords']), 1.0)
            capabilities.append({
                'name': capability_name,
                'category': info['category'],
                'description': info['description'],
                'source': 'domain',
                'confidence': confidence,
                'evidence': matched_keywords
            })

    return capabilities
```

### Step 3: 集成能力识别

从任务类型识别集成能力需求。

```python
def extract_integration_capabilities(workflow_description, tasks):
    """
    从任务类型识别集成能力

    Args:
        workflow_description: 工作流描述
        tasks: 结构化任务列表

    Returns:
        集成能力列表
    """
    capabilities = []
    description_lower = workflow_description.lower()

    integration_keywords = {
        'api-integrator': {
            'keywords': ['api', 'rest', 'graphql', 'endpoint', 'http', 'request'],
            'category': 'integration',
            'description': '集成外部API，处理HTTP请求'
        },
        'service-connector': {
            'keywords': ['service', 'microservice', 'connect', 'integration', 'call'],
            'category': 'integration',
            'description': '连接和协调多个服务'
        },
        'event-dispatcher': {
            'keywords': ['event', 'message', 'queue', 'publish', 'subscribe', 'emit'],
            'category': 'integration',
            'description': '分发事件和消息到订阅者'
        },
        'data-transformer': {
            'keywords': ['transform', 'convert', 'map', 'etl', 'process', 'format'],
            'category': 'integration',
            'description': '转换数据格式和结构'
        },
        'notification-dispatcher': {
            'keywords': ['notify', 'alert', 'send', 'message', 'email', 'slack'],
            'category': 'integration',
            'description': '发送通知和告警消息'
        }
    }

    for capability_name, info in integration_keywords.items():
        matched_keywords = [kw for kw in info['keywords'] if kw in description_lower]
        match_count = len(matched_keywords)

        if match_count >= 2:
            confidence = min(match_count / len(info['keywords']), 1.0)
            capabilities.append({
                'name': capability_name,
                'category': info['category'],
                'description': info['description'],
                'source': 'integration',
                'confidence': confidence,
                'evidence': matched_keywords
            })

    return capabilities
```

### Step 4: 可复用性评分

评估每个能力的可复用性。

```python
def calculate_reusability(capability, workflow_description, category):
    """
    计算能力的可复用性评分

    Args:
        capability: 能力信息
        workflow_description: 工作流描述
        category: 工作流分类

    Returns:
        0.0-1.0 的可复用性评分
    """
    reusability_score = 0.0

    # 因素1: 能力类型 (40%)
    # 编排能力最通用，集成能力次之，领域能力看具体情况
    if capability['category'] == 'orchestration':
        type_score = 1.0  # 编排能力高度通用
    elif capability['category'] == 'integration':
        type_score = 0.85  # 集成能力较通用
    else:  # domain
        type_score = 0.7  # 领域能力通用性中等

    reusability_score += type_score * 0.4

    # 因素2: 抽象程度 (30%)
    # 检查描述中是否包含工作流特定的词汇
    workflow_specific_keywords = [
        'multi-region', 'blue-green', 'canary', 'specific-project',
        'custom-logic', 'one-time', 'legacy'
    ]

    specific_count = sum(1 for kw in workflow_specific_keywords
                        if kw in workflow_description.lower())

    # 越少工作流特定词汇，抽象程度越高
    abstraction_score = max(0.0, 1.0 - (specific_count * 0.2))
    reusability_score += abstraction_score * 0.3

    # 因素3: 适用场景广度 (20%)
    # 基于能力名称估算适用场景数
    broad_capabilities = [
        'parallel-coordinator', 'sequential-coordinator', 'conditional-router',
        'test-coordinator', 'deployment-orchestrator', 'health-monitor'
    ]

    if capability['name'] in broad_capabilities:
        breadth_score = 1.0
    else:
        breadth_score = 0.7

    reusability_score += breadth_score * 0.2

    # 因素4: 置信度 (10%)
    # 高置信度意味着需求明确，更可能被复用
    reusability_score += capability['confidence'] * 0.1

    return round(reusability_score, 2)
```

### Step 5: 能力去重和优先级

合并重复能力，按优先级排序。

```python
def prioritize_capabilities(all_capabilities):
    """
    去重并按优先级排序能力

    Args:
        all_capabilities: 所有提取的能力列表

    Returns:
        去重并排序后的能力列表
    """
    # 按能力名称分组
    capability_groups = {}
    for cap in all_capabilities:
        name = cap['name']
        if name not in capability_groups:
            capability_groups[name] = []
        capability_groups[name].append(cap)

    # 对每组选择最佳候选
    unique_capabilities = []
    for name, caps in capability_groups.items():
        # 选择置信度最高的
        best_cap = max(caps, key=lambda x: x['confidence'])

        # 合并所有证据
        all_evidence = []
        for cap in caps:
            all_evidence.extend(cap.get('evidence', []))
        best_cap['evidence'] = list(set(all_evidence))

        unique_capabilities.append(best_cap)

    # 按置信度和可复用性排序
    sorted_capabilities = sorted(
        unique_capabilities,
        key=lambda x: (x.get('reusability', 0), x['confidence']),
        reverse=True
    )

    # 过滤低置信度能力
    filtered = [cap for cap in sorted_capabilities if cap['confidence'] >= 0.6]

    return filtered
```

---

## 完整提取流程

```python
def extract_all_capabilities(workflow_description, detected_patterns, category, tasks):
    """
    完整的能力提取流程

    Args:
        workflow_description: 用户的工作流描述
        detected_patterns: 检测到的图模式
        category: 工作流分类
        tasks: 结构化任务列表

    Returns:
        提取的能力列表
    """
    all_capabilities = []

    # Step 1: 从模式提取编排能力
    pattern_caps = extract_pattern_capabilities(detected_patterns)
    all_capabilities.extend(pattern_caps)

    # Step 2: 从领域提取领域能力
    domain_caps = extract_domain_capabilities(workflow_description, category, tasks)
    all_capabilities.extend(domain_caps)

    # Step 3: 识别集成能力
    integration_caps = extract_integration_capabilities(workflow_description, tasks)
    all_capabilities.extend(integration_caps)

    # Step 4: 计算可复用性
    for cap in all_capabilities:
        cap['reusability'] = calculate_reusability(cap, workflow_description, category)

    # Step 5: 去重和优先级排序
    final_capabilities = prioritize_capabilities(all_capabilities)

    return final_capabilities
```

---

## 输出格式

```yaml
extracted_capabilities:
  - name: "deployment-orchestrator"
    category: "domain"
    description: "编排部署流程，协调多环境发布"
    source: "domain"
    confidence: 0.92
    reusability: 0.95
    evidence: ["deploy", "release", "rollout"]
    applicable_scenarios:
      - "multi-region deployment"
      - "blue-green deployment"
      - "canary release"
      - "rolling update"

  - name: "parallel-coordinator"
    category: "orchestration"
    description: "协调并行执行多个独立任务"
    source: "pattern"
    confidence: 0.88
    reusability: 0.98
    evidence: ["parallel pattern detected"]
    applicable_scenarios:
      - "parallel builds"
      - "concurrent tests"
      - "multi-region operations"

  - name: "health-monitor"
    category: "domain"
    description: "监控系统健康状态，执行验证检查"
    source: "domain"
    confidence: 0.85
    reusability: 0.90
    evidence: ["health", "verify", "check"]
    applicable_scenarios:
      - "deployment verification"
      - "service health checks"
      - "system monitoring"
```

---

## 使用示例

### 示例 1: 多区域部署工作流

**输入**:
```
工作流描述: "Deploy to three regions in parallel. For each region: deploy to staging,
verify health, if healthy deploy to production else rollback."
```

**提取结果**:
```yaml
capabilities:
  - deployment-orchestrator (confidence: 0.95, reusability: 0.95)
  - parallel-coordinator (confidence: 0.90, reusability: 0.98)
  - health-monitor (confidence: 0.88, reusability: 0.90)
  - conditional-router (confidence: 0.85, reusability: 0.95)
  - rollback-handler (confidence: 0.82, reusability: 0.88)
```

### 示例 2: 测试工作流

**输入**:
```
工作流描述: "Run linter, tests, and type checker in parallel, then generate report"
```

**提取结果**:
```yaml
capabilities:
  - parallel-coordinator (confidence: 0.92, reusability: 0.98)
  - test-coordinator (confidence: 0.88, reusability: 0.92)
  - sequential-coordinator (confidence: 0.75, reusability: 0.95)
```

---

## Claude 使用指南

**何时使用**: 在 Workflow Creation Protocol 的 Step 5A (新增步骤)

**输入**:
- 工作流描述
- 检测到的图模式
- 工作流分类
- 结构化任务列表

**执行步骤**:

1. **调用完整提取流程**:
   ```python
   capabilities = extract_all_capabilities(
       workflow_description=user_description,
       detected_patterns=patterns_from_step2,
       category=category_from_step5,
       tasks=tasks_from_step1
   )
   ```

2. **验证结果**:
   - 确保至少提取到1个能力
   - 检查可复用性评分 (应该 >= 0.6)
   - 验证置信度 (应该 >= 0.6)

3. **格式化输出**:
   ```yaml
   extracted_capabilities:
     - name: capability-name
       confidence: 0.XX
       reusability: 0.XX
       evidence: [keywords]
   ```

4. **传递给下一步**: 将提取的能力传递给 capability-library.md 进行库检查

**下一步**: 使用 `core/capability-library.md` 检查能力库，决定复用还是创建
