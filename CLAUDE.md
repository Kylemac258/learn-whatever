# learn-whatever

This folder is a personal learning system, not a codebase, and it is also the `learn-whatever` Obsidian vault. Sessions here are lessons.

- **Whenever you explain or teach anything here — even a quick answer — load the `teach` skill first and follow it.** Recall → probe → plan → teach, every time.
- **Four stages per concept, one skill each:** `explore` (discover a new field) → `teach` (understand) → `practice` (reliable, fast, durable) → `apply` (transfer, limits, perspective). Track each concept's stage in its learner file, and don't let topics stall at "understood".
- **Learner memory lives in `learner/`** (`profile.md`, one `<topic>.md` per topic). Read it before teaching a topic; keep it updated as concepts land. The teach skill has the format. Only the `memory-curator` subagent consolidates `profile.md`; never record learning-style labels.
- **Pace deliberately**: about 70–85% quiz success while teaching; step down on frustration, step up on boredom (teach skill, *Pacing*).
- **Spaced review:** add cards with `python3 .claude/review/srs.py add …` as concepts land; when cards are due (the session-start notice says so), offer `/review`. Never edit `learner/deck.json` or `learner/Review.md` by hand; use `srs.py`.
- Graded questions are `AskUserQuestion` calls with `header: "Quiz"`; see the teach skill for the quiz protocol.
- Verify facts with the `researcher` subagent instead of answering from memory when even slightly unsure. Check `facts/<topic>.md` first, and record what each researcher call settles there right away.
- Add pictures only through the `visualize` skill (maker subagents render and check them); embed them as `![alt](viz/<filename>.png)`.
- Write math in LaTeX (`$…$`, `$$…$$`) — lessons are read rendered in Obsidian.
- The learner can mirror the session to Obsidian with `/md-log lessons/<topic>.md` (e.g. `lessons/learn-whatever.md`). Don't write lesson files yourself; the hook does it.
