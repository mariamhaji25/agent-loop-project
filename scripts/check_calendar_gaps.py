#!/usr/bin/env python3
"""Scan the content calendar for scheduling gaps and missing metadata.

Flags: (a) stretches of --days-ahead or more with no scheduled post,
(b) rows missing a required field (platform, content_type, owner),
(c) rows whose target_date has already passed but status isn't 'posted'.
This is the loop's "Observe" step -- see docs/agent_loop.md.
"""

import argparse
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = ["platform", "content_type", "owner"]


def load_rows(calendar_path):
    with open(calendar_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_missing_fields(rows):
    problems = []
    for row in rows:
        missing = [field for field in REQUIRED_FIELDS if not row.get(field, "").strip()]
        if missing:
            problems.append(f"Row {row['id']} ({row['title']}): missing {', '.join(missing)}")
    return problems


def find_past_due(rows, today):
    problems = []
    for row in rows:
        target_date = datetime.date.fromisoformat(row["target_date"])
        if target_date < today and row.get("status") != "posted":
            problems.append(
                f"Row {row['id']} ({row['title']}): target_date {row['target_date']} has passed "
                f"but status is '{row.get('status')}', not 'posted'"
            )
    return problems


def find_gaps(rows, days_ahead, today):
    dates = sorted(datetime.date.fromisoformat(row["target_date"]) for row in rows)
    dates = [d for d in dates if d >= today] or dates
    problems = []
    for earlier, later in zip(dates, dates[1:]):
        gap = (later - earlier).days
        if gap >= days_ahead:
            problems.append(f"{gap}-day gap between {earlier.isoformat()} and {later.isoformat()}")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calendar", default=str(ROOT / "content_calendar" / "calendar.csv"))
    parser.add_argument("--days-ahead", type=int, default=14)
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    parser.add_argument("--out", help="also write the report to this file")
    args = parser.parse_args()

    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
    rows = load_rows(args.calendar)

    lines = ["Content Calendar Gap Report", f"(as of {today.isoformat()})", ""]

    lines.append("Missing required fields:")
    missing = find_missing_fields(rows)
    lines += [f"  - {p}" for p in missing] if missing else ["  - none"]
    lines.append("")

    lines.append("Past-due, not marked posted:")
    past_due = find_past_due(rows, today)
    lines += [f"  - {p}" for p in past_due] if past_due else ["  - none"]
    lines.append("")

    lines.append(f"Scheduling gaps of {args.days_ahead}+ days:")
    gaps = find_gaps(rows, args.days_ahead, today)
    lines += [f"  - {p}" for p in gaps] if gaps else ["  - none"]

    report = "\n".join(lines)
    print(report)

    if args.out:
        pathlib.Path(args.out).write_text(report + "\n", encoding="utf-8")
        print(f"\nSaved to {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
