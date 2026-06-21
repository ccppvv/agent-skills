[35m项目结构 (全在线递归扫描)[0m
```
[dir] knowledge-absorber
[dir] knowledge-absorber/references
[dir] knowledge-absorber/scripts
[file] README.md
[file] README_EN.md
[file] knowledge-absorber/SKILL.md
[file] knowledge-absorber/requirements.txt
```

[35m主要语言: [0mPython

[35m关键文档内容[0m

[35m文件: README.md[0m
<div align="center">

# 📚 Knowledge Absorber (知识吸收器)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version: 4.0.0](https://img.shields.io/badge/Version-4.0.0-green.svg)](CHANGELOG.md)

**通用 AI 技能模块 | 适用于 Trae, Claude, Gemini, VS Code Copilot 等环境**

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

---

**Knowledge Absorber** 是一个独立的“外挂大脑”模块。它赋予 AI 助手深度阅读、解析长文档并生成结构化知识晶体（Markdown + HTML）的能力。

</div>

---

## 🚀更新

> 更新内容


- **修复报错**：修复MAC中pywin32 报错。
- **⚛️ 深度裂变模块 (Deep Fission)**：新增原子级矛盾分析与版本考据模块，用于揭示颠覆常识的结论（样式：`.fission-section`）。
- **🔍 严格搜索内化 (Strict Filter)**：HTML 交互升级，搜索框现在会**严格隐藏**不匹配的内容块，而非仅高亮，提供专注阅读体验。
- **🛡️ Mermaid 安全协议**：内置语法自动修正机制，强制转义特殊字符，杜绝图表渲染崩溃。

---

## 支持功能

- 支持多链接/文件同步抓取。
- 实现具备高对比度色彩的实时状态追踪与彩色终端任务看板。
- 新增 `【💡 深度链接】` 分析，自动对比多源输入冲突，强化 AI 的事实校验能力。

## 📂 跨平台移植指南 (Portability Guide)

本模块设计为 **"文件夹级即插即用"**。
不同的 AI 助手通常会扫描项目根目录下的特定配置文件夹。为了让其他 AI (如 Claude 或 Gemini) 识别此技能，你只需要**修改父目录的名称**。

### 📂 目录结构适配

假设你把 `skills` 文件夹放在项目根目录：

1.  **在 Trae 中使用** (默认):

    ```text
    Project_Root/
    └── .trae/              <-- 保持原名
        └── skills/
            └── knowledge-absorber/
    ```

2.  **在 Claude Projects 中使用**:
    - 将 `.trae` 重命名为 `.claude`。

    ```text
    Project_Root/
    └── .claude/            <-- 重命名为 .claude
        └── skills/
            └── knowledge-absorber/
    ```

3.  **在 Gemini Advanced / AI Studio 中使用**:
    - 将 `.trae` 重命名为 `.gemini`。

    ```text
    Project_Root/
    └── .gemini/            <-- 重命名为 .gemini
        └── skills/
            └── knowledge-absorber/
    ```

4.  **在 VS Code (Copilot/Cline) 中使用**:
    - 将 `.trae` 重命名为 `.vscode`。
    ```text
    Project_Root/
    └── .vscode/            <-- 重命名为 .vscode
        └── skills/
            └── knowledge-absorber/
    ```

> **💡 核心原理**：AI 助手通常有权限读取隐藏文件夹（以 `.` 开头）。只要路径正确，并明确指示 AI “使用这个技能”，它就能工作。

---

## 🛠️ 安装与使用 (Installation & Usage)

### 第一步：环境准备

确保你的电脑安装了 Python 3.8+。
在 `knowledge-absorber` 目录下运行：

```bash
pip install -r requirements.txt
```

### 第二步：何时调用 (When to Activate)

不要为简单的 Google 搜索使用此技能。请在以下“高认知负载”场景召唤它：

1.  **啃大部头**：当你面对数百页的 PDF、技术框架文档（如 BMad, React 源码）或古籍时。
2.  **需要知识晶体**：当你不仅要一个简单的总结，而是要生成可永久存档、排版精美的 HTML 卡片时。
3.  **多源交叉分析**：当需要同时对比抓取多个不同平台的链接（如知乎 + 博客 + 官方文档）进行深度真理锚定时。

### 第三步：调用机制 (Workflow)

你不需要手动运行复杂的命令行，只需在对话中**自然指令**，AI 会自动代理执行：

- **用户指令示例**：

  > “帮我深度解析这个链接：`https://docs.bmad-method.org/`”
  > “读取 `manual.pdf` 并按【机械透镜】拆解生成知识卡片。”

- **AI 的执行逻辑**：
  1.  **摄取**：并发调用 `scripts/content_ingester.py` 抓取并清洗内容。
  2.  **透镜分析**：根据 `SKILL.md` 中的协议（如机械透镜、意义透镜）进行深度推理。
  3.  **交付**：自动生成 `.md`（深度笔记）和 `.html`（可视化卡片）文件。

---

## 📦 产出物 (Outputs)

该技能会自动生成两种格式的文件（位于 `data/` 目录）：

1.  **Markdown 深度笔记 (`.md`)**：
    - 包含元数据、核心概念破冰、深度拆解、思维导图、避坑指南。
    - 支持“双文异构”（古文繁体/解释简体）或“技术栈模版”。
2.  **HTML 可视化卡片 (`.html`)**：
    - 精美的排版，适合分享或作为知识库归档。
    - 支持深色/浅色模式适配，代码高亮与 Mermaid 导图完美显示。

---

## 🤖 技能协议 (Skill Protocol)

核心逻辑定义在 `SKILL.md` 文件中。
如果你想修改 AI 的思考方式（例如修改解析的深度、改变输出风格），请直接编辑 `SKILL.md`。

---

> **维护者**: Little Code Sauce
> **版本**: v4.0.0 (Mixed Script Edition)


------------------------------------------------------------


[35m文件: README_EN.md[0m
<div align="center">

# 📚 Knowledge Absorber

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version: 4.0.0](https://img.shields.io/badge/Version-4.0.0-green.svg)](CHANGELOG.md)

**Universal AI Skill Module | Compatible with Trae, Claude, Gemini, VS Code Copilot, etc.**

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

---

**Knowledge Absorber** is an independent "External Brain" module. It empowers AI agents with the ability to deeply read long documents, analyze complex content, and generate structured "Knowledge Crystals" (Markdown + HTML).

</div>

---

## 🚀 What's New

> **v4.0.0 "Mixed Script Edition"**

- **⚡ High-Speed Concurrent Engine**: Introduced `ThreadPoolExecutor` and `threading.Lock` for simultaneous scraping of multiple links/files, improving processing efficiency by 300%+.
- **🎨 Visual Progress System**: Integrated `Rich` library for high-contrast color tracking, providing a clear task board and real-time progress feedback in the terminal.
- **⚓ Truth Anchoring Protocol**: Added `【💡 Deep Linking】` analysis to automatically identify factual conflicts or complementarities across multiple sources.
- **🔍 Deep Protocol Alignment**: Mandatory integration of the "Seven Holographic Lenses" protocol, ensuring outputs include "Mind Maps" and "Pitfall Guides".
- **🛡️ Enhanced Robustness**: Optimized SSL verification for offline testing and added auto-fix for character encoding issues (Mojibake) on major platforms.
- **⚛️ Deep Fission Module**: Added atomic-level contradiction analysis and version archeology module to reveal counter-intuitive conclusions (Style: `.fission-section`).
- **🔍 Strict Search Filter**: Upgraded HTML interaction; search box now **strictly hides** non-matching content blocks instead of just highlighting, providing a focused reading experience.
- **🛡️ Mermaid Safety Protocol**: Built-in syntax auto-correction mechanism that forcibly escapes special characters to prevent diagram rendering crashes.

---

## 📂 Portability Guide

This module is designed for **"Folder-Level Plug & Play"**.
AI assistants typically scan specific configuration folders in the project root. To let other AIs (like Claude or Gemini) recognize this skill, you simply need to **rename the parent directory**.

### 📂 Directory Structure Adaptation

Assuming your `skills` folder is located at the project root:

1.  **For Trae** (Default):
    ```text
    Project_Root/
    └── .trae/              <-- Keep original name
        └── skills/
            └── knowledge-absorber/
    ```

2.  **For Claude Projects**:
    *   Rename `.trae` to `.claude`.
    ```text
    Project_Root/
    └── .claude/            <-- Rename to .claude
        └── skills/
            └── knowledge-absorber/
    ```

3.  **For Gemini Advanced / AI Studio**:
    *   Rename `.trae` to `.gemini`.
    ```text
    Project_Root/
    └── .gemini/            <-- Rename to .gemini
        └── skills/
            └── knowledge-absorber/
    ```

4.  **For VS Code (Copilot/Cline)**:
    *   Rename `.trae` to `.vscode`.
    ```text
    Project_Root/
    └── .vscode/            <-- Rename to .vscode
        └── skills/
            └── knowledge-absorber/
    ```

> **💡 Core Principle**: AI agents usually have permission to read hidden folders (starting with `.`). As long as the path is correct and you explicitly instruct the AI to "use this skill", it will work.

---

## 🛠️ Installation & Usage

### Step 1: Environment Preparation
Ensure Python 3.8+ is installed on your machine.
Run the following command in the `knowledge-absorber` directory:
```bash
pip install -r requirements.txt
```

### Step 2: When to Activate
Do not use this skill for simple Google searches. Summon it for **"High Cognitive Load"** scenarios:

1.  **Heavy Lifting**: When facing hundreds of pages of PDFs, technical framework docs (e.g., BMad, React Source), or ancient texts.
2.  **Knowledge Crystals Needed**: When you need more than a simple summary—you need a beautifully formatted, archivable HTML card.
3.  **Cross-Source Analysis**: When you need to scrape and compare multiple links (e.g., Zhihu + Blog + Official Docs) for deep Truth Anchoring.

### Step 3: Workflow
You don't need to manually run complex command-line instructions. Just use **Natural Language** in the chat, and the AI will proxy the execution:

*   **User Instruction Examples**:
    > "Help me deeply analyze this link: `https://docs.bmad-method.org/`"
    > "Read `manual.pdf` and apply the [Mechanistic Lens] to generate knowledge cards."

*   **AI Execution Logic**:
    1.  **Ingestion**: Automatically calls `scripts/content_ingester.py` to scrape and clean content concurrently.
    2.  **Lens Analysis**: Applies deep reasoning based on protocols defined in `SKILL.md` (e.g., Mechanistic Lens, Evolution Lens).
    3.  **Delivery**: Automatically generates `.md` (Deep Notes) and `.html` (Visual Cards).

---

## 📦 Outputs

This skill automatically generates files in two formats (located in the `data/` directory):

1.  **Markdown Deep Notes (`.md`)**:
    *   Includes metadata, concept icebreaking, deep deconstruction, mind maps, and pitfall guides.
    *   Supports "Mixed Script Protocol" (Traditional/Simplified) or "Tech Stack Templates".
2.  **HTML Visual Cards (`.html`)**:
    *   Beautiful formatting, perfect for sharing or archiving in a knowledge base.
    *   Supports Dark/Light mode adaptation, with perfected code highlighting and Mermaid diagram display.

---

## 🤖 Skill Protocol

The core logic is defined in the `SKILL.md` file.
If you want to modify the AI's way of thinking (e.g., changing the depth of analysis or output style), please edit `SKILL.md` directly.

---

> **Maintainer**: Little Code Sauce
> **Version**: v4.0.0 (Mixed Script Edition)


------------------------------------------------------------


[35m依赖项详情[0m

[35mrequirements.txt[0m
```
requests
beautifulsoup4
rapidocr_onnxruntime
pypdf
html2text
DrissionPage
python-docx
Pillow
opencv-python-headless
pywin32; sys_platform == 'win32'
tqdm
rich

```
