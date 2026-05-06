---
name: connector-recommender
description: Picks the smallest set of MCP connectors + external skills the user actually needs based on their detected business profile. Wraps the global `connector-recommender` skill with marketing-agency context.
---

## When to invoke
Phase 2 (strategy selection). Once Phase 1 baseline + 5-question answers exist, before Phase 5 MCP installation.

## Context to pass
- `.state/business-baseline.md` — auto-discovered profile
- `.state/answers.json` — 5-question replies
- `.state/voice-fingerprint.json` (if Phase 1.5 ran)
- Available platforms detected in `~/.marketing-agency/tokens/`

## Delegation
1. Invoke the global `connector-recommender` skill via Skill tool.
2. Pass it the baseline + answers as a summary.
3. It returns a ranked list of connectors with rationale.

## Output contract
Write `.state/connector-plan.json`:
```json
{
  "version": 1,
  "tier_required": ["meta-ads", "google-ads", "ghl"],
  "tier_recommended": ["linkedin-ads", "manychat", "notion"],
  "tier_skip": ["tiktok-ads", "microsoft-ads"],
  "rationale": { "meta-ads": "Detected Meta pixel + AU paid mix points to Meta as #1", "..." : "..." },
  "external_skills": ["claude-ads/skills/ads-meta", "claude-ads/skills/ads-google", "ghl-crm", "ghl-landing-pages"]
}
```

## Read back
Phase 5 reads `connector-plan.json` and only installs the `tier_required` + `tier_recommended` MCPs. Phase 1 (post-onboard) external-skill resolver only fetches the `external_skills` list. Skips everything in `tier_skip`.

## Plain-English summary surfaced to owner
"Based on your business + answers, you need: <X> (must), <Y> (recommended), <Z> (skip for now). Connecting those now."
