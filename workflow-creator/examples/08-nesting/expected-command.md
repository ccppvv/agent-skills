---
name: microservices-cicd
description: "Execute CI/CD for each microservice with nested workflows. Graph: → ForEach[Service] └→ CI/CD[Build→Test→Deploy]"
category: orchestration
complexity: complex
mcp-servers: [sequential, playwright, serena]
personas: [devops-architect, system-architect, backend-architect, qa-specialist]
---

# /microservices-cicd - Microservices CI/CD Orchestration

> **Workflow Description**: Execute complete CI/CD pipeline for each microservice with nested build-test-deploy workflows

**Detected Patterns**: nesting, batch

## Workflow Graph

```
→ DiscoverMicroservices [nest_1]
→ ForEachMicroservice [nest_2]
  └→ ExecuteCI/CD [nest_2_sub]
      → Build [nest_2_sub_1]
        - Compile code
        - Create Docker image
      → Test [nest_2_sub_2]
        - Unit tests
        - Integration tests
      → Deploy [nest_2_sub_3]
        - Deploy to staging
        - Verify health
        - Deploy to production
```

## Behavioral Flow

1. **Discover Microservices**
   - Scan repository for microservice definitions
   - Identify services requiring deployment
   - Determine deployment order based on dependencies

2. **For Each Microservice** (sequential or parallel based on dependencies)
   - Execute nested CI/CD workflow:

     a. **Build Phase**
        - Compile service code
        - Run linter and type checker
        - Build Docker image
        - Tag with version

     b. **Test Phase**
        - Run unit tests
        - Run integration tests
        - Verify test coverage thresholds

     c. **Deploy Phase**
        - Deploy to staging environment
        - Run health checks
        - If healthy: Deploy to production
        - If unhealthy: Rollback and alert

3. **Aggregate Results**
   - Collect status from all microservices
   - Report overall deployment status
   - Generate deployment summary

## MCP Integration

- **sequential MCP**: Complex nested workflow orchestration
- **playwright MCP**: Automated testing and health verification
- **serena MCP**: Code building and deployment operations

## Usage Examples

```bash
/microservices-cicd

# Discovers all microservices (e.g., 5 services)
# For each service: Build → Test → Deploy
# Total: 15 sub-workflows (3 per service)
# Handles dependencies and ordering automatically
```

## Boundaries

**Will:**
- Execute complete CI/CD for each microservice
- Handle inter-service dependencies
- Rollback individual services on failure
- Provide detailed per-service status

**Will Not:**
- Deploy services with failing tests
- Ignore service dependencies
- Proceed if critical service fails
- Skip health verification
