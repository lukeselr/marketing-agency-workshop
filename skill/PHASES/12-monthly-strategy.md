# Phase 12 — Monthly strategy review

The "your agency presents the deck" moment, automated.

## How it runs

```bash
bash ~/.claude/skills/marketing-agency/scripts/monthly-strategy.py
```

## What it does

1. Loads last 4 weekly reports from `~/marketing/reports/`
2. Computes 30-day trend (spend, leads, CPA)
3. Schedules wedge re-evaluation via `competitive-cartographer`
4. Schedules competitor delta via `delegate-competitor-watch`
5. Schedules 70/20/10 budget rebalance via `claude-ads/skills/ads-budget`
6. Drafts 3 next-30-day bets (filled by `monthly-strategy-orchestrator` agent)
7. Renders Markdown preview + JSON deck for downstream PDF/Notion conversion

## Outputs

- `~/marketing/reports/YYYY-MM-monthly.md` (preview)
- `~/marketing/reports/YYYY-MM-monthly.json` (data)
- After delegate run: `YYYY-MM-monthly.pdf` + Notion page + 5-min narration script

## Cron

1st of month, 8am AEST.
