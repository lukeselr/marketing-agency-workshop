#!/usr/bin/env bash
# Connect manychat MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="manychat"
if mcp_exists "manychat"; then
  green "manychat MCP already configured"
  exit 0
fi
KEY_FILE="$HOME/.marketing-agency/tokens/manychat.json"
if [ ! -f "$KEY_FILE" ]; then
  yellow "manychat: paste API key into $KEY_FILE first (jq pattern: {\"api_key\": \"...\"})."
  exit 0
fi
KEY=$(jq -r '.api_key // empty' "$KEY_FILE")
[ -n "$KEY" ] || { red "manychat api_key empty"; exit 1; }
mcp_add_uvx "manychat" "manychat-mcp" "--api-key" "$KEY"
green "manychat MCP added"
