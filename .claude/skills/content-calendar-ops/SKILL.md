---
name: content-calendar-ops
description: Use when checking what content is due, finding scheduling gaps, or logging how a published post performed.
---

## What this does
Covers the two "operations" scripts that keep the content calendar healthy:
finding problems before they become urgent (`check_calendar_gaps.py`) and
recording what actually happened after content is published
(`log_post_performance.py`).

## Purpose of the project
Part of the Silverleaf marketing-automation toolkit — see `CLAUDE.md` for
the full project purpose and rules.

## Tech / tools
- Python 3 stdlib only (`csv`, `datetime`, `argparse`).
- `content_calendar/calendar.csv` is the source of truth for planned
  content. `content_calendar/performance_log.csv` is generated the first
  time `log_post_performance.py` runs — it doesn't exist until then.

## Conventions
- `calendar.csv` columns: `id, target_date, content_type, platform, title,
  owner, status, notes`. `status` values used so far: `planned`,
  `needs_review`, `posted`.
- `performance_log.csv` is **append-only** — rows are never edited or
  deleted, by design (`log_post_performance.py` only ever appends).
- Engagement scores are a manually-assigned 1–10 the user enters themselves
  — never scraped from an API, never fabricated. This keeps the "Improve"
  recommendation honest.
- Dates are always ISO `YYYY-MM-DD`.

## Common tasks
- Check for gaps/missing fields in the next two weeks:
  `python scripts/check_calendar_gaps.py --days-ahead 14`
- Save the gap report to a file:
  `python scripts/check_calendar_gaps.py --out generated/gap_report.md`
- Log a published post's performance:
  `python scripts/log_post_performance.py --date 2026-06-15 --content-type video_testimonial --platform instagram --engagement-score 8`
- See which content type is performing best: the recommendation prints
  automatically after every `log_post_performance.py` run.

## Gotchas
- `check_calendar_gaps.py` flags a row as past-due if `target_date` is
  before today and `status` isn't exactly `posted` — remember to update
  `status` after publishing, or it'll show up as a false problem.
- `find_gaps` compares consecutive scheduled dates from today onward — a
  calendar with only past dates will fall back to comparing all dates, which
  is a signal the calendar needs new rows added, not a bug.
- Required fields for `check_calendar_gaps.py` are `platform`,
  `content_type`, and `owner` — a blank `notes` field is fine and won't be
  flagged.
