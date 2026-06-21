# Capability Library Manager

## Purpose
管理已存在的能力 agent，避免重复创建。这是能力复用的核心模块。

## 设计原则

**复用优先原则**:
```yaml
检查流程:
  1. 精确匹配 → 覆盖度 >= 0.85 → 直接复用
  2. 精确匹配 → 覆盖度 < 0.85 → 评估是否扩展
  3. 模糊匹配 → 相似度 >= 0.8 → 评估是否复用
  4. 无匹配 → 评估可复用性 → 决定是否创建

创建决策:
  - 可复用性 >= 0.7 → 创建通用能力 agent
  - 可复用性 < 0.7 → 内联到 command，不创建 agent
```

---

## 能力库目录结构

```bash
~/.claude/agents/capabilities/
├── orchestration/              # 编排能力
│   ├── parallel-coordinator.md
│   ├── sequential-coordinator.md
│   ├── conditional-router.md
│   ├── async-executor.md
│   ├── retry-coordinator.md
│   └── state-manager.md
├── domain/                     # 领域能力
│   ├── deployment-orchestrator.md
│   ├── health-monitor.md
│   ├── rollback-handler.md
│   ├── test-coordinator.md
│   ├── batch-processor.md
│   ├── config-validator.md
│   ├── build-orchestrator.md
│   └── migration-coordinator.md
└── integration/                # 集成能力
    ├── api-integrator.md
    ├── service-connector.md
    ├── event-dispatcher.md
    ├── data-transformer.md
    └── notification-dispatcher.md
```

**目录说明**:
- `orchestration/`: 与执行模式相关的编排能力
- `domain/`: 与业务领域相关的专业能力
- `integration/`: 与系统集成相关的连接能力

---

## 能力库扫描

### 扫描算法

```python
def scan_capability_library():
    """
    扫描能力库，构建能力索引

    Returns:
        能力库字典 {capability_name: capability_data}
    """
    import os
    import yaml

    library = {}
    base_path = os.path.expanduser("~/.claude/agents/capabilities/")

    # 如果目录不存在，返回空库
    if not os.path.exists(base_path):
        return library

    # 扫描三个子目录
    for category in ['orchestration', 'domain', 'integration']:
        category_path = os.path.join(base_path, category)

        if not os.path.exists(category_path):
            continue

        # 扫描该分类下的所有 .md 文件
        for filename in os.listdir(category_path):
            if not filename.endswith('.md'):
                continue

            capability_name = filename.replace('.md', '')
            file_path = os.path.join(category_path, filename)

            # 解析能力文件
            capability_data = parse_capability_file(file_path)
            capability_data['path'] = file_path
            capability_data['category'] = category

            library[capability_name] = capability_data

    return library


def parse_capability_file(file_path):
    """
    解析能力 agent 文件，提取元数据和关键信息

    Args:
        file_path: 能力文件路径

    Returns:
        能力数据字典
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
        else:
            frontmatter = {}
    else:
        frontmatter = {}

    # 提取关键部分
    capability_data = {
        'name': frontmatter.get('name', ''),
        'type': frontmatter.get('type', 'capability'),
        'reusability': frontmatter.get('reusability', 0.0),
        'applicable_workflows': frontmatter.get('applicable_workflows', []),
        'description': frontmatter.get('description', ''),
        'focus_areas': extract_focus_areas(content),
        'key_actions': extract_key_actions(content),
        'triggers': extract_triggers(content)
    }

    return capability_data


def extract_focus_areas(content):
    """从内容中提取 Focus Areas"""
    focus_areas = []
    in_focus_section = False

    for line in content.split('\n'):
        if '## Focus Areas' in line:
            in_focus_section = True
            continue
        if in_focus_section:
            if line.startswith('##'):  # 新的章节开始
                break
            if line.startswith('- **'):
                # 提取 "- **Area Name**:" 格式
                area = line.split('**')[1] if '**' in line else ''
                if area:
                    focus_areas.append(area)

    return focus_areas


def extract_key_actions(content):
    """从内容中提取 Key Actions"""
    actions = []
    in_actions_section = False

    for line in content.split('\n'):
        if '## Key Actions' in line:
            in_actions_section = True
            continue
        if in_actions_section:
            if line.startswith('##'):
                break
            if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                # 提取 "1. **Action Name**:" 格式
                if '**' in line:
                    action = line.split('**')[1]
                    actions.append(action)

    return actions


def extract_triggers(content):
    """从内容中提取 Triggers"""
    triggers = []
    in_triggers_section = False

    for line in content.split('\n'):
        if '## Triggers' in line:
            in_triggers_section = True
            continue
        if in_triggers_section:
            if line.startswith('##'):
                break
            if line.startswith('- '):
                trigger = line[2:].strip()
                triggers.append(trigger)

    return triggers
```

