---
name: kill-rule-monitor
description: Phase 9 — daily perf monitor. Checks every active campaign, kills any breaking the rules in shared/conversion-events.json, alerts the user via Telegram or Google Chat.
---

Deployed in one of three modes (auto-picked based on `MARKETING_OS_INSTALLED` env): AWS server cron, macOS launchd, or Anthropic Routine cloud cron. Runs `scripts/kill-rule-monitor.py` once daily.
