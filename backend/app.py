#!/usr/bin/env python3
"""Flask API + static frontend for the Silverleaf content-calendar toolkit.

Every route calls straight into scripts/ (the same functions the CLI uses)
so the web app and the CLI share one implementation of the rules in
CLAUDE.md: never fabricate a missing field, never invent an engagement
score, never delete calendar or performance-log history.
"""

import csv
import datetime
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from flask import Flask, jsonify, request, send_from_directory  # noqa: E402

from scripts import check_calendar_gaps, generate_content_brief, log_post_performance  # noqa: E402

CALENDAR_PATH = ROOT / "content_calendar" / "calendar.csv"
PERFORMANCE_LOG_PATH = ROOT / "content_calendar" / "performance_log.csv"

app = Flask(__name__, static_folder=str(ROOT / "frontend"), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/calendar")
def get_calendar():
    return jsonify(check_calendar_gaps.load_rows(CALENDAR_PATH))


@app.get("/api/gaps")
def get_gaps():
    days_ahead = int(request.args.get("days_ahead", 14))
    rows = check_calendar_gaps.load_rows(CALENDAR_PATH)
    today = datetime.date.today()
    return jsonify(
        {
            "as_of": today.isoformat(),
            "missing_fields": check_calendar_gaps.find_missing_fields(rows),
            "past_due": check_calendar_gaps.find_past_due(rows, today),
            "gaps": check_calendar_gaps.find_gaps(rows, days_ahead, today),
        }
    )


@app.post("/api/briefs/<row_id>")
def create_brief(row_id):
    row = generate_content_brief.load_row(CALENDAR_PATH, row_id=row_id)
    if row is None:
        return jsonify({"error": "no matching calendar row"}), 404

    template_name = generate_content_brief.TEMPLATE_BY_CONTENT_TYPE.get(row["content_type"])
    if not template_name:
        return jsonify({"error": f"no template mapped for content_type '{row['content_type']}'"}), 400

    template_path = ROOT / "templates" / template_name
    template_text = template_path.read_text(encoding="utf-8")
    filled = generate_content_brief.fill_template(template_text, row)

    all_placeholders = generate_content_brief.PLACEHOLDER_RE.findall(template_text)
    needs_input = sorted({f for f in all_placeholders if not row.get(f, "").strip()})

    out_dir = ROOT / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{row['target_date']}_{generate_content_brief.slugify(row['title'])}.md"
    out_path.write_text(filled, encoding="utf-8")

    return jsonify({"brief": filled, "needs_input": needs_input, "filename": out_path.name})


@app.get("/api/performance")
def get_performance():
    entries = []
    if PERFORMANCE_LOG_PATH.exists():
        with open(PERFORMANCE_LOG_PATH, newline="", encoding="utf-8") as f:
            entries = list(csv.DictReader(f))
    return jsonify({"entries": entries, "recommendation": log_post_performance.recommend()})


@app.post("/api/performance")
def add_performance():
    data = request.get_json(silent=True) or {}
    required = ["date", "content_type", "platform", "engagement_score"]
    missing = [k for k in required if not str(data.get(k, "")).strip()]
    if missing:
        return jsonify({"error": f"missing required field(s): {', '.join(missing)}"}), 400

    try:
        score = float(data["engagement_score"])
    except (TypeError, ValueError):
        return jsonify({"error": "engagement_score must be a number"}), 400
    if not (1 <= score <= 10):
        return jsonify({"error": "engagement_score must be between 1 and 10"}), 400

    try:
        datetime.date.fromisoformat(data["date"])
    except ValueError:
        return jsonify({"error": "date must be YYYY-MM-DD"}), 400

    log_post_performance.append_row(
        data["date"], data["content_type"], data["platform"], score, data.get("notes", "")
    )
    return jsonify({"ok": True, "recommendation": log_post_performance.recommend()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
