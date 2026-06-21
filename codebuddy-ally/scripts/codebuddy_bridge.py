"""
Codebuddy Bridge Script for Claude Agent Skills.
Wraps the Codebuddy CLI to provide a JSON-based interface for Claude.
"""
from __future__ import annotations

import json
import re
import os
import sys
import select
import queue
import subprocess
import threading
import time
import shutil
import argparse
from pathlib import Path
from typing import Generator, List, Optional

try:
    import pty
except ImportError:  # pragma: no cover - Windows does not provide pty
    pty = None

ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def _get_windows_npm_paths() -> List[Path]:
    """Return candidate directories for npm global installs on Windows."""
    if os.name != "nt":
        return []
    paths: List[Path] = []
    env = os.environ
    if prefix := env.get("NPM_CONFIG_PREFIX") or env.get("npm_config_prefix"):
        paths.append(Path(prefix))
    if appdata := env.get("APPDATA"):
        paths.append(Path(appdata) / "npm")
    if localappdata := env.get("LOCALAPPDATA"):
        paths.append(Path(localappdata) / "npm")
    if programfiles := env.get("ProgramFiles"):
        paths.append(Path(programfiles) / "nodejs")
    return paths


def _augment_path_env(env: dict) -> None:
    """Prepend npm global directories to PATH if missing."""
    if os.name != "nt":
        return
    path_key = next((k for k in env if k.upper() == "PATH"), "PATH")
    path_entries = [p for p in env.get(path_key, "").split(os.pathsep) if p]
    lower_set = {p.lower() for p in path_entries}
    for candidate in _get_windows_npm_paths():
        if candidate.is_dir() and str(candidate).lower() not in lower_set:
            path_entries.insert(0, str(candidate))
            lower_set.add(str(candidate).lower())
    env[path_key] = os.pathsep.join(path_entries)


def _resolve_executable(name: str, env: dict) -> str:
    """Resolve executable path, checking npm directories for .cmd/.bat on Windows."""
    if os.path.isabs(name) or os.sep in name or (os.altsep and os.altsep in name):
        return name
    path_key = next((k for k in env if k.upper() == "PATH"), "PATH")
    path_val = env.get(path_key)
    win_exts = {".exe", ".cmd", ".bat", ".com"}
    if resolved := shutil.which(name, path=path_val):
        if os.name == "nt":
            suffix = Path(resolved).suffix.lower()
            if not suffix:
                resolved_dir = str(Path(resolved).parent)
                for ext in (".cmd", ".bat", ".exe", ".com"):
                    candidate = Path(resolved_dir) / f"{name}{ext}"
                    if candidate.is_file():
                        return str(candidate)
            elif suffix not in win_exts:
                return resolved
        return resolved
    if os.name == "nt":
        for base in _get_windows_npm_paths():
            for ext in (".cmd", ".bat", ".exe", ".com"):
                candidate = base / f"{name}{ext}"
                if candidate.is_file():
                    return str(candidate)
    return name


