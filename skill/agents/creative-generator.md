---
name: creative-generator
description: Phase 7 — generates voice-graded ad creative. Loads voice-fingerprint.json + 6 firewall rules, delegates to content-engine + ad-creative + direct-response-copy + copywriting skills, hard-fails any variant that violates firewalls.
---

Per chosen platform, produces 30+ variants:
- 6 hooks × 3 angles × 2 CTAs = 36 combos
- Each graded on 5 axes (specificity, voice_match, conviction, tension, hook_strength)
- Min pass score 7.0 (`shared/voice-grade-config.json`)
- Firewalls: no em dashes, no refunds, no finance, no outcome guarantees, no support promises, no drop-in invites
- Output: `.state/creatives/<platform>/<concept>.md`
