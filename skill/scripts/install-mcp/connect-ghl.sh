#!/usr/bin/env bash
# Connect ghl MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="ghl"
if mcp_exists "ghl-official"; then
  green "ghl MCP already configured"
  exit 0
fi
yellow "ghl: Claude Desktop has 'ghl-official' + 'ghl-community' connectors. Enable in Settings → Connectors. No CLI install."
