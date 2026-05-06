---
name: delegate-landing-page
description: Phase 6.5 landing page generation. Detects host (Framer/GHL/Vercel/Shopify/Webflow/WP) and delegates to the matching builder skill, generates voice-graded copy + A/B variants, installs heatmap + speed audit.
---

## When to invoke
After Phase 6 (tracking installed) when owner has an active campaign needing a converting LP.

## Context
- `.state/scrape/dns-host.json` for host hint
- `.state/voice-fingerprint.json`
- Campaign objective from `.state/strategy-selection.json`
- Top creative from `.state/creatives/`

## Delegation
| Host | Skill |
|---|---|
| framer | `framer-builder` |
| ghl | `ghl-landing-pages` |
| vercel/netlify | manual HTML via `templates/landing-page-skeleton.html.tmpl` + `vercel-deployment` |
| wordpress/shopify | snippet via `install-tracking.py` injection pattern |
| custom | raw HTML hand-off, owner pastes |

Then:
1. `direct-response-copy` for hero + sub + CTA
2. `copywriting` for proof + FAQ
3. `content-engine` voice-grade
4. Inject Microsoft Clarity heatmap snippet
5. Run PageSpeed Insights API check, surface blockers

## Read back
`.state/landing/<campaign>/index.html` + `.state/landing/<campaign>/variants.json`
