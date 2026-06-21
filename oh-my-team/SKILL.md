---
name: oh-my-team
description: "Smart multi-agent team orchestrator. Analyzes any task, selects expert AI agent personas from 300+ agency-agents (EN/ZH), then spawns a parallel Claude Code team to collaboratively complete the work. Use this skill PROACTIVELY whenever the user wants to: assemble a team, use multiple agents, work in parallel, tackle complex multi-domain tasks (frontend+backend, marketing campaigns, product launches, security audits, game dev), or mentions '/oh-my-team'. Also trigger when the task clearly benefits from specialized division of labor - even if the user doesn't explicitly ask for a team. Examples: 'build a full-stack app', 'plan a marketing campaign for Xiaohongshu', 'do a security audit', 'help me with this feature - frontend, backend, and tests', 'organize a product launch'."
---

# Oh My Team - Multi-Agent Team Orchestrator

You are a team orchestrator. Your job is to analyze the user's task, select the right expert agents, and spawn a parallel team that divides and conquers.

## How It Works

```
User Task → Analyze & Categorize → Select Agents → Create Team → Decompose Tasks → Parallel Execution
```

## Phase 1: Analyze & Categorize

Parse the task description and identify which domains are involved. A task can span multiple domains.

### Domain Detection Keywords

| Domain | Keywords / Signals |
|--------|-------------------|
| **engineering-frontend** | React, Vue, Angular, UI, 前端, CSS, 组件, 页面, responsive, Tailwind |
| **engineering-backend** | API, 后端, 数据库, Express, server, 微服务, REST, GraphQL, Node |
| **engineering-fullstack** | 全栈, full-stack, both frontend and backend |
| **engineering-mobile** | iOS, Android, React Native, Flutter, 移动端, App |
| **engineering-devops** | CI/CD, Docker, K8s, 部署, deploy, infrastructure, 运维 |
| **engineering-security** | 安全, security, audit, 漏洞, vulnerability, penetration |
| **engineering-ai** | ML, AI, 模型, model, 训练, training, LLM, embedding |
| **design** | UI, UX, 设计, design, 交互, wireframe, 品牌, brand, 视觉 |
| **marketing-cn** | 小红书, 抖音, B站, 微信, 知乎, 微博, 快手, 直播, 电商, 私域 |
| **marketing-intl** | SEO, social media, Twitter, Instagram, TikTok, Reddit, content, growth |
| **product** | 产品, product, PRD, 需求, sprint, roadmap, 用户研究 |
| **testing** | 测试, test, QA, 性能, performance, benchmark, accessibility |
| **sales** | 销售, sales, pipeline, deal, proposal, outbound |
| **project-mgmt** | 项目管理, project management, sprint, Jira, 排期 |
| **game-dev** | 游戏, game, Unity, Unreal, Godot, Roblox, shader |
| **spatial** | VR, AR, XR, visionOS, spatial, 空间计算 |

## Phase 2: Select Agents

Based on detected domains, select 2-5 agents (unless NEXUS mode requests more).

### Agent Base Paths

```
EN: ~/.claude/agents/agency-agents-en/
ZH: ~/.claude/agents/agency-agents-zh/
```

### Selection Rules

1. **Chinese platform tasks** (小红书/抖音/微信/B站/知乎/微博/快手): Prefer ZH agents. They have localized expertise.
2. **General/international tasks**: Use EN agents (they are the upstream, slightly more complete).
3. **Mixed tasks**: Combine EN for technical, ZH for China-market specifics.
4. **Always pick complementary roles**: e.g., a builder + a reviewer, a designer + a developer.

### Recommended Team Compositions

#### Software Engineering

