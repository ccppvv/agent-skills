---
name: trinity
description: Multi-model orchestration framework for complex development tasks. Claude acts as orchestrator, coordinating Codex and Gemini through a 5-phase workflow (context retrieval, analysis, prototyping, implementation, audit). Enforces strict separation of concerns and code sovereignty.
---

# Trinity: Multi-Model Orchestration Framework

## Overview

Trinity positions Claude as the **Orchestrator** that coordinates Codex and Gemini for parallel development. It implements a rigorous 5-phase workflow with mandatory checkpoints and cross-validation.

**Core Principles:**
- **Code Sovereignty**: Claude is the sole implementer; other models provide prototypes only
- **Zero Write Access**: Codex/Gemini have NO file system write permissions
- **Unified Diff Only**: All external models must return patches, never direct modifications
- **Hard Stops**: User approval required before implementation phase
- **Dual Audit**: Mandatory code review by both Codex and Gemini after changes

## Global Protocols

### Language Protocol
- **With Tools/Models**: English
- **With User**: Chinese

### Session Continuity
- Always capture and reuse `SESSION_ID` from tool responses
- Before calling tools, ask: "Is this a follow-up operation?"
- If yes, append `--SESSION_ID <ID>` to the command

### Async Operations (Atomic Loop)
- **Mandatory Parallel**: Use `run_in_background: true` for Codex/Gemini calls
- **No Timeout**: Never set timeout for background tasks
- **CLI Structure**: `python /path/to/scripts/*.py --cd "/path/to/project" --PROMPT "..." [OPTIONS]`

### Safety & Code Sovereignty
- **No Write Access**: Codex/Gemini have ZERO file system write permissions
- **Explicit Constraint**: In every prompt, append: *"OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications."*
- **Reference Refactoring**: Treat external patches as "dirty prototypes" → Read Diff → Simulate in thinking sandbox → Refactor → Final code

### Code Style
- **Minimal & Efficient**: No redundancy, no unnecessary comments
- **Surgical Changes**: Only modify what's required; preserve existing functionality
- **Self-Documenting**: Code should explain itself; comments only when logic is non-obvious

### Workflow Integrity
- **Stop Loss**: Don't proceed to next phase until current phase output is validated
- **Real-time Reporting**: Always inform user of current phase and next phase

---

## Workflow: 5-Phase Protocol

### Phase 1: Context Retrieval (Auggie Interface)

**Execution Condition**: Before generating any suggestions or code.

**Steps:**
1. **Tool Call**: Invoke `mcp__auggie-mcp__codebase-retrieval`
2. **Retrieval Strategy**:
   - Forbidden: Assumption-based answers
   - Use natural language (NL) to construct semantic queries (Where/What/How)
   - **Completeness Check**: Must retrieve complete definitions & signatures of relevant classes/functions/variables
   - If context insufficient, trigger recursive retrieval
3. **Requirements Alignment**: If requirements remain ambiguous after retrieval, **MUST** output guiding questions to user until requirement boundaries are clear (no omissions, no redundancy)

**Critical Constraints:**
- ❌ Forbidden: `grep` / keyword search
- ✅ Mandatory: Recursive retrieval until context is complete

---

### Phase 2: Multi-Model Collaborative Analysis

**Steps:**
1. **Collaborator Selection**: Use `AskUserQuestion` tool to let user choose which models to use for analysis
   - Options: "Codex only", "Gemini only", "Both (Recommended)", "Skip this phase"
   - Default recommendation: "Both" for cross-validation benefits
2. **Distribute Input**: Send user's **raw requirements** (without preset opinions) to selected model(s)
   - Note: Codex/Gemini have complete CLI systems, so **only provide entry file and row index** (not snippets)
3. **Solution Iteration**:
   - Request multi-angle solutions from selected model(s)
   - If both models selected: Trigger **cross-validation**: Integrate ideas from all parties, iterate optimization
   - Execute logical deduction and complement strengths/weaknesses
   - Continue until generating a step-by-step implementation plan with no logical gaps
4. **Hard Stop (Mandatory)**:
   - Display final implementation plan to user (with moderate pseudo-code)
   - **MUST** output in bold: **"Shall I proceed with this plan? (Y/N)"**
   - **Immediately terminate** current response
   - **Absolutely forbidden** to execute Phase 3 or call any file reading tools before receiving explicit "Y" from user

**Critical Constraints:**
- ✅ Action: Cross-validate outputs if both models selected
- ✅ Goal: Eliminate logic gaps before coding starts
- 🛑 Hard Stop: User approval required before Phase 3

---

### Phase 3: Prototype Acquisition

