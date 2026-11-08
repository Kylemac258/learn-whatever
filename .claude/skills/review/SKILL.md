---
name: review
description: Run a spaced-review session over due cards from past lessons (FSRS-scheduled). Use when the learner says /review, "let's review", "quiz me on what I've learned", or when the session-start notice says cards are due and they agree to review.
argument-hint: "[topic]"
---

# Review

Spaced review brings each learned idea back just before it would be forgotten. Each successful recall pushes the next one further out (days → weeks → months); each miss brings it back tomorrow. The scheduler (`srs.py`, FSRS) handles *when*; your job is to ask well, grade honestly, and repair misses fast.

Arguments: `$ARGUMENTS` (optional topic slug to restrict to).

## 1. Fetch what's due

```bash
python3 .claude/review/srs.py due            # or: due --topic <slug>
```

It returns JSON cards, **foundations first** (lowest `level` in the lesson map), then most-forgotten first: `id`, `topic`, `concept`, `kind`, `level`, `depends_on`, `prompt`, `answer` (the grading key), `recall_odds`. If nothing is due, say so in one line, show `srs.py stats`, and stop.

**Keep that order.** If a foundation has faded, questions about what's built on it give misleading answers — you'd read a broken root as a broken conclusion. Within the same level, mix topics rather than doing one topic in a block.

If more than ~15 are due, tell them the count and ask how many to do now (overdue cards keep; nothing breaks if they're done tomorrow). Take the first N in order, so foundations are never the ones deferred.

Skim `learner/<topic>.md` for each topic involved (recorded misconceptions, and in **Concepts** how each idea was originally taught), and `learner/profile.md` for what explanations work for them.

## 2. Ask — one card per message

**Never show the `answer` key before they answer** (the Obsidian log shows everything live).

- **Rephrase every time.** Ask for the card's idea in fresh words, not the stored `prompt` verbatim — the goal is recall of the idea, not of the sentence.
- **`explain`** — ask them to explain *why/how* in their own words, in chat. Free recall beats recognition, so default to this.
- **`apply`** — invent a **new** concrete case each time (different numbers, a different scenario) and ask them to work it.
- **`solve`** — a fresh short problem of the card's type (new numbers or setting), worked in chat.
- **`recall`** — a short direct question in chat; or, for something with crisp alternatives, an `AskUserQuestion` with `header: "Quiz"` (2–3 options + `I don't know`, built per the teach skill's option procedure).

Keep it brisk: the question, nothing else. LaTeX for math.

## 3. Grade and rate

Compare their answer with the key points, by meaning (not wording). Respond tightly:

- `✓` / `~` / `✗`, then the missing or wrong key point(s) in a sentence or two. On `✓`, one line confirming *why* it's right is enough.

Then rate honestly — inflating ratings just schedules forgetting:

| Rating | When |
|---|---|
| `1` Again | Wrong, blank, "I don't know", or right only after you hinted |
| `2` Hard | Got there, but missed a key point or clearly struggled |
| `3` Good | All key points, with normal effort |
| `4` Easy | All key points, instantly, and fluently — or they extended it beyond the key |

```bash
python3 .claude/review/srs.py rate <id> <1-4>
```

If they dispute a rating ("I actually knew that"), `srs.py undo <id>` and re-rate. Don't announce the next interval for every card; a summary at the end is enough.

**On a miss (`1`)**, repair it before moving on — briefly, in the teach skill's spirit: re-motivate the idea and re-connect it to what it rests on (2–5 sentences, not a new lesson).

- **Explain it differently from last time.** They've heard the original explanation and it didn't hold; repeating it louder rarely works. Check how it was taught (the topic file's evidence, or the lesson log) and reach for a different motivating problem, a different example, or a different discovery path. Prefer the kinds of explanation `learner/profile.md` says land for them.
- **Then confirm the repair** with one quick fresh question on the same idea. Don't re-rate the card — the miss stands; the scheduler will bring it back tomorrow.
- **Record it** in `learner/<topic>.md`: set that concept's status to 🟨/🟥 with the evidence, add the misconception if their answer revealed one, and note which new explanation worked (or didn't). If the new framing clearly landed, add it to **What works** in `learner/profile.md`.
- If the card itself was the problem (ambiguous, two ideas at once), fix it with `srs.py edit <id> --prompt … --answer …`.

**If the missed card is a foundation** (other cards rest on it), everything built on it is now suspect, even cards not due yet:

```bash
python3 .claude/review/srs.py dependents --topic <slug> --concept "<concept>"
python3 .claude/review/srs.py recheck <id>     # for each dependent, after the repair
```

Re-check the dependents in this same session, after the foundation is repaired — a dependent that also fails was probably failing *because of* the foundation, so one repair may fix both.

## 4. Close

One short summary: how many reviewed, how many missed and which concepts, and when the next batch is due (`srs.py stats`). If the misses cluster around one strand, suggest a short lesson on it next time and note that in the topic file's **Sessions** line.
