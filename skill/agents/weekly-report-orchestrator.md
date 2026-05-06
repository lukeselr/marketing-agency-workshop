---
name: weekly-report-orchestrator
description: Runs the Phase 9.5 weekly client report — pulls Meta / Google / LinkedIn / GHL / GA4, compresses last-week numbers + winners + kills + audience health + creative fatigue + pipeline + next-week plan into one HTML page + Telegram + Notion drop.
---

## When to invoke
Cron Mondays 7am AEST (deployed by Phase 9). Manual fire: `bash scripts/weekly-report.py`.

## Context to pull
- `.state/connector-plan.json` — which platforms are live
- `~/.marketing-agency/tokens/*.json` — credentials (mode 600, never logged)
- Last 7 + previous 7 days from each ads MCP
- GHL pipeline snapshot via `mcp__ghl-community__*` (leads → MQL → SQL counts)
- GA4 sessions + conversions if `google-analytics` token present
- `kill-rule-monitor` state for things paused this week

## Delegation
1. Numbers: query each ads MCP for `get_campaign_performance` last-7d + previous-7d.
2. Winners (3): pick top stat-sig deltas by ROAS.
3. Killed: read `.state/kill-log.json` for the week.
4. Audience health: call `claude-ads/skills/ads-audit` for pixel-event firing + LAL freshness + frequency.
5. Creative fatigue: `claude-ads/skills/ads-creative` CTR-decline curve.
6. Pipeline: GHL contact counts by tag/status.
7. Next-week plan (3 actions): `claude-ads/skills/ads-plan` template seeded with this-week deltas.

## Output contract
- `.state/reports/YYYY-WW.html` — printable, embeddable
- Telegram message via `~/.claude/skills/marketing-agency/shared/progress-streamer.sh` (link + 3-line TL;DR)
- Notion page via `notion-automation` skill, parented under owner's "Marketing" page
- `~/marketing/this-week.md` updated with the same numbers

## Firewall
Every owner-facing string passes through `shared/voice-grade-config.json`:
- Strip em dashes
- Block refund / outcome-guarantee / drop-in / personal-finance language
- Sentence-length cap from `voice-fingerprint.json`

## Read back
Used by Phase 12 monthly strategy (last 4 weekly reports → 1 deck).
