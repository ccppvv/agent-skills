# Mental Model Mentor - Detailed Usage Guide

This guide contains comprehensive workflow details, learning paths, and troubleshooting. For quick start, see [SKILL.md](../SKILL.md).

---

## Core Workflow

### Step 1: Problem Clarification

**Goal**: Understand what you're really solving

**Key Questions**:
- What type of problem is this? (10-structure classification)

| 结构 | 核心问题 | 信号词 |
|------|---------|--------|
| 决策 | "该不该/要不要/选哪个？" | 纠结、抉择、两个方向 |
| 诊断 | "为什么/根因/怎么回事？" | 出问题、失效、越来越差 |
| 预测 | "会怎样/如果...那么？" | 趋势、后果、万一、长期 |
| 设计 | "怎么设计/怎么构建？" | 搭建、架构、从零开始 |
| 优化 | "怎么改进/提效？" | 提升、降低成本、精简 |
| 谈判 | "怎么说服/利益分配？" | 博弈、冲突、对抗 |
| 评估 | "值不值/风险收益？" | 投资回报、可行性、性价比 |
| 学习 | "怎么学/技能提升？" | 入门、进修、掌握 |
| 领导 | "怎么管/怎么带人？" | 团队、下属、文化 |
| 创新 | "新点子/差异化/突破？" | 颠覆、独特、蓝海 |

- What's the complexity?
  - 快速 (2-3 models, low-risk decisions)
  - 标准 (3-5 models, default)
  - 深度 (5-8 models, high-stakes/irreversible)

- What's the domain?
  - 个人 / 商业 / 工程 / 社会 / 学术

**Tools**:
- `python3 scripts/model_matcher.py "your problem"` for automatic routing
- First Principles (get to root cause)
- Frame from multiple angles

---

### Step 2: Model Selection

**Goal**: Choose relevant mental models via three-layer routing

**Three Approaches**:

#### Option A - Automated Three-Layer Routing (推荐)
```bash
python3 scripts/model_matcher.py "your problem description"
python3 scripts/model_matcher.py -v "problem"     # verbose debug info
```
Executes Layer 1 (structure) → Layer 2 (complexity) → Layer 3 (domain), then scores 499+ indexed models with category diversity enforcement and cross-validation.

#### Option B - Manual Browse
Browse by category:
- **Strategic decisions** → [strategic.md](../references/strategic.md)
- **Bias detection** → [cognitive.md](../references/cognitive.md)
- **Complex systems** → [systems.md](../references/systems.md)
- **Uncertainty** → [probability.md](../references/probability.md)
- **Incentives/trade-offs** → [economics.md](../references/economics.md)
- **Game theory** → [game-theory.md](../references/game-theory.md)
- **Innovation** → [innovation.md](../references/innovation.md)
- **Management** → [management.md](../references/management.md)
- All 36 categories → [references/](../references/)

#### Option C - Framework-Based
Use Five-Dimensional Analysis (strategic + systems + cognitive + probability + economic). See [frameworks.md](../references/frameworks.md)

**How Three-Layer Routing Works**:

1. **Layer 1 — Problem Structure**: Identifies which of 10 structures your problem fits, narrowing candidate categories and priority models
2. **Layer 2 — Complexity**: Auto-detects quick/standard/deep from query signals, controlling model count
3. **Layer 3 — Domain**: Identifies personal/business/engineering/social/academic, appending domain-specific categories
4. **Cross-Validation**: Checks category diversity, flags missing essential perspectives (cognitive/strategic/systems)

---

### Step 3: Structured Analysis

**Choose your depth**:

#### Quick Analysis (5-15 min / 2-3 models)
- Low-risk, reversible decisions
- Time pressure or clear problem
- Apply 2-3 most relevant models
- Best for: Familiar problems, daily decisions

#### Standard Analysis (15-30 min / 3-5 models)
- Medium risk, need multi-perspective
- Regular decision-making workflow
- Cross-validation between models
- Best for: Most common decisions, team issues

#### Deep Analysis (1-2 hours / 5-8 models)
- High-stakes, irreversible decisions
- Use Five-Dimensional Framework
- Comprehensive recommendations with full evidence chain
- Include P0/P1/P2 actions + stop-loss conditions
- Best for: Career changes, major investments, strategic pivots

**Output Formats**:
- **关键洞察** (简洁版): Bullet points, key takeaways
- **完整报告** (详细版): Full analysis with reasoning
- **决策矩阵** (可行动版): Structured comparison with scores

