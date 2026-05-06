---
name: delegate-analytics-dashboard
description: Phase 9.5 numbers source. PostHog/Mixpanel/GA4 dashboards with funnel + retention + ROAS by channel.
---

## When to invoke
Phase 9.5 report builder calls this every Monday.

## Context
- All connected platforms
- Conversion taxonomy from `shared/conversion-events.json`

## Delegation
1. `analytics-product` — pull metrics (PostHog/Mixpanel/GA4 as available)
2. Compute MQL/SQL/CAC/LTV proxies
3. Compare last 7d vs prior 7d

## Read back
`.state/analytics-snapshot-YYYY-WW.json` for weekly report consumption.
