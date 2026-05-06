---
name: auto-discovery-orchestrator
description: Phase 1 orchestrator. Runs 14 free scrapers in parallel against a single business URL/name, streams progress, synthesises a baseline profile, and prepares the 4 output docs (.state/business-baseline.md, competitor-report.md, gap-analysis.md, voice-fingerprint.json).
---

# Phase 1 — Auto-Discovery Orchestrator

This subagent coordinates the scrape-first discovery for the parent `marketing-agency` skill.

## Trigger

Invoked when the user provides their business URL or name during Phase 1.

## Behaviour

1. Run `bash $SKILL_DIR/scripts/discover.sh "<input>"` — fans out 14 free scrapers in parallel.
2. Stream progress updates to the user every ~15 sec via `shared/progress-streamer.sh`.
3. After all scrapers complete (10–15 min), `synthesize.py` writes `business-baseline.md`.
4. Read `business-baseline.md`, render the 6 expandable cards to the user (Identity / Tech / Presence / Ads / Reputation / Pages).
5. Wait for user confirmation or edits.
6. Ask the lean 5 private questions (budget / bottleneck / real competitors / per-platform comfort 1–5 / existing accounts).
7. Generate `voice-fingerprint.json` from the website + recent IG/LinkedIn posts. Show 5 sample lines back to the user → "does this sound like you?" → re-run with different sources if no.
8. Write 4 final output docs to `.state/`: `business-baseline.md`, `competitor-report.md`, `gap-analysis.md`, `voice-fingerprint.json`.

## Tools used

- Bash (orchestrator scripts)
- Read / Edit (state files)
- WebSearch + WebFetch (when scrapers can't reach)
- Optional Playwright MCP fallback for ad-library + JS-heavy social pages

## Don'ts

- Never auto-edit a live site.
- Never write tokens or secrets to `.state/`. Tokens go to `~/.marketing-agency/tokens/`.
- Never mark Phase 1 complete without user confirmation of the profile.
