# Graph Patterns Quick Reference

Complete reference for all 9 workflow graph characteristics.

## Symbol Legend

```
→  Sequential flow
⎡⎢⎣ Parallel execution branches
├─ Conditional branch (if/then)
└─ Conditional branch (else)
⚡ Async (non-blocking)
↻  Loop/Retry
📦 Shared resource/state
⊕  Converging point (multiple inputs)
```

---

## 1. Node (单节点)

**Definition**: Single atomic operation.

**When to Use**:
- Simple, standalone tasks
- No special execution patterns needed
- One input, one output

**Example**:
```
→ CheckConfig [node_1]
```

**Natural Language Triggers**:
- "Check...", "Validate...", "Verify..."
- Single action verb
- No iteration or branching

---

## 2. Batch (批处理)

**Definition**: Same operation applied to multiple items.

**When to Use**:
- Processing collections/lists
- Uniform operation across items
- Can parallelize iterations

**Example**:
```
→ AddTypeAnnotations [batch_1]
  Items: [file1.py, file2.py, file3.py, ...]
  Parallel: 4 concurrent
```

**Natural Language Triggers**:
- "all files...", "each item...", "batch process..."
- "for every...", "for all..."
- Collection/plural nouns

---

## 3. Parallel (并行)

**Definition**: Independent tasks executing simultaneously.

**When to Use**:
- Tasks with no inter-dependencies
- Can run concurrently
- Optimization opportunity

**Example**:
```
⎡→ BuildFrontend [task_1]
⎢→ BuildBackend [task_2]
⎣→ BuildAPI [task_3]
```

**Natural Language Triggers**:
- "in parallel...", "at the same time..."
- "concurrently...", "simultaneously..."
- "both X and Y..."

---

## 4. Flow (流程)

**Definition**: Sequential data transformation pipeline.

**When to Use**:
- Data flows through stages
- Each stage transforms/processes
- Linear dependency chain

**Example**:
```
→ Extract [flow_1]
→ Transform [flow_2]
→ Load [flow_3]
```

**Natural Language Triggers**:
- "then...", "next...", "after that..."
- "pipeline...", "workflow..."
- Stage-based descriptions

---

## 5. Async (异步)

**Definition**: Background execution without blocking.

**When to Use**:
- Fire-and-forget operations
- Notifications, logging
- Main workflow doesn't wait

**Example**:
```
→ Deploy [main_1]
  ⚡ SendNotification [async_1] (non-blocking)
→ VerifyDeployment [main_2]
```

**Natural Language Triggers**:
- "in background...", "async..."
- "trigger and continue...", "non-blocking..."
- "fire and forget..."

---

## 6. Looping (循环)

**Definition**: Repeated execution until condition met.

**When to Use**:
- Retry logic
- Polling/waiting
- Iterative processing

**Example**:
```
→ Deploy [loop_1]
  ↻ HealthCheck [loop_2]
    Condition: retry up to 3 times if unhealthy
    Wait: 5 seconds between attempts
```

**Natural Language Triggers**:
- "retry...", "repeat...", "until..."
- "while...", "keep trying..."
- "up to N times..."

---

## 7. Branch (分支)

**Definition**: Conditional execution paths.

**When to Use**:
- Decision points
- Different actions based on conditions
- If/else logic

**Example**:
```
→ RunTests [branch_1]
  ├─ [Pass] → Deploy [branch_2a]
  └─ [Fail] → Rollback [branch_2b]
```

**Natural Language Triggers**:
- "if...", "when...", "based on..."
- "depending on...", "in case of..."
- "success/failure...", "pass/fail..."

---

## 8. Nesting (嵌套)

**Definition**: Workflows within workflows.

**When to Use**:
- Sub-processes
- Hierarchical workflows
- Reusable workflow components

**Example**:
```
→ ForEachMicroservice [nest_1]
  └→ ExecuteCICD [nest_2]
      → Build [nest_2a]
      → Test [nest_2b]
      → Deploy [nest_2c]
```