---

## 能力匹配

### 精确匹配

```python
def exact_match(required_capability, library):
    """
    精确匹配：检查能力库中是否存在同名能力

    Args:
        required_capability: 需要的能力
        library: 能力库

    Returns:
        匹配结果 {exists: bool, capability: dict, coverage: float}
    """
    cap_name = required_capability['name']

    if cap_name in library:
        existing_cap = library[cap_name]
        coverage = calculate_coverage(required_capability, existing_cap)

        return {
            'exists': True,
            'capability': existing_cap,
            'coverage': coverage,
            'match_type': 'exact'
        }

    return {
        'exists': False,
        'capability': None,
        'coverage': 0.0,
        'match_type': 'none'
    }
```

### 模糊匹配

```python
def fuzzy_match(required_capability, library):
    """
    模糊匹配：查找相似的能力

    Args:
        required_capability: 需要的能力
        library: 能力库

    Returns:
        最相似的能力及相似度
    """
    from difflib import SequenceMatcher

    cap_name = required_capability['name']
    best_match = None
    best_similarity = 0.0

    for existing_name, existing_cap in library.items():
        # 计算名称相似度
        similarity = SequenceMatcher(None, cap_name, existing_name).ratio()

        # 如果描述相似，提高相似度
        if 'description' in required_capability and 'description' in existing_cap:
            desc_similarity = SequenceMatcher(
                None,
                required_capability['description'],
                existing_cap['description']
            ).ratio()
            similarity = similarity * 0.7 + desc_similarity * 0.3

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = existing_cap

    if best_similarity >= 0.8:
        return {
            'exists': True,
            'capability': best_match,
            'similarity': best_similarity,
            'match_type': 'fuzzy'
        }

    return {
        'exists': False,
        'capability': None,
        'similarity': 0.0,
        'match_type': 'none'
    }
```

### 覆盖度计算

```python
def calculate_coverage(required, existing):
    """
    计算现有能力对需求的覆盖度

    Args:
        required: 需要的能力
        existing: 现有的能力

    Returns:
        0.0-1.0 的覆盖度评分
    """
    coverage_scores = []

    # 1. Focus Areas 覆盖度 (40%)
    if 'focus_areas' in required and 'focus_areas' in existing:
        req_areas = set(required.get('focus_areas', []))
        exist_areas = set(existing.get('focus_areas', []))

        if req_areas:
            focus_coverage = len(req_areas & exist_areas) / len(req_areas)
        else:
            focus_coverage = 1.0  # 如果没有要求，认为完全覆盖

        coverage_scores.append(('focus', focus_coverage, 0.4))

    # 2. Key Actions 覆盖度 (40%)
    if 'key_actions' in required and 'key_actions' in existing:
        req_actions = set(required.get('key_actions', []))
        exist_actions = set(existing.get('key_actions', []))

        if req_actions:
            action_coverage = len(req_actions & exist_actions) / len(req_actions)
        else:
            action_coverage = 1.0

        coverage_scores.append(('actions', action_coverage, 0.4))

    # 3. 适用场景覆盖度 (20%)
    req_scenarios = required.get('applicable_scenarios', [])
    exist_workflows = existing.get('applicable_workflows', [])

    if req_scenarios and exist_workflows:
        # 检查是否有重叠的场景
        scenario_overlap = any(
            any(scenario.lower() in workflow.lower() or workflow.lower() in scenario.lower()
                for workflow in exist_workflows)
            for scenario in req_scenarios
        )
        scenario_coverage = 1.0 if scenario_overlap else 0.5
    else:
        scenario_coverage = 0.8  # 默认中等覆盖

    coverage_scores.append(('scenarios', scenario_coverage, 0.2))

    # 计算加权平均
    if coverage_scores:
        total_coverage = sum(score * weight for _, score, weight in coverage_scores)
    else:
        # 如果没有详细信息，基于名称和描述相似度
        total_coverage = 0.7  # 默认中等覆盖

    return round(total_coverage, 2)
```

