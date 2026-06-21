#!/usr/bin/env python3
"""
Locate a coding session by ID/prefix across Codex and Claude Code stores,
and emit a handoff context for continuing its work in the current session
(with a relaunch command as fallback).

Read-only: only searches and reads session files. Never executes the resume.

Usage:
  locate_session.py <id> --continue-here [--type codex|claude] [--json] [--copy]   (default)
  locate_session.py <id-or-prefix> [--type codex|claude] [--json] [--copy]          (light locate)
  locate_session.py --recent [--type codex|claude]

Exit codes: 0 = single match / ok, 1 = no match, 2 = multiple matches, 3 = bad usage.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
CODEX_DIR = HOME / ".codex" / "sessions"
CLAUDE_DIR = HOME / ".claude" / "projects"
ALIAS_FILE = HOME / ".agents" / "skills" / "throw" / "aliases.json"
UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
# Absolute paths under /Users; stop at whitespace, quotes, angle brackets, backtick,
# backslash (JSON escapes like \n), and shell metacharacters (defense-in-depth).
USER_PATH_RE = re.compile(r"/Users/[^\s\"'<>`\\;|&$]+")
ABOUT_MAX = 120
TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")  # strip markup tags, not `a < b` comparisons


# ---------- helpers ----------------------------------------------------------

def _local_dt(iso_ts):
    """ISO-8601 timestamp -> friendly local string. Handles Z and explicit offsets."""
    if not iso_ts:
        return "?"
    s = str(iso_ts)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M")
    except Exception:
        pass
    try:
        base = s.rstrip("Z").split(".")[0]
        dt = datetime.strptime(base, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).astimezone()
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return s


def _mtime_str(p):
    try:
        return datetime.fromtimestamp(p.stat().st_mtime).astimezone().strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"


def _mtime_num(p):
    try:
        return p.stat().st_mtime
    except Exception:
        return 0.0


def _read_json_lines(path, n=80):
    """Parse JSON objects from up to n lines (n=None for all). Skips bad lines."""
    out = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            i = 0
            for line in f:
                if n is not None and i >= n:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                    i += 1
                except Exception:
                    continue
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
    except Exception:
        pass
    return out


def _short(s, n=ABOUT_MAX):
    if not s:
        return ""
    s = TAG_RE.sub("", str(s))
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _trunc(s, n=400):
    if not s:
        return ""
    s = TAG_RE.sub("", str(s))
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _copy_to_clipboard(text):
    """Copy text to the macOS clipboard without involving a shell. Returns success."""
    try:
        subprocess.run(["pbcopy"], input=text.encode(), check=False)
        return True
    except FileNotFoundError:
        return False  # pbcopy not available (non-macOS)
    except Exception:
        return False


def _launch_command(tool, uid, cwd):
    """Build the exact resume/relaunch command for a session. cwd is user-controlled -> quoted."""
    cwd_exists = bool(cwd) and os.path.isdir(cwd)
    if tool == "Codex":
        cmd = f"codex resume {uid}"
        if cwd_exists:
            cmd += f" -C {shlex.quote(cwd)}"
        note = "storage is global; -C sets the working dir. If a direct resume can't find it from an odd cwd, use: codex resume --all " + uid
        return cmd, note
    # Claude Code
    if cwd_exists:
        return (f"cd {shlex.quote(cwd)} && claude --resume {uid}",
                "claude --resume only searches the current project dir, so the cd into the original project is required.")
    return (f"claude --resume {uid}",
            "original project dir not found on disk; claude --resume may not locate this session — try running it from the session's original project.")


# ---------- per-tool summarizers (metadata) ---------------------------------

def _claude_meta(path):
    cwd = branch = start_ts = None
    for obj in _read_json_lines(path, 80):
        if not isinstance(obj, dict):
            continue
        if cwd is None and obj.get("cwd"):
            cwd = obj["cwd"]
        if branch is None and obj.get("gitBranch"):
            branch = obj["gitBranch"]
        if start_ts is None and obj.get("timestamp"):
            start_ts = obj["timestamp"]
        if cwd and start_ts:
            break
    return cwd, branch, start_ts


def _codex_meta(path):
    cwd = start_ts = None
    for obj in _read_json_lines(path, 80):
        if isinstance(obj, dict) and obj.get("type") == "session_meta":
            p = obj.get("payload")
            if isinstance(p, dict):
                cwd = cwd or p.get("cwd")
                start_ts = start_ts or p.get("timestamp")
    return cwd, start_ts


def _claude_intent(path):
    for obj in _read_json_lines(path, 80):
        if isinstance(obj, dict) and obj.get("type") == "user":
            msg = obj.get("message")
            if isinstance(msg, dict):
                c = msg.get("content")
                if isinstance(c, str) and c.strip():
                    return c.strip()
    return None


def _codex_intent(path):
    for obj in _read_json_lines(path, 80):
        if not isinstance(obj, dict) or obj.get("type") == "session_meta":
            continue
        p = obj.get("payload")
        text = None
        if isinstance(p, dict):
            text = p.get("text") or p.get("message")
            if isinstance(text, list):
                text = " ".join(t.get("text", "") for t in text if isinstance(t, dict))
        if isinstance(text, str) and text.strip():
            return text.strip()
    return None


# ---------- finders ----------------------------------------------------------
# Only real session files are considered:
#   Codex       -> rollout-*-<UUID>.jsonl  (UUID must appear in the name)
#   Claude Code -> <UUID>.jsonl            (stem must be exactly a UUID)
# This excludes subagent transcripts (agent-*.jsonl) and other non-session noise.

def _find_codex(query):
    res = []
    if not CODEX_DIR.exists():
        return res
    q = query.lower()
    for p in CODEX_DIR.rglob("*.jsonl"):
        m = UUID_RE.search(p.name)
        if not m:
            continue
        if q in p.name.lower():
            res.append((p, m.group(0)))
    return res


def _find_claude(query):
    res = []
    if not CLAUDE_DIR.exists():
        return res
    q = query.lower()
    for p in CLAUDE_DIR.rglob("*.jsonl"):
        if not UUID_RE.fullmatch(p.stem):
            continue
        if q in p.stem.lower():
            res.append((p, p.stem))
    return res


# ---------- describers (light locate mode) ----------------------------------

def _describe_codex(p, uid):
    cwd, start_ts = _codex_meta(p)
    cmd, note = _launch_command("Codex", uid, cwd)
    return {
        "type": "Codex",
        "id": uid,
        "path": str(p),
        "project": cwd or "(unknown)",
        "branch": "",
        "started": _local_dt(start_ts) if start_ts else "?",
        "last_active": _mtime_str(p),
        "about": _short(_codex_intent(p)),
        "command": cmd,
        "command_note": note,
        "_mtime": _mtime_num(p),
    }


def _describe_claude(p, uid):
    cwd, branch, start_ts = _claude_meta(p)
    cmd, note = _launch_command("Claude Code", uid, cwd)
    return {
        "type": "Claude Code",
        "id": uid,
        "path": str(p),
        "project": cwd or "(unknown)",
        "branch": branch or "",
        "started": _local_dt(start_ts) if start_ts else "?",
        "last_active": _mtime_str(p),
        "about": _short(_claude_intent(p)),
        "command": cmd,
        "command_note": note,
        "_mtime": _mtime_num(p),
    }


def _search(query, type_filter):
    results = []
    if type_filter != "claude":
        for p, uid in _find_codex(query):
            results.append(_describe_codex(p, uid))
    if type_filter != "codex":
        for p, uid in _find_claude(query):
            results.append(_describe_claude(p, uid))
    return results


# ---------- handoff extraction (--continue-here) ----------------------------

def _extract_turn(obj):
    """Return (role, text) for a user/assistant turn, or (None, None). Best-effort across formats."""
    if not isinstance(obj, dict):
        return None, None
    t = obj.get("type")
    if t == "user":
        msg = obj.get("message")
        if isinstance(msg, dict):
            c = msg.get("content")
            if isinstance(c, str) and c.strip():
                return "user", c.strip()
        return None, None
    if t == "assistant":
        msg = obj.get("message")
        if isinstance(msg, dict):
            c = msg.get("content")
            if isinstance(c, list):
                parts = [b.get("text", "") for b in c
                         if isinstance(b, dict) and b.get("type") == "text" and b.get("text")]
                if parts:
                    return "assistant", " ".join(parts).strip()
        return None, None
    if t == "event_msg":  # Codex
        p = obj.get("payload")
        if isinstance(p, dict):
            pt = p.get("type")
            text = p.get("text") or p.get("message")
            if isinstance(text, list):
                text = " ".join(x.get("text", "") for x in text if isinstance(x, dict))
            if isinstance(text, str) and text.strip():
                if pt == "user_message":
                    return "user", text.strip()
                if pt == "agent_message":
                    return "assistant", text.strip()
    return None, None


def _norm_todo(x):
    if not isinstance(x, dict):
        return None
    subj = x.get("subject") or x.get("content") or x.get("description") or x.get("task")
    stat = x.get("status") or ""
    if subj:
        return {"subject": str(subj), "status": str(stat)}
    return None


def _todos_from_obj(obj):
    """Latest TodoWrite snapshot as list of {subject,status}, or None."""
    if not isinstance(obj, dict) or obj.get("type") != "assistant":
        return None
    msg = obj.get("message")
    if not isinstance(msg, dict):
        return None
    c = msg.get("content")
    if not isinstance(c, list):
        return None
    for b in c:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "TodoWrite":
            todos = (b.get("input") or {}).get("todos")
            if isinstance(todos, list):
                out = [t for t in (_norm_todo(x) for x in todos) if t]
                if out:
                    return out
    return None


def _files_from_obj(obj):
    """Set of file paths mentioned in one record (structured tool_use + raw regex)."""
    found = set()
    if not isinstance(obj, dict):
        return found
    if obj.get("type") == "assistant":
        msg = obj.get("message")
        if isinstance(msg, dict):
            c = msg.get("content")
            if isinstance(c, list):
                for b in c:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        inp = b.get("input") or {}
                        for k in ("file_path", "notebook_path"):
                            fp = inp.get(k)
                            if isinstance(fp, str):
                                found.add(fp)
    raw = json.dumps(obj, ensure_ascii=False)
    for m in USER_PATH_RE.findall(raw):
        found.add(m.rstrip(".,;:)]}>"))
    return found


def extract_handoff(path, tool, uid):
    """Stream a session transcript and extract a bounded handoff context + relaunch command."""
    intent = None
    recent = deque(maxlen=12)
    last_state = None
    todos = None
    tasks_created = []          # fallback when TodoWrite isn't used (TaskCreate-based harness)
    file_last_seen = {}
    cwd = branch = start_ts = None
    idx = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if not isinstance(obj, dict):
                    continue
                role, text = _extract_turn(obj)
                if role and text:
                    recent.append((role, text))
                    if intent is None and role == "user":
                        intent = text
                    if role == "assistant":
                        last_state = text
                t = _todos_from_obj(obj)
                if t:
                    todos = t  # latest snapshot wins
                if obj.get("type") == "assistant":
                    msg = obj.get("message")
                    if isinstance(msg, dict):
                        c = msg.get("content")
                        if isinstance(c, list):
                            for b in c:
                                if isinstance(b, dict) and b.get("type") == "tool_use" \
                                        and b.get("name") == "TaskCreate":
                                    inp = b.get("input") or {}
                                    subj = inp.get("subject")
                                    if subj and len(tasks_created) < 100:
                                        tasks_created.append({"subject": str(subj), "status": ""})
                for fp in _files_from_obj(obj):
                    file_last_seen[fp] = idx
                if cwd is None and obj.get("cwd"):
                    cwd = obj["cwd"]
                if branch is None and obj.get("gitBranch"):
                    branch = obj["gitBranch"]
                if start_ts is None and obj.get("timestamp"):
                    start_ts = obj["timestamp"]
                if obj.get("type") == "session_meta":
                    p = obj.get("payload")
                    if isinstance(p, dict):
                        cwd = cwd or p.get("cwd")
                        start_ts = start_ts or p.get("timestamp")
                idx += 1
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)

    if not todos and tasks_created:
        todos = tasks_created

    # Keep only real, sufficiently-specific paths (drops bare /Users, home dir,
    # and regex/markup fragments that slipped through).
    files = [fp for fp, _ in sorted(file_last_seen.items(), key=lambda kv: kv[1], reverse=True)
             if os.path.exists(fp) and len(fp.rstrip("/").split("/")) >= 4][:40]

    cmd, note = _launch_command(tool, uid, cwd)

    return {
        "tool": tool,
        "id": uid,
        "path": str(path),
        "project": cwd or "(unknown)",
        "branch": branch or "",
        "started": _local_dt(start_ts) if start_ts else "?",
        "last_active": _mtime_str(Path(path)),
        "intent": intent or "",
        "todos": todos or [],
        "files": files,
        "recent": list(recent),
        "last_state": last_state or "",
        "command": cmd,
        "command_note": note,
    }


# ---------- rendering --------------------------------------------------------

def _render_one(r):
    lines = [
        "SESSION FOUND",
        f"  type:         {r['type']}",
        f"  id:           {r['id']}",
        f"  project:      {r['project']}",
    ]
    if r["branch"]:
        lines.append(f"  branch:       {r['branch']}")
    lines += [
        f"  started:      {r['started']}",
        f"  last active:  {r['last_active']}",
        f"  about:        {r['about'] or '(unavailable)'}",
        "",
        "RESUME COMMAND",
        f"  {r['command']}",
        f"  ({r['command_note']})",
    ]
    return "\n".join(lines)


def _render_multi(query, results):
    lines = [f"MULTIPLE MATCHES for \"{query}\" ({len(results)})", ""]
    for r in results:
        loc = f"in {r['project']}" if r["project"] != "(unknown)" else ""
        lines.append(f"  [{r['type']}] {r['id']}  {loc}  last: {r['last_active']}")
        if r["about"]:
            lines.append(f"               about: {_short(r['about'], 90)}")
    lines += ["", "Re-run with the full UUID, or pass --type codex|claude to narrow."]
    return "\n".join(lines)


def _render_none(query, type_filter):
    if type_filter == "codex":
        where = "Codex (~/.codex/sessions)"
    elif type_filter == "claude":
        where = "Claude Code (~/.claude/projects)"
    else:
        where = "Codex (~/.codex/sessions) or Claude Code (~/.claude/projects)"
    return (
        f"NO MATCH for \"{query}\" in {where}.\n\n"
        "List recent sessions with:\n"
        "  python3 ~/.agents/skills/pick/scripts/locate_session.py --recent"
    )


def _render_recent(results, limit=5):
    by_type = {"Codex": [], "Claude Code": []}
    for r in results:
        by_type.setdefault(r["type"], []).append(r)
    lines = ["RECENT SESSIONS"]
    for t in ("Codex", "Claude Code"):
        rows = sorted(by_type.get(t, []), key=lambda r: r["_mtime"], reverse=True)[:limit]
        lines.append("")
        lines.append(f"{t}:" if rows else f"{t}: (none found)")
        for r in rows:
            loc = f"in {r['project']}" if r["project"] != "(unknown)" else ""
            lines.append(f"  {r['id']}  {loc}  last: {r['last_active']}")
            if r["about"]:
                lines.append(f"    about: {_short(r['about'], 90)}")
    return "\n".join(lines)


def _render_handoff(h):
    L = [f"HANDOFF CONTEXT  (source: {h['tool']} session {h['id']})", ""]
    L.append(f"  project:      {h['project']}")
    if h["branch"]:
        L.append(f"  branch:       {h['branch']}")
    L.append(f"  started:      {h['started']}")
    L.append(f"  last active:  {h['last_active']}")
    L.append("")
    L.append("INTENT (first user message)")
    L.append(f"  {_trunc(h['intent'], 400) or '(unavailable)'}")
    L.append("")
    if h["todos"]:
        L.append("OPEN TODOS (latest snapshot / tasks created)")
        for t in h["todos"]:
            mark = f"[{t['status']}]" if t.get("status") else "[—]"
            L.append(f"  {mark} {t['subject']}")
        L.append("")
    if h["files"]:
        L.append(f"FILES TOUCHED (most recent first, {len(h['files'])})")
        for fp in h["files"]:
            L.append(f"  {fp}")
        L.append("")
    L.append("RECENT ACTIVITY (last turns, truncated)")
    if h["recent"]:
        for role, text in h["recent"]:
            L.append(f"  [{role}] {_trunc(text, 400)}")
    else:
        L.append("  (none)")
    L.append("")
    L.append("LAST STATE")
    L.append(f"  {_trunc(h['last_state'], 400) or '(unavailable)'}")
    L.append("")
    L.append("RELAUNCH (if you'd rather reopen the session elsewhere)")
    L.append(f"  {h['command']}")
    L.append(f"  ({h['command_note']})")
    return "\n".join(L)


# ---------- alias resolution ------------------------------------------------

def _load_aliases():
    """Load the alias map {name: entry} from the throw skill's data file, or {}."""
    if not ALIAS_FILE.exists():
        return {}
    try:
        with open(ALIAS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _resolve_alias(query, data=None):
    """Exact alias match -> (id, tool_hint, name); else None.
    Aliases live in ~/.agents/skills/throw/aliases.json (managed by the throw skill)."""
    if data is None:
        data = _load_aliases()
    entry = data.get(query)
    if not isinstance(entry, dict) or not entry.get("id"):
        return None
    tool = entry.get("tool") if entry.get("tool") in ("codex", "claude") else None
    return entry["id"], tool, query


def _levenshtein(a, b):
    """Edit distance between two strings (typo tolerance for alias names)."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _is_subsequence(needle, haystack):
    """True if `needle`'s chars appear in order within `haystack` (fuzzy match)."""
    it = iter(haystack)
    return all(c in it for c in needle)


# Alias match tiers, best -> worst: exact > prefix > substring > fuzzy > typo.
# Each tier gets a wide lead over the next so a prefix never loses to a fuzzy hit,
# and within a tier a shorter name (closer to the query) ranks higher. This is the
# autojump / Ctrl+R idea: a remembered-but-imprecise name should surface its siblings.
def _score_alias(query, name):
    """How well does `query` match alias `name`? Returns (score, tier) or None.

    Case-insensitive. None = no usable match. Tiers:
      exact      q == n                   (test -> test)
      prefix     n starts with q          (test -> testb)
      substring  q occurs inside n        (est -> test)
      fuzzy      q is a subsequence of n  (ts -> test)
      typo       small edit distance      (tset -> test)
    """
    q = query.lower()
    n = name.lower()
    if q == n:
        return (1000, "exact")
    if n.startswith(q):
        return (900 - (len(n) - len(q)), "prefix")
    if q in n:
        return (700 - (len(n) - len(q)), "substring")
    # Require >= 2 chars before accepting a subsequence match, so a single stray
    # keystroke doesn't fuzzy-match every alias containing that letter.
    if len(q) >= 2 and _is_subsequence(q, n):
        return (400 - (len(n) - len(q)), "fuzzy")
    dist = _levenshtein(q, n)
    # Forgive typos only when lengths are close, so a 1-char query can't
    # typo-match a long alias and flood the results.
    if dist <= 2 and abs(len(q) - len(n)) <= 2:
        return (200 - dist * 30, "typo")
    return None


def _find_alias_candidates(query, data, exclude=None, max_n=8):
    """Alias names close to `query` (excluding exact `exclude`), best first.

    Returns list of (name, entry, tier). Used two ways: when the query has an
    exact alias hit, the strong near-misses (prefix/typo) become a hint; when
    there's no exact hit, all tiers become a pick-list (Ctrl+R / autojump style)."""
    scored = []
    for name, entry in data.items():
        if not isinstance(entry, dict) or not entry.get("id"):
            continue
        if name == exclude:
            continue
        s = _score_alias(query, name)
        if s is None:
            continue
        score, tier = s
        scored.append((score, name, entry, tier))
    scored.sort(key=lambda x: (-x[0], x[1]))  # score desc, then name asc for stable order
    return [(name, entry, tier) for _, name, entry, tier in scored[:max_n]]


def _render_alias_candidates(query, candidates):
    """Pick-list shown when a query matches no exact alias but has close ones."""
    lines = [f'NO ALIAS "{query}" — did you mean one of these?', ""]
    for name, entry, tier in candidates:
        loc = f"[{entry.get('tool', '?')} in {entry.get('project', '?')}]" if entry.get("tool") else ""
        note = f"  # {entry['note']}" if entry.get("note") else ""
        lines.append(f"  {name} {loc}  ({tier}){note}")
    lines += ["", "Re-run pick with the exact alias name you want."]
    return "\n".join(lines)


def _format_alias_hint(near):
    """One-line, low-noise hint appended after a successful resume when other
    aliases were a strong near-miss (e.g. typed "test" but "testb" also exists)."""
    names = ", ".join(n for n, _, _ in near)
    return f"(alias tip: also close — {names}; re-run `pick <name>` if you meant one of these)"


# ---------- main -------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Locate a Codex or Claude Code session by ID/prefix; default = handoff for continuing here."
    )
    ap.add_argument("query", nargs="?", default=None, help="session UUID, prefix, alias name, or Codex name")
    ap.add_argument("--type", choices=["codex", "claude"], default=None,
                    help="force a tool (skip auto-detection)")
    ap.add_argument("--recent", action="store_true", help="list recent sessions")
    ap.add_argument("--continue-here", action="store_true",
                    help="emit a handoff context for continuing the session's work in the current session (default behavior)")
    ap.add_argument("--copy", action="store_true",
                    help="copy the resume/relaunch command to the clipboard (single-match modes)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    if args.recent:
        if args.query:
            print("error: --recent ignores a query argument", file=sys.stderr)
            return 3
        results = _search("", args.type)
        if args.json:
            for r in results:
                r.pop("_mtime", None)
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return 0
        print(_render_recent(results))
        return 0

    if not args.query:
        print("error: provide a session ID/prefix, or use --recent", file=sys.stderr)
        return 3

    # Resolve alias -> id (alias takes precedence over UUID/prefix search).
    orig_query = args.query
    alias_name = None
    real_id = None
    near_aliases = []  # close alias names — hint after resume, or a pick-list
    alias_data = _load_aliases()
    alias_info = _resolve_alias(orig_query, alias_data)
    if alias_info:
        real_id, tool_hint, alias_name = alias_info
        args.query = real_id
        if args.type is None and tool_hint:
            args.type = tool_hint
        # Surface strong near-misses (prefix/typo) as a low-noise hint, so a
        # remembered-but-imprecise name like "test" still reveals "testb".
        near_aliases = [c for c in _find_alias_candidates(orig_query, alias_data, exclude=alias_name)
                        if c[2] in ("prefix", "typo")][:3]
    else:
        # No exact alias. Before falling back to UUID/prefix search, offer close
        # alias names — the user likely misremembered one (Ctrl+R / autojump style).
        cands = _find_alias_candidates(orig_query, alias_data)
        if cands:
            print(_render_alias_candidates(orig_query, cands))
            return 2
        # No close alias either; treat orig_query as a UUID/prefix below.

    results = _search(args.query, args.type)

    if not results:
        print(_render_none(args.query, args.type))
        if alias_name:
            print(f"(alias '{alias_name}' pointed to {real_id}, but no session with that id was found)")
        return 1
    if len(results) > 1:
        if args.json:
            for r in results:
                r.pop("_mtime", None)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(_render_multi(args.query, results))
        return 2

    # Single match.
    r = results[0]
    if args.continue_here:
        h = extract_handoff(Path(r["path"]), r["type"], r["id"])
        if args.json:
            print(json.dumps(h, ensure_ascii=False, indent=2))
            return 0
        if alias_name:
            print(f"(via alias '{alias_name}' -> {real_id})")
        print(_render_handoff(h))
        if args.copy:
            if _copy_to_clipboard(h["command"]):
                print("\n(copied relaunch command to clipboard)")
            else:
                print("\n(pbcopy unavailable — copy the command above manually)")
        if near_aliases:
            print(_format_alias_hint(near_aliases))
        return 0

    # Light locate mode.
    if args.json:
        r.pop("_mtime", None)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    if alias_name:
        print(f"(via alias '{alias_name}' -> {real_id})")
    print(_render_one(r))
    if args.copy:
        if _copy_to_clipboard(r["command"]):
            print("\n(copied resume command to clipboard)")
        else:
            print("\n(pbcopy unavailable — copy the command above manually)")
    if near_aliases:
        print(_format_alias_hint(near_aliases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
