# Mental Model Mentor - Interactive Dialogue Guide

This guide shows how to use `AskUserQuestion` Tool to create smooth, guided analysis experiences. For workflow details, see [detailed-guide.md](detailed-guide.md).

---

## Core Principles

1. **Click, Don't Type**: Use `AskUserQuestion` to provide options - users click instead of typing long text
2. **Progressive Disclosure**: Start simple, add complexity only when needed
3. **Smart Defaults**: Recommend options based on problem type
4. **4-Option Limit**: `AskUserQuestion` supports maximum **4 options** per question
5. **Multiselect When Appropriate**: Use for non-exclusive choices (e.g., learning actions)

---

## Standard Dialogue Flow

### Flow 0: Ultra-Fast (1 Question) ⚡ NEW!

**Best for**: Users who want immediate analysis, trust AI selection

```
Question: "How do you want to proceed?"
    ├─ Quick Analysis (推荐) → Auto-select models → Analyze
    ├─ Custom Analysis → Go to Flow 1
    └─ Learning Mode → Go to Flow 3
```

**Time**: 2 min setup + analysis time

**Key Innovation**: Single decision point, then AI handles everything else.

---

### Flow 1: Simplified Interactive (2-3 Questions)

**Best for**: First-time users, want some control

```
Question 1: "How do you want to start?"
    ├─ Quick Analysis → Auto-select → Execute
    ├─ Custom → Question 2
    └─ Learning Mode → Go to Flow 3

Question 2 (if Custom): "Which model combination?"
    ├─ Recommended (based on problem) → Execute
    ├─ System Analysis → Execute
    ├─ Bias Detection → Execute
    └─ Custom Selection → Execute

Execute Analysis → Present Insights
```

**Time**: 3-5 min setup + analysis time

---

### Flow 1-Legacy: Original Flow (3 Questions)

**Best for**: Users who want full control over each step

```
Question 1: Problem Type
    ↓
Question 2: Model Selection (with recommendation)
    ↓
Question 3: Analysis Depth
    ↓
Execute Analysis
    ↓
Present Insights
```

**Time**: 5-10 min setup + analysis time

---

### Flow 2: Expert Mode (1 Question)

**Best for**: Experienced users who know what they want

```
Question: Quick or Custom?
    ↓
If Quick → Auto-select models → Execute
If Custom → Browse references → Self-directed
```

**Time**: 2-3 min setup + analysis time

---

### Flow 3: Learning Mode (5+ Questions)

**Best for**: Users wanting to learn mental models through practice

```
Question 1: Problem Type
    ↓
Question 2: "Which models do YOU think apply?" (Socratic)
    ↓
Feedback on selection
    ↓
Question 3: "What would First Principles reveal?"
    ↓
Guide through application
    ↓
Question 4: "What biases might affect you?"
    ↓
Reflection and synthesis
```

**Time**: 30-60 min (educational focus)

---

## AskUserQuestion Templates

### Template 0: Ultra-Fast Start (NEW! ⚡)

```yaml
AskUserQuestion:
  question: "我来帮你用思维模型分析这个问题。你想如何开始？"
  header: "开始方式"
  options:
    - label: "快速分析 (推荐)"
      description: "我来选择模型，5-10分钟给你洞察"
    - label: "自定义分析"
      description: "你选择模型和深度，更多控制"
    - label: "学习模式"
      description: "通过提问引导你学习思维模型"
  multiSelect: false
```

**When to use**: Start of EVERY analysis (replaces old 3-step flow)
**Follow-up**:
- Quick → Auto-analyze with recommended models
- Custom → Go to Template 0.5
- Learning → Go to Socratic flow

**Key benefit**: Single question gets user started immediately

---

### Template 0.5: Custom Model Selection (Conditional)

```yaml
AskUserQuestion:
  question: "基于你的【{problem_type}】问题，推荐使用【{recommended}】。你想用哪种模型组合？"
  header: "模型选择"
  options:
    - label: "{recommended} (推荐)"
      description: "{models} - 最适合你的问题类型"
    - label: "系统分析"
      description: "系统思维 + 反馈循环 + 杠杆点"
    - label: "偏见检测"
      description: "确认偏误 + 锚定效应 + 沉没成本"
    - label: "概率决策"
      description: "贝叶斯思维 + 期望值 + 基础概率"
  multiSelect: false
```

**When to use**: Only if user chose "Custom" in Template 0
**Customization**: Replace {problem_type} and {recommended} based on user's problem
**Follow-up**: Execute analysis with selected models

---