---

## 完整匹配流程

```python
def match_capabilities(required_capabilities, library):
    """
    完整的能力匹配流程

    Args:
        required_capabilities: 需要的能力列表
        library: 能力库

    Returns:
        匹配结果 {existing, missing, partial}
    """
    results = {
        'existing': [],   # 可直接复用
        'missing': [],    # 需要创建
        'partial': []     # 部分匹配，需要评估
    }

    for req_cap in required_capabilities:
        # Step 1: 尝试精确匹配
        exact_result = exact_match(req_cap, library)

        if exact_result['exists']:
            if exact_result['coverage'] >= 0.85:
                # 高覆盖度，直接复用
                results['existing'].append({
                    'name': req_cap['name'],
                    'path': exact_result['capability']['path'],
                    'coverage': exact_result['coverage'],
                    'match_type': 'exact',
                    'action': 'reuse'
                })
            else:
                # 低覆盖度，标记为部分匹配
                results['partial'].append({
                    'name': req_cap['name'],
                    'path': exact_result['capability']['path'],
                    'coverage': exact_result['coverage'],
                    'match_type': 'exact',
                    'gaps': identify_gaps(req_cap, exact_result['capability']),
                    'action': 'extend_or_create'
                })
        else:
            # Step 2: 尝试模糊匹配
            fuzzy_result = fuzzy_match(req_cap, library)

            if fuzzy_result['exists'] and fuzzy_result['similarity'] >= 0.8:
                # 找到相似能力
                results['partial'].append({
                    'name': req_cap['name'],
                    'similar_to': fuzzy_result['capability']['name'],
                    'similarity': fuzzy_result['similarity'],
                    'match_type': 'fuzzy',
                    'action': 'evaluate_similarity'
                })
            else:
                # Step 3: 无匹配，标记为缺失
                results['missing'].append({
                    'name': req_cap['name'],
                    'confidence': req_cap['confidence'],
                    'reusability': req_cap['reusability'],
                    'category': req_cap['category'],
                    'action': 'create_if_reusable'
                })

    return results


def identify_gaps(required, existing):
    """
    识别现有能力与需求之间的差距

    Args:
        required: 需要的能力
        existing: 现有的能力

    Returns:
        差距列表
    """
    gaps = []

    # Focus areas 差距
    req_areas = set(required.get('focus_areas', []))
    exist_areas = set(existing.get('focus_areas', []))
    missing_areas = req_areas - exist_areas
    if missing_areas:
        gaps.append(f"Missing focus areas: {', '.join(missing_areas)}")

    # Key actions 差距
    req_actions = set(required.get('key_actions', []))
    exist_actions = set(existing.get('key_actions', []))
    missing_actions = req_actions - exist_actions
    if missing_actions:
        gaps.append(f"Missing actions: {', '.join(missing_actions)}")

    return gaps
```

---

## 创建决策

```python
def decide_creation(match_results):
    """
    基于匹配结果决定是否创建新能力

    Args:
        match_results: 匹配结果

    Returns:
        创建决策
    """
    decisions = {
        'reuse': [],      # 直接复用的能力
        'create': [],     # 需要创建的能力
        'inline': [],     # 内联到 command 的逻辑
        'extend': []      # 需要扩展的能力
    }

    # 处理已存在的能力
    for cap in match_results['existing']:
        decisions['reuse'].append({
            'name': cap['name'],
            'path': cap['path'],
            'coverage': cap['coverage'],
            'rationale': f"能力库中已存在，覆盖度 {cap['coverage']*100:.0f}%"
        })

    # 处理缺失的能力
    for cap in match_results['missing']:
        if cap['reusability'] >= 0.7:
            # 高可复用性，创建通用能力 agent
            decisions['create'].append({
                'name': cap['name'],
                'category': cap['category'],
                'reusability': cap['reusability'],
                'type': 'capability',
                'rationale': f"通用{cap['name']}能力缺失，可复用性 {cap['reusability']*100:.0f}%"
            })
        else:
            # 低可复用性，内联到 command
            decisions['inline'].append({
                'name': cap['name'],
                'reusability': cap['reusability'],
                'rationale': f"可复用性低 ({cap['reusability']*100:.0f}%)，建议内联到 command"
            })

    # 处理部分匹配的能力
    for cap in match_results['partial']:
        if cap.get('coverage', 0) >= 0.7:
            # 覆盖度中等，可以考虑扩展
            decisions['extend'].append({
                'name': cap['name'],
                'path': cap.get('path', ''),
                'coverage': cap.get('coverage', 0),
                'gaps': cap.get('gaps', []),
                'rationale': f"现有能力覆盖度 {cap.get('coverage', 0)*100:.0f}%，可考虑扩展"
            })
        else:
            # 覆盖度低，创建新能力
            decisions['create'].append({
                'name': cap['name'],
                'category': 'domain',  # 默认分类
                'type': 'capability',
                'rationale': f"现有能力覆盖度不足，创建新能力"
            })

    return decisions
```

