# One-Pager: Why This Personal Bot Needed Skills, Agents, Loop & Hook

**Project:** Silverleaf Marketing Content Automation (personal bot)
**Repo:** https://github.com/mariamhaji25/agent-loop-project
**Author:** Mariam Haji

---

## What Claude created

### Skill files (4)
1. **marketing-content-workflow** — how to turn a calendar row into a finished brief
2. **content-calendar-ops** — how to check gaps and log post performance
3. **privacy-and-compliance** — non-negotiable rules for working with student data
4. **daily-wrap-up** — end-of-day notes → done/doing/next summary

### Agents (3)
1. **content-brief-generator** — runs the brief script and reports NEEDS INPUT gaps
2. **calendar-gap-checker** — runs gap check and prioritizes what needs attention
3. **performance-logger** — records engagement scores the human provides (never invents them)

### Automation layers (2)
1. **Loop** — weekday 6pm schedule that re-runs daily-wrap-up automatically
2. **Hook** — PostToolUse trigger on notes/ saves that re-runs daily-wrap-up immediately

---

## Why this project needed them

This is not a generic coding project — it is a **school marketing operation** where the same multi-step workflows repeat every week: plan content, generate briefs, catch calendar gaps, log what performed, and protect student privacy. Without skills and agents, every new AI session would re-discover CSV columns, template rules, and consent constraints from scratch.

**Skills** solve the "context amnesia" problem. They encode what the project does, which tools it uses, and the gotchas (e.g. never invent engagement scores, never commit real student names) so any assistant starts informed.

**Agents** solve the "repetitive workflow" problem. Generating a brief, checking gaps, and logging performance are three separate multi-step tasks that happen weekly — each one is a natural subagent with a fixed script and clear output.

**Loop + hook** solve the "personal bot" problem. The daily-wrap-up skill turns raw session notes into a running log. The hook fires it the moment notes are saved; the loop fires it at 6pm on weekdays. Together they give the project a memory without the human remembering to summarize.

---

## Proof each layer fired

| Layer | Evidence |
|---|---|
| Skills | Brief generated (id 2), gap found (week of 20th), performance logged (score 8) — see `notes/2026-07-09.md` |
| Agents | calendar-gap-checker re-ran cleanly — `log/2026-07-09.md` line 7 |
| Loop | CronCreate at 2026-07-09 12:18:24 EAST regenerated `log/2026-07-09.md` — see `notes/loop-hook-proof.md` |
| Hook | Notes-save triggered daily-wrap-up; hook-test line appeared in log **Doing** bucket — `log/2026-07-09.md` line 11 |

---

## The thinking takeaway

Using AI tools means asking once and getting an answer. **Thinking with AI** means building structures — skills for knowledge, agents for workflows, loops and hooks for persistence — so the system gets better at your specific work over time instead of starting over every session. For a school marketing bot handling student privacy and recurring content cycles, that structure is not optional; it is what makes the bot trustworthy and useful.