### Template 1: Problem Type Identification (v4.0 — 10 structures)

```yaml
AskUserQuestion:
  question: "你的问题属于哪种类型？"
  header: "问题结构"
  options:
    - label: "做决策"
      description: "该不该/要不要/选哪个 — 需要做出选择"
    - label: "诊断原因"
      description: "为什么出问题/根因在哪 — 需要深入分析"
    - label: "评估价值"
      description: "值不值/风险多大/回报如何 — 需要量化判断"
    - label: "其他 (优化/谈判/创新/学习/领导/设计/预测)"
      description: "让 AI 自动识别或后续追问"
  multiSelect: false
```

**When to use**: Start of every analysis (when user wants to self-classify)
**Follow-up**: AI confirms or adjusts via `model_matcher.py` three-layer routing

---

### Template 2: Model Combination Selection (v4.0)

```yaml
AskUserQuestion:
  question: "基于你的【{problem_type}】问题，三层路由推荐以下模型。你想用哪种方式？"
  header: "模型选择"
  options:
    - label: "AI 自动选择 (推荐)"
      description: "由 model_matcher.py 三层路由自动匹配，覆盖多样类别"
    - label: "手动指定类别"
      description: "从 strategic/cognitive/systems/probability/economics 等 37 个类别中自选"
    - label: "框架模式"
      description: "使用五维框架 (战略+系统+认知+概率+经济) 全维度分析"
    - label: "学习模式"
      description: "通过苏格拉底式提问引导你自主选择模型"
  multiSelect: false
```

**When to use**: After problem type identified
**Customization**: Replace {problem_type} based on 10-structure routing result

---

### Template 3: Analysis Depth (v4.0)

```yaml
AskUserQuestion:
  question: "你希望多深度的分析？"
  header: "分析深度"
  options:
    - label: "快速分析 (推荐)"
      description: "2-3个模型，5-15分钟，聚焦关键洞察"
    - label: "标准分析"
      description: "3-5个模型，15-30分钟，多类别交叉校验"
    - label: "深度分析"
      description: "5-8个模型，1-2小时，五维框架全覆盖 + 反证 + 偏差检查"
  multiSelect: false
```

**When to use**: After model selection
**Follow-up**: Aligns with `COMPLEXITY_PRESETS` in `model_matcher.py`

---

### Template 4: Decision Action

```yaml
AskUserQuestion:
  question: "基于分析，你想采取什么行动？"
  header: "行动选择"
  options:
    - label: "立即执行"
      description: "模型一致指向明确方向，信心较高"
    - label: "收集更多信息"
      description: "需要更多数据来提高信心"
    - label: "小规模试验"
      description: "先小范围测试，降低风险"
    - label: "延后决策"
      description: "不是紧急决策，可以再思考"
  multiSelect: false
```

**When to use**: After presenting analysis insights
**Follow-up**:
- Execute → Implementation planning
- More info → Identify information gaps
- Test → Design experiment
- Delay → Set review date

---

### Template 5: Learning Reflection

```yaml
AskUserQuestion:
  question: "分析完成后，你想要做什么？"
  header: "后续行动"
  options:
    - label: "保存分析记录"
      description: "将分析保存到思维日记，供未来参考"
    - label: "应用下一个问题"
      description: "用这些模型分析另一个问题"
    - label: "创建个人模板"
      description: "将这个分析过程保存为可复用模板"
    - label: "学习更多模型"
      description: "深入了解使用的思维模型"
  multiSelect: true  # Allow multiple selections
```

**When to use**: End of analysis
**Follow-up**:
- Save → Use Serena `write_memory()`
- Apply → Start new analysis
- Template → Create custom template
- Learn → Link to relevant references/

---

## Complete Dialogue Examples

### Example 0: Ultra-Fast Career Decision (NEW! ⚡)

