#!/usr/bin/env bash
# Engineer-audit fix: detect if platform UIs have shifted since selectors.json was tested_on.
# Compares tested_on to today; warns if older than 30 days.
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
today=$(date +%Y-%m-%d)
warn_days=30
exit_status=0
for sel in "$SKILL_DIR"/platforms/*/selectors.json; do
  [ -f "$sel" ] || continue
  platform=$(basename "$(dirname "$sel")")
  tested=$(jq -r '.tested_on' "$sel")
  age_days=$(( ( $(date -j -f %Y-%m-%d "$today" +%s 2>/dev/null || date -d "$today" +%s) \
              - $(date -j -f %Y-%m-%d "$tested" +%s 2>/dev/null || date -d "$tested" +%s) ) / 86400 ))
  if [ "$age_days" -gt "$warn_days" ]; then
    echo "[warn] $platform selectors are $age_days days old (tested_on $tested) — re-run smoke test."
    exit_status=1
  else
    echo "[ok] $platform selectors $age_days days old"
  fi
done
exit "$exit_status"
