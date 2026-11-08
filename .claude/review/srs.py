#!/usr/bin/env python3
"""srs.py — spaced review for learn-whatever, scheduled with FSRS-5.

Cards live in learner/deck.json. Every change also regenerates
learner/Review.md, a read-only dashboard for Obsidian.

A card is one idea the learner should be able to *use*, not a flashcard to
parrot: `prompt` says what to ask (Claude rephrases it each review),
`answer` lists the key points a correct answer must contain.

Ratings (FSRS):  1 Again · 2 Hard · 3 Good · 4 Easy

Commands:
  add    --topic T --concept C --prompt P --answer A [--kind explain|apply|recall] [--rating 1-4]
         [--level N] [--depends-on "concept A, concept B"]
  due    [--topic T] [--limit N] [--summary]      foundations (low level) first
  dependents --topic T --concept C               cards that rest on concept C
  recheck <id>                                   make a card due today
  rate   <id> <1-4>
  undo   <id>                 revert the most recent rating (e.g. the learner disputes it)
  edit   <id> [--concept C] [--prompt P] [--answer A] [--kind K]
  delete <id>
  export-anki [--topic T] [--out PATH] [--include-all]
                              recall cards → Anki TSV; they then live in Anki, not /review
  stats  [--topic T]
  list   [--topic T]
  dashboard

Set SRS_TODAY=YYYY-MM-DD to pretend it's another day (testing).
"""

import argparse
import json
import math
import os
import re
import sys
import tempfile
import uuid
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]  # <project>/.claude/review -> <project>
LEARNER = PROJECT / "learner"
DECK = LEARNER / "deck.json"
DASHBOARD = LEARNER / "Review.md"

# FSRS-5 default parameters.
W = [0.40255, 1.18385, 3.173, 15.69105, 7.1949, 0.5345, 1.4604, 0.0046, 1.54575, 0.1192,
     1.01925, 1.9395, 0.11, 0.29605, 2.2698, 0.2315, 2.9898, 0.51655, 0.6621]
DECAY = -0.5
FACTOR = 19 / 81
DESIRED_RETENTION = 0.9
MAX_INTERVAL = 3650
RATING_NAMES = {1: "Again", 2: "Hard", 3: "Good", 4: "Easy"}
KINDS = ("explain", "apply", "recall", "solve")


# ── FSRS-5 ─────────────────────────────────────────────────────────────────

def clamp_d(d):
    return min(10.0, max(1.0, d))


def init_difficulty(g):
    return clamp_d(W[4] - math.exp(W[5] * (g - 1)) + 1)


def init_stability(g):
    return max(W[g - 1], 0.1)


def retrievability(elapsed_days, s):
    return (1 + FACTOR * max(elapsed_days, 0) / s) ** DECAY


def next_interval(s):
    ivl = s / FACTOR * (DESIRED_RETENTION ** (1 / DECAY) - 1)
    return int(min(MAX_INTERVAL, max(1, round(ivl))))


def next_difficulty(d, g):
    d2 = d + (-W[6] * (g - 3)) * (10 - d) / 9          # linear damping
    return clamp_d(W[7] * init_difficulty(4) + (1 - W[7]) * d2)  # mean reversion


def stability_after_recall(d, s, r, g):
    hard = W[15] if g == 2 else 1.0
    easy = W[16] if g == 4 else 1.0
    return s * (1 + math.exp(W[8]) * (11 - d) * s ** (-W[9]) * (math.exp(W[10] * (1 - r)) - 1) * hard * easy)


def stability_after_forget(d, s, r):
    return min(s, W[11] * d ** (-W[12]) * ((s + 1) ** W[13] - 1) * math.exp(W[14] * (1 - r)))


def stability_same_day(s, g):
    return s * math.exp(W[17] * (g - 3 + W[18]))


def schedule(card, g, today):
    """Apply rating g (1-4) on `today`; mutate the card's memory state and due date."""
    card["prev"] = {k: card[k] for k in ("difficulty", "stability", "reps", "lapses", "last_review", "due")}
    if card["reps"] == 0:
        d, s = init_difficulty(g), init_stability(g)
    else:
        d, s = card["difficulty"], card["stability"]
        elapsed = (today - date.fromisoformat(card["last_review"])).days
        if elapsed < 1:
            s = stability_same_day(s, g)
        else:
            r = retrievability(elapsed, s)
            s = stability_after_forget(d, s, r) if g == 1 else stability_after_recall(d, s, r, g)
        d = next_difficulty(d, g)
    s = max(s, 0.1)
    interval = 1 if g == 1 else next_interval(s)
    card.update(
        difficulty=round(d, 4),
        stability=round(s, 4),
        reps=card["reps"] + 1,
        lapses=card["lapses"] + (1 if g == 1 and card["reps"] > 0 else 0),
        last_review=today.isoformat(),
        due=(today + timedelta(days=interval)).isoformat(),
    )
    card.setdefault("history", []).append({"date": today.isoformat(), "rating": g})
    return interval