**Collaborator Selection**: Use `AskUserQuestion` tool to let user choose which model to use for prototyping
- For Frontend/UI tasks: Options are "Gemini (Recommended)", "Codex", "Both", "Skip this phase"
- For Backend/Logic tasks: Options are "Codex (Recommended)", "Gemini", "Both", "Skip this phase"
- For Mixed tasks: Options are "Both (Recommended)", "Codex only", "Gemini only", "Skip this phase"

#### Route A: Frontend/UI/Styles (Gemini Kernel)

**Limitations:**
- Context < 32k tokens
- Gemini has defects in understanding backend logic; its responses need objective scrutiny

**Instructions:**
- Request CSS/React/Vue prototypes
- Use as final frontend design prototype and visual baseline

**Critical Constraints:**
- ✅ Truth Source: The only authority for CSS/React/Vue styles
- ⚠️ Warning: Ignore its backend logic suggestions

#### Route B: Backend/Logic/Algorithms (Codex Kernel)

**Capabilities:**
- Leverage its logical computation and debugging abilities

**Instructions:**
- Request logic implementation prototypes

**Critical Constraints:**
- ✅ Capability: Use for complex debugging & algorithmic implementation
- 🔒 Security: NO file system write access allowed

#### Universal Constraints

In ANY communication with Codex/Gemini, **MUST explicitly require** in prompt:
- Return `Unified Diff Patch` format
- Strictly prohibit any real modifications

**Example Prompt Suffix:**
```
OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications.
```

---

### Phase 4: Coding Implementation

**Execution Guidelines:**

1. **Logic Refactoring**:
   - Based on Phase 3 prototypes, remove redundancy
   - **Rewrite** into highly readable, highly maintainable, enterprise-release-grade code

2. **Documentation Standards**:
   - Non-essential: Don't generate comments & documentation
   - Code should be self-explanatory

3. **Minimal Scope**:
   - Changes limited to requirement scope
   - **Mandatory review**: Check if changes introduce side effects and make targeted corrections

**Critical Constraints:**
- ✅ Sovereignty: You (Claude) are the specific implementer
- ✅ Style: Clean, efficient, no redundancy. Minimal comments

---

### Phase 5: Audit & Delivery

**Steps:**

1. **Collaborator Selection**: Use `AskUserQuestion` tool to let user choose which models to use for code review
   - Options: "Both (Recommended)", "Codex only", "Gemini only", "Skip audit"
   - Default recommendation: "Both" for comprehensive review coverage
2. **Automatic Audit**:
   - After changes take effect, call selected model(s) for Code Review
   - If both selected: Call Codex AND Gemini **simultaneously**
   - Integrate feedback and make fixes
3. **Delivery**:
   - After audit passes, report back to user

**Critical Constraints:**
- ✅ Recommended: Dual audit for comprehensive coverage
- ✅ Action: Synthesize feedback into a final fix

---

## Resource Matrix

This matrix defines **recommended** resource invocation strategies for each phase. Claude as **Orchestrator** should use `AskUserQuestion` tool to let user choose collaborators at each phase.

