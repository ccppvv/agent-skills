---
name: dependency-update-flow
description: "Sequential dependency update pipeline. Graph: → UpdateDeps → Test → Build → Publish"
category: workflow
complexity: standard
mcp-servers: []
personas: [backend-developer]
---

# /dependency-update-flow - Dependency Update Pipeline

> **Workflow Description**: Sequential flow for updating, testing, building, and publishing package

**Detected Patterns**: flow

## Workflow Graph

```
→ UpdateDependencies [flow_1]
→ RunTests [flow_2]
→ BuildPackage [flow_3]
→ PublishToNpm [flow_4]
```

## Behavioral Flow

1. **Update Dependencies**
   - Update package.json dependencies to latest versions
   - Run npm/yarn update

2. **Run Tests**
   - Execute full test suite
   - Ensure no breaking changes

3. **Build Package**
   - Compile TypeScript/Bundle code
   - Generate distribution files

4. **Publish to NPM**
   - Bump version number
   - Publish to npm registry
   - Create git tag

## Usage Examples

```bash
/dependency-update-flow

# Complete pipeline: update → test → build → publish
```

## Boundaries

**Will:**
- Execute each step in strict sequence
- Halt on any step failure
- Create version tag on success

**Will Not:**
- Skip testing phase
- Publish without successful build
- Continue if tests fail
