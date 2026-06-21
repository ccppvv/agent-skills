# Workflow Dependency Graph Builder

## Purpose
Construct Directed Acyclic Graph (DAG) representing task dependencies and execution order.

## Input Format
- Parsed tasks from analyzer
- Detected patterns from graph-detector
- Execution hints and conditions

## Core Concepts

### Directed Acyclic Graph (DAG)
A graph where:
- **Nodes**: Individual tasks or operations
- **Edges**: Dependencies (A → B means "B depends on A")
- **Acyclic**: No circular dependencies (A → B → C → A is invalid)

### Dependency Types

#### 1. Sequential (顺序依赖)
```
Task A → Task B → Task C
```
Task B cannot start until A completes; C waits for B.

#### 2. Parallel (并行依赖)
```
Task A ⎡→ Task B
        ⎢→ Task C
        ⎣→ Task D
```
B, C, D can all execute simultaneously after A completes.

#### 3. Converging (汇聚依赖)
```
Task A ⎤
Task B ⎥→ Task D
Task C ⎦
```
D requires all of A, B, C to complete before starting.

#### 4. Conditional (条件依赖)
```
Task A → [Condition]
           ├─ [True] → Task B
           └─ [False] → Task C
```
Execution path depends on condition evaluation.

#### 5. Cyclical (handled via Looping)
```
Task A → Task B → Task C
         ↑__________|
         (retry condition)
```
Implements retry/loop logic without creating true cycles in DAG.

## Construction Algorithm

### Phase 1: Node Creation
Create a node for each task:

```python
graph = {
    'nodes': [],
    'edges': [],
    'metadata': {}
}

for task in tasks:
    node = {
        'id': generate_id(task),
        'name': task.name,
        'type': task.type,
        'action': task.action,
        'dependencies': []
    }
    graph['nodes'].append(node)
```

### Phase 2: Edge Creation
Build edges based on dependency rules:

```python
for dep in dependencies:
    edge = {
        'from': dep.source_task_id,
        'to': dep.target_task_id,
        'type': dep.dependency_type,  # sequential/parallel/conditional
        'condition': dep.condition if dep.type == 'conditional'
    }
    graph['edges'].append(edge)
    graph['nodes'][dep.target_task_id]['dependencies'].append(dep.source_task_id)
```

### Phase 3: Cycle Detection
Ensure DAG property using DFS:

```python
def has_cycle(graph):
    visited = set()
    rec_stack = set()

    def dfs(node_id):
        visited.add(node_id)
        rec_stack.add(node_id)

        for neighbor in get_neighbors(node_id):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True  # Cycle detected!

        rec_stack.remove(node_id)
        return False

    for node in graph['nodes']:
        if node['id'] not in visited:
            if dfs(node['id']):
                raise CycleDetectedError("Cannot create workflow with circular dependencies")
```

**Handling Loops**: Convert to special loop nodes that don't create cycles:
```python
if pattern == 'looping':
    loop_node = {
        'id': 'loop_' + task_id,
        'type': 'loop_controller',
        'body': task_id,
        'condition': loop_condition,
        'max_iterations': max_iter
    }
    # Loop node doesn't create back-edge in DAG
```

### Phase 4: Topological Sorting
Determine valid execution order:

```python
def topological_sort(graph):
    in_degree = {node['id']: 0 for node in graph['nodes']}

    # Calculate in-degrees
    for edge in graph['edges']:
        in_degree[edge['to']] += 1

    # Start with nodes having no dependencies
    queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
    execution_order = []

    while queue:
        current = queue.pop(0)
        execution_order.append(current)

        # Reduce in-degree of neighbors
        for edge in graph['edges']:
            if edge['from'] == current:
                in_degree[edge['to']] -= 1
                if in_degree[edge['to']] == 0:
                    queue.append(edge['to'])

    return execution_order
```

## Dependency Analysis

### Identify Execution Levels
Group tasks by dependency level:

```python
levels = []
current_level = [node for node in nodes if not node.dependencies]

while current_level:
    levels.append(current_level)
    next_level = []

    for node in all_nodes:
        if all(dep in completed_nodes for dep in node.dependencies):
            if node not in completed_nodes and node not in current_level:
                next_level.append(node)

    completed_nodes.extend(current_level)
    current_level = next_level
```

