# CLAUDE.md

## Purpose
This project automates the repetitive parts of running a school's marketing
content operation: turning a content-calendar entry into a ready-to-use
brief, catching scheduling gaps before they become a problem, and tracking
which content types actually perform so future planning improves over time.

## Rules — never break
- Never include a real student's name, photo, or identifying story in any
  template, example, or generated output without documented
  parental/guardian consent on file. This applies everywhere, including
  drafts. See `.claude/skills/privacy-and-compliance/SKILL.md`.
- Never invent engagement numbers, metrics, or facts. Performance data comes
  only from what a human manually logs via `scripts/log_post_performance.py`.
- Never delete calendar rows or performance-log history — the log is
  append-only.
- Always ask before publishing or sending anything outside this workspace.
- If a calendar field is missing, flag it (`NEEDS INPUT: ...`) — do not guess
  a title, date, quote, or detail.

## Where things live
- Content calendar (source of truth for what's planned) → `content_calendar/calendar.csv`
- Performance history (append-only) → `content_calendar/performance_log.csv`
- Content templates → `templates/`
- A worked, fully-synthetic example → `examples/`
- Automation scripts → `scripts/`
- Generated briefs (not committed, regenerated on demand) → `generated/`
- Background on the agent-loop design behind these scripts → `docs/agent_loop.md`

## How we work
- Write in a warm, concrete, human voice — avoid generic corporate-speak
  ("engaging content") in favor of specific moments and details.
- A finished brief should be usable by a filmer/writer/designer with no
  further clarification needed, or it should clearly say what's missing.
- Run `scripts/check_calendar_gaps.py` before planning a new week to catch
  scheduling gaps and missing fields early.
- After a piece of content goes live, log it with
  `scripts/log_post_performance.py` so the next planning cycle is informed
  by what actually worked, not guesswork.
