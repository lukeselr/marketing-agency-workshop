# Quickstart video — 3-minute walkthrough script

## Section 1 — Install (45 sec)

```
git clone https://github.com/lukeselr/marketing-agency-workshop ~/marketing-agency-workshop
bash ~/marketing-agency-workshop/install.sh
```

What you see:
- Pre-flight checks (toolchain, deps, MCPs) — 3 seconds
- Python deps auto-install — 5 seconds
- 11 MCPs connect — 30 seconds (some need OAuth in browser, you do that once)
- Dashboard scaffold drops at `~/marketing/`
- "✅ Installed marketing-agency v2.0"

## Section 2 — First run (60 sec)

In Claude Code:

```
/marketing-agency
```

Paste your URL when asked. Watch:
- 14 free scrapers run in parallel (15 sec)
- 6-card business profile shown (you confirm or correct)
- 5 quick private questions (budget, bottleneck, competitors, comfort, accounts)
- Voice fingerprint extracted (3 sample sentences in your voice)

Output: your business profile + voice + 30-day plan.

## Section 3 — Day-of-week experience (75 sec)

What happens automatically once it's running:

- **Daily** — `kill-rule-monitor` watches campaigns, pauses anything bleeding
- **Mondays 7am** — weekly report at `~/marketing/reports/`
- **1st of month** — monthly strategy deck
- **Anytime new lead arrives** — instant SMS + email reply, drip starts, hot leads pinged to your Slack

You only open Claude Code if `~/marketing/tasks-for-you.md` has something.

## Section 4 — When you want more (30 sec)

Just say it in Claude Code:
- "Make new ads" → delegate-creative generates 30+ voice-graded variants
- "Build landing page for X" → delegate-landing-page → host-aware build
- "Show me competitor changes" → delegate-competitor-watch
- "Find me 50 leads matching ICP" → delegate-lead-research

That's it. The dashboard updates. You approve the activations.
