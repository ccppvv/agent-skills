# Mental Model Memory Templates

记忆系统模板集合，用于跟踪决策历史、思维模式和学习进展。

---

## 📋 Template 1: Decision Record (决策记录)

**用途**: 记录每次使用思维模型做出的决策，便于后续回顾和学习

**使用时机**: 每次完成重要决策分析后

**Serena MCP 命令**:
```python
write_memory("decision_YYYY-MM-DD_brief-title", {
  "date": "YYYY-MM-DD",
  "problem_type": "决策类/分析类/改进类/预测类/选择类",
  "problem_statement": "清晰描述要解决的问题",
  "context": {
    "urgency": "立即/可深思",
    "stakes": "高/中/低",
    "reversibility": "可逆/不可逆/部分可逆"
  },
  "models_used": [
    "First Principles",
    "Expected Value",
    "Opportunity Cost"
  ],
  "analysis_summary": {
    "key_insights": [
      "洞察1: 具体发现",
      "洞察2: 具体发现"
    ],
    "model_convergence": "所有模型指向同一方向/模型有分歧/模型相互矛盾",
    "tensions_identified": "如果模型有分歧，描述张力点"
  },
  "decision_made": "具体决策内容",
  "confidence_level": "高/中/低",
  "reasoning": "为什么做出这个决策",
  "alternatives_considered": [
    "备选方案1",
    "备选方案2"
  ],
  "implementation_plan": "如何执行这个决策",
  "success_criteria": "如何判断决策是否成功",
  "review_date": "YYYY-MM-DD (建议3-6个月后回顾)",
  "tags": ["career", "investment", "product", "personal"]
})
```

**示例**:
```python
write_memory("decision_2026-01-02_switch-jobs", {
  "date": "2026-01-02",
  "problem_type": "决策类",
  "problem_statement": "是否接受新公司的 offer？",
  "context": {
    "urgency": "可深思",
    "stakes": "高",
    "reversibility": "部分可逆"
  },
  "models_used": [
    "First Principles",
    "Expected Value",
    "Opportunity Cost",
    "Second-Order Thinking"
  ],
  "analysis_summary": {
    "key_insights": [
      "当前角色缺乏成长空间（First Principles）",
      "新角色学习机会是当前的2倍（Expected Value）",
      "留在当前公司的机会成本很高（Opportunity Cost）",
      "跳槽后可能面临适应期挑战（Second-Order Thinking）"
    ],
    "model_convergence": "所有模型指向同一方向",
    "tensions_identified": "无重大分歧"
  },
  "decision_made": "接受新 offer",
  "confidence_level": "高",
  "reasoning": "成长机会远超过适应期风险",
  "alternatives_considered": [
    "留在当前公司争取晋升",
    "继续寻找其他机会"
  ],
  "implementation_plan": "2周内提交辞职，1个月过渡期",
  "success_criteria": "6个月内掌握新技能栈，1年内晋升",
  "review_date": "2026-07-02",
  "tags": ["career", "high-stakes"]
})
```

---

## 📊 Template 2: Model Effectiveness Tracker (模型效果跟踪)

**用途**: 跟踪哪些思维模型对你最有效，识别个人思维偏好

**使用时机**: 每月或每季度总结一次

**Serena MCP 命令**:
```python
write_memory("model_effectiveness_YYYY-MM", {
  "period": "YYYY-MM",
  "total_decisions": 10,
  "model_usage_stats": {
    "First Principles": {
      "times_used": 8,
      "usefulness_rating": 9,
      "best_for": "战略决策、产品设计",
      "notes": "几乎每次都有帮助，是我的核心模型"
    },
    "Expected Value": {
      "times_used": 6,
      "usefulness_rating": 8,
      "best_for": "投资决策、风险评估",
      "notes": "量化思维很有帮助，但需要准确估计概率"
    },
    "Systems Thinking": {
      "times_used": 5,
      "usefulness_rating": 7,
      "best_for": "复杂问题分析",
      "notes": "需要更多练习才能熟练应用"
    }
  },
  "most_valuable_models": [
    "First Principles",
    "Expected Value",
    "Opportunity Cost"
  ],
  "underutilized_models": [
    "Inversion",
    "Base Rates"
  ],
  "learning_goals": "下个月重点练习 Inversion 和 Base Rates",
  "pattern_observations": "我倾向于使用战略模型，需要加强概率思维"
})
```

