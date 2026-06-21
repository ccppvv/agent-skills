# Safety Guardrails

## NEVER Operations

These operations are ABSOLUTELY FORBIDDEN and must never be executed:

### File System Safety
- ❌ Delete memory files (`.claude/memories/*`)
- ❌ Delete Claude configuration (`.claude/*` except temporary files)
- ❌ Delete system critical directories (`/etc`, `/System`, `C:\Windows`, `/usr/bin`)
- ❌ Modify system PATH or environment variables permanently
- ❌ Execute `rm -rf /` or equivalents
- ❌ Modify boot configurations

### Data Safety
- ❌ Delete databases without explicit backup confirmation
- ❌ Truncate production tables
- ❌ Modify password/credential files (`.env`, `credentials.json`, `secrets.*`)
- ❌ Expose API keys or tokens in logs/outputs

### Code Safety
- ❌ Execute unverified remote code
- ❌ Install packages from untrusted sources
- ❌ Disable security features (CSRF protection, authentication, etc.)
- ❌ Commit secrets to version control

### Network Safety
- ❌ Automated mass requests (DDoS patterns)
- ❌ Unauthorized penetration testing
- ❌ Modify firewall rules without review

## ALWAYS Confirm Operations

These operations require explicit user confirmation BEFORE execution:

### High-Risk File Operations
- ⚠️ Delete >5 files in one operation
- ⚠️ Modify >10 files simultaneously
- ⚠️ Change file permissions recursively
- ⚠️ Move critical project files

### Database Operations
- ⚠️ CREATE/DROP/ALTER database/table
- ⚠️ DELETE with WHERE clause (requires review)
- ⚠️ UPDATE affecting >100 rows
- ⚠️ Any production database operation

### Git Operations
- ⚠️ `git push --force` to any branch
- ⚠️ `git push --force-with-lease` to main/master
- ⚠️ Delete remote branches
- ⚠️ Rewrite public history
- ⚠️ Merge without review on main/master

### External API Calls
- ⚠️ POST/PUT/DELETE requests to external APIs
- ⚠️ Payment processing operations
- ⚠️ User data modification via API
- ⚠️ Bulk operations via API

### Deployment Operations
- ⚠️ Deploy to production
- ⚠️ Modify production configuration
- ⚠️ Restart production services
- ⚠️ Scale infrastructure resources

## Risk Level Classification

### 🟢 Low Risk (Auto-execute)
- Read file operations
- Search/grep operations
- Code analysis
- Documentation generation
- Test execution (non-production)
- Git status/log/diff
- Package installation (development)

### 🟡 Medium Risk (Show plan, one-click approve)
- Write/modify <5 files
- Git commit/push to feature branch
- Install production dependencies
- Configuration changes (development)
- Database queries (SELECT only)
- Create new files/directories

### 🔴 High Risk (Step-by-step confirmation)
- Operations in "ALWAYS Confirm" list
- Any operation affecting production
- Irreversible data operations
- Security-related changes
- Cross-service operations

## Pre-execution Checklist

Before executing any medium/high-risk operation:

```markdown
□ Operation not in NEVER list
□ Backup/rollback plan exists
□ Impact scope assessed
□ User explicitly authorized
□ Critical data backed up (if applicable)
□ Dry-run performed (if applicable)
□ Dependencies verified
□ Side effects understood
```

## Error Handling Rules

When encountering errors during execution:

1. **STOP immediately** - Don't continue to next step
2. **Report error context** - What was being attempted
3. **Preserve state** - Don't modify files further
4. **Request guidance** - Ask user how to proceed
5. **Document in memory** - Record error for learning

## Rollback Procedures

For each operation type, maintain rollback capability:

- **File changes**: Git commit before modifications
- **Database**: Backup before ALTER/DROP
- **Configuration**: Store previous values
- **Deployment**: Keep previous version accessible
- **Infrastructure**: Document state before changes
