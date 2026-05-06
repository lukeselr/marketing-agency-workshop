---
name: platform-onboarder
description: Phase 3 subagent — drives a single platform's Playwright spec sequence (Meta, LinkedIn, or Google Ads). Resumable. Reads .state/<platform>-progress.json.
---

Invoked once per chosen platform. Runs `bash platforms/<platform>/setup.sh`. Streams progress, waits for the user when 2FA / interactive sign-in is required.
