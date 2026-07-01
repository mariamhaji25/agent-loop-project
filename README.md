# Marketing Content Automation (Silverleaf)

A small, dependency-free toolkit that automates the repetitive parts of
running a school's marketing content calendar: turning a planned post into a
finished brief, catching scheduling gaps, and tracking what actually
performs. See [`CLAUDE.md`](CLAUDE.md) for the full purpose, rules, and
conventions, and [`docs/agent_loop.md`](docs/agent_loop.md) for the design
philosophy behind it.

All sample data in this repo (`content_calendar/calendar.csv`,
`examples/example_filled_video_script.md`) is synthetic — fake names, fake
dates — see `.claude/skills/privacy-and-compliance/SKILL.md`.

## Requirements
Python 3, standard library only. No installs needed.

## Quickstart

Generate a content brief from a calendar row:
```
python scripts/generate_content_brief.py --id 2
```

Check the calendar for gaps or missing fields:
```
python scripts/check_calendar_gaps.py --days-ahead 14
```

Log how a published post performed and get a recommendation:
```
python scripts/log_post_performance.py --date 2026-06-15 --content-type video_testimonial --platform instagram --engagement-score 8
```

## Layout
- `content_calendar/` — the CSV calendar (source of truth) and the append-only performance log
- `templates/` — placeholder content templates (video script, social post, event flyer brief)
- `examples/` — one fully filled synthetic example
- `scripts/` — the three automation scripts above
- `generated/` — script output (not committed)
- `docs/` — background on the agent-loop design
- `.claude/skills/`, `.claude/agents/` — Claude Code project skills and subagents documenting/automating this workflow
