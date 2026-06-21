---
name: react-dropdown-persist-on-parent-recreation
description: |
  Fix React dropdown/modal closing when parent component recreates child instance
  after internal state changes. Use when: (1) Dropdown closes after clicking internal
  Radio/Select/Button, (2) onChange triggers parent update that recreates component,
  (3) useState and useRef both reset unexpectedly, (4) stopPropagation doesn't help.
  Solves component remount (not re-render) state persistence using module-level variables.
author: Claude Code
version: 1.0.0
date: 2026-02-24
---

# React Dropdown Persist on Parent Recreation

## Problem

A dropdown or modal component closes unexpectedly when clicking internal controls (Radio,
Select, Button) because the parent component completely recreates the child component
instance after `onChange` is triggered, resetting all internal state.

## Context / Trigger Conditions

**Symptoms:**
- Dropdown/modal closes immediately after clicking internal controls
- `console.log` shows component is being re-instantiated (constructor/useState initializer runs again)
- Both `useState` and `useRef` values are reset
- `stopPropagation()` on click events doesn't prevent the closing

**Root Cause:**
Parent component recreates the child component instance (remount) rather than just
re-rendering it. This happens when:
- Parent doesn't use stable `key` prop
- Parent conditionally renders the component
- Parent's render logic creates new component instances

**Key Distinction:**
- **Re-render**: Component function runs again, but state persists
- **Remount**: Component is destroyed and recreated, all state is lost

## Solution

Use a module-level variable to persist state across component recreation:

```typescript
// Module-level variable (outside component)
let shouldKeepDropdownOpen = false;

const DropdownComponent = ({ onChange }) => {
  // Initialize state by checking the module-level flag
  const [isOpen, setIsOpen] = useState(() => {
    if (shouldKeepDropdownOpen) {
      console.log('Restoring open state from module flag');
      shouldKeepDropdownOpen = false; // Reset immediately
      return true;
    }
    return false;
  });

  // Wrap onChange to set flag before triggering parent update
  const handleChange = (value) => {
    console.log('Setting shouldKeepDropdownOpen flag');
    shouldKeepDropdownOpen = true;
    onChange(value); // This may cause parent to recreate this component
  };

  return (
    <Dropdown
      open={isOpen}
      onOpen={() => setIsOpen(true)}
      onClose={() => {
        // Check flag before closing
        if (shouldKeepDropdownOpen) {
          console.log('Preventing close due to flag');
          shouldKeepDropdownOpen = false;
          return; // Don't close
        }
        setIsOpen(false);
      }}
    >
      <InternalControls onChange={handleChange} />
    </Dropdown>
  );
};
```

### Why This Works

1. **Module-level scope**: Variable survives component destruction
2. **Lazy initialization**: `useState(() => ...)` runs only on mount, checks flag
3. **Immediate reset**: Flag is reset after use to avoid affecting future interactions
4. **Timing**: Flag is set before `onChange`, checked during new instance initialization

## Verification

Add logging to verify the solution:

```typescript
console.log('[Component] Rendered, isOpen:', isOpen, 'flag:', shouldKeepDropdownOpen);
```

You should see:
1. "Setting shouldKeepDropdownOpen flag" when clicking internal control
2. "Restoring open state from module flag" when component recreates
3. Dropdown remains open after interaction

## Failed Approaches (Why They Don't Work)

### 1. stopPropagation
```typescript
// ❌ Doesn't work - not an event bubbling issue
<Radio onClick={(e) => e.stopPropagation()} />
```
The problem isn't event bubbling; it's component recreation.

### 2. Controlled open state
```typescript
// ❌ Doesn't work - state resets on remount
const [isOpen, setIsOpen] = useState(false);
```
When component remounts, `useState` initializes with default value.

### 3. useRef
```typescript
// ❌ Doesn't work - ref also resets on remount
const shouldStayOpenRef = useRef(false);
```
`useRef` only persists across re-renders, not remounts. See [Understanding the Lifecycle of useRef](https://www.wavether.com/blog/2025/07/21/understanding-the-lifecycle-of-useref-in-react-and-avoiding-stale-reference-bugs/).

## Alternative Solutions

### Option 1: Fix Parent Component (Preferred)
Prevent parent from recreating child:

```typescript
// ✅ Use stable key
<DropdownComponent key="stable-key" />

// ✅ Lift state to parent
const [isOpen, setIsOpen] = useState(false);
<DropdownComponent isOpen={isOpen} onOpenChange={setIsOpen} />
```

### Option 2: Use Context/Global State
For complex scenarios, use React Context or state management library:

```typescript
const DropdownContext = createContext();
// Store open state in context that survives remounts
```

### When to Use Module-Level Variable
- Quick fix when you can't modify parent component
- Parent component is in third-party library
- Refactoring parent would be too complex
- Temporary workaround during migration

## Notes

**Caveats:**
- Module-level variables are shared across all instances of the component
- Not suitable if multiple instances need independent state
- Can cause issues in SSR (server-side rendering) - reset on server
- Consider this a tactical solution, not architectural best practice

**Best Practices:**
- Add clear comments explaining why module-level variable is needed
- Use descriptive variable names (e.g., `shouldKeepDropdownOpen` not `flag`)
- Reset flag immediately after use to avoid side effects
- Consider refactoring to lift state up when possible

**Edge Cases:**
- Multiple dropdowns on same page: Use instance-specific identifiers
- Concurrent mode: Module variables are synchronous, should work fine
- Hot module replacement: Variable resets on HMR, which is acceptable

## Example: Complete Implementation

```typescript
// VoiceSelector.tsx
import { useState } from 'react';
import { Dropdown } from '@tencent/tea-component';

// Module-level persistence
let shouldKeepDropdownOpen = false;

export const VoiceSelector = ({ voiceType, customTTSConfig, onChange }) => {
  const [isOpen, setIsOpen] = useState(() => {
    if (shouldKeepDropdownOpen) {
      shouldKeepDropdownOpen = false;
      return true;
    }
    return false;
  });

  const handleChange = (value) => {
    shouldKeepDropdownOpen = true;
    onChange(value); // Parent may recreate this component
  };

  return (
    <Dropdown
      open={isOpen}
      onOpen={() => setIsOpen(true)}
      onClose={() => {
        if (shouldKeepDropdownOpen) {
          shouldKeepDropdownOpen = false;
          return;
        }
        setIsOpen(false);
      }}
      clickClose={false}
    >
      <VoiceConfigPanel
        voiceType={voiceType}
        customTTSConfig={customTTSConfig}
        onChange={handleChange}
      />
    </Dropdown>
  );
};
```

## References

- [How to keep React component state between mount/unmount?](https://stackoverflow.com/questions/31352261/how-to-keep-react-component-state-between-mount-unmount)
- [React keep state alive for remount](https://stackoverflow.com/questions/71172898/react-keep-state-alive-for-remount)
- [Understanding the Lifecycle of useRef in React and Avoiding Stale Reference Bugs](https://www.wavether.com/blog/2025/07/21/understanding-the-lifecycle-of-useref-in-react-and-avoiding-stale-reference-bugs/)
- [React Lifecycle](https://www.geeksforgeeks.org/reactjs-lifecycle-components/)
