#!/usr/bin/env python3
"""
Manage session aliases: a name -> session_id map at ~/.agents/skills/throw/aliases.json.
Pairs with pick, which resolves aliases before searching.

Usage:
  alias_session.py set <name> [<session-id>] [--note "..."]   # no id -> current session
  alias_session.py list
  alias_session.py rm <name>
  alias_session.py show <name>

Exit codes: 0 ok, 1 not found / nothing to do, 2 bad usage.
"""
import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
ALIAS_FILE = HOME / ".agents" / "skills" / "throw" / "aliases.json"
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def _load():
    if not ALIAS_FILE.exists():
        return {}
    try:
        with open(ALIAS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save(data):
    ALIAS_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(ALIAS_FILE.parent), prefix=".aliases-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, ALIAS_FILE)  # atomic
    except Exception:
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


def _now():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")


def _detect_current():
    """Return (id, tool, project) for the current session, or (None, None, None)."""
    # Claude Code exposes the current session id directly.
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if sid:
        return sid, "claude", os.getcwd()
    # Fallback: newest non-agent .jsonl in the current Claude project dir.
    cwd = os.getcwd()
    encoded = cwd.replace("/", "-")
    proj_dir = HOME / ".claude" / "projects" / encoded
    if proj_dir.is_dir():
        newest, newest_mtime = None, 0.0
        for p in proj_dir.glob("*.jsonl"):
            if p.name.startswith("agent-"):
                continue
            try:
                m = p.stat().st_mtime
            except Exception:
                continue
            if m > newest_mtime:
                newest_mtime, newest = m, p
        if newest:
            return newest.stem, "claude", cwd
    return None, None, None


def cmd_set(args):
    if not NAME_RE.match(args.name):
        print(f"error: invalid alias name '{args.name}' (use letters, digits, . _ -)", file=sys.stderr)
        return 2
    if args.session_id:
        sid, tool, project = args.session_id, None, None
    else:
        sid, tool, project = _detect_current()
        if not sid:
            print("error: could not detect the current session "
                  "(no CLAUDE_CODE_SESSION_ID and no session file found). "
                  "Pass a session id explicitly: set <name> <id>", file=sys.stderr)
            return 1
    data = _load()
    entry = {"id": sid, "created": _now()}
    if tool:
        entry["tool"] = tool
    if project:
        entry["project"] = project
    if args.note:
        entry["note"] = args.note
    existed = args.name in data
    data[args.name] = entry
    _save(data)
    action = "updated" if existed else "set"
    loc = f" [{tool} in {project}]" if tool else ""
    print(f"alias {action}: {args.name} -> {sid}{loc}")
    return 0


def cmd_list(args):
    data = _load()
    if not data:
        print(f"(no session aliases in {ALIAS_FILE})")
        return 0
    print(f"{len(data)} alias(es) in {ALIAS_FILE}:")
    for name in sorted(data):
        e = data[name]
        loc = f"[{e.get('tool', '?')} in {e.get('project', '?')}]" if e.get("tool") else ""
        note = f"  # {e['note']}" if e.get("note") else ""
        print(f"  {name} -> {e['id']} {loc}  ({e.get('created', '?')}){note}")
    return 0


def cmd_rm(args):
    data = _load()
    if args.name not in data:
        print(f"error: no alias named '{args.name}'", file=sys.stderr)
        return 1
    sid = data[args.name].get("id")
    del data[args.name]
    _save(data)
    print(f"alias removed: {args.name} (was -> {sid})")
    return 0


def cmd_show(args):
    data = _load()
    if args.name not in data:
        print(f"error: no alias named '{args.name}'", file=sys.stderr)
        return 1
    e = data[args.name]
    print(f"alias: {args.name}")
    for k in ("id", "tool", "project", "created", "note"):
        if k in e:
            print(f"  {k}: {e[k]}")
    print(f"  resume with: pick {args.name}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Manage session aliases (name -> session_id).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_set = sub.add_parser("set", help="alias a session to a name")
    p_set.add_argument("name")
    p_set.add_argument("session_id", nargs="?", default=None)
    p_set.add_argument("--note", default=None)
    p_set.set_defaults(func=cmd_set)
    p_list = sub.add_parser("list", help="list all aliases")
    p_list.set_defaults(func=cmd_list)
    p_rm = sub.add_parser("rm", help="remove an alias")
    p_rm.add_argument("name")
    p_rm.set_defaults(func=cmd_rm)
    p_show = sub.add_parser("show", help="show an alias")
    p_show.add_argument("name")
    p_show.set_defaults(func=cmd_show)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
