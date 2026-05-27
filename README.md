# Module 3 — Ads (Marketing Agency in a box)

> Part of the Selr AI Workshop. You should have finished Module 1 (Workshop Kit) before running this.

This is the kit attendees clone in Module 3. It installs the `marketing-agency` skill on your laptop. Once installed, type `/marketing-agency` in Claude Code and paste your business URL. Expect 60-90 minutes of hands-on setup (you sign in to Meta / Google / LinkedIn once each) plus 1-5 days of passive verification while the platforms approve dev access. After that you have a real ad agency replacement running locally — automatic business research, voice-graded creative, paid ads on Meta + Google + LinkedIn (PAUSED until you approve), lead lifecycle drips, weekly reports.

## What it does

- **Setup half** — auto-discover business profile from public sources, extract your voice, drive Meta + Google + LinkedIn ad-account setup via Playwright, install conversion tracking, generate 30+ voice-graded ad variants, launch PAUSED campaigns.
- **Operate half** — weekly client report (Mondays 7am), lead lifecycle automation (instant SMS + email + drip), landing-page CRO + A/B tests, organic content calendar, monthly strategy review with PDF deck, daily kill-rule monitor.
- **Orchestrator** — delegates to specialised skills already installed by Module 1 (`ad-creative`, `ghl-landing-pages`, `email-sequence`, `social-orchestrator`, etc) instead of re-implementing them.

## Install

### macOS / Linux

```bash
git clone https://github.com/lukeselr/marketing-agency-workshop /tmp/marketing-agency-workshop
bash /tmp/marketing-agency-workshop/install.sh
rm -rf /tmp/marketing-agency-workshop
```

### Windows

```powershell
git clone https://github.com/lukeselr/marketing-agency-workshop $env:TEMP\marketing-agency-workshop
pwsh $env:TEMP\marketing-agency-workshop\install.ps1
Remove-Item -Recurse -Force $env:TEMP\marketing-agency-workshop
```

The installer copies the skill into `~/.claude/skills/marketing-agency/`, runs Phase 0 pre-flight, builds your `~/marketing/` dashboard folder, and wires every MCP (Playwright, Meta Ads, LinkedIn Ads, Gmail, Google Drive, ManyChat, GHL, Telegram, Notion, Slack, Google Sheets).

## Use

In Claude Code:

```
/marketing-agency
```

State-aware: first run goes to Phase 0 + 1 discovery (about 15 seconds, 14 free public-source scrapers). Subsequent runs show a picker (weekly report, refresh creative, lead lifecycle review, monthly strategy, new campaign).

Or directly:

```bash
bash ~/.claude/skills/marketing-agency/scripts/run.sh https://your-business.com.au
```

## Owner dashboard

Every owner gets a `~/marketing/` folder in their home directory:

```
~/marketing/
|-- this-week.md          # current numbers (auto-refreshed daily)
|-- pipeline.md           # CRM snapshot
|-- reports/2026-W19.html # weekly + monthly archives
|-- creatives/            # generated ad variants
|-- calendar/this-month.md# 30-post organic calendar
+-- tasks-for-you.md      # only when human action needed
```

You don't need to open Claude Code unless `tasks-for-you.md` has something.

## What's automated

- **Daily** — `kill-rule-monitor`: pauses campaigns bleeding, refreshes `~/marketing/this-week.md`
- **Mondays 7am** — `weekly-report`: full one-page client report to email + Telegram + Notion
- **1st of month** — `monthly-strategy`: PDF deck + 5-min narration script
- **On every new lead** — instant SMS within 60 sec, email within 90 sec, 6-step drip starts, hot leads pinged via Slack

## Files in this repo

```
marketing-agency-workshop/
|-- README.md             # this file
|-- SETUP-PROMPT.md       # the source-of-truth Claude Code prompt
|-- MODULE-3-NOTION.md    # the source-of-truth Notion page content
|-- install.sh            # macOS / Linux installer
|-- install.ps1           # Windows installer
+-- skill/                # the marketing-agency skill itself (v2.1.1)
```

## Costs

Zero baseline. The skill ships free:
- LinkedIn Marketing Developer Platform (free, vetted)
- Meta Ads developer access (free)
- Google Ads developer access (free)
- 14 public-source scrapers (no Apify, no third-party costs)

Ad spend is separate and entirely up to you. The skill launches every campaign PAUSED, so nothing spends until you approve.

## Support

This is unsupported community software. For paid support, attend the workshop or join the community at [workshop.selrai.com.au](https://workshop.selrai.com.au).

## Licence

MIT (`LICENSE.md`). The skill bundles or depends on Playwright (Apache 2.0), jq (MIT), BeautifulSoup4 (MIT), instaloader (MIT), google-ads-python (Apache 2.0, optional), requests (Apache 2.0). Their licences carry through.
