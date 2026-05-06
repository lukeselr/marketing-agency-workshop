---
name: monthly-strategy-orchestrator
description: Runs the Phase 12 monthly strategy review — compresses last 4 weekly reports into a 1-page deck, re-evaluates the wedge, refreshes competitor delta, recommends budget rebalance, and ranks next 30-day playbook.
---

## When to invoke
Cron 1st of month, 8am AEST. Manual fire: `bash scripts/monthly-strategy.py`.

## Context to pull
- Last 4 weekly reports from `.state/reports/YYYY-WW.html`
- `.state/business-baseline.md` + `.state/answers.json`
- `.state/connector-plan.json`
- 30-days-ago snapshot of competitor data (auto-stored by `delegate-competitor-watch`)

## Delegation
1. Trend the last 4 weeks: spend, leads, CPA, ROAS, frequency, CTR-decay.
2. Wedge re-evaluation: `competitive-cartographer` re-run vs the 2 alternatives picked in Phase 2. Did the chosen wedge perform?
3. Competitor delta: `apify-competitor-intelligence` + `claude-ads/skills/ads-competitor`. What changed vs 30 days ago in their ad library, pricing, positioning?
4. Budget rebalance: `claude-ads/skills/ads-budget` 70/20/10 framework. Where to push.
5. Next 30-day playbook: 3 wedge bets ranked by expected lift.

## Output contract
- `.state/strategy/YYYY-MM.pdf` (rendered via `pdf` skill)
- 5-min auto-narration script `.state/strategy/YYYY-MM-narration.md` for Loom/Tella
- Notion page (parented under "Marketing > Monthly Strategy")
- `~/marketing/strategy/this-month.md` symlink update
- Telegram drop: 3-line TL;DR + link

## Firewall
Same as weekly: voice-grade + 6-rule firewall on every owner-facing string.

## Read back
Owner reviews. If they accept the playbook, set `.state/strategy/YYYY-MM-accepted.json` so Phase 8 (launch) and Phase 11 (calendar) pick up the new bets next week.
