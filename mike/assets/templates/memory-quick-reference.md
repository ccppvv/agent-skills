# Memory Templates Quick Reference

快速查看所有7个记忆模板的使用场景和命令。

---

## 📋 Template 1: Decision Record
**何时使用**: 每次重要决策后
**频率**: 按需
**命令**: `write_memory("decision_YYYY-MM-DD_title", {...})`
**核心字段**: problem, models_used, decision, confidence, review_date, tags

---

## 📊 Template 2: Model Effectiveness Tracker
**何时使用**: 评估模型效果
**频率**: 每月
**命令**: `write_memory("model_effectiveness_YYYY-MM", {...})`
**核心字段**: model_usage_stats, most_valuable_models, learning_goals

---

## 🔄 Template 3: Decision Outcome Review
**何时使用**: 回顾决策结果
**频率**: 决策后3-6个月
**命令**: `write_memory("outcome_review_YYYY-MM-DD_title", {...})`
**核心字段**: actual_outcome, prediction_accuracy, lessons_learned

---

## 🧠 Template 4: Personal Thinking Patterns
**何时使用**: 识别思维模式
**频率**: 每季度
**命令**: `write_memory("thinking_patterns_YYYY-QX", {...})`
**核心字段**: cognitive_biases_detected, thinking_strengths/weaknesses, improvement_goals

---

## 🎯 Template 5: Quick Analysis Log
**何时使用**: 日常小决策
**频率**: 每天/每周
**命令**: `write_memory("quick_log_YYYY-MM-DD", {...})`
**核心字段**: decisions (array), daily_reflection

---

## 📚 Template 6: Learning Progress Tracker
**何时使用**: 跟踪学习进度
**频率**: 每月
**命令**: `write_memory("learning_progress_YYYY-MM", {...})`
**核心字段**: current_level, models_learned, next_month_goals

---

## 🔍 Template 7: Model Combination Library
**何时使用**: 发现有效组合
**频率**: 按需
**命令**: `write_memory("model_combo_problem-type", {...})`
**核心字段**: combination_name, models_in_sequence, when_to_use

---

## 🗓️ 推荐使用频率

| 时间周期 | 使用模板 |
|---------|---------|
| **每天** | Template 5 (Quick Log) |
| **每周** | Template 5 (Quick Log 总结) |
| **每月** | Template 2 (Model Effectiveness) + Template 6 (Learning Progress) |
| **每季度** | Template 4 (Thinking Patterns) |
| **按需** | Template 1 (Decision Record) + Template 7 (Model Combo) |
| **决策后3-6个月** | Template 3 (Outcome Review) |

---

## 🚀 快速开始

### 新手推荐流程
1. **第1周**: 只用 Template 5 (Quick Log) 记录日常小决策
2. **第2-4周**: 加入 Template 1 (Decision Record) 记录重要决策
3. **第1个月末**: 使用 Template 6 (Learning Progress) 总结学习进度
4. **第2个月**: 加入 Template 2 (Model Effectiveness) 评估模型效果
5. **第3个月**: 开始使用 Template 3 (Outcome Review) 回顾早期决策
6. **第3个月末**: 使用 Template 4 (Thinking Patterns) 识别思维模式
7. **发现有效组合时**: 随时使用 Template 7 (Model Combo) 记录

### 最小化使用
如果时间有限，至少使用:
- **Template 1** (Decision Record) - 重要决策必记
- **Template 5** (Quick Log) - 每周快速记录

### 完整使用
全面跟踪思维发展:
- 所有7个模板按推荐频率使用
- 建立完整的个人决策知识库

---

## 💡 使用技巧

### 1. 标签系统
建议使用的标签:
- **领域**: career, investment, product, personal, business, technical
- **重要性**: high-stakes, medium-stakes, low-stakes
- **类型**: strategic, tactical, operational
- **结果**: success, partial-success, failure, pending

### 2. 命名规范
- Decision Record: `decision_YYYY-MM-DD_brief-title`
- Outcome Review: `outcome_review_YYYY-MM-DD_brief-title`
- Quick Log: `quick_log_YYYY-MM-DD`
- Model Effectiveness: `model_effectiveness_YYYY-MM`
- Thinking Patterns: `thinking_patterns_YYYY-QX`
- Learning Progress: `learning_progress_YYYY-MM`
- Model Combo: `model_combo_problem-type`

### 3. 搜索技巧
```python
# 查找所有职业相关决策
list_memories(filter="decision_*", tags=["career"])

# 查找高风险决策
list_memories(filter="decision_*", tags=["high-stakes"])

# 查找需要回顾的决策
list_memories(filter="decision_*", review_date="<today")

# 查看学习进度
read_memory("learning_progress_*")
```

---

## 📖 完整文档

详细模板内容和示例: [memory-templates.md](memory-templates.md)

---

**记住**: 从简单开始，逐步扩展。记忆系统的价值在于持续使用，而不是一次性完美。
