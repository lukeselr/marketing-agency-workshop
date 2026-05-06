# Phase 11 — Organic content calendar

Repurposes paid-ad winners into 30 organic posts/month across LinkedIn / IG / FB / TikTok / X.

## How it runs

```bash
bash ~/.claude/skills/marketing-agency/scripts/build-calendar.py
```

## What it does

1. Pulls top 3 paid winners from latest Phase 9.5 weekly report
2. Builds 30-day calendar with rotation across 6 format-platform combos
3. Drops human-readable preview in `~/marketing/calendar/this-month.md`
4. Writes deploy plan in `.state/content-calendar.json`
5. Hand-off to `delegate-organic-calendar` agent for actual copy + carousel generation + Notion push + optional auto-publish

## Format mix (rotating)

| Platform | Format |
|---|---|
| LinkedIn | thought-leader-post |
| Instagram | carousel |
| Instagram | reel-script |
| Facebook | post |
| Twitter/X | thread |
| TikTok | video-script |

## Auto-publish

Optional. Owner opts in per platform:
- IG: `instagram-automation`
- LinkedIn: `linkedin-automation`
- IG DMs: `manychat`

## Cron

Monthly (1st of month, after Phase 12 monthly strategy completes). Re-runs throughout the month as new weekly winners surface.
