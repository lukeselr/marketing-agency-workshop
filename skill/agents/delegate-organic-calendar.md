---
name: delegate-organic-calendar
description: Phase 11 organic content calendar. Repurposes paid-ad winners into LinkedIn / IG / FB / TikTok / X posts. 30 posts/month rolling.
---

## When to invoke
Phase 11 monthly run or after Phase 9.5 weekly report identifies a winner.

## Context
- Phase 9.5 last-week report with top 3 paid winners
- Voice fingerprint
- `apify-content-analytics` for best-time-to-post

## Delegation
1. `social-orchestrator` for cross-platform formatting
2. `carousel-generator` for IG carousels
3. `social-content` for short-form copy variations
4. `content-marketer` for SEO blog repurposing
5. Push to Notion calendar via `notion-automation`
6. Optional auto-publish via `instagram-automation` + `linkedin-automation`

## Read back
`.state/content-calendar.json` + Notion DB ID.
