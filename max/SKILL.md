---
name: max
description: |
  Multi-turn conversation state management through state reconstruction, history reminders, and XML structured output.
  Use when: (1) Conversation reaches 3+ turns, (2) Context usage exceeds 60%, (3) Working on cross-file/cross-component complex tasks,
  (4) Need to remember multiple parallel decisions, (5) User explicitly requests "remember this information", (6) Using --state-aware flag.
---

# Max - State Reconstruction

Maintain memory coherence in long conversations through state reconstruction rather than full history retention.

## Core Mechanism

**Three-Component Architecture:**

1. **State Reconstruction (SR)** - Control input length per turn
   - Each turn input = new content + key state from previous turn
   - Input length stays relatively fixed, not growing linearly with turns

2. **History Reminder (HR)** - Force model attention on cross-turn information
   - Explicitly remind model of confirmed core conclusions
   - Combat forgetting in long conversations

3. **XML Structured Output** - Enable automated information extraction
   - Mark all key information with `<info>...</info>` tags
   - Program can auto-parse and build next turn input

## Response Format Protocol

Every response MUST follow this structure:

```xml
<info category="核心发现|技术决策|问题分析|解决方案|风险提示|状态更新|依赖关系|性能指标">
[Concise description of key information]
</info>

<info category="...">
[Another key information]
</info>
```

## Information Extraction Rules

1. **Completeness Principle**: Each response must contain "previous key information + new information from this turn"
2. **Conciseness Principle**: Each `<info>` content limited to 1-2 sentences, focus on core points
3. **Categorization Principle**: Use category attribute to mark information type for filtering and organization
4. **Accumulation Principle**: Key information carries forward in subsequent turns until problem resolved or information obsolete

## Category Types

See [references/category-types.md](references/category-types.md) for detailed category descriptions and usage guidelines.

Quick reference:
- `核心发现`: Important discoveries and insights
- `技术决策`: Confirmed technical solutions and architecture choices
- `问题分析`: Root cause, impact scope, severity
- `解决方案`: Specific fix solutions and implementation steps
- `风险提示`: Potential risks, precautions, boundary conditions
- `状态更新`: Task progress, completion status, next steps
- `依赖关系`: Component dependencies, call relationships, data flows
- `性能指标`: Performance data, benchmarks, optimization effects

## Workflow

1. **Turn 1**: Respond normally + extract key information into `<info>` tags
2. **Turn 2+**: Include previous `<info>` content in context + add new `<info>` for this turn
3. **Continuous**: Carry forward relevant `<info>` until task completion or information obsolescence

## Example Usage

See [references/examples.md](references/examples.md) for complete multi-turn conversation examples.

**Turn 1**:
```
[Regular response content...]

<info category="问题分析">auth.js:45 has SQL injection vulnerability using string concatenation</info>
<info category="技术决策">Adopt parameterized query approach using pg.query($1, [param]) pattern</info>
```

**Turn 2**:
```
[Response based on previous information...]

<info category="问题分析">auth.js:45 has SQL injection vulnerability using string concatenation</info>
<info category="技术决策">Adopt parameterized query approach using pg.query($1, [param]) pattern</info>
<info category="解决方案">Completed auth.js fix, discovered same pattern in user.js:128</info>
<info category="风险提示">Need to check all database query statements, estimated impact on 12 files</info>
```

## Activation Rules

**Auto-activate when:**
- Conversation turns ≥ 3
- Context usage > 60%
- Cross-file/cross-component complex tasks
- Need to remember multiple parallel decisions

**Manual activation:**
- User explicitly requests "remember this information"
- Using `--state-aware` flag

## Integration Notes

- Works with task management tools (TodoWrite, write_memory)
- Supports token efficiency optimization
- Enables meta-cognitive activity through state extraction
- Can persist key state information to memory systems
