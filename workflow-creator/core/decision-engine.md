# Workflow Intelligence Decision Engine

## Purpose
Automatically determine optimal command metadata: category, complexity, MCP servers, and personas.

## Input Format
- Workflow description and goals
- Detected graph patterns
- Dependency analysis
- Parallelization plan

## Decision Dimensions

### 1. Category Classification

**Decision Tree**:
```python
def determine_category(workflow):
    if has_pattern(workflow, 'flow') and involves_transformation(workflow):
        return 'workflow'

    if has_pattern(workflow, 'looping') or has_keyword(workflow, 'retry|repeat'):
        return 'automation'

    if involves_data_analysis(workflow) or has_keyword(workflow, 'analyze|check|verify'):
        return 'analysis'

    if involves_code_generation(workflow) or has_keyword(workflow, 'generate|create|build'):
        return 'generation'

    if has_keyword(workflow, 'deploy|release|publish'):
        return 'deployment'

    if has_keyword(workflow, 'test|verify|validate'):
        return 'testing'

    if has_keyword(workflow, 'fix|update|maintain|clean'):
        return 'maintenance'

    if has_pattern(workflow, 'nesting') or has_multiple_workflows(workflow):
        return 'orchestration'

    return 'workflow'  # Default
```

**Categories**:
- **workflow**: General multi-step processes
- **automation**: Repetitive tasks with retry logic
- **analysis**: Investigation and reporting workflows
- **generation**: Code/document/asset creation
- **deployment**: Release and deployment pipelines
- **testing**: Quality assurance workflows
- **maintenance**: Cleanup and update operations
- **orchestration**: Complex multi-workflow coordination

---

### 2. Complexity Assessment

**Scoring System** (0-1 scale, weighted):

```python
def calculate_complexity(workflow, graph, parallel_plan):
    # Factor 1: Step Count (30% weight)
    step_count = len(graph['nodes'])
    step_score = min(step_count / 20, 1.0)  # Normalize: 20+ steps = 1.0

    # Factor 2: Dependency Complexity (25% weight)
    dependency_score = assess_dependency_complexity(graph)
    # Simple linear: 0.25
    # Tree structure: 0.5
    # Complex DAG: 0.75
    # Graph with conditions: 1.0

    # Factor 3: Tool Diversity (20% weight)
    required_tools = estimate_required_tools(workflow)
    tool_score = min(len(required_tools) / 8, 1.0)  # Normalize: 8+ tools = 1.0

    # Factor 4: Error Handling (15% weight)
    error_handling_score = assess_error_handling(workflow)
    # No handling: 0.0
    # Basic retry: 0.25
    # Partial recovery: 0.5
    # Rollback capability: 0.75
    # Complete compensation: 1.0

    # Factor 5: State Management (10% weight)
    state_score = assess_state_management(workflow)
    # Stateless: 0.0
    # Local state: 0.25
    # Shared state: 0.5
    # Persistent state: 0.75
    # Distributed state: 1.0

    total_score = (
        step_score * 0.30 +
        dependency_score * 0.25 +
        tool_score * 0.20 +
        error_handling_score * 0.15 +
        state_score * 0.10
    )

    return total_score
```

**Complexity Levels**:
```python
def classify_complexity(score):
    if score < 0.3:
        return 'simple'
    elif score < 0.6:
        return 'standard'
    elif score < 0.85:
        return 'complex'
    else:
        return 'high'
```

---

### 3. MCP Server Selection

**Selection Rules**:

```python
def select_mcp_servers(workflow, detected_patterns):
    servers = []

    # Rule 1: UI/Frontend Tasks
    if has_ui_tasks(workflow):
        servers.append('magic')
        servers.append('context7')  # For framework docs

    # Rule 2: Browser/Testing Tasks
    if has_testing_tasks(workflow) or has_browser_tasks(workflow):
        servers.append('playwright')

    # Rule 3: Complex Analysis
    if complexity >= 'complex' or has_pattern(workflow, 'nesting'):
        servers.append('sequential')

    # Rule 4: Code Navigation/Refactoring
    if has_code_manipulation(workflow):
        servers.append('serena')

    # Rule 5: Documentation Lookup
    if needs_framework_docs(workflow):
        servers.append('context7')

    # Rule 6: Default for complex workflows
    if not servers and complexity >= 'standard':
        servers.append('sequential')

    return servers
```