---

## 🔄 Template 3: Decision Outcome Review (决策结果回顾)

**用途**: 回顾过去的决策，评估思维模型的准确性

**使用时机**: 决策执行3-6个月后

**Serena MCP 命令**:
```python
write_memory("outcome_review_YYYY-MM-DD_brief-title", {
  "original_decision_id": "decision_2026-01-02_switch-jobs",
  "review_date": "YYYY-MM-DD",
  "time_elapsed": "6个月",
  "actual_outcome": "成功/部分成功/失败",
  "outcome_description": "详细描述实际发生了什么",
  "prediction_accuracy": {
    "what_was_correct": [
      "预测1: 实际情况",
      "预测2: 实际情况"
    ],
    "what_was_wrong": [
      "预测1: 实际情况",
      "预测2: 实际情况"
    ]
  },
  "model_performance": {
    "First Principles": "准确/部分准确/不准确 - 原因",
    "Expected Value": "准确/部分准确/不准确 - 原因"
  },
  "blind_spots_identified": [
    "盲点1: 没有考虑到的因素",
    "盲点2: 没有考虑到的因素"
  ],
  "lessons_learned": [
    "教训1: 具体学到了什么",
    "教训2: 具体学到了什么"
  ],
  "would_decide_differently": "是/否",
  "if_yes_what_would_change": "如果重新决策会怎么做",
  "confidence_calibration": "当时信心高，结果成功 → 校准良好",
  "next_similar_decision": "下次遇到类似问题时的改进点"
})
```

**示例**:
```python
write_memory("outcome_review_2026-07-02_switch-jobs", {
  "original_decision_id": "decision_2026-01-02_switch-jobs",
  "review_date": "2026-07-02",
  "time_elapsed": "6个月",
  "actual_outcome": "成功",
  "outcome_description": "成功适应新环境，掌握了新技能栈，团队合作良好",
  "prediction_accuracy": {
    "what_was_correct": [
      "成长机会确实比之前多2倍",
      "学习曲线陡峭但可管理"
    ],
    "what_was_wrong": [
      "低估了文化适应的时间（预计1个月，实际3个月）"
    ]
  },
  "model_performance": {
    "First Principles": "准确 - 成长空间分析正确",
    "Expected Value": "准确 - 收益评估准确",
    "Opportunity Cost": "准确 - 留在原公司确实会错失机会",
    "Second-Order Thinking": "部分准确 - 预测了适应期，但低估了文化冲击"
  },
  "blind_spots_identified": [
    "没有充分考虑公司文化差异",
    "低估了建立新人际关系网络的时间"
  ],
  "lessons_learned": [
    "文化适应比技能学习更耗时，下次要更重视",
    "Second-Order Thinking 需要更深入，不只是一阶效应"
  ],
  "would_decide_differently": "否",
  "if_yes_what_would_change": "N/A",
  "confidence_calibration": "当时信心高，结果成功 → 校准良好",
  "next_similar_decision": "增加文化适应评估，延长预期适应期"
})
```

---

## 🧠 Template 4: Personal Thinking Patterns (个人思维模式)

**用途**: 识别个人思维偏好、盲点和改进方向

**使用时机**: 每季度总结一次

