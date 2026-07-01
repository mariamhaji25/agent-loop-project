#!/usr/bin/env python3
"""Turn one content-calendar row into a filled-in content brief.

Reads a row from content_calendar/calendar.csv, picks the matching
template from templates/ (based on content_type unless --template is
given), fills {{placeholder}} fields from the row, and writes the
result to generated/. Fields the calendar row doesn't have are left as
"NEEDS INPUT: <field>" rather than invented -- see
.claude/skills/privacy-and-compliance/SKILL.md.
"""

import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_BY_CONTENT_TYPE = {
    "video_testimonial": "video_script_template.md",
    "day_in_the_life": "video_script_template.md",
    "social_post": "social_post_template.md",
    "event_flyer": "event_flyer_brief_template.md",
}
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


def load_row(calendar_path, row_id=None, target_date=None):
    with open(calendar_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row_id is not None and row["id"] == str(row_id):
                return row
            if target_date is not None and row["target_date"] == target_date:
                return row
    return None


def fill_template(template_text, row):
    def replace(match):
        field = match.group(1)
        value = row.get(field, "").strip()
        return value if value else f"NEEDS INPUT: {field}"

    return PLACEHOLDER_RE.sub(replace, template_text)


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calendar", default=str(ROOT / "content_calendar" / "calendar.csv"))
    parser.add_argument("--id", dest="row_id", help="calendar row id")
    parser.add_argument("--date", dest="target_date", help="calendar row target_date (YYYY-MM-DD)")
    parser.add_argument("--template", help="override template filename in templates/")
    parser.add_argument("--out-dir", default=str(ROOT / "generated"))
    args = parser.parse_args()

    if not args.row_id and not args.target_date:
        parser.error("pass --id or --date to select a calendar row")

    row = load_row(args.calendar, args.row_id, args.target_date)
    if row is None:
        print("No matching calendar row found.", file=sys.stderr)
        return 1

    template_name = args.template or TEMPLATE_BY_CONTENT_TYPE.get(row["content_type"])
    if not template_name:
        print(f"No template mapped for content_type '{row['content_type']}'.", file=sys.stderr)
        return 1

    template_path = ROOT / "templates" / template_name
    template_text = template_path.read_text(encoding="utf-8")
    filled = fill_template(template_text, row)

    missing = PLACEHOLDER_RE.findall(template_text)
    warnings = [f for f in missing if not row.get(f, "").strip()]
    if warnings:
        print(f"Warning: missing fields left as NEEDS INPUT: {', '.join(sorted(set(warnings)))}")

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{row['target_date']}_{slugify(row['title'])}.md"
    out_path.write_text(filled, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
