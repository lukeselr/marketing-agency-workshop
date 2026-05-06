# Phase 1 — Auto-Discovery

The new heart. Scrape-first onboarding.

## Step 1.0 — Single identity prompt
> "What's your business website URL?"

Fallback if no website: "What's your business name + city?"

## Step 1.1 — Massive parallel scrape

`bash scripts/discover.sh "<input>"` runs 14 free scrapers in parallel. ~10-15 min total.

## Step 1.2 — Synthesize

`scripts/synthesize.py` merges scraper outputs → `.state/business-baseline.md`.

## Step 1.3 — Show 6 cards (progressive disclosure)

Identity / Tech / Presence / Ads / Reputation / Pages. User confirms or edits. ~2 minutes.

## Step 1.4 — Lean 5 questions

Budget / bottleneck / real competitors / per-platform comfort / existing accounts. ~5 minutes.

## Step 1.5 — Output 4 docs

- `business-baseline.md` (confirmed)
- `competitor-report.md`
- `gap-analysis.md`
- `voice-fingerprint.json`