**Tool Matrix**:
| Workflow Type | Primary Tools | Optional Tools |
|---------------|---------------|----------------|
| UI Generation | magic, context7 | playwright (testing) |
| Testing | playwright | sequential (complex), serena (code) |
| Analysis | sequential | serena (code analysis) |
| Code Refactor | serena | sequential (planning) |
| Documentation | context7 | - |
| Complex Multi-Step | sequential | others as needed |

**Combination Rules**:
```yaml
magic_with_context7:
  when: ui_component_generation
  reason: "Magic generates components, Context7 provides framework docs"

playwright_with_magic:
  when: ui_testing
  reason: "Magic creates UI, Playwright tests it"

sequential_with_serena:
  when: complex_code_analysis
  reason: "Sequential plans, Serena executes code operations"

sequential_as_coordinator:
  when: complexity >= 'complex'
  reason: "Sequential coordinates multiple specialized tools"
```

---

### 4. Persona Selection

**Selection Algorithm**:

```python
def select_personas(workflow, mcp_servers, category):
    personas = []

    # Domain-based selection
    if category == 'deployment' or has_keyword(workflow, 'deploy|release'):
        personas.append('devops-architect')

    if category == 'testing' or has_testing_tasks(workflow):
        personas.append('qa-specialist')

    if involves_security(workflow) or complexity >= 'complex':
        personas.append('security-engineer')

    if has_ui_tasks(workflow) or 'magic' in mcp_servers:
        personas.append('frontend-architect')

    if has_backend_tasks(workflow) or has_api_tasks(workflow):
        personas.append('backend-architect')

    if category == 'analysis' or has_analysis_tasks(workflow):
        personas.append('system-analyst')

    if complexity >= 'complex' or has_architectural_decisions(workflow):
        personas.append('system-architect')

    # Limit to 7 personas (practical maximum)
    if len(personas) > 7:
        personas = prioritize_personas(personas, workflow)[:7]

    # Ensure at least one persona
    if not personas:
        personas.append('general-purpose')

    return personas
```

**Persona Categories**:

| Category | Personas |
|----------|----------|
| Architecture | system-architect, backend-architect, frontend-architect |
| Implementation | developer, frontend-developer, backend-developer |
| Quality | qa-specialist, security-engineer, performance-engineer |
| Specialized | devops-architect, data-engineer, ml-engineer |
| Analysis | system-analyst, requirements-analyst |

**Auto-Include Rules**:
```yaml
frontend-architect:
  when: "'magic' in mcp_servers"
  priority: high

security-engineer:
  when: "complexity >= 'complex'"
  priority: medium

system-architect:
  when: "has_architectural_decisions or complexity == 'high'"
  priority: high

devops-architect:
  when: "category == 'deployment'"
  priority: high
```

---

## Decision Workflow

### Phase 1: Initial Assessment
```python
assessment = {
    'workflow_type': identify_workflow_type(workflow),
    'primary_domain': identify_primary_domain(workflow),
    'key_patterns': detected_patterns,
    'task_types': extract_task_types(workflow)
}
```

### Phase 2: Complexity Calculation
```python
complexity_score = calculate_complexity(
    workflow=workflow,
    graph=dependency_graph,
    parallel_plan=parallelization_plan
)
complexity_level = classify_complexity(complexity_score)
```

### Phase 3: Resource Selection
```python
# Select MCP servers
mcp_servers = select_mcp_servers(workflow, detected_patterns)

# Select personas
personas = select_personas(
    workflow=workflow,
    mcp_servers=mcp_servers,
    category=category
)
```

