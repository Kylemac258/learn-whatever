---
name: explore
description: The DISCOVER stage — give the learner a map of a field they don't know yet, spark curiosity, and let them choose what to learn. Use when they start a brand-new topic with a vague goal ("I want to learn about X", "where do I start with X", "what's worth knowing in X"), or ask what's next to something they know. Breadth, not depth; hands off to the teach skill.
---

# Explore — discovery and awareness

Before someone can understand an idea, they have to know it exists and why anyone cares. Discovery gives them a map of the field — its regions, the questions each answers, and which ones pull at them — and it's where curiosity starts.

The failure mode is teaching too early: diving deep into the first region before they've seen the shape of the whole. Stay wide; depth belongs to `teach`.

## Process

1. **Check memory.** `ls learner/ facts/` — if they've touched this field before, start from what's recorded instead of from zero.
2. **Scope with the `researcher`, always** (after checking `facts/<topic>.md`). Ask for a field map: the 5–9 main regions or sub-questions, the landmark ideas in each, why practitioners care, common misconceptions, and what's still open or contested. Your memory of a field's shape is exactly where confident mistakes hide. Record the scan in `facts/<topic>.md`.
3. **Open with a hook, not an outline.** A concrete puzzle, surprising fact, or everyday thing the field explains, which they can take a guess at. Ask for the guess before revealing (curiosity peaks when they can *almost* answer). Then: "this field is how you'd actually answer that."
4. **Show the map.** Each region gets one line: *the question it answers* (not its jargon name) and one hook — a surprising consequence, an application they'd recognise, or an open problem. Draw it as a small ```mermaid``` graph or mindmap; one screen at most. Say honestly which parts are settled, contested, or open.
5. **Guess, don't test.** A few quick `AskUserQuestion` quizzes (header `Quiz`), framed explicitly as guesses ("nobody's expected to know this yet — take a guess"). They're for curiosity and a rough read of what they already know, not assessment; keep the reveal light and interesting.
6. **Let them choose.** An open `AskUserQuestion` (header `Goal`): which region pulls at them, and what they want to be able to *do*. Offer the regions as options, foundational one first if one clearly underlies the others.
7. **Save and hand off.** Create `learner/<topic>.md` (format in the teach skill) with the goal in their words and the chosen region's first concepts at stage `discover`. Then load `teach` — its probe starts from here.

## Rules

- **Cap the breadth:** 5–9 regions. Twenty boxes is noise; group them.
- **Questions over names.** "How do computers agree when messages can get lost?" lands; "distributed consensus" doesn't, until it's attached to the question.
- **Re-enter any time.** Mid-topic, when they ask "what's next to this?" or finish a region, run a mini-explore around the current concept: what it unlocks, what's adjacent, where it leads.