```
用户: "我不确定是否应该换工作"

助手: 我来帮你用思维模型分析这个决策。

[AskUserQuestion - Template 0: Ultra-Fast Start]
question: "你想如何开始？"
options:
  - 快速分析 (推荐)
  - 自定义分析
  - 学习模式

→ 用户选择: "快速分析"

助手: 好的！我会自动选择最合适的模型进行分析。

[AI 自动分析 - 无需更多问题]

**分析开始** (使用战略组合: First Principles + Expected Value + Opportunity Cost)

**First Principles**:
- 核心问题: 为什么考虑换工作？
  ✓ 当前: 缺乏成长空间
  ✓ 新机会: 2x 学习机会 + 30% 薪资提升

**Expected Value**:
- 留下: 稳定性 (90%) × 当前价值 = 中等
- 换工作: 成功 (70%) × 高价值 + 失败 (30%) × 低价值 = 较高

**Opportunity Cost**:
- 留下的代价: 错过学习机会，职业停滞
- 换工作的代价: 短期适应压力，人脉重建

**偏见检查**:
⚠️ 确认偏误: 是否只看到新工作的好处？
⚠️ 沉没成本: 不要因为"已经待了3年"而留下

**综合洞察**:
✅ 如果成长是核心价值 → 换工作合理
⚠️ 建议: 与新公司深度交流，验证学习机会真实性

[AskUserQuestion - Template 4: Decision Action]
→ 用户选择: "小规模试验"

助手: 建议试验方式:
1. 与新团队成员深度交流
2. 要求试用期或项目合作
3. 与现公司讨论成长路径

完成！
```

**Total time**: ~8 minutes (vs 20 minutes in old flow)
**Key difference**: Only 2 questions total, AI handles model selection

---

### Example 1: Career Decision (Simplified Interactive)

```
用户: "我不确定是否应该换工作"

助手: 我来帮你用思维模型系统分析这个决策。

[AskUserQuestion - Template 0]
→ 用户选择: "自定义分析"

助手: 好的。基于你的决策问题，我推荐使用战略组合模型。

[AskUserQuestion - Template 0.5]
question: "基于你的【决策】问题，推荐使用【战略组合】。你想用哪种模型组合？"
→ 用户选择: "战略组合 (推荐)"

助手: 很好。我们将使用 First Principles、二阶思维和机会成本来分析。

[执行分析 - 与 Example 0 相同]
...

[AskUserQuestion - Template 4]
→ 用户选择: "小规模试验"

完成！
```

**Total time**: ~15 minutes
**Key difference**: User has control over model selection

---

### Example 1-Legacy: Career Decision (Original Flow)

```
用户: "我不确定是否应该换工作"

助手: 我来帮你用思维模型系统分析这个决策。

[AskUserQuestion - Template 1: Problem Type]
→ 用户选择: "做决策"

助手: 好的，这是一个决策问题。基于这个类型，我推荐使用战略组合模型。

[AskUserQuestion - Template 2: Model Selection]
→ 用户选择: "战略组合 (推荐)"

助手: 很好。我们将使用 First Principles、二阶思维和机会成本来分析。

[AskUserQuestion - Template 3: Analysis Depth]
→ 用户选择: "快速分析"

助手: 明白，我会在 15-30 分钟内完成核心分析。

[执行分析]

**First Principles 分析**:
- 为什么考虑换工作？
  - 当前工作缺乏成长空间
  - 新工作提供 2x 学习机会
  - 薪资提升 30%

**二阶思维 (后果推演)**:
- 换工作 → 学习新技能 → 职业发展加速
- 换工作 → 失去现有人脉 → 需要重建关系
- 换工作 → 适应期 3-6 个月 → 短期压力

**机会成本**:
- 留下的代价: 错过学习机会，职业停滞
- 换工作的代价: 稳定性，现有人脉

**偏见检查**:
- 确认偏误: 是否只看到新工作的好处？
- 沉没成本: 不要因为"已经待了3年"而留下

**综合洞察**:
✅ 模型一致指向: 如果成长是核心价值，换工作是合理选择
⚠️ 注意事项: 确认新工作的学习机会是真实的，不是招聘话术

[AskUserQuestion - Template 4: Decision Action]
→ 用户选择: "小规模试验"

助手: 好主意！建议的试验方式:
1. 与新公司团队成员深度交流 (验证学习机会)
2. 要求试用期或项目合作 (降低风险)
3. 与现公司讨论成长路径 (探索替代方案)

[AskUserQuestion - Template 5: Learning Reflection]
→ 用户选择: "保存分析记录" + "创建个人模板"

助手: 已保存分析到记忆系统。我还为你创建了"职业决策模板"，下次遇到类似问题可以直接使用。
```

**Total time**: ~20 minutes

---

### Example 2: System Problem (Deep Analysis)