def _run_shell_command_with_pty(cmd: List[str], env: dict, cwd: Optional[str] = None) -> Generator[str, None, None]:
    """Execute a command through a pseudo-tty (required by newer codebuddy CLI)."""
    popen_cmd = cmd.copy()
    exe_path = _resolve_executable(cmd[0], env)
    popen_cmd[0] = exe_path

    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(
        popen_cmd,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        cwd=cwd,
        env=env,
        close_fds=True,
    )
    os.close(slave_fd)

    buffer = ""
    graceful_shutdown_delay = 0.3

    def is_turn_completed(line: str) -> bool:
        try:
            data = json.loads(strip_ansi_control_sequences(line))
            data_type = data.get("type")
            if data_type == "turn.completed":
                return True
            if data_type == "result":
                return True
            return False
        except (json.JSONDecodeError, AttributeError, TypeError):
            return False

    try:
        while True:
            readable, _, _ = select.select([master_fd], [], [], 0.5)
            if readable:
                chunk = os.read(master_fd, 4096)
                if not chunk:
                    if process.poll() is not None:
                        break
                    continue
                decoded = chunk.decode("utf-8", errors="replace")
                buffer += decoded
                while "\n" in buffer:
                    raw_line, buffer = buffer.split("\n", 1)
                    line = raw_line.rstrip("\r")
                    if line:
                        yield line
                        if is_turn_completed(line):
                            time.sleep(graceful_shutdown_delay)
                            process.terminate()
            elif process.poll() is not None:
                break

        if buffer.strip():
            yield buffer.strip()
    finally:
        try:
            os.close(master_fd)
        except OSError:
            pass
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def run_shell_command(cmd: List[str], cwd: Optional[str] = None) -> Generator[str, None, None]:
    """Execute a command and stream its output line-by-line."""
    env = os.environ.copy()
    _augment_path_env(env)

    if os.name != "nt" and pty is not None:
        yield from _run_shell_command_with_pty(cmd, env, cwd)
        return

    popen_cmd = cmd.copy()
    exe_path = _resolve_executable(cmd[0], env)
    popen_cmd[0] = exe_path

    # Windows .cmd/.bat files need cmd.exe wrapper (avoid shell=True for security)
    if os.name == "nt" and Path(exe_path).suffix.lower() in {".cmd", ".bat"}:
        # Escape shell metacharacters for cmd.exe
        def _cmd_quote(arg: str) -> str:
            if not arg:
                return '""'
            # For Windows batch files, % and ^ must be escaped before quoting
            arg = arg.replace('%', '%%')
            arg = arg.replace('^', '^^')
            if any(c in arg for c in '&|<>()^" \t'):
                # To safely escape " inside "...", close quote, escape ", reopen
                escaped = arg.replace('"', '"^""')
                return f'"{escaped}"'
            return arg
        cmdline = " ".join(_cmd_quote(a) for a in popen_cmd)
        comspec = env.get("COMSPEC", "cmd.exe")
        popen_cmd = f'"{comspec}" /d /s /c "{cmdline}"'

    process = subprocess.Popen(
        popen_cmd,
        shell=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8',
        errors='replace',
        env=env,
        cwd=cwd,
    )

    output_queue: queue.Queue[Optional[str]] = queue.Queue()
    GRACEFUL_SHUTDOWN_DELAY = 0.3

    def is_turn_completed(line: str) -> bool:
        try:
            data = json.loads(line)
            data_type = data.get("type")
            if data_type == "turn.completed":
                return True
            if data_type == "result":
                return True
            return False
        except (json.JSONDecodeError, AttributeError, TypeError):
            return False

    def read_output() -> None:
        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                stripped = line.strip()
                output_queue.put(stripped)
                if is_turn_completed(stripped):
                    time.sleep(GRACEFUL_SHUTDOWN_DELAY)
                    process.terminate()
                    break
            process.stdout.close()
        output_queue.put(None)

    thread = threading.Thread(target=read_output)
    thread.start()

    while True:
        try:
            line = output_queue.get(timeout=0.5)
            if line is None:
                break
            yield line
        except queue.Empty:
            if process.poll() is not None and not thread.is_alive():
                break

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    thread.join(timeout=5)

    while not output_queue.empty():
        try:
            line = output_queue.get_nowait()
            if line is not None:
                yield line
        except queue.Empty:
            break

def windows_escape(prompt):
    """Windows style string escaping for newlines and special chars in prompt text."""
    result = prompt.replace('\n', '\\n')
    result = result.replace('\r', '\\r')
    result = result.replace('\t', '\\t')
    return result


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

def strip_ansi_control_sequences(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)

def extract_assistant_text(message: dict) -> str:
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if not isinstance(content, list):
        return ""
    parts: List[str] = []
    for block in content:
        if isinstance(block, dict):
            block_type = block.get("type")
            if block_type in {"text", "output_text"}:
                text = block.get("text", "")
                if isinstance(text, str):
                    parts.append(text)
    return "".join(parts)

