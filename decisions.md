# decisions.md

Reconstructed from git history and CLAUDE.md — the calls made on this project and why.

---

## Stdlib-only Python scripts instead of a no-code stack (Zapier/Make/HubSpot)
This is a single-person tool for one school's marketing operation, not a
multi-department integration project. A no-code SaaS stack adds accounts,
free-tier limits, and vendor lock-in for a job three small scripts already
do. **Why:** lowest possible operating cost and no external dependency to
break. **Applies to:** any future feature — prefer a local script over a new
SaaS integration unless the school genuinely needs cross-platform sync.

## CSV as the source of truth, not a database
`content_calendar/calendar.csv` and `content_calendar/performance_log.csv`
are plain, human-editable files instead of a database. **Why:** anyone on
the team can open and edit the calendar in a spreadsheet app without
learning a new tool, and there's no server/infra to maintain for a dataset
this small. **Applies to:** keep the calendar as the row-level source of
truth even after the web app exists — the app reads/writes the same CSVs,
it doesn't replace them.

## Performance log is append-only
`log_post_performance.py` never edits or deletes existing rows. **Why:**
it's a historical record used to recommend future content types; silently
rewriting history would undermine the "what actually worked" signal.
**Applies to:** the backend API must not expose any delete/edit endpoint
for performance-log rows — only append.

## Never invent missing calendar fields or fabricate metrics
`generate_content_brief.py` writes `NEEDS INPUT: <field>` rather than
guessing a title, quote, or date; `log_post_performance.py` only accepts a
human-assigned 1–10 engagement score, never a scraped or estimated one.
**Why:** a wrong guess in a brief goes straight to a filmer/writer/designer
and can produce real, published content based on a hallucination; a
fabricated engagement score corrupts the one feedback signal the loop
relies on. **Applies to:** the same rule holds in the web UI — a brief with
gaps must show them as gaps, not silently fill them in; the performance
form must reject scores outside 1–10 and must not offer an "auto-fill"
option.

## Real student data is never allowed in this repo or its output
Only synthetic names/dates are used anywhere (`content_calendar/calendar.csv`,
`examples/`), per `.claude/skills/privacy-and-compliance/SKILL.md`. **Why:**
protects students who can't consent, and keeps the repo safe to make
public. **Applies to:** before adding new sample rows or deploying, confirm
no real student is named anywhere in the data being shipped.

## Repurposed the repo from a generic "business report generator" placeholder
The original `agent_loop.md`/`CLAUDE.md` were a stand-in for an
unspecified report-automation idea; commit `26f0c2f` replaced that with the
concrete Silverleaf content-calendar toolkit. **Why:** a concrete, real
workflow (the school's actual content calendar) is more useful to build
skills/agents around than a hypothetical one. **Applies to:** treat the
Silverleaf marketing-content scope as final unless a new, equally concrete
use case replaces it.

## Skills vs. agents split
Fixed, no-judgment procedures became **skills** (`marketing-content-workflow`,
`content-calendar-ops`, `privacy-and-compliance`, `daily-wrap-up`). Tasks
that chain a script and then report/prioritize became **agents**
(`content-brief-generator`, `calendar-gap-checker`, `performance-logger`).
**Why:** same test used elsewhere in this line of work — "same steps every
time" is a skill, "runs a step and then makes a judgment call about what to
report" is an agent. **Applies to:** any new repeated task — sort it with
this same test before deciding where it goes.

## Daily Wrap-Up loop + hook for cross-session memory
A weekday-6pm scheduled run and a `PostToolUse` hook on notes/ saves both
re-trigger `daily-wrap-up`. **Why:** a personal bot loses everything between
sessions unless something writes down what happened; automating that removes
the need to remember to summarize. **Applies to:** keep both trigger paths —
the hook catches ad hoc work, the loop catches days with no notes activity.

---

## Deployment-specific decisions (this module)

## Backend imports the existing scripts as modules, doesn't shell out or duplicate logic
`backend/app.py` does `from scripts import generate_content_brief, ...` and
calls the same functions the CLI uses (`load_row`, `fill_template`,
`find_gaps`, `append_row`, `recommend`). **Why:** the CLI scripts remain the
single source of truth for the domain logic; the web app is just another
caller, so a bug fix or rule change only needs to happen once. **Applies
to:** any new API route should call into `scripts/`, not reimplement its
logic.

## Plain HTML/CSS/vanilla JS frontend, no build step or framework
No React/bundler — one `index.html`, one `app.js`, one `style.css`,
served as static files by the same Flask app. **Why:** consistent with the
project's existing "no dependencies beyond the standard library" stance,
and it means there's nothing to build before deploying — the whole app is
one process. **Applies to:** keep the frontend framework-free unless the UI
genuinely outgrows this (routing, complex state) — this project's scope
doesn't.

## Single Flask service (API + static frontend together), deployed to Render
Rather than splitting frontend (Vercel) and backend (Railway) into two
deployments, one Flask app serves both. **Why:** avoids CORS configuration
and two separate deploy pipelines for what is a small, single-user
internal tool. **Applies to:** revisit only if the frontend needs to scale
independently (CDN caching, a separate team owning it) — not the case here.

## No authentication on the write endpoints for this deployment
`POST /api/briefs/<id>` and `POST /api/performance` are open once the app
is live. **Why accepted:** all data in this repo is synthetic (see the
privacy rule above), so a stranger writing a junk row is low-stakes for
this assessment deployment. **Known gap:** if this tool ever holds real
school data, it needs auth (even a single shared password) before the
write endpoints go on a public URL — do not skip that step at that point.
