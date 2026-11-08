# learn-whatever

A personal learning system for Claude Code + Obsidian. This folder is both the Claude Code project and the Obsidian vault.

It's a Claude Code port of Amos Blomqvist's AI learning system
([amosblomqvist/learn](https://github.com/amosblomqvist/learn), from the video
[How I Use AI to Learn Things](https://www.youtube.com/watch?v=kzcI5F4tGiU)).
The original is a configuration for the *pi* agent; the teaching method is his,
the plumbing here is rebuilt for Claude Code.

## What's in it

| Piece | Where | What it does |
|---|---|---|
| `teach` skill | `.claude/skills/teach/` | The method: unconditional truths first, "how could I have discovered this?", and the recall → probe → plan → teach loop. |
| `explore` skill | `.claude/skills/explore/` | Discover: a map of a new field, framed as questions, with hooks and guesses, so you can choose what to learn. |
| `practice` skill | `.claude/skills/practice/` | Practise: recall, worked examples that fade, explain-it-back, mixed problem sets, timed fluency drills, printable worksheets. |
| `apply` skill | `.claude/skills/apply/` | Apply: transfer problems that don't say which idea to use, real (researched) cases, where the idea breaks, trade-offs, small projects. |
| Drill log | `.claude/practice/drill.py` | Times and logs every practice item in `learner/practice.jsonl`; reports accuracy, speed, speed-up over time, and fluency. |
| `/review` skill | `.claude/skills/review/` | Spaced review of past lessons: re-asks each due idea in fresh words, grades it, and reschedules it. |
| Learner memory | `learner/<topic>.md`, `learner/profile.md` | Per topic: what you've mastered, where your edge is, misconceptions seen, what's next. Across topics: what explanations work for you, your pace, recurring misconceptions, open threads. |
| `memory-curator` | `.claude/agents/` | Weekly tidy-up of `profile.md`: merges duplicates, settles contradictions, drops stale entries, spots patterns across topics. |
| Checked facts | `facts/<topic>.md` | Every fact the researcher has verified, with sources, so it's reused instead of re-searched and taught the same way each time. |
| Review scheduler | `.claude/review/srs.py` | FSRS-5 spaced repetition (the algorithm modern Anki uses). Cards in `learner/deck.json`; dashboard in `learner/Review.md`. |
| `visualize` skill | `.claude/skills/visualize/` | Adds one correct, minimal diagram to a lesson when a picture beats words. |
| `/md-log` skill | `.claude/skills/md-log/` | Mirrors the session into a markdown file you read in Obsidian (LaTeX, mermaid, images render). |
| `researcher` | `.claude/agents/` | Web-searches to verify facts before they're taught. |
| `mermaid-maker`, `svg-maker` | `.claude/agents/` | Draw a diagram, render it to PNG, *look at it*, fix it, publish to `viz/`. |
| Renderer | `.claude/visual-tools/render.py` | Mermaid/SVG → PNG using headless Google Chrome + a vendored `mermaid.min.js`. No Node needed. |
| Log hook | `.claude/md-log/md_log.py` | Appends your prompts, Claude's prose, quiz questions and your answers to the linked file. |

How the original's pi-only parts map over:

- **`quiz` tool → `AskUserQuestion` with header `Quiz`.** Claude grades your answer in its next message (✓/✗, the right answer, why). Each quiz has an "I don't know" option, and you can type a note in the "Other" box.
- **`ask_user_question` → `AskUserQuestion`** with any other header, for goals and preferences.
- **pi subagents → Claude Code subagents** (`.claude/agents/*.md`).
- **`md-log` extension → hooks** that read the session transcript and append new parts to your file.

## Setup (one time)

0. **Get it.** Clone it wherever you keep projects:

   ```bash
   git clone https://github.com/Kylemac258/learn-whatever.git
   cd learn-whatever
   ```

   Your personal learning data (`learner/`, `lessons/`, `facts/`, `practice/`, `viz/`) is gitignored, so it stays on your machine even if you commit and push changes to the system itself.

1. **Install the hooks and permissions.** Claude can't edit its own settings, so copy the prepared file into place yourself:

   ```bash
   cp setup/claude-settings.json .claude/settings.json
   ```

   This turns on the md-log hooks, a session-start check that tells Claude when review cards are due, and a hook that records exactly when you answer timed drills. It also pre-approves the render, log, review and drill scripts, edits inside `learner/`, `facts/` and `practice/`, and web search/fetch (for the researcher). Without it, everything still works except the Obsidian log and the due-cards notice, and you'll get more permission prompts. If you copied an earlier version, copy it again.

2. **Open the `learn-whatever` vault in Obsidian.** The folder already has its `.obsidian/` config. If it isn't in your vault list yet, use *Open folder as vault* → `~/Projects/learn-whatever`. Lessons go in `lessons/`, pictures in `viz/`. Obsidian hides `.claude/`, and the vault config also hides `setup/`.

3. **Requirements:** Google Chrome (for rendering diagrams) and `python3` (built into macOS). Nothing to install.

## Using it

Start a **new** Claude Code session in this folder (skills, agents and hooks load at session start), then:

```
/md-log lessons/learn-whatever.md
I want to understand how TCP makes an unreliable network reliable.
```

Open `lessons/learn-whatever.md` in Obsidian (name each lesson file after its topic) and read along. Claude will probe what you know with quizzes, ask what you're aiming for, propose a plan with a dependency map, wait for your OK, then teach concept by concept. Each concept ends with a quiz. `/md-log off` stops logging.

### Memory and review

- **Between sessions**, Claude keeps `learner/<topic>.md` up to date: your goal, the lesson map, each concept's status (🟩 solid, 🟨 shaky, 🟥 gap) with the evidence, where your edge is, misconceptions it has seen, and what's next. Next time you pick a topic up, Claude reads it, briefly re-checks the edge, and continues instead of starting over. The files are plain markdown in the vault, so you can read them and correct them.
- **After each concept lands**, Claude adds 1–3 review cards. Cards test *why* and *what if*, not definitions.
- **When cards are due**, Claude mentions it at the start of a session. Run `/review` (or `/review tcp` for one topic). Each idea is re-asked in fresh words, you answer in your own words, and Claude grades it against the key points and reschedules it. Ideas you know move out to weeks and months; misses come back tomorrow, get a quick repair, and are noted in your learner file.
- **Review checks foundations first.** Each card knows its place in the lesson map. If a foundation has faded, Claude repairs it, then re-checks everything built on it in the same session. A missed idea is re-explained *differently* from the first time.
- **`learner/Review.md`** shows what's due and coming up, and per-topic progress.
### Four stages: discover → understand → practise → apply

Each concept moves through four stages, tracked in its learner file. `explore` maps a new field so you can choose where to go. `teach` builds understanding. `practice` makes it reliable, then fast (timed drills; a concept is "fluent" after two correct answers in a row under the time limit), then durable (review cards). `apply` checks you can use it on problems that don't say which idea to use. Claude suggests what a session should focus on based on where your concepts are, and you can always ask directly: "drill me on X", "give me a worksheet", "how is this used in practice?".

**Anki:** `python3 .claude/review/srs.py export-anki` writes your fact cards (`recall` kind) to `learner/anki-export.txt` for Anki's *File → Import*. They then live in Anki (good for phone review) and stop coming up in `/review`. Re-exporting updates existing cards instead of duplicating them. The "explain"/"apply" cards stay in `/review`, because they need Claude to grade your answer.

- **Pacing:** Claude aims for roughly 70–85% quiz success while teaching. It steps down when you're struggling, steps up when it's too easy, and learns your personal sweet spot over time.

Ideas borrowed from forks of the original: foundations-first review and re-explaining differently ([ChristopherGoodale/adversarial_learning_system](https://github.com/ChristopherGoodale/adversarial_learning_system)), the checked-facts store ([TonyPansera/learning_model](https://github.com/TonyPansera/learning_model)), and evidence-linked learner memory with a curator ([darkhanakh/learn](https://github.com/darkhanakh/learn)).

## Making it yours

The `teach` skill was originally written by one learner for their own use. Edit `.claude/skills/teach/SKILL.md` to match how you learn: pacing, how hard to push in the probe phase, Socratic vs. narrated.

Note: the upstream repo has no license file; it's shared publicly "as-is" for personal use. Keep that in mind before redistributing this port.
