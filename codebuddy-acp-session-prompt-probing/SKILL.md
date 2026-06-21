---
name: codebuddy-acp-session-prompt-probing
description: |
  Probe CodeBuddy ACP session/prompt payloads and event flow. Use when: (1) `codebuddy --acp --acp-transport stdio` is available, (2) you need to integrate a persistent CodeBuddy worker instead of `--print`, (3) `session/prompt` rejects message-style payloads like `{role:"user",content:...}`, or (4) you need to determine whether ACP expects content blocks vs chat messages. Covers verified `initialize -> session/new -> session/prompt` probing, minimal valid text payload shape, and how to distinguish schema validation success from missing completion events.
author: Claude Code
version: 1.0.0
date: 2026-03-08
---

# CodeBuddy ACP Session Prompt Probing

## Problem
When integrating CodeBuddy through ACP, it is not obvious what `session/prompt` expects. A common mistake is to send chat-message style payloads such as `{ role: "user", content: ... }`, assuming ACP mirrors Anthropic/OpenAI message formats. In practice, this causes schema errors and blocks persistent-session integrations.

## Context / Trigger Conditions
Use this skill when all of the following are true:

- You are using `codebuddy --acp --acp-transport stdio`
- You have already confirmed `initialize` and `session/new` or `session/load` exist
- `session/prompt` complains about payload shape, especially with errors like:
  - `Invalid input: expected array, received string`
  - `invalid_union`
  - `Invalid input: expected "text"`
  - `Invalid input: expected string, received undefined`
- You need to know whether ACP expects:
  - message objects (`role`, `content`), or
  - content blocks (`type`, `text`, etc.)

## Solution

### 1. Establish a stable ACP baseline
Always probe in this order:

1. `initialize`
2. `session/new` (or `session/load` if resuming)
3. `session/prompt`

Verified minimal working setup:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":1,"capabilities":{},"clientInfo":{"name":"probe","version":"0.1.0"}}}
```

```json
{"jsonrpc":"2.0","id":2,"method":"session/new","params":{"cwd":"/absolute/path","mcpServers":[],"model":"claude-sonnet-4.6"}}
```

### 2. Treat `session/prompt.prompt` as an array of content items, not chat messages
Verified behavior:

- `prompt` must be an **array**
- The array items are **content-block union variants**
- They are **not** message objects with `role` and `content`

### 3. Use this as the minimal text payload
This payload passed schema validation in probing:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "session/prompt",
  "params": {
    "sessionId": "<session-id>",
    "prompt": [
      { "type": "text", "text": "reply with exactly pong" }
    ]
  }
}
```

### 4. Treat these shapes as invalid for ACP `session/prompt`
These were explicitly rejected during probing:

```json
[{"role":"user","content":"..."}]
[{"role":"user","content":[{"type":"text","text":"..."}]}]
[{"type":"message","role":"user","content":"..."}]
[{"type":"message","role":"user","content":[{"type":"text","text":"..."}]}]
[{"type":"user","text":"..."}]
[{"kind":"text","text":"..."}]
```

### 5. Infer the union schema from error details
When probing with invalid payloads like `[{}]`, CodeBuddy returned `invalid_union` errors showing branches such as:

- text block:
  - `type: "text"`
  - `text: string`
- image block:
  - `type: "image"`
  - `data: string`
  - `mimeType: string`
- audio block:
  - `type: "audio"`
  - `data: string`
  - `mimeType: string`

This means ACP prompt items should be modeled like content blocks, e.g.:

```ts
type AcpPromptItem =
  | { type: "text"; text: string }
  | { type: "image"; data: string; mimeType: string }
  | { type: "audio"; data: string; mimeType: string };
```

### 6. Separate schema success from completion delivery
A valid text item may still produce no immediate RPC result for the request id. In probing, the payload:

```json
[{"type":"text","text":"reply with exactly pong and nothing else"}]
```

produced:

- no schema error
- a `session/update` notification with `sessionUpdate: "available_commands_update"`
- no immediate terminal `id:3 result` or `id:3 error` within the observation window

Interpretation:

- the input shape was accepted
- `session/prompt` may be asynchronous and notification-driven
- payload validation and completion delivery are separate concerns

## Verification
You have verified the finding if all of the following are true:

1. `initialize` returns `protocolVersion: 1`
2. `session/new` returns a real `sessionId`
3. `session/prompt` with `prompt: "..."` fails because ACP expects an array
4. `session/prompt` with message-style items fails with `invalid_union`
5. `session/prompt` with `[{"type":"text","text":"..."}]` does **not** fail schema validation
6. You may see only `session/update` notifications initially; that still counts as input-shape success

## Example
Suppose you are replacing a gateway design like:

```text
HTTP request -> flatten history -> spawn codebuddy --print -> return text
```

with a persistent ACP worker design:

```text
HTTP request -> reuse ACP worker -> session/prompt -> consume updates/events
```

The correct first-step mapping is:

```ts
const promptItems = [
  { type: "text", text: userText }
];
```

Not:

```ts
const promptItems = [
  { role: "user", content: userText }
];
```

## Notes
- Do not assume CodeBuddy ACP mirrors Anthropic Messages API or OpenAI Responses API.
- `session/prompt` appears session-centric and event-driven rather than simple request-response RPC.
- A successful schema probe does **not** prove you have found the final assistant-output event type.
- The next investigation step after payload validation is: identify which `session/update` variants or follow-up events carry assistant text and completion state.

## References
- CodeBuddy CLI local probing with `codebuddy --acp --acp-transport stdio`
- Verified in local investigation on 2026-03-08
