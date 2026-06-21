---
name: react-infinite-render-useeffect-spread
description: |
  Fix React infinite render loops caused by useEffect + object spread pattern.
  Use when: (1) Console shows "Maximum update depth exceeded" warning, (2) Page
  freezes or becomes unresponsive, (3) useEffect triggers on every render despite
  dependencies, (4) Parent component spreads large objects before passing to child.
  Common in form components, config panels, and nested component hierarchies with
  shared state.
author: Claude Code
version: 1.0.0
date: 2026-02-12
---

# React Infinite Render Loop: useEffect + Object Spread Pattern

## Problem
React components enter infinite render loops when useEffect dependencies trigger
on every render due to new object references created by spreading operations in
parent components.

## Context / Trigger Conditions
**Symptoms:**
- Console warning: "Maximum update depth exceeded"
- Page becomes unresponsive or freezes
- React DevTools shows component re-rendering continuously
- useEffect runs on every render despite having dependencies

**Common Pattern:**
```javascript
// Parent component
const handleSave = (values) => {
  setState({
    ...largeObject,  // ❌ Creates new reference every time
    ...values,
  });
};

// Child component
useEffect(() => {
  onSave(data);  // ❌ Triggers parent update
}, [onSave, data]);  // ❌ onSave or data changes every render
```

## Root Cause Analysis
The infinite loop forms through this chain:

1. Child's `useEffect` calls parent's callback
2. Parent spreads large object and updates state
3. New object reference causes child to re-render
4. Child's `useEffect` detects dependency change
5. Loop back to step 1

## Solution

### 1. Remove Auto-Triggering useEffect
Replace automatic effects with user-triggered callbacks:

```javascript
// ❌ Before: Auto-triggers on every change
useEffect(() => {
  onConfigChange({
    languages: values.languages,
  });
}, [onConfigChange, values.languages]);

// ✅ After: Only triggers on user action
<Select
  onChange={(value) => {
    field.onChange(value);
    onConfigChange({ languages: value });
  }}
/>
```

### 2. Simplify Data Passing
Only pass changed values, not entire objects:

```javascript
// ❌ Before: Spreads entire object (20+ fields)
const handleSave = (values) => {
  onConfigChange({
    ...speechData,  // Unnecessary spread
    ...values,
  });
};

// ✅ After: Pass only changed values
const handleSave = (values) => {
  onConfigChange(values);  // Parent merges
};
```

### 3. Use useCallback for Stable References
Memoize callbacks to prevent new function references:

```javascript
// ❌ Before: New function on every render
const handleSave = (values) => {
  setSpeechConfig({
    ...speechConfig,  // Depends on current state
    ...values,
  });
};

// ✅ After: Stable reference with functional update
const handleSave = useCallback((values) => {
  setSpeechConfig(prev => ({
    ...prev,
    ...values,
  }));
}, []);  // No dependencies needed
```

### 4. Use Functional State Updates
Avoid state dependencies in callbacks:

```javascript
// ❌ Before: Depends on speechConfig
setSpeechConfig({
  ...speechConfig,
  ...values,
});

// ✅ After: Uses previous state
setSpeechConfig(prev => ({
  ...prev,
  ...values,
}));
```

## Verification Steps

1. **Check Console**: No "Maximum update depth" warnings
2. **Monitor Re-renders**: Use React DevTools Profiler
3. **Test Interactions**: Verify UI updates work correctly
4. **Check Dependencies**: Run ESLint exhaustive-deps rule

## Complete Example

**Before (Infinite Loop):**
```javascript
// Parent
const [config, setConfig] = useState(initialConfig);

const handleSave = (values) => {
  setConfig({
    ...config,  // ❌ New reference
    ...values,
  });
};

// Child
useEffect(() => {
  onSave({ field: value });  // ❌ Auto-triggers
}, [onSave, value]);
```

**After (Fixed):**
```javascript
// Parent
const [config, setConfig] = useState(initialConfig);

const handleSave = useCallback((values) => {
  setConfig(prev => ({  // ✅ Functional update
    ...prev,
    ...values,
  }));
}, []);  // ✅ Stable reference

// Child - removed useEffect, use direct callback
<Input
  onChange={(value) => {
    field.onChange(value);
    onSave({ field: value });  // ✅ User-triggered only
  }}
/>
```

## Notes

### When to Use Each Technique

- **Remove useEffect**: When updates should only happen on user actions
- **Simplify data passing**: When parent spreads large objects unnecessarily
- **useCallback**: When callbacks are passed as props to child components
- **Functional updates**: When new state depends on previous state

### Edge Cases

- **Multiple fields**: If child has multiple fields, batch updates or debounce
- **Validation**: Validate before calling parent callback to avoid invalid states
- **Initial mount**: Use `useEffect` with empty deps `[]` for mount-only logic

### Performance Considerations

- Object spreading is O(n) where n is number of properties
- Large objects (20+ fields) create significant overhead
- Consider using `useReducer` for complex state updates

## References

- [React Hooks: useCallback](https://react.dev/reference/react/useCallback)
- [React Hooks: useEffect](https://react.dev/reference/react/useEffect)
- [React State Updates](https://react.dev/learn/queueing-a-series-of-state-updates)