---

### Step 4: Synthesis & Decision

**Goal**: Convert analysis into action

**Process**:
1. **Identify convergence**: Where do models agree?
2. **Explore tensions**: Where do models disagree? (often most valuable!)
3. **Check blind spots**: What's missing?
4. **Generate options**: What are the possibilities?
5. **Decide**: Based on evidence and values
6. **Plan implementation**: With feedback loops

**Model Consistency Check**:
- **所有模型指向同一方向** → 高信心决策
- **模型有分歧** → 探索张力点，理解权衡
- **模型相互矛盾** → 价值观决定，没有"正确"答案

**Next Step Options**:
- **立即执行**: 高信心 + 高紧急度
- **收集更多信息**: 低信心 + 高影响
- **小规模试验**: 中等信心 + 高风险
- **延后决策**: 低紧急度

**Key Principle**: Don't expect models to give "the answer" - they illuminate trade-offs and help you decide wisely.

---

### Step 5: Learning & Iteration

**Goal**: Build long-term capability

**After each analysis**:
- What models were most useful?
- What insights emerged?
- What would you do differently?
- How can you apply this pattern in future?

**Learning Checklist**:
- ✅ 哪些模型最有用？
- ✅ 最大的洞察是什么？
- ✅ 下次会做什么不同？
- ✅ 如何将这个模式应用到未来？

**Practice Consistently**:
- Use worksheets for deliberate practice
- Apply models to daily decisions
- Review past decisions with model lens
- Keep a "thinking journal"

**Follow-up Actions**:
- 保存分析记录 (use Serena `write_memory()`)
- 应用到下一个类似问题
- 教授给他人 (best way to internalize)
- 创建个人模板

---

## Learning Path

### Level 1: Foundation (Start here)
**Time**: 2-3 weeks of daily practice

**Core 5 Models**:
1. First Principles
2. Second-Order Thinking
3. Confirmation Bias
4. Expected Value
5. Systems Thinking

**Activities**:
- Practice with [beginner worksheet](../assets/worksheets/)
- Use `model_matcher.py` to find relevant models
- Apply to small daily decisions
- Read model descriptions in [references/](../references/)

**Success Criteria**:
- Can explain each model in your own words
- Recognize when to apply each model
- Successfully apply to 3+ real decisions

---

### Level 2: Expansion
**Time**: 1-2 months

**Add 10 More Models** (2 from each category):
- **Strategic**: Inversion, Reversibility
- **Cognitive**: Anchoring, Framing Effect
- **Systems**: Feedback Loops, Leverage Points
- **Probability**: Base Rates, Black Swan
- **Economic**: Opportunity Cost, Incentives

**Activities**:
- Use [decision-matrix.md](../assets/templates/decision-matrix.md) for important decisions
- Practice bias detection daily
- Start teaching models to others
- Combine 2-3 models per analysis

**Success Criteria**:
- Comfortable with 15 models
- Can combine models fluidly
- Teaching others successfully

---

### Level 3: Integration
**Time**: 3-6 months

**Skills**:
- Use Five-Dimensional Framework
- Combine models fluidly
- Develop personal model toolkit
- Create custom frameworks for recurring problems

**Activities**:
- Apply frameworks to complex problems
- Document your model combinations
- Create templates for your common decisions
- Analyze past decisions with models

**Success Criteria**:
- Models feel natural, not forced
- Can handle complex multi-faceted problems
- Have personal framework library

---

### Level 4: Mastery
**Time**: 1+ years

**Characteristics**:
- Models become intuitive
- Apply unconsciously to daily thinking
- Create novel model combinations
- Teach and refine mental models

**Activities**:
- Mentor others in mental models
- Contribute new model combinations
- Write about your applications
- Develop domain-specific frameworks

**Success Criteria**:
- Models are second nature
- Others seek your analytical advice
- Can explain complex problems simply

---

## Troubleshooting

### "I don't know which models to use"

**Solutions**:
1. Run: `python3 scripts/model_matcher.py "your problem"` — three-layer routing auto-selects
2. Use the 30-second decision tree in [quick-reference.md](quick-reference.md)
3. Start with First Principles + Systems Thinking (good defaults for most problems)
4. Browse [quick-reference.md](quick-reference.md) for your problem structure type

**Why this happens**: 499+ models across 36 categories. The three-layer routing (structure × complexity × domain) narrows this down automatically. Normal for beginners to feel overwhelmed — the routing handles this.