def get_codebuddy_version() -> str:
    env = os.environ.copy()
    _augment_path_env(env)
    exe = _resolve_executable("codebuddy", env)
    try:
        result = subprocess.run(
            [exe, "-V"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=5,
            check=False,
        )
    except Exception:
        return ""
    output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
    match = re.search(r"(\d+\.\d+\.\d+)", output)
    return match.group(1) if match else ""

def build_legacy_command(args: argparse.Namespace, prompt: str) -> List[str]:
    cmd = ["codebuddy", "exec", "--sandbox", args.sandbox, "--cd", args.cd, "--json"]

    if args.image:
        cmd.extend(["--image", ",".join(args.image)])

    if args.model:
        cmd.extend(["--model", args.model])

    if args.profile:
        cmd.extend(["--profile", args.profile])

    if args.yolo:
        cmd.append("--yolo")

    if args.skip_git_repo_check:
        cmd.append("--skip-git-repo-check")

    if args.SESSION_ID:
        cmd.extend(["resume", args.SESSION_ID])

    cmd += ["--", prompt]
    return cmd

def build_modern_command(args: argparse.Namespace, prompt: str) -> List[str]:
    cmd = ["codebuddy", "--print", "--output-format", "stream-json"]

    # Non-interactive bridge must avoid runtime permission prompts that block in CI/pipe mode.
    cmd.extend(["--permission-mode", "bypassPermissions"])

    if args.sandbox == "danger-full-access" or args.yolo:
        cmd.append("--dangerously-skip-permissions")

    if args.model:
        cmd.extend(["--model", args.model])

    if args.profile:
        cmd.extend(["--profile", args.profile])

    if args.SESSION_ID:
        cmd.extend(["--resume", args.SESSION_ID])

    cmd += ["--", prompt]
    return cmd


def main():
    configure_windows_stdio()
    parser = argparse.ArgumentParser(description="Codebuddy Bridge")
    parser.add_argument("--PROMPT", required=True, help="Instruction for the task to send to codebuddy.")
    parser.add_argument("--cd", required=True, help="Set the workspace root for codebuddy before executing the task.")
    parser.add_argument("--sandbox", default="read-only", choices=["read-only", "workspace-write", "danger-full-access"], help="Sandbox policy for model-generated commands. Defaults to `read-only`.")
    parser.add_argument("--SESSION_ID", default="", help="Resume the specified session of the codebuddy. Defaults to `None`, start a new session.")
    parser.add_argument("--skip-git-repo-check", action="store_true", default=True, help="Allow codebuddy running outside a Git repository (useful for one-off directories).")
    parser.add_argument("--return-all-messages", action="store_true", help="Return all messages (e.g. reasoning, tool calls, etc.) from the codebuddy session. Set to `False` by default, only the agent's final reply message is returned.")
    parser.add_argument("--image", action="append", default=[], help="Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.")
    parser.add_argument("--model", default="", help="The model to use for the codebuddy session. This parameter is strictly prohibited unless explicitly specified by the user.")
    parser.add_argument("--yolo", action="store_true", help="Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.")
    parser.add_argument("--profile", default="", help="Configuration profile name to load from `~/.codebuddy/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.")

    args = parser.parse_args()

    version = get_codebuddy_version()
    major_version = int(version.split(".")[0]) if version else 0
    use_modern_cli = major_version >= 2

    PROMPT = args.PROMPT
    if os.name == "nt":
        PROMPT = windows_escape(PROMPT)

    if use_modern_cli:
        cmd = build_modern_command(args, PROMPT)
    else:
        cmd = build_legacy_command(args, PROMPT)

    # Execution Logic
    all_messages = []
    agent_messages = ""
    success = True
    err_message = ""
    thread_id = None

    for line in run_shell_command(cmd, cwd=args.cd):
        try:
            clean_line = strip_ansi_control_sequences(line.strip())
            if not clean_line:
                continue
            line_dict = json.loads(clean_line)
            all_messages.append(line_dict)
            item = line_dict.get("item", {})
            item_type = item.get("type", "")
            if item_type == "agent_message":
                agent_messages = agent_messages + item.get("text", "")

            line_type = line_dict.get("type", "")
            if line_type == "assistant":
                assistant_text = extract_assistant_text(line_dict.get("message", {}))
                if assistant_text:
                    agent_messages = agent_messages + assistant_text
            if line_type == "result" and len(agent_messages) == 0:
                result_text = line_dict.get("result", "")
                if isinstance(result_text, str):
                    agent_messages = result_text

            if line_dict.get("thread_id") is not None:
                thread_id = line_dict.get("thread_id")
            if line_dict.get("session_id") is not None:
                thread_id = line_dict.get("session_id")
            if "fail" in line_dict.get("type", ""):
                success = False if len(agent_messages) == 0 else success
                err_message += "\n\n[codebuddy error] " + line_dict.get("error", {}).get("message", "")
            if line_type == "result" and line_dict.get("is_error"):
                success = False if len(agent_messages) == 0 else success
                err_message += "\n\n[codebuddy error] " + str(line_dict.get("result", "unknown error"))
            if "error" in line_dict.get("type", ""):
                error_msg = line_dict.get("message", "")
                is_reconnecting = bool(re.match(r'^Reconnecting\.\.\.\s+\d+/\d+$', error_msg))

                if not is_reconnecting:
                    success = False if len(agent_messages) == 0 else success
                    err_message += "\n\n[codebuddy error] " + error_msg

        except json.JSONDecodeError:
            err_message += "\n\n[json decode error] " + line
            continue

        except Exception as error:
            err_message += "\n\n[unexpected error] " + f"Unexpected error: {error}. Line: {line!r}"
            success = False
            break

    if thread_id is None and args.SESSION_ID:
        thread_id = args.SESSION_ID

    if thread_id is None:
        success = False
        err_message = "Failed to get `SESSION_ID` from the codebuddy session. \n\n" + err_message

    if len(agent_messages) == 0:
        success = False
        err_message = "Failed to get `agent_messages` from the codebuddy session. \n\n You can try to set `return_all_messages` to `True` to get the full reasoning information. " + err_message

    if success:
        result = {
            "success": True,
            "SESSION_ID": thread_id,
            "agent_messages": agent_messages,
        }

    else:
        result = {"success": False, "error": err_message}

    if args.return_all_messages:
        result["all_messages"] = all_messages

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
