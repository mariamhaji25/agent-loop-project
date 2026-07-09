---
name: daily-wrap-up
description: Use at the end of a work session (or on a schedule/hook) to turn today's raw notes into a short dated done/doing/next summary in the log.
---

## What this does
Reads today's file in `notes/` and distills it into a short, dated
done/doing/next summary appended to `log/`, so there's a running record of
what actually happened each day without re-reading the raw notes later.

## Purpose of the project
Part of the Silverleaf marketing-automation toolkit — see `CLAUDE.md` for
the full project purpose and rules. This skill is the "personal bot" layer:
it doesn't touch the content calendar itself, just summarizes the day's
work on it.

## When to use it
- At the end of a work session, to close the day out.
- On the 6pm-weekday schedule (see the loop set up for this skill).
- Whenever a notes file is saved (see the hook set up for this skill).
- Never on a day with no notes file — there's nothing to summarize, so skip
  it rather than inventing one.

## Steps
1. Find today's notes file: `notes/YYYY-MM-DD.md` for today's date. If it
   doesn't exist, stop — nothing to summarize.
2. Read the file and sort its content into three buckets:
   - **Done** — things completed today.
   - **Doing** — things in progress, started but not finished.
   - **Next** — things planned but not yet started.
3. Keep each bullet short (one line) and concrete — carry over specifics
   (IDs, dates, names of scripts) from the notes rather than vague
   paraphrases like "worked on content."
4. Don't invent anything not present in the notes. If a note is ambiguous
   about which bucket it belongs in, use judgment but don't fabricate detail.
5. Write the summary to `log/YYYY-MM-DD.md` (create `log/` if it doesn't
   exist), headed by the date. If a log file for today already exists,
   overwrite it — the notes file is the source of truth, not the log.

## Example
Given `notes/2026-07-09.md` containing raw notes about a finished content
brief, a calendar gap found, a logged performance score, an unfilled gap,
a planned flyer brief, and a pending privacy check —

`log/2026-07-09.md` becomes:

```markdown
# Daily Wrap-Up — 2026-07-09

**Done**
- Finished and sent the video testimonial content brief (id 2) to the filmer.
- Logged performance for the June 15 Instagram post (engagement score 8).

**Doing**
- Investigating the calendar gap in the week of the 20th.
- Privacy-and-compliance check pending on two new example photos in `examples/`.

**Next**
- Fill the July 20 gap, likely with an open-house social post.
- Draft the event flyer brief for the open house once the gap slot is confirmed.
```

## Gotchas
- `notes/` and `log/` are both plain markdown, one file per day, `YYYY-MM-DD.md`
  — no other naming scheme.
- This skill only reads/summarizes — it never edits `content_calendar/` or
  runs the automation scripts itself.
