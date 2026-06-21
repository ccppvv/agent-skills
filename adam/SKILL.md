---
name: adam
description: Generate simple, memorable, and contextually appropriate English names for Claude Code skills. Use when users need help naming a new skill or renaming an existing skill based on its functionality and characteristics.
---

# Adam - The Skill Namer

Generate effective names for Claude Code skills that are simple, memorable, and accurately reflect the skill's purpose.

## Core Principles

1. **Simplicity**: Easy to spell and pronounce
2. **Memorability**: Easy to remember and recall
3. **Relevance**: Accurately reflects the skill's core functionality
4. **Consistency**: Follows Claude Code naming conventions (kebab-case)

## Naming Workflow

### Step 1: Analyze Skill Characteristics

Extract key information:
- **Core functionality**: What does the skill do?
- **Key mechanisms**: How does it work?
- **Use cases**: When is it used?
- **Target users**: Who will use it?

### Step 2: Generate Name Categories

Provide options across multiple categories:

1. **Functional Names** (e.g., `context-keeper`, `memory-chain`)
   - Directly describe what the skill does
   - Use common technical terms
   - 2-3 words maximum

2. **Common Human Names** (e.g., `max`, `sage`, `alex`)
   - Simple, real English names (4-6 letters preferred)
   - Easy to spell and pronounce
   - Can have metaphorical meaning related to functionality

3. **Metaphorical Names** (e.g., `lighthouse`, `compass`)
   - Use familiar objects or concepts
   - Create mental associations with functionality
   - Should be intuitive

### Step 3: Evaluate and Rank

For each name option, consider:
- **Spelling difficulty**: Can users spell it without looking?
- **Pronunciation**: Is it clear how to say it?
- **Memorability**: Will users remember it after one use?
- **Uniqueness**: Does it stand out from other skills?
- **Appropriateness**: Does it fit the skill's purpose?

### Step 4: Present Recommendations

Format:
```
## 🎯 Recommended Names

### 1. [name] ⭐⭐⭐⭐⭐
- **Type**: [Functional/Human Name/Metaphorical]
- **Meaning**: [What it means/represents]
- **Strengths**: [Why it's a good choice]
- **Considerations**: [Any potential issues]

[Repeat for 5-7 options]

## 💡 Top Pick
[Your #1 recommendation with detailed reasoning]
```

## Naming Guidelines

### DO:
- Use lowercase with hyphens (kebab-case)
- Keep it under 20 characters
- Choose words from common English vocabulary
- Consider how it sounds when spoken aloud
- Test if it's easy to type quickly

### DON'T:
- Use obscure technical jargon
- Include numbers or special characters
- Use words that are commonly misspelled
- Choose names that are too similar to existing skills
- Use acronyms unless universally known

## Common Name Patterns

See [references/naming-patterns.md](references/naming-patterns.md) for detailed patterns and examples.

Quick reference:
- **Agent/Role**: `architect`, `reviewer`, `planner`
- **Action**: `builder`, `analyzer`, `optimizer`
- **Tool**: `toolkit`, `helper`, `assistant`
- **Concept**: `workflow`, `pipeline`, `framework`
- **Human Names**: `max`, `sage`, `alex`, `quinn`

## Example Usage

**Input**: Skill that manages multi-turn conversation state through XML-tagged information extraction

**Output**:
1. `memory-chain` (functional) - Describes information chaining
2. `context-keeper` (functional) - Emphasizes context preservation
3. `max` (human name) - Simple, suggests maximizing memory
4. `sage` (human name) - Wisdom/knowledge accumulation
5. `chronicle` (metaphorical) - Recording history

**Top Pick**: `max` - Ultra-simple (3 letters), suggests maximizing memory capacity, easy to type and remember

## Integration Notes

- Works well with skill-creator workflow
- Can be used during skill initialization or refactoring
- Helps maintain consistent naming across skill collections
