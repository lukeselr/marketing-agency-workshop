#!/usr/bin/env bash
# Connect every MCP needed by marketing-agency. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
echo
echo "marketing-agency — connecting MCPs"
echo "==================================="
for s in playwright meta-ads linkedin-ads gmail google-drive manychat ghl telegram notion slack google-sheets; do
  echo
  echo "[$s]"
  bash "$DIR/connect-$s.sh" || true
done
echo
echo "Done. Restart Claude Code if any MCP was newly added."
