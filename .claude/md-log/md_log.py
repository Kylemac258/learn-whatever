#!/usr/bin/env python3
"""md-log: mirror a Claude Code learning session into a markdown file.

The terminal / chat is hard on the eyes for long lessons and doesn't render
LaTeX. The linked .md is meant to be read rendered in Obsidian, where $math$,
mermaid, code, callouts and ![[image]] embeds all render natively.

Captured (reading-relevant content only):
  - your prompts
  - Claude's prose
  - questions asked with AskUserQuestion (written BEFORE you answer, so they
    appear live; never containing the correct answer) and your answers
  - one-line notes when a skill loads or a subagent is dispatched
Other tool calls (Bash, Read, Edit, ...) are omitted.

Append-only: your own edits to the file are never overwritten.

Commands (run by the /md-log skill):
  md_log.py link <file.md>   create/validate the file; the PostToolUse hook
                             then binds it to this session and backfills
  md_log.py unlink           the hook unbinds this session
  md_log.py hook             entry point for Claude Code hooks (JSON on stdin)
"""

import fcntl
import hashlib
import json
import re
import shlex
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]  # <project>/.claude/md-log -> <project>
STATE_DIR = HERE / "state"
EMBED_WIDTH = 600


# ── helpers ────────────────────────────────────────────────────────────────

def resolve_target(arg: str) -> Path:
    p = Path(arg).expanduser()
    if not p.is_absolute():
        p = PROJECT / p
    if p.suffix.lower() != ".md":
        p = p.with_suffix(p.suffix + ".md") if p.suffix else p.with_suffix(".md")
    return p.resolve()


def qhash(tool_input) -> str:
    return hashlib.sha1(json.dumps(tool_input, sort_keys=True).encode()).hexdigest()[:16]


def callout(kind: str, title: str, body: str = "") -> str:
    lines = [f"> [!{kind}] {title}"]
    for line in body.splitlines():
        lines.append(">" if not line.strip() else f"> {line}")
    return "\n".join(lines)


VIZ_IMG = re.compile(r"!\[[^\]]*\]\((?:<)?(?:[^)\s]*/)?viz/([^)/\s>]+\.(?:png|svg|jpg|jpeg))(?:>)?\)")


def rewrite_images(text: str) -> str:
    """Markdown images pointing into viz/ become Obsidian embeds."""
    return VIZ_IMG.sub(lambda m: f"![[{m.group(1)}|{EMBED_WIDTH}]]", text)


def clean_user_text(text: str):
    """Return the prompt as the user typed it, or None to skip it."""
    if "<command-name>" in text:
        name = re.search(r"<command-name>(.*?)</command-name>", text, re.S)
        args = re.search(r"<command-args>(.*?)</command-args>", text, re.S)
        name = name.group(1).strip() if name else ""
        if name.lstrip("/") == "md-log":
            return None
        return f"{name} {args.group(1).strip() if args else ''}".strip() or None
    for tag in ("system-reminder", "local-command-stdout", "local-command-stderr", "local-command-caveat"):
        text = re.sub(rf"<{tag}>.*?</{tag}>", "", text, flags=re.S)
    text = re.sub(r"</?pasted_content[^>]*>", "", text)
    text = text.strip()
    if not text or text.startswith("[Request interrupted"):
        return None
    return text


def question_block(tool_input) -> str:
    parts = []
    for q in (tool_input or {}).get("questions", []) or []:
        graded = str(q.get("header", "")).strip().lower() == "quiz"
        body = [f"**{q.get('question', '').strip()}**"]
        if q.get("multiSelect"):
            body.append("*(select all that apply)*")
        body.append("")
        for i, opt in enumerate(q.get("options", []) or [], 1):
            line = f"{i}. {opt.get('label', '')}"
            if opt.get("description"):
                line += f" — {opt['description']}"
            body.append(line)
        parts.append(callout("question", "QUIZ" if graded else "QUESTION", "\n".join(body)))
    return "\n\n".join(parts)


def answer_block(tool_input, response, is_error=False) -> str:
    if is_error:
        return callout("warning", "Question dismissed")
    answers = {}
    if isinstance(response, dict):
        answers = response.get("answers") or {}
        text = ""
    else:
        text = response if isinstance(response, str) else json.dumps(response)
    if not answers and text:
        answers = dict(re.findall(r'"(.+?)"="(.*?)"(?=[.,]|\s|$)', text, re.S))
    questions = [q.get("question", "") for q in (tool_input or {}).get("questions", []) or []]
    if answers:
        if len(answers) == 1 and len(questions) <= 1:
            body = str(next(iter(answers.values())))
        else:
            body = "\n".join(f"**{k}** — {v}" for k, v in answers.items())
    else:
        body = text.strip() or "(no answer)"
    return callout("info", "YOUR ANSWER", body)


def tool_result_text(block) -> str:
    c = block.get("content")
    if isinstance(c, list):
        return "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
    return c if isinstance(c, str) else ""


# ── state ──────────────────────────────────────────────────────────────────

class Session:
    def __init__(self, session_id: str):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", session_id)
        self.path = STATE_DIR / f"{safe}.json"
        self.lock_f = open(STATE_DIR / f"{safe}.lock", "w")
        fcntl.flock(self.lock_f, fcntl.LOCK_EX)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else None

    def save(self):
        if self.data is None:
            self.path.unlink(missing_ok=True)
        else:
            self.path.write_text(json.dumps(self.data))

    def emit(self, key: str, kind: str, md: str):
        """Append one block to the log unless it was already written."""
        d = self.data
        if key in d["rendered"] or not md.strip():
            return
        target = Path(d["file"])
        target.parent.mkdir(parents=True, exist_ok=True)
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        if kind == "assistant" and d.get("last_kind") == "assistant":
            chunk = md  # continue the same CLAUDE section
        elif kind == "assistant":
            chunk = callout("abstract", "CLAUDE") + "\n\n" + md
        else:
            chunk = md
        sep = "" if not existing.strip() else ("\n" if existing.endswith("\n") else "\n\n")
        with open(target, "a", encoding="utf-8") as f:
            f.write(sep + chunk.rstrip() + "\n")
        d["rendered"].append(key)
        d["last_kind"] = kind


