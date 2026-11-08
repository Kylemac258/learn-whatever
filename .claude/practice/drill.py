#!/usr/bin/env python3
"""drill.py — time and log practice attempts, so fluency is measured, not guessed.

Every practice item is logged to learner/practice.jsonl (accuracy and, for timed
items, seconds). `report` turns the log into per-concept accuracy, speed, trend
and a fluent/not-yet verdict.

Timing: `start` is called right after the question is shown. The answer time is
taken from a hook mark written the moment the learner submits (UserPromptSubmit,
or PostToolUse for AskUserQuestion), so Claude's own thinking time isn't counted.
Without the hook it falls back to the time `stop` runs (slightly long).

Commands:
  start  --topic T --concept C --kind K [--limit SECONDS]   -> prints an item id
  stop   <id> --result correct|partial|wrong|dontknow
  log    --topic T --concept C --kind K --result R            (untimed item)
  report [--topic T] [--concept C]
  mark                                                         (hook entry point)
"""

import argparse
import json
import os
import re
import statistics
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LEARNER = PROJECT / "learner"
LOG = LEARNER / "practice.jsonl"
STATE = HERE / "state"
PENDING = STATE / "pending.json"
MARK = STATE / "last_answer"

KINDS = ("recall", "solve", "explain", "discriminate", "speed", "transfer", "case", "boundary", "create")
RESULTS = ("correct", "partial", "wrong", "dontknow")
FLUENT_STREAK = 2  # correct-within-limit timed attempts in a row


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "general"


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_pending():
    return json.loads(PENDING.read_text()) if PENDING.exists() else {}


def save_pending(p):
    STATE.mkdir(parents=True, exist_ok=True)
    PENDING.write_text(json.dumps(p))


def append(entry):
    LEARNER.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_log():
    if not LOG.exists():
        return []
    out = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def cmd_start(a):
    p = load_pending()
    item = uuid.uuid4().hex[:6]
    p[item] = {"topic": slug(a.topic), "concept": a.concept.strip(), "kind": a.kind,
               "limit": a.limit, "t0": time.time()}
    save_pending(p)
    lim = f", limit {a.limit:g}s" if a.limit else ""
    print(f"started {item} ({a.kind}{lim}) — ask the question now; call `stop {item}` first thing next turn")


def cmd_stop(a):
    p = load_pending()
    it = p.pop(a.id, None)
    if not it:
        sys.exit(f"No running item {a.id!r}.")
    save_pending(p)
    t_end, source = time.time(), "stop"
    if MARK.exists():
        try:
            m = float(MARK.read_text().strip())
            if it["t0"] < m <= t_end:
                t_end, source = m, "answer"
        except ValueError:
            pass
    secs = round(t_end - it["t0"], 1)
    within = None if not it["limit"] else (secs <= it["limit"] and a.result == "correct")
    entry = {"ts": now_iso(), "topic": it["topic"], "concept": it["concept"], "kind": it["kind"],
             "result": a.result, "seconds": secs, "limit": it["limit"], "within_limit": within,
             "timing": source}
    append(entry)
    msg = f"{a.result}, {secs:g}s"
    if it["limit"]:
        msg += f" (limit {it['limit']:g}s: {'✓ within' if within else '✗ over' if a.result == 'correct' else '—'})"
    if source == "stop":
        msg += " [no answer mark; time includes Claude's turn]"
    print(msg)
    s = summarize([e for e in read_log() if e["topic"] == it["topic"] and e["concept"] == it["concept"]])
    print(f"{it['concept']}: {s['line']}")


def cmd_log(a):
    append({"ts": now_iso(), "topic": slug(a.topic), "concept": a.concept.strip(), "kind": a.kind,
            "result": a.result, "seconds": None, "limit": None, "within_limit": None, "timing": None})
    print(f"logged {a.result} ({a.kind}) for {a.concept.strip()}")


def summarize(entries):
    score = {"correct": 1.0, "partial": 0.5, "wrong": 0.0, "dontknow": 0.0}
    n = len(entries)
    acc = sum(score[e["result"]] for e in entries) / n if n else 0.0
    recent = entries[-6:]
    recent_acc = sum(score[e["result"]] for e in recent) / len(recent) if recent else 0.0
    timed = [e for e in entries if e.get("seconds") is not None and e["result"] == "correct"]
    med = statistics.median(e["seconds"] for e in timed) if timed else None
    trend = None
    if len(timed) >= 4:
        half = len(timed) // 2
        first = statistics.median(e["seconds"] for e in timed[:half])
        last = statistics.median(e["seconds"] for e in timed[half:])
        trend = (last - first) / first if first else None
    limited = [e for e in entries if e.get("limit")]
    streak = 0
    for e in reversed(limited):
        if e.get("within_limit"):
            streak += 1
        else:
            break
    fluent = streak >= FLUENT_STREAK
    parts = [f"{n} attempts", f"accuracy {acc:.0%} (last {len(recent)}: {recent_acc:.0%})"]
    if med is not None:
        parts.append(f"median {med:g}s when correct")
    if trend is not None:
        parts.append(f"{'faster' if trend < 0 else 'slower'} by {abs(trend):.0%} over time")
    if limited:
        parts.append("FLUENT" if fluent else f"not fluent yet ({streak}/{FLUENT_STREAK} in a row within limit)")
    return {"n": n, "acc": acc, "recent_acc": recent_acc, "median": med, "trend": trend,
            "fluent": fluent, "line": ", ".join(parts)}


def cmd_report(a):
    entries = read_log()
    if a.topic:
        entries = [e for e in entries if e["topic"] == slug(a.topic)]
    if a.concept:
        entries = [e for e in entries if e["concept"].lower() == a.concept.strip().lower()]
    if not entries:
        print("No practice logged yet.")
        return
    groups = {}
    for e in entries:
        groups.setdefault((e["topic"], e["concept"]), []).append(e)
    for (tp, c), es in sorted(groups.items()):
        print(f"[{tp}] {c}: {summarize(es)['line']}")


def cmd_mark(_a):
    """Hook entry point: remember when the learner last submitted an answer."""
    try:
        sys.stdin.read()  # drain hook JSON; we only need the time
    except Exception:
        pass
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        MARK.write_text(str(time.time()))
    except Exception:
        pass
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description="Time and log practice attempts.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("start")
    p.add_argument("--topic", required=True)
    p.add_argument("--concept", required=True)
    p.add_argument("--kind", choices=KINDS, required=True)
    p.add_argument("--limit", type=float, help="seconds a fluent answer fits comfortably in")
    p.set_defaults(fn=cmd_start)

    p = sub.add_parser("stop")
    p.add_argument("id")
    p.add_argument("--result", choices=RESULTS, required=True)
    p.set_defaults(fn=cmd_stop)

    p = sub.add_parser("log")
    p.add_argument("--topic", required=True)
    p.add_argument("--concept", required=True)
    p.add_argument("--kind", choices=KINDS, required=True)
    p.add_argument("--result", choices=RESULTS, required=True)
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("report")
    p.add_argument("--topic")
    p.add_argument("--concept")
    p.set_defaults(fn=cmd_report)

    p = sub.add_parser("mark")
    p.set_defaults(fn=cmd_mark)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