**Natural Language Triggers**:
- "for each...", "for all..."
- "execute workflow...", "run pipeline..."
- "within...", "as part of..."

---

## 9. Shared (共享资源)

**Definition**: Multiple tasks accessing shared state/resources.

**When to Use**:
- Coordinated access needed
- Shared configuration/state
- Resource synchronization

**Example**:
```
⎡→ RegionA Deploy [shared_1a]
⎢→ RegionB Deploy [shared_1b]
⎣→ RegionC Deploy [shared_1c]
    ↓
📦 SharedStatus { all_regions_status }
    ↓
→ GlobalHealthCheck [shared_2]
```

**Natural Language Triggers**:
- "shared...", "global...", "coordinated..."
- "synchronized...", "centralized..."
- "update shared status..."

---

## Pattern Combinations

Real workflows often combine multiple patterns:

### Example: Parallel + Branch + Async
```
⎡→ FrontendTests [combo_1a]
⎢  ⚡ SendProgressUpdate (async)
⎣→ BackendTests [combo_1b]
    ↓
→ AggregateResults [combo_2]
  ├─ [AllPass] → Deploy [combo_3a]
  │  ⚡ NotifySuccess (async)
  └─ [AnyFail] → Alert [combo_3b]
     ⚡ NotifyFailure (async)
```

### Example: Flow + Looping + Shared
```
→ Initialize [combo2_1]
📦 SharedConfig { deployment_settings }
    ↓
→ Deploy [combo2_2]
  ↻ Verify [combo2_3]
    Retry: 3 times
    Uses: SharedConfig
    ↓
→ UpdateSharedStatus [combo2_4]
→ Finalize [combo2_5]
```

---

## Pattern Selection Decision Tree

```
Does it repeat?
├─ Yes → Looping or Batch
│  └─ Same op on multiple items? → Batch
│      Different condition? → Looping
│
└─ No → Continue

Does it branch?
├─ Yes → Branch
│  └─ Also parallel? → Branch + Parallel
│
└─ No → Continue

Can tasks run simultaneously?
├─ Yes → Parallel
│  └─ Share resources? → Parallel + Shared
│
└─ No → Continue

Does it have sub-workflows?
├─ Yes → Nesting
│
└─ No → Continue

Is it non-blocking?
├─ Yes → Async
│
└─ No → Continue

Is it a pipeline?
├─ Yes → Flow
│
└─ No → Node (simple task)
```

---

## Complexity Scoring by Pattern

| Pattern | Base Complexity | Notes |
|---------|-----------------|-------|
| Node | 0.1 | Simple atomic task |
| Batch | 0.3 | Adds iteration |
| Parallel | 0.4 | Coordination needed |
| Flow | 0.3 | Linear but multi-step |
| Async | 0.2 | Background execution |
| Looping | 0.5 | Retry logic complexity |
| Branch | 0.4 | Conditional logic |
| Nesting | 0.6 | Sub-workflow complexity |
| Shared | 0.5 | Synchronization needed |

**Combined patterns**: Add scores, cap at 1.0

**Example**:
- Parallel (0.4) + Branch (0.4) + Async (0.2) = 1.0 → "high" complexity

---

## Best Practices

### Do:
- ✅ Use clear, descriptive task names
- ✅ Document shared resources explicitly
- ✅ Show retry/loop conditions
- ✅ Indicate parallel execution opportunities
- ✅ Mark async tasks clearly

### Don't:
- ❌ Create circular dependencies (use Looping pattern instead)
- ❌ Over-parallelize (consider resource limits)
- ❌ Nest too deeply (>3 levels)
- ❌ Skip error handling in complex flows
- ❌ Ignore shared resource conflicts

---

## Quick Pattern Matching

Input: "Check config, then run tests in parallel for frontend and backend, deploy if both pass"

Analysis:
1. "Check config" → **Node**
2. "run tests in parallel for frontend and backend" → **Parallel**
3. "deploy if both pass" → **Branch**

Result: **Flow + Parallel + Branch** combination