**Example Output**:
```
Level 0: [initialize_config]
Level 1: [build_frontend, build_backend]  # Can run in parallel
Level 2: [run_tests]
Level 3: [deploy_staging]
Level 4: [health_check]
Level 5: [deploy_production]
```

### Critical Path Analysis
Identify longest path (determines minimum execution time):

```python
def find_critical_path(graph):
    # Calculate earliest start time for each node
    earliest_start = {node['id']: 0 for node in graph['nodes']}

    for node_id in topological_order:
        for edge in get_incoming_edges(node_id):
            earliest_start[node_id] = max(
                earliest_start[node_id],
                earliest_start[edge['from']] + get_task_duration(edge['from'])
            )

    # Backtrack to find critical path
    critical_path = []
    current = max(earliest_start, key=earliest_start.get)

    while current:
        critical_path.insert(0, current)
        current = get_critical_predecessor(current, earliest_start)

    return critical_path
```

## Output Format

### Text Description (for command description field)
```
Workflow Graph:
→ Initialize [node_1]
  ⎡→ BuildFrontend [node_2]
  ⎣→ BuildBackend [node_3]
→ RunTests [node_4] (depends on: node_2, node_3)
  ├─ [Pass] → DeployStaging [node_5]
  └─ [Fail] → NotifyFailure [node_6]
→ HealthCheck [node_7] (depends on: node_5)
  ├─ [Healthy] → DeployProduction [node_8]
  └─ [Unhealthy] → Rollback [node_9]
```

### Structured Data (for processing)
```yaml
graph:
  nodes:
    - id: "node_1"
      name: "Initialize"
      type: "node"
      level: 0
      dependencies: []

    - id: "node_2"
      name: "BuildFrontend"
      type: "node"
      level: 1
      dependencies: ["node_1"]

    - id: "node_3"
      name: "BuildBackend"
      type: "node"
      level: 1
      dependencies: ["node_1"]

    - id: "node_4"
      name: "RunTests"
      type: "node"
      level: 2
      dependencies: ["node_2", "node_3"]

  edges:
    - from: "node_1"
      to: "node_2"
      type: "sequential"

    - from: "node_1"
      to: "node_3"
      type: "sequential"

    - from: "node_2"
      to: "node_4"
      type: "converging"

    - from: "node_3"
      to: "node_4"
      type: "converging"

  execution_levels:
    - level: 0
      tasks: ["node_1"]
      parallelizable: false

    - level: 1
      tasks: ["node_2", "node_3"]
      parallelizable: true

    - level: 2
      tasks: ["node_4"]
      parallelizable: false

  critical_path: ["node_1", "node_2", "node_4", "node_5", "node_7", "node_8"]
```

## Error Handling

### Circular Dependency Detection
```
Error: Circular dependency detected
Path: TaskA → TaskB → TaskC → TaskA

Suggestion: Use looping pattern instead:
- TaskA → TaskB → TaskC
- If condition met, retry from TaskA (controlled loop)
```

### Missing Dependencies
```
Warning: TaskB references TaskX which doesn't exist
Suggestion: Add TaskX definition or remove dependency
```

### Orphaned Tasks
```
Warning: TaskC has no dependencies and no dependents
Suggestion: Connect to workflow or mark as independent async task
```

## Usage in Workflow Creation

```
Graph Detector Output
    ↓
Dependency Builder (construct DAG)
    ↓
Structured Dependency Graph
    ↓
Parallel Optimizer (identify optimization opportunities)
```

This structured graph is essential for:
- Determining valid execution orders
- Identifying parallelization opportunities
- Generating workflow description text
- Creating command logic

## How Claude Should Use This

**When to Use**: This is Step 3 in the Workflow Creation Protocol (see SKILL.md).

**Input**:
- Structured tasks from Step 1 (`core/analyzer.md`)
- Detected patterns from Step 2 (`core/graph-detector.md`)

**Execution Steps**:

1. **Create Nodes** (Phase 1):
   - For each task from analyzer output, create a node with unique ID
   - Include: id, name, type, action, dependencies (initially empty list)

