---
name: delegate-creative
description: Phase 7 creative generation. Delegates to ad-creative + content-engine + direct-response-copy + copywriting with voice-fingerprint.json + 6 firewall files. Returns 30+ voice-graded variants per platform.
---

## When to invoke
Phase 7 launch prep, weekly creative refresh from Phase 9.5 winners, or whenever owner says "make new ads".

## Context to pass
- `.state/voice-fingerprint.json` (verbatim)
- `.state/business-baseline.md` (current profile)
- `.state/profile.json` (5-question answers)
- 7 firewall rules embedded in `shared/voice-grade-config.json` (no em dashes, no refund promises, no personal-finance content, no outcome guarantees, no support promises, no drop-in invites, no fabricated facts)
- Target platform (meta/google/linkedin)

## Delegation
1. Task tool → `ad-creative` skill: generate 6 hooks × 3 angles × 2 CTAs = 36 combos
2. Task tool → `direct-response-copy`: tighten hooks for cold traffic
3. Task tool → `copywriting`: long-form ad body
4. Task tool → `content-engine`: 5-axis voice-grade each variant; reject < 8/10
5. Hard-fail any firewall hit; rewrite

## Read back
`.state/creatives/<platform>/<concept>.md` — top 30 ranked + scored
