---
name: parallel-quality-check
description: "Run linter, tests, and type checker in parallel. Graph: ⎡→ Lint ⎢→ Test ⎣→ TypeCheck → Aggregate"
category: testing
complexity: standard
mcp-servers: [playwright]
personas: [qa-specialist, backend-developer]
---

# /parallel-quality-check - Parallel Quality Assurance

> **Workflow Description**: Execute multiple quality checks simultaneously for maximum speed

**Detected Patterns**: parallel

## Workflow Graph

```
⎡→ RunLinter [task_1]
⎢→ RunTests [task_2]
⎣→ TypeCheck [task_3]
    ↓
→ AggregateResults [task_4]
```

## Behavioral Flow

1. **Parallel Execution** (3 tasks simultaneously)
   - Run linter on all source files
   - Execute full test suite
   - Perform type checking
   - All three run concurrently

2. **Aggregate Results**
   - Collect results from all checks
   - Report combined status
   - Fail if any check fails

## MCP Integration

- **playwright MCP**: Automated test execution and validation

## Usage Examples

```bash
/parallel-quality-check

# Runs 3 checks in parallel
# Sequential time: ~90s → Parallel time: ~30s (3x speedup)
```

## Boundaries

**Will:**
- Execute all quality checks in parallel
- Report comprehensive results
- Fail fast if any check fails

**Will Not:**
- Skip any quality check
- Proceed with failures
- Modify code automatically
