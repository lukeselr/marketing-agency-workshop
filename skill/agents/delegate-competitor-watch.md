---
name: delegate-competitor-watch
description: Weekly competitor monitoring. Detects new ads, pricing changes, page launches.
---

## When to invoke
Weekly cron (Mondays before Phase 9.5 report) and on owner request.

## Context
- Top 3-5 competitors from Phase 1 baseline + owner-confirmed via 5 questions

## Delegation
1. `competitive-cartographer` for positioning shifts
2. `apify-competitor-intelligence` for ad-library deltas + pricing
3. `claude-ads/skills/ads-competitor` for media-buying signals
4. Compare against last week's snapshot in `.state/competitor-snapshots/`

## Read back
`.state/competitor-delta-YYYY-WW.md` — diffs only.
