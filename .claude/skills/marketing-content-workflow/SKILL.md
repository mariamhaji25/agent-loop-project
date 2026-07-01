---
name: marketing-content-workflow
description: Use when creating a content brief from the calendar, filling a template, or turning a planned post into something a filmer/writer/designer can execute.
---

## What this does
Turns one row of the content calendar into a finished, ready-to-use content
brief (video script, social caption, or event flyer brief), so nobody has to
start from a blank page.

## Purpose of the project
This repo automates the recurring, mechanical parts of running a school's
marketing content operation for Silverleaf: generating briefs, catching
scheduling gaps, and tracking what performs. See `CLAUDE.md` for the full
context.

## Tech / tools
- Python 3, standard library only (`csv`, `argparse`, `re`, `pathlib`) —
  no installs, no external services, no AI calls (yet — noted in the script
  docstring as a natural future extension point).
- Storage is plain files: CSV for structured data, Markdown for templates
  and output.

## Conventions
- Templates live in `templates/` and use `{{field_name}}` placeholders.
- A calendar row's `content_type` picks the template automatically
  (`video_testimonial`/`day_in_the_life` → `video_script_template.md`,
  `social_post` → `social_post_template.md`, `event_flyer` →
  `event_flyer_brief_template.md`).
- Any placeholder with no matching (non-empty) calendar field is rendered as
  literally `NEEDS INPUT: <field>` in the output — never guessed or invented.
- Generated briefs go to `generated/` (gitignored, regenerate on demand).
  `examples/example_filled_video_script.md` is the one committed, fully
  filled reference — always synthetic data.

## Common tasks
- Generate a brief for a specific calendar row:
  `python scripts/generate_content_brief.py --id 2`
- Generate a brief by date instead of id:
  `python scripts/generate_content_brief.py --date 2026-06-15`
- Force a specific template regardless of content_type:
  `python scripts/generate_content_brief.py --id 2 --template social_post_template.md`
- Add a new content type: add it to `TEMPLATE_BY_CONTENT_TYPE` in
  `scripts/generate_content_brief.py` and add a matching template file.

## Gotchas
- Never fill a template with a real student's name, photo, or identifying
  detail without documented consent — see the `privacy-and-compliance`
  skill; this is the repo's top rule.
- The script only fills fields that exist as CSV columns
  (`id, target_date, content_type, platform, title, owner, status, notes`).
  Fields like `hook_line`, `quote`, `closing_line` are intentionally NOT
  calendar columns — they always come out as `NEEDS INPUT` and are meant to
  be filled by a human, not invented by automation.
- Dates must be ISO `YYYY-MM-DD` — the scripts don't handle other formats.