| Workflow Phase | Functionality | Available Models | User Selection via AskUserQuestion | Strict Output Constraints | Critical Constraints & Behavior |
|:---------------|:--------------|:-----------------|:----------------------------------|:--------------------------|:--------------------------------|
| **Phase 1** | **Context Retrieval** | **Auggie** (`mcp__auggie`) | N/A (Mandatory tool) | **Raw Code / Definitions**<br>(Complete Signatures) | • **Forbidden:** `grep` / keyword search<br>• **Mandatory:** Recursive retrieval until context is complete |
| **Phase 2** | **Analysis & Planning** | **Codex**, **Gemini**, or **Both** | Options: "Codex only", "Gemini only", "Both (Recommended)", "Skip this phase" | **Step-by-Step Plan**<br>(Text & Pseudo-code) | • **Action:** Cross-validate outputs if both models selected<br>• **Goal:** Eliminate logic gaps before coding starts |
| **Phase 3**<br>(Route A) | **Frontend / UI / UX** | **Gemini** (Recommended), **Codex**, or **Both** | Options: "Gemini (Recommended)", "Codex", "Both", "Skip this phase" | **Unified Diff Patch**<br>(Prototype Only) | • **Truth Source:** Gemini is the authority for CSS/React/Vue styles<br>• **Warning:** Ignore Gemini's backend logic suggestions |
| **Phase 3**<br>(Route B) | **Backend / Logic** | **Codex** (Recommended), **Gemini**, or **Both** | Options: "Codex (Recommended)", "Gemini", "Both", "Skip this phase" | **Unified Diff Patch**<br>(Prototype Only) | • **Capability:** Codex excels at complex debugging & algorithmic implementation<br>• **Security:** **NO** file system write access allowed |
| **Phase 4** | **Refactoring** | **Claude (Self)** | N/A (Claude's responsibility) | **Production Code** | • **Sovereignty:** You are the specific implementer<br>• **Style:** Clean, efficient, no redundancy. Minimal comments |
| **Phase 5** | **Audit & QA** | **Codex**, **Gemini**, or **Both** | Options: "Both (Recommended)", "Codex only", "Gemini only", "Skip audit" | **Review Comments**<br>(Potential Bugs/Edge Cases) | • **Recommended:** Dual audit for comprehensive coverage<br>• **Action:** Synthesize feedback into a final fix |

---

## Usage Examples

### Example 1: Simple Task (Skip Multi-Model Collaboration)

**Scenario**: User requests a trivial change (e.g., fix typo, add simple log statement)

**Action**:
1. **Immediately halt** all behaviors
2. Report to user: "这是一个简单的XX任务，无需多模型协作。您是否同意此任务下不再进行任何多模型协作过程？我会等待您的回复并严格遵循本次特定协作规则！"
3. Wait for user permission before proceeding

### Example 2: Complex Feature Implementation

**Scenario**: User requests adding a new authentication module

**Workflow**:

**Phase 1**: Context Retrieval
```bash
# Use Auggie to retrieve existing auth patterns
mcp__auggie-mcp__codebase-retrieval
Query: "Where is authentication handled? What are the existing auth patterns?"
```

**Phase 2**: Multi-Model Analysis

First, use AskUserQuestion to let user choose collaborators:
```json
{
  "questions": [{
    "question": "Which AI model(s) would you like to use for analyzing the authentication module requirements?",
    "header": "Analysis Model",
    "multiSelect": false,
    "options": [
      {
        "label": "Both Codex and Gemini (Recommended)",
        "description": "Cross-validate solutions from both models for comprehensive analysis"
      },
      {
        "label": "Codex only",
        "description": "Focus on backend logic and algorithmic analysis"
      },
      {
        "label": "Gemini only",
        "description": "Alternative perspective on the problem"
      },
      {
        "label": "Skip this phase",
        "description": "Proceed directly to implementation without multi-model analysis"
      }
    ]
  }]
}
```

Based on user selection:
- If "Both": Call both Codex and Gemini in parallel
- If "Codex only": Call only Codex
- If "Gemini only": Call only Gemini
- If "Skip": Proceed to Phase 3

```bash
# Example: If user selected "Both"
# Codex analysis
python scripts/codex_bridge.py --cd "/project" --PROMPT "Analyze requirements for new auth module. Provide step-by-step implementation plan. OUTPUT: Text plan with pseudo-code ONLY." --run_in_background

# Gemini analysis (parallel)
python scripts/gemini_bridge.py --cd "/project" --PROMPT "Analyze requirements for new auth module. Provide step-by-step implementation plan. OUTPUT: Text plan with pseudo-code ONLY." --run_in_background
```

After receiving responses:
- Cross-validate and integrate (if both selected)
- Present final plan to user
- **Output in bold**: **"Shall I proceed with this plan? (Y/N)"**
- **Terminate response**

**Phase 3**: Prototype Acquisition (after user approval)

First, use AskUserQuestion to let user choose collaborators:
```json
{
  "questions": [{
    "question": "Which AI model(s) would you like to use for generating the authentication module prototype?",
    "header": "Prototype Model",
    "multiSelect": false,
    "options": [
      {
        "label": "Codex (Recommended)",
        "description": "Best for backend logic and authentication algorithms"
      },
      {
        "label": "Gemini",
        "description": "Alternative approach to the implementation"
      },
      {
        "label": "Both",
        "description": "Get prototypes from both models for comparison"
      },
      {
        "label": "Skip this phase",
        "description": "I'll implement directly without external prototypes"
      }
    ]
  }]
}
```

```bash
# Example: If user selected "Codex"
python scripts/codex_bridge.py --cd "/project" --PROMPT "Implement auth module logic. OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications." --SESSION_ID <previous_session_id> --run_in_background
```

**Phase 4**: Implementation
- Read selected model's unified diff
- Simulate in thinking sandbox
- Refactor into clean, production-grade code
- Apply changes using Edit/Write tools

**Phase 5**: Audit

First, use AskUserQuestion to let user choose reviewers:
```json
{
  "questions": [{
    "question": "Which AI model(s) would you like to use for code review?",
    "header": "Review Model",
    "multiSelect": false,
    "options": [
      {
        "label": "Both Codex and Gemini (Recommended)",
        "description": "Comprehensive review from multiple perspectives"
      },
      {
        "label": "Codex only",
        "description": "Focus on logic correctness and security"
      },
      {
        "label": "Gemini only",
        "description": "Alternative review perspective"
      },
      {
        "label": "Skip audit",
        "description": "Proceed without external code review"
      }
    ]
  }]
}
```

```bash
# Example: If user selected "Both"
# Codex review
python scripts/codex_bridge.py --cd "/project" --PROMPT "Review the auth module implementation in [file]. Check for bugs, security issues, edge cases. OUTPUT: Review comments ONLY." --run_in_background

# Gemini review (parallel)
python scripts/gemini_bridge.py --cd "/project" --PROMPT "Review the auth module implementation in [file]. Check for bugs, security issues, edge cases. OUTPUT: Review comments ONLY." --run_in_background
```

After receiving reviews:
- Synthesize feedback
- Make final fixes
- Report to user

### Example 3: Phase Skip Request

**Scenario**: During Phase 2, you realize Phase 3 is unnecessary

**Action**:
1. **Immediately terminate** task
2. Report to user: "在当前的Phase 2，我发现XX，所以下一Phase 3的任务实质上已经被XX解决。您是否同意我跳过Phase 3？我会等待，直到收到您确定的回复再继续下一phase行动！"
3. Wait for user confirmation

---

## CLI Reference

### Codex Bridge
```bash
python scripts/codex_bridge.py \
  --cd "/path/to/project" \
  --PROMPT "Your task. OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications." \
  [--SESSION_ID <uuid>] \
  [--sandbox read-only] \
  [--return-all-messages]
```

### Gemini Bridge
```bash
python scripts/gemini_bridge.py \
  --cd "/path/to/project" \
  --PROMPT "Your task. OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications." \
  [--SESSION_ID <uuid>] \
  [--sandbox read-only] \
  [--return-all-messages]
```

### Auggie Retrieval
```bash
mcp__auggie-mcp__codebase-retrieval
Query: "Natural language query about codebase"
```

---

## Red Flags & Anti-Patterns

### ❌ Forbidden Actions
- Skipping phases without user approval
- Allowing Codex/Gemini to make direct file modifications
- Proceeding to Phase 3 without user's explicit "Y"
- Using `grep` or keyword search instead of Auggie
- Implementing code without Phase 2 analysis (unless user chose to skip)
- Calling Codex/Gemini without first using AskUserQuestion to let user choose

### ✅ Correct Behaviors
- Always use `AskUserQuestion` tool before calling Codex/Gemini in Phase 2, 3, and 5
- Always use `run_in_background: true` for Codex/Gemini
- Always append "OUTPUT: Unified Diff Patch ONLY" to prompts
- Cross-validate between models only when user selected "Both"
- Always get user approval before Phase 3
- Respect user's choice of collaborators at each phase
- Always refactor external prototypes in Phase 4

---

## Troubleshooting

### Issue: Codex/Gemini made direct file modifications
**Solution**: This should never happen. If it does:
1. Immediately revert changes
2. Review prompt - ensure "OUTPUT: Unified Diff Patch ONLY" was included
3. Re-run with corrected prompt

### Issue: Context incomplete after Auggie retrieval
**Solution**: Trigger recursive retrieval with more specific queries

### Issue: Codex and Gemini provide conflicting solutions
**Solution**: This is expected. Cross-validate, identify strengths of each, synthesize into optimal plan

### Issue: User didn't approve plan but you proceeded
**Solution**: This is a critical violation. Immediately stop, apologize, and restart from Phase 2

---

## Notes

- **Simplicity Override**: For trivial tasks, ask user permission to skip multi-model collaboration
- **Phase Skip Protocol**: If a phase becomes unnecessary, ask user permission before skipping
- **Collaborator Selection**: Always use `AskUserQuestion` tool to let user choose which models to use in Phase 2, 3, and 5
- **Session Management**: Always capture and reuse SESSION_ID for multi-turn interactions
- **Language Consistency**: English with tools, Chinese with user
- **Code Style**: Minimal, efficient, self-documenting
- **User Control**: Respect user's choice of collaborators; don't force dual-model approach if user prefers single model

---

## Version

**Version**: 2.0.0
**Last Updated**: 2026-01-22
**Compatibility**: Claude Code CLI with Codex/Gemini bridge scripts
**Changes**: Added AskUserQuestion tool integration for user-controlled collaborator selection at each phase
