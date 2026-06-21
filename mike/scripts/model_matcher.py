#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mike Model Matcher v4.0 — 三层路由 + 全量模型索引

三层路由:
  Layer 1: 问题结构 (决策/诊断/预测/设计/优化/谈判/评估)
  Layer 2: 复杂度 (快速/标准/深度)
  Layer 3: 领域 (个人/商业/工程/社会/学术)

匹配流程:
  1. 识别问题结构 → 缩小类别范围
  2. 识别领域 → 进一步筛选
  3. 在候选类别中做 semantic-aware 匹配
  4. 交叉校验：模型组合是否自洽、类别是否多样
"""

import re
import json
import os
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from collections import Counter

# ============================================================
# LAYER 1: 问题结构 → 类别优先级
# ============================================================

STRUCTURE_ROUTING = {
    "决策": {
        "match": ["该不该", "要不要", "选哪个", "做决定", "应该做", "是否应该",
                  "我该如何选", "怎么选", "抉择", "要不要做", "能不能做",
                  "should i", "decide", "choose", "choice", "option",
                  "纠结", "犹豫", "两个都", "两个方向"],
        "priority_categories": [
            "strategic", "decision-making", "economics",
            "probability", "cognitive", "game-theory"
        ],
        "priority_models": [
            "First Principles", "Expected Value", "Opportunity Cost",
            "Second-Order Thinking", "Reversibility", "Regret Minimization"
        ]
    },
    "诊断": {
        "match": ["为什么", "原因", "根因", "怎么回事", "问题在哪",
                  "效率越来越差", "效果越来越差", "出问题", "失效",
                  "不work", "为什么失败", "哪里出了问题", "瓶颈",
                  "why", "root cause", "diagnose", "diagnosis", "broken",
                  "不再增长", "衰退", "越来越糟", "停滞不前", "不涨了"],
        "priority_categories": [
            "systems", "cognitive", "economics",
            "strategic", "complexity", "psychology-deep"
        ],
        "priority_models": [
            "Systems Thinking", "Feedback Loops", "Incentives",
            "First Principles", "Leverage Points", "Confirmation Bias"
        ]
    },
    "预测": {
        "match": ["会怎样", "如果", "那么", "趋势", "将来", "预测",
                  "后续影响", "后果", "导致", "长期", "走势",
                  "what if", "predict", "forecast", "consequence",
                  "万一", "有一天", "将来会", "会不会变成"],
        "priority_categories": [
            "strategic", "probability", "systems",
            "complexity", "risk-management", "economics"
        ],
        "priority_models": [
            "Second-Order Thinking", "Expected Value", "Feedback Loops",
            "Black Swan", "Scenario Planning", "Bayesian Thinking"
        ]
    },
    "设计": {
        "match": ["怎么设计", "架构", "构建", "打造", "体系", "框架",
                  "重新设计", "怎么搭", "怎么建", "怎么构建", "怎么组织",
                  "design", "architect", "build", "structure", "construct",
                  "设计一个", "从零开始", "from scratch", "搭建", "组建"],
        "priority_categories": [
            "design", "systems", "strategic", "innovation",
            "network-science", "project-management", "physics"
        ],
        "priority_models": [
            "Systems Thinking", "First Principles", "Gestalt Principles",
            "Visual Hierarchy", "Affordances", "Modularity",
            "Leverage Points", "Emergence"
        ]
    },
    "优化": {
        "match": ["怎么改进", "提效", "降低成本", "优化", "效率", "提升",
                  "提高", "改善", "改善什么", "增加", "减少", "精简",
                  "improve", "optimize", "efficiency", "reduce", "increase",
                  "增长", "增长率", "增速", "产能", "产出",
                  "降到", "缩短", "压缩", "加快", "提速", "加速",
                  "降本增效", "增效"],
        "priority_categories": [
            "systems", "economics", "strategic",
            "project-management", "physics", "learning"
        ],
        "priority_models": [
            "Leverage Points", "Marginal Thinking", "Inversion",
            "Pareto Principle", "Theory of Constraints", "Compounding",
            "Bottleneck Analysis", "Feedback Loops"
        ]
    },
    "谈判": {
        "match": ["怎么说服", "谈判", "利益分配", "博弈", "冲突",
                  "对方不答应", "不配合", "对抗", "竞争", "对手",
                  "negotiate", "convince", "persuade", "conflict",
                  "讨价", "还价", "分配", "公平", "份额",
                  "谈价格", "谈条件", "谈估值",
                  "怎么谈", "要价", "开价", "压价"],
        "priority_categories": [
            "game-theory", "communication", "psychology-deep",
            "behavioral-economics", "military-strategy", "cognitive"
        ],
        "priority_models": [
            "BATNA", "Nash Equilibrium", "Prisoner's Dilemma",
            "Reciprocity", "Framing", "Loss Aversion",
            "ZOPA", "Anchoring", "Win-Win Thinking"
        ]
    },
    "评估": {
        "match": ["值不值", "风险评估", "回报率", "估值", "评估",
                  "判断", "对比", "比较", "选哪个更好",
                  "evaluate", "assess", "rate", "compare", "worth",
                  "性价比", "投资回报", "ROI", "可行性", "会不会赔钱"],
        "priority_categories": [
            "probability", "risk-management", "economics",
            "decision-making", "financial-engineering", "data-science"
        ],
        "priority_models": [
            "Expected Value", "Risk Matrix", "Opportunity Cost",
            "Base Rates", "Margin of Safety", "Diversification",
            "Value at Risk", "Bayesian Thinking", "Stress Testing"
        ]
    },
    "学习": {
        "match": ["怎么学", "学习路径", "掌握", "技能提升", "入门",
                  "进修", "转行", "新领域", "能力提升", "成长",
                  "learn", "study", "skill", "master", "improve at",
                  "读书", "课程", "培训", "自学", "考证"],
        "priority_categories": [
            "learning", "cognitive", "psychology-deep",
            "neuroscience", "strategic", "communication"
        ],
        "priority_models": [
            "Spaced Repetition", "Deliberate Practice", "Metacognition",
            "Growth Mindset", "Chunking", "First Principles",
            "Cognitive Load Theory", "Interleaving"
        ]
    },
    "领导": {
        "match": ["怎么管", "领导", "团队", "带人", "下属不", "员工不",
                  "激励团队", "分权", "授权", "怎么让团队", "人心涣散",
                  "lead", "leadership", "team", "manage people",
                  "文化", "组织", "招人", "留人", "开除"],
        "priority_categories": [
            "management", "psychology-deep", "communication",
            "economics", "sociology", "cognitive"
        ],
        "priority_models": [
            "Psychological Safety", "Incentives", "Servant Leadership",
            "Delegation", "Feedback Culture", "OKRs",
            "Span of Control", "First Principles", "Growth Mindset"
        ]
    },
    "创新": {
        "match": ["怎么创新", "新点子", "创意", "不一样", "突破",
                  "颠覆", "差异化", "新方向", "独特", "蓝海",
                  "innovate", "creative", "disrupt", "novel", "unique",
                  "原创", "前所未有", "首创", "新型", "创新方案"],
        "priority_categories": [
            "innovation", "biology", "strategic", "design",
            "complexity", "cognitive-linguistics"
        ],
        "priority_models": [
            "First Principles", "Blue Ocean Strategy", "Disruptive Innovation",
            "Design Thinking", "SCAMPER", "Lateral Thinking",
            "Crossing the Chasm", "Jobs to be Done", "Analogical Thinking"
        ]
    }
}


# ============================================================
# LAYER 2: 复杂度预设
# ============================================================

COMPLEXITY_PRESETS = {
    "快速": {"max_models": 3, "allow_cross_validate": False},
    "标准": {"max_models": 5, "allow_cross_validate": True},
    "深度": {"max_models": 8, "allow_cross_validate": True}
}


# ============================================================
# LAYER 3: 领域 → 附加类别
# ============================================================

DOMAIN_BONUS = {
    "个人": ["psychology-deep", "behavioral-economics", "cognitive",
             "learning", "decision-making"],
    "商业": ["marketing", "management", "innovation",
             "financial-engineering", "competitive-strategy", "data-science"],
    "工程": ["systems", "physics", "project-management",
             "information-theory", "network-science", "mathematics"],
    "社会": ["sociology", "anthropology", "law-policy",
             "philosophy", "military-strategy", "communication"],
    "学术": ["mathematics", "philosophy", "complexity",
             "information-theory", "learning", "biology"]
}

DOMAIN_KEYWORDS = {
    "个人": ["我", "个人", "职业", "生活", "家庭", "感情", "健康",
             "my", "personal", "career", "life", "family"],
    "商业": ["公司", "企业", "部门", "产品", "客户", "市场", "收入",
             "利润", "增长策略", "竞争", "商业", "销售额",
             "company", "business", "product", "market", "revenue"],
    "工程": ["系统", "代码", "架构", "技术栈", "服务器", "接口",
             "数据", "算法", "基础设施", "部署",
             "system", "code", "architecture", "tech", "server"],
    "社会": ["社会", "公共", "政府", "政策", "群体", "文化", "道德",
             "society", "public", "government", "policy", "culture"],
    "学术": ["研究", "理论", "论文", "学术", "科学", "实验",
             "research", "theory", "academic", "science", "experiment"]
}


# 中文概念 → 英文模型名 映射 (bridge Chinese queries to English model names)
ZH_CONCEPT_BRIDGE = {
    # Strategic
    "第一性原理": ["First Principles Thinking", "First Principles"],
    "第一性": ["First Principles Thinking"],
    "二阶思维": ["Second-Order Thinking"],
    "二阶": ["Second-Order Thinking"],
    "机会成本": ["Opportunity Cost"],
    "逆向思维": ["Inversion"],
    "反证": ["Inversion"],
    "可逆性": ["Reversibility"],
    "沉没成本": ["Sunk Cost Fallacy", "Sunk Cost"],
    "长期": ["Long-Term Greedy", "Second-Order Thinking", "Compounding"],
    "复利": ["Compounding"],
    "安全边际": ["Margin of Safety"],
    "杠杆": ["Leverage Points", "Leverage"],
    "杠杆点": ["Leverage Points"],
    "帕累托": ["Pareto Principle"],
    "二八": ["Pareto Principle"],
    "瓶颈": ["Theory of Constraints", "Bottleneck Analysis"],
    "护城河": ["MOAT"],
    "选择权": ["Optionality"],

    # Systems
    "系统思维": ["Systems Thinking"],
    "反馈循环": ["Feedback Loops"],
    "反馈": ["Feedback Loops"],
    "涌现": ["Emergence"],

    # Cognitive
    "确认偏误": ["Confirmation Bias"],
    "确认偏差": ["Confirmation Bias"],
    "锚定": ["Anchoring", "Anchoring Effect"],
    "锚定效应": ["Anchoring Effect"],
    "框架效应": ["Framing", "Framing Effect"],
    "可得性偏差": ["Availability Heuristic"],
    "后见之明": ["Hindsight Bias"],

    # Probability
    "期望值": ["Expected Value"],
    "贝叶斯": ["Bayesian Thinking"],
    "基础概率": ["Base Rates"],
    "黑天鹅": ["Black Swan"],
    "概率": ["Bayesian Thinking", "Expected Value"],

    # Economics
    "激励": ["Incentives"],
    "激励机制": ["Incentives"],
    "供需": ["Supply and Demand"],
    "边际": ["Marginal Thinking"],
    "边际思维": ["Marginal Thinking"],
    "边际成本": ["Marginal Thinking"],
    "网络效应": ["Network Effects"],

    # Risk
    "风险": ["Risk Matrix", "Expected Value", "Margin of Safety"],
    "尾部风险": ["Tail Risk", "Black Swan"],
    "风险评估": ["Risk Matrix", "Expected Value", "Stress Testing"],
    "多元化": ["Diversification"],

    # Decision
    "决策": ["Decision Trees", "Expected Value", "Opportunity Cost"],
    "决策矩阵": ["Decision Trees"],
    "后悔": ["Regret Minimization"],

    # Game Theory
    "博弈": ["Nash Equilibrium", "Prisoner's Dilemma"],
    "囚徒困境": ["Prisoner's Dilemma"],
    "纳什": ["Nash Equilibrium"],
    "BATNA": ["BATNA"],
    "谈判": ["BATNA", "ZOPA", "Framing"],

    # Innovation / Design
    "创新": ["Disruptive Innovation", "Design Thinking", "Blue Ocean Strategy"],
    "设计思维": ["Design Thinking"],
    "蓝海": ["Blue Ocean Strategy"],
    "颠覆": ["Disruptive Innovation"],
    "差异化": ["Differentiation"],
    "最小可行": ["MVP"],
    "原型": ["Prototyping"],

    # Management
    "团队": ["Psychological Safety", "Incentives", "Feedback Culture"],
    "领导": ["Servant Leadership", "Delegation"],
    "心理安全": ["Psychological Safety"],
    "OKR": ["OKRs"],
    "激励团队": ["Incentives", "Psychological Safety"],

    # Learning
    "学习": ["Spaced Repetition", "Deliberate Practice", "Metacognition"],
    "刻意练习": ["Deliberate Practice"],
    "间隔重复": ["Spaced Repetition"],
    "元认知": ["Metacognition"],
    "成长心态": ["Growth Mindset"],

    # Finance
    "投资组合": ["Portfolio Theory", "Diversification"],
    "投资回报": ["Expected Value", "ROI"],
    "估值": ["Expected Value", "Margin of Safety"],

    # Product / Growth
    "产品": ["Jobs to be Done", "Product-Market Fit", "First Principles Thinking"],
    "用户体验": ["Design Thinking", "Cognitive Load Theory", "Affordances"],
    "留存": ["Network Effects", "Feedback Loops", "Incentives"],
    "增长": ["Network Effects", "Compounding", "Feedback Loops"],
    "增长策略": ["Network Effects", "Expected Value", "Feedback Loops"],
    "转化": ["Framing", "Incentives", "Loss Aversion"],
    "转化率": ["Framing", "Social Proof", "Loss Aversion"],
    "产品市场契合": ["Product-Market Fit"],
    "PMF": ["Product-Market Fit"],

    # Communication
    "说服": ["Reciprocity", "Framing", "Social Proof"],
    "社会证明": ["Social Proof"],
    "互惠": ["Reciprocity"],

    # Physics analogy
    "惯性": ["Inertia"],
    "熵": ["Entropy"],
    "相变": ["Phase Transitions"],
    "临界点": ["Critical Mass", "Tipping Point"],
    "临界": ["Critical Mass", "Tipping Point"],

    # ── Musk Methodology (H3 models) ──
    "白痴指数": ["Idiot Index"],
    "五步工作法": ["The Five-Step Algorithm", "5 Whys"],
    "原型优先": ["Prototype First", "Prototyping"],
    "特种部队": ["Special Forces Model", "Task Force"],
    "极限思维": ["Limit Thinking"],
    "物理学思维": ["Physics Thinking", "First Principles Thinking"],
    "使命驱动": ["Mission-Driven Selection"],
    "能力圈": ["Competence Expansion", "Circle of Competence"],
    "嚼碎玻璃": ["Glass Chewing", "Grit", "Resilience"],
    "凝视深渊": ["Staring into the Abyss", "Worst-Case Analysis"],
    "时间至上": ["Time Supremacy", "Compounding", "Urgency"],
    "勇敢冒险": ["Courage to Risk", "Risk Appetite"],
    "从0到1": ["First Principles Thinking", "Blue Ocean Strategy"],

    # ── Sub-system models ──
    "正反馈": ["Reinforcing (Positive) Loops", "Feedback Loops"],
    "负反馈": ["Balancing (Negative) Loops", "Feedback Loops"],
    "强化循环": ["Reinforcing (Positive) Loops"],
    "平衡循环": ["Balancing (Negative) Loops"],

    # Problem diagnosis
    "为什么": ["First Principles Thinking", "Systems Thinking", "Feedback Loops"],
    "根因": ["First Principles Thinking", "5 Whys", "Root Cause Analysis"],
    "怎么回事": ["Systems Thinking", "Feedback Loops"],
    "不涨": ["Feedback Loops", "Leverage Points", "Network Effects"],
    "衰退": ["Feedback Loops", "Second-Order Thinking"],
    "越来越差": ["Feedback Loops", "Systems Thinking", "Incentives"],
    "失效": ["Feedback Loops", "First Principles Thinking"],
    "问题": ["First Principles Thinking", "Systems Thinking"],

    # ── Expanded synonyms (v4.1) ──
    # Career / Life decisions
    "离职": ["Opportunity Cost", "Expected Value", "Regret Minimization"],
    "跳槽": ["Opportunity Cost", "Expected Value", "Regret Minimization"],
    "换工作": ["Opportunity Cost", "Expected Value", "Regret Minimization"],
    "职业转换": ["Opportunity Cost", "Expected Value", "Regret Minimization", "Second-Order Thinking"],
    "职业规划": ["Second-Order Thinking", "Compounding", "Opportunity Cost"],
    "换个环境": ["Opportunity Cost", "Reversibility", "Expected Value"],

    # Thinking / Analysis
    "从本质出发": ["First Principles Thinking"],
    "回归本源": ["First Principles Thinking"],
    "根本原因": ["First Principles Thinking", "Root Cause Analysis", "5 Whys"],
    "底层逻辑": ["First Principles Thinking"],
    "重新审视": ["First Principles Thinking", "Inversion", "Second-Order Thinking"],
    "换个角度": ["Inversion", "Lateral Thinking", "Reframing"],
    "跳出框架": ["Inversion", "Lateral Thinking", "First Principles Thinking"],
    "长期影响": ["Second-Order Thinking", "Compounding"],
    "隐藏代价": ["Second-Order Thinking", "Opportunity Cost"],
    "连锁反应": ["Second-Order Thinking", "Feedback Loops"],

    # Decision quality
    "判断力": ["Confirmation Bias", "Metacognition", "Bayesian Thinking"],
    "决策质量": ["Decision Trees", "Expected Value", "Confirmation Bias"],
    "做错了": ["Confirmation Bias", "Hindsight Bias", "Inversion"],
    "后悔": ["Regret Minimization", "Sunk Cost Fallacy"],
    "纠结": ["Decision Trees", "Opportunity Cost", "Reversibility"],
    "两难": ["Decision Trees", "Opportunity Cost", "Trade-off Analysis"],
    "犹豫": ["Reversibility", "Opportunity Cost", "Regret Minimization"],

    # Growth / Business
    "不增长": ["Feedback Loops", "Leverage Points", "Network Effects"],
    "增长停滞": ["Feedback Loops", "Leverage Points", "Second-Order Thinking"],
    "越投越差": ["Diminishing Returns", "Feedback Loops", "Sunk Cost Fallacy"],
    "投入产出": ["Expected Value", "Marginal Thinking", "Pareto Principle"],
    "回报低": ["Expected Value", "Marginal Thinking", "Opportunity Cost"],
    "竞争激烈": ["Competitive Strategy", "Differentiation", "Blue Ocean Strategy"],
    "对手": ["Game Theory", "Competitive Strategy", "Nash Equilibrium"],
    "市场进入": ["Scenario Planning", "Expected Value", "Blue Ocean Strategy"],

    # Team / People
    "团队协作": ["Psychological Safety", "Incentives", "Feedback Culture"],
    "不配合": ["Incentives", "Game Theory", "BATNA"],
    "氛围差": ["Psychological Safety", "Incentives", "Systems Thinking"],
    "留不住人": ["Incentives", "Psychological Safety", "Opportunity Cost"],
    "执行力": ["Theory of Constraints", "OKRs", "Feedback Loops"],
    "内耗": ["Game Theory", "Incentives", "Systems Thinking"],

    # Learning / Growth
    "入门": ["Deliberate Practice", "Spaced Repetition", "Chunking"],
    "掌握": ["Deliberate Practice", "Metacognition", "Growth Mindset"],
    "效率低": ["Pareto Principle", "Leverage Points", "Theory of Constraints"],
    "学不会": ["Deliberate Practice", "Metacognition", "Cognitive Load Theory"],
    "怎么进步": ["Deliberate Practice", "Growth Mindset", "Feedback Loops"],

    # Risk / Uncertainty
    "不确定": ["Bayesian Thinking", "Optionality", "Scenario Planning"],
    "最坏情况": ["Worst-Case Analysis", "Margin of Safety", "Stress Testing"],
    "万一": ["Black Swan", "Tail Risk", "Scenario Planning"],
    "保底": ["Margin of Safety", "BATNA", "Optionality"],
    "会不会赔": ["Expected Value", "Risk Matrix", "Margin of Safety"],

    # Conflict / Negotiation
    "谈价格": ["BATNA", "ZOPA", "Anchoring"],
    "谈条件": ["BATNA", "Reciprocity", "Framing"],
    "议价": ["BATNA", "ZOPA", "Anchoring"],
    "博弈": ["Nash Equilibrium", "Prisoner's Dilemma", "Game Theory"],
    "利益冲突": ["Game Theory", "BATNA", "Incentives"],

    # Innovation / Product
    "没差异": ["Differentiation", "Blue Ocean Strategy", "Jobs to be Done"],
    "同质化": ["Differentiation", "Blue Ocean Strategy", "First Principles Thinking"],
    "新方向": ["First Principles Thinking", "Blue Ocean Strategy", "Design Thinking"],
    "怎么创新": ["First Principles Thinking", "Disruptive Innovation", "Lateral Thinking"],
    "产品方向": ["Jobs to be Done", "First Principles Thinking", "Product-Market Fit"],
}

# Section headers that are NOT model names
NON_MODEL_HEADERS = {
    # English section headers
    "overview", "introduction", "summary", "core models", "key models",
    "key concepts", "principles", "how to use", "when to use", "questions",
    "questions to ask", "example", "examples", "pitfalls", "common pitfalls",
    "applications", "application", "further reading", "references",
    "see also", "related", "resources", "tips", "notes", "conclusion",
    "faq", "appendix", "getting started", "quick start", "usage",
    "how it works", "benefits", "limitations", "warning", "caution",
    "quick tips", "stages", "stages of competence", "stages of learning",
    "components", "causes", "rules", "method", "formula", "key insight",
    "integration with other models", "practical applications",
    "further reading and resources", "related concepts",
    # Chinese section headers (musk-methodology and general)
    "总览", "方向选择", "思维引擎", "执行算法", "心智韧性",
    "模型组合推荐", "与其他", "适用场景速查", "总结", "参考",
    "第1层", "第2层", "第3层", "第4层",
    "第1层：方向选择", "第2层：思维引擎", "第3层：执行算法", "第4层：心智韧性",
    "总览：马斯克方法论的四层架构",
    "模型组合推荐", "与其他 mike 模型的映射", "适用场景速查",
    # Sub-section headers (musk-methodology H3 structural, not models)
    "从0到1创业", "成本优化", "产品设计", "团队建设", "心智锻造",
}


# ============================================================
# 模型索引构建
# ============================================================

def parse_reference_files(ref_dir: str) -> Dict[str, Dict]:
    """Parse all reference markdown files and extract model entries.

    Multi-strategy extraction:
    1. `## Model Name` headers — primary model definitions (standard files)
    2. `### Sub-Model Name` headers — sub-models within section-structured files
       (e.g. musk-methodology.md, systems.md where ## are sections and ### are models)
    """
    models = {}
    ref_path = Path(ref_dir)

    if not ref_path.exists():
        return models

    for md_file in sorted(ref_path.glob("*.md")):
        if md_file.name in ("README.md", "vds-framework.md", "frameworks.md"):
            continue

        category = md_file.stem

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # ── Strategy 1: ## headers as primary model names ──
        for match in re.finditer(r'^##\s+(.+?)$', content, re.MULTILINE):
            name = match.group(1).strip()
            if _is_header_noise(name):
                continue

            start = match.end()
            desc = _extract_description(content[start:])
            first_sentence = _first_sentence(desc)

            _add_model(models, name, category, first_sentence)

        # ── Strategy 2: ### headers as sub-models ──
        # Files like musk-methodology.md use ## for sections and ### for models.
        # Track current ## section to provide context.
        current_section = ""
        for line in content.split("\n"):
            h2_match = re.match(r'^##\s+(.+?)$', line)
            h3_match = re.match(r'^###\s+(.+?)$', line)

            if h2_match:
                current_section = h2_match.group(1).strip()
            elif h3_match:
                name = h3_match.group(1).strip()
                if _is_header_noise(name):
                    continue
                desc_ctx = f"(in {current_section})" if current_section else ""
                _add_model(models, name, category, desc_ctx)

    return models


def _is_header_noise(name: str) -> bool:
    """Check if a header name is structural noise, not a model."""
    if len(name) < 3 or len(name) > 100:
        return True
    if name.lower() in NON_MODEL_HEADERS:
        return True
    # Chinese section patterns: "第X层", "第X步", etc.
    if re.match(r'^第\d+[层步节章篇部]', name):
        return True
    # Structural patterns like "工具1：xxx" or "案例：xxx"
    if re.match(r'^(工具\d+|案例)[：:]', name):
        return True
    return False


def _extract_description(text_after_header: str) -> str:
    """Extract description text after a header until next header or separator."""
    desc_match = re.search(r'(.*?)(?=\n##|\n---|\n\n##)', text_after_header, re.DOTALL)
    return desc_match.group(1).strip()[:300] if desc_match else ""


def _first_sentence(desc: str, min_len: int = 10) -> str:
    """Extract first meaningful sentence from a description."""
    if not desc:
        return ""
    first = re.split(r'[.\n]', desc)[0].strip()
    if len(first) < min_len:
        first = desc[:150]
    return first[:200]


def _add_model(models: Dict, name: str, category: str, description: str):
    """Add or merge a model entry into the index."""
    key = name.lower()
    if key in models:
        # Merge: keep the entry with a better description
        existing_desc = models[key].get("description", "")
        if len(description) > len(existing_desc):
            models[key]["description"] = description
            # Update category only if the new one is more specific
            if category not in ("frameworks",):
                models[key]["category"] = category
    else:
        models[key] = {
            "name": name,
            "category": category,
            "description": description[:200],
            "keywords": _extract_keywords(name, description)
        }

# ============================================================
# 跨语言 Tokenization
# ============================================================


def _extract_keywords(name: str, desc: str) -> List[str]:
    """Extract meaningful keywords from model name and description."""
    combined = f"{name} {desc}"
    tokens = _tokenize_english(combined)
    # Remove very common words
    stopwords = {"the", "a", "an", "of", "in", "to", "and", "is", "or",
                 "for", "with", "on", "that", "this", "it", "as", "by",
                 "be", "are", "was", "not", "from", "at", "but", "can"}
    return [t for t in tokens if t not in stopwords and len(t) > 1]


# ============================================================
# 跨语言 Tokenization
# ============================================================

def _tokenize_english(text: str) -> List[str]:
    """Tokenize English text into lowercase words."""
    return re.findall(r'[a-zA-Z]{2,}', text.lower())


def _tokenize_chinese(text: str) -> List[str]:
    """Tokenize Chinese using character bigrams (no external deps needed).

    Bigram segmentation captures multi-character terms like "决策"/"风险"/"系统"
    without needing a dictionary. Single characters are also included for
    single-character matches.
    """
    # Extract Chinese character sequences
    chinese_chars = re.findall(r'[一-鿿]+', text)
    tokens = []
    for seq in chinese_chars:
        # Bigrams
        for i in range(len(seq) - 1):
            tokens.append(seq[i:i+2])
        # Also keep unigrams for short-term matching
        for ch in seq:
            tokens.append(ch)
    return tokens


def tokenize(text: str) -> List[str]:
    """Unified tokenization: Chinese bigrams + English words."""
    en_tokens = _tokenize_english(text)
    zh_tokens = _tokenize_chinese(text)
    return en_tokens + zh_tokens


# ============================================================
# 三层路由匹配
# ============================================================

def identify_structure(problem: str) -> str:
    """Identify problem structure type from query text."""
    scores = {}
    problem_lower = problem.lower()

    for struct_name, config in STRUCTURE_ROUTING.items():
        score = 0
        for keyword in config["match"]:
            if keyword.lower() in problem_lower:
                # Longer keyword matches are stronger signals
                score += len(keyword) * (3.0 if len(keyword) >= 4 else 1.0)
        scores[struct_name] = score

    if not scores or max(scores.values()) == 0:
        return "诊断"  # default fallback

    return max(scores, key=scores.get)


def identify_domain(problem: str) -> str:
    """Identify domain from query text."""
    scores = {}
    problem_lower = problem.lower()

    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw.lower() in problem_lower:
                score += len(kw) * 2.0
        scores[domain] = score

    if not scores or max(scores.values()) == 0:
        return "个人"  # default fallback

    return max(scores, key=scores.get)


def identify_complexity(problem: str) -> str:
    """Heuristic complexity detection based on query signals."""
    deep_signals = ["深度", "全面", "彻底", "五个维度", "五维",
                    "多角度", "系统性", "全方位", "详细", "仔细",
                    "deep", "thorough", "comprehensive", "full analysis"]
    quick_signals = ["快速", "简单", "大概", "粗略", "大致",
                     "quick", "fast", "simple", "brief", "一分钟"]

    problem_lower = problem.lower()

    for sig in deep_signals:
        if sig.lower() in problem_lower:
            return "深度"
    for sig in quick_signals:
        if sig.lower() in problem_lower:
            return "快速"

    return "标准"


# ============================================================
# 模型评分
# ============================================================

def score_models(
    query_tokens: List[str],
    candidate_categories: List[str],
    model_index: Dict[str, Dict],
    query_lower: str,
    priority_models: Optional[List[str]] = None
) -> List[Tuple[str, float, Dict]]:
    """Score all models against query, prioritizing candidate categories.

    Uses four signal types:
    1. Chinese concept bridge (ZH_CONCEPT_BRIDGE) — map Chinese terms to model names
    2. Keyword matching against model keywords + description
    3. Category bonus for models in priority categories
    4. Priority model bonus — structure-specific models get extra weight
    """
    scored = []
    priority_set = set(p.lower() for p in (priority_models or []))

    # Resolve Chinese concepts to target model names
    zh_matched_models: Dict[str, float] = {}  # model_name → bonus score
    for zh_term, model_names in ZH_CONCEPT_BRIDGE.items():
        if zh_term in query_lower:
            for mn in model_names:
                key = mn.lower()
                zh_matched_models[key] = max(
                    zh_matched_models.get(key, 0),
                    len(zh_term) * 1.5  # longer match = stronger signal
                )

    for model_name, model_data in model_index.items():
        score = 0.0
        category = model_data["category"]

        # Category bonus
        if category in candidate_categories:
            score += 3.0
            # Extra bonus for top-priority categories (first 3)
            if category in candidate_categories[:3]:
                score += 1.0

        # Priority model bonus — structure-curated models get strong boost
        key = model_name.lower()
        if key in priority_set:
            score += 6.0

        # Chinese concept bridge bonus
        if key in zh_matched_models:
            score += zh_matched_models[key]

        # English keyword matching
        keywords = model_data.get("keywords", [])
        for kw in keywords:
            if kw.lower() in query_lower:
                score += 2.0
            kw_tokens = _tokenize_english(kw)
            for kt in kw_tokens:
                if kt in query_tokens:
                    score += 0.3

        # Model name literal match
        if key in query_lower:
            score += 5.0

        # Name tokens match in query
        name_tokens = _tokenize_english(model_name)
        for nt in name_tokens:
            if nt in query_tokens:
                score += 1.0

        if score > 0:
            scored.append((model_name, score, model_data))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


# ============================================================
# 交叉校验
# ============================================================

def cross_validate(selected: List[Tuple[str, float, Dict]]) -> Dict:
    """Validate that the selected model combination is coherent.

    Checks:
    1. Category diversity — are we drawing from enough categories?
    2. Redundancy — are any models too similar?
    3. Blind spots — are any key categories missing?
    """
    if len(selected) < 2:
        return {"ok": True, "warnings": [], "missing_categories": []}

    categories = [m[2]["category"] for m in selected]
    cat_counts = Counter(categories)

    warnings = []

    # Check: all from same category
    if len(set(categories)) == 1 and len(selected) >= 3:
        warnings.append(
            f"所有{len(selected)}个模型来自同一类别 ({categories[0]})，"
            f"建议引入其他视角"
        )

    # Check for essential missing categories
    essential = {
        "cognitive": "认知偏差检查",
        "strategic": "战略/根本性思考",
        "systems": "系统性视角"
    }
    missing = []
    for cat, label in essential.items():
        if cat not in categories:
            missing.append(f"{label} ({cat})")

    return {
        "ok": len(warnings) == 0,
        "warnings": warnings,
        "missing_categories": missing
    }


# ============================================================
# 主匹配函数
# ============================================================

def match_models(
    problem: str,
    top_n: int = 5,
    complexity: Optional[str] = None,
    structure: Optional[str] = None,
    domain: Optional[str] = None,
    verbose: bool = False
) -> Dict:
    """Match mental models using three-layer routing.

    Args:
        problem: Problem description (Chinese or English)
        top_n: Max models to return
        complexity: Override auto-detected complexity
        structure: Override auto-detected structure (skip keyword matching)
        domain: Override auto-detected domain (skip keyword matching)
        verbose: Include debug info in output

    Returns:
        Dict with routing info and matched models
    """
    # Build model index
    script_dir = Path(__file__).parent.parent
    ref_dir = script_dir / "references"
    model_index = parse_reference_files(str(ref_dir))

    if verbose:
        print(f"[DEBUG] Loaded {len(model_index)} models from reference files")

    # Layer 1: Identify structure (use explicit if provided)
    if structure is not None and structure in STRUCTURE_ROUTING:
        pass  # use explicit
    else:
        structure = identify_structure(problem)

    struct_config = STRUCTURE_ROUTING[structure]

    # Layer 2: Identify complexity (use explicit if provided)
    if complexity is None:
        complexity = identify_complexity(problem)
    elif complexity not in COMPLEXITY_PRESETS:
        complexity = identify_complexity(problem)

    # Layer 3: Identify domain (use explicit if provided)
    if domain is not None and domain in DOMAIN_BONUS:
        pass  # use explicit
    else:
        domain = identify_domain(problem)

    # Build candidate category list
    candidate_categories = list(struct_config["priority_categories"])
    # Add domain-specific bonus categories
    for bonus_cat in DOMAIN_BONUS.get(domain, []):
        if bonus_cat not in candidate_categories:
            candidate_categories.append(bonus_cat)

    # Tokenize query
    query_tokens = tokenize(problem)
    query_lower = problem.lower()

    # Score all models
    priority_models = struct_config.get("priority_models", [])
    scored = score_models(
        query_tokens, candidate_categories, model_index, query_lower,
        priority_models=priority_models
    )

    # Apply complexity limit
    max_models = COMPLEXITY_PRESETS[complexity]["max_models"]
    selected = scored[:max(top_n * 3, 20)]  # get more for diversity selection

    # Ensure category diversity: pick top per category first
    seen_categories = set()
    diverse_selection = []
    for model in selected:
        cat = model[2]["category"]
        if cat not in seen_categories:
            diverse_selection.append(model)
            seen_categories.add(cat)
        else:
            # Only add same-category models after we have 3+ categories
            if len(seen_categories) >= 3:
                diverse_selection.append(model)

    # Fill remaining slots with best-scoring models not yet included
    selected_names = {m[0] for m in diverse_selection}
    for model in selected:
        if model[0] not in selected_names and len(diverse_selection) < top_n:
            diverse_selection.append(model)
            selected_names.add(model[0])

    final_selection = diverse_selection[:top_n]

    # Cross-validate
    validation = cross_validate(final_selection)

    # Also include priority models that might not have matched via keywords
    # but are highly relevant for the problem structure
    priority_fallback = []
    selected_names_final = {m[0] for m in final_selection}
    for pm_name in struct_config["priority_models"]:
        if pm_name not in selected_names_final and pm_name in model_index:
            priority_fallback.append(
                (pm_name, 1.0, model_index[pm_name])
            )

    return {
        "routing": {
            "structure": structure,
            "complexity": complexity,
            "domain": domain,
            "candidate_categories": candidate_categories
        },
        "models": final_selection,
        "priority_fallback": priority_fallback[:2],
        "validation": validation,
        "total_models_loaded": len(model_index)
    }


# ============================================================
# 输出格式化
# ============================================================

def render_output(result: Dict) -> str:
    """Render match results in a structured format for the LLM to consume."""
    routing = result["routing"]
    validation = result["validation"]
    models = result["models"]

    lines = []
    lines.append(f"## Mike 路由决策")
    lines.append(f"")
    lines.append(f"**问题结构**: {routing['structure']} | **复杂度**: {routing['complexity']} | **领域**: {routing['domain']}")
    lines.append(f"**候选类别**: {', '.join(routing['candidate_categories'][:8])}")
    lines.append(f"**模型库大小**: {result['total_models_loaded']} 个模型已索引")
    lines.append(f"")

    if validation.get("warnings"):
        lines.append(f"### 交叉校验警告")
        for w in validation["warnings"]:
            lines.append(f"- ⚠️ {w}")
        lines.append(f"")

    if validation.get("missing_categories"):
        lines.append(f"### 建议补充视角")
        for m in validation["missing_categories"]:
            lines.append(f"- {m}")
        lines.append(f"")

    lines.append(f"### 匹配模型 (Top {len(models)})")
    lines.append(f"")
    lines.append(f"| # | 模型 | 类别 | 得分 | 一句话 |")
    lines.append(f"|---|------|------|------|--------|")
    for i, (name, score, data) in enumerate(models, 1):
        desc = data.get("description", "")[:60]
        lines.append(f"| {i} | **{name}** | {data['category']} | {score:.1f} | {desc} |")
    lines.append(f"")

    if result["priority_fallback"]:
        lines.append(f"### 结构推荐补充")
        for name, score, data in result["priority_fallback"]:
            lines.append(f"- **{name}** ({data['category']}): {data.get('description', '')[:80]}")
        lines.append(f"")

    # Actionable next steps
    lines.append(f"### 分析建议")
    lines.append(f"")
    lines.append(f"1. 用上述 {len(models)} 个模型构建**框架-证据-结论**对照表")
    lines.append(f"2. 至少做 1 条反证检查：什么证据会推翻当前判断？")
    lines.append(f"3. 至少做 1 条认知偏差检查（确认偏误/锚定/沉没成本）")
    lines.append(f"4. 输出 P0/P1/P2 分层行动 + 止损/回滚条件")

    return "\n".join(lines)


def print_results(result: Dict):
    """Simple terminal output."""
    print(render_output(result))


# ============================================================
# Trigger Detection (for skill activation gating)
# ============================================================

# Signal words that indicate a query needs mental-model analysis
TRIGGER_SIGNALS = [
    # Decision signals
    "该不该", "要不要", "选哪个", "怎么选", "抉择", "纠结",
    "要不要做", "能不能做", "是否应该", "如何选择",
    "权衡", "两难", "选A", "还是做", "还是继续",
    # Diagnosis signals
    "为什么", "根因", "怎么回事", "问题在哪", "出问题",
    "失效", "越来越差", "不涨", "衰退", "停滞",
    # Evaluation signals
    "值不值", "风险评估", "可行性", "回报率", "性价比",
    "会不会赔", "ROI", "投资回报",
    # Negotiation signals
    "怎么说服", "谈判", "利益分配", "博弈", "对方不",
    "讨价", "还价",
    # Innovation signals
    "差异化", "颠覆", "蓝海", "新点子", "突破",
    # Learning signals
    "怎么学", "学习路径", "转行", "技能提升",
    # Leadership signals
    "怎么管", "团队不", "下属", "员工不", "人心",
    "心理安全", "怎么让团队",
    # Design signals
    "怎么设计", "怎么构建", "怎么搭建", "从零开始",
    # Explicit invocation
    "思维模型", "mental model", "mike",
]

# Negative signals that indicate pure execution / not analytical
NEGATIVE_SIGNALS = [
    "写一个", "帮我写", "代码", "组件", "脚本",
    "500", "报错", "bug", "修一下",
    "翻译成", "翻译", "translate",
    "nginx", "配置", "rate limit",
    "PRD", "需求文档",
]


def should_trigger(problem: str) -> bool:
    """Determine whether the mike skill should activate for a query.

    Uses layered signal detection: strong analytical terms → trigger;
    positive signal words + analysis intent → trigger; explicit opt-out → suppress.

    Returns True if mental-model analysis is likely needed.
    """
    query = problem.lower()

    # Explicit opt-out: user says they don't want analysis
    opt_out = ["不必上升到", "不要用思维模型", "不用分析", "只是个简单",
               "就按普通计划", "不必...分析", "不需要深度"]
    if any(s.lower() in query for s in opt_out):
        return False

    # Explicit "mike" invocation always triggers
    if "mike" in query:
        return True

    # Strong analytical terms — frameworks, named biases, specific models
    strong_analytical = [
        "二阶思维", "第一性原理", "机会成本", "期望值",
        "系统思维", "博弈论", "batna", "尾部风险", "认知偏差",
        "蓝海战略", "心理安全", "刻意练习", "框架效应",
        "沉没成本", "确认偏误", "锚定效应", "贝叶斯",
        "黑天鹅", "激励机制", "反馈循环", "安全边际"
    ]
    if any(s.lower() in query for s in strong_analytical):
        return True

    # Analysis intent words — indicate user wants structured thinking
    analysis_intent = ["分析", "拆解", "评估", "审视", "判断", "权衡",
                       "诊断", "思考", "帮我看看", "帮我梳理", "怎么看"]

    positive_hits = sum(1 for s in TRIGGER_SIGNALS if s.lower() in query)
    negative_hits = sum(1 for s in NEGATIVE_SIGNALS if s.lower() in query)
    has_intent = any(w.lower() in query for w in analysis_intent)

    # Pure execution with no analytical intent → skip
    if negative_hits >= 2 and positive_hits == 0:
        return False

    # Positive signal + analysis intent → trigger
    if positive_hits >= 1 and has_intent:
        return True

    # Multiple positive signals → trigger
    if positive_hits >= 2:
        return True

    return False


def run_eval(evals_path: str) -> Dict:
    """Run trigger evaluation against a JSON eval file.

    Returns dict with accuracy, failures, and per-case results.
    """
    import json
    with open(evals_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    results = []
    correct = 0
    total = 0

    for case in cases:
        query = case["query"]
        expected = case["should_trigger"]
        predicted = should_trigger(query)
        ok = predicted == expected
        if ok:
            correct += 1
        total += 1
        results.append({
            "query": query[:80],
            "expected": expected,
            "predicted": predicted,
            "ok": ok
        })

    return {
        "accuracy": correct / total if total > 0 else 0,
        "correct": correct,
        "total": total,
        "failures": [r for r in results if not r["ok"]]
    }


# ============================================================
# CLI
# ============================================================

def main():
    import sys

    args = sys.argv[1:]

    if "--eval" in args:
        script_dir = Path(__file__).parent.parent
        evals_path = script_dir / "evals" / "trigger-eval.json"
        result = run_eval(str(evals_path))
        print(f"Trigger Eval: {result['correct']}/{result['total']} correct ({result['accuracy']:.1%})")
        if result["failures"]:
            print("\nFailures:")
            for f in result["failures"]:
                print(f"  [{f['expected']}→{f['predicted']}] {f['query']}")
        return

    if args:
        # Parse named flags
        flags = {"-v"}
        named_flags = {"--structure", "--domain", "--complexity"}
        query_parts = []
        explicit_structure = None
        explicit_domain = None
        explicit_complexity = None

        i = 0
        while i < len(args):
            if args[i] == "--structure" and i + 1 < len(args):
                explicit_structure = args[i + 1]
                i += 2
            elif args[i] == "--domain" and i + 1 < len(args):
                explicit_domain = args[i + 1]
                i += 2
            elif args[i] == "--complexity" and i + 1 < len(args):
                explicit_complexity = args[i + 1]
                i += 2
            elif args[i] not in flags and args[i] not in named_flags:
                query_parts.append(args[i])
                i += 1
            else:
                i += 1

        problem = " ".join(query_parts)
        result = match_models(
            problem, top_n=5,
            structure=explicit_structure,
            domain=explicit_domain,
            complexity=explicit_complexity,
            verbose=("-v" in args)
        )
        print_results(result)
    else:
        print("\n" + "=" * 60)
        print("  Mike Model Matcher v4.1 — 三层路由 + 显式路由")
        print("=" * 60)
        print(f"\n  Usage: python model_matcher.py \"your problem\"")
        print(f"  Options:")
        print(f"    --structure TYPE   Override auto-detected structure")
        print(f"    --domain TYPE      Override auto-detected domain")
        print(f"    --complexity TYPE  Override auto-detected complexity")
        print(f"    -v                Verbose mode")
        print(f"    --eval            Run trigger evaluation")
        print(f"\n  Structures: 决策/诊断/预测/设计/优化/谈判/评估/学习/领导/创新")
        print(f"  Domains:    个人/商业/工程/社会/学术")
        print(f"  Complexity: 快速/标准/深度")
        print(f"\n  示例:")
        print(f'    python model_matcher.py "我该不该换工作？"')
        print(f'    python model_matcher.py "为什么团队效率越来越差？" --structure 诊断 --domain 商业')
        print(f'    python model_matcher.py --eval')
        print()


if __name__ == "__main__":
    main()