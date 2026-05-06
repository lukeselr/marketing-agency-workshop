# Phase 9 — Monitor + Optimize

`scripts/kill-rule-monitor.py` runs daily.

## Deployment modes (auto-pick)

- **AWS server** (operators with their own EC2) — cron entry on the operator's host
- **macOS launchd** (attendees on Mac) — `~/Library/LaunchAgents/com.marketing-agency.plist`
- **Anthropic Routine** (attendees no-server) — daily cloud cron via `/schedule` skill

## Kill rules

Read from `shared/conversion-events.json`:
- CPA > 3x target -> pause
- CTR < 0.5% -> pause (Meta)
- Spend > $50 AUD with no conversion -> pause

## Alerts

- Telegram (preferred, set up your own bot via `@BotFather`)
- Or Google Chat DM
- Or Email