```
用户: "我们的产品用户留存率很低，不知道为什么"

助手: 这是一个复杂的系统问题，让我帮你深入分析。

[AskUserQuestion - Template 1]
→ 用户选择: "分析原因"

[AskUserQuestion - Template 2]
→ 用户选择: "系统分析"

[AskUserQuestion - Template 3]
→ 用户选择: "深度分析"

助手: 我会使用系统思维、反馈循环和杠杆点进行全面分析。

[执行深度分析 - 使用 Five-Dimensional Framework]

**1. Strategic View (战略视角)**:
- First Principles: 用户为什么来？为什么走？
  - 来: 解决特定问题
  - 走: 问题未解决 OR 解决后无持续价值

**2. Systems View (系统视角)**:
- 系统结构:
  ```
  新用户 → 首次体验 → 价值感知 → 留存决策
     ↑                                    ↓
     └──────── 口碑传播 ←─────────────────┘
  ```
- 反馈循环:
  - 正循环: 好体验 → 留存 → 口碑 → 更多用户
  - 负循环: 差体验 → 流失 → 差评 → 用户减少

**3. Cognitive View (认知视角)**:
- 确认偏误: 团队是否只关注留存用户的反馈？
- 锚定效应: 是否被竞品的留存率锚定？
- 框架效应: "留存率低"vs"流失率高" - 不同框架不同洞察

**4. Probabilistic View (概率视角)**:
- 基础概率: 行业平均留存率是多少？
- 贝叶斯更新: 哪些用户群体留存率更高？
- 期望值: 提升留存 10% 的价值是多少？

**5. Economic View (经济视角)**:
- 激励: 用户留下的动机是什么？
- 机会成本: 用户用你的产品 vs 竞品的权衡
- 边际效用: 用户使用越多，价值是递增还是递减？

**杠杆点识别** (从低到高):
1. 🔧 参数调整: 优化通知频率
2. 🔧 缓冲区: 增加免费试用期
3. ⚙️ 反馈延迟: 加快价值实现速度
4. ⚙️ 信息流: 改进用户引导
5. 🎯 规则: 改变激励机制
6. 🎯 系统目标: 重新定义"成功"

**综合洞察**:
🔍 根本原因: 用户在首次体验中未感知到核心价值
🎯 高杠杆点: 优化 onboarding 流程，加快"啊哈时刻"
⚠️ 系统风险: 如果只优化留存指标，可能牺牲新用户获取

**行动建议**:
1. 立即: 分析流失用户的行为路径 (数据)
2. 短期: A/B 测试不同 onboarding 流程
3. 中期: 建立用户价值感知的反馈循环
4. 长期: 重新设计产品核心价值主张

[AskUserQuestion - Template 4]
→ 用户选择: "收集更多信息"

助手: 建议收集的信息:
- 流失用户的最后操作是什么？
- 留存用户 vs 流失用户的行为差异？
- 用户访谈: 为什么离开？
- 竞品分析: 他们如何解决这个问题？

[AskUserQuestion - Template 5]
→ 用户选择: "保存分析记录" + "学习更多模型"

助手: 分析已保存。推荐深入学习:
- [systems.md](../references/systems.md) - 系统思维和杠杆点
- [frameworks.md](../references/frameworks.md) - 五维分析框架
```

**Total time**: ~90 minutes

---

### Example 3: Learning Mode (Socratic Dialogue)

```
用户: "我想学习如何用思维模型分析问题"

助手: 很好！我会通过引导式提问帮你学习。让我们用一个真实问题练习。

[AskUserQuestion]
question: "你最近遇到的一个需要决策的问题是什么？"
options:
  - 职业发展
  - 投资理财
  - 学习规划
  - 其他 (自定义)

→ 用户选择: "学习规划"
→ 用户补充: "不知道应该学 AI 还是 Web3"

助手: 好的，这是一个选择问题。在我告诉你答案之前，让我们一起思考。

[Socratic Question 1]
question: "如果你用 First Principles (第一性原理) 思考，你学习的根本目的是什么？"
options:
  - 找工作/升职
  - 个人兴趣
  - 跟上趋势
  - 解决具体问题

→ 用户选择: "找工作/升职"

助手: 很好！你识别出了根本目的。现在让我们用 Expected Value (期望值) 思考。

[Socratic Question 2]
question: "如果学习 AI，你认为成功概率和收益分别是多少？"
(引导用户估算)

→ 用户回答: "成功概率 70%，收益是找到 AI 工作"

助手: 不错。现在思考 Web3 的期望值。然后我们比较。

[继续引导...]

助手: 你刚才应用了两个核心模型:
✅ First Principles - 找到根本目的
✅ Expected Value - 量化比较

现在让我们检查认知偏见。

[Socratic Question 3]
question: "你是否因为最近 AI 很火热，就倾向于选择 AI？这可能是什么偏见？"
options:
  - 确认偏误 (只看支持的证据)
  - 可得性偏误 (最近听到的影响判断)
  - 从众效应 (大家都学所以我也学)
  - 没有偏见

→ 用户选择: "可得性偏误"

助手: 完全正确！你刚才识别出了可得性偏误。这就是思维模型的力量 - 帮你看到思维盲点。

[总结学习]
你刚才学会了:
1. First Principles - 找根本目的
2. Expected Value - 量化决策
3. Availability Bias - 识别偏见

下次遇到类似问题，你可以自己应用这些模型。

[AskUserQuestion - Template 5]
→ 用户选择: "应用下一个问题"

助手: 太好了！找一个新问题，这次你来主导分析，我只在需要时提供帮助。
```