# ── transcript sync ────────────────────────────────────────────────────────

def sync(sess: Session, transcript_path: str):
    d = sess.data
    tp = Path(transcript_path)
    if not tp.exists():
        return
    with open(tp, "rb") as f:
        f.seek(d.get("offset", 0))
        chunk = f.read()
    end = chunk.rfind(b"\n")
    if end < 0:
        return
    d["offset"] = d.get("offset", 0) + end + 1
    pending = d.setdefault("pending_q", {})  # tool_use_id -> tool_input

    for raw in chunk[: end + 1].splitlines():
        try:
            e = json.loads(raw)
        except ValueError:
            continue
        if e.get("isSidechain") or e.get("type") not in ("user", "assistant"):
            continue
        msg = e.get("message") or {}
        content = msg.get("content")
        uuid = e.get("uuid", "")

        if e["type"] == "user":
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            texts = []
            for b in content or []:
                if b.get("type") == "text" and not e.get("isMeta"):
                    t = clean_user_text(b.get("text", ""))
                    if t:
                        texts.append(t)
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in pending:
                    ti = pending.pop(b["tool_use_id"])
                    resp = e.get("toolUseResult")
                    if not isinstance(resp, dict):
                        resp = tool_result_text(b)
                    sess.emit("a:" + qhash(ti), "answer", answer_block(ti, resp, b.get("is_error")))
            if texts:
                sess.emit("u:" + uuid, "user", callout("quote", "YOU") + "\n\n" + "\n\n".join(texts))
            continue

        if msg.get("model") == "<synthetic>":
            continue
        for i, b in enumerate(content or []):
            bt = b.get("type")
            if bt == "text" and b.get("text", "").strip():
                sess.emit(f"t:{uuid}:{i}", "assistant", rewrite_images(b["text"].strip()))
            elif bt == "tool_use":
                name, ti = b.get("name"), b.get("input") or {}
                if name == "AskUserQuestion":
                    pending[b.get("id", "")] = ti
                    sess.emit("q:" + qhash(ti), "question", question_block(ti))
                elif name == "Skill" and ti.get("skill") != "md-log":
                    sess.emit("s:" + b.get("id", ""), "note",
                              callout("note", f"SKILL loaded: {ti.get('skill', '?')}"))
                elif name in ("Agent", "Task"):
                    who = ti.get("subagent_type") or "subagent"
                    sess.emit("g:" + b.get("id", ""), "note",
                              callout("note", f"{who}: {ti.get('description', '')}".strip()))


# ── entry points ───────────────────────────────────────────────────────────

def md_log_command(cmd: str):
    """If a Bash command ran md_log.py link/unlink, return (action, arg)."""
    if "md_log.py" not in cmd:
        return None
    try:
        toks = shlex.split(cmd)
    except ValueError:
        return None
    for i, t in enumerate(toks):
        if t.endswith("md_log.py") and i + 1 < len(toks):
            action = toks[i + 1]
            if action == "link" and i + 2 < len(toks):
                return ("link", toks[i + 2])
            if action == "unlink":
                return ("unlink", None)
    return None


def hook():
    inp = json.load(sys.stdin)
    sid = inp.get("session_id")
    if not sid:
        return
    event = inp.get("hook_event_name")
    tool = inp.get("tool_name")
    cmd = md_log_command((inp.get("tool_input") or {}).get("command", "")) if tool == "Bash" else None

    # Cheap exit for unlinked sessions.
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", sid)
    if not cmd and not (STATE_DIR / f"{safe}.json").exists():
        return

    sess = Session(sid)
    try:
        if cmd and event == "PostToolUse":
            action, arg = cmd
            if action == "unlink":
                sess.data = None
                return
            sess.data = {"file": str(resolve_target(arg)), "rendered": [], "offset": 0}
        if sess.data is None:
            return
        sync(sess, inp.get("transcript_path", ""))

        if tool == "AskUserQuestion":
            ti = inp.get("tool_input") or {}
            if event == "PreToolUse":  # show the question live, before it's answered
                sess.emit("q:" + qhash(ti), "question", question_block(ti))
            elif event == "PostToolUse":
                for k, v in list(sess.data.get("pending_q", {}).items()):
                    if v == ti:
                        sess.data["pending_q"].pop(k)
                sess.emit("a:" + qhash(ti), "answer", answer_block(ti, inp.get("tool_response")))
    finally:
        sess.save()


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "link":
        if len(args) < 2:
            sys.exit("usage: md_log.py link <file.md>")
        target = resolve_target(args[1])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch(exist_ok=True)
        print(f"Linked: {target}\nThis session will now be mirrored there (backfilled from the start).")
    elif args[0] == "unlink":
        print("Unlinked: this session is no longer mirrored.")
    elif args[0] == "hook":
        try:
            hook()
        except Exception:
            STATE_DIR.mkdir(parents=True, exist_ok=True)
            with open(STATE_DIR / "error.log", "a") as f:
                f.write(traceback.format_exc() + "\n")
        # Never block or inject anything into the session.
        sys.exit(0)
    else:
        sys.exit(f"unknown command: {args[0]}")


if __name__ == "__main__":
    main()
