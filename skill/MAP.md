# Marketing Agency — Skill Routing Map

When the user says X → load Y → invoke Z. Read this BEFORE jumping to a phase.

## Owner intent → phase + skill

| Owner says | Phase | Primary delegate(s) |
|---|---|---|
| "Set up my ads" / "Replace my marketing agency" | 0→8 (full first-run) | `run.sh` driver |
| "Run a fresh business profile" | 1 | `auto-discovery-orchestrator` agent |
| "Pick the right strategy" | 2 | `connector-recommender` + ads-strategy memory |
| "Connect Meta/Google/LinkedIn" | 3 | `platform-onboarder` agent → platforms/<platform>/setup.sh |
| "Install my pixels" / "Tracking" | 6 | `tracking-installer` + Microsoft Clarity heatmap |
| "Make me ads" / "Refresh creative" | 7 | **`delegate-creative`** |
| "Build my landing page" / "Improve conversion rate" | 6.5 | **`delegate-landing-page`** |
| "Launch the campaigns" | 8 | `platform-onboarder` (PAUSED), then owner approval |
| "Watch my campaigns" / "Kill bad ads" | 9 | `kill-rule-monitor` + **`delegate-ads-audit`** (190 checks) |
| "Send me a weekly report" | 9.5 | `weekly-report-orchestrator` |
| "Build my email follow-ups" / "Drip" | 10 | **`delegate-email-drip`** |
| "Build instant lead reply" / "SMS auto-reply" | 10 | **`delegate-sms-instant`** |
| "Build my content calendar" / "Organic posts" | 11 | **`delegate-organic-calendar`** |
| "Watch competitors" | 11/12 | **`delegate-competitor-watch`** |
| "Monthly strategy review" | 12 | `monthly-strategy-orchestrator` |
| "Audit my SEO" | (one-shot) | **`delegate-seo-audit`** |
| "Find me leads" / "Outbound" | (on demand) | **`delegate-lead-research`** |
| "Show me my numbers" / "Dashboard" | (any) | **`delegate-analytics-dashboard`** |

## External skill index (symlinked at `references/external/`)

39 skills available locally. Highest-value:
- `claude-ads/` — 12 sub-skills, 190-check audit, full media-buying playbook
- `claude-seo/` — 12 SEO sub-skills
- `ad-creative`, `content-engine`, `direct-response-copy`, `copywriting` — creative stack
- `ghl-landing-pages`, `framer-builder`, `vercel-deployment` — page builders
- `email-sequence`, `email-marketing`, `sms-blast`, `manychat` — lifecycle stack
- `ghl-crm`, `ghl-browser` — CRM ops
- `social-orchestrator`, `social-content`, `carousel-generator`, `instagram-automation`, `linkedin-automation` — organic stack
- `competitive-cartographer`, `apify-competitor-intelligence`, `apify-market-research`, `apify-content-analytics` — intel stack
- `analytics-product`, `notion-automation`, `googlesheets-automation`, `slack-automation` — reporting stack
- `lead-research-assistant`, `deep-research`, `last30days` — research stack
- `humanizer`, `avoid-ai-writing` — voice firewall stack

## Always-on hard rules
1. PAUSED on launch. Always.
2. 6 firewall rules on every owner-visible asset (no em dashes, no refunds, no finance, no outcome guarantees, no support promises, no drop-in invites).
3. Voice fingerprint enforced via 5-axis critic (`shared/voice-grade-config.json`).
4. Tokens stored mode 600 at `~/.marketing-agency/tokens/`.
