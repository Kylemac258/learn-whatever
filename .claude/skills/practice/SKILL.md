---
name: practice
description: The PRACTICE stage — turn concepts the learner understands into ones they can produce reliably, fast, and durably, through retrieval, varied and interleaved problems, worked examples that fade, explain-it-back, timed fluency drills, flashcards, and printable worksheets. Use after a concept passes teach's quiz-check, when the learner says "drill me", "practice", "give me exercises", "worksheet", or "flashcards", or when a learner file shows concepts at stage `understood`.
argument-hint: "[topic] [concept]"
---

# Practice — reliable, fast, durable

Understanding a concept once doesn't mean they can produce it next week, or fast enough to use it. Practice builds three properties, in this order: **reliable** (they can produce it), **fluent** (they can produce it quickly, freeing their attention for harder things), **durable** (they still can later).

The failure mode is passive practice: re-reading, re-explaining it *to* them, recognising the right option. Producing an answer from memory beats restudying it, so in practice **they produce, you grade**. Multiple choice only when the skill really is telling confusable things apart.

Arguments: `$ARGUMENTS`. Read `learner/<topic>.md` and `learner/profile.md` first, and run `python3 .claude/practice/drill.py report --topic <slug>` to see what's been practised and how fast.

## Pick what to practise

Concepts at stage `understood` (they passed the quiz-check but haven't practised) come first, then `practising` ones that aren't fluent yet. Never practise a concept they don't understand yet — if they miss most items on it, stop and send it back to `teach`. A session is ~10–20 items over 2–5 concepts; say which ones up front.

## The ladder (per concept, climb in order)

1. **Retrieval.** They produce it from memory, in their own words or working. Formats by what the concept is:

   | Concept is a… | Item format (`--kind`) |
   |---|---|
   | fact, definition, term | `recall` — short answer, typed |
   | procedure, calculation | `solve` — work a problem (see worked examples below) |
   | idea, mechanism, "why" | `explain` — explain it as if to a smart friend who's never heard of it (Feynman) |
   | pair of confusable things | `discriminate` — which one applies here, and why (MC is fine here) |

   Climb when they're at ~85–90% on the concept.
2. **Variation and interleaving.** Same concept, changed surface: different numbers, a different framing, reversed direction ("here's the output — what was the input?"). Mix in *similar, easily confused* concepts instead of blocking one at a time; interleaving helps most exactly when items are confusable, so don't bother mixing unrelated things.
3. **Fluency** — only for things worth having fast (facts, procedures, recognitions), never for deep "why" questions. Once untimed accuracy is ~95%, run timed `speed` items with a limit a fluent answer fits in comfortably (state it). A concept is **fluent** after 2 correct-within-limit attempts in a row. A timeout means "not fluent yet", not "doesn't know"; keep the bar, try again later.
4. **Durability.** Make sure the concept has review cards (`srs.py add`, per the teach skill) so it comes back over days and weeks. For atomic facts, add `--kind recall` cards; those are the ones that can go to Anki.

### Worked examples that fade (for `solve`)

New procedures go: **full worked example** (you solve one, narrating why each step) → **completion problem** (you do most, they finish the last steps) → **faded** (they do most, you give the first step) → **independent**. Move down a rung after a correct answer, back up after a miss. Beginners learn procedures faster from studying worked examples than from solving cold; the fading hands the work over.

## Running items

One item per message: the question, nothing else (no hints, no answer). Then:

- **Timed items** — right after writing the question in your message, start the clock:
  ```bash
  python3 .claude/practice/drill.py start --topic <slug> --concept "<concept>" --kind <kind> [--limit <seconds>]
  ```
  When they answer, judge it, then call `stop` with the result as the first tool call of that turn:
  ```bash
  python3 .claude/practice/drill.py stop <id> --result correct|partial|wrong|dontknow
  ```
  A hook records the instant they submit, so your own thinking time doesn't count. (If the output says there was no answer mark, the hook isn't installed and the time runs a little long.) Report the time on speed items ("✓ 6.2s — under the 10s limit").
- **Untimed items** — after grading:
  ```bash
  python3 .claude/practice/drill.py log --topic <slug> --concept "<concept>" --kind <kind> --result <result>
  ```

**Grade immediately and tightly:** ✓ / ~ / ✗, what's missing, the correct answer or step. For `explain` items, check for the key points and for whether the *mechanism* is right, not the wording; point out gaps and jargon used without meaning.

**A miss re-enters the queue:** ask the same item (or a close variant) again 2–3 items later, and once more at the end. A miss followed by a later success is the strongest rep there is.

Follow the teach skill's **Pacing** targets (~70–85% success). All hits means make it harder; mostly misses means the concept isn't understood yet — stop practising it and send it back to `teach`.

## Worksheets (practice away from the chat)

If they want problems to do on paper or later, write `practice/<slug>-<YYYY-MM-DD>.md` (it's in the vault, so it renders in Obsidian):

```markdown
# <Topic> practice — <date>

## 1. <problem>
> [!example]- Answer
> <worked solution, with the why behind each step>
```

Collapsed callouts keep answers hidden until clicked. Order problems easy → hard, interleave concepts, include at least one "explain why" and one variation problem. When they come back with answers, grade them and log each with `drill.py log`.

## Close

Summarise in two or three lines: which concepts got more reliable, any that became **fluent** (with times), and which misses to watch. Then update `learner/<topic>.md` — each concept's **Stage** (`practising`, or `fluent` once the drill report says FLUENT or, for concepts where speed isn't the goal, after reliable success on varied items across two sessions) with the evidence — and anything notable about pacing in `learner/profile.md`.
