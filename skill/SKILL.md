---
name: marketing-agency
description: "FULLY AUTONOMOUS marketing agency replacement for small business owners. Scrapes the user's business + competitors from public sources first (free, no Apify), confirms a draft profile, asks 5 lean private questions, then drives Playwright through Meta + Google + LinkedIn ad-account setup, conversion tracking install, creative generation (voice-graded), and PAUSED-by-default campaign launch. Use when user says: 'set up my ads', 'replace my marketing agency', 'launch ads for my business', 'audit my marketing'. User signs into each platform once, watches Playwright drive everything else."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, mcp__plugin_playwright_playwright__*, mcp__meta-ads__*, mcp__linkedin-ads__*, mcp__claude_ai_Gmail__*, mcp__claude_ai_Google_Drive__*
metadata:
  category: Marketing & Ads
  tags: [marketing, ads, meta, facebook, instagram, google, linkedin, autonomous, workshop]
  audience: workshop attendees + small business owners
  distribution: public attendee repo
  time-to-complete: 60-90 min user-touch, plus 1-5 days passive verification gauntlet
  cost-to-user: $0 baseline (LinkedIn Marketing API free + vetted; Meta + Google free dev access). Optional ad-spend separate.
  autonomy-bar: "User signs into each platform once. Maybe answers 5 private questions about budget + bottleneck. That is it."
  version: 2.1.1
  last_updated: 2026-05-07
---

# Marketing Agency — Fully Autonomous Multi-Platform Setup

> **The standard:** scrape-first, ask-second. Most info about a business is already public on the internet. The skill auto-discovers everything it can, then asks only for the truly non-discoverable. Then Playwright drives every dev-portal click, OAuth dance, scope tick, ID extraction, conversion-event creation, tracking-tag install, and PAUSED campaign creation across Meta + Google + LinkedIn.
>
> **Reference architecture:** `~/.claude/skills/server-setup/SKILL.md` (phase pattern) + `~/.claude/skills/xero-mcp-setup/SKILL.md` (Playwright DOM extraction + safe config merge) + `~/.claude/skills/ai-ops-architect/SKILL.md` (`.state/` persistence).
>
> **If Playwright MCP isn't available, STOP.** Same rule as xero-mcp-setup. Do not fall back to copy-paste API keys. Install Playwright MCP first.

---

## Autonomy Bar

| User DOES | User DOES NOT |
|---|---|
| Provide business URL (or name + city if no URL) | Type any API keys, Pixel IDs, Conversion Action IDs, Insight Tag Partner IDs |
| Confirm the auto-discovered profile (lean review) | Fill in business details Playwright can scrape |
| Sign into Meta + Google + LinkedIn once each | Click developer-portal buttons (Playwright clicks) |
| Answer 5 private questions (budget, bottleneck, competitors, comfort, existing accounts) | Fill in form fields (Playwright fills) |
| Approve PAUSED campaigns before activation | Generate creative copy (auto-generated, voice-graded, firewall-checked) |
| Possibly upload Business Verification docs (Meta, if high spend) | Read raw error messages (silent recovery) |

**If at any point you are about to ask the user to copy or paste a value, STOP.** Read the DOM directly via Playwright.

---

## How This Skill Works

User says any of:
- "Set up my ads"
- "Replace my marketing agency"
- "Launch ads for my business"
- "Audit my marketing"
- **"Install the marketing-agency skill from the zip in my Downloads folder..."** (Phase -1 bootstrap)

Agent runs phases below. The user experiences ~60-90 min of guided conversation with 4 main touchpoints:
1. URL provision (10 sec)
2. Profile confirmation (5 min)
3. 5 private questions (5 min)
4. Per-platform sign-ins (~5 min each × 3 platforms)
5. Per-PAUSED-campaign approval before activation

Everything else runs in background.

---

## Phase -1: Self-Install From Zip (Bootstrap)

Mirrors `xero-mcp-setup` Phase -1 verbatim. See `PHASES/-1-self-install.md`.

OS-aware: detects Mac/Linux vs Windows, unzips into `~/.claude/skills/marketing-agency/`, verifies SKILL.md present, continues to Phase 0 in same session.

---

## Phase 0: Pre-Flight Checks

Run before any user message. Fix silently where possible.

