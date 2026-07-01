#!/usr/bin/env python3
"""Log how a published piece of content performed, and recommend what to
try next.

Engagement scores are manually assigned by a human (1-10) -- this script
never scrapes or fabricates metrics. This is the loop's "Get Feedback /
Improve" step -- see docs/agent_loop.md.

Log is append-only: existing rows are never modified or deleted.
"""

import argparse
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "content_calendar" / "performance_log.csv"
FIELDS = ["date", "content_type", "platform", "engagement_score", "notes"]


def append_row(date, content_type, platform, engagement_score, notes):
    is_new = not LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "date": date,
                "content_type": content_type,
                "platform": platform,
                "engagement_score": engagement_score,
                "notes": notes or "",
            }
        )


def recommend():
    if not LOG_PATH.exists():
        return "No performance history yet."

    totals = {}
    counts = {}
    with open(LOG_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            content_type = row["content_type"]
            score = float(row["engagement_score"])
            totals[content_type] = totals.get(content_type, 0.0) + score
            counts[content_type] = counts.get(content_type, 0) + 1

    averages = {ct: totals[ct] / counts[ct] for ct in totals}
    best = max(averages, key=averages.get)
    return (
        f"'{best}' has been your best-performing content type so far "
        f"(avg {averages[best]:.1f} across {counts[best]} post(s)) — "
        f"consider scheduling more of it."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD the content was posted")
    parser.add_argument("--content-type", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument(
        "--engagement-score",
        required=True,
        type=float,
        help="manually assigned 1-10 score, not scraped from any API",
    )
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    if not (1 <= args.engagement_score <= 10):
        parser.error("--engagement-score must be between 1 and 10")

    append_row(args.date, args.content_type, args.platform, args.engagement_score, args.notes)
    print(f"Logged: {args.date} {args.content_type}/{args.platform} = {args.engagement_score}")
    print(recommend())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
