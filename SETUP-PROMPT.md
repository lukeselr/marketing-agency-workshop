# SETUP-PROMPT — Module 3 (Ads)

This is the **source of truth** for the prompt attendees paste into Claude Code in Module 3. The Notion page (`MODULE-3-NOTION.md`) embeds it inside a single fenced code block. Update this file first; copy the block into Notion second.

The prompt is deliberately aggressive: attendees already have Claude Code, the workshop kit, and 86 skills loaded. They want to paste once and walk away. The prompt forbids confirmation questions and forces Claude to install + run end-to-end.

---

## The prompt (single block, copy verbatim)

```javascript
I'm in a Selr AI workshop. I have Claude Code installed, the workshop kit installed, and 86 skills loaded. Now I need you to install the marketing-agency skill and run it for me end-to-end without asking a single confirmation question. Your job is to get this done.

Here's exactly what to do, in order. Do not skip steps. Do not ask me which OS — detect it. Do not ask me where files are. Do not ask me to confirm anything. Just execute.

1. Detect my OS and home directory. Make sure ~/.claude/skills/ exists. If it doesn't, create it.

2. Make a temp working dir at /tmp/selrai-marketing-install (or the OS equivalent on Windows). Create it fresh.

3. Clone the public repo into the temp dir:
   git clone https://github.com/lukeselr/marketing-agency-workshop /tmp/selrai-marketing-install/marketing-agency-workshop

4. Run the installer. It copies the skill into ~/.claude/skills/marketing-agency, installs Python deps, runs pre-flight, builds my ~/marketing/ dashboard folder, wires every MCP (Playwright, Meta Ads, LinkedIn Ads, Gmail, Google Drive, ManyChat, GHL, Telegram, Notion, Slack, Google Sheets), and resolves external skill dependencies:
   bash /tmp/selrai-marketing-install/marketing-agency-workshop/install.sh

5. If a dependency is missing (git, python3, node, jq, rsync), install it via the system package manager: brew on Mac, apt on Linux, winget on Windows. Do not ask me first.

6. Once install is green, ask me ONE question, in plain English, and only one:
   "What's your business website? Paste the URL."

7. The moment I paste the URL, run:
   bash ~/.claude/skills/marketing-agency/scripts/run.sh <THE_URL>
   This kicks off Phase 0 + Phase 1: 14 free public-source scrapers in parallel (about 15 seconds total). They produce a 6-card business profile.

8. When .state/business-baseline.md exists, render it for me as plain English and stop. Tell me:
   "Here is what we found about your business in 15 seconds from public sources. Anything wrong? Reply with corrections. Anything missing? Tell me. Otherwise say 'looks good' and we will go to Phase 2 (strategy selection)."

9. Do not start Phase 2 until I confirm.

10. Clean up /tmp/selrai-marketing-install once install is done.

11. End with one short message:
    - "Skill installed. Dashboard at ~/marketing/."
    - "Next: paste your business URL above."

Rules — non-negotiable:
- Do not ask me for permission to read, write, clone, install, or run anything. Just do it.
- Do not stop and ask me clarifying questions. If you have to make a judgment call, make it and tell me what you chose afterwards.
- Do not summarise what you're "about to do" — just do the next step. Stream output.
- Do not show me long terminal output. Tell me in plain English what just happened.
- Do not use jargon. No "MCP", no "Playwright", no "Phase 0". Translate everything.
- The only stop is the baseline review (step 8). Everything else: execute.

Start now.
```

## Why this prompt is calibrated this way

- **Workshop context up front.** Claude Code is installed. Workshop kit is installed. 86 skills loaded. We do not re-check those.
- **One human checkpoint only.** After the 14-scraper baseline lands, the attendee eyeballs their auto-discovered profile. That's it. Everything else runs.
- **Plain language only.** Claude is forbidden from using "MCP", "Playwright", "Phase 0". The skill itself uses these words internally; the attendee never sees them.
- **Auto-install missing deps.** brew / apt / winget without asking. The attendee shouldn't be hand-installing git on a workshop floor.
- **Stop only at baseline.** Step 8 is the agency moment ("have we got you right?"). Phase 2 onwards waits.

## Acceptance test

Paste this into a fresh Claude Code session on a Mac that finished Module 1. Within 5 minutes wall clock the attendee should see a 6-card business profile, no terminal commands typed by hand, and a single question waiting for them.
