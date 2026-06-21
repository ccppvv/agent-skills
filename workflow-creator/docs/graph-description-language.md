# Workflow Graph Description Language (WGDL)

## Purpose

Standardized text-based language for describing workflow execution graphs in command descriptions. This ensures consistency, parseability, and clarity across all generated workflow commands.

## Design Principles

1. **Human-Readable**: Clear and intuitive for users reading command descriptions
2. **Machine-Parseable**: Structured format that can be validated programmatically
3. **Compact**: Efficient use of space in YAML frontmatter
4. **Unambiguous**: One-to-one mapping between text and graph topology
5. **Extensible**: Can represent all 9 graph patterns and their combinations

## Formal Grammar

### Core Syntax

```ebnf
workflow_graph ::= "Workflow Graph:" newline node_sequence

node_sequence ::= node (newline node)*

node ::= indent_level symbol node_name node_id dependencies? condition?

indent_level ::= ("→" | "  " | "│" | "├─" | "└─" | "⎡" | "⎢" | "⎣")+

symbol ::= "→" | "⎡→" | "⎢→" | "⎣→" | "⚡" | "↻" | "📦" | "├─" | "└─"

node_name ::= [A-Z][a-zA-Z0-9_]*

node_id ::= "[" identifier "]"

dependencies ::= "(depends on: " identifier_list ")"

condition ::= branch_condition | loop_condition

branch_condition ::= "├─ [" condition_expr "]" | "└─ [" condition_expr "]"

loop_condition ::= "(retry " number "x)" | "(until " condition_expr ")"
```

### Symbol Reference

| Symbol | Meaning | Usage | Example |
|--------|---------|-------|---------|
| `→` | Sequential | Single sequential step | `→ BuildApp [node_1]` |
| `⎡→` | Parallel Start | First parallel task | `⎡→ TestFrontend [node_2]` |
| `⎢→` | Parallel Middle | Middle parallel task | `⎢→ TestBackend [node_3]` |
| `⎣→` | Parallel End | Last parallel task | `⎣→ TestAPI [node_4]` |
| `├─` | Branch True | Conditional true path | `├─ [Pass] → Deploy [node_5]` |
| `└─` | Branch False | Conditional false path | `└─ [Fail] → Rollback [node_6]` |
| `⚡` | Async | Background execution | `⚡ SendNotification [node_7]` |
| `↻` | Loop | Retry/repeat | `↻ HealthCheck [node_8] (retry 3x)` |
| `📦` | Shared | Shared resource access | `📦 UpdateStatus [node_9]` |

### Indentation Rules

1. **Base Level**: Root nodes start with `→`
2. **Parallel Group**: Use `⎡⎢⎣` alignment
3. **Nested Branch**: Indent with `│` for branch body
4. **Sub-workflow**: Indent entire nested workflow

## Standard Patterns

### Pattern 1: Single Node
```
Workflow Graph:
→ ExecuteTask [node_1]
```

### Pattern 2: Sequential Flow
```
Workflow Graph:
→ Initialize [node_1]
→ Process [node_2]
→ Finalize [node_3]
```

### Pattern 3: Parallel Execution
```
Workflow Graph:
→ Setup [node_1]
  ⎡→ TaskA [node_2]
  ⎢→ TaskB [node_3]
  ⎣→ TaskC [node_4]
→ Cleanup [node_5] (depends on: node_2, node_3, node_4)
```

### Pattern 4: Conditional Branch
```
Workflow Graph:
→ RunTests [node_1]
  ├─ [Pass] → Deploy [node_2]
  └─ [Fail] → Rollback [node_3]
```

### Pattern 5: Nested Branch
```
Workflow Graph:
→ CheckConfig [node_1]
  ├─ [Valid] → Deploy [node_2]
  │  ├─ [Success] → Notify [node_3]
  │  └─ [Failed] → Alert [node_4]
  └─ [Invalid] → Fix [node_5]
```

### Pattern 6: Parallel with Branch
```
Workflow Graph:
→ Prepare [node_1]
  ⎡→ BuildFrontend [node_2]
  ⎢→ BuildBackend [node_3]
  ⎣→ BuildAPI [node_4]
→ Test [node_5] (depends on: node_2, node_3, node_4)
  ├─ [Pass] → DeployStaging [node_6]
  └─ [Fail] → NotifyTeam [node_7]
```

### Pattern 7: Async Execution
```
Workflow Graph:
→ Deploy [node_1]
⚡ SendMetrics [node_2]
⚡ UpdateDashboard [node_3]
→ VerifyDeployment [node_4]
```

### Pattern 8: Loop/Retry
```
Workflow Graph:
→ Deploy [node_1]
↻ HealthCheck [node_2] (retry 3x)
  ├─ [Healthy] → Complete [node_3]
  └─ [Unhealthy] → Rollback [node_4]
```

