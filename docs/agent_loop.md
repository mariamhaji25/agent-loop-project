# Agent Loop: How an Autonomous Agent Learns and Improves

## The Loop at a Glance

```
Observe → Decide → Act → Get Feedback → Improve ↻
```

An autonomous agent does not answer once and stop. It keeps going — watching what happens, learning from results, and making better decisions each time around the loop.

---

## Example Scenario: Ayesha the Learner

### 1. Observe
The agent looks at available data and notices:
- Ayesha has **not logged in for 9 days**
- She has completed only **1 out of 4 assignments**
- Her peers at the same stage have completed 3–4 assignments

The agent identifies Ayesha as an at-risk learner who may need support.

---

### 2. Decide
Based on what it observed, the agent decides the most appropriate action is a gentle nudge — a reminder to re-engage.

---

### 3. Act
The agent recommends (and carries out):
> **"Send Ayesha a reminder email encouraging her to log back in and continue her assignments."**

---

### 4. Get Feedback
Three days pass. The agent checks the outcome:
- Ayesha still has **not logged in**
- She did **not respond** to the email
- Her assignment count remains at **1 out of 4**

The email did not work. The agent now has new information.

---

### 5. Improve — Next Recommendation
Because the first action failed, the agent updates its understanding and tries a stronger approach:

> **"The email reminder was not effective. Escalate by notifying Ayesha's course mentor to reach out with a personal message. Also, unlock a shorter 'catch-up' version of the missed assignments to lower the barrier to re-engagement."**

The agent has improved by:
- Recognising that passive reminders are not enough for Ayesha
- Choosing a more personal, human-assisted intervention
- Reducing friction so re-engagement feels easier

The loop continues — the agent will observe whether this new action works and adjust again if needed.

---

## How This Is Different from a Normal Chatbot

A normal chatbot answers a question and stops — it has no memory of what happened next and no way to find out. An autonomous agent, by contrast, stays in the loop: it watches real-world outcomes, compares them to what it expected, and changes its behaviour based on what it learns. Over many cycles, the agent gets progressively better at helping each individual learner — something a one-shot chatbot response can never do.

---

## Applying This to Marketing Content

This repo implements the same five-step loop for school-marketing content, using plain scripts instead of a live agent:

1. **Observe** → `scripts/check_calendar_gaps.py` scans the content calendar for gaps, missing fields, and past-due posts.
2. **Decide / Act** → `scripts/generate_content_brief.py` turns a calendar row into a finished content brief, ready for a human to film/write/design.
3. **Get Feedback / Improve** → `scripts/log_post_performance.py` records how a published post actually performed (manually-assigned engagement score) and recommends which content type to lean into next.

Nothing here fabricates data at any step — see `.claude/skills/privacy-and-compliance/SKILL.md` for the rules that keep this loop honest.
