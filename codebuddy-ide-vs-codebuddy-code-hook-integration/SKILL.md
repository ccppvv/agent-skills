---
name: codebuddy-ide-vs-codebuddy-code-hook-integration
description: |
  Diagnose cases where a project reacts to CodeBuddy Code sessions but not to CodeBuddy IDE activity.
  Use when: (1) `~/.codebuddy/settings.json` already contains hooks, (2) CodeBuddy Code / CLI events work,
  but opening or using CodeBuddy IDE alone does not trigger state changes, (3) the codebase posts status via
  hook scripts to a local HTTP endpoint, and (4) you need to distinguish CLI hook integration from IDE-native events.
  Covers the common root cause where `.codebuddy/settings.json` config applies to CodeBuddy Code/CLI, not IDE work status.
version: 1.0.0
author: Claude Code
date: 2026-04-01
---

# CodeBuddy IDE vs CodeBuddy Code Hook Integration

## Problem
A desktop companion, status widget, or automation reacts correctly to `CodeBuddy Code` sessions, but does nothing when only `CodeBuddy IDE` is open or actively being used.

## Context / Trigger Conditions
Use this skill when all or most of the following are true:

- The project registers hooks into `~/.codebuddy/settings.json`
- Runtime status changes are driven by hook scripts or log polling
- The local app receives updates through an HTTP endpoint such as `/state`
- CodeBuddy CLI / Code events work, but IDE-only activity does not
- Repository searches show `CodeBuddy Code` support, but no `ACP`, IDE event API, or IDE-specific hook integration

Typical symptoms:

- `~/.codebuddy/settings.json` already contains hook commands, but the app stays idle when only CodeBuddy IDE is used
- The project distinguishes editors only as `code` / `cursor`, not `codebuddy`
- There is no fallback telemetry except hook events or log polling

## Solution

1. **Separate CodeBuddy Code from CodeBuddy IDE mentally first**
   - `~/.codebuddy/settings.json` belongs to the **CodeBuddy Code / CLI configuration layer**.
   - Do not assume it provides **IDE work-status events**.

2. **Verify the existing integration path**
   - Check whether the repository writes hooks to `~/.codebuddy/settings.json`
   - Check whether hook scripts post `{ state, session_id, event, agent_id }` to a local server
   - Confirm whether the status server only updates on incoming hook/log events

3. **Search for IDE-native support**
   Look for any of the following:
   - `ACP` / `acp`
   - IDE plugin or extension code that emits work-state events
   - CodeBuddy IDE-specific config files or APIs
   - `editor === "codebuddy"` or similar editor normalization

   If none exist, the project likely supports **CodeBuddy Code only**, not IDE-native activity.

4. **Check whether hooks are actually installed**
   - If `~/.codebuddy/settings.json` contains the hook commands, then installation is likely fine
   - If the app still does not react to IDE-only activity, the missing piece is **event source support**, not hook registration

5. **Check backup detection paths**
   Some projects have a backup “process is running” detection path for startup recovery.
   - If that path only checks processes like `claude`, `codex`, `copilot`, `gemini`, it will not help CodeBuddy IDE
   - Even if a registry contains `codebuddy-code`, a separate hardcoded startup detector may still omit it

6. **Conclude the root cause explicitly**
   The root cause is usually:
   - The project is integrated with **CodeBuddy Code hooks**, not **CodeBuddy IDE work-state events**
   - Therefore opening the IDE alone produces **no state events** for the app to consume

7. **Pick the correct fix direction**
   Choose one of these depending on product intent:

   - **If only CodeBuddy Code support is intended**:
     update docs/UI text to make that distinction explicit
   - **If CodeBuddy IDE should also drive status**:
     add a real IDE event source, such as:
     - IDE-specific hook integration
     - IDE extension/plugin bridge
     - ACP/session bridge if the IDE exposes one
     - a polling mechanism over an IDE-owned state/log source

## Verification

A diagnosis is confirmed when:

- `~/.codebuddy/settings.json` already has the expected hook commands
- Repository search shows support for `CodeBuddy Code` but not IDE-native integration
- The local status server updates only through hook/log inputs
- Using CodeBuddy IDE alone does not generate any incoming status events

## Example

A pet app posts all agent activity through `/state` and installs hooks into `~/.codebuddy/settings.json`. The repo contains:

- a `codebuddy-code` agent definition
- hook registration for target `codebuddy`
- a hook script that detects `codebuddy` / `codebuddy-code`
- no `ACP` references
- no `editor: "codebuddy"` normalization

Result: `CodeBuddy Code` sessions animate the pet, but opening `CodeBuddy IDE` alone does not. The issue is not broken hook installation; it is that the project has **no CodeBuddy IDE event bridge**.

## Notes

- A project may partially support CodeBuddy via CLI hooks while still lacking IDE support
- Backup startup detection is often misleading because it can be hardcoded separately from the main agent registry
- If docs say “supports CodeBuddy” without saying “CodeBuddy Code”, users will often assume IDE-native support exists

## References

- `https://www.codebuddy.ai/docs/zh/cli/settings` — confirms `.codebuddy/settings.json` is part of CodeBuddy Code / CLI configuration
