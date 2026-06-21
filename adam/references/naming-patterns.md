# Naming Patterns Reference

Comprehensive guide to naming patterns for Claude Code skills with real-world examples.

## Pattern Categories

### 1. Agent/Role Names

**Pattern**: `[role-name]`

**When to use**: Skills that act as a specific role or persona

**Examples**:
- `architect` - System design and architecture planning
- `reviewer` - Code review and quality assessment
- `planner` - Task planning and breakdown
- `debugger` - Bug investigation and fixing
- `optimizer` - Performance optimization
- `mentor` - Educational guidance and teaching

**Characteristics**:
- Single word, typically a job title
- Implies agency and expertise
- Clear role definition

### 2. Action-Based Names

**Pattern**: `[action]-[object]` or `[action]er`

**When to use**: Skills focused on performing specific actions

**Examples**:
- `code-builder` - Builds code implementations
- `test-runner` - Executes test suites
- `doc-generator` - Generates documentation
- `file-analyzer` - Analyzes file structures
- `data-transformer` - Transforms data formats
- `api-explorer` - Explores API endpoints

**Characteristics**:
- Verb-based or agent noun (-er suffix)
- Action-oriented
- Clear about what it does

### 3. Tool/Utility Names

**Pattern**: `[domain]-[tool-type]`

**When to use**: Skills that provide tools or utilities

**Examples**:
- `git-toolkit` - Git operation utilities
- `docker-helper` - Docker management assistance
- `sql-assistant` - SQL query assistance
- `json-formatter` - JSON formatting utilities
- `image-processor` - Image processing tools
- `pdf-editor` - PDF editing capabilities

**Characteristics**:
- Tool/helper/assistant suffix
- Domain-specific
- Utility-focused

### 4. Concept/Framework Names

**Pattern**: `[concept-name]`

**When to use**: Skills representing methodologies or frameworks

**Examples**:
- `workflow` - Workflow management
- `pipeline` - CI/CD pipeline operations
- `framework` - Development framework setup
- `pattern` - Design pattern implementation
- `strategy` - Strategic planning approach
- `protocol` - Communication protocol handling

**Characteristics**:
- Abstract concept
- Methodology-focused
- Framework-oriented

### 5. Human Names

**Pattern**: `[first-name]`

**When to use**: Skills with personality or conversational nature

**Examples**:
- `max` - Maximizing capabilities (memory, performance)
- `sage` - Wisdom and knowledge (guidance, advice)
- `alex` - Protection and defense (security, validation)
- `grace` - Elegance and refinement (code quality, style)
- `sam` - Listening and recording (logging, monitoring)
- `quinn` - Intelligence and analysis (data analysis, insights)
- `morgan` - Preservation and keeping (archiving, backup)

**Characteristics**:
- 3-6 letters preferred
- Common English names
- Can have metaphorical meaning
- Gender-neutral names often preferred

### 6. Metaphorical Names

**Pattern**: `[metaphor]`

**When to use**: Skills where a metaphor enhances understanding

**Examples**:
- `lighthouse` - Guidance and navigation
- `compass` - Direction finding
- `bridge` - Connection and integration
- `lens` - Analysis and inspection
- `forge` - Creation and building
- `garden` - Growth and cultivation
- `atlas` - Mapping and exploration

**Characteristics**:
- Familiar objects or concepts
- Creates mental associations
- Intuitive understanding
- Single word preferred

## Naming Decision Tree

```
Is the skill conversational/has personality?
├─ YES → Consider Human Names (max, sage, alex)
└─ NO → Continue

Does it perform a specific action?
├─ YES → Use Action-Based (builder, analyzer)
└─ NO → Continue

Does it represent a role?
├─ YES → Use Agent/Role (architect, reviewer)
└─ NO → Continue

Is it a tool/utility?
├─ YES → Use Tool/Utility (toolkit, helper)
└─ NO → Use Concept/Framework or Metaphorical
```

## Length Guidelines

### Ultra-Short (3-5 letters)
**Best for**: Frequently used skills, human names
- `max`, `sage`, `alex`, `sam`
- Easy to type, memorable
- Use when simplicity is paramount

### Short (6-10 letters)
**Best for**: Most skills, single-word names
- `builder`, `planner`, `compass`
- Good balance of clarity and brevity
- Recommended default length

### Medium (11-15 letters)
**Best for**: Compound names, specific tools
- `code-builder`, `test-runner`
- Clear and descriptive
- Use when specificity needed

### Long (16-20 letters)
**Best for**: Very specific or complex skills
- `api-documentation-generator`
- Maximum clarity
- Use sparingly, only when necessary

## Multi-Word Naming

### Two-Word Pattern
**Format**: `[adjective/domain]-[noun]`

**Examples**:
- `smart-builder` - Intelligent code building
- `quick-analyzer` - Fast analysis
- `deep-explorer` - Thorough exploration
- `auto-formatter` - Automatic formatting

### Three-Word Pattern (Avoid if possible)
**Format**: `[domain]-[action]-[object]`

**Examples**:
- `api-doc-generator` - API documentation generator
- `code-quality-checker` - Code quality checker

**Note**: Three words often too long; consider abbreviation or simplification

## Cultural Considerations

### Universal Names
Names that work across cultures:
- Simple English words
- Common human names
- Universal metaphors (sun, moon, star)

### Avoid
- Culture-specific references
- Puns that don't translate
- Idioms or slang
- Regional terminology

## Testing Your Name

### The 5-Second Test
Can someone:
1. Spell it correctly after hearing it once?
2. Pronounce it correctly after seeing it once?
3. Remember it after 5 minutes?
4. Understand what it does from the name?
5. Type it quickly without errors?

If YES to 4-5: Excellent name
If YES to 3: Good name
If YES to 1-2: Reconsider

### The Collision Test
Check against existing skills:
- Is it too similar to existing names?
- Could it be confused with another skill?
- Does it conflict with common commands?

## Real-World Examples

### Good Names
- `commit` - Clear action, universally understood
- `review-pr` - Specific purpose, easy to understand
- `pdf` - Domain-specific, short
- `max` - Simple, memorable, metaphorical

### Names to Avoid
- `super-advanced-ai-powered-code-generator` - Too long
- `xtrm-optmzr` - Hard to spell/pronounce
- `thing-doer` - Too vague
- `mnemosyne` - Hard to spell for most users

## Renaming Guidelines

When to rename:
- Name doesn't reflect current functionality
- Users consistently misspell it
- Too similar to another skill
- Feedback indicates confusion

How to rename:
1. Announce deprecation of old name
2. Support both names temporarily
3. Update all documentation
4. Communicate change to users
5. Remove old name after transition period