### Phase 4: Validation & Refinement
```python
# Ensure consistency
if 'magic' in mcp_servers and 'frontend-architect' not in personas:
    personas.insert(0, 'frontend-architect')

if 'playwright' in mcp_servers and 'qa-specialist' not in personas:
    personas.append('qa-specialist')

# Check for conflicts
validate_tool_persona_compatibility(mcp_servers, personas)
```

---

## Output Format

```yaml
command_metadata:
  category: "deployment"
  complexity: "complex"
  complexity_score: 0.72
  complexity_breakdown:
    step_count: 0.25  # (10 steps / 20 * 0.30)
    dependency: 0.1875  # (0.75 * 0.25)
    tool_diversity: 0.10  # (4 tools / 8 * 0.20)
    error_handling: 0.1125  # (0.75 * 0.15)
    state_management: 0.05  # (0.5 * 0.10)

  mcp-servers: ["sequential", "playwright", "serena"]
  mcp_rationale:
    sequential: "Complex multi-step coordination and analysis"
    playwright: "Automated testing and verification"
    serena: "Code manipulation and refactoring"

  personas: ["devops-architect", "system-architect", "security-engineer", "qa-specialist"]
  persona_rationale:
    devops-architect: "Primary: deployment category"
    system-architect: "Complex workflow requiring architectural oversight"
    security-engineer: "Auto-include for complex workflows"
    qa-specialist: "Testing and validation requirements"

decision_confidence:
  category: 0.95
  complexity: 0.88
  mcp_servers: 0.82
  personas: 0.79
  overall: 0.86
```

---

## Special Cases

### Case 1: Minimal Workflow
```yaml
scenario: Single node, no special patterns
decisions:
  category: "workflow"
  complexity: "simple"
  mcp-servers: []  # No special tools needed
  personas: ["general-purpose"]
```

### Case 2: Pure UI Workflow
```yaml
scenario: Only UI component generation
decisions:
  category: "generation"
  complexity: "simple" or "standard"
  mcp-servers: ["magic", "context7"]
  personas: ["frontend-architect"]
```

### Case 3: Complex Orchestration
```yaml
scenario: Multiple nested workflows, high complexity
decisions:
  category: "orchestration"
  complexity: "high"
  mcp-servers: ["sequential", "serena", "magic", "playwright"]
  personas: ["system-architect", "devops-architect", "frontend-architect",
             "backend-architect", "security-engineer", "qa-specialist"]
```

### Case 4: Testing-Focused
```yaml
scenario: Primarily testing and validation
decisions:
  category: "testing"
  complexity: "standard"
  mcp-servers: ["playwright", "sequential"]
  personas: ["qa-specialist", "security-engineer"]
```

---

## Confidence Scoring

Rate decision confidence:

```python
def calculate_decision_confidence(workflow, decisions):
    confidence = {}

    # Category confidence
    category_keywords = count_category_keywords(workflow, decisions['category'])
    confidence['category'] = min(category_keywords / 3, 1.0)

    # Complexity confidence
    complexity_variance = calculate_scoring_variance(decisions['complexity_breakdown'])
    confidence['complexity'] = 1.0 - complexity_variance

    # MCP confidence
    tool_match_score = count_matched_rules(workflow, decisions['mcp-servers'])
    confidence['mcp_servers'] = tool_match_score / len(decisions['mcp-servers']) if decisions['mcp-servers'] else 1.0

    # Persona confidence
    persona_match_score = count_matched_rules(workflow, decisions['personas'])
    confidence['personas'] = persona_match_score / len(decisions['personas'])

    confidence['overall'] = sum(confidence.values()) / len(confidence)

    return confidence
```

---

## Usage in Workflow Creation

```
Parallel Optimizer Output
    ↓
Decision Engine (determine metadata)
    ↓
Complete Command Metadata
    ↓
Command Generator (create executable command)
```

