---
name: workflow-create
description: Automatically create custom workflow slash commands from natural language descriptions using graph pattern analysis and intelligent decision-making
---

# Workflow Create

## Overview

Workflow Create is a meta-level skill that enables you to create custom slash commands for complex workflows by simply describing them in natural language. It automatically analyzes your workflow description, identifies execution patterns (parallel, sequential, conditional, etc.), generates optimized workflow graphs, and creates fully functional slash commands with appropriate MCP tools and expert personas—all placed directly in `~/.claude/commands/workflows/`.

**Use this skill when:**
- Describing a multi-step workflow you want to automate
- Need a reusable command for complex task orchestration
- Want to create workflows with parallel execution, branching logic, or retry mechanisms
- Building specialized workflows that combine multiple tools and expert knowledge

## Core Workflow

### 1. Describe Your Workflow in Natural Language

Simply tell Claude what workflow you need:

```
"Check configuration, then run frontend and backend tests in parallel,
deploy to staging if both pass, verify health, and deploy to production
if healthy"
```

### 2. Automatic Plan Mode & User Approval

When you use this skill, Claude **automatically enters Plan Mode** to analyze your workflow. After analysis, Claude presents a comprehensive plan and waits for your approval before generating any files.

**Analysis includes**:
- Parse your natural language description
- Identify graph characteristics (Node, Batch, Parallel, Flow, Async, Looping, Branch, Nesting, Shared)
- Construct dependency graph (DAG)
- Analyze parallelization opportunities
- Make intelligent decisions about:
  - Command category (workflow/automation/deployment/testing/etc.)
  - Complexity level (simple/standard/complex/high)
  - Required MCP servers (sequential, magic, playwright, serena, context7)
  - Expert personas (architects, developers, specialists)

**You will review and approve** the plan before any commands or agents are created.

### 3. Generate Executable Command

