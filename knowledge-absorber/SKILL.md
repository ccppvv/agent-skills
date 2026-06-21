---
name: knowledge-absorber
description: 深度解析链接、文档或代码，生成"全能导师级"的教学笔记（零基础直达精通）。具备"真理锚定"校验能力，自动识别幻觉与过时信息。
tags: ["learning","学习","analysis","分析","documentation","文档","knowledge-base","知识库","知识吸收","knowledge-absorber"]
version: 4.4.0
---

# Knowledge Absorber (知识吸收器)

深度解析链接、文档或代码，生成结构化的"知识晶体"（Markdown + HTML）。

SKILL_PATH = `~/.claude/skills/knowledge-absorber`

## 核心流程 (Core Workflow)

采用 **三级加载机制** 配合 **真理锚定协议**。严格按以下步骤执行。

### 第一步：智能摄取 (Content Ingestion)

运行脚本获取干净的 Markdown 数据。脚本自动清洗 HTML 噪音并处理多模态内容（PDF/OCR）。

1. **运行摄取脚本**：
   ```bash
   python3 ~/.claude/skills/knowledge-absorber/scripts/content_ingester.py "INPUT_URL_OR_PATH"
   ```
   - **依赖自愈**: 若发现 `ImportError`，立即执行 `pip install -r ~/.claude/skills/knowledge-absorber/requirements.txt`，无需询问用户。

2. **读取结果**：
   - 读取 `~/.claude/skills/knowledge-absorber/config/raw_content.txt`
   - 该文件已通过 `html2text` 清洗，可直接用于分析。

### 第二步：真理锚定 (Truth Anchoring)

**"不要轻信任何文本，哪怕它看起来很专业。"**

1. **提取核心主张**：扫描 `raw_content.txt`，提取所有关键事实性主张。
   - 重点关注：具体数据、代码 API 用法、历史事件、绝对化论断。

2. **联网审计**：调用 `WebSearch`，针对每个主张构造验证性搜索。
   - 必须包含当前年份以确保时效性。

3. **生成校准报告**：如发现原文有误、过时或存在争议，必须在教学笔记中显式标注。

### 第三步：加载导师人格 (Load Persona)

读取系统提示词以激活"首席认知架构师"人格：
```bash
cat ~/.claude/skills/knowledge-absorber/references/system_prompt.md
```
将读取到的内容作为 System Prompt 注入当前上下文。

### 第四步：生成教学内容 (Generate Content)

根据 `raw_content.txt` + `system_prompt.md` + 校准报告，生成多模态输出：

1. **结构化输出**：严格遵循 `system_prompt.md` 中的 [Construct Narrative] 章节定义。
2. **生成与写入**：
   - 同时生成 Markdown 和 HTML 文件
   - 写入位置：项目根目录下 `knowledge_{YYYYMMDD}_{Title}/`
   - 技术类 → Preset A（现代清爽）；国学/人文类 → Preset B（水墨清茶）

### 第五步：质量验收 (Quality Assurance)

交付前必须自检：
- [ ] HTML 是否包含 `<script>` 搜索逻辑？
- [ ] 国学模式下，是否使用了"扪心自问"和"藏经阁"标题？
- [ ] 是否包含 Mermaid 认知地图？
- [ ] 是否包含 5-8 个自测题？

若任一项缺失，必须重新生成。

## 何时调用

1. **显式学习指令**：用户说"学习这个"、"深度分析"、"解析链接"、"解释这个概念"
2. **复杂多模态输入**：用户提供 URL 链接、上传 PDF/Word/Markdown/图片
3. **代码深度解析**：用户问"这段代码是怎么跑的？"、"架构是怎样的？"
4. **隐式教学需求**：用户说"我不理解"、"太难了"、"用大白话解释一下"

## 依赖安装

```bash
pip install -r ~/.claude/skills/knowledge-absorber/requirements.txt
```

核心依赖：requests, beautifulsoup4, pypdf, html2text, DrissionPage, rich, tqdm

## 搜索增强
整个过程中，所有需要联网搜索互联网上内容的场景，使用 /agent-reach 来进行增强搜索
