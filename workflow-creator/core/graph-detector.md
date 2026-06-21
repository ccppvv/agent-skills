# Workflow Graph Pattern Detector

## Purpose
Identify graph characteristics in parsed workflow structures to determine execution patterns.

## Input Format
Structured task data from analyzer module:
```yaml
tasks: [...]
dependencies: [...]
execution_hints: [...]
conditions: [...]
```

## Graph Characteristics

### 1. Node (单节点)
**Definition**: Single atomic operation with no special execution pattern.

**Detection Criteria**:
- Single task with simple dependencies
- No iteration, parallelism, or branching
- Straightforward input → output transformation

**Markers**:
```yaml
pattern: node
indicators:
  - task_count: 1
  - dependency_type: "simple"
  - execution: "sequential"
```

**Example**: "Check system health status"

---

### 2. Batch (批处理)
**Definition**: Process multiple items of the same type with same operation.

**Detection Criteria**:
- Keywords: "all", "batch", "bulk", "each", "every"
- Iteration over collection
- Same operation applied to multiple items

**Markers**:
```yaml
pattern: batch
indicators:
  - iteration_present: true
  - collection_target: true
  - uniform_operation: true
```

**Example**: "Add type annotations to all Python files"

---

### 3. Parallel (并行)
**Definition**: Independent tasks execute simultaneously without dependencies.

**Detection Criteria**:
- Keywords: "parallel", "concurrent", "simultaneously", "at the same time"
- Multiple tasks with no inter-dependencies
- Can be executed in any order

**Markers**:
```yaml
pattern: parallel
indicators:
  - parallel_hint: true
  - no_dependencies: true
  - independent_tasks: true
```

**Example**: "Run frontend tests and backend tests in parallel"

---

### 4. Flow (流程)
**Definition**: Sequential data transformation pipeline with clear flow.

**Detection Criteria**:
- Linear dependency chain
- Data flows from one stage to next
- Each stage transforms or processes data

**Markers**:
```yaml
pattern: flow
indicators:
  - dependency_chain: "linear"
  - data_transformation: true
  - sequential: true
```

**Example**: "Update dependencies → Run tests → Build package → Publish"

---

### 5. Async (异步)
**Definition**: Background execution without blocking main workflow.

**Detection Criteria**:
- Keywords: "async", "background", "non-blocking", "fire and forget"
- Task can complete independently
- Main workflow doesn't wait for result

**Markers**:
```yaml
pattern: async
indicators:
  - async_keyword: true
  - non_blocking: true
  - independent_completion: true
```

**Example**: "Run integration tests in background"

---

### 6. Looping (循环)
**Definition**: Repeated execution until condition met or iteration complete.

**Detection Criteria**:
- Keywords: "retry", "until", "while", "repeat"
- Condition-based repetition
- Feedback loop present

**Markers**:
```yaml
pattern: looping
indicators:
  - loop_keyword: true
  - condition_present: true
  - retry_logic: true
```

**Example**: "Retry deployment up to 3 times if health check fails"

---

### 7. Branch (分支)
**Definition**: Conditional execution based on decision points.

**Detection Criteria**:
- Keywords: "if", "when", "based on", "depending on"
- Multiple execution paths
- Condition determines which path

**Markers**:
```yaml
pattern: branch
indicators:
  - conditional: true
  - multiple_paths: true
  - decision_point: true
```

**Example**: "If tests pass deploy to production, else rollback"

---

### 8. Nesting (嵌套)
**Definition**: Workflow contains sub-workflows or nested execution contexts.

**Detection Criteria**:
- Sub-workflow references
- Keywords: "within", "as part of", "execute workflow"
- Hierarchical structure

**Markers**:
```yaml
pattern: nesting
indicators:
  - sub_workflow_present: true
  - hierarchical: true
  - nested_context: true
```

**Example**: "Execute full CI/CD pipeline (build → test → deploy) for each microservice"

---

### 9. Shared (共享资源)
**Definition**: Multiple tasks access or modify shared state/resources.

**Detection Criteria**:
- Keywords: "shared", "global", "coordinated", "synchronized"
- Multiple tasks referencing same resource
- Requires coordination or locking

**Markers**:
```yaml
pattern: shared
indicators:
  - shared_resource: true
  - coordination_needed: true
  - state_synchronization: true
```

**Example**: "Update shared deployment status after each region deployment"

---

## Detection Algorithm

### Phase 1: Single Pattern Detection
For each task structure, check all 9 patterns in parallel:

```python
detected_patterns = []

for pattern in [node, batch, parallel, flow, async, looping, branch, nesting, shared]:
    score = calculate_pattern_score(workflow, pattern)
    if score > threshold:
        detected_patterns.append({
            'pattern': pattern,
            'confidence': score,
            'evidence': extract_evidence(workflow, pattern)
        })
```