2. **Create Edges** (Phase 2):
   - For each dependency relationship from analyzer output, create an edge
   - Classify edge type: sequential, parallel, conditional, converging
   - If conditional, include the condition expression

3. **Detect Cycles** (Phase 3):
   - Implement depth-first search (DFS) algorithm
   - Use visited set and recursion stack
   - **If cycle detected**:
     - Check if it's a legitimate loop pattern (retry/while/until)
     - If legitimate loop: Convert to loop controller node (no back-edge in DAG)
     - If illegitimate: Raise error with clear message showing the cycle path

4. **Topological Sort** (Phase 4):
   - Calculate in-degree for each node (number of incoming edges)
   - Start with nodes having in-degree 0 (no dependencies)
   - Process nodes level by level, reducing in-degrees
   - Output: Valid execution order

5. **Calculate Execution Levels**:
   - Group tasks by dependency depth
   - Level 0: No dependencies
   - Level 1: Depends only on Level 0
   - Level N: Depends on tasks in Levels 0 to N-1
   - Tasks at same level CAN be parallelized

6. **Identify Critical Path** (optional but recommended for complex workflows):
   - Calculate earliest start time for each node
   - Backtrack from final node to find longest path
   - Critical path determines minimum execution time

7. **Generate Text Visualization**:
   - Convert DAG to text-based graph description
   - Use symbols: → (sequential), ⎡⎢⎣ (parallel), ├─└─ (branch)
   - Format shown in "Text Description" section above

8. **Format Structured Output** using YAML from "Structured Data" section

**Example Execution**:

Input from Steps 1-2:
```yaml
tasks:
  - id: task_1
    action: "check"
    subject: "config"
  - id: task_2
    action: "run"
    subject: "frontend tests"
  - id: task_3
    action: "run"
    subject: "backend tests"
  - id: task_4
    action: "deploy"
    subject: "application"

dependencies:
  - from: task_1
    to: task_2
  - from: task_1
    to: task_3
  - from: task_2
    to: task_4
    type: "conditional"
  - from: task_3
    to: task_4
    type: "conditional"

detected_patterns:
  - pattern: "parallel"
  - pattern: "branch"
```

Your DAG construction:
```yaml
graph:
  nodes:
    - id: "task_1"
      name: "CheckConfig"
      level: 0
      dependencies: []
    - id: "task_2"
      name: "RunFrontendTests"
      level: 1
      dependencies: ["task_1"]
    - id: "task_3"
      name: "RunBackendTests"
      level: 1
      dependencies: ["task_1"]
    - id: "task_4"
      name: "DeployApplication"
      level: 2
      dependencies: ["task_2", "task_3"]

  edges:
    - from: "task_1"
      to: "task_2"
      type: "sequential"
    - from: "task_1"
      to: "task_3"
      type: "sequential"
    - from: "task_2"
      to: "task_4"
      type: "conditional"
      condition: "task_2 success"
    - from: "task_3"
      to: "task_4"
      type: "conditional"
      condition: "task_3 success"

  execution_levels:
    - level: 0
      tasks: ["task_1"]
      parallelizable: false
    - level: 1
      tasks: ["task_2", "task_3"]
      parallelizable: true
      note: "Frontend and backend tests can run in parallel"
    - level: 2
      tasks: ["task_4"]
      parallelizable: false

  topological_order: ["task_1", "task_2", "task_3", "task_4"]
  cycles_detected: false

  text_visualization: |
    Workflow Graph:
    → CheckConfig [task_1]
      ⎡→ RunFrontendTests [task_2]
      ⎣→ RunBackendTests [task_3]
    → DeployApplication [task_4] (depends on: task_2, task_3)
      ├─ [BothPass] → Deploy
      └─ [AnyFail] → Skip
```

**Error Handling**:

If you detect a cycle:
```yaml
error: "Circular dependency detected"
cycle_path: ["task_A", "task_B", "task_C", "task_A"]
suggestion: "Use looping pattern with explicit retry condition instead"
```

If you find orphaned tasks:
```yaml
warning: "Orphaned task detected"
task_id: "task_X"
suggestion: "Connect to workflow or mark as async independent task"
```

**Next Step**: Pass the constructed DAG (graph YAML) to `core/parallel-optimizer.md` for optimization analysis.
