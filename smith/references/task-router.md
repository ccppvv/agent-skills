# Task Router Logic

## Task Classification System

### Primary Categories

#### 1. Code Development Tasks
**Indicators**: "implement", "refactor", "fix bug", "add feature", "optimize"
**Route to**:
- Simple edits → Native Edit/Write tools
- Symbol operations → Serena MCP
- Pattern-based edits → Morphllm MCP (if >3 files)
- Architecture changes → Sequential MCP for analysis first

**Examples**:
- "Fix the authentication bug" → Debug + Edit
- "Rename getUserData everywhere" → Serena MCP
- "Update all console.log to logger" → Morphllm MCP

#### 2. UI/Frontend Tasks
**Indicators**: "create UI", "build component", "design interface", "responsive"
**Route to**: Magic MCP (21st.dev patterns)

**Examples**:
- "Create a login form" → Magic MCP
- "Build a responsive navbar" → Magic MCP
- "Add a data table with sorting" → Magic MCP

#### 3. Research & Analysis Tasks
**Indicators**: "research", "investigate", "analyze", "explore", "understand"
**Route to**:
- Current information → WebSearch or deep-research agent
- Official docs → Context7 MCP
- Codebase structure → Explore agent
- Complex analysis → Sequential MCP

**Examples**:
- "Research React 18 features" → Context7 MCP
- "Analyze the authentication flow" → Sequential MCP
- "What's the latest in AI?" → deep-research agent

#### 4. Testing & Validation Tasks
**Indicators**: "test", "validate", "verify", "check accessibility"
**Route to**: Playwright MCP (E2E testing)

**Examples**:
- "Test the login flow" → Playwright MCP
- "Validate accessibility" → Playwright MCP
- "Check responsive design" → Playwright MCP

#### 5. Documentation Tasks
**Indicators**: "document", "write docs", "explain", "create guide"
**Route to**: Native Claude with Context7 for patterns

#### 6. Deployment & Infrastructure
**Indicators**: "deploy", "CI/CD", "infrastructure", "cloud"
**Route to**: Sequential MCP for planning + Native execution

#### 7. Memory & Session Management
**Indicators**: "save progress", "load context", "remember", "/sc:load", "/sc:save"
**Route to**: Serena MCP

## Task Complexity Scoring

Calculate complexity score (1-10) to determine execution strategy:

### Complexity Factors

```yaml
Base Score: 1

File Operations:
  +1: Single file modification
  +2: 2-5 files
  +3: 6-10 files
  +4: >10 files

Architectural Impact:
  +2: Requires understanding system architecture
  +3: Changes core abstractions
  +4: Multi-service changes

External Dependencies:
  +1: Uses existing APIs
  +2: Integrates new service
  +3: Multi-service orchestration

Risk Level:
  +1: Development environment only
  +2: Staging/testing changes
  +3: Production impact possible

User Specification:
  +3: User explicitly requests "全力以赴" / "spare no effort"
  +2: User requests thorough analysis
```

### Complexity-Based Strategy

```
Score 1-3 (Simple):
├─ Model: Current (Sonnet 4.5)
├─ Tools: Direct native tools
└─ Planning: Brief outline

Score 4-6 (Medium):
├─ Model: Current, suggest Opus 4.5
├─ Tools: Specialized MCPs as needed
└─ Planning: Structured plan with phases

Score 7-10 (Complex):
├─ Model: Auto-recommend Opus 4.5
├─ Tools: Sequential + specialized MCPs
└─ Planning: Detailed multi-phase plan with checkpoints
```

## Model Selection Logic

### When to Suggest Opus 4.5

**Auto-recommend** (strong suggestion):
- Complexity score ≥7
- Architectural analysis required
- Multi-system integration
- User explicitly requests maximum capability

**Suggest** (user decides):
- Complexity score 4-6
- Complex debugging needed
- Performance optimization required
- Strategic decision-making

**Current model sufficient**:
- Complexity score ≤3
- Simple CRUD operations
- Straightforward implementations
- Clear requirements

### Recommendation Format

```markdown
⚙️ Task Complexity: [Score]/10

📊 Analysis:
- [Factor 1]: +[points]
- [Factor 2]: +[points]

💡 Model Recommendation:
For optimal results, I recommend switching to Claude Opus 4.5 because:
- [Reason 1]
- [Reason 2]

Would you like to:
1. ✅ Switch to Opus 4.5 (recommended)
2. 🔄 Continue with current model
```

## Tool Selection Matrix

| Task Type | Primary Tool | Alternative | When to Use Alternative |
|-----------|-------------|-------------|------------------------|
| Simple code edit | Edit/Write | MultiEdit | If >3 related files |
| Symbol operations | Serena MCP | Grep + Edit | If LSP unavailable |
| Pattern replacement | Morphllm MCP | MultiEdit | If <3 files |
| UI components | Magic MCP | Manual | If custom framework |
| Documentation lookup | Context7 MCP | WebSearch | If unofficial info needed |
| Browser testing | Playwright MCP | Manual | If simple validation |
| Deep analysis | Sequential MCP | Native | If straightforward logic |
| Code search | Explore agent | Grep/Glob | If needle-in-haystack |

## Execution Mode Selection

Based on task characteristics, choose execution mode:

### 🐌 Cautious Mode
**When**:
- First time using this skill with user
- User expressed concern about automation
- High-risk operations involved
- Complexity score ≥8

**Behavior**: Request confirmation for EVERY step

### ⚡ Balanced Mode (DEFAULT)
**When**:
- Normal operations
- Medium risk/complexity
- User trusts AI judgment

**Behavior**:
- Auto-execute low-risk operations
- Show plan for medium-risk, one-click approve
- Step-by-step for high-risk

### 🚀 Autonomous Mode
**When**:
- User explicitly enabled auto-mode
- Low-risk operations only
- Established trust relationship

**Behavior**: Auto-execute all low/medium-risk operations, report results

## Decision Flow

```
User Request
    ↓
Classify Task Type
    ↓
Calculate Complexity Score
    ↓
[Score ≥ 7?] → Recommend Opus 4.5
    ↓
Select Execution Mode
    ↓
Choose Tools (Primary + Alternatives)
    ↓
Generate Plan (Adaptive Detail Level)
    ↓
Risk Assessment
    ↓
[High Risk?] → Multi-step confirmation
[Med Risk?] → Plan approval
[Low Risk?] → Auto-execute
    ↓
Execute with monitoring
    ↓
Report results + learning
```
