---
name: md-log
description: Mirror this session into a markdown file (for reading the lesson rendered in Obsidian). Usage /md-log <path.md> to link, /md-log off to stop.
argument-hint: "<path.md> | off"
disable-model-invocation: true
---

The user wants to link this session to a markdown log. Arguments: `$ARGUMENTS`

- If the arguments are `off`, `stop` or `unlink`, run exactly:
  `python3 .claude/md-log/md_log.py unlink`
- If the arguments are empty, pick `lessons/<short-kebab-topic-or-date>.md` (use today's date, e.g. `lessons/2026-11-07.md`, if there's no topic yet) and use that as the path.
- Otherwise run exactly (quote the path):
  `python3 .claude/md-log/md_log.py link "<path>"`

Run it from the project root as a single Bash command with nothing chained onto it — a hook watches for this exact command to bind the file to this session and backfill everything said so far.

Then reply in one line with the linked file's path (or that logging stopped). Do not write to the file yourself; the hook appends prose, quiz questions and answers as the session goes.
