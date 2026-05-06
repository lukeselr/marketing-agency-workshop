# SETUP-PROMPT — Module 3 (Ads)

This is the **source of truth** for the prompt attendees paste into Claude Code in Module 3. The Notion page (`MODULE-3-NOTION.md`) embeds it inside a single fenced code block. Update this file first; copy the block into Notion second.

---

## The prompt (single block, copy verbatim)

```text
You are running Module 3 (Ads) of the Selr AI Workshop. The attendee already finished Module 1 (workshop kit). Your job is to install the marketing-agency skill and get them to Phase 1 baseline review without asking for technical input.

Run these steps in order. Stream output as it runs. Do not recap.

1. Clone the kit:
   git clone https://github.com/lukeselr/marketing-agency-workshop ~/marketing-agency-workshop

2. Install:
   bash ~/marketing-agency-workshop/install.sh
   This copies the skill to ~/.claude/skills/marketing-agency, installs Python deps, runs pre-flight, builds the ~/marketing/ dashboard folder, and wires every MCP (Playwright, Meta Ads, LinkedIn Ads, Gmail, Google Drive, ManyChat, GHL, Telegram, Notion, Slack, Google Sheets).

3. Ask the attendee one question, in plain English:
   "What's your business website? Paste the URL."

4. Trigger Phase 0 + Phase 1 against that URL:
   bash ~/.claude/skills/marketing-agency/scripts/run.sh <THEIR_URL>

5. When .state/business-baseline.md appears, render it and stop. Tell them:
   "Here is what we found about your business in 15 seconds from public sources. Anything wrong? Reply with corrections. Anything missing? Tell me. Otherwise say 'looks good' and we will move on to Phase 2 (strategy selection)."

Do not start Phase 2 until they confirm. Do not skip Phase 0 pre-flight. Surface the ~/marketing/ dashboard at the end of every action so they know where to look.
```

## Why this prompt is calibrated this way

- **Assumes Module 1 ran.** Claude Code is installed, the workshop kit is on disk, the user profile exists. We do not re-check those.
- **Stand-alone from Module 2.** No mention of `managed-agents-setup`. Module 3 works on a fresh Mac that finished only Module 1.
- **One human question.** "Paste your URL." Nothing else. The 5 lean private questions come later in Phase 1.4, not now.
- **Stops at baseline review.** The attendee eyeballs the auto-discovered profile before the orchestrator picks a strategy. This is the moment a real agency would stop and ask "have we got you right?".
- **Plain language only.** No "MCP", "Playwright", "Phase". Just verbs the attendee can follow.

## Acceptance test

Paste this into a fresh Claude Code session on a Mac that finished Module 1. Within 5 minutes wall clock the attendee should see a 6-card business profile, no terminal commands typed by hand, and a single question waiting for them.