# ── storage ────────────────────────────────────────────────────────────────

def today():
    v = os.environ.get("SRS_TODAY")
    return date.fromisoformat(v) if v else date.today()


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "general"


def load():
    if not DECK.exists():
        return {"version": 1, "cards": []}
    return json.loads(DECK.read_text(encoding="utf-8"))


def save(deck):
    LEARNER.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=LEARNER, prefix=".deck-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(deck, f, indent=1, ensure_ascii=False)
    os.replace(tmp, DECK)
    write_dashboard(deck)


def find(deck, card_id):
    for c in deck["cards"]:
        if c["id"] == card_id:
            return c
    sys.exit(f"No card with id {card_id!r}. Use `srs.py list` to see ids.")


def current_r(card, t):
    if not card.get("last_review"):
        return 0.0
    return retrievability((t - date.fromisoformat(card["last_review"])).days, card["stability"])


UNKNOWN_LEVEL = 50


def level_of(card):
    lv = card.get("level")
    return UNKNOWN_LEVEL if lv is None else lv


def due_cards(deck, t, topic=None):
    """Foundations first (lowest level in the lesson map), then most-forgotten first.

    If a root idea has faded, questions about what's built on it give misleading
    answers — so roots are always checked before their dependents.
    """
    cards = [c for c in deck["cards"] if date.fromisoformat(c["due"]) <= t and (not topic or c["topic"] == topic)
             and not c.get("in_anki")]
    return sorted(cards, key=lambda c: (level_of(c), current_r(c, t)))


# ── dashboard ──────────────────────────────────────────────────────────────