```bash
# Run scripts/check-preflight.sh
bash ~/.claude/skills/marketing-agency/scripts/check-preflight.sh
```

Verifies:
- Claude Code installed + healthy
- Node 18+ (install via brew/nvm if missing, no sudo where avoidable)
- jq, curl, git, gh CLI
- Python 3.10+
- Playwright MCP available in session (install from marketplace if missing → restart → resume)
- `~/.claude.json` exists or scaffold
- `~/.marketing-agency/` directory created (mode 700) for tokens + state
- Free scrape stack: `dig`, `whois`, `instaloader` (pip), `beautifulsoup4` (pip)
- NO Apify check (deliberately — free stack only)

If pre-flight fails, fix silently. Surface only blockers to user with plain-English explanation.

Detailed phase doc: `PHASES/00-pre-flight.md`.

---

## Phase 1: Auto-Discovery (Scrape-First, Ask-Second) — THE NEW HEART

This is the differentiator. Mirrors `~/projects/marketing-assets/linkedin-ads-launch-pack/research/VOICE-AND-ASSETS.md` extraction pattern but extends to 14+ parallel scrapers.

### Step 1.0: Single identity prompt

> "What's your business website URL? (Or business name + city if no website.)"

### Step 1.1: Massive parallel auto-scrape (10-15 min, live progress streamed)

Dispatched via `agents/auto-discovery-orchestrator.md` (Task tool subagent):