**Serena MCP 命令**:
```python
write_memory("thinking_patterns_YYYY-QX", {
  "period": "YYYY年第X季度",
  "total_decisions_analyzed": 15,
  "cognitive_biases_detected": {
    "Confirmation Bias": {
      "frequency": "高/中/低",
      "examples": ["具体案例1", "具体案例2"],
      "mitigation_strategy": "主动寻找反对证据"
    },
    "Anchoring": {
      "frequency": "中",
      "examples": ["被第一个数字锚定"],
      "mitigation_strategy": "先独立思考再看数据"
    }
  },
  "thinking_strengths": [
    "擅长系统性思考",
    "善于识别反馈循环",
    "量化分析能力强"
  ],
  "thinking_weaknesses": [
    "容易陷入分析瘫痪",
    "对不确定性容忍度低",
    "忽视情感因素"
  ],
  "recurring_patterns": {
    "positive": [
      "总是从第一性原理开始",
      "善于识别机会成本"
    ],
    "negative": [
      "过度依赖数据，忽视直觉",
      "分析时间过长"
    ]
  },
  "improvement_goals": [
    "提高决策速度，设置分析时间上限",
    "平衡理性分析和直觉判断",
    "更多使用 Inversion 模型"
  ],
  "model_mastery_progress": {
    "mastered": ["First Principles", "Expected Value"],
    "proficient": ["Systems Thinking", "Opportunity Cost"],
    "learning": ["Inversion", "Base Rates"],
    "need_practice": ["Black Swan", "Marginal Thinking"]
  }
})
```

---

## 🎯 Template 5: Quick Analysis Log (快速分析日志)

**用途**: 记录日常小决策，积累思维模型应用经验

**使用时机**: 每天或每周记录小决策

**Serena MCP 命令**:
```python
write_memory("quick_log_YYYY-MM-DD", {
  "date": "YYYY-MM-DD",
  "decisions": [
    {
      "problem": "是否参加这个会议？",
      "model": "Opportunity Cost",
      "insight": "会议价值低于当前工作价值",
      "decision": "拒绝",
      "outcome": "节省2小时，完成重要任务"
    },
    {
      "problem": "选择哪个技术方案？",
      "model": "First Principles + Reversibility",
      "insight": "方案A更符合核心需求且可逆",
      "decision": "选择方案A",
      "outcome": "待观察"
    }
  ],
  "daily_reflection": "今天应用了3次思维模型，感觉越来越自然",
  "tomorrow_focus": "练习使用 Inversion 模型"
})
```

---

## 📚 Template 6: Learning Progress Tracker (学习进度跟踪)

**用途**: 跟踪思维模型学习进度和能力发展

**使用时机**: 每月更新一次

**Serena MCP 命令**:
```python
write_memory("learning_progress_YYYY-MM", {
  "month": "YYYY-MM",
  "current_level": "Level 1: Foundation / Level 2: Expansion / Level 3: Integration / Level 4: Mastery",
  "models_learned_this_month": [
    {
      "model": "Inversion",
      "status": "学习中/已掌握",
      "practice_count": 5,
      "confidence": "低/中/高",
      "notes": "需要更多练习"
    }
  ],
  "total_models_mastered": 8,
  "practice_activities": {
    "worksheets_completed": 3,
    "real_decisions_analyzed": 10,
    "teaching_sessions": 1
  },
  "success_criteria_progress": {
    "can_explain_in_own_words": "8/15 models",
    "recognize_when_to_apply": "6/15 models",
    "successfully_applied": "5/15 models"
  },
  "next_month_goals": [
    "掌握 Base Rates 和 Black Swan",
    "完成5个 decision-matrix 练习",
    "教授他人 First Principles"
  ],
  "challenges_faced": [
    "分析瘫痪问题仍然存在",
    "概率模型应用不够熟练"
  ],
  "breakthroughs": [
    "First Principles 已经成为直觉",
    "能够流畅组合2-3个模型"
  ]
})
```

---

## 🔍 Template 7: Model Combination Library (模型组合库)

**用途**: 记录有效的模型组合，建立个人框架库

**使用时机**: 发现有效组合时立即记录

