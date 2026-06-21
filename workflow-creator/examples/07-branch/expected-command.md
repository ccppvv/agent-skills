---
name: test-and-deploy
description: "Conditional deployment based on test results. Graph: → Test ├─ [Pass] → Deploy └─ [Fail] → Notify"
category: deployment
complexity: standard
mcp-servers: [playwright]
personas: [devops-architect, qa-specialist]
---

# /test-and-deploy - Test-Gated Deployment

> **Workflow Description**: Deploy to staging only if tests pass, otherwise send failure notification

**Detected Patterns**: branch

## Workflow Graph

```
→ RunTests [branch_1]
  ├─ [Pass] → DeployStaging [branch_2a]
  │  → VerifyDeployment [branch_2a1]
  └─ [Fail] → SendFailureNotification [branch_2b]
     → AbortDeployment [branch_2b1]
```

## Behavioral Flow

1. **Run Tests**
   - Execute complete test suite
   - Collect test results and coverage

2. **Conditional Branch**
   - **If tests pass**:
     - Deploy to staging environment
     - Verify deployment health
     - Report success
   - **If tests fail**:
     - Send failure notification with details
     - Abort deployment process
     - Report specific test failures

## MCP Integration

- **playwright MCP**: Automated testing and deployment verification

## Usage Examples

```bash
/test-and-deploy

# Safe deployment: only deploys if tests pass
# Automatic notification on failure
```

## Boundaries

**Will:**
- Execute all tests before deployment decision
- Deploy only on complete test pass
- Send detailed failure notifications

**Will Not:**
- Deploy with failing tests
- Skip test execution
- Proceed without verification
