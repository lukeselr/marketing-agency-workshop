# marketing-agency v2.0

A Claude Code skill that replaces a real $5–20k/mo marketing agency for an SMB owner.

## What it does

**Setup half (Phases 0-8)** — auto-discover business profile, voice fingerprint, drive Meta/LinkedIn/Google Ads onboarding via Playwright, install tracking, generate 30+ voice-graded ad variants per platform, launch PAUSED campaigns.

**Operate half (Phases 9-12)** — weekly client report, lead lifecycle automation (instant SMS/email + drips), landing-page CRO + A/B tests, organic content calendar, monthly strategy review with PDF deck, daily kill-rule monitor.

**Orchestrator** — delegates to 39 specialised skills (12 from `claude-ads`, 12 from `claude-seo`, plus Selr's `ad-creative` / `ghl-landing-pages` / `framer-builder` / `email-sequence` / `sms-blast` / `social-orchestrator` / `analytics-product` / etc) instead of re-implementing them.

## Install

```bash
# Mac/Linux
bash install.sh

# Windows
pwsh install.ps1
```

This auto-installs Python deps, runs pre-flight, builds your `~/marketing/` dashboard, and wires every MCP (Playwright, Meta Ads, LinkedIn Ads, Gmail, Google Drive, ManyChat, GHL, Telegram, Notion, Slack, Google Sheets).

## Use

In Claude Code:

```
/marketing-agency
```

State-aware: first run goes to Phase 0+1 discovery. Subsequent runs show a picker.

Or directly:

```bash
bash scripts/run.sh https://your-business.com.au
```

## Owner dashboard

Every owner gets `~/marketing/`:

```
~/marketing/
├── this-week.md          ← current numbers (auto-refreshed daily)
├── pipeline.md           ← CRM snapshot
├── reports/2026-W19.html ← weekly + monthly archives
├── creatives/            ← generated ad variants
├── calendar/this-month.md ← 30-post organic calendar
└── tasks-for-you.md      ← only when human action needed
```

The owner doesn't open Claude Code unless `tasks-for-you.md` has something.

## What's automated (cron-deployed)

- **Daily** — `kill-rule-monitor`: pauses campaigns bleeding, refreshes `~/marketing/this-week.md`
- **Mondays 7am AEST** — `weekly-report`: full one-page client report → email + Telegram + Notion
- **1st of month 8am AEST** — `monthly-strategy`: 4-week trend, wedge re-eval, 70/20/10 budget rebalance, 3 next-30-day bets, PDF deck

## Routing

`MAP.md` shows the owner-intent → delegate-skill table. Examples:

- "Make new ads" → `delegate-creative` (ad-creative + content-engine + direct-response-copy)
- "Build me a landing page" → `delegate-landing-page` (claude-ads/ads-landing + framer-builder OR ghl-landing-pages)
- "Drip my leads" → `delegate-email-drip` (email-sequence + email-marketing)
- "Audit my ads" → `delegate-ads-audit` (190 checks from claude-ads/ads-audit)
- "Find me 50 leads" → `delegate-lead-research` (lead-research-assistant + apify-market-research)

## Hard rules

- All campaigns launched **PAUSED**. Never auto-active.
- 6 firewall rules on every owner-visible asset (no em dashes / refunds / personal finance / outcome guarantees / support promises / drop-in invites)
- 5-axis voice critic on every variant; min score 8/10
- Tokens at `~/.marketing-agency/tokens/<platform>.json` mode 600. Never committed.
- `~/marketing/` is owner-readable. `.state/` is internal scratch.

## Distribution

Public attendee repo. Workshop drop. Updates land via `bash update.sh`.

## License

MIT for the wrapper. Underlying skills carry their own.

## Quickstart video

3-min walkthrough script: `docs/quickstart-video.md`
