# Phase 3 — Per-platform Account Setup

Routes to `platforms/<platform>/setup.sh` per chosen platform.

- `platforms/meta/setup.sh` — 7 specs
- `platforms/linkedin/setup.sh` — 6 specs (3 + wait + 3 post-approval)
- `platforms/google-ads/setup.sh` — 7 specs

Serial per platform. Resumable via `.state/<platform>-progress.json`.
