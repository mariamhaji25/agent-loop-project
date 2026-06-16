# CLAUDE.md

## Purpose
This project automates the generation of business reports and summaries.
The agent reads raw data or notes and turns them into clean, professional reports
ready to share with a manager, team, or client — with no extra editing needed.

## Rules — never break
- Never invent numbers, statistics, or facts. If data is missing, say so.
- Never delete source files or raw input data.
- Always ask before sending or sharing any report outside this workspace.
- Do not include personal or confidential employee information in any output.
- If something is unclear in the source data, flag it — do not guess.

## Where things live
- Raw data and input notes → /inputs folder
- Finished reports → /outputs folder
- Report templates → /templates folder
- Past examples of good reports → /examples folder

## How we work
- Write in clear, professional English. Short sentences. No jargon.
- Every report must have: a one-line summary at the top, key findings in bullets, and a short conclusion.
- Use numbers and specifics wherever possible — "sales rose 12%" not "sales improved."
- Tone is formal but human — avoid stiff corporate language.
- If the report is longer than one page, add a table of contents.
- Flag anything unusual or worth the reader's attention in a "Notes" section at the end.
- When in doubt, keep it shorter. A tight half-page beats a padded two-page report.
