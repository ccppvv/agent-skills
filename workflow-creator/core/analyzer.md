# Workflow Natural Language Analyzer

## Purpose
Parse natural language workflow descriptions to extract structured task information.

## Input Format
Natural language description of workflow requirements, such as:
- "Check configuration, then run tests in parallel for each service"
- "Deploy to staging, verify health, if pass then deploy to production"
- "Batch process all user files and generate reports"

## Analysis Process

### 1. Tokenization
Split input into meaningful units:
- **Action verbs**: check, run, deploy, verify, process, generate, etc.
- **Subjects**: configuration, tests, services, staging, files, reports
- **Connectors**: then, after, and, or, if, when, for each
- **Modifiers**: in parallel, sequentially, async, until, while

### 2. Semantic Parsing
Identify semantic components:
- **Tasks**: Actions to be performed (verb + object)
- **Dependencies**: Temporal or logical relationships between tasks
- **Conditions**: Branch triggers (if/when clauses)
- **Iterations**: Loop specifications (for each, while, until)
- **Parallelism**: Concurrent execution indicators
- **Async markers**: Background or non-blocking execution hints

### 3. Constraint Extraction
Extract workflow constraints:
- **Ordering**: Sequential vs parallel vs flexible
- **Timing**: Immediate, delayed, scheduled
- **Failure handling**: Retry, skip, rollback, fail-fast
- **Resource sharing**: Shared state, locks, coordination

## Output Format

```yaml
tasks:
  - id: task_1
    action: "check"
    subject: "configuration"
    type: "node"

  - id: task_2
    action: "run"
    subject: "tests"
    type: "batch"
    iteration: "each service"

dependencies:
  - from: task_1
    to: task_2
    type: "sequential"

execution_hints:
  - task_id: task_2
    hint: "parallel"

conditions:
  - task_id: task_3
    trigger: "task_2 success"
    branch: "if pass"
```

## Key Patterns to Recognize

### Sequential Indicators
- "then", "after", "next", "followed by", "subsequently"
- Example: "Build → Test → Deploy"

### Parallel Indicators
- "in parallel", "at the same time", "concurrently", "simultaneously"
- "for each", "all at once"
- Example: "Test frontend and backend in parallel"

### Conditional Indicators
- "if", "when", "unless", "provided that"
- "success", "failure", "pass", "fail"
- Example: "If tests pass, deploy to production"

### Loop Indicators
- "for each", "for all", "repeat", "until", "while"
- "retry", "iterate", "loop through"
- Example: "For each region, deploy and verify"

### Async Indicators
- "in background", "async", "non-blocking", "asynchronously"
- "trigger and continue", "fire and forget"
- Example: "Trigger notification async and continue"

### Batch Indicators
- "all", "batch", "bulk", "group", "collection"
- "each", "every", "for all"
- Example: "Batch process all pending orders"

### Nesting Indicators
- "within", "inside", "as part of", "sub-task"
- Explicit sub-workflow references
- Example: "Execute deployment workflow for each environment"

### Shared Resource Indicators
- "shared", "global", "coordinated", "synchronized"
- "lock", "mutex", "atomic"
- Example: "Update shared deployment status"

## Usage in Workflow Creation

This analyzer is the first step in the workflow creation pipeline:

```
Natural Language Input
    ↓
Analyzer (parse and structure)
    ↓
Graph Detector (identify patterns)
    ↓
Dependency Builder (construct DAG)
    ↓
[Continue to other modules...]
```

The structured output from this analyzer feeds directly into the graph-detector module for pattern recognition.

## How Claude Should Use This

**When to Use**: This is Step 1 in the Workflow Creation Protocol (see SKILL.md).

**Execution Steps**:

1. **Read the user's workflow description** from the activation message

2. **Apply Tokenization** (Section 1 above):
   - Identify all action verbs in the description
   - Extract subjects (nouns) that verbs act upon
   - Find connectors that indicate relationships
   - Spot modifiers that indicate execution style

3. **Apply Semantic Parsing** (Section 2 above):
   - Group verb-subject pairs into tasks
   - Identify temporal relationships (which task comes first/after/during)
   - Extract conditional logic (if/when clauses)
   - Find iteration patterns (for each, while)
   - Mark parallel execution indicators
   - Identify async markers

4. **Extract Constraints** (Section 3 above):
   - Determine ordering constraints
   - Identify timing requirements
   - Find failure handling specifications
   - Spot resource sharing needs

5. **Format Output** using the YAML structure from "Output Format" section above

**Example Execution**:

User input: "Check config, then run frontend and backend tests in parallel, deploy if both pass"

Your analysis:
```yaml
tasks:
  - id: task_1
    action: "check"
    subject: "config"
    type: "node"
  - id: task_2
    action: "run"
    subject: "frontend tests"
    type: "parallel_member"
  - id: task_3
    action: "run"
    subject: "backend tests"
    type: "parallel_member"
  - id: task_4
    action: "deploy"
    subject: "application"
    type: "node"

dependencies:
  - from: task_1
    to: task_2
    type: "sequential"
  - from: task_1
    to: task_3
    type: "sequential"
  - from: task_2
    to: task_4
    type: "conditional"
  - from: task_3
    to: task_4
    type: "conditional"

execution_hints:
  - task_id: task_2
    hint: "parallel_with_task_3"
  - task_id: task_3
    hint: "parallel_with_task_2"

conditions:
  - task_id: task_4
    trigger: "task_2 AND task_3 success"
    branch: "if both pass"
```

**Next Step**: Pass this structured output to `core/graph-detector.md` for pattern detection.
