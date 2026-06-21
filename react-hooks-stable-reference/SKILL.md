---
name: react-hooks-stable-reference
description: |
  Fix React Hook exhaustive-deps warnings when using default values like `value || []`
  or `value || {}` in dependency arrays. Use when: (1) oxlint/eslint reports "depends
  on X, which changes every render", (2) useMemo/useEffect/useCallback dependencies
  include variables created with `|| []` or `|| {}`, (3) hooks re-run on every render
  despite props not changing. Solution: wrap with useMemo to maintain stable reference.
author: Claude Code
version: 1.0.0
date: 2026-02-11
---

# React Hooks Stable Reference Pattern

## Problem

When using default values like `const items = props.items || []` in React components,
each render creates a new array/object reference. If this variable is used in a
`useMemo`, `useEffect`, or `useCallback` dependency array, the hook will re-run on
every render, defeating the purpose of memoization.

## Context / Trigger Conditions

**Exact error message from oxlint/eslint:**
```
React hook useMemo depends on `variableName`, which changes every render
```

**Code patterns that trigger this:**
```typescript
// ❌ Problem: Creates new array reference every render
const selectedItems = props.items || [];

const result = useMemo(() => {
  return selectedItems.map(item => transform(item));
}, [selectedItems]); // ⚠️ selectedItems changes every render
```

**When this occurs:**
- Using `|| []` or `|| {}` for default values
- Variable is used in dependency array of hooks
- Props/state value might be `null`, `undefined`, or falsy
- ESLint/oxlint exhaustive-deps rule is enabled

## Solution

### Option 1: Wrap with useMemo (Recommended)

```typescript
// ✅ Solution: Memoize the default value
const selectedItems = useMemo(() => props.items || [], [props.items]);

const result = useMemo(() => {
  return selectedItems.map(item => transform(item));
}, [selectedItems]); // ✓ selectedItems only changes when props.items changes
```

### Option 2: Use the prop directly in dependency array

```typescript
// ✅ Alternative: Skip intermediate variable
const result = useMemo(() => {
  const items = props.items || [];
  return items.map(item => transform(item));
}, [props.items]); // ✓ Depend on the prop directly
```

### Option 3: Use nullish coalescing with stable empty value

```typescript
// ✅ For module-level constants
const EMPTY_ARRAY: string[] = [];

function Component({ items }: Props) {
  const selectedItems = items ?? EMPTY_ARRAY;

  const result = useMemo(() => {
    return selectedItems.map(item => transform(item));
  }, [selectedItems]); // ✓ EMPTY_ARRAY is stable reference
}
```

## Verification

After applying the fix:

1. **ESLint/oxlint should not report warnings** for the dependency array
2. **Hook should not re-run unnecessarily**: Add a `console.log` inside the hook to verify it only runs when dependencies actually change
3. **Performance improvement**: Use React DevTools Profiler to confirm reduced re-renders

```typescript
const result = useMemo(() => {
  console.log('useMemo running'); // Should only log when props.items changes
  return selectedItems.map(item => transform(item));
}, [selectedItems]);
```

## Example: Real-world Fix

**Before (problematic code):**
```typescript
export const LanguageSelector = ({ value, onChange }: Props) => {
  const selectedLanguages = value || []; // ❌ New array every render

  const buttonText = useMemo(() => {
    if (selectedLanguages.length === 0) {
      return 'Select languages';
    }
    return selectedLanguages.join(', ');
  }, [selectedLanguages]); // ⚠️ Re-runs every render

  return <button>{buttonText}</button>;
};
```

**After (fixed code):**
```typescript
export const LanguageSelector = ({ value, onChange }: Props) => {
  const selectedLanguages = useMemo(() => value || [], [value]); // ✅ Stable reference

  const buttonText = useMemo(() => {
    if (selectedLanguages.length === 0) {
      return 'Select languages';
    }
    return selectedLanguages.join(', ');
  }, [selectedLanguages]); // ✓ Only re-runs when value changes

  return <button>{buttonText}</button>;
};
```

## Notes

### Why This Happens

JavaScript creates a new array/object reference with each `|| []` or `|| {}` evaluation:

```javascript
[] === []  // false - different references
{} === {}  // false - different references
```

React's dependency comparison uses `Object.is()`, which checks reference equality.
Even though the arrays/objects are "empty" and logically equivalent, they're
different references, causing hooks to re-run.

### Performance Impact

- **Minor impact**: For simple components, the performance difference is negligible
- **Significant impact**: For expensive computations, large lists, or deeply nested
  components, unnecessary re-runs can cause noticeable lag
- **Best practice**: Fix these warnings to maintain predictable performance as the
  app grows

### Related Patterns

This same issue applies to:
- Object literals: `const config = props.config || {}`
- Function references: `const handler = props.onEvent || (() => {})`
- Computed values: `const items = props.items || getDefaultItems()`

### TypeScript Considerations

When using TypeScript, prefer nullish coalescing (`??`) over logical OR (`||`) to
avoid treating `0`, `''`, or `false` as missing values:

```typescript
// ❌ Treats 0 as missing
const count = props.count || 10; // count=0 becomes 10

// ✅ Only treats null/undefined as missing
const count = props.count ?? 10; // count=0 stays 0
```

## References

- [React Hooks API Reference: useMemo](https://react.dev/reference/react/useMemo)
- [React Hooks FAQ: Performance Optimizations](https://react.dev/learn/react-compiler#what-does-the-compiler-assume)
- [ESLint Plugin React Hooks: exhaustive-deps](https://github.com/facebook/react/tree/main/packages/eslint-plugin-react-hooks)