| Source | Script | Cost |
|---|---|---|
| Website crawl + Wayback | `scripts/scrape/website.py` | FREE |
| DNS / host detection | `scripts/scrape/dns-host.py` | FREE |
| AU ABR business lookup | `scripts/scrape/abn-lookup.py` | FREE (gov't API) |
| Google Search press + listings | `scripts/scrape/google-search.py` | FREE (WebSearch tool) |
| Google Maps GMB | `scripts/scrape/google-maps.py` | FREE (Playwright) |
| Industry directories | `scripts/scrape/industry-directories.py` | FREE |
| LinkedIn company page | `scripts/scrape/linkedin-page.py` | FREE (unauth scrape) |
| Instagram public | `scripts/scrape/instagram-public.py` | FREE (instaloader) |
| Facebook page | `scripts/scrape/facebook-page.py` | FREE (Playwright) |
| Meta Ad Library | `scripts/scrape/meta-ad-library.py` | FREE (public, Playwright) |
| LinkedIn Ad Library | `scripts/scrape/linkedin-ad-library.py` | FREE (public, Playwright) |
| Google Ads Transparency | `scripts/scrape/google-ads-transparency.py` | FREE (public, Playwright) |
| Reviews aggregation | `scripts/scrape/reviews.py` | FREE (Playwright) |
| News mentions | `scripts/scrape/news-mentions.py` | FREE (Google News) |
| Cloud drives (consented) | `scripts/scrape/cloud-drives.py` | FREE (existing Drive MCP) |

`shared/progress-streamer.sh` emits live updates every 15 sec.

### Step 1.2: Synthesize draft profile

`scripts/synthesize.py` merges all scraper outputs into `business-baseline.md`.

### Step 1.3: Lean confirmation (6 expandable cards, not a 2000-word dump)

Show profile, user confirms or edits.

### Step 1.4: 5 private questions only

Budget · Bottleneck · Real competitors · Per-platform comfort · Existing-vs-new ad accounts.

### Step 1.5: Output 4 docs to `.state/`

`business-baseline.md`, `competitor-report.md`, `gap-analysis.md`, `voice-fingerprint.json`.

Detailed phase doc: `PHASES/01-auto-discovery.md`.

---

## Phase 2: Strategy Selection

Read `business-baseline.md` + `gap-analysis.md` + the 4 ads-strategy memory files (`ads-strategy-master-2026-05.md`, `ads-strategy-meta-2026-05.md`, `ads-strategy-linkedin-2026-05.md`, `ads-strategy-google-2026-05.md`).

Present 3 ranked options. User picks. Save to `.state/strategy-selection.json`.

Detailed phase doc: `PHASES/02-strategy-selection.md`.

---

## Phase 3: Per-Platform Account Setup (Playwright)

For each platform user selected, run that platform's sub-skill:

- **Meta:** `platforms/meta/SKILL.md` — Business Manager, Ad Account, System User, Pixel, CAPI Dataset, Lead Gen Form
- **Google Ads:** `platforms/google-ads/SKILL.md` — Cloud Project, Ads API, OAuth, Dev Token, MCC, Conversion Tracking
- **LinkedIn:** `platforms/linkedin/SKILL.md` — Dev App, Marketing API request, OAuth, Insight Tag, Lead Gen Form

Each platform sub-skill mirrors `xero-mcp-setup` Phase 2 pattern.

Detailed phase doc: `PHASES/03-account-setup.md`.

---

## Phase 4: Verification Gauntlet

Each platform has its own approval choke point. See `references/verification-troubleshooting.md` for rejection-recovery patterns.

While waiting, `templates/while-you-wait.md` engagement loop runs (write organic posts, prep creative, install tracking — all useful work that doesn't need API approval).

`scripts/poll-approvals.sh` runs every 12h via cron, checks Gmail for approval emails, advances state when approval arrives.

Detailed phase doc: `PHASES/04-verification-gauntlet.md`.

---

## Phase 5: MCP Installation

- Meta: `meta-ads-mcp` (registered)
- LinkedIn: `linkedin-ads` (registered, OAuth runs once Marketing API approved)
- Google Ads: install community MCP if available, else build thin wrapper at `~/mcp-servers/google-ads-mcp/`

Single batched restart of Claude Code at end of Phase 5 (not per-platform).

Detailed phase doc: `PHASES/05-mcp-installation.md`.

---

## Phase 6: Tracking Setup

`scripts/install-tracking.py` detects site host (Framer / Vercel / GHL / Webflow / WordPress / Shopify / Squarespace / GTM) and Playwright-drives the tag injection. Verifies firing via Chrome DevTools network filter.

Detailed phase doc: `PHASES/06-tracking-setup.md`.

---

## Phase 7: Creative Generation

Subagent `agents/creative-generator.md` delegates to existing skills (`content-engine` + `ad-creative` + `direct-response-copy` + `competitive-cartographer`) with `voice-fingerprint.json` from Phase 1.

Hard rules baked in (loaded from memory):
- `feedback_no_em_dashes.md`
- `feedback_no_refund_promises.md`
- `feedback_no_finance_in_marketing.md`
- `feedback_no_outcome_guarantees.md`
- `feedback_no_support_promises.md`
- `feedback_no_drop_in_invites.md`

Output: ~30 voice-graded variants per platform (image + video + document + TLA).

Detailed phase doc: `PHASES/07-creative-generation.md`.

---

## Phase 8: Launch (PAUSED by default)

Per platform: create campaigns + ad sets + ads via MCP, **status PAUSED**. Surface dashboard URLs. User approves via chat or Telegram before any activation. Never auto-active.

Detailed phase doc: `PHASES/08-launch.md`.

---

## Phase 9: Monitor & Optimize

Daily kill-rule cron auto-deployed in one of three modes (auto-detected):
- AWS server cron (operators with their own EC2 box)
- macOS `launchd` (attendees on Mac)
- Anthropic Routine cloud cron (Windows or no-server)

3x kill rule, CTR floor, frequency cap, weekly budget rebalance, Telegram notifications.

Detailed phase doc: `PHASES/09-monitor-and-optimize.md`.

---

## Reference Index — Load on Demand

| If user asks | Load |
|---|---|
| "How do you decide which platforms?" | `PHASES/02-strategy-selection.md` |
| "What if my LinkedIn API gets rejected?" | `references/verification-troubleshooting.md` |
| "What's actually firing on my site?" | `PHASES/06-tracking-setup.md` |
| "Show me Meta strategy details" | `references/meta-2026-state.md` (symlink to ads-strategy-meta-2026-05.md) |
| "Show me LinkedIn strategy details" | `references/linkedin-2026-state.md` |
| "Show me Google strategy details" | `references/google-2026-state.md` |
| "What's the master cross-platform playbook?" | `references/master-strategy.md` |

---

## Hard Rules (Apply Everywhere)

1. **Scrape-first, ask-second.** Don't ask the user for anything publicly discoverable.
2. **Never echo credentials.** API keys, Pixel IDs, tokens — never appear in user-visible output after capture.
3. **PAUSED by default.** Every campaign created PAUSED. User approves before any activation.
4. **All firewall rules apply** to creative copy: no em dashes, no refunds, no personal finance, no outcome guarantees, no support promises, no drop-in invites.
5. **No Apify, no paid scraping tools.** Free stack only — Playwright + Python libs + public ad libraries.
6. **Single batched restart of Claude Code** at end of Phase 5 (not per-platform).
7. **Voice-graded creative.** Every variant passes `content-engine` 5-axis critic with score ≥ 8/10.
8. **Manual fallback** documented per platform in `manual.md` with screenshots — but never the primary path.

---

## Setup Checklist (Agent Tracks)

Do NOT tell the user "done" before every box is ticked:

- [ ] Phase -1: skill installed at `~/.claude/skills/marketing-agency/`
- [ ] Phase 0: pre-flight green, Playwright MCP available
- [ ] Phase 1: 4 docs in `.state/`, profile user-confirmed, voice-fingerprint user-approved
- [ ] Phase 2: strategy-selection.json saved
- [ ] Phase 3: each selected platform credentialed (Playwright extracted, no copy-paste)
- [ ] Phase 4: pending approvals being polled, while-you-wait engagement active
- [ ] Phase 5: MCPs registered + single restart confirmed
- [ ] Phase 6: tags firing on user's site (verified via DevTools)
- [ ] Phase 7: ≥30 variants per platform, all voice-graded ≥ 8/10, all firewall-checked
- [ ] Phase 8: campaigns PAUSED, user-approved before activation
- [ ] Phase 9: kill-rule cron deployed in correct mode for the user's setup

---

## Version + Update

```bash
# Check current version
cat ~/.claude/skills/marketing-agency/VERSION

# Update to latest
bash ~/.claude/skills/marketing-agency/update.sh
```

Distribution: public attendee repo. Latest version on disk after running `install.sh`.

---


---

## v2.0 — Operate-half phases (added 2026-05-06)

| Phase | Name | When |
|---|---|---|
| 6.5 | Landing-page CRO | After Phase 6 tracking install |
| 9.5 | Weekly client report | Mondays 7am AEST cron |
| 10  | Lead lifecycle automation | After first leads land |
| 11  | Organic content calendar | Monthly + after weekly winners |
| 12  | Monthly strategy review | 1st of month, 8am AEST cron |

Each new phase has a doc in `PHASES/`, a script in `scripts/`, a delegate agent in `agents/`. See `MAP.md` for the full owner-intent → delegate routing table.

## Delegating to other skills

`marketing-agency` v2.0 is an orchestrator. The heavy lifting delegates to 39 external skills symlinked at `references/external/`. Highlights:
- `claude-ads/` (12 sub-skills, 190-check audit, full media-buying playbook)
- `claude-seo/` (12 SEO sub-skills)
- `ad-creative` + `content-engine` + `direct-response-copy` + `copywriting`
- `ghl-landing-pages` + `framer-builder` + `vercel-deployment`
- `email-sequence` + `email-marketing` + `sms-blast` + `manychat`
- `social-orchestrator` + `carousel-generator` + `instagram-automation` + `linkedin-automation`
- `competitive-cartographer` + `apify-competitor-intelligence`
- `analytics-product` + `notion-automation` + `googlesheets-automation` + `slack-automation`
- `lead-research-assistant` + `deep-research`

Read `MAP.md` for the full intent → delegate routing table.

## Owner dashboard at `~/marketing/`

After first run, every owner has:
- `~/marketing/this-week.md` — current numbers
- `~/marketing/pipeline.md` — CRM snapshot
- `~/marketing/reports/` — weekly + monthly archives
- `~/marketing/creatives/` — generated ad variants
- `~/marketing/calendar/this-month.md` — 30-post organic calendar
- `~/marketing/tasks-for-you.md` — only when human action needed

The owner doesn't need to open Claude Code unless `tasks-for-you.md` has something.

## Built By

Selr AI. Reference architecture: `xero-mcp-setup` (Playwright autonomy standard), `server-setup` (phase pattern), `ai-ops-architect` (`.state/` + intake → recommend → delegate).

If a platform's UI changes and DOM extraction breaks, see `selectors.json` per platform for selectors + `tested_on` date stamps. `scripts/selectors-version-check.sh` runs daily via GitHub Action and opens a PR when drift detected.
