---
name: tracking-installer
description: Phase 6 — drives Pixel + Insight Tag + Google Ads conversion install on the user's site. Routes to host-specific skill (framer-builder / ghl-landing-pages / vercel-deployment / etc).
---

Runs `python scripts/install-tracking.py` first, reads `.state/tracking-plan.md`, then dispatches to the correct host skill. Verifies tags are firing via `webapp-testing` skill before marking phase complete.
