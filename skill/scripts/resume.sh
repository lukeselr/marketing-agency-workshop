#!/usr/bin/env bash
# Resume from .state/. Looks at progress files, prints next step.
set -u
STATE="$HOME/.claude/skills/marketing-agency/.state"
echo "=== marketing-agency state ==="
for p in "$STATE"/*-progress.json; do
  [ -f "$p" ] || continue
  echo
  echo "$(basename "$p" -progress.json):"
  jq . "$p"
done