### Phase 2: Pattern Combination
Identify complex workflows using multiple patterns:

```python
if len(detected_patterns) > 1:
    combined_pattern = {
        'primary': highest_score_pattern,
        'secondary': other_patterns,
        'complexity': calculate_complexity(detected_patterns)
    }
```

### Scoring Formula

```python
score = (
    keyword_match_weight * keyword_score +
    structure_match_weight * structure_score +
    dependency_match_weight * dependency_score +
    semantic_match_weight * semantic_score
)
```

**Weights**:
- keyword_match: 0.3
- structure_match: 0.35
- dependency_match: 0.25
- semantic_match: 0.1

**Threshold**: 0.6 (patterns with score >= 0.6 are considered detected)

## Output Format

```yaml
detected_patterns:
  - pattern: "parallel"
    confidence: 0.85
    evidence:
      - "keyword: 'in parallel'"
      - "independent tasks: frontend_test, backend_test"
      - "no inter-dependencies"

  - pattern: "branch"
    confidence: 0.75
    evidence:
      - "conditional: 'if tests pass'"
      - "multiple paths: deploy / rollback"

combined_assessment:
  primary_pattern: "parallel"
  secondary_patterns: ["branch"]
  complexity: "standard"
  recommendation: "Use parallel execution with conditional branching"
```

## Usage in Workflow Creation

```
Analyzer Output
    ↓
Graph Detector (identify patterns)
    ↓
Pattern List with Confidence Scores
    ↓
Dependency Builder (construct execution graph)
```

The detected patterns guide the generation of appropriate command structures and execution logic.

## How Claude Should Use This

**When to Use**: This is Step 2 in the Workflow Creation Protocol (see SKILL.md).

**Input**: Structured YAML output from `core/analyzer.md` (Step 1)

**Execution Steps**:

1. **Read the structured task data** from Step 1 (tasks, dependencies, execution_hints, conditions)

2. **For each of the 9 patterns**, calculate confidence score using the scoring formula:
   ```
   score = (
     keyword_match × 0.3 +
     structure_match × 0.35 +
     dependency_match × 0.25 +
     semantic_match × 0.1
   )
   ```

3. **Calculate individual components** for each pattern:
   - **keyword_match**: Check for pattern-specific keywords in the original user input
     - Node: simple, single-action keywords
     - Batch: "all", "each", "batch", "bulk"
     - Parallel: "parallel", "concurrent", "simultaneously"
     - Flow: sequential connectors "then", "next", "after"
     - Async: "async", "background", "non-blocking"
     - Looping: "retry", "until", "while", "repeat"
     - Branch: "if", "when", "based on", "else"
     - Nesting: "within", "as part of", "sub-workflow"
     - Shared: "shared", "global", "coordinated"

   - **structure_match**: Analyze task structure
     - Count of tasks, dependency relationships, execution flow

   - **dependency_match**: Examine dependency graph
     - Linear chains (Flow), no dependencies (Parallel), conditional dependencies (Branch)

   - **semantic_match**: Overall semantic fit with pattern definition

4. **Filter patterns** with confidence ≥ 0.6

5. **Identify pattern combinations** if multiple patterns detected

6. **Extract evidence** for each detected pattern (keywords found, structural features)

7. **Format output** using the YAML structure from "Output Format" section

**Example Execution**:

Input from Step 1:
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

execution_hints:
  - task_id: task_2
    hint: "parallel_with_task_3"
```

Your pattern detection:
```yaml
detected_patterns:
  - pattern: "parallel"
    confidence: 0.85
    evidence:
      - "keyword: 'in parallel' from user input"
      - "execution_hint: parallel_with_task_3"
      - "independent tasks: task_2, task_3"
      - "structure: 2 tasks at same dependency level"

  - pattern: "branch"
    confidence: 0.72
    evidence:
      - "keyword: 'if both pass' from user input"
      - "conditional dependency: task_4 depends on task_2 AND task_3"
      - "decision_point: success/failure branches"

  - pattern: "flow"
    confidence: 0.65
    evidence:
      - "keyword: 'then' from user input"
      - "sequential: task_1 → tasks_2/3 → task_4"
      - "linear chain present"

combined_assessment:
  primary_pattern: "parallel"
  secondary_patterns: ["branch", "flow"]
  complexity: "standard"
  recommendation: "Parallel execution with conditional branching in sequential flow"
```

**Decision Making**:
- If **no patterns** detected (all scores < 0.6): Default to "node" pattern
- If **1 pattern** detected: Single-pattern workflow
- If **2-3 patterns** detected: Combined pattern workflow (common)
- If **4+ patterns** detected: Highly complex workflow, recommend splitting

**Next Step**: Pass detected patterns + original structured tasks to `core/dependency-builder.md` for DAG construction.
