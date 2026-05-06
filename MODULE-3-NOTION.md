# MODULE-3-NOTION — Source of truth for the Notion page

This is the canonical Markdown for the Notion page used in the workshop. The live Notion page mirrors this file exactly. To update the prompt, edit `SETUP-PROMPT.md` first, then propagate the code block here, then push to Notion via `mcp__claude_ai_Notion__notion-update-page`.

---

# Module 3 — Ads. Run a real marketing agency from your laptop.

Paste this prompt into Claude Code. It installs your ad agency, looks up your business from public sources, and shows you a 6-card profile in 15 seconds. You take it from there.

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

## What happens after you paste

- Claude clones the kit and installs the skill (about 3 minutes on a fresh Mac)
- You paste your business URL when asked
- You see your business profile pulled from 14 public sources in 15 seconds, plus 5 lean questions only public data cannot answer

---

Selr AI Workshop · [workshop.selrai.com.au](https://workshop.selrai.com.au)
IG [@mr_heka](https://instagram.com/mr_heka) · YouTube [@mr_heka](https://youtube.com/@mr_heka) · IG [@selr__ai](https://instagram.com/selr__ai)
