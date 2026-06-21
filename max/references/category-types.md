# Category Types Reference

Detailed descriptions and usage guidelines for each information category type.

## Core Categories

### 核心发现 (Core Discoveries)
**When to use**: Important discoveries and insights during analysis

**Examples**:
- "Identified performance bottleneck in data processing pipeline at transform.js:234"
- "Discovered undocumented API behavior: rate limit resets at midnight UTC"
- "Found circular dependency between UserService and AuthService"

**Best practices**:
- Focus on non-obvious findings
- Include specific locations (file:line)
- Explain impact or significance

### 技术决策 (Technical Decisions)
**When to use**: Confirmed technical solutions and architecture choices

**Examples**:
- "Adopt Redis for session storage instead of in-memory cache"
- "Use WebSocket for real-time updates, fallback to polling for older browsers"
- "Implement JWT authentication with 15-minute access tokens and 7-day refresh tokens"

**Best practices**:
- State the decision clearly
- Include rationale when non-obvious
- Note any trade-offs considered

### 问题分析 (Problem Analysis)
**When to use**: Root cause, impact scope, and severity assessment

**Examples**:
- "Memory leak caused by event listeners not being cleaned up in useEffect"
- "Race condition in payment processing affects 2% of transactions during peak hours"
- "Database connection pool exhaustion under load > 1000 concurrent users"

**Best practices**:
- Identify root cause, not just symptoms
- Quantify impact when possible
- Assess severity/priority

## Solution Categories

### 解决方案 (Solutions)
**When to use**: Specific fix solutions and implementation steps

**Examples**:
- "Add cleanup function in useEffect to remove event listeners on unmount"
- "Implement optimistic locking with version field in payment records"
- "Increase connection pool size to 50 and add connection timeout of 30s"

**Best practices**:
- Be specific and actionable
- Include implementation details
- Reference related code locations

### 风险提示 (Risk Alerts)
**When to use**: Potential risks, precautions, and boundary conditions

**Examples**:
- "Migration requires downtime, schedule during low-traffic window"
- "New caching layer may cause stale data issues, implement cache invalidation strategy"
- "Breaking API change affects mobile app versions < 2.0, coordinate release"

**Best practices**:
- Identify potential issues proactively
- Suggest mitigation strategies
- Note dependencies and constraints

## Progress Categories

### 状态更新 (Status Updates)
**When to use**: Task progress, completion status, and next steps

**Examples**:
- "Completed authentication module (3/5 user stories), starting authorization next"
- "All unit tests passing, integration tests reveal CORS issue"
- "Database migration successful, pending QA verification"

**Best practices**:
- Provide clear progress indicators
- Note blockers or issues
- Outline next steps

### 依赖关系 (Dependencies)
**When to use**: Component dependencies, call relationships, and data flows

**Examples**:
- "UserController depends on AuthService, EmailService, and UserRepository"
- "Payment flow: Cart → OrderService → PaymentGateway → InventoryService"
- "Frontend requires API v2 endpoints, backend still on v1"

**Best practices**:
- Map critical dependencies
- Identify potential coupling issues
- Note version requirements

## Performance Categories

### 性能指标 (Performance Metrics)
**When to use**: Performance data, benchmarks, and optimization effects

**Examples**:
- "Page load time reduced from 3.2s to 1.1s after image optimization"
- "API response time: p50=120ms, p95=450ms, p99=1200ms"
- "Memory usage decreased 40% after implementing object pooling"

**Best practices**:
- Include baseline and target metrics
- Use percentiles for latency
- Quantify improvements

## Category Selection Guidelines

**Multiple categories**: Use multiple `<info>` tags when information spans categories
```xml
<info category="问题分析">Database queries causing 5s page load</info>
<info category="解决方案">Add indexes on user_id and created_at columns</info>
<info category="性能指标">Expected improvement: 5s → 500ms based on query analysis</info>
```

**Category evolution**: Information may change categories across turns
- Turn 1: `<info category="核心发现">Slow query identified</info>`
- Turn 2: `<info category="问题分析">Query missing index on join column</info>`
- Turn 3: `<info category="解决方案">Added composite index (user_id, created_at)</info>`
- Turn 4: `<info category="性能指标">Query time reduced from 5s to 50ms</info>`

**Obsolete information**: Drop `<info>` tags when:
- Problem fully resolved
- Decision superseded by new approach
- Information no longer relevant to current task