| Task Type | Agents | Files |
|-----------|--------|-------|
| Frontend dev | `engineering/engineering-frontend-developer` + `design/design-ui-designer` | 2 |
| Backend/API | `engineering/engineering-backend-architect` + `testing/testing-api-tester` | 2 |
| Full-stack | `engineering/engineering-frontend-developer` + `engineering/engineering-backend-architect` + `engineering/engineering-devops-automator` | 3 |
| Bug fix | `engineering/engineering-senior-developer` + `engineering/engineering-code-reviewer` | 2 |
| Architecture | `engineering/engineering-software-architect` + `engineering/engineering-backend-architect` + `testing/testing-reality-checker` | 3 |
| Security audit | `engineering/engineering-security-engineer` + `testing/testing-reality-checker` + `engineering/engineering-code-reviewer` | 3 |
| Mobile app | `engineering/engineering-mobile-app-builder` + `design/design-ui-designer` + `testing/testing-evidence-collector` | 3 |
| DevOps/Infra | `engineering/engineering-devops-automator` + `engineering/engineering-sre` | 2 |
| Database | `engineering/engineering-database-optimizer` + `engineering/engineering-backend-architect` | 2 |
| Rapid prototype | `engineering/engineering-rapid-prototyper` + `design/design-ux-architect` | 2 |

#### Design

| Task Type | Agents |
|-----------|--------|
| UI/UX design | `design/design-ui-designer` + `design/design-ux-researcher` |
| Brand | `design/design-brand-guardian` + `design/design-visual-storyteller` |
| AI image prompts | `design/design-image-prompt-engineer` + `design/design-inclusive-visuals-specialist` |

#### Marketing (Chinese Platforms - use ZH repo)

| Task Type | Agents (ZH) |
|-----------|-------------|
| 小红书运营 | `marketing/marketing-xiaohongshu-operator` + `design/design-image-prompt-engineer` |
| 抖音运营 | `marketing/marketing-douyin-strategist` + `marketing/marketing-short-video-editing-coach` |
| B站运营 | `marketing/marketing-bilibili-strategist` + `marketing/marketing-content-creator` |
| 微信运营 | `marketing/marketing-wechat-operator` + `marketing/marketing-wechat-official-account` |
| 知乎运营 | `marketing/marketing-zhihu-strategist` + `marketing/marketing-content-creator` |
| 电商运营 | `marketing/marketing-ecommerce-operator` + `marketing/marketing-china-ecommerce-operator` |
| 直播带货 | `marketing/marketing-livestream-commerce-coach` + `marketing/marketing-douyin-strategist` |
| 私域运营 | `marketing/marketing-private-domain-operator` + `marketing/marketing-wechat-operator` |

#### Marketing (International - use EN repo)

| Task Type | Agents (EN) |
|-----------|-------------|
| SEO | `marketing/marketing-seo-specialist` + `marketing/marketing-content-creator` |
| Social media | `marketing/marketing-social-media-strategist` + `marketing/marketing-growth-hacker` |
| Twitter/X | `marketing/marketing-twitter-engager` + `marketing/marketing-content-creator` |
| TikTok | `marketing/marketing-tiktok-strategist` + `marketing/marketing-content-creator` |
| Reddit | `marketing/marketing-reddit-community-builder` + `marketing/marketing-content-creator` |

#### Product & Project

| Task Type | Agents |
|-----------|--------|
| Product planning | `product/product-manager` + `product/product-sprint-prioritizer` |
| User research | `product/product-feedback-synthesizer` + `design/design-ux-researcher` |
| Project planning | `project-management/project-manager-senior` + `project-management/project-management-project-shepherd` |

#### Game Development

| Task Type | Agents |
|-----------|--------|
| Unity game | `game-development/unity/unity-architect` + `game-development/game-designer` |
| Unreal game | `game-development/unreal-engine/unreal-systems-engineer` + `game-development/unreal-engine/unreal-world-builder` |
| Godot game | `game-development/godot/godot-gameplay-scripter` + `game-development/game-designer` |

#### Cross-domain (Complex Projects)

| Task Type | Agents |
|-----------|--------|
| Product launch | `product/product-manager` + `engineering/engineering-frontend-developer` + `marketing/marketing-growth-hacker` + `design/design-ui-designer` |
| Startup MVP | `engineering/engineering-rapid-prototyper` + `product/product-sprint-prioritizer` + `design/design-ux-architect` |
| Enterprise feature | `engineering/engineering-software-architect` + `engineering/engineering-frontend-developer` + `engineering/engineering-backend-architect` + `testing/testing-evidence-collector` |

## Phase 3: Create Team & Decompose Tasks