def esc(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def write_dashboard(deck):
    t = today()
    cards = deck["cards"]
    due = due_cards(deck, t)
    upcoming = {}
    for c in cards:
        dd = date.fromisoformat(c["due"])
        if not c.get("in_anki") and t < dd <= t + timedelta(days=14):
            upcoming[dd] = upcoming.get(dd, 0) + 1
    week = sum(n for dd, n in upcoming.items() if dd <= t + timedelta(days=7))

    out = [
        "# Review",
        "",
        f"*Regenerated by `srs.py` on {t.isoformat()} — don't edit by hand. Run `/review` in Claude Code to work through due cards.*",
        "",
        f"**Due now:** {len(due)} · **Next 7 days:** {week} · **Total cards:** {len(cards)}",
        "",
        "## Due now",
        "",
    ]
    if due:
        out += ["| Topic | Concept | Due since | Recall odds |", "|---|---|---|---|"]
        for c in due:
            out.append(f"| [[{c['topic']}]] | {esc(c['concept'])} | {c['due']} | {round(current_r(c, t) * 100)}% |")
    else:
        out.append("Nothing due. 🎉")
    out += ["", "## Coming up (14 days)", ""]
    if upcoming:
        out += ["| Date | Cards |", "|---|---|"]
        out += [f"| {dd.isoformat()} | {n} |" for dd, n in sorted(upcoming.items())]
    else:
        out.append("Nothing scheduled in the next two weeks.")
    out += ["", "## By topic", ""]
    topics = sorted({c["topic"] for c in cards})
    if topics:
        out += ["| Topic | Cards | Due | Solid (≥ 3 weeks) | Lapses | In Anki |", "|---|---|---|---|---|---|"]
        for tp in topics:
            tc = [c for c in cards if c["topic"] == tp]
            out.append(
                f"| [[{tp}]] | {len(tc)} | "
                f"{sum(1 for c in tc if date.fromisoformat(c['due']) <= t and not c.get('in_anki'))} | "
                f"{sum(1 for c in tc if c['stability'] >= 21)} | {sum(c['lapses'] for c in tc)} | "
                f"{sum(1 for c in tc if c.get('in_anki'))} |"
            )
    else:
        out.append("No cards yet. They're added as you finish concepts in lessons.")
    LEARNER.mkdir(parents=True, exist_ok=True)
    DASHBOARD.write_text("\n".join(out) + "\n", encoding="utf-8")


# ── commands ───────────────────────────────────────────────────────────────

def card_view(c, t):
    return {
        "id": c["id"], "topic": c["topic"], "concept": c["concept"], "kind": c["kind"], "level": c.get("level"),
        "depends_on": c.get("depends_on", []), "prompt": c["prompt"], "answer": c["answer"], "due": c["due"],
        "recall_odds": round(current_r(c, t), 2), "reviews": c["reps"], "lapses": c["lapses"],
    }


def split_list(v):
    return [x.strip() for x in (v or "").split(",") if x.strip()]


def cmd_dependents(a):
    """Cards (any due date) in a topic whose depends_on names this concept."""
    deck, t = load(), today()
    topic, concept = slug(a.topic), a.concept.strip().lower()
    hits = [c for c in deck["cards"]
            if c["topic"] == topic and concept in [d.lower() for d in c.get("depends_on", [])]]
    print(json.dumps([card_view(c, t) for c in hits], indent=1, ensure_ascii=False))


def cmd_recheck(a):
    """Pull a card's due date forward to today (e.g. its foundation just lapsed)."""
    deck, t = load(), today()
    card = find(deck, a.id)
    if date.fromisoformat(card["due"]) > t:
        card["due"] = t.isoformat()
        save(deck)
        print(f"{card['id']} ({card['concept']}) is due again today")
    else:
        print(f"{card['id']} is already due")


def cmd_add(a):
    deck, t = load(), today()
    topic = slug(a.topic)
    for c in deck["cards"]:
        if c["topic"] == topic and c["prompt"].strip().lower() == a.prompt.strip().lower():
            sys.exit(f"Duplicate: card {c['id']} already has this prompt.")
    card = {
        "id": uuid.uuid4().hex[:8], "topic": topic, "concept": a.concept.strip(), "kind": a.kind,
        "level": a.level, "depends_on": split_list(a.depends_on),
        "prompt": a.prompt.strip(), "answer": a.answer.strip(), "created": t.isoformat(),
        "difficulty": 0.0, "stability": 0.0, "reps": 0, "lapses": 0, "last_review": None, "due": t.isoformat(),
        "history": [],
    }
    ivl = schedule(card, a.rating, t)
    deck["cards"].append(card)
    save(deck)
    print(f"added {card['id']} [{topic}] {card['concept']} — first review in {ivl} day(s), on {card['due']}")


def cmd_due(a):
    deck, t = load(), today()
    cards = due_cards(deck, t, slug(a.topic) if a.topic else None)
    if a.summary:
        if cards:
            topics = sorted({c["topic"] for c in cards})
            print(f"Spaced review: {len(cards)} card(s) due today ({', '.join(topics)}). "
                  "At a natural moment, offer the learner a quick `/review` before or instead of new material.")
        return
    print(json.dumps([card_view(c, t) for c in cards[: a.limit]], indent=1, ensure_ascii=False))
    if len(cards) > a.limit:
        print(f"... {len(cards) - a.limit} more due", file=sys.stderr)


def cmd_rate(a):
    deck, t = load(), today()
    card = find(deck, a.id)
    ivl = schedule(card, a.rating, t)
    save(deck)
    print(f"{card['id']} rated {RATING_NAMES[a.rating]} — next review in {ivl} day(s), on {card['due']} "
          f"(stability {card['stability']:.1f}d, difficulty {card['difficulty']:.1f}/10)")


def cmd_undo(a):
    deck = load()
    card = find(deck, a.id)
    prev = card.pop("prev", None)
    if not prev or not card.get("history"):
        sys.exit(f"Nothing to undo for {card['id']}.")
    card.update(prev)
    undone = card["history"].pop()
    save(deck)
    print(f"{card['id']}: undid {RATING_NAMES[undone['rating']]} from {undone['date']}; due {card['due']} again")


def cmd_edit(a):
    deck = load()
    card = find(deck, a.id)
    for field in ("concept", "prompt", "answer", "kind"):
        v = getattr(a, field)
        if v:
            card[field] = v.strip()
    if a.level is not None:
        card["level"] = a.level
    if a.depends_on is not None:
        card["depends_on"] = split_list(a.depends_on)
    save(deck)
    print(f"edited {card['id']}")


def cmd_delete(a):
    deck = load()
    card = find(deck, a.id)
    deck["cards"].remove(card)
    save(deck)
    print(f"deleted {card['id']} ({card['concept']})")


def cmd_stats(a):
    deck, t = load(), today()
    cards = [c for c in deck["cards"] if not a.topic or c["topic"] == slug(a.topic)]
    if not cards:
        print("No cards.")
        return
    by_topic = {}
    for c in cards:
        by_topic.setdefault(c["topic"], []).append(c)
    for tp, tc in sorted(by_topic.items()):
        due = sum(1 for c in tc if date.fromisoformat(c["due"]) <= t)
        avg_r = sum(current_r(c, t) for c in tc) / len(tc)
        weak = sorted(tc, key=lambda c: (c["stability"], -c["lapses"]))[:3]
        print(f"{tp}: {len(tc)} cards, {due} due, avg recall odds {avg_r:.0%}, "
              f"{sum(c['lapses'] for c in tc)} lapses; weakest: " + "; ".join(c["concept"] for c in weak))


def to_anki_html(text):
    """Escape for Anki's HTML fields and convert $…$ / $$…$$ to MathJax delimiters."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", text, flags=re.S)
    text = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", r"\\(\1\\)", text)
    return text.replace("\t", " ").replace("\n", "<br>")


def cmd_export_anki(a):
    """Write an Anki-importable TSV. Recall cards are handed off to Anki (no longer
    asked in /review); explain/apply/solve cards need grading, so they're only
    exported with --include-all and stay in /review too."""
    deck, t = load(), today()
    kinds = set(KINDS) if a.include_all else {"recall"}
    cards = [c for c in deck["cards"] if c["kind"] in kinds and (not a.topic or c["topic"] == slug(a.topic))]
    if not cards:
        print("No matching cards to export.")
        return
    out = Path(a.out).expanduser() if a.out else LEARNER / "anki-export.txt"
    if not out.is_absolute():
        out = PROJECT / out
    lines = ["#separator:tab", "#html:true", "#notetype:Basic", "#guid column:1", "#deck column:2", "#tags column:5"]
    for c in cards:
        back = to_anki_html(c["answer"]) + f"<br><br><small>{to_anki_html(c['concept'])}</small>"
        lines.append("\t".join([
            f"learn-whatever-{c['id']}",
            f"learn-whatever::{c['topic']}",
            to_anki_html(c["prompt"]),
            back,
            f"learn-whatever {c['topic']} {c['kind']}",
        ]))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    handed = 0
    for c in cards:
        if c["kind"] == "recall" and not c.get("in_anki"):
            c["in_anki"] = t.isoformat()
            handed += 1
    save(deck)
    print(f"wrote {len(cards)} card(s) to {out}\n"
          f"{handed} recall card(s) now live in Anki and are skipped by /review. "
          "Import in Anki: File → Import → choose the file (re-importing updates cards by id instead of duplicating).")


def cmd_list(a):
    deck, t = load(), today()
    cards = [c for c in deck["cards"] if not a.topic or c["topic"] == slug(a.topic)]
    for c in sorted(cards, key=lambda c: (c["topic"], c["due"])):
        print(f"{c['id']}  [{c['topic']}] {c['concept']}  due {c['due']}  odds {current_r(c, t):.0%}  "
              f"reps {c['reps']} lapses {c['lapses']}")


def main():
    ap = argparse.ArgumentParser(description="FSRS spaced review for learn-whatever.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add")
    p.add_argument("--topic", required=True)
    p.add_argument("--concept", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--answer", required=True)
    p.add_argument("--kind", choices=KINDS, default="explain")
    p.add_argument("--rating", type=int, choices=[1, 2, 3, 4], default=3,
                   help="how the in-lesson quiz-check went (sets the first interval)")
    p.add_argument("--level", type=int, help="depth in the lesson map: 0 = foundation, 1 = built on it, ...")
    p.add_argument("--depends-on", help="comma-separated concepts (as named on their cards) this one rests on")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("dependents", help="cards in a topic that rest on a concept")
    p.add_argument("--topic", required=True)
    p.add_argument("--concept", required=True)
    p.set_defaults(fn=cmd_dependents)

    p = sub.add_parser("recheck", help="make a card due today")
    p.add_argument("id")
    p.set_defaults(fn=cmd_recheck)

    p = sub.add_parser("due")
    p.add_argument("--topic")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--summary", action="store_true", help="one line for session start; silent if nothing is due")
    p.set_defaults(fn=cmd_due)

    p = sub.add_parser("rate")
    p.add_argument("id")
    p.add_argument("rating", type=int, choices=[1, 2, 3, 4])
    p.set_defaults(fn=cmd_rate)

    p = sub.add_parser("undo", help="revert a card's most recent rating (once)")
    p.add_argument("id")
    p.set_defaults(fn=cmd_undo)

    p = sub.add_parser("edit")
    p.add_argument("id")
    p.add_argument("--concept")
    p.add_argument("--prompt")
    p.add_argument("--answer")
    p.add_argument("--kind", choices=KINDS)
    p.add_argument("--level", type=int)
    p.add_argument("--depends-on")
    p.set_defaults(fn=cmd_edit)

    p = sub.add_parser("delete")
    p.add_argument("id")
    p.set_defaults(fn=cmd_delete)

    p = sub.add_parser("stats")
    p.add_argument("--topic")
    p.set_defaults(fn=cmd_stats)

    p = sub.add_parser("list")
    p.add_argument("--topic")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("export-anki", help="write an Anki-importable TSV (recall cards by default)")
    p.add_argument("--topic")
    p.add_argument("--out", help="output path (default learner/anki-export.txt)")
    p.add_argument("--include-all", action="store_true", help="also export explain/apply/solve cards (they stay in /review)")
    p.set_defaults(fn=cmd_export_anki)

    p = sub.add_parser("dashboard")
    p.set_defaults(fn=lambda a: (write_dashboard(load()), print(f"wrote {DASHBOARD}")))

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
