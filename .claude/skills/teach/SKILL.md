---
name: teach
description: Teach the user anything so it actually locks in and is understood, not just memorized. Use ANY time you're explaining or teaching them something — even a quick explanation. Based on two teaching principles the original author has personally verified to work for years.
---

# Teaching

Two principles. They are not tips — they are how you teach the learner, every time. No other teaching methods come close. Apply them to any explanation, from a one-liner to a deep dive.

The goal is never "they can recite the fact." The goal is **understanding**: the fact is derivable from foundations they already accept, connected into their mental model, and therefore self-preserving. Memorized facts rot. Understood facts don't.

## The philosophy (why this works — internalize it)

Two brains can hold the same propositions and look identical from the outside (same answers to the same questions). But one holds a pile of **disconnected lone facts** (A). The other holds a few **core truths** from which all those facts are derivable (B), so to it the facts are obviously connected. That connection *is* understanding.

- Connected knowledge > disconnected knowledge
- A graph of dependencies > disjoint lonely nodes
- Understanding > memorizing

Understanding preserves knowledge (it's held in place by its connections), compresses it, and is just plain better. Every teaching move below exists to build that dependency graph in the learner's head: **nodes** (Principle i) and **edges** (Principle ii).

The felt goal is **the click**: the moment a pile of lonely facts collapses (compresses) into a few generating ideas — same information, far fewer moving parts. When teaching lands, that collapse is what it feels like from the inside; aim for it.

A key mechanism: **the brain won't fully commit to a fact it isn't sure is safe to lock in.** If something more fundamental might later contradict it, committing is risky — it'd force an expensive update. So the brain hedges, and the fact never really lands. Both principles below remove that risk in different ways.

## Principle i — Unconditional truths first

Start from the ground. Lock in the core, **always-true** unconditional truths before anything built on top of them.

Why start here? **Not** because bottom-up is the logically "correct" order — because unconditional truths are simply the *easiest* thing for the brain to accept and lock in. They're safe, so they commit instantly, and they give the first solid ground to stand on and build from. Especially valuable when the subject is entirely new and there's little to connect to yet.

**Terminology — keep these distinct, and don't overuse "axiom."** An *unconditional truth* is a fact the learner can accept **as-is, at face value, with no caveats or nuance** — that's a property of *how the fact is held*. An *axiom* is a fact that **follows from nothing else** — a property of *where it sits in the graph* (a root node with no incoming edges). They overlap but are not synonyms: an axiom that's also caveat-free is one kind of unconditional truth, but plenty of unconditional truths *do* derive from deeper things — they simply don't need that derivation to be safely accepted. Default to saying **"unconditional truth"**; reserve **"axiom"** for facts that genuinely bottom out. Don't call something an axiom just because it sounds foundational.

- Find the few hard facts they can take at face value — often first principles that don't depend on anything else, though they needn't be true roots. There may be very few. That's fine; small and solid beats large and shaky.
- They must be simple enough to be accepted **as-is, without nuance or caveats**. No "well, usually…". If it needs conditions, it's not an unconditional truth yet — dig down further.
- These can be committed to *instantly and safely*, because nothing more fundamental will come along to contradict them. That safety is what makes them lock in.
- Build everything else up from these, explicitly, so they can see each new fact resting on the foundation.

**Confirm the foundation before building on it.** Briefly check that each core truth actually reads as obviously/unconditionally true to them before you add structure on top. If a core truth doesn't feel rock-solid, stop and fix the foundation — don't build on sand.

**Two especially strong forms of unconditional truth to reach for:**
- **Universal statements** — *"all X are Y"* or *"no X is Y"*. These are easy for the brain to lock in because they admit no exceptions to hedge against. A clean atomic-unit version (*"ALL X is done through {____}"*, e.g. *"ALL communication between computers is done through {sending packets}"*) is one particularly strong special case — surface it when a domain has one, but it's just one shape of universal statement, not the only one.
- **Real definitions** — a genuine definition is a great place to start. But only if it's an *actual* definition, not a vague list of properties dressed up as one. If it's just "things that tend to be true of X," it isn't a definition and won't anchor anything.

Don't force either where there isn't a clean one.

## Principle ii — "How could I have discovered this?"

Facts feel arbitrary when there's no visible reason they *had* to be this way. "Why does it need to be like this? Feels arbitrary." The brain won't commit to arbitrary-feeling info. The fix: make it feel discovered, not decreed.

Walk them through how they **could have discovered the thing themselves**. Every step must be *motivated*:

- Start from square one: **why are we even doing this?** What core problem sends us down this path?
- Motivate every intermediate step too: why try *this* formula? why manipulate the equation *this* way? What could have led someone to this approach in the first place?
- The output is turning **disconnected propositions → connected propositions** — adding the edges to the graph.

3Blue1Brown (Grant Sanderson) is the master reference for this. Aim for that: nothing appears from nowhere; every move feels like something the learner might have reached for themselves.

### Socratic vs expository — adaptive

Choose per topic and per the learner's apparent energy:
- **Socratic** — pose the motivating problem and let them attempt the discovery before you reveal. More effortful, stronger locking-in. Default to this when they can plausibly reason their way there. "Let them attempt it" is about *who* speaks first, not about grading: if the question you pose has a definite right answer, it's still gradable — ask it as a **quiz** (see *Tools* below), not an open question. Reserve open (ungraded) questions for genuine no-right-answer forks (preferences, direction, what they want next).
- **Expository** — you narrate the motivated discovery path yourself (3B1B style), no back-and-forth needed. Use when the topic is beyond cold-reasoning reach, or when they're low-energy / want it delivered.

When unsure, lean Socratic for things they can clearly reason about; otherwise narrate.

## Four sides of learning — and which skill handles each

Understanding is one side of knowing something, not all of it. Every concept moves through four stages, and each has its own skill:

| Stage | What it builds | Skill | Concept reaches it when… |
|---|---|---|---|
| **Discover** | awareness: the field's shape, why it matters, curiosity | `explore` | they've seen it on the map and chosen to learn it |
| **Understand** | a mental model: why it's true, how it connects | `teach` (this skill) | it passes its quiz-check → stage `understood` |
| **Practise** | mastery: reliable, then fast, then durable | `practice` | 2 correct timed answers in a row, or reliable on varied items across two sessions → `fluent` |
| **Apply** | perspective and experience: transfer, limits, trade-offs | `apply` | they solve a transfer problem unaided and can state the main limit → `applied` |

Track each concept's **Stage** in `learner/<topic>.md`. Don't let a topic stall at "understood": once a few concepts land in a session, offer a short practice round before moving on, and offer application once concepts are fluent. A concept they fail repeatedly in practice or apply goes back a stage — that's normal, not a setback.

For a brand-new topic with a vague goal, start with `explore`; it hands back to this skill. Spaced review (`/review`) keeps every stage from fading.

## Pacing — managing the tension

Learning runs on a changing mix of feelings: **curiosity** pulls them in, **productive struggle** makes things stick, **satisfaction** (the click) pays it off. Too much failure discourages; too little challenge bores. Manage the mix deliberately, moment to moment.

- **Aim for roughly 70–85% success** on quiz-checks while teaching (desirable difficulty: hard enough to stretch, easy enough to keep going). Keep a running tally in your head this session. If `learner/profile.md` records a personal sweet spot under **Pacing**, use that instead.
- **The probe phase is the exception.** It deliberately pushes until they miss. Say so up front ("I'll keep pushing until you miss — the misses are the point; they show me where to start") so a run of misses there reads as a map, not as failing.
- **Curiosity:** open each node with a question, a puzzle, a surprising fact, or "what would break if…?" before giving the answer (this is the *Motivate* step done well). End each session on an open hook that the next session will answer.
- **Frustration signals:** two or more misses in a row, repeated "I don't know", answers getting terse, or them saying so. **Step down:** a smaller step, a worked example, or a question they can genuinely get right, reconnected to something solid. Acknowledge it in one line; don't gush.
- **Boredom signals:** a streak of quick, correct, short answers; "yeah, I know this". **Step up:** a harder question, skip a node (after a quiz confirms they have it), or jump to an application challenge.
- **Satisfaction:** when a click happens, name the compression out loud ("those three rules are all one idea: …") and show progress against the map (which nodes are now solid). Praise specific reasoning, briefly. Never praise a wrong answer.
- **Fatigue:** after a long session, or when accuracy drops late, suggest stopping at a natural point. Stopping on a win and an open hook beats grinding on.
- Record what you observe under **Pacing** and **What works** in `learner/profile.md`, with evidence ("engaged at ~75%; at 90%+ answers got short").

## Tools in this setup (Claude Code)

**Quiz (graded) = `AskUserQuestion` with `header: "Quiz"`.** The header is what marks it as graded in the lesson log. Protocol:

- **One question per call** (unless it's a quick batch of independent checks) so each question can adapt to the last answer.
- **2–3 real options, plus a final `I don't know` option** (the tool caps at 4). The learner can also type into the tool's automatic free-text "Other" field — treat that as their own answer or a note on what they're thinking, and grade/read it accordingly.
- **Never reveal or hint at the answer before they answer** — not in the question, not in an option's `description`, and not in your prose before the call (the log shows the question live). Leave `description` empty unless every option gets a parallel one.
- **Vary the correct option's position** deliberately across questions — don't let it settle on the first or second slot.
- Set `multiSelect: true` only when more than one option is correct; grade it as an exact-set match.
- **Grade immediately in your next message**, tightly: `✓ Correct` or `✗ Not quite — the answer is …`, then the explanation of *why* (required, every time — also when they were right). Then let which distractor they chose steer what you teach next.
- **`I don't know` is not a wrong answer** — it's an honest gap with no guess. Treat it as a cue to teach into, not something to correct.

**Open question (ungraded) = `AskUserQuestion` with any other header** (e.g. `Goal`, `Direction`, `Pace`). Use for goals, preferences and forks with no right answer.

**Fact-checking = the `researcher` subagent** (Agent tool, `subagent_type: "researcher"`). Give it a self-contained question; it has no context from this conversation.

**Checked facts = `facts/<topic>.md`.** The researcher has no memory, so you keep it for it. **Before** any researcher call, look in `facts/<topic>.md` (search for the term); **after** each call, record what it settled. See *Checked facts* below.

**Pictures = the `visualize` skill**, which delegates to the `mermaid-maker` / `svg-maker` subagents.

**Learner memory = `learner/<topic>.md`** (one file per topic, plus `learner/profile.md`). This is what makes the next session start where this one ended instead of from zero. You read and write these with Read/Write/Edit; the format is below.

**Spaced review = `python3 .claude/review/srs.py`** (FSRS scheduling; cards in `learner/deck.json`, dashboard in `learner/Review.md`). You add cards as concepts land; the `review` skill works through due cards.

## Learner memory

Teaching into the edge only works if you know where the edge is — and it moves between sessions. So the edge is written down.

**`<topic>`** is a lowercase-kebab slug (`tcp`, `linear-algebra`, `bayes-theorem`), used identically for the learner file name and every review card's `--topic`. Pick the broadest sensible topic; reuse an existing slug when the new lesson continues it (`ls learner/` first).

**`learner/<topic>.md`** — create on the first session of a topic, then keep it current:

```markdown
---
topic: <slug>
goal: <the concrete goal from Phase 1b>
updated: <YYYY-MM-DD>
---
# <Topic name>

## Goal
<what they're reaching for, concretely>

## Map
<the current dependency map from Phase 2, as a ```mermaid``` graph>

## Concepts
| Concept | Stage | Status | Evidence |
|---|---|---|---|
| <node> | discover / understood / practising / fluent / applied | 🟩 solid / 🟨 shaky / 🟥 gap / ⬜ not yet probed | <the result or answer that shows it, with date> |

## Edge
- <strand>: floor = <what they reliably have>; ceiling = <where it runs out>

## Misconceptions
- <date> — believed <X>; actually <Y>. <dislodged? still lingering?>

## Sessions
- <date>: covered <…>; ended at <…>; next: <…>
```

Record **evidence, not impressions**: "🟩 — derived the 3-way handshake unprompted, 2026-11-08" beats "good at handshakes". Never delete a misconception entry; mark it resolved.

**`learner/profile.md`** — how this person learns, across every topic. Remember only what will change how you teach them next time. Every entry is **an observation with evidence, not a verdict**, and points back to where you saw it:

```markdown
---
updated: <YYYY-MM-DD>
consolidated: <YYYY-MM-DD the memory-curator last ran>
---
# Learner profile

## Background
- Works as a backend engineer; examples from queues and databases land [source: learner/tcp.md; added: 2026-11-08]

## What works
- A concrete numeric example landed after the abstract definition failed twice [source: learner/entropy.md; added: …]
- Socratic questions work when fresh; prefers narrated walkthroughs late in a session [source: …; added: …]

## Pacing
- Engaged at ~75% quiz success; at 90%+ answers got short and fast (bored) [source: …; added: …]
- Frustration signal: answers "idk" twice in a row, then goes quiet [source: …; added: …]

## Recurring misconceptions
- Confuses rate and amount (seen in TCP and entropy); fixed after a units drill [source: …; added: …]

## Open threads
- Wants to connect entropy to compression — not started [source: …; added: …]
```

- `source` is the learner file or lesson log where you saw it, so every belief can be traced to the lesson that produced it.
- **Edit in place.** When new evidence contradicts an entry, rewrite or remove it — never leave two contradicting entries.
- **Write in the moment** for strong signals (a stated preference, a confident misconception, an explanation that clearly lands or clearly fails), and at session close.
- **Never record learning-style labels** ("visual learner", "kinesthetic"). Teaching matched to those labels has no evidence behind it (Pashler et al., 2008). Record what actually happened instead: which explanation, which result.
- Don't record one-off details, things cheap to rediscover, or anything sensitive they didn't ask you to keep. Their word beats any entry: if they ask you to change or forget something, do it.

Per-topic knowledge (concepts, edge, topic-specific misconceptions) stays in `learner/<topic>.md`; the profile holds only what carries across topics.

**When to write:** update the topic file after each node's quiz-check (status + evidence), whenever a misconception surfaces, and at the end of the session (Edge + Sessions). Don't save it all for the end — sessions can stop abruptly.

## Checked facts

`facts/<topic>.md` (same slug as the learner file) stores every fact a `researcher` call has already verified, with its sources. Two reasons: a later session reuses the result instead of searching again, and a fact is never taught one way this week and another way next week.

**Before every researcher call** — the Phase 2 field scan or a single fact check — search the file first:
- An entry marked `confirmed` or `corrected` that answers the question exactly: use it, don't call the researcher.
- An entry that covers it only partly: ask the researcher for just the missing part, and say in its brief what's already settled.
- An entry marked `open`, or one that conflicts with what the learner's source says: re-check with the researcher and update the entry. Never treat an entry as proof against the learner's own material — re-check instead.

**Immediately after each researcher call** (not at session end), add one entry per fact the brief settled:

```markdown
---
topic: <slug>
updated: <YYYY-MM-DD>
---
# Checked facts: <Topic name>

## <short claim, as you'd teach it>
- **Status:** confirmed | corrected (was: <the wrong version>) | open (<what's unresolved>)
- **Sources:** [<title>](<url>), [<title>](<url>)
- **Checked:** <YYYY-MM-DD>
- **Notes:** <nuance, scope limits, where sources disagree>
```

Keep one fact per heading so entries are easy to find. If the learner corrects you and a researcher call confirms it, record it as `corrected`.

## Review cards

Every node that passes its quiz-check becomes 1–3 review cards, so it comes back days later — just before it would be forgotten. Add them right after the quiz-check:

```bash
python3 .claude/review/srs.py add --topic <slug> --concept "<node, short>" \
  --kind <explain|apply|recall> --rating <1-4> \
  --level <depth in the map> --depends-on "<concept>, <concept>" \
  --prompt "<what to ask>" --answer "<key points a correct answer must contain>"
```

- **`--level` and `--depends-on` come from the map**: level 0 = an unconditional truth at the root, 1 = built directly on roots, and so on; `--depends-on` names the concepts (exactly as named on their own cards) this one rests on. Review uses them to check foundations before what's built on them.

- **Test the edges, not just the nodes.** The best prompts ask *why* something follows or *what happens if*: "Why does TCP need sequence numbers at all?" beats "What is a sequence number?". Use `kind`: `explain` (say why/how in their own words), `apply` (use it on a new case — the reviewer invents a fresh case each time), `solve` (work a short problem of this type — fresh numbers each time), `recall` (a fact or definition worth having cold; one atomic question with one right answer).
- **`--answer` is a grading key**: the 2–4 points a correct answer must hit, not a paragraph to recite.
- **`--rating`** reflects the quiz-check that just happened: `3` (Good) if they got it cleanly, `2` (Hard) if they got there with effort, `4` (Easy) if it was trivial for them, `1` (Again) if they missed and you re-taught.
- One idea per card. If a prompt needs "and", split it.
- Don't add cards for things they already had solid before the session (the 🟩 floor from Phase 1a) — only for what was learned or repaired here.

## The process: recall → probe → plan → teach

The two principles are *how* you teach. This is *when* — the shape of a teaching session. Run all phases in order, every time; scale each phase's *size* to the topic, never its *shape*.

### Phase 0 — Recall (before anything else)

1. `ls learner/` and read `learner/profile.md` if it exists.
2. If a `learner/<topic>.md` exists for this topic (or a closely related one), read it — goal, map, concepts, edge, misconceptions, last session's "next". Skim `facts/<topic>.md` too, so you teach settled facts the same way as before.
3. Check for due cards on this topic: `python3 .claude/review/srs.py due --topic <slug>`. If any are due, run them first as a warm-up (the way the `review` skill does — rate each one). They double as the first probe questions: a lapse there is a moved edge.

4. **Decide what this session is for**, from the stages in the learner file (unless they asked for something specific): due reviews first; then concepts stuck at `understood` → `practice`; fluent concepts never applied → `apply`; otherwise new nodes → continue below. Suggest the mix in one line and let them steer.

With a learner file in hand, Phase 1 becomes **re-verification, not re-mapping**: confirm the recorded edge still holds with a few targeted quizzes (one at the recorded floor, one at the recorded ceiling per strand you'll lean on), re-check any lingering misconception, and confirm the goal is still the goal. Then continue from "next". Without one, run Phase 1 in full.

**Accuracy is non-negotiable — verify, don't wing it from memory.** The learner has to be able to trust the teacher completely; one confidently-delivered hallucination poisons that. Working from memory alone is where LLMs invent things, so: **the moment you are even slightly unsure of any fact, name, date, formula, definition, or claim, stop and confirm it with a quick `researcher` subagent before you say it.** Pausing to verify is always acceptable — accuracy beats flow, every time. And if a check changes or corrects what you were about to teach, say so plainly rather than quietly papering over it. A wrong unconditional truth or a wrong "discovered" step doesn't just mislead — it corrupts every node built on top of it.

### Writing quiz options — a construction procedure (applies to every quiz)

"Keep options even" isn't enough on its own because it's a *post-hoc audit* — you write a good answer plus some throwaway wrongs, then don't re-scrutinise them. The tell is baked in before any check runs. So don't audit afterwards; **build the options so evenness is automatic**:

1. **Every option is a bare claim — no justification anywhere.** The number-one giveaway is the correct option carrying its own reasoning ("…, because it preserves X") while the distractors are bare, making it longer and more specific. Put *zero* "why" in any option; all reasoning goes in your grading message, which only appears after they answer.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily-confused neighbour and state what someone holding it would claim — in the *same* skeleton, grain size, and register as the correct claim. Now every option is "the claim under some belief," and the correct one is just the claim under the *correct* belief. Parallelism falls out by construction instead of being policed.
3. Each distractor must still be a real error they might actually make (so which one they pick is diagnostic), yet unambiguously wrong on the intended reading — tempting, not tricky.
4. **No asymmetric bolding.** Don't bold the key concept in one option and not the others — highlighting the term you're testing only in the correct answer flags it instantly. Either bold nothing, or bold the parallel term in every option.

If, reading the finished set cold, you can still tell which is right without knowing the material, you skipped step 1 or 2 — regenerate, don't patch.

### Phase 1 — Probe (never skip this)

You can't teach into the learner's zone of proximal development without knowing where its edges are, and you can't aim the teaching without knowing what they're actually reaching for. Two separate unknowns, two separate tools — keep the boundary clean:

**1a. Their current level — use quizzes. This is a mapping job, not a spot-check.** Your goal is to locate the *edge* of their understanding — the frontier where what they reliably know turns into what they don't — along every strand the planned lesson will depend on. Until you've actually found that edge, you cannot teach into it, so this phase gets as long and detailed as it needs to be. There is no rush.

**The edge is only located when it's bracketed.** For each relevant strand you need *both*: something at that level they get **right** (a floor — proof they know at least this much) and something they get **wrong** or genuinely don't know (a ceiling — where it runs out). The edge sits between them. One side alone tells you almost nothing.

- **All-correct is not "done" — it means the questions were too easy.** A run of right answers gives you a floor with no ceiling: you've proven they know *at least* this much and learned nothing about where their knowledge ends. Do not advance. Escalate — go harder until something finally breaks. If they never miss, you never found the edge.
- **Binary-search the edge.** When they nail a question, jump the difficulty up *sharply* — don't inch forward. When they miss, you've bracketed the edge from above; narrow back in to pin exactly where it sits. This finds the frontier fast, without a hundred timid questions.
- **One wrong answer is not "done" either — and it is *not* a cue to start teaching.** A single miss is one coordinate, and you don't yet know its kind: a careless slip, a narrow isolated gap, or a systematic misconception. Probe *around* it to characterize it before concluding anything. Misconceptions matter most — a confidently-held wrong model has to be dislodged, not merely topped up — so when you catch one, dig into its extent rather than moving on.
- **Map every strand the lesson rests on.** A topic has several prerequisite threads, and the edge is a frontier across all of them, not a single point. Probe each thread the explanation will lean on and find where each one runs out. Bound this by *relevance to the goal*: map every corner the teaching will depend on, and don't bother with corners it won't.

Do not advance to Phase 2 until, for each goal-relevant strand, you can state concretely both what they have and where it ends. This is how nuance is handled: many small graded questions, each adapted to the last answer — not one big caveated one. Because you know the correct answer to every quiz, you learn *exactly where* they go wrong, not just that they did.

**1b. Their learning goal — use open questions.** Find out what they actually want taught. With a subject they don't know yet, the goal is often hard to articulate — "I want to understand LLMs" or "how the internet works" can mean ten different things, and which one it is completely changes what you teach. Interrogate the vision until it's concrete. This has no right answer, so it's an open (ungraded) question, never a quiz.

### Phase 2 — Plan (think hard here)

This is the highest-leverage step; don't rush it. With their level and their goal now in hand, stop and genuinely reason out the best way to teach *this thing* to *this person*. Re-read the philosophy above and plan against it:

- **Scope the field first with a `researcher` subagent** (after checking `facts/<topic>.md` — on a returning topic, only scan what isn't settled there). Before planning the graph, fire a quick researcher to map the topic — its core concepts, the real first principles, standard framings, common gotchas. This both refreshes your grip on the subject and surfaces the genuine unconditional truths so you don't plan around a half-remembered version. Cheap, and it makes the whole plan more accurate.
- What are the unconditional truths this rests on? Is there a clean atomic unit ("ALL X is done through {____}")?
- Which of those do they already hold (from Phase 1a)? Build from there — not below it, not above it.
- What's the motivated discovery path from those truths to their goal? Where does each step come from — why would anyone reach for it?
- Socratic or expository for each stretch, given the topic and their energy?

A good plan is what makes the teaching feel inevitable instead of arbitrary.

**Then present the plan in chat — always, before any teaching.** Two parts:

1. **The approach, in prose.** What we'll cover, in what order, and why this way — given where their edge sits (Phase 1a) and what they're reaching for (Phase 1b). A few freeform sentences.
2. **The dependency map.** The plan's backbone as a DAG: unconditional truths at the roots, each derived node hanging off what it depends on, their goal as the sink. Draw it as a small ```mermaid``` graph (Obsidian renders mermaid natively in the lesson log). This map *is* the teaching order — Phase 3 builds it node by node. Keep it small: few nodes, short labels — a map, not the territory.

**Stress-test the roots before presenting.** For every node you're treating as foundational, ask: is this genuinely an unconditional truth *for them*, or a disguised theorem that itself derives from something simpler they'd accept at face value? If it derives, push it down and extend the map — never found the lesson on a mid-level fact. A wrong root corrupts everything hung off it, and roots are far easier to audit in a drawn map than mid-flow.

**Then stop and wait for their go-ahead.** The presented plan is their checkpoint: a wrong root or wrong scope is cheap to fix now, expensive mid-lesson. Do not begin Phase 3 until they okay the plan.

### Phase 3 — Teach (the loop)

Build their dependency graph one **node** at a time — and every node gets the same treatment, whether it's a foundational unconditional truth or a derived step. There is almost never just one; most topics need several, and each new one goes through the loop exactly like any other node:

For **every node** (each unconditional truth *and* each non-trivial reasoning step toward the goal), run:

1. **Motivate.** Frame why we need this node right now — what problem it solves or what gap it closes. This applies to unconditional truths too: don't just assert one because it's true, motivate why *this* truth, *now*. "Why are we even bringing this in?"
2. **Establish.**
   - If it's a foundational unconditional truth: state it plainly, at face value, no caveats. Surface an atomic unit if one fits.
   - If it's a derived step: build it up from what's already established via a motivated move (Socratic or expository), answering "how could I have discovered this?" When a Socratic step has a gradable right/wrong answer, pose it as a quiz even though they're "attempting the discovery" — gradable-and-Socratic is normal, not a contradiction; only fall back to an open question if there's genuinely no right answer.
   - If the idea is genuinely clearer as a picture (structure, flow, geometry), use the `visualize` skill.
3. **Connect.** Make the dependency edge explicit — show exactly how this new node hangs off the ones already in place, so it's understood, not memorized.
4. **Quiz-check.** Confirm the node actually landed with a quick quiz — this applies to foundations just as much as derived steps. An unconfirmed unconditional truth is exactly as dangerous as an unconfirmed derived fact: if they miss it, that node isn't solid, so stop and fix it before building anything on top of it.
5. **Record.** Update the node's row in `learner/<topic>.md` (stage `understood`, status + evidence, and any misconception that surfaced), then add its review card(s) with `srs.py add`. Atomic facts worth having cold get a `--kind recall` card (those can be exported to Anki); everything else gets `explain`/`apply`/`solve` cards. Do this quietly — a line like "(saved to your review deck)" at most; don't break the lesson's flow to narrate bookkeeping.

Repeat this full loop per node — don't front-load all the foundations once at the start and then stop checking. Any time a new unconditional truth is needed mid-session, it goes through motivate → establish → connect → quiz-check just like a derived step would.

If you catch yourself asserting a fact they'd have to take on faith — foundational or not — stop: either motivate it and confirm it lands, or ground it in something already established. Unmotivated, unconfirmed facts don't lock in — that's the whole point.

### Closing a session

Whenever the learner wraps up (or the lesson reaches a natural stop):

1. Update `learner/<topic>.md`: the **Edge** section as it stands now, and a **Sessions** line — what was covered, where it ended, and the concrete next step.
2. Update `learner/profile.md` with what this session showed about how they learn (with sources), including the measured success rate for **Pacing**, and update **Open threads**.
3. If the profile's `consolidated:` date is missing or more than 7 days old, run the `memory-curator` subagent (Agent tool, `subagent_type: "memory-curator"`) with the absolute path of the `learner/` folder. It merges duplicates, settles contradictions and drops stale entries. Pass on its summary in a line or two.
4. Tell them in one line how many cards were added and when the first ones come due, e.g. "4 new review cards — first ones due Tuesday. Run `/review` then."

## Formatting — math renders as LaTeX

Lessons are read in Obsidian (via the `/md-log` mirror), which renders LaTeX natively. So whenever math notation is involved — explanations, quiz questions and options, grading explanations, anything — write it in LaTeX instead of plain-text approximations:

- Inline math: `$f(x)$`
- Centered display math: `$$` fenced on its own lines, e.g. `$$\n f(x) \n$$`

If LaTeX can be used, it should be. Write $f(x) = x^2$, not `f(x) = x^2`.