---

## 输出格式

```yaml
library_check_results:
  # 可直接复用的能力
  existing:
    - name: "deployment-orchestrator"
      path: "~/.claude/agents/capabilities/domain/deployment-orchestrator.md"
      coverage: 0.95
      match_type: "exact"
      action: "reuse"

  # 需要创建的能力
  missing:
    - name: "health-monitor"
      confidence: 0.88
      reusability: 0.90
      category: "domain"
      action: "create_if_reusable"

  # 部分匹配的能力
  partial:
    - name: "custom-validator"
      similar_to: "config-validator"
      similarity: 0.82
      match_type: "fuzzy"
      action: "evaluate_similarity"

creation_decisions:
  # 直接复用
  reuse:
    - name: "deployment-orchestrator"
      path: "~/.claude/agents/capabilities/domain/deployment-orchestrator.md"
      coverage: 0.95
      rationale: "能力库中已存在，覆盖度 95%"

  # 创建新能力
  create:
    - name: "health-monitor"
      category: "domain"
      reusability: 0.90
      type: "capability"
      rationale: "通用健康监控能力缺失，可复用性 90%"

  # 内联到 command
  inline:
    - name: "custom-business-logic"
      reusability: 0.45
      rationale: "可复用性低 (45%)，建议内联到 command"

  # 扩展现有能力
  extend:
    - name: "advanced-validator"
      path: "~/.claude/agents/capabilities/domain/config-validator.md"
      coverage: 0.75
      gaps: ["complex validation rules", "custom business logic"]
      rationale: "现有能力覆盖度 75%，可考虑扩展"
```

---

## 使用示例

### 示例 1: 完全复用

**需求**:
```yaml
required_capabilities:
  - deployment-orchestrator (reusability: 0.95)
  - parallel-coordinator (reusability: 0.98)
```

**库检查结果**:
```yaml
decisions:
  reuse:
    - deployment-orchestrator (coverage: 0.95)
    - parallel-coordinator (coverage: 0.98)
  create: []
  inline: []
```

### 示例 2: 混合场景

**需求**:
```yaml
required_capabilities:
  - deployment-orchestrator (reusability: 0.95)  # 已存在
  - health-monitor (reusability: 0.90)           # 不存在，高可复用
  - custom-validation (reusability: 0.45)        # 不存在，低可复用
```

**库检查结果**:
```yaml
decisions:
  reuse:
    - deployment-orchestrator (coverage: 0.95)
  create:
    - health-monitor (reusability: 0.90)
  inline:
    - custom-validation (reusability: 0.45)
```

---

## Claude 使用指南

**何时使用**: 在 Workflow Creation Protocol 的 Step 5B (新增步骤)

**输入**:
- 从 capability-extractor.md 提取的能力列表

**执行步骤**:

1. **扫描能力库**:
   ```python
   library = scan_capability_library()
   ```

2. **匹配能力**:
   ```python
   match_results = match_capabilities(required_capabilities, library)
   ```

3. **决定创建策略**:
   ```python
   decisions = decide_creation(match_results)
   ```

4. **格式化输出**:
   ```yaml
   library_check:
     existing: [...]
     missing: [...]
     partial: [...]

   creation_decisions:
     reuse: [...]
     create: [...]
     inline: [...]
   ```

5. **传递给下一步**: 将创建决策传递给 decision-engine.md 的 Step 5C

**下一步**: 使用 `core/decision-engine.md` Step 5C 完成最终决策
