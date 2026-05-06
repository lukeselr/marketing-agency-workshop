---
name: competitor-scraper
description: Deep-dive scraper for a specific competitor. Pulls active ads, pricing, page count, recent posts, social cadence. Loaded after Phase 1 baseline confirms top competitors.
---

Takes one competitor URL/handle. Runs the Phase 1 scrapers narrowed to that target plus Meta/LinkedIn/Google ad libraries. Writes `.state/competitors/<slug>.md`.
