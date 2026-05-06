---
name: delegate-ads-audit
description: Full 190-check paid-ads audit (Google/Meta/LinkedIn/TikTok/Microsoft). Replaces bare kill-rule monitor with health-score-driven recommendations.
---

## When to invoke
Weekly cron Sunday night before Phase 9.5 report.

## Context
- Active platforms from `~/.marketing-agency/tokens/`
- Pixel + conversion data
- 7-day spend window

## Delegation
1. `claude-ads/skills/ads-audit` — 190 checks, score 0-100
2. `claude-ads/skills/ads-budget` — 70/20/10 + 3x kill recommendations
3. `claude-ads/skills/ads-creative` — fatigue check
4. Aggregate into single health card

## Read back
`.state/ads-health-YYYY-WW.json` + summary feeds Phase 9.5 report.
