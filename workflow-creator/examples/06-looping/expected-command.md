---
name: deploy-with-retry
description: "Deploy with automatic retry on health check failure. Graph: → Deploy → ↻ HealthCheck (retry 3x)"
category: deployment
complexity: standard
mcp-servers: [sequential, playwright]
personas: [devops-architect, qa-specialist]
---

# /deploy-with-retry - Deployment with Retry Logic

> **Workflow Description**: Deploy to production with automatic retry on transient health check failures

**Detected Patterns**: looping

## Workflow Graph

```
→ DeployToProduction [loop_1]
  ↻ HealthCheck [loop_2]
    Condition: Retry up to 3 times if unhealthy
    Wait: 5 seconds between attempts
    ├─ [Healthy] → Success [branch_1]
    └─ [AllRetriesFailed] → Rollback [branch_2]
```

## Behavioral Flow

1. **Deploy to Production**
   - Deploy application to production environment
   - Wait for deployment to stabilize (30 seconds)

2. **Health Check with Retry** (loop)
   - Check application health endpoint
   - If unhealthy:
     - Wait 5 seconds
     - Retry (up to 3 total attempts)
   - If healthy: Proceed to success
   - If all retries fail: Trigger rollback

3. **Handle Result**
   - Success: Complete deployment
   - Failure: Automatic rollback to previous version

## MCP Integration

- **sequential MCP**: Retry logic coordination
- **playwright MCP**: Automated health check verification

## Usage Examples

```bash
/deploy-with-retry

# Deploys and verifies with automatic retry
# Handles transient failures gracefully
# Rolls back if consistently unhealthy
```

## Boundaries

**Will:**
- Retry health checks on transient failures
- Wait between retry attempts
- Rollback on persistent failures

**Will Not:**
- Retry indefinitely
- Proceed with unhealthy deployment
- Skip health verification
