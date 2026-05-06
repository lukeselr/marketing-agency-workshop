# Phase 6 — Tracking Setup

`scripts/install-tracking.py` writes `.state/tracking-plan.md`. Then `tracking-installer` agent dispatches to host-specific install:

- Framer → `framer-builder` skill
- GHL → `ghl-landing-pages` skill
- Vercel/Next.js → edit `app/layout.tsx`
- Shopify → `theme.liquid` head
- Custom → manual snippet paste

Verifies tags fire via `webapp-testing` skill. Phase complete only when all 3 tags green.
