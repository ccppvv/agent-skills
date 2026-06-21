---
name: claude-inline
description: >
  Launch Claude Code CLI with custom baseurl and apikey via environment variables.
  Use this skill when the user wants to start Claude Code with a custom API endpoint,
  or when they mention "claude-inline", "启动 claude", "用自定义 endpoint 跑 claude",
  or pass a baseurl/apikey for Claude Code. Supports both interactive mode and
  non-interactive (-p) mode. Prints the launch command for the user to run.
---

# Claude Inline

Launch Claude Code CLI with custom `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY`
environment variables. Useful for connecting to custom endpoints (OpenRouter,
local proxies, etc.).

## Configuration

Store defaults in `~/.workbuddy/skills/claude-inline/config.json`:

```json
{
  "baseurl": "https://openrouter.ai/api/v1",
  "apikey": "sk-...",
  "model": "anthropic/claude-3-5-sonnet"
}
```

- `baseurl` — custom API base URL
- `apikey` — API key for the endpoint
- `model` — (optional) model to use via `ANTHROPIC_MODEL`

If config file exists, use its values as defaults. CLI arguments override config values.

## Usage

### Parse user input

Accept baseurl and apikey from:
1. Explicit arguments in the user's message (e.g., `baseurl=xxx apikey=xxx`)
2. The config file at `~/.workbuddy/skills/claude-inline/config.json`
3. Ask the user if neither is available

### Print the launch command

Construct and print the command. **Do NOT execute it** — only print for the user.

**Interactive mode (default):**
```bash
ANTHROPIC_BASE_URL="<baseurl>" ANTHROPIC_API_KEY="<apikey>" claude
```

**Non-interactive mode (with `-p` flag):**
```bash
ANTHROPIC_BASE_URL="<baseurl>" ANTHROPIC_API_KEY="<apikey>" claude -p "<prompt>"
```

**With model override:**
```bash
ANTHROPIC_BASE_URL="<baseurl>" ANTHROPIC_API_KEY="<apikey>" ANTHROPIC_MODEL="<model>" claude
```

### Save config (optional)

If the user provides baseurl/apikey and it differs from the config, ask if they
want to save it as the new default. Write to the config file if confirmed.

## Notes

- Claude Code CLI must be installed separately (`npm install -g @anthropic-ai/claude-code`)
- The `ANTHROPIC_BASE_URL` must be a fully qualified URL (include `https://`)
- For OpenRouter: `ANTHROPIC_MODEL` should be set to the model ID (e.g., `anthropic/claude-3-5-sonnet-20241022`)
- Always wrap URL and key in double quotes to handle special characters
