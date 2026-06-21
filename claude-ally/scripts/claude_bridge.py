"""
Claude Bridge Script for Claude Agent Skills.
Wraps the Claude Code CLI to provide a JSON-based interface.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Dict


def configure_windows_stdio() -> None:
    """Configure stdout/stderr to use UTF-8 encoding on Windows."""
    if os.name != "nt":
        return
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def parse_json_output(raw: str) -> Dict[str, Any]:
    """Parse Claude JSON output. Supports single JSON or last-line JSON."""
    text = raw.strip()
    if not text:
        raise ValueError("Empty output from claude CLI")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue

    raise ValueError("Failed to parse JSON output from claude CLI")


def main() -> None:
    configure_windows_stdio()

    parser = argparse.ArgumentParser(description="Claude Bridge")
    parser.add_argument("--PROMPT", required=True, help="Instruction for the task to send to claude.")
    parser.add_argument("--cd", required=True, help="Set the workspace root before executing the task.")
    parser.add_argument("--SESSION_ID", default="", help="Resume the specified session ID.")
    parser.add_argument("--permission-mode", default="default", choices=["default", "acceptEdits", "bypassPermissions", "dontAsk", "plan"], help="Permission mode for Claude Code session.")
    parser.add_argument("--allowed-tools", default="", help="Comma-separated allowed tools.")
    parser.add_argument("--disallowed-tools", default="", help="Comma-separated disallowed tools.")
    parser.add_argument("--append-system-prompt", default="", help="Append system prompt.")
    parser.add_argument("--return-all-messages", action="store_true", help="Return raw JSON response.")
    parser.add_argument("--model", default="", help="The model to use. This parameter is strictly prohibited unless explicitly specified by the user.")
    parser.add_argument("--dangerously-skip-permissions", action="store_true", help="Bypass all permission checks. Use only in trusted sandboxes.")
    args = parser.parse_args()

    cmd = [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--permission-mode",
        args.permission_mode,
    ]

    if args.SESSION_ID:
        cmd.extend(["--resume", args.SESSION_ID])

    if args.allowed_tools:
        cmd.extend(["--allowedTools", args.allowed_tools])

    if args.disallowed_tools:
        cmd.extend(["--disallowedTools", args.disallowed_tools])

    if args.append_system_prompt:
        cmd.extend(["--append-system-prompt", args.append_system_prompt])

    if args.model:
        cmd.extend(["--model", args.model])

    if args.dangerously_skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    cmd.append(args.PROMPT)

    try:
        completed = subprocess.run(
            cmd,
            cwd=args.cd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except Exception as error:
        result = {"success": False, "error": f"Failed to execute claude CLI: {error}"}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    stdout_text = completed.stdout or ""
    stderr_text = completed.stderr or ""

    try:
        data = parse_json_output(stdout_text)
    except Exception as error:
        err = f"{error}."
        if stderr_text.strip():
            err += f"\n\n[claude stderr]\n{stderr_text.strip()}"
        if stdout_text.strip():
            err += f"\n\n[claude stdout]\n{stdout_text.strip()}"
        result = {"success": False, "error": err}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    session_id = data.get("session_id") or args.SESSION_ID
    agent_message = data.get("result", "")
    is_error = bool(data.get("is_error"))

    success = (not is_error) and bool(session_id) and bool(agent_message)

    if success:
        result = {
            "success": True,
            "SESSION_ID": session_id,
            "agent_messages": agent_message,
        }
    else:
        err_parts = []
        if is_error:
            err_parts.append("Claude returned is_error=true")
        if not session_id:
            err_parts.append("Failed to get SESSION_ID from Claude response")
        if not agent_message:
            err_parts.append("Failed to get agent_messages from Claude response")
        if stderr_text.strip():
            err_parts.append(f"[claude stderr]\n{stderr_text.strip()}")
        result = {
            "success": False,
            "error": "\n\n".join(err_parts) if err_parts else "Unknown Claude bridge error",
        }

    if args.return_all_messages:
        result["all_messages"] = data

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