These intelligent decisions ensure generated commands have:
- Accurate categorization for discoverability
- Appropriate complexity rating for resource allocation
- Optimal tool selection for task execution
- Relevant expert personas for specialized knowledge

## How Claude Should Use This

**When to Use**: This is Step 5 in the Workflow Creation Protocol (see SKILL.md).

**Input**: All previous analysis outputs (tasks, patterns, DAG, parallelization)

**Execution Steps**:

1. **Determine Category**: Match workflow domain keywords to 8 categories (workflow, automation, analysis, generation, deployment, testing, maintenance, orchestration)

2. **Calculate Complexity Score** using 5-factor formula:
   ```
   complexity = (
     step_count_score × 0.30 +
     dependency_score × 0.25 +
     tool_diversity_score × 0.20 +
     error_handling_score × 0.15 +
     state_management_score × 0.10
   )
   ```
   - simple: < 0.3
   - standard: 0.3 - 0.6
   - complex: 0.6 - 0.85
   - high: ≥ 0.85

3. **Select MCP Servers**: Apply rules based on task types:
   - UI tasks → magic + context7
   - Testing → playwright
   - Complex analysis → sequential
   - Code operations → serena
   - Complex workflows → sequential (coordinator)

4. **Choose Personas**: Match based on domain + complexity:
   - Extract domain keywords (frontend, backend, deployment, testing, security)
   - Add base personas for domain
   - Add senior personas for high complexity (system-architect, security-engineer)

5. **Extract Capabilities** (新增 Step 5A):
   - Read `core/capability-extractor.md`
   - Extract pattern-based capabilities (parallel-coordinator, conditional-router, etc.)
   - Extract domain-based capabilities (deployment-orchestrator, health-monitor, etc.)
   - Extract integration capabilities (api-integrator, service-connector, etc.)
   - Calculate reusability scores for each capability
   - Output: List of required capabilities with confidence and reusability scores

6. **Check Capability Library** (新增 Step 5B):
   - Read `core/capability-library.md`
   - Scan `~/.claude/agents/capabilities/` directory
   - Match required capabilities against existing agents
   - Calculate coverage scores for matches
   - Identify gaps and missing capabilities
   - Output: Match results (existing, missing, partial)

7. **Make Creation Decision** (修改 Step 5C):
   - **旧逻辑 ❌**: `if complexity >= 'complex': create agent`
   - **新逻辑 ✅**: 基于能力库检查结果决定
   - 复用现有能力 (coverage >= 0.85)
   - 创建缺失的通用能力 (reusability >= 0.7)
   - 内联低可复用性逻辑 (reusability < 0.7)
   - Output: Creation decisions (reuse, create, inline)

8. **Format Output** in YAML

**Example Execution (新流程)**:

Input summary:
- 7 tasks, parallel + branch patterns, deployment domain, moderate complexity

Your decisions:
```yaml
decisions:
  category: "deployment"
  complexity: 0.65
  complexity_level: "complex"
  mcp_servers: ["sequential", "playwright"]
  personas: ["devops-architect", "qa-specialist", "security-engineer"]

  # 新增：能力分析
  extracted_capabilities:
    - name: "deployment-orchestrator"
      confidence: 0.92
      reusability: 0.95
    - name: "parallel-coordinator"
      confidence: 0.88
      reusability: 0.98
    - name: "health-monitor"
      confidence: 0.85
      reusability: 0.90

  # 新增：能力库检查
  library_check:
    existing:
      - deployment-orchestrator (coverage: 0.95)
    missing:
      - health-monitor (reusability: 0.90)
    partial: []

  # 修改：创建决策（能力导向）
  capability_decisions:
    reuse:
      - deployment-orchestrator
    create:
      - name: health-monitor
        type: capability
        category: domain
        reusability: 0.90
        rationale: "通用健康监控能力缺失，可被多个部署/测试工作流复用"
    inline: []
```

**Next Step**: Use these decisions in SKILL.md Step 7 to compile the comprehensive plan for user approval.