### Pattern 9: Shared Resource
```
Workflow Graph:
→ Initialize [node_1]
  ⎡→ ProcessRegion1 [node_2]
  ⎢  📦 UpdateGlobalStatus [node_3]
  ⎢→ ProcessRegion2 [node_4]
  ⎢  📦 UpdateGlobalStatus [node_5]
  ⎣→ ProcessRegion3 [node_6]
     📦 UpdateGlobalStatus [node_7]
→ Finalize [node_8]
```

### Pattern 10: Complex Combined
```
Workflow Graph:
→ Initialize [node_1]
  ⎡→ BuildFrontend [node_2]
  ⎢→ BuildBackend [node_3]
  ⎣→ BuildDatabase [node_4]
→ RunTests [node_5] (depends on: node_2, node_3, node_4)
  ├─ [Pass] → DeployStaging [node_6]
  │  ↻ HealthCheck [node_7] (retry 3x)
  │    ├─ [Healthy] → DeployProduction [node_8]
  │    │  ⚡ NotifySlack [node_9]
  │    │  📦 UpdateDeploymentStatus [node_10]
  │    └─ [Unhealthy] → Rollback [node_11]
  └─ [Fail] → NotifyFailure [node_12]
```

## Validation Rules

### Rule 1: Node ID Uniqueness
Each `[node_X]` must be unique within a workflow graph.

**Valid**:
```
→ TaskA [node_1]
→ TaskB [node_2]
```

**Invalid**:
```
→ TaskA [node_1]
→ TaskB [node_1]  ❌ Duplicate node_1
```

### Rule 2: Dependency Reference Validity
All node IDs in `(depends on: ...)` must exist in the graph.

**Valid**:
```
→ TaskA [node_1]
→ TaskB [node_2] (depends on: node_1)
```

**Invalid**:
```
→ TaskA [node_1]
→ TaskB [node_2] (depends on: node_5)  ❌ node_5 doesn't exist
```

### Rule 3: Parallel Group Completeness
Parallel groups must have proper start (⎡), middle (⎢*), and end (⎣) markers.

**Valid**:
```
⎡→ TaskA [node_1]
⎢→ TaskB [node_2]
⎣→ TaskC [node_3]
```

**Invalid**:
```
⎡→ TaskA [node_1]
⎢→ TaskB [node_2]
→ TaskC [node_3]  ❌ Missing ⎣ end marker
```

### Rule 4: Branch Pair Completeness
Branch conditions should have both true (├─) and false (└─) paths, or be clearly labeled as single-path.

**Valid (Complete)**:
```
→ Test [node_1]
  ├─ [Pass] → Deploy [node_2]
  └─ [Fail] → Skip [node_3]
```

**Valid (Single Path with Label)**:
```
→ Test [node_1]
  └─ [OnlyIfPass] → Deploy [node_2]
```

**Invalid (Ambiguous)**:
```
→ Test [node_1]
  ├─ [Pass] → Deploy [node_2]
  ❌ Missing false path
```

### Rule 5: Indentation Consistency
Indentation must be consistent within each level.

**Valid**:
```
→ TaskA [node_1]
  ├─ [X] → TaskB [node_2]
  └─ [Y] → TaskC [node_3]
```

**Invalid**:
```
→ TaskA [node_1]
  ├─ [X] → TaskB [node_2]
     └─ [Y] → TaskC [node_3]  ❌ Inconsistent indent
```

### Rule 6: No Circular Dependencies
Dependencies must form a DAG (no cycles).

**Valid**:
```
→ A [node_1]
→ B [node_2] (depends on: node_1)
→ C [node_3] (depends on: node_2)
```

**Invalid**:
```
→ A [node_1] (depends on: node_3)
→ B [node_2] (depends on: node_1)
→ C [node_3] (depends on: node_2)
❌ Circular: node_1 → node_2 → node_3 → node_1
```

## Generation Algorithm

### From DAG to WGDL

```python
def generate_wgdl(dag):
    """Convert DAG to WGDL text representation"""

    output = ["Workflow Graph:"]
    visited = set()

    # Get nodes by execution level
    levels = topologically_sort_by_level(dag)

    for level in levels:
        # Check for parallel execution at this level
        if len(level.nodes) > 1 and level.parallel:
            output.extend(render_parallel_group(level.nodes))
        else:
            for node in level.nodes:
                output.append(render_node(node))

                # Check for branching
                if has_conditional_branches(node):
                    output.extend(render_branches(node))

                # Check for loop
                if has_loop(node):
                    output.append(render_loop(node))

    return "\n".join(output)

def render_node(node):
    """Render single node with appropriate symbol"""
    symbol = get_symbol(node)
    deps = f" (depends on: {', '.join(node.dependencies)})" if node.dependencies else ""
    return f"{symbol} {node.name} [{node.id}]{deps}"

def render_parallel_group(nodes):
    """Render parallel node group"""
    lines = []
    for i, node in enumerate(nodes):
        if i == 0:
            symbol = "⎡→"
        elif i == len(nodes) - 1:
            symbol = "⎣→"
        else:
            symbol = "⎢→"
        lines.append(f"  {symbol} {node.name} [{node.id}]")
    return lines
```

## Usage in Workflow Creation