---

### "Analysis paralysis - too many models"

**Solutions**:
1. Limit to 2-3 models maximum for quick decisions
2. Use decision deadline to force conclusion
3. Remember: "Good enough" decision > perfect analysis
4. Use Quick Analysis mode (15-30 min)

**Why this happens**: Perfectionism, fear of missing something. Models should clarify, not complicate.

**Rule of thumb**: Simple problem = 1-2 models. Complex problem = 3-5 models. Very complex = framework (but still focused).

---

### "Models point in different directions"

**This is valuable!** Reveals trade-offs.

**Solutions**:
1. Don't force agreement - explore the tension
2. Your values decide when models disagree
3. Document the trade-offs explicitly
4. Consider: Can you get benefits of both? (creative solution)

**Example**:
- Expected Value says "take the risk" (high upside)
- Loss Aversion says "avoid the risk" (fear of downside)
- **Resolution**: Your risk tolerance decides. Both models are correct.

---

### "Not sure if I'm applying models correctly"

**Solutions**:
1. Use templates (they guide application)
2. Start with practice worksheets
3. Compare your analysis with examples in [references/](../references/)
4. Ask for feedback/review
5. Teach the model to someone (reveals gaps)

**Common mistakes**:
- Applying model mechanically without understanding
- Seeking models to confirm existing beliefs
- Using model jargon without substance
- Skipping the synthesis step

---

### "Too abstract - need concrete examples"

**Solutions**:
1. Each model in [references/](../references/) has examples
2. Worksheets provide practice scenarios
3. Apply to your own recent decisions (best learning)
4. Start with simple, familiar problems

**Tip**: Abstract → Concrete is a skill. Practice by:
- Taking abstract model → finding 3 examples from your life
- Taking your decision → identifying which models apply

---

## Integration with Other Tools

### With Sequential Thinking MCP
- **Use Sequential for**: Complex multi-step reasoning, systematic decomposition
- **Use Mental Models for**: Thinking frameworks, bias checking
- **Combine**: Sequential structures the process, Mental Models provide the lenses

**Example**: Debugging complex system
1. Sequential: Break down into components
2. Mental Models: Apply Systems Thinking to understand interactions
3. Sequential: Test hypotheses systematically
4. Mental Models: Check for Confirmation Bias in interpretation

---

### With Brainstorming Skill
- **Use Brainstorming for**: Idea generation, divergent thinking
- **Use Mental Models for**: Evaluation, selection, convergent thinking

**Workflow**:
1. Brainstorm → Generate many options
2. Mental Models → Evaluate with First Principles, Expected Value
3. Brainstorm → Refine top options
4. Mental Models → Final decision with bias check

---

### With Serena MCP (Memory)

**完整记忆系统** - 7个专业模板帮助你跟踪思维发展:

#### 核心模板
1. **Decision Record** (决策记录) - 每次重要决策后使用
2. **Model Effectiveness Tracker** (模型效果跟踪) - 每月总结
3. **Decision Outcome Review** (决策结果回顾) - 决策后3-6个月
4. **Personal Thinking Patterns** (个人思维模式) - 每季度总结
5. **Quick Analysis Log** (快速分析日志) - 每天/每周记录
6. **Learning Progress Tracker** (学习进度跟踪) - 每月更新
7. **Model Combination Library** (模型组合库) - 发现有效组合时记录

#### 快速示例
```python
# Template 1: Decision Record
write_memory("decision_2026-01-02_switch-jobs", {
  "date": "2026-01-02",
  "problem_type": "决策类",
  "problem_statement": "是否接受新公司的 offer？",
  "models_used": ["First Principles", "Expected Value", "Opportunity Cost"],
  "key_insights": ["当前角色缺乏成长空间", "新角色学习机会是当前的2倍"],
  "decision_made": "接受新 offer",
  "confidence_level": "高",
  "review_date": "2026-07-02",
  "tags": ["career", "high-stakes"]
})

# Template 5: Quick Analysis Log (日常使用)
write_memory("quick_log_2026-01-02", {
  "date": "2026-01-02",
  "decisions": [
    {
      "problem": "是否参加这个会议？",
      "model": "Opportunity Cost",
      "insight": "会议价值低于当前工作价值",
      "decision": "拒绝"
    }
  ]
})
```

