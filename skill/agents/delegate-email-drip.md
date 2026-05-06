---
name: delegate-email-drip
description: Phase 10 lead drip sequences. Delegates to email-sequence + email-marketing for day-0/1/3/7/14/30 nurture in user's voice with 6 firewall rules enforced.
---

## When to invoke
Phase 10 deploy, or when owner says "build my email follow-ups".

## Context
- Voice fingerprint, profile, industry from baseline
- Pick template from `templates/lifecycle-sequences/<industry>.json`

## Delegation
1. `email-sequence`: 6-step sequence skeleton (day 0/1/3/7/14/30)
2. `email-marketing`: HTML rendering for GHL deployment
3. `content-engine`: voice-grade
4. `humanizer` + `avoid-ai-writing`: pass each draft
5. Deploy via `ghl-crm` → workflow + email steps (status DRAFT)

## Read back
`.state/lifecycle/email-drip.json` with 6 drafts ready for owner approval.