### Step 1: Generate During Dependency Building
When constructing the DAG in `core/dependency-builder.md` Step 7, use this algorithm to create the text visualization.

### Step 2: Include in Command Description
The generated WGDL goes in two places:

1. **YAML Frontmatter** (compact version):
```yaml
---
description: "Deploy application with health checks"
graph: "→ Build → Test ├─[Pass]→Deploy └─[Fail]→Rollback"
---
```

2. **Command Body** (full version):
```markdown
## Workflow Execution

Workflow Graph:
→ Build [node_1]
→ Test [node_2]
  ├─ [Pass] → Deploy [node_3]
  │  ↻ HealthCheck [node_4] (retry 3x)
  └─ [Fail] → Rollback [node_5]
```

### Step 3: Validate Before File Creation
Before generating the command file in SKILL.md Step 10, validate the WGDL against all 6 validation rules.

## Parser Implementation (Reference)

```python
import re

class WGDLParser:
    """Parse and validate WGDL text"""

    NODE_PATTERN = r'([→⎡⎢⎣⚡↻📦├└│\s]+)([A-Z][a-zA-Z0-9_]*)\s+\[([a-z_0-9]+)\](\s*\(depends on: ([^)]+)\))?'

    def parse(self, wgdl_text):
        """Parse WGDL text into graph structure"""
        lines = wgdl_text.strip().split('\n')[1:]  # Skip "Workflow Graph:"
        nodes = []

        for line in lines:
            match = re.match(self.NODE_PATTERN, line)
            if match:
                symbol, name, node_id, _, deps = match.groups()
                nodes.append({
                    'symbol': symbol.strip(),
                    'name': name,
                    'id': node_id,
                    'dependencies': deps.split(', ') if deps else []
                })

        return nodes

    def validate(self, nodes):
        """Validate parsed nodes against rules"""
        errors = []

        # Rule 1: Unique node IDs
        node_ids = [n['id'] for n in nodes]
        if len(node_ids) != len(set(node_ids)):
            errors.append("Duplicate node IDs detected")

        # Rule 2: Valid dependency references
        for node in nodes:
            for dep in node['dependencies']:
                if dep not in node_ids:
                    errors.append(f"Invalid dependency reference: {dep}")

        # Rules 3-6: Additional validation...

        return len(errors) == 0, errors
```

## Best Practices

### DO ✅

- Use consistent indentation (2 spaces per level)
- Include node IDs for all nodes
- Specify dependencies explicitly for converging nodes
- Use descriptive node names (PascalCase)
- Include condition labels in brackets for branches
- Document retry counts for loops

### DON'T ❌

- Mix different indentation styles
- Omit node IDs (breaks traceability)
- Create circular dependencies
- Use ambiguous condition labels
- Exceed 5 levels of nesting (readability)
- Use symbols inconsistently

## Examples from Real Workflows

### Example 1: CI/CD Pipeline
```
Workflow Graph:
→ Checkout [node_1]
→ InstallDeps [node_2]
  ⎡→ Lint [node_3]
  ⎢→ TypeCheck [node_4]
  ⎣→ UnitTest [node_5]
→ IntegrationTest [node_6] (depends on: node_3, node_4, node_5)
  ├─ [Pass] → Build [node_7]
  │  → Deploy [node_8]
  │    ↻ SmokeTest [node_9] (retry 3x)
  │      ├─ [Pass] → TagRelease [node_10]
  │      │  ⚡ NotifySlack [node_11]
  │      └─ [Fail] → Rollback [node_12]
  └─ [Fail] → NotifyFailure [node_13]
```

### Example 2: Multi-Region Deployment
```
Workflow Graph:
→ PrepareArtifact [node_1]
📦 InitGlobalStatus [node_2]
  ⎡→ DeployUSEast [node_3]
  ⎢  ↻ HealthCheckUSEast [node_4] (until healthy)
  ⎢  📦 UpdateGlobalStatus [node_5]
  ⎢→ DeployUSWest [node_6]
  ⎢  ↻ HealthCheckUSWest [node_7] (until healthy)
  ⎢  📦 UpdateGlobalStatus [node_8]
  ⎣→ DeployEU [node_9]
     ↻ HealthCheckEU [node_10] (until healthy)
     📦 UpdateGlobalStatus [node_11]
📦 CheckGlobalStatus [node_12] (depends on: node_5, node_8, node_11)
  ├─ [AllHealthy] → Complete [node_13]
  └─ [AnyFailed] → GlobalRollback [node_14]
```

## Integration with Command Template

In `docs/command-template-reference.md`, the WGDL should appear in the "## Workflow Execution" section of every generated command:

```markdown
---
name: example-workflow
description: "Example workflow description"
category: deployment
complexity: complex
---

# Example Workflow

## Workflow Execution

**Execution Pattern**: Parallel + Branch + Loop

Workflow Graph:
[WGDL text here]

## Behavioral Instructions
[Implementation details...]
```

---

**Version**: 1.0
**Status**: Production Ready
**Last Updated**: 2025-11-04
