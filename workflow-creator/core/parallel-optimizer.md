# Workflow Parallel Optimization Analyzer

## Purpose
Identify opportunities for parallel execution to optimize workflow performance.

## Input Format
- Dependency graph (DAG) from dependency-builder
- Execution levels from topological sort
- Task duration estimates (if available)

## Parallel Execution Principles

### When Tasks Can Run in Parallel
Tasks can execute simultaneously if:
1. **No dependencies** between them
2. **Shared resources** don't conflict
3. **Same execution level** in dependency graph
4. **Independent data** (no read-after-write conflicts)

### When Tasks Must Be Sequential
Tasks must run sequentially if:
1. **Direct dependency** exists (A must complete before B starts)
2. **Resource conflict** (both need exclusive access to same resource)
3. **Data dependency** (B needs A's output)
4. **Ordering constraint** explicitly specified

## Analysis Process

### Step 1: Level-Based Parallelization
Identify tasks at same dependency level:

```python
def find_parallel_opportunities(execution_levels):
    opportunities = []

    for level_index, level in enumerate(execution_levels):
        if len(level['tasks']) > 1:
            opportunity = {
                'level': level_index,
                'parallelizable_tasks': level['tasks'],
                'count': len(level['tasks']),
                'pattern': 'level_based'
            }
            opportunities.append(opportunity)

    return opportunities
```

**Example**:
```
Level 1: [build_frontend, build_backend, build_api]
→ All 3 can run in parallel (no dependencies between them)
```

### Step 2: Independent Subgraph Detection
Find disconnected subgraphs that can run independently:

```python
def find_independent_subgraphs(graph):
    visited = set()
    subgraphs = []

    def dfs(node_id, current_subgraph):
        visited.add(node_id)
        current_subgraph.add(node_id)

        for neighbor in get_all_neighbors(node_id):  # Both incoming and outgoing
            if neighbor not in visited:
                dfs(neighbor, current_subgraph)

    for node in graph['nodes']:
        if node['id'] not in visited:
            subgraph = set()
            dfs(node['id'], subgraph)
            subgraphs.append(subgraph)

    return [sg for sg in subgraphs if len(sg) > 0]
```

**Example**:
```
Subgraph A: config_check → validate_config
Subgraph B: database_backup → verify_backup
→ Both subgraphs can run in parallel
```

### Step 3: Async Task Identification
Identify tasks that can run asynchronously:

```python
def identify_async_tasks(graph):
    async_candidates = []

    for node in graph['nodes']:
        # Check if no downstream tasks depend on this node's result
        if not has_data_consumers(node):
            # Check if task is fire-and-forget (e.g., notifications, logging)
            if is_fire_and_forget(node):
                async_candidates.append({
                    'task': node['id'],
                    'reason': 'no_data_consumers',
                    'pattern': 'async'
                })

    return async_candidates
```

**Example**:
```
Main workflow: Build → Test → Deploy
Async task: SendNotification (can run in background)
```

### Step 4: Batch Parallelization
Identify batch operations that can parallelize iterations:

```python
def analyze_batch_parallelization(batch_tasks):
    parallel_batches = []

    for batch_task in batch_tasks:
        if can_parallelize_items(batch_task):
            parallel_batches.append({
                'task': batch_task['id'],
                'items': batch_task['iteration_target'],
                'parallelism': estimate_parallelism(batch_task),
                'pattern': 'batch_parallel'
            })

    return parallel_batches
```

**Example**:
```
Sequential: Process file1 → file2 → file3 → file4
Parallel: Process [file1, file2, file3, file4] simultaneously
```

## Parallelization Strategies

### Strategy 1: Task-Level Parallelism
Execute independent tasks simultaneously:

```yaml
strategy: task_level
execution:
  - parallel_group:
      - task: build_frontend
      - task: build_backend
      - task: build_api
```

### Strategy 2: Data-Level Parallelism
Partition data and process chunks in parallel:

```yaml
strategy: data_level
execution:
  - task: process_files
    parallelism: 4  # Process 4 files at a time
    items: [file1, file2, ..., file100]
```

### Strategy 3: Pipeline Parallelism
Overlap stages of pipeline:

```yaml
strategy: pipeline
execution:
  - stage_1: read_data
  - stage_2: transform_data  # Starts when stage_1 produces first chunk
  - stage_3: write_data      # Starts when stage_2 produces first result
```

### Strategy 4: Hybrid Parallelism
Combine multiple strategies:

```yaml
strategy: hybrid
execution:
  - parallel_group:
      - pipeline:
          - stage: extract
          - stage: transform
          - stage: load
      - batch_parallel:
          - task: process_reports
            parallelism: 3
```

## Performance Estimation

### Speedup Calculation
Estimate performance improvement:

```python
def calculate_speedup(sequential_time, parallel_opportunities):
    # Amdahl's Law: Speedup = 1 / (S + P/N)
    # S = fraction that must be sequential
    # P = fraction that can be parallel
    # N = number of processors

    total_time = sequential_time
    parallelizable_time = sum(opp['duration'] for opp in parallel_opportunities)
    sequential_only_time = total_time - parallelizable_time

    S = sequential_only_time / total_time
    P = parallelizable_time / total_time
    N = estimate_available_parallelism()

    speedup = 1 / (S + P / N)
    return speedup
```

### Resource Utilization
Assess resource requirements:

```python
def estimate_resource_needs(parallel_plan):
    max_concurrent_tasks = 0

    for level in parallel_plan['execution_levels']:
        concurrent_count = len(level['tasks'])
        max_concurrent_tasks = max(max_concurrent_tasks, concurrent_count)

    return {
        'max_concurrent_tasks': max_concurrent_tasks,
        'memory_estimate': max_concurrent_tasks * avg_task_memory,
        'cpu_estimate': max_concurrent_tasks * avg_task_cpu,
        'recommendation': suggest_parallelism_level(max_concurrent_tasks)
    }
```

## Optimization Recommendations

### Conservative (Safe Parallelism)
```yaml
approach: conservative
recommendation:
  - parallelize: only_explicit_parallel_hints
  - max_concurrent: 2
  - rationale: "Minimize resource contention, easier debugging"
```

### Balanced (Recommended)
```yaml
approach: balanced
recommendation:
  - parallelize: same_level_tasks
  - max_concurrent: 4
  - rationale: "Good performance improvement with manageable complexity"
```

### Aggressive (Maximum Performance)
```yaml
approach: aggressive
recommendation:
  - parallelize: all_independent_tasks
  - max_concurrent: 8+
  - rationale: "Maximum speedup, requires more resources and monitoring"
```

## Output Format

### Optimization Report
```yaml
parallelization_analysis:
  opportunities:
    - type: "level_based"
      level: 1
      tasks: ["build_frontend", "build_backend", "build_api"]
      potential_speedup: "3x (if fully parallel)"
      recommendation: "Execute in parallel"

    - type: "batch_parallel"
      task: "process_user_files"
      items_count: 50
      suggested_parallelism: 5
      potential_speedup: "5x"
      recommendation: "Parallel batch processing"

    - type: "async"
      task: "send_notifications"
      blocking: false
      potential_time_saved: "2 seconds"
      recommendation: "Execute asynchronously"

  overall_assessment:
    sequential_time_estimate: "120 seconds"
    parallel_time_estimate: "45 seconds"
    speedup: "2.67x"
    complexity_increase: "moderate"
    recommended_approach: "balanced"

  execution_plan:
    levels:
      - level: 0
        tasks: ["initialize"]
        execution: "sequential"

      - level: 1
        tasks: ["build_frontend", "build_backend", "build_api"]
        execution: "parallel"
        max_concurrent: 3

      - level: 2
        tasks: ["run_tests"]
        execution: "sequential"

      - level: 3
        tasks: ["deploy_staging"]
        execution: "sequential"

      - level: 4
        tasks: ["health_check"]
        execution: "sequential"
        async_tasks: ["send_notifications"]

  warnings:
    - "Parallel execution requires 3x memory at level 1"
    - "Ensure shared resources (database) can handle concurrent access"
```

### Workflow Description Update
Add parallelization info to text description:

```
Workflow Graph (Optimized for Parallel Execution):
→ Initialize [node_1]
  ⎡→ BuildFrontend [node_2]  ┐
  ⎢→ BuildBackend [node_3]   ├─ Parallel Execution (3 tasks)
  ⎣→ BuildAPI [node_4]       ┘
→ RunTests [node_5] (depends on: all builds)
  ⚡ SendNotifications (async, non-blocking)
→ DeployStaging [node_6]
→ HealthCheck [node_7]
  ├─ [Healthy] → DeployProduction [node_8]
  └─ [Unhealthy] → Rollback [node_9]

Parallelization: 2.67x speedup (120s → 45s)
Max Concurrency: 3 tasks
```

## Integration with Command Generation

Parallelization insights influence:
- **MCP server selection**: Parallel workflows may need additional coordination tools
- **Complexity rating**: More parallelism = higher complexity
- **Implementation code**: Generate appropriate parallel execution logic
- **Resource requirements**: Document in command description

## Usage in Workflow Creation

```
Dependency Builder Output
    ↓
Parallel Optimizer (identify opportunities)
    ↓
Optimized Execution Plan
    ↓
Decision Engine (select tools and personas)
```

This optimization analysis is critical for generating efficient, high-performance workflows.

## How Claude Should Use This

**When to Use**: This is Step 4 in the Workflow Creation Protocol (see SKILL.md).

**Input**: DAG from Step 3 (`core/dependency-builder.md`) with execution levels

**Execution Steps**:

1. **Identify Independent Tasks**: For each execution level, find tasks with no inter-dependencies
2. **Estimate Speedup**: Use Amdahl's Law formula:
   ```
   Speedup = 1 / ((1 - P) + P/N)
   where P = parallelizable fraction, N = number of parallel tasks
   ```
3. **Assess Resource Usage**: Estimate CPU, memory, I/O requirements for parallel execution
4. **Recommend Strategy**:
   - Conservative: 2-3 parallel tasks, low resource overhead
   - Balanced: 3-5 parallel tasks, moderate resources (default)
   - Aggressive: 5+ parallel tasks, high throughput
5. **Generate Recommendations**: Specify which tasks to parallelize and how

**Example Execution**:

Input DAG:
```yaml
execution_levels:
  - level: 1
    tasks: ["build_frontend", "build_backend", "build_api"]
    parallelizable: true
```

Your analysis:
```yaml
parallelization:
  opportunities:
    - level: 1
      tasks: ["build_frontend", "build_backend", "build_api"]
      estimated_speedup: 2.8x
      resource_utilization: "moderate"
  strategy: "balanced"
  recommendation: "Execute 3 build tasks in parallel using Task tool with 3 parallel calls"
```

**Next Step**: Pass all analysis results to `core/decision-engine.md` for metadata decisions.
