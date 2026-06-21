---
name: tdd-integration-test-side-effects
description: |
  Fix integration tests that pass when they shouldn't by checking side effects
  instead of return values. Use when: (1) TDD RED phase test passes immediately,
  (2) testing code that only has placeholder implementation, (3) integration test
  needs to verify actual behavior not just API calls. Applies to any language
  where functions may succeed without doing real work.
author: Claude Code
version: 1.0.0
date: 2026-02-22
---

# TDD Integration Testing - Side Effect Validation

## Problem

During TDD RED phase, integration tests pass immediately even though the
implementation is just a placeholder (e.g., `println!("TODO")` or `return Ok(())`).
This violates TDD principles because you never saw the test fail, so you don't
know if it's testing the right thing.

## Context / Trigger Conditions

Use this pattern when:
- Writing integration tests for CLI tools, file operations, or system interactions
- Test passes in RED phase when it should fail
- Implementation is a placeholder that returns success without doing work
- Testing code that has side effects (creates files, modifies state, calls external systems)

**Example scenario**: Testing a CLI command that should create a session directory:
```rust
// Weak assertion - always passes
let result = cli.execute().await;
assert!(result.is_ok() || result.is_err()); // This is useless!
```

## Solution

**Instead of checking return values, verify side effects:**

1. **Identify the expected side effect**
   - File/directory creation
   - Database records
   - Log entries
   - State changes
   - External API calls

2. **Assert on the side effect directly**
   ```rust
   // Strong assertion - checks actual behavior
   let result = cli.execute().await;
   assert!(result.is_ok(), "Execute should succeed");

   // Verify the side effect
   let sessions_dir = cache_dir.path().join("sessions");
   assert!(sessions_dir.exists(), "Sessions directory should be created");
   ```

3. **Verify the test fails in RED phase**
   - Run test before implementation
   - Confirm it fails with the expected error message
   - If it passes, strengthen the assertion

## Verification

After applying this pattern:
1. Test should fail in RED phase with clear error message
2. Test should pass in GREEN phase after implementation
3. Error message should indicate what side effect is missing

**Example failure message**:
```
thread 'test_execute_creates_session' panicked at tests/integration_test.rs:25:5:
Sessions directory should be created
```

## Example

**Before (weak test)**:
```rust
#[tokio::test]
async fn test_execute_with_instruction() {
    let cli = Cli::parse_from(&["app", "test"]);
    let result = cli.execute().await;
    // This passes even with placeholder implementation!
    assert!(result.is_ok() || result.is_err());
}
```

**After (strong test)**:
```rust
#[tokio::test]
async fn test_execute_with_instruction() {
    let cache_dir = tempdir().unwrap();
    let cli = Cli::parse_from(&[
        "app",
        "--cache-dir", cache_dir.path().to_str().unwrap(),
        "test"
    ]);

    let result = cli.execute().await;
    assert!(result.is_ok(), "Execute should succeed");

    // Verify side effects
    let sessions_dir = cache_dir.path().join("sessions");
    assert!(sessions_dir.exists(), "Sessions directory should be created");

    // Can also check file contents, counts, etc.
    let session_files: Vec<_> = std::fs::read_dir(&sessions_dir)
        .unwrap()
        .collect();
    assert!(!session_files.is_empty(), "Should create at least one session file");
}
```

## Common Side Effects to Test

| Operation Type | Side Effect to Verify |
|----------------|----------------------|
| File operations | File exists, content matches, permissions correct |
| Database | Record exists, fields have expected values |
| CLI output | stdout/stderr contains expected text |
| State changes | Object state updated, cache invalidated |
| External calls | Mock was called with correct parameters |
| Async operations | Callback executed, promise resolved |

## Notes

- **Isolation**: Use temporary directories (tempfile crate in Rust) to avoid test pollution
- **Cleanup**: Tests should clean up side effects or use isolated environments
- **Timing**: For async operations, may need to wait for side effects to complete
- **Mocking**: Sometimes checking mock call counts is appropriate, but prefer real side effects when possible
- **Error cases**: Also test that side effects DON'T happen when they shouldn't

## Anti-Patterns

❌ **Don't do this**:
```rust
// Too weak - accepts any result
assert!(result.is_ok() || result.is_err());

// Only checks API contract, not behavior
assert!(result.is_ok());

// Checks mock instead of real behavior
assert!(mock.was_called());
```

✅ **Do this**:
```rust
// Checks actual side effect
assert!(file_exists(&expected_path));

// Verifies content, not just existence
let content = read_file(&path);
assert_eq!(content, expected_content);

// Checks observable state change
assert_eq!(system.get_state(), ExpectedState::Active);
```

## References

- [Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) - Kent Beck
- [Growing Object-Oriented Software, Guided by Tests](https://www.amazon.com/Growing-Object-Oriented-Software-Guided-Tests/dp/0321503627) - Freeman & Pryce
- [Rust Testing Documentation](https://doc.rust-lang.org/book/ch11-00-testing.html)
