---
name: apply
description: The APPLY stage — make knowledge transfer to unfamiliar problems and give it perspective: transfer problems that don't name the idea needed, real cases (researched, never invented), where the idea breaks, its history and trade-offs, and small things to build or teach. Use when concepts are fluent or solid, or when the learner asks "how is this used", "when would I use this", "what are the trade-offs", or wants a project, case study, or real-world problem.
argument-hint: "[topic] [concept]"
---

# Apply — transfer, perspective, experience

Knowing an idea in the setting it was taught is not the same as recognising when it applies out in the world, where nothing arrives labelled with the chapter it belongs to. Application builds that: transfer to unfamiliar surfaces, a sense of where the idea stops working, and enough perspective to weigh it against alternatives.

The failure mode is "application" that's really more practice: the same problem with new numbers, or a question that names the technique it wants. **Real application hides which idea is needed; spotting it is half the skill.**

Arguments: `$ARGUMENTS`. Read `learner/<topic>.md` (pick concepts at stage `fluent`, or `practising` ones that are reliable) and `learner/profile.md` (**Background** — their work and interests make the best application settings).

## Modes — pick by the concept and their goal

1. **Transfer problem.** An unfamiliar surface with the same deep structure. Don't name the concept. Grade *recognition* (did they spot which idea applies, and why?) and the reasoning, not only the final answer.
2. **Real case.** A real system, incident, product, paper or event, analysed through the idea — ideally from their own work or interests (ask with an open `AskUserQuestion`: "where might you run into this?"). **Get cases from the `researcher`** (checking `facts/<topic>.md` first) and record them there; never invent "real" examples. Anything hypothetical is labelled hypothetical.
3. **Boundaries.** Where does it break? What does it assume? When is the usual rule false? Have them find the edge first, then fill in what they missed.
4. **Perspective.** What problem drove its invention, what came before, what it replaced; the alternatives and their trade-offs; how different fields see it. This is where an isolated concept joins the wider map.
5. **Create.** Something small to build, design, estimate or decide using the idea; or teach it back to an imagined beginner. Producing something new is the strongest test of understanding. For a larger piece of work, write a brief to `practice/<slug>-project-<date>.md` with the goal, constraints, milestones and how they'll know it works, then check in on it in later sessions.

Mix modes across a session; one transfer problem plus one real case or boundary question per concept is a good default.

## Grading

- Open-ended answers get **0 / ½ / 1** against a rubric written *for the reasoning*: did they recognise the right idea, state its assumptions, notice its limits, reach a defensible conclusion? Write the rubric before they answer (privately — don't show it).
- Give feedback on the reasoning first, then the answer. Show a model answer only after they've tried.
- Log every item: `python3 .claude/practice/drill.py log --topic <slug> --concept "<concept>" --kind transfer|case|boundary|create --result correct|partial|wrong|dontknow`.
- Transfer is hard; more misses are normal here than in practice, and the teach skill's **Pacing** still applies over a session. If transfer keeps failing on one concept, the gap is usually upstream: check with one quick retrieval question, and if that fails too, send the concept back to `practice` or `teach`.

## Close

- A concept reaches stage **`applied`** when they've solved a transfer problem unaided *and* can state the idea's main limit. Update its row in `learner/<topic>.md` with the evidence and what they applied it to.
- Add 1–2 review cards with `--kind apply` (prompt: the deep structure, not this specific case — the reviewer will invent a fresh case each time).
- End with the map: one line on how this connects back — what the idea rests on and what it unlocks next. Note new **Open threads** in `learner/profile.md` if an application raised one.