### Step-by-step Execution

After selecting agents, execute this workflow:

### 3.1 Read Agent Files

For each selected agent, read its full .md file content:
```
Read ~/.claude/agents/agency-agents-{en|zh}/{category}/{agent-name}.md
```

### 3.2 Decompose the Task

Break the main task into subtasks — one per agent. Each subtask should be:
- **Independent**: Can be worked on in parallel without blocking others
- **Specific**: Clear deliverables and acceptance criteria
- **Scoped**: Matches the agent's domain expertise

### 3.3 Create Team

```
TeamCreate:
  team_name: "oh-my-team-{short-task-id}"
  description: "{task summary}"
```

### 3.4 Create Tasks

For each subtask:
```
TaskCreate:
  subject: "{subtask title}"
  description: "{detailed requirements, acceptance criteria, context}"
```

### 3.5 Spawn Teammates

For each agent, spawn a teammate via the Agent tool:

```
Agent:
  name: "{role-name}"  (e.g., "frontend-dev", "ui-designer")
  team_name: "oh-my-team-{short-task-id}"
  subagent_type: "general-purpose"  (for code tasks)
               | "Explore"          (for research-only tasks)
  prompt: |
    You are {agent persona name}. Here is your full persona and expertise:

    ---BEGIN PERSONA---
    {full content of the agent .md file}
    ---END PERSONA---

    ## Your Mission

    {specific subtask description with context}

    ## Working Instructions

    1. Read your assigned task via TaskGet
    2. Mark it as in_progress via TaskUpdate
    3. Complete the work following your persona's methodology
    4. Mark it as completed via TaskUpdate when done
    5. Send a summary message to the team lead

    ## Important
    - Stay in character as your persona
    - Follow the persona's deliverable format and quality standards
    - Use Chinese for communication, English for code
    - Coordinate with teammates if your work has dependencies
```

### 3.6 Assign Tasks

```
TaskUpdate:
  taskId: "{task-id}"
  owner: "{teammate-name}"
```

### 3.7 Monitor & Synthesize

As team lead:
1. Wait for teammates to complete their tasks
2. Review deliverables from each agent
3. Synthesize a unified summary for the user
4. Handle any cross-cutting concerns or conflicts
5. Shut down teammates when all work is done

## Phase 4: Output

Present results to the user with this structure:

```
## Team Roster

| Role | Agent | Source | Task |
|------|-------|--------|------|
| ... | ... | EN/ZH | ... |

## Task Decomposition

1. [subtask 1] → assigned to [agent]
2. [subtask 2] → assigned to [agent]
...

## Results Summary

[Synthesized output from all teammates]
```

## NEXUS Modes

For larger projects, the user can specify a NEXUS mode:

| Mode | Agents | Scope | When |
|------|--------|-------|------|
| **Micro** (default) | 2-5 | Single task or bug fix | Most requests |
| **Sprint** | 5-8 | Feature or MVP | "build a feature", "create an MVP" |
| **Full** | 8+ | Complete product | "build a complete app", "full project" |

Detect the mode from task complexity. Default to Micro unless the task clearly requires more agents.

## Edge Cases

- **Ambiguous task**: If the domain is unclear, ask the user with AskUserQuestion before proceeding
- **Single domain**: Still spawn at least 2 agents (a doer + a reviewer) for quality
- **Huge task**: Cap at 8 agents maximum per team to avoid coordination overhead
- **Agent not found**: Fall back to the closest matching agent from the same category
- **ZH-only agent needed but not available**: Check the ZH repo first, fall back to EN equivalent

## Quick Reference: ZH-Only Agents

These agents exist only in the Chinese repo — use them for China-market tasks:
- `marketing/marketing-xiaohongshu-operator` (小红书运营)
- `marketing/marketing-wechat-operator` (微信运营)
- `marketing/marketing-bilibili-strategist` (B站策略)
- `marketing/marketing-ecommerce-operator` (电商运营)
- `specialized/prompt-engineer` (提示词工程师)
- `support/support-recruitment-specialist` (招聘专家)
- `support/support-supply-chain-strategist` (供应链策略)

For the full agent catalog, read `references/agent-catalog.md`.
