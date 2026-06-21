# Analysis & Plan Template

Use this template to structure task understanding and execution planning.

## Part 1: Understanding (使用 Mental Model Mentor)

### 🧠 Quick Analysis

**First Principles - 问题本质**:
- 核心需求: [用户真正想要什么]
- 关键约束: [限制条件]

**Second-Order Thinking - 后续影响**:
- 直接影响: [一阶后果]
- 间接影响: [二阶后果]
- 潜在风险: [需要注意的问题]

**Inversion - 失败场景**:
- 如何失败: [可能的失败模式]
- 如何避免: [预防措施]

---

## Part 2: Task Classification

**Task Type**: [Code/UI/Research/Testing/Documentation/Deployment/Other]

**Complexity Score**: [X]/10

**Calculation**:
```
Base: 1
+ Files: [+N points]
+ Architecture: [+N points]
+ Dependencies: [+N points]
+ Risk: [+N points]
+ User specification: [+N points]
= Total: [X]
```

**Selected Tools**:
- Primary: [Tool name]
- Alternative: [Tool name] (if needed)
- Reasoning: [Why these tools]

---

## Part 3: Model Recommendation

⚙️ **Recommended Model**: [Current/Opus 4.5]

**Reasoning**:
- [Factor 1]
- [Factor 2]

**User Choice**:
- [ ] Switch to Opus 4.5 (recommended)
- [ ] Continue with current model

---

## Part 4: Execution Plan

### Plan Detail Level: [Concise/Balanced/Detailed]

**Chosen because**: [Simple task/Medium complexity/Complex multi-phase]

---

### 📋 Execution Phases

#### Phase 1: [Phase Name] [Risk: 🟢/🟡/🔴]

**Objective**: [What this phase accomplishes]

**Steps**:
1. [Specific action 1]
   - Tool: [Tool name]
   - Expected output: [What you'll get]

2. [Specific action 2]
   - Tool: [Tool name]
   - Expected output: [What you'll get]

**Success Criteria**: [How to know phase succeeded]

**Rollback Plan**: [How to undo if needed]

---

#### Phase 2: [Phase Name] [Risk: 🟢/🟡/🔴]

**Objective**: [What this phase accomplishes]

**Steps**:
1. [Specific action 1]
2. [Specific action 2]

**Success Criteria**: [How to know phase succeeded]

**Rollback Plan**: [How to undo if needed]

---

### 🎯 Overall Success Metrics

**Definition of Done**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Validation**:
- [ ] Tests pass
- [ ] No regressions
- [ ] Documentation updated (if needed)

---

## Part 5: Risk Assessment

### Pre-execution Checklist

```markdown
□ Operation not in NEVER list
□ Backup/rollback plan exists
□ Impact scope assessed
□ User authorized execution
□ Critical data backed up (if needed)
```

### Risk Breakdown

**🟢 Low Risk Operations**:
- [List operations that auto-execute]

**🟡 Medium Risk Operations**:
- [List operations needing plan approval]

**🔴 High Risk Operations**:
- [List operations needing step-by-step confirmation]

---

## Part 6: User Authorization

### Execution Mode: [🐌 Cautious / ⚡ Balanced / 🚀 Autonomous]

**Authorization Request**:

```markdown
I've analyzed your request and created the plan above.

📊 Summary:
- Complexity: [X]/10
- Risk level: [Low/Medium/High]
- Estimated phases: [N]
- Tools: [List]

🎯 What I'll do:
[One-sentence summary of the plan]

⚙️ How to proceed:
1. ✅ Full approval - Execute entire plan (I'll pause before high-risk steps)
2. 📋 Phase-by-phase - I'll ask for approval after each phase
3. 🛠️ Step-by-step - I'll confirm every action
4. ✏️ Modify plan - Tell me what to change

Please choose [1/2/3/4]:
```

---

## Part 7: Execution Tracking

### Progress Updates

Update after each significant step:

```markdown
✅ Completed: [Step description]
   - Tool used: [Tool name]
   - Result: [Outcome]
   - Files affected: [List]

🔄 Next: [What's coming next]
```

### Error Handling

If error occurs:

```markdown
❌ Error in: [Step description]
   - Error: [Error message]
   - Context: [What was being attempted]
   - State: [Current state preserved]

🤔 Options:
1. Retry with adjustment: [Proposed fix]
2. Skip and continue: [Impact of skipping]
3. Rollback: [Undo recent changes]
4. Stop and reconsider: [Await your guidance]

How should I proceed?
```

---

## Template Usage Notes

**For Simple Tasks (Score 1-3)**:
- Use concise format
- Skip detailed breakdown
- Focus on direct execution

**For Medium Tasks (Score 4-6)**:
- Use balanced format
- 2-3 phases with clear steps
- Highlight key decisions

**For Complex Tasks (Score 7-10)**:
- Use detailed format
- Multiple phases with dependencies
- Comprehensive risk analysis
- Regular checkpoints
