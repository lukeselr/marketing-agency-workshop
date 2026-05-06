# MODULE-3-NOTION — Source of truth for the Notion page

This is the canonical Markdown for the Module 3 (Ads) Notion page used in the workshop. The live Notion page mirrors this file exactly. To update the prompt, edit `SETUP-PROMPT.md` first, then propagate the code block here, then push to Notion via `mcp__claude_ai_Notion__notion-update-page`.

Layout matches Module 2 (Build Your First AI Automations) for consistency: whiteboard link → 1-paragraph intro → ASCII diagram → step 1 prompt → industry examples → safeguards → troubleshooting → links.

---

> **Whiteboard for this module** → [Open the live whiteboard](https://link.excalidraw.com/l/UPyKNqBGvl/8GxoaRFlZj0)

This is where you stop fiddling with marketing agencies and start running real ad campaigns. By the end of this module you'll have **the marketing-agency skill installed** in Claude Code that, working with the workshop kit you already loaded in Module 1, lets you paste your business URL and get a real working ad agency deployed: voice-graded creative, paused-by-default safety, lead lifecycle drips, weekly reports, and a kill-rule monitor that pauses anything bleeding.

You don't have to think. Claude does the install. You paste your URL. Watch.

---

## How it actually works (the diagram)

```plain text
          You + workshop kit (installed in Module 1)
                       |
                       | paste the prompt
                       v
+---------------------------------------------+
|     marketing-agency installer              |
|  - copies skill into ~/.claude/skills/      |
|  - wires 11 MCPs (Meta, Google, LinkedIn,   |
|    Gmail, GHL, Notion, Telegram, etc)       |
|  - builds ~/marketing/ dashboard            |
+---------------------------------------------+
                       |
                       | paste your business URL
                       v
+---------------------------------------------+
|  Phase 0 + 1 (15 seconds, 100% free)        |
|  - 14 public-source scrapers in parallel    |
|  - business profile + tech stack            |
|  - active ads on Meta / Google / LinkedIn   |
|  - reviews, news, reputation, voice         |
+---------------------------------------------+
                       |
                       v
              YOU REVIEW THE PROFILE
            (the only checkpoint today)
                       |
                       | "looks good"
                       v
+---------------------------------------------+
|  Phase 2 - 12  (one hour to one day)        |
|  - strategy + budget                        |
|  - onboard Meta / Google / LinkedIn         |
|  - install conversion tracking              |
|  - 30+ voice-graded ad variants             |
|  - PAUSED launch + retargeting + lookalike  |
|  - lead lifecycle drips (SMS + email)       |
|  - landing page CRO + A/B test              |
|  - daily kill-rule monitor                  |
|  - weekly report (Mondays 7am AEST)         |
|  - monthly strategy deck (PDF + narration)  |
+---------------------------------------------+
                       |
                       v
                ~/marketing/ dashboard
       (you check it once a week, that's it)
```

**In one sentence**: you paste your business URL, Claude pulls 14 public sources in 15 seconds, shows you a 6-card profile, asks 5 lean questions only public data can't answer, then builds your full ad agency on top of the answers.

---

## Step 1 — Paste this prompt into Claude Code and walk away

Open Claude Code. Paste the entire block below into the prompt. Hit enter. Don't touch anything until it asks for your URL.

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

When it asks for your URL, paste it. When the 6-card profile lands, scan it, correct anything wrong, then say "looks good". Done.

---

## What you'll actually build today (by industry)

You don't pick from a menu of toy demos. The skill detects your industry from your website and picks from **19 lifecycle templates** wired with the right paid platforms, voice-graded creative, audience automation, and AU SPAM-Act-compliant lead drips. A few examples:

- **Coaches / consultants** — discovery-call SMS within 60 seconds, 6-step nurture drip, weekly content briefer from your top ad winners, monthly strategy review
- **Trades / services** — quote triage agent, missed-lead SMS-back, on-site booking flow, kill-rule monitor that pauses anything bleeding past $50 with no conversion
- **E-commerce** — abandoned-cart sequencer, retargeting + 1%/3%/5% lookalike audiences, landing-page A/B test, hashtag and best-time-to-post calendar
- **Local services** — hyperlocal Meta + Google ads with postcode targeting, instant SMS reply, Saturday no-show recovery, review-request automation
- **Cafe / gym / salon / dentist** — function/membership/booking-specific SMS templates, trial conversion drip, hot-lead Slack ping when score hits 7
- **Mortgage broker / financial planner / buyer's agent** — pre-approval-detection lead scoring, doc-checklist email sequence, named-spouse-aware nurture

Every campaign launches **PAUSED**. Nothing spends until you click activate.

---

## Built-in safeguards (you don't have to ask for these)

- **Paused by default** — every Meta / Google / LinkedIn campaign launches PAUSED. You approve before any activation.
- **Kill-rule monitor** — daily cron pauses anything bleeding (CPA > 3x target, CTR < 0.5%, $50 spend with no conversion). Auto-deployed in one of three modes (AWS server, macOS launchd, or Anthropic Routine cloud cron).
- **Voice firewall** — every owner-facing string passes through 7 firewall rules: no em dashes, no refund promises, no outcome guarantees, no support promises, no drop-in invites, no personal-finance leakage, no fabricated facts. Hard fail and rewrite, never silent strip.
- **AU SPAM Act compliance** — every email and SMS includes ABN, opt-out (reply STOP), physical address. 19 industry templates baked with this from day one.
- **Owner dashboard at ~/marketing/** — daily numbers, kill log, weekly archive, monthly deck. You only open Claude Code if `tasks-for-you.md` has something.
- **Cost cap is $0 baseline** — 14 free public-source scrapers (no Apify), free dev access on Meta + Google + LinkedIn, no third-party tooling fees. Ad spend is yours and entirely separate.

---

## If something breaks

- **`git: command not found`** → tell Claude in the same chat: "git is missing, install it for me." It will run `brew install git` (Mac), `sudo apt install git` (Linux), or `winget install Git.Git` (Windows).
- **`Permission denied`** on a script → tell Claude: "fix the script permissions and re-run." It will `chmod +x` the affected scripts.
- **Pre-flight reports a blocker** → tell Claude: "fix the pre-flight blocker." It reads the output and patches.
- **`/marketing-agency` doesn't appear after restart** → fully quit Claude Code (not just close the window) and reopen. The skill loads on fresh start.
- **Wrong industry detected** → tell Claude: "I'm not <X>, I'm a <Y>." The skill re-runs the detector and switches templates.
- **Anything else** → describe what happened in plain English. The skill is built to fix itself; just describe the problem.

---

## Links

- **Marketing-agency kit (public)** — [github.com/lukeselr/marketing-agency-workshop](https://github.com/lukeselr/marketing-agency-workshop)
- **Module 1 (workshop kit)** — see Module 1 for the prompt
- **Module 2 (build your first AI automations)** — see Module 2 for the prompt
- **Selr AI** — [workshop.selrai.com.au](https://workshop.selrai.com.au)

That's the module. Paste the prompt, paste your URL, get a real ad agency before lunch.

---

Selr AI Workshop · [workshop.selrai.com.au](https://workshop.selrai.com.au)
IG [@mr_heka](https://instagram.com/mr_heka) · YouTube [@mr_heka](https://youtube.com/@mr_heka) · IG [@selr__ai](https://instagram.com/selr__ai)