Creates a complete slash command in `~/.claude/commands/workflows/[name].md` with:
- Proper YAML frontmatter metadata
- Workflow graph visualization using symbols (→, ⎡⎢⎣, ├─, ⚡, ↻, 📦)
- Step-by-step behavioral instructions
- MCP tool integrations
- Usage examples
- Clear boundaries (will/won't do)

### 4. Optional: Create Custom Agent

For complex workflows (complexity: complex/high), may also create a specialized sub-agent in `~/.claude/agents/workflows/[name]-specialist.md` with:
- Domain-specific triggers
- Focus areas and key actions
- Expected outputs
- Clear operational boundaries

## Graph Characteristics Reference

The skill understands and applies 9 core graph patterns:

| Pattern | Symbol | Description | Example Trigger |
|---------|---------|-------------|-----------------|
| **Node** | `→` | Single atomic operation | "Check config" |
| **Batch** | `→ Batch[N]` | Same operation on multiple items | "all files", "each item" |
| **Parallel** | `⎡⎢⎣` | Independent simultaneous tasks | "in parallel", "concurrently" |
| **Flow** | `→ → →` | Sequential data pipeline | "then", "next", "after" |
| **Async** | `⚡` | Background non-blocking | "in background", "async" |
| **Looping** | `↻` | Retry/repeat until condition | "retry", "until", "while" |
| **Branch** | `├─└─` | Conditional execution paths | "if", "when", "based on" |
| **Nesting** | `└→` | Sub-workflows within workflows | "for each... execute workflow" |
| **Shared** | `📦` | Shared state/resources | "shared", "global", "coordinated" |

**Pattern Combination**: Real workflows often combine multiple patterns (e.g., Parallel + Branch + Async).

## Usage Examples

### Example 1: Simple Validation (Node Pattern)

**Input**:
```
Create a workflow to check system configuration
```

**Generated**: `/check-config`
- Category: analysis
- Complexity: simple
- Pattern: node
- Location: `~/.claude/commands/workflows/check-config.md`

---

### Example 2: Batch Processing

**Input**:
```
Add type annotations to all Python files in src/
```

**Generated**: `/batch-type-annotate`
- Category: maintenance
- Complexity: standard
- Pattern: batch
- MCP: serena (code manipulation)
- Persona: backend-developer

---

### Example 3: Parallel Quality Checks

**Input**:
```
Run linter, tests, and type checker in parallel
```

**Generated**: `/parallel-quality-check`
- Category: testing
- Complexity: standard
- Pattern: parallel
- MCP: playwright (testing)
- Persona: qa-specialist

---

### Example 4: Conditional Deployment (Branch Pattern)

**Input**:
```
Run tests, if pass deploy to staging, else notify failure
```

**Generated**: `/test-and-deploy`
- Category: deployment
- Complexity: standard
- Pattern: branch
- MCP: playwright
- Personas: devops-architect, qa-specialist

---

### Example 5: Complex Multi-Region (Combined Patterns)

**Input**:
```
Deploy to three regions in parallel. For each region: deploy to staging,
verify health, if healthy deploy to production else rollback. Track shared
deployment status. If any region fails, trigger global rollback.
```

**Generated**: `/multi-region-deploy`
- Category: deployment
- Complexity: high
- Patterns: parallel, flow, branch, async, shared
- MCP: sequential, playwright, serena
- Personas: devops-architect, system-architect, security-engineer, backend-architect, qa-specialist
- Also creates: `multi-region-deploy-specialist` agent

---

## Analysis Modules

The skill uses a sophisticated analysis pipeline (all automated, no user action needed):

### 1. Natural Language Analyzer (`core/analyzer.md`)
- Parses natural language into structured tasks
- Identifies actions, subjects, dependencies, conditions
- Extracts execution hints (parallel, async, retry)

### 2. Graph Pattern Detector (`core/graph-detector.md`)
- Identifies which of the 9 graph patterns are present
- Calculates confidence scores for each pattern
- Supports pattern combinations

### 3. Dependency Graph Builder (`core/dependency-builder.md`)
- Constructs Directed Acyclic Graph (DAG)
- Performs topological sorting
- Identifies execution levels
- Detects circular dependencies

### 4. Parallel Optimizer (`core/parallel-optimizer.md`)
- Finds parallelization opportunities
- Estimates speedup potential
- Recommends execution strategies (conservative/balanced/aggressive)

### 5. Decision Engine (`core/decision-engine.md`)
- Determines command category
- Calculates complexity score (0-1 scale)
- Selects appropriate MCP servers
- Chooses expert personas
- Decides if custom agent needed

## Command Metadata Intelligence

### Category Selection (8 options)
- **workflow**: General multi-step processes
- **automation**: Repetitive tasks with retry logic
- **analysis**: Investigation and reporting
- **generation**: Code/document/asset creation
- **deployment**: Release pipelines
- **testing**: Quality assurance workflows
- **maintenance**: Cleanup and updates
- **orchestration**: Multi-workflow coordination

### Complexity Scoring (5 factors, weighted)
```
Complexity = (
  step_count × 0.30 +
  dependency_complexity × 0.25 +
  tool_diversity × 0.20 +
  error_handling × 0.15 +
  state_management × 0.10
)
```

**Levels**:
- simple: < 0.3
- standard: 0.3 - 0.6
- complex: 0.6 - 0.85
- high: ≥ 0.85

### MCP Server Selection Rules
- UI tasks → `magic` + `context7`
- Testing → `playwright`
- Complex analysis → `sequential`
- Code operations → `serena`
- Complex workflows → `sequential` (coordinator)

### Persona Selection
Automatically includes relevant experts based on:
- Domain keywords (frontend, backend, deployment, testing)
- Workflow complexity (security-engineer for complex)
- MCP tools (frontend-architect if magic is used)
- Task types (devops-architect for deployment)

## Advanced Features

### Workflow Graph Text Description

Generated commands include visual workflow descriptions:

```
→ Initialize [node_1]
⎡→ BuildFrontend [node_2]
⎢→ BuildBackend [node_3]
⎣→ BuildAPI [node_4]
→ RunTests [node_5] (depends on: 2, 3, 4)
  ├─ [Pass] → Deploy [node_6]
  └─ [Fail] → Alert [node_7]
```

### Custom Agent Creation

For high-complexity workflows, automatically creates specialized agents:

**Decision Criteria**:
- Complexity: complex or high
- Specialized domain not covered by existing personas
- Reusable pattern across multiple workflows

**Agent Includes**:
- Specific triggers and activation patterns
- Focus areas (4-6 specialized domains)
- Key actions (4-6 systematic steps)
- Concrete outputs (4-6 deliverables)
- Clear boundaries (will/won't do)

### Output Locations

**Commands**: `~/.claude/commands/workflows/[command-name].md`
**Agents**: `~/.claude/agents/workflows/[agent-name].md`

Directories are created automatically if they don't exist.

## Workflow Creation Protocol

**IMPORTANT FOR CLAUDE**: When this skill is activated, follow this protocol exactly. This ensures proper Plan Mode usage and user approval workflow.

### Phase 1: Enter Plan Mode & Analyze (Planning Phase)

**You MUST enter Plan Mode at the start**. You are now planning, not executing.

#### Step 1: Parse Natural Language
**Input**: User's workflow description
**Actions**:
1. Read `core/analyzer.md` for parsing patterns
2. Apply tokenization: identify verbs, nouns, connectors
3. Extract structured information:
   - Actions (verbs): "check", "deploy", "run", "verify"
   - Subjects (nouns): "tests", "config", "application"
   - Dependencies (connectors): "then", "after", "before"
   - Conditions: "if", "when", "unless"
   - Execution hints: "in parallel", "async", "retry 3 times"

**Output Format**:
```yaml
tasks:
  - id: task_1
    action: "check"
    subject: "configuration"
    dependencies: []
  - id: task_2
    action: "deploy"
    subject: "application"
    dependencies: [task_1]
    conditions: ["if task_1 succeeds"]
```

#### Step 2: Detect Graph Patterns
**Input**: Structured tasks from Step 1
**Actions**:
1. Read `core/graph-detector.md` for pattern detection algorithms
2. For each of the 9 patterns, calculate confidence score:
   - Keyword matching (weight: 0.3)
   - Structure matching (weight: 0.35)
   - Dependency matching (weight: 0.25)
   - Semantic matching (weight: 0.1)
3. Select patterns with confidence ≥ 0.6

**Output Format**:
```yaml
detected_patterns:
  - name: "parallel"
    confidence: 0.85
    evidence: ["in parallel", "concurrently"]
  - name: "branch"
    confidence: 0.72
    evidence: ["if pass", "else"]
```

#### Step 3: Build Dependency Graph
**Input**: Structured tasks + detected patterns
**Actions**:
1. Read `core/dependency-builder.md` for DAG construction
2. Create nodes for each task
3. Create edges based on dependencies
4. Perform cycle detection using DFS
5. Perform topological sorting for execution order
6. Calculate execution levels (which tasks can run in parallel)

**Output Format**:
```yaml
dag:
  nodes:
    - id: task_1
      level: 0
    - id: task_2
      level: 1
  edges:
    - from: task_1
      to: task_2
  execution_order: [task_1, task_2]
  cycles_detected: false
```

#### Step 4: Optimize for Parallelization
**Input**: DAG from Step 3
**Actions**:
1. Read `core/parallel-optimizer.md` for optimization strategies
2. Identify independent tasks at each level
3. Estimate speedup using Amdahl's Law
4. Recommend execution strategy (conservative/balanced/aggressive)

**Output Format**:
```yaml
parallelization:
  opportunities:
    - level: 1
      tasks: [task_2, task_3, task_4]
      estimated_speedup: 2.8x
  strategy: "balanced"
  recommendation: "Execute tasks 2-4 in parallel using Task tool"
```

#### Step 5: Make Intelligent Decisions
**Input**: All previous outputs
**Actions**:
1. Read `core/decision-engine.md` for decision rules
2. Determine category based on domain keywords
3. Calculate complexity score (0-1) using 5-factor formula
4. Select MCP servers based on task types
5. Choose personas based on domain and complexity
6. Decide if custom agent needed (complexity ≥ complex OR specialized domain)

**Output Format**:
```yaml
decisions:
  category: "deployment"
  complexity: 0.75
  complexity_level: "complex"
  mcp_servers: ["sequential", "playwright"]
  personas: ["devops-architect", "qa-specialist", "security-engineer"]
  custom_agent_needed: true
  agent_rationale: "Complex deployment workflow with health checks requires specialized coordination"
```

#### Step 6: Generate Workflow Graph Description
**Input**: DAG + detected patterns
**Actions**:
1. Convert DAG to text-based graph description
2. Use standard symbols: → (sequential), ⎡⎢⎣ (parallel), ├─└─ (branch), ⚡ (async), ↻ (loop), 📦 (shared)
3. Include node IDs and dependency relationships

**Output Format**:
```
Workflow Graph:
→ CheckConfig [task_1]
⎡→ BuildFrontend [task_2]
⎢→ BuildBackend [task_3]
⎣→ BuildAPI [task_4]
→ RunTests [task_5] (depends on: task_2, task_3, task_4)
  ├─ [Pass] → DeployStaging [task_6]
  │  → VerifyHealth [task_7]
  │    ├─ [Healthy] → DeployProduction [task_8]
  │    └─ [Unhealthy] → Rollback [task_9]
  └─ [Fail] → NotifyFailure [task_10]
```

### Phase 2: Present Plan & Get User Approval

#### Step 7: Compile Comprehensive Plan
**Actions**:
1. Synthesize all analysis results into a cohesive plan
2. Include all key information:
   - Detected workflow patterns with confidence scores
   - Workflow graph visualization (text-based)
   - Parallelization opportunities and estimated benefits
   - Proposed command metadata (name, category, complexity, mcp-servers, personas)
   - Whether custom agent will be created and why
   - Workflow graph description (exact text for command file)

**Plan Structure**:
```markdown
# Workflow Analysis Plan

## Detected Patterns
- Parallel (confidence: 0.85): Independent build tasks
- Branch (confidence: 0.72): Conditional deployment
- Flow (confidence: 0.90): Sequential pipeline

## Workflow Graph
[Text-based visualization from Step 6]

## Parallelization Opportunities
- Level 1: BuildFrontend, BuildBackend, BuildAPI (estimated speedup: 2.8x)

## Proposed Command Metadata
- Name: test-and-deploy
- Category: deployment
- Complexity: complex (score: 0.75)
- MCP Servers: sequential, playwright
- Personas: devops-architect, qa-specialist, security-engineer

## Custom Agent Creation
✅ Yes - Will create `test-and-deploy-specialist` agent
Rationale: Complex deployment workflow with health checks requires specialized coordination

## Output Locations
- Command: ~/.claude/commands/workflows/test-and-deploy.md
- Agent: ~/.claude/agents/workflows/test-and-deploy-specialist.md
```

#### Step 8: Use ExitPlanMode Tool
**CRITICAL**: You MUST use the ExitPlanMode tool with the compiled plan from Step 7.

**Actions**:
```
Use ExitPlanMode tool with parameter:
plan = [The comprehensive plan from Step 7]
```

This presents the plan to the user for review.

#### Step 9: Wait for User Approval
**Actions**:
- **DO NOT proceed to Phase 3 until user explicitly approves**
- User may:
  - Approve the plan → Proceed to Phase 3
  - Request modifications → Return to relevant steps in Phase 1
  - Reject the plan → Stop and discuss alternatives

### Phase 3: Execute Generation (After User Approval)

**Only execute this phase after user has approved the plan.**

#### Step 10: Generate Command File
**Input**: Approved plan + all analysis outputs
**Actions**:
1. Read `docs/command-template-reference.md` for template structure
2. Create command file at `~/.claude/commands/workflows/[name].md`
3. Include:
   - YAML frontmatter with metadata (name, description, category, complexity, mcp-servers, personas)
   - Workflow graph description (from Step 6)
   - Behavioral instructions for executing the workflow
   - MCP integration guidance
   - Usage examples
   - Boundaries (will/won't do)

#### Step 11: Generate Agent File (If Needed)
**Input**: Decision from Step 5
**Actions**:
1. If `custom_agent_needed == true`:
   - Read `docs/agent-template-reference.md` for template structure
   - Create agent file at `~/.claude/agents/workflows/[name]-specialist.md`
   - Include:
     - Activation triggers
     - Focus areas (4-6 specialized domains)
     - Key actions (4-6 systematic steps)
     - Expected outputs (4-6 deliverables)
     - Boundaries (will/won't do)

#### Step 11.5: Validate Generated Files
**CRITICAL**: Validate all generated files before reporting completion.

**Actions**:
1. **Validate Command File**:
   ```bash
   python validators/command-validator.py ~/.claude/commands/workflows/[name].md
   ```
   - Checks YAML frontmatter syntax
   - Validates required metadata fields (name, description, category, complexity)
   - Verifies MCP server availability
   - Validates persona names
   - Checks command naming conventions
   - Confirms body structure completeness

2. **Validate Workflow Graph**:
   ```bash
   python validators/graph-validator.py ~/.claude/commands/workflows/[name].md
   ```
   - Validates WGDL (Workflow Graph Description Language) compliance
   - Checks node ID uniqueness
   - Validates dependency references
   - Verifies parallel group completeness (⎡, ⎢*, ⎣)
   - Checks branch pair completeness (├─, └─)
   - Validates indentation consistency
   - Detects circular dependencies (DAG validation)

3. **Handle Validation Errors**:
   - If validation fails, **DO NOT proceed to Step 12**
   - Review validation error messages
   - Fix the generated files
   - Re-run validation until all checks pass
   - Common issues and fixes are in "Troubleshooting Guide" section below

**Expected Output**:
```
🔍 Validating command file: test-and-deploy.md
  ✅ YAML syntax valid
  ✅ All required fields present
  ✅ MCP servers available
  ✅ Personas valid
  ✅ Command name format correct
  ✅ Body structure complete
✅ Command validation passed!

🔍 Validating workflow graph in: test-and-deploy.md
  ✅ Graph validation passed (10 nodes, 12 edges)
  ✅ No circular dependencies
  ✅ All dependencies valid
  ✅ Parallel groups complete
  ✅ Branch pairs complete
✅ Graph validation passed!
```

#### Step 12: Report Completion
**Actions**:
1. Confirm file creation with exact paths
2. Provide summary of what was created
3. Suggest next steps (test the command, provide feedback)

**Completion Report Format**:
```markdown
✅ Workflow command created successfully!

## Generated Files
- Command: ~/.claude/commands/workflows/test-and-deploy.md
- Agent: ~/.claude/agents/workflows/test-and-deploy-specialist.md

## What Was Created
- Command: `/test-and-deploy`
  - Category: deployment
  - Complexity: complex
  - Patterns: parallel, branch, flow
  - MCP Servers: sequential, playwright
  - Personas: devops-architect, qa-specialist, security-engineer

- Agent: test-and-deploy-specialist
  - Specialized coordinator for complex deployment workflows
  - Handles health checks and rollback logic

## Next Steps
1. Try using the command: `/test-and-deploy`
2. Provide feedback if adjustments needed
3. Iterate until workflow meets your requirements
```

---

## Resources

### Core Analysis Modules (`core/`)
Referenced automatically during workflow creation:
- `analyzer.md`: Natural language parsing patterns
- `graph-detector.md`: Pattern detection algorithms
- `dependency-builder.md`: DAG construction methods
- `parallel-optimizer.md`: Optimization strategies
- `decision-engine.md`: Intelligent metadata selection

### Generation Scripts (`generators/`)
Python scripts for creating output files:
- `command-generator.py`: Creates slash command markdown
- `agent-generator.py`: Creates custom agent definitions
- `workflow-orchestrator.py`: Coordinates entire pipeline

### Reference Documentation (`docs/`)
Detailed references loaded as needed:
- `graph-patterns-reference.md`: Complete pattern descriptions with triggers
- `command-template-reference.md`: Command structure and validation
- `agent-template-reference.md`: Agent structure and naming conventions

### Example Workflows (`examples/`)
Nine complete examples demonstrating each pattern:
- `01-node/`: Simple single-task workflow
- `02-batch/`: Batch processing example
- `03-parallel/`: Parallel execution example
- `04-flow/`: Sequential pipeline example
- `05-async/`: Background execution example
- `06-looping/`: Retry logic example
- `07-branch/`: Conditional branching example
- `08-nesting/`: Nested workflows example
- `09-combined/`: Complex multi-pattern combination

Each example includes:
- `input.txt`: Natural language input
- `expected-command.md`: Generated command
- `analysis.yaml`: Analysis breakdown

## Best Practices

### When Describing Workflows

**Do**:
- ✅ Use clear action verbs ("check", "deploy", "run", "verify")
- ✅ Specify relationships ("then", "if", "in parallel", "for each")
- ✅ Include conditions ("if pass", "until healthy", "up to 3 times")
- ✅ Mention all steps in sequence

**Don't**:
- ❌ Be vague ("do some stuff", "handle things")
- ❌ Omit critical steps
- ❌ Create circular dependencies
- ❌ Mix unrelated workflows

### Workflow Naming

Generated command names follow conventions:
- lowercase-with-hyphens
- Descriptive of primary action
- 3-30 characters
- Examples: `check-config`, `parallel-quality-check`, `multi-region-deploy`

### Iteration and Refinement

After generation:
1. Test the generated command
2. Provide feedback if adjustments needed
3. Skill can regenerate with modifications
4. Iterate until workflow meets requirements

## Troubleshooting

### Workflow Analysis Issues

#### "Pattern Not Detected"
- **Cause**: Ambiguous natural language
- **Solution**: Use explicit keywords (see pattern trigger table above)
- **Example**: Instead of "do things together", say "run in parallel"

#### "Complexity Too Low/High"
- **Cause**: Scoring algorithm mismatch with perception
- **Solution**: Provide feedback; skill adjusts scoring
- **Note**: Complexity is calculated using 5-factor formula (step count, dependencies, tool diversity, error handling, state management)

#### "Wrong MCP Servers Selected"
- **Cause**: Task type not clearly specified
- **Solution**: Mention specific tools needed ("using Playwright", "with code manipulation")
- **Tip**: Review MCP Server Selection Rules in "Intelligent Decision Making" section

#### "Missing Persona"
- **Cause**: Domain keywords not recognized
- **Solution**: Explicitly mention expertise needed ("with security review", "frontend validation")
- **Tip**: Personas are auto-selected based on domain keywords and complexity

### Validation Errors (Step 11.5)

#### Command Validation Errors

**Error: "YAML syntax error"**
```
Cause: Invalid YAML in frontmatter (missing quotes, incorrect indentation)
Fix: Ensure YAML frontmatter follows strict syntax:
---
name: command-name
description: "Description in quotes"
category: workflow
complexity: standard
mcp-servers: [server1, server2]
personas: [persona1, persona2]
---
```

**Error: "Missing required fields"**
```
Cause: name, description, category, or complexity field missing
Fix: All four fields are mandatory - add missing field(s)
```

**Error: "Invalid name format"**
```
Cause: Command name not in lowercase-with-hyphens format
Examples:
  ❌ "checkConfig" (camelCase)
  ❌ "Check_Config" (underscores/caps)
  ✅ "check-config" (correct)
Fix: Use lowercase letters, numbers, hyphens only. Must start with letter, 3-30 chars.
```

**Error: "Invalid category"**
```
Cause: Category not in valid list
Valid: workflow, automation, analysis, generation, deployment, testing, maintenance, orchestration
Fix: Choose one of the 8 valid categories
```

**Error: "Invalid complexity"**
```
Cause: Complexity not in valid list
Valid: simple, standard, complex, high
Fix: Use one of the 4 valid complexity levels
```

**Error: "Unavailable MCP servers"**
```
Cause: Referenced MCP server not available
Available: sequential, magic, context7, playwright, serena
Fix: Use only available MCP servers or leave empty []
```

**Error: "Invalid personas"**
```
Cause: Referenced persona not in valid list
Valid personas: general-purpose, system-architect, backend-architect, frontend-architect,
  backend-developer, frontend-developer, qa-specialist, security-engineer,
  performance-engineer, devops-architect, data-engineer, ml-engineer
Fix: Use only valid personas from list above
```

**Error: "Missing body sections"**
```
Cause: Required markdown sections missing from command body
Required sections:
  - # /command-name (title)
  - Workflow Description
  - Detected Patterns
  - Workflow Graph
  - Behavioral Flow
  - Usage Examples
  - Boundaries
Fix: Ensure all 7 sections are present in command file
```

#### Graph Validation Errors (WGDL)

**Error: "Duplicate node ID"**
```
Cause: Same [node_X] used multiple times
Example:
  → TaskA [node_1]
  → TaskB [node_1]  ❌ Duplicate

Fix: Ensure each node has unique ID: [node_1], [node_2], [node_3], etc.
```

**Error: "Node references non-existent dependency"**
```
Cause: (depends on: node_X) references node that doesn't exist
Example:
  → TaskA [node_1]
  → TaskB [node_2] (depends on: node_5)  ❌ node_5 doesn't exist

Fix: Ensure all dependency references exist in graph
```

**Error: "Unmatched parallel group markers"**
```
Cause: Missing ⎡ (start) or ⎣ (end) for parallel group
Example:
  ⎡→ TaskA [node_1]
  ⎢→ TaskB [node_2]
  → TaskC [node_3]  ❌ Missing ⎣

Fix: Complete parallel groups:
  ⎡→ TaskA [node_1]
  ⎢→ TaskB [node_2]
  ⎣→ TaskC [node_3]  ✅
```

**Error: "Branch without false path"**
```
Cause: ├─ (true branch) without └─ (false branch)
Example:
  → Test [node_1]
    ├─ [Pass] → Deploy [node_2]
    ❌ Missing └─ false path

Fix: Add both paths or use clear single-path label:
  → Test [node_1]
    ├─ [Pass] → Deploy [node_2]
    └─ [Fail] → Skip [node_3]  ✅
```

**Error: "Inconsistent indentation"**
```
Cause: Sudden indentation jumps or misaligned levels
Fix: Use consistent indentation (2 spaces per level)
  → Level0 [node_1]
    ├─ [X] → Level1 [node_2]
    └─ [Y] → Level1 [node_3]  ✅ Same indent
```

**Error: "Circular dependency detected"**
```
Cause: Node dependencies form a cycle (A → B → C → A)
Example:
  → TaskA [node_1] (depends on: node_3)
  → TaskB [node_2] (depends on: node_1)
  → TaskC [node_3] (depends on: node_2)
  ❌ Circular: node_1 → node_2 → node_3 → node_1

Fix: Remove back-edge or use loop pattern (↻) for retries:
  → TaskA [node_1]
  → TaskB [node_2]
  ↻ TaskC [node_3] (retry 3x)  ✅ Loop, not cycle
```

**Error: "Node name not in PascalCase"**
```
Cause: Node names not following PascalCase convention
Examples:
  ❌ "runTests" → "RunTests"
  ❌ "deploy_app" → "DeployApp"
  ✅ "BuildFrontend"

Fix: Use PascalCase: capitalize first letter of each word, no separators
```

### When Validation Fails

1. **Review Error Messages**: Validators provide specific line numbers and explanations
2. **Consult WGDL Spec**: See `docs/graph-description-language.md` for graph format rules
3. **Check Templates**: Review `docs/command-template-reference.md` for structure requirements
4. **Fix and Re-validate**: Make corrections and run validators again
5. **Iterate**: Continue fixing until all validations pass

### Getting Help

If you encounter persistent validation errors:
1. Check the error message carefully - it usually indicates the exact issue
2. Review the relevant documentation (`docs/` directory)
3. Look at the example commands in `~/.claude/commands/workflows/` for correct patterns
4. Provide feedback to improve validation rules or error messages

---

**This skill is self-improving**: As you use it and provide feedback, the pattern detection and decision-making become more accurate for your specific workflow needs.