**Total time**: ~45 minutes (educational focus)

---

## Advanced Techniques

### Technique 1: Adaptive Questioning

**Adjust questions based on user responses**:

```python
if user_selected == "做决策" and problem_complexity == "high":
    # Recommend deep analysis
    options = ["深度分析 (推荐)", "快速分析", "对话式探索"]
elif user_selected == "做决策" and problem_complexity == "low":
    # Recommend quick analysis
    options = ["快速分析 (推荐)", "深度分析", "对话式探索"]
```

---

### Technique 2: Progressive Disclosure

**Start simple, add complexity only when needed**:

```
Level 1: "Quick or Custom?"
    ↓ If Custom
Level 2: "Which category of models?"
    ↓ If need more
Level 3: "Which specific models?"
```

Don't overwhelm with all options upfront.

---

### Technique 3: Smart Defaults

**Pre-select recommended options**:

```yaml
options:
  - label: "战略组合 (推荐)" ✅  # Visually indicate recommendation
    description: "..."
```

Users can still choose others, but have a clear starting point.

---

### Technique 4: Multiselect for Non-Exclusive Choices

**Use when multiple selections make sense**:

```yaml
question: "分析完成后，你想要做什么？"
multiSelect: true  # Allow multiple
options:
  - 保存分析记录
  - 应用下一个问题
  - 创建个人模板
  - 学习更多模型
```

---

## Common Pitfalls

### ❌ Pitfall 1: Too Many Questions
**Problem**: 5+ questions before analysis starts
**Solution**: Combine into 3 questions max, use smart defaults

### ❌ Pitfall 2: Vague Options
**Problem**: Options like "Option A", "Option B"
**Solution**: Clear labels + descriptive explanations

### ❌ Pitfall 3: False Choices
**Problem**: All options lead to same outcome
**Solution**: Each option should meaningfully change the analysis

### ❌ Pitfall 4: Overwhelming Descriptions
**Problem**: 3-sentence descriptions for each option
**Solution**: 1 sentence max, 10-15 words

### ❌ Pitfall 5: No Recommendations
**Problem**: All options presented equally
**Solution**: Mark recommended option, explain why

---

## Integration with Other Modes

### With Quick Reference
**When user seems lost**:
```
"不确定选哪个？查看 [quick-reference.md](quick-reference.md) 的 30 秒决策树"
```

### With Detailed Guide
**When user wants to learn more**:
```
"想了解这些模型的详细用法？查看 [detailed-guide.md](detailed-guide.md)"
```

### With Templates
**When user wants structure**:
```
"想要更结构化的分析？使用 [decision-matrix.md](../assets/templates/decision-matrix.md)"
```

---

## Success Metrics

**Good interactive experience**:
- ✅ User completes analysis without confusion
- ✅ Questions feel natural, not interrogative
- ✅ User learns something about thinking
- ✅ Analysis is actionable
- ✅ User wants to use again

**Poor interactive experience**:
- ❌ User abandons mid-way
- ❌ Too many questions before value
- ❌ Options don't match user's mental model
- ❌ Analysis feels mechanical
- ❌ User doesn't understand why questions matter

---

## Quick Reference: When to Use Which Template

| Situation | Template | Purpose |
|-----------|----------|---------|
| Analysis start | Template 1 (Problem Type) | Classify problem |
| After classification | Template 2 (Model Selection) | Choose frameworks |
| Before analysis | Template 3 (Analysis Depth) | Set scope |
| After insights | Template 4 (Decision Action) | Convert to action |
| Analysis end | Template 5 (Learning Reflection) | Capture learning |
| User confused | Quick Reference link | Fast navigation |
| User wants depth | Detailed Guide link | Comprehensive info |
| User wants structure | Template link | Guided framework |

---

**Remember**: The goal of interactive dialogue is to **lower the barrier** to systematic thinking. Make it feel like a conversation, not a form to fill out.

**The best interaction is one the user doesn't notice - they just think clearly.**
