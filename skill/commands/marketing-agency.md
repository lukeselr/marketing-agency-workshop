---
description: Run the marketing-agency skill — auto-detects state and suggests next phase
---

You are operating the `marketing-agency` skill at `~/.claude/skills/marketing-agency/`.

## Step 1: Detect state
Read `~/.claude/skills/marketing-agency/.state/` to determine where the user is:
- No `.state/business-baseline.md` → first-run mode (Phase 0+1)
- Baseline exists, no `.state/profile.json` → ask 5 questions (Phase 1.4)
- Profile exists, no platform tokens at `~/.marketing-agency/tokens/` → Phase 3 onboarding
- Tokens exist, no `.state/launches.log` → Phase 7 + 8 (creative + launch)
- Already launched → present picker: weekly report / refresh creative / lead lifecycle / monthly strategy / new campaign

## Step 2: Greet + act
Lead with the user's business name (read from `.state/business-baseline.md`) if known, else: "What's your business website URL or name?"

For first-run: kick off `bash ~/.claude/skills/marketing-agency/scripts/run.sh <URL>` and stream the progress to the user.

For subsequent runs: present a numbered picker of next-step phases. User picks. Drive that phase via the matching script in `scripts/`.

## Step 3: Hard rules
- Read `~/.claude/skills/marketing-agency/MAP.md` to route owner intents to the right delegate agent
- Never skip Phase 0 pre-flight on a new machine
- Always show what's about to happen before running it
- Surface the `~/marketing/` dashboard at end of every action so the owner knows where to look

## Step 4: Show the dashboard
After every command, print:

```
Your dashboard:  ~/marketing/
   - this-week.md   — current numbers
   - tasks-for-you.md — anything that needs you
   - reports/       — weekly + monthly archives
```
