---
name: async-integration-tests
description: "Run integration tests in background without blocking. Graph: → TriggerTests ⚡ (async, non-blocking)"
category: testing
complexity: simple
mcp-servers: [playwright]
personas: [qa-specialist]
---

# /async-integration-tests - Async Integration Testing

> **Workflow Description**: Trigger long-running integration tests in background while continuing work

**Detected Patterns**: async

## Workflow Graph

```
⚡ RunIntegrationTests [async_1] (non-blocking)
  → Fire and continue working
  → Results available when complete
```

## Behavioral Flow

1. **Trigger Async Tests** (non-blocking)
   - Start integration test suite in background
   - Return immediately (don't wait for completion)
   - Tests run independently

2. **Continue Working**
   - User can continue other tasks
   - Tests execute in parallel with main work

3. **Check Results Later**
   - Results available when tests complete
   - Notification on completion

## MCP Integration

- **playwright MCP**: Browser-based integration test execution

## Usage Examples

```bash
/async-integration-tests

# Tests start immediately, command returns
# Continue coding while tests run (~10-15 minutes)
# Check results when convenient
```

## Boundaries

**Will:**
- Execute tests in background
- Allow continued work during execution
- Notify when tests complete

**Will Not:**
- Block user from continuing work
- Wait for test completion
- Interrupt ongoing tasks
