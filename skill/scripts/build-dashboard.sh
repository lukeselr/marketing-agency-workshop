#!/usr/bin/env bash
# Create or refresh ~/marketing/ dashboard for the current owner.
set -u
DASH="$HOME/marketing"
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
mkdir -p "$DASH/reports" "$DASH/creatives" "$DASH/calendar" "$DASH/calendar/draft-posts"

# README
[ -f "$DASH/README.md" ] || cat > "$DASH/README.md" << 'EOR'
# Your Marketing Dashboard

This folder is your weekly agency view. Look here every Monday morning.

## Files

- `this-week.md` — current numbers (spend, leads, CPA, ROAS, ▲/▼ vs last week)
- `pipeline.md` — leads in your CRM, status, what to action
- `tasks-for-you.md` — only when human action needed (approve a campaign, etc)
- `reports/YYYY-WW.html` — weekly archive
- `reports/YYYY-MM-monthly.pdf` — monthly strategy decks
- `creatives/` — generated ad variants per platform
- `calendar/this-month.md` + `draft-posts/` — your organic content

## How it updates

Auto-refreshed by:
- Daily cron (kill-rule monitor) → updates `this-week.md`
- Monday 7am AEST → weekly report → `reports/`
- 1st of month 8am AEST → monthly strategy → `reports/`

## Run it manually

```bash
bash ~/.claude/skills/marketing-agency/scripts/weekly-report.py
bash ~/.claude/skills/marketing-agency/scripts/build-dashboard.sh
```
EOR

# Refresh this-week.md from latest .state/
TODAY=$(date +%Y-%m-%d)
WEEK=$(date +%Y-W%V)
cat > "$DASH/this-week.md" << EOR
# This week — $TODAY ($WEEK)

_Auto-refreshed. Run \`bash $SKILL_DIR/scripts/weekly-report.py\` for a full Monday report._

## Status
EOR

if [ -f "$SKILL_DIR/.state/business-baseline.md" ]; then
  NAME=$(grep -E "^# Business Baseline" "$SKILL_DIR/.state/business-baseline.md" | head -1 | sed 's/# Business Baseline: //')
  echo "- Business: **$NAME**" >> "$DASH/this-week.md"
fi

if [ -f "$SKILL_DIR/.state/profile.json" ]; then
  BUDGET=$(jq -r '.budget_aud_monthly // "not set"' "$SKILL_DIR/.state/profile.json")
  echo "- Monthly budget: **\$$BUDGET AUD**" >> "$DASH/this-week.md"
fi

# Pull last kill-rule actions if any
LOG="$SKILL_DIR/.state/kill-rule.log"
if [ -f "$LOG" ]; then
  KILLS=$(tail -7 "$LOG" 2>/dev/null | wc -l | tr -d ' ')
  echo "- Last 7 days: **$KILLS** auto-actions logged" >> "$DASH/this-week.md"
fi

cat >> "$DASH/this-week.md" << 'EOR'

## Top numbers

_Will populate after first weekly report runs (Monday 7am AEST). Manually run:_
```bash
bash ~/.claude/skills/marketing-agency/scripts/weekly-report.py
```

## What's working

- _(weekly report fills this in)_

## What got killed

- _(weekly report fills this in)_

## Next 3 actions

- _(weekly report fills this in)_
EOR

# tasks-for-you.md (only created if needed)
if [ ! -f "$DASH/tasks-for-you.md" ]; then
  cat > "$DASH/tasks-for-you.md" << 'EOR'
# Tasks for you

_Empty = nothing needs your attention. The skill will write here only when human action is required._

(no open tasks)
EOR
fi

# pipeline.md placeholder
[ -f "$DASH/pipeline.md" ] || cat > "$DASH/pipeline.md" << 'EOR'
# Pipeline

_Auto-pulled from GHL CRM by `delegate-analytics-dashboard`. Re-run:_
```bash
bash ~/.claude/skills/marketing-agency/scripts/weekly-report.py
```
EOR

echo "[ok] dashboard refreshed at $DASH"
ls "$DASH"