#### 记忆系统工作流
**决策前**: 读取历史决策和思维模式
**决策后**: 使用 Template 1 记录决策
**定期回顾**:
- 每周: Template 5 (快速日志)
- 每月: Template 2 (模型效果) + Template 6 (学习进度)
- 每季度: Template 4 (思维模式)
- 决策后3-6个月: Template 3 (结果回顾)

**完整模板和使用指南**: [memory-templates.md](../assets/templates/memory-templates.md)

**Benefits**:
- Track decision quality over time
- Identify your most useful models
- Learn from past analyses
- Build personal decision library
- Calibrate confidence levels
- Identify cognitive biases and blind spots

---

### With Magic MCP (Visualization)
**Generate visualizations**:
- Decision trees (multi-option comparison)
- System loop diagrams (feedback cycles)
- Probability distributions (Expected Value)
- Bias detection dashboard

**When to use**: After deep analysis, for communication, for complex systems

---

## Tips for Effective Use

1. **Match tool to task**: Simple problem = 1-2 models. Complex problem = framework.

2. **Start with exploration**: Use Socratic mode when learning. Switch to templates when comfortable.

3. **Bias check is mandatory**: Always review cognitive models before finalizing.

4. **Document your thinking**: Write it down. Forces clarity and enables future learning.

5. **Iterate**: First analysis rarely perfect. Refine as you learn more.

6. **Teach others**: Best way to internalize models.

7. **Build habits**: Apply one model per day to small decisions. Compounds over time.

8. **Embrace uncertainty**: Models illuminate trade-offs, not eliminate uncertainty.

9. **Quality over quantity**: Better to deeply understand 5 models than superficially know 50.

10. **Context matters**: Same problem, different context → different models. Always clarify context first.

---

## Advanced Techniques

### Creating Custom Model Combinations

**For recurring problem types**, create your own combinations:

**Example - Product Launch Decision**:
1. First Principles: What problem does this solve?
2. Expected Value: What's the upside/downside?
3. Opportunity Cost: What else could we do?
4. Second-Order Thinking: What happens after launch?
5. Incentives: What motivates our team/users?

Document this as your "Product Launch Framework" and reuse.

---

### Model Stacking

**Apply models in sequence**, each building on the last:

**Example - Career Decision**:
1. First Principles → Identify core values
2. Systems Thinking → Map career ecosystem
3. Expected Value → Calculate options
4. Confirmation Bias → Check for wishful thinking
5. Reversibility → Assess if decision is reversible

Each model refines the analysis.

---

### Negative Space Analysis

**Use Inversion**: What would make this decision terrible?
- Helps identify risks
- Reveals hidden assumptions
- Complements positive analysis

---

## Common Pitfalls

1. **Model Worship**: Models are tools, not truth. Reality is messy.

2. **Analysis Paralysis**: More analysis ≠ better decision after a point.

3. **Confirmation Seeking**: Using models to justify pre-made decisions.

4. **Jargon Overload**: Using model names without substance.

5. **Ignoring Context**: Same model, different context = different conclusions.

6. **Skipping Synthesis**: Applying models but not integrating insights.

7. **Perfectionism**: Waiting for perfect analysis instead of good enough.

8. **Lone Wolf**: Not seeking feedback or teaching others.

---

## Success Metrics

**How to know you're improving**:

1. **Speed**: Faster to identify relevant models
2. **Accuracy**: Better decisions (track outcomes)
3. **Confidence**: More certain about reasoning
4. **Flexibility**: Can switch models fluidly
5. **Teaching**: Can explain to others clearly
6. **Intuition**: Models become automatic
7. **Creativity**: Generate novel model combinations
8. **Impact**: Others seek your analytical input

---

## Further Resources

**In this skill**:
- [Interactive Guide](interactive-guide.md) - AskUserQuestion flows
- [Quick Reference](quick-reference.md) - Fast model lookup
- [References](../references/) - Detailed model descriptions
- [Templates](../assets/templates/) - Decision frameworks
- [Worksheets](../assets/worksheets/) - Practice exercises

**External**:
- Farnam Street Blog (fs.blog) - Mental models library
- "Thinking in Systems" by Donella Meadows
- "Thinking, Fast and Slow" by Daniel Kahneman
- "Poor Charlie's Almanack" by Charlie Munger

---

**Remember**: The goal is not to memorize all models, but to internalize a few core ones and apply them instinctively. Start small, practice consistently, build gradually.

**The best mental model is the one you actually use.**
