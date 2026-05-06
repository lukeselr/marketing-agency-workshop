#!/usr/bin/env bash
# Emits live progress to stdout + appends to .state/discover.log.
# Used by discover.sh and any long-running phase orchestrator.
STATE_DIR="${MA_STATE_DIR:-$HOME/.claude/skills/marketing-agency/.state}"
LOG="$STATE_DIR/discover.log"
START_FILE="$STATE_DIR/.start_ts"
[ -f "$START_FILE" ] || date +%s > "$START_FILE"
START=$(cat "$START_FILE")
elapsed=$(( $(date +%s) - START ))
mins=$((elapsed / 60))
secs=$((elapsed % 60))
prefix=$(printf "[%dm%02ds]" "$mins" "$secs")
echo "$prefix $*" | tee -a "$LOG"