**Serena MCP 命令**:
```python
write_memory("model_combo_problem-type", {
  "combination_name": "产品决策框架",
  "problem_type": "产品功能优先级决策",
  "models_in_sequence": [
    {
      "step": 1,
      "model": "First Principles",
      "purpose": "识别核心用户需求"
    },
    {
      "step": 2,
      "model": "Expected Value",
      "purpose": "评估每个功能的价值"
    },
    {
      "step": 3,
      "model": "Opportunity Cost",
      "purpose": "考虑资源分配"
    },
    {
      "step": 4,
      "model": "Second-Order Thinking",
      "purpose": "预测功能上线后的连锁反应"
    },
    {
      "step": 5,
      "model": "Confirmation Bias",
      "purpose": "检查是否有偏见"
    }
  ],
  "when_to_use": "产品路线图规划、功能优先级排序",
  "success_rate": "8/10 次有效",
  "typical_duration": "1-2小时",
  "notes": "这个组合在产品决策中非常有效，已经成为标准流程",
  "examples": [
    "decision_2026-01-15_feature-prioritization",
    "decision_2026-02-20_roadmap-planning"
  ]
})
```

---

## 💡 使用建议

### 1. 记忆系统工作流

**决策前**:
1. 读取相关历史决策: `read_memory("decision_*")`
2. 查看个人思维模式: `read_memory("thinking_patterns_*")`
3. 参考有效模型组合: `read_memory("model_combo_*")`

**决策中**:
1. 应用思维模型进行分析
2. 记录分析过程和洞察

**决策后**:
1. 使用 Template 1 记录决策
2. 设置回顾提醒

**定期回顾**:
1. 每周: Template 5 (快速日志)
2. 每月: Template 2 (模型效果) + Template 6 (学习进度)
3. 每季度: Template 4 (思维模式)
4. 决策后3-6个月: Template 3 (结果回顾)

### 2. 记忆标签系统

**建议标签分类**:
- **领域**: career, investment, product, personal, business, technical
- **重要性**: high-stakes, medium-stakes, low-stakes
- **类型**: strategic, tactical, operational
- **结果**: success, partial-success, failure, pending
- **学习**: breakthrough, challenge, pattern-identified

**示例**:
```python
"tags": ["career", "high-stakes", "strategic", "success"]
```

### 3. 搜索和检索

**常用搜索模式**:
```python
# 查找所有职业相关决策
list_memories(filter="decision_*", tags=["career"])

# 查找高风险决策
list_memories(filter="decision_*", tags=["high-stakes"])

# 查找特定模型的使用记录
read_memory("model_effectiveness_*")

# 查找需要回顾的决策
list_memories(filter="decision_*", review_date="<today")
```

### 4. 记忆维护

**每月清理**:
- 归档已完成的决策
- 更新决策结果
- 删除不再相关的快速日志

**每季度总结**:
- 生成思维模式报告
- 更新模型组合库
- 调整学习目标

---

## 🎓 进阶技巧

### 1. 决策质量评分系统

在 Template 3 中添加评分:
```python
"decision_quality_score": {
  "process_quality": 8,  # 分析过程质量 (1-10)
  "outcome_quality": 7,  # 实际结果质量 (1-10)
  "speed": 6,           # 决策速度 (1-10, 10=最快)
  "confidence_calibration": 9  # 信心校准 (1-10, 10=完美校准)
}
```

### 2. 模型效果矩阵

跟踪每个模型在不同场景下的表现:
```python
"model_effectiveness_matrix": {
  "First Principles": {
    "career_decisions": 9,
    "investment_decisions": 7,
    "product_decisions": 10,
    "personal_decisions": 8
  }
}
```

### 3. 思维模式演化追踪

记录思维能力的长期发展:
```python
"thinking_evolution": {
  "2026-Q1": "Level 1 - 学习基础模型",
  "2026-Q2": "Level 2 - 开始组合模型",
  "2026-Q3": "Level 2 - 熟练应用5个核心模型",
  "2026-Q4": "Level 3 - 创建个人框架"
}
```

---

## 📖 相关文档

- [SKILL.md](../../SKILL.md) - 技能主入口
- [detailed-guide.md](../../docs/detailed-guide.md) - 详细使用指南
- [decision-matrix.md](decision-matrix.md) - 决策矩阵模板
- [analysis-framework.md](analysis-framework.md) - 分析框架模板

---

**记住**: 记忆系统的价值在于持续使用。开始时可能感觉繁琐，但随着积累，你会建立起强大的个人决策知识库。

**最佳实践**: 从 Template 1 (决策记录) 和 Template 5 (快速日志) 开始，逐步扩展到其他模板。
