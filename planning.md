# planning.md — Silverleaf Marketing Content Automation

## Goal
Give one school marketing team (currently: Mariam, acting as the whole
team) a small, low-maintenance tool that turns a content-calendar entry
into a ready-to-use brief, catches scheduling problems before they become
a crisis, and tracks which content types actually perform — without
fabricating any data along the way.

This is a **personal/small-team tool**, not a school-wide, multi-department
integration platform. (A separate, broader planning document exists at
`~/planning.md` describing a full HubSpot/Zapier-based marketing
automation program for the whole organization — that is a different,
larger initiative and is out of scope here. This document describes only
what is actually built in this repo.)

## Users
- **Marketing owner** (Mariam): plans the content calendar, generates
  briefs, hands them to a filmer/writer/designer, logs performance after
  posting.
- No other roles yet — no admin/viewer separation, no multi-user accounts.

## Core features (built)
1. **Content brief generation** — turn one calendar row into a filled
   template (video script / social post / event flyer brief), leaving
   `NEEDS INPUT: <field>` for anything the calendar doesn't have.
2. **Calendar gap checking** — flag missing required fields (platform,
   content_type, owner), past-due rows not marked `posted`, and scheduling
   gaps of N+ days.
3. **Performance logging** — append a human-assigned engagement score
   (1–10) per posted piece of content, and get a "which content type is
   working" recommendation based on the running average.
4. **Web app (this module's addition)** — a frontend so the calendar,
   gap report, and performance log can be viewed and acted on from a
   browser instead of only the CLI, backed by an API that calls the same
   underlying logic.

## Explicitly out of scope
- No live integrations to Instagram/Facebook/TikTok/Eventbrite APIs —
  content still gets posted manually; this tool only prepares briefs and
  logs outcomes a human reports.
- No database — CSV files remain the source of truth (see `decisions.md`).
- No user accounts or auth on this deployment (see `decisions.md` — known
  gap if real student data is ever involved).
- No auto-fabricated metrics or auto-filled brief fields, ever.
- No deletion of calendar rows or performance-log history.

## Data model
- `content_calendar/calendar.csv` — columns: `id, target_date,
  content_type, platform, title, owner, status, notes`.
- `content_calendar/performance_log.csv` — columns: `date, content_type,
  platform, engagement_score, notes`. Append-only.
- All sample data is synthetic (no real students) — see
  `.claude/skills/privacy-and-compliance/SKILL.md`.

## Tech stack
- **Backend:** Python, Flask, importing the existing `scripts/` modules
  directly (no logic duplication).
- **Frontend:** plain HTML/CSS/vanilla JS, no build step, served as static
  files by the same Flask process.
- **Deployment:** single web service (see `decisions.md`).

## Success criteria for this module
- Live URL loads the calendar, gap report, and performance log.
- Generating a brief from the UI produces the same output the CLI would.
- Logging a performance entry from the UI appends to the same CSV the CLI
  writes to, and updates the recommendation.
- All existing CLAUDE.md rules (no fabricated data, append-only log,
  privacy) hold in the web app exactly as they do in the CLI.
